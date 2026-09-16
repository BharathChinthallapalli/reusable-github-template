# Local validation — 2026-09-16

Implementation baseline: f3ba4feb3b0a18d00e94720c5e1e2502cbd050b5 plus the reviewed
SDLC foundation diff. Linux; Python3.12.14; prepared .venv for repository/Guardian
tools. No installation, account grant, runtime reconfiguration or Azure deployment
was performed for this slice.

| Exact command / check | Observed result | Coverage limit |
| --- | --- | --- |
| python3 -m unittest discover -s tests -p test_sdlc.py -q |47 tests passed | Local inert contracts, governance, monitor, metrics and scratch instantiation |
| .venv/bin/python -m unittest discover -s tests -q |202 tests run;200 passed,2 platform-specific skips | macOS system-Python and native Windows bootstrap skipped |
| .venv/bin/python -m unittest discover -s tests/guardian -q |38 passed;6 adapter subprocesses,max0.078s | No installed Copilot/Claude/Codex model or IDE test |
| .venv/bin/python -m unittest discover -s tests/integration -q |22 passed | Local Git/hook/scanner integration, not hosted CI |
| .venv/bin/ruff check tools/sdlc_contracts.py tools/sdlc_governance.py tools/sdlc_monitor.py tools/sdlc_metrics.py scripts tests/test_sdlc.py |Passed | Static lint |
| .venv/bin/python hooks/agent_hooks.py --event check |Exit0, empty JSON result | Repository Ruff/Gitleaks check, not endpoint detection assurance |
| python3 tools/check_repository.py |Passed | Project license still unselected; application/GitHub settings separate |
| python3 tools/check_ai_configuration.py |Passed,40 skills/14 agents | Static metadata only |
| python3 tools/ai_catalog.py |Passed | Generated catalog freshness |
| Skill-creator quick_validate.py for each of6 new skill directories |All valid | Metadata/basic structure only |
| python3 tools/check_design.py after explicit ADD seal |Passed | Structural design/content binding, not human approval |
| git diff --check |Passed | Tracked diff whitespace; final staged check also required |

The default system Python initially lacked tree-sitter: that baseline invocation
failed import/diagnostic cases. The existing prepared .venv had the required
dependencies and passed all38 Guardian tests. No policy weakening or scanner
suppression was used to obtain the passing result.

Regression review found and fixed: missing change-path admission, overbroad lock
matching that could block ordinary clock.py, numeric aggregate overflow, and
double-reading spec sources before hashing. The scratch test caught a temporary
missing documentation link; after completion the full snapshot initialized,
passed repository checks and ran the monitor successfully.

Guardian engine, adapters, policy and runtime hook files have **no diff** against
the implementation baseline. The source reading log is the only new .guardian
artifact. See [worked example](WORKED-EXAMPLE.md) for synthetic metrics and
[activation findings](ACTIVATION.md) for unimplemented/unverified delivery surfaces.

Total in the final broad lanes:260 passed and2 skipped. The focused47 are included
in the202 repository lane, not added again. These are deterministic software
tests, not model-obedience statistics, proof of zero Defender alerts, a real
production release or certification evidence.
