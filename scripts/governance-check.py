"""Project-local entrypoint; no external commands or permission changes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from sdlc_governance import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
