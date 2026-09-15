"""Locked append-only audit records; external checkpoints are still required."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import time


class LedgerError(ValueError):
    """Audit persistence or integrity could not be established."""


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


@contextmanager
def locked(path: Path, max_bytes: int = 8_388_608):
    """Serialize readers and appends without ever truncating the ledger."""
    if any(part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction())
           for part in (path, *path.parents)) or (path.exists() and path.stat().st_nlink != 1):
        raise LedgerError("Ledger links are prohibited")
    if not path.parent.is_dir():
        raise LedgerError("Ledger directory must be provisioned before hook invocation")
    lock_path = path.with_suffix(path.suffix + ".lock")
    if lock_path.is_symlink() or (lock_path.exists() and lock_path.stat().st_nlink != 1):
        raise LedgerError("Ledger lock links are prohibited")
    with lock_path.open("a+b") as lock:
        lock.seek(0, 2)
        if lock.tell() == 0:
            lock.write(b"0")
            lock.flush()
        deadline = time.monotonic() + 0.25
        acquired = False
        while not acquired:
            try:
                lock.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                if time.monotonic() >= deadline:
                    raise LedgerError("Ledger lock deadline exceeded") from None
                time.sleep(0.005)
        try:
            if not path.exists():
                # A missing ledger must not silently erase prior deny/token history.
                raise LedgerError("Ledger missing: operator must initialize an empty ledger")
            if path.stat().st_size > max_bytes:
                raise LedgerError("Ledger capacity reached; archive with an external checkpoint")
            records = []
            previous = "0" * 64
            with path.open("rb") as stream:
                for line in stream:
                    if not line.endswith(b"\n"):
                        raise LedgerError("Incomplete ledger entry")
                    try:
                        record = json.loads(line)
                    except (ValueError, UnicodeError):
                        raise LedgerError("Malformed ledger entry") from None
                    if not isinstance(record, dict) or record.get("previous_hash") != previous:
                        raise LedgerError("Ledger hash chain mismatch")
                    records.append(record)
                    previous = hashlib.sha256(line).hexdigest()
            yield Journal(path, records, previous, max_bytes)
        finally:
            lock.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


class Journal:
    def __init__(self, path: Path, records: list, previous: str, max_bytes: int):
        self.path, self.records = path, records
        self.previous, self.max_bytes = previous, max_bytes

    def append(self, record: dict) -> dict:
        entry = {**record, "previous_hash": self.previous}
        line = canonical(entry) + b"\n"
        if self.path.stat().st_size + len(line) > self.max_bytes:
            raise LedgerError("Ledger capacity reached")
        with self.path.open("ab") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())
        self.previous = hashlib.sha256(line).hexdigest()
        self.records.append(entry)
        return entry
