---
applyTo: "tools/**/*.py,tests/**/*.py"
---

Repository tooling supports Python 3.12 or newer. Keep initialization and the
foundation checker on the standard library. AI metadata diagnostics use the
pinned PyYAML development dependency and safe loading; never execute YAML tags.
Use pathlib and explicit UTF-8. Do not construct shell commands from user input.
Validate all initializer inputs and target paths before the first write.
Keep initialization repeatable and preserve files edited after initialization.
Use unittest and temporary directories for tests that modify files.
Add tests for meaningful failure paths; avoid tests that only repeat constants.
