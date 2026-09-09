"""Verify pinned installation with controlled archives and network responses."""

import hashlib
import io
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError
from urllib.request import Request
import zipfile

from tools import install_hook_tools as installer


class DownloadResponse(io.BytesIO):
    def geturl(self):
        return "https://release-assets.githubusercontent.com/synthetic-archive"


def release_archive(kind="tar", *, name=None, file_type="regular", duplicate=False):
    content = io.BytesIO()
    binary = b"synthetic executable fixture; never executed\n"
    binary_name = "gitleaks.exe" if kind == "zip" else "gitleaks"
    member_name = name or binary_name
    if kind == "zip":
        with zipfile.ZipFile(content, "w") as archive:
            entry = zipfile.ZipInfo(member_name)
            entry.create_system = 3
            entry.external_attr = ((stat.S_IFLNK if file_type == "symlink" else stat.S_IFREG) | 0o755) << 16
            archive.writestr(entry, binary)
            archive.writestr("../outside.txt", b"must never be extracted")
    else:
        with tarfile.open(fileobj=content, mode="w:gz") as archive:
            for _ in range(2 if duplicate else 1):
                entry = tarfile.TarInfo(member_name)
                if file_type == "symlink":
                    entry.type = tarfile.SYMTYPE
                    entry.linkname = "../outside.txt"
                    archive.addfile(entry)
                else:
                    entry.size = len(binary)
                    archive.addfile(entry, io.BytesIO(binary))
            unrelated = tarfile.TarInfo("../outside.txt")
            unrelated.size = 5
            archive.addfile(unrelated, io.BytesIO(b"never"))
    raw = content.getvalue()
    asset = installer.ReleaseAsset(
        "synthetic.zip" if kind == "zip" else "synthetic.tar.gz",
        hashlib.sha256(raw).hexdigest(), len(raw),
    )
    return raw, asset, binary


class InstallHookToolsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="template-scanner-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def archive_file(self, raw):
        archive = self.root / "release.archive"
        archive.write_bytes(raw)
        return archive

    def existing_binary(self, asset):
        binary = self.root / ".tools/bin" / asset.binary_name
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_bytes(b"existing binary must survive failure")
        return binary

    def test_six_platform_assets_and_aliases_are_selected(self):
        for system in ("Linux", "Darwin", "Windows"):
            for machine, architecture in (("x86_64", "x64"), ("AMD64", "x64"),
                                          ("aarch64", "arm64"), ("arm64", "arm64")):
                with self.subTest(system=system, machine=machine), \
                     patch.object(installer.platform, "system", return_value=system), \
                     patch.object(installer.platform, "machine", return_value=machine):
                    asset = installer.current_asset()
                    self.assertEqual(asset, installer.RELEASE_ASSETS[(system, architecture)])
                    self.assertRegex(asset.sha256, r"^[0-9a-f]{64}$")
                    self.assertTrue(asset.url.startswith("https://github.com/gitleaks/gitleaks/"))

    def test_unsupported_platform_fails_before_download(self):
        with patch.object(installer.platform, "system", return_value="Unsupported"), \
             patch.object(installer, "download_archive") as download:
            with self.assertRaises(installer.InstallError):
                installer.install_gitleaks(self.root)
        download.assert_not_called()

    def test_verified_tar_and_zip_replace_only_the_expected_binary(self):
        for kind in ("tar", "zip"):
            with self.subTest(kind=kind):
                raw, asset, expected = release_archive(kind)
                existing = self.existing_binary(asset)
                with patch.object(installer, "current_asset", return_value=asset), \
                     patch.object(installer.subprocess, "run") as run:
                    run.return_value = subprocess.CompletedProcess([], 0, installer.GITLEAKS_VERSION + "\n", "")
                    installed = installer.install_gitleaks(self.root, self.archive_file(raw))
                self.assertEqual(installed, existing)
                self.assertEqual(installed.read_bytes(), expected)
                self.assertEqual(run.call_args.args[0][1:], ["version"])
                self.assertEqual(Path(run.call_args.args[0][0]).name, asset.binary_name)
                self.assertNotIn("shell", run.call_args.kwargs)
                self.assertFalse((self.root / "outside.txt").exists())
                self.assertFalse(list(installed.parent.glob(".gitleaks-install-*")))
                if os.name != "nt":
                    self.assertTrue(installed.stat().st_mode & stat.S_IXUSR)

    def test_wrong_checksum_or_size_never_executes_or_replaces_binary(self):
        raw, asset, _ = release_archive()
        existing = self.existing_binary(asset)
        before = existing.read_bytes()
        for content in (b"x" * len(raw), raw[:-1], raw + b"x"):
            with self.subTest(size=len(content)), \
                 patch.object(installer, "current_asset", return_value=asset), \
                 patch.object(installer.subprocess, "run") as run:
                with self.assertRaises(installer.InstallError):
                    installer.install_gitleaks(self.root, self.archive_file(content))
                run.assert_not_called()
                self.assertEqual(existing.read_bytes(), before)

    def test_malformed_archive_cannot_replace_binary(self):
        raw = b"not an archive, even with a matching controlled test digest"
        asset = installer.ReleaseAsset("fixture.tar.gz", hashlib.sha256(raw).hexdigest(), len(raw))
        existing = self.existing_binary(asset)
        before = existing.read_bytes()
        with patch.object(installer, "current_asset", return_value=asset), \
             patch.object(installer.subprocess, "run") as run:
            with self.assertRaises(installer.InstallError):
                installer.install_gitleaks(self.root, self.archive_file(raw))
        run.assert_not_called()
        self.assertEqual(existing.read_bytes(), before)

    def test_missing_duplicate_and_symlink_binary_members_are_rejected(self):
        cases = (
            {"name": "../gitleaks"}, {"duplicate": True}, {"file_type": "symlink"},
            {"kind": "zip", "file_type": "symlink"},
        )
        for options in cases:
            with self.subTest(options=options):
                raw, asset, _ = release_archive(**options)
                with patch.object(installer, "current_asset", return_value=asset), \
                     patch.object(installer.subprocess, "run") as run:
                    with self.assertRaises(installer.InstallError):
                        installer.install_gitleaks(self.root, self.archive_file(raw))
                run.assert_not_called()

    def test_oversized_uncompressed_binary_is_rejected(self):
        raw, asset, _ = release_archive()
        with patch.object(installer, "current_asset", return_value=asset), \
             patch.object(installer, "MAX_BINARY_BYTES", 10), \
             patch.object(installer.subprocess, "run") as run:
            with self.assertRaises(installer.InstallError):
                installer.install_gitleaks(self.root, self.archive_file(raw))
        run.assert_not_called()

    def test_failed_version_check_preserves_existing_binary_and_cleans_staging(self):
        raw, asset, _ = release_archive()
        existing = self.existing_binary(asset)
        before = existing.read_bytes()
        for result in (subprocess.CompletedProcess([], 0, "0.0.0\n", ""),
                       subprocess.CompletedProcess([], 1, installer.GITLEAKS_VERSION, "")):
            with self.subTest(result=result.returncode), \
                 patch.object(installer, "current_asset", return_value=asset), \
                 patch.object(installer.subprocess, "run", return_value=result):
                with self.assertRaises(installer.InstallError):
                    installer.install_gitleaks(self.root, self.archive_file(raw))
                self.assertEqual(existing.read_bytes(), before)
                self.assertEqual(list(existing.parent.iterdir()), [existing])

    def test_destination_symlinks_never_write_or_execute_external_content(self):
        raw, asset, _ = release_archive()
        archive = self.archive_file(raw)
        outside = self.root / "outside"
        outside.mkdir()
        for relative in (".tools", ".tools/bin", ".tools/bin/gitleaks"):
            with self.subTest(destination=relative):
                fixture = self.root / relative.replace("/", "-")
                fixture.mkdir()
                link = fixture / relative
                link.parent.mkdir(parents=True, exist_ok=True)
                try:
                    link.symlink_to(outside, target_is_directory=True)
                except (OSError, NotImplementedError) as error:
                    self.skipTest(f"Symlink creation unavailable: {type(error).__name__}")
                with patch.object(installer, "current_asset", return_value=asset), \
                     patch.object(installer.subprocess, "run") as run:
                    with self.assertRaises(installer.InstallError):
                        installer.install_gitleaks(fixture, archive)
                run.assert_not_called()
                self.assertEqual(list(outside.iterdir()), [])

    def test_download_size_limit_is_enforced_before_installation(self):
        raw, asset, _ = release_archive()
        with patch.object(installer, "build_opener") as opener:
            opener.return_value.open.return_value = DownloadResponse(raw + b"extra")
            with self.assertRaisesRegex(installer.InstallError, "pinned size"):
                installer.download_archive(asset)

    def test_download_deadline_is_enforced(self):
        raw, asset, _ = release_archive()
        with patch.object(installer, "build_opener") as opener, \
             patch.object(installer.time, "monotonic", side_effect=[0, 31]):
            opener.return_value.open.return_value = DownloadResponse(raw)
            with self.assertRaisesRegex(installer.InstallError, "time limit"):
                installer.download_archive(asset)

    def test_verified_download_uses_https_and_socket_timeout(self):
        raw, asset, _ = release_archive()
        with patch.object(installer, "build_opener") as opener:
            opener.return_value.open.return_value = DownloadResponse(raw)
            self.assertEqual(installer.verified_archive(asset, None), raw)
        self.assertEqual(opener.return_value.open.call_args.args[0].full_url, asset.url)
        self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 10)

    def test_https_redirect_cannot_downgrade_to_http(self):
        handler = installer.HTTPSRedirectHandler()
        with self.assertRaises(installer.InstallError):
            handler.redirect_request(
                Request("https://github.com/fixture"), None, 302, "Found", {},
                "http://example.invalid/archive",
            )

    def test_download_failure_has_no_raw_url_in_cli_diagnostic(self):
        with patch.object(installer, "ROOT", self.root), \
             patch.object(installer, "download_archive", side_effect=URLError("sensitive-signed-url")), \
             patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(installer.main([]), 1)
        self.assertNotIn("sensitive-signed-url", stderr.getvalue())
        self.assertIn("installation failed", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
