"""Install the pinned Gitleaks release; Ruff comes from requirements-dev.txt."""

import argparse
from dataclasses import dataclass
import hashlib
import io
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import zipfile


ROOT = Path(__file__).resolve().parents[1]
GITLEAKS_VERSION = "8.30.1"
MAX_BINARY_BYTES = 64 * 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 30
SOCKET_TIMEOUT_SECONDS = 10
VERSION_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class ReleaseAsset:
    name: str
    sha256: str
    size: int

    @property
    def url(self) -> str:
        return (
            "https://github.com/gitleaks/gitleaks/releases/download/"
            f"v{GITLEAKS_VERSION}/{self.name}"
        )

    @property
    def binary_name(self) -> str:
        return "gitleaks.exe" if self.name.endswith(".zip") else "gitleaks"


# GitHub release API digests and sizes verified on 2026-09-09:
# https://api.github.com/repos/gitleaks/gitleaks/releases/tags/v8.30.1
RELEASE_ASSETS = {
    ("Linux", "x64"): ReleaseAsset(
        "gitleaks_8.30.1_linux_x64.tar.gz",
        "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb",
        8230402,
    ),
    ("Linux", "arm64"): ReleaseAsset(
        "gitleaks_8.30.1_linux_arm64.tar.gz",
        "e4a487ee7ccd7d3a7f7ec08657610aa3606637dab924210b3aee62570fb4b080",
        7601421,
    ),
    ("Darwin", "x64"): ReleaseAsset(
        "gitleaks_8.30.1_darwin_x64.tar.gz",
        "dfe101a4db2255fc85120ac7f3d25e4342c3c20cf749f2c20a18081af1952709",
        8359235,
    ),
    ("Darwin", "arm64"): ReleaseAsset(
        "gitleaks_8.30.1_darwin_arm64.tar.gz",
        "b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5",
        7897593,
    ),
    ("Windows", "x64"): ReleaseAsset(
        "gitleaks_8.30.1_windows_x64.zip",
        "d29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e",
        8438883,
    ),
    ("Windows", "arm64"): ReleaseAsset(
        "gitleaks_8.30.1_windows_arm64.zip",
        "b95f5e4f5c425cedca7ee203d9afd29597e692c4924a12ed42f970537c72cc0f",
        7701820,
    ),
}


class InstallError(ValueError):
    """Installation did not produce a verified replacement binary."""


def current_asset() -> ReleaseAsset:
    machine = platform.machine().lower()
    architecture = {
        "x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"
    }.get(machine)
    asset = RELEASE_ASSETS.get((platform.system(), architecture))
    if asset is None:
        raise InstallError("Supported platforms are Linux, macOS and Windows on x64 or arm64")
    return asset


class HTTPSRedirectHandler(HTTPRedirectHandler):
    max_redirections = 5

    def redirect_request(self, request, response, code, message, headers, new_url):
        if urlsplit(new_url).scheme != "https":
            raise InstallError("Release download attempted a non-HTTPS redirect")
        return super().redirect_request(request, response, code, message, headers, new_url)


def download_archive(asset: ReleaseAsset) -> bytes:
    """Bound transfer size and elapsed reads; never print signed redirect URLs."""
    request = Request(asset.url, headers={"User-Agent": "repository-hook-tools-installer"})
    deadline = time.monotonic() + DOWNLOAD_TIMEOUT_SECONDS
    chunks = []
    received = 0
    with build_opener(HTTPSRedirectHandler()).open(
        request, timeout=SOCKET_TIMEOUT_SECONDS
    ) as response:
        if urlsplit(response.geturl()).scheme != "https":
            raise InstallError("Release download did not use HTTPS")
        while True:
            if time.monotonic() >= deadline:
                raise InstallError("Release download exceeded its time limit")
            chunk = response.read1(min(65536, asset.size + 1 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > asset.size:
                raise InstallError("Release archive exceeds the pinned size")
    return b"".join(chunks)


def verified_archive(asset: ReleaseAsset, archive: Path | None) -> bytes:
    if archive is None:
        content = download_archive(asset)
    else:
        if not archive.is_file():
            raise InstallError("The local archive must be a regular file")
        with archive.open("rb") as source:
            content = source.read(asset.size + 1)
    if len(content) != asset.size:
        raise InstallError("Release archive size does not match the pinned release")
    if hashlib.sha256(content).hexdigest() != asset.sha256:
        raise InstallError("Release archive SHA-256 does not match the pinned release")
    return content


def extract_binary(content: bytes, asset: ReleaseAsset) -> bytes:
    """Read one exact regular member; never extract archive paths to disk."""
    if asset.name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            matches = [entry for entry in archive.infolist() if entry.filename == asset.binary_name]
            if len(matches) != 1:
                raise InstallError("Archive must contain exactly one expected Gitleaks binary")
            member = matches[0]
            file_type = stat.S_IFMT(member.external_attr >> 16)
            if member.is_dir() or file_type not in (0, stat.S_IFREG):
                raise InstallError("The archived Gitleaks binary must be a regular file")
            if not 0 < member.file_size <= MAX_BINARY_BYTES:
                raise InstallError("The archived Gitleaks binary exceeds its size limit")
            with archive.open(member) as source:
                binary = source.read(MAX_BINARY_BYTES + 1)
    else:
        with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as archive:
            matches = [entry for entry in archive if entry.name == asset.binary_name]
            if len(matches) != 1:
                raise InstallError("Archive must contain exactly one expected Gitleaks binary")
            member = matches[0]
            if not member.isfile() or member.sparse is not None:
                raise InstallError("The archived Gitleaks binary must be a regular file")
            if not 0 < member.size <= MAX_BINARY_BYTES:
                raise InstallError("The archived Gitleaks binary exceeds its size limit")
            with archive.extractfile(member) as source:
                binary = source.read(MAX_BINARY_BYTES + 1)
    if not binary or len(binary) > MAX_BINARY_BYTES:
        raise InstallError("The archived Gitleaks binary has an invalid size")
    return binary


def install_destination(root: Path, binary_name: str) -> Path:
    root = root.resolve(strict=True)
    destination = root / ".tools" / "bin" / binary_name
    for path in (destination.parent.parent, destination.parent, destination):
        if path.is_symlink() or path.is_junction():
            raise InstallError("Refusing a symlink or junction in the installation destination")
        if path.exists() and not (path.is_file() if path == destination else path.is_dir()):
            raise InstallError("The installation destination has an unexpected file type")
        if not path.resolve().is_relative_to(root):
            raise InstallError("The installation destination must remain inside the repository")
    return destination


def verify_binary_version(binary: Path) -> None:
    result = subprocess.run(
        [str(binary), "version"], capture_output=True, text=True,
        timeout=VERSION_TIMEOUT_SECONDS, check=False,
    )
    if result.returncode or result.stdout.strip() not in (GITLEAKS_VERSION, "v" + GITLEAKS_VERSION):
        raise InstallError("The verified release binary did not report the pinned Gitleaks version")


def install_gitleaks(root: Path, archive: Path | None = None) -> Path:
    """Always verify an archive; an existing version string is not provenance."""
    try:
        asset = current_asset()
        destination = install_destination(root, asset.binary_name)
        binary = extract_binary(verified_archive(asset, archive), asset)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".gitleaks-install-", dir=destination.parent) as staging:
            candidate = Path(staging) / asset.binary_name
            candidate.write_bytes(binary)
            candidate.chmod(0o755)
            verify_binary_version(candidate)
            # Recheck just before replacement. This is not a sandbox against
            # another process with permission to rewrite the same checkout.
            install_destination(root, asset.binary_name)
            os.replace(candidate, destination)
        return destination
    except (OSError, URLError, tarfile.TarError, zipfile.BadZipFile, RuntimeError,
            subprocess.SubprocessError, UnicodeError) as error:
        raise InstallError("Could not download, read or verify the Gitleaks release") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--archive", type=Path,
        help="Use a local release archive, still checked against the pinned platform digest",
    )
    arguments = parser.parse_args(argv)
    try:
        destination = install_gitleaks(ROOT, arguments.archive)
    except InstallError as error:
        print(f"Gitleaks installation failed: {error}", file=sys.stderr)
        return 1
    print(f"Installed Gitleaks {GITLEAKS_VERSION}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
