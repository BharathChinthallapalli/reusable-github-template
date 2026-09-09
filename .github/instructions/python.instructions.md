---
applyTo: "tools/**/*.py,tests/**/*.py"
---

Repository tooling supports Python 3.12 or newer using the standard library.
Use pathlib and explicit UTF-8. Do not construct shell commands from user input.
Validate all initializer inputs and target paths before the first write.
Keep initialization repeatable and preserve files edited after initialization.
Use unittest and temporary directories for tests that modify files.
Add tests for meaningful failure paths; avoid tests that only repeat constants.
