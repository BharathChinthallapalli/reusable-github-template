"""Conservative literal-command policy; never executes the submitted program.

Tree-sitter validates syntax; a deliberately small supported language limits effects.
Approval is not executable provenance, filesystem isolation, or a TOCTOU defense.
"""

import base64
import binascii
from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_bash
import tree_sitter_powershell

MAX_BYTES = 16384
DENIALS = (
    ("MAIL_STORE", r"\.ost\b|\.pst\b|outlook"),
    (
        "CREDENTIAL_ACCESS",
        r"cmdkey|vaultcmd|credman|storedcredential|protecteddata|cryptunprotectdata|dpapi|[/\\]microsoft[/\\](?:protect|credentials|vault)|login data|web data|cookies|local state|[/\\]\.ssh|id_rsa|id_ed25519|[/\\]\.aws|[/\\]\.azure|kubeconfig|[/\\]\.kube|consolehost_history|get-credential|lsass|comsvcs|procdump|out-minidump|secret|token|credential|private.?key|\.(?:pem|pfx|key)\b",
    ),
    (
        "ENCODED_OR_EVASION",
        r"(?:^|\s)-(?:e|enc|encodedcommand)\b|frombase64|base64|amsiutils|amsiinitfailed|executionpolicy\s+(?:bypass|unrestricted)|windowstyle\s+hidden",
    ),
    (
        "DOWNLOAD_OR_EXECUTION",
        r"invoke-expression|\biex\b|downloadstring|downloadfile|invoke-webrequest|invoke-restmethod|webclient|\bcurl\b|\bwget\b|\bcertutil\b|\bbitsadmin\b|\bmshta\b|\bregsvr32\b|\brundll32\b",
    ),
    (
        "ENDPOINT_TAMPER",
        r"(?:set|add)-mppreference|controlledfolder|disablerealtime|disablebehavior|attack.?surface",
    ),
    (
        "PERSISTENCE",
        r"register-wmievent|__eventfilter|new-service|\bsc\s+create|schtasks|shell:startup|start menu|runonce|hklm|hkcu",
    ),
    (
        "REMOTE_EXECUTION",
        r"psexec|invoke-command|enter-pssession|winrm|wmiprocess|win32_process",
    ),
    (
        "EXFILTRATION_OR_RECON",
        r"compress-archive|\b7z\b|\btar\b|get-aduser|get-localuser|get-localgroupmember",
    ),
    (
        "CLOUD_MUTATION",
        r"vaultdelete|keydelete|keypurge|keybackup|vaultget|secretget|keyget|roleassignment|role\s+assignment|pim|nsg|firewall|private.?endpoint|diagnostic.?setting|conditional.?access|\bmfa\b|consent|service.?principal|new-az|remove-az|set-az|microsoft\.graph|\bget-mg|\baz\s+(?:ad|deployment|group\s+delete|resource\s+delete|rest)\b",
    ),
)
SENSITIVE_PARTS = {
    ".guardian",
    ".git",
    ".claude",
    ".codex",
    ".github",
    ".vscode",
    "hooks",
    "tools",
    "agents.md",
    "claude.md",
    ".ssh",
    ".aws",
    ".azure",
    ".kube",
    "appdata",
    "credentials",
    "vault",
    "protect",
    "outlook",
    "login data",
    "web data",
    "cookies",
    "local state",
    "consolehost_history.txt",
}
STRUCTURE = {"program", "statement_list", "pipeline", "pipeline_chain", "list"}
TOKEN = re.compile(r"""\s*(?:"([^"\r\n]*)"|'([^'\r\n]*)'|([^\s'";&|<>]+))""")


def _result(decision, rule, parsed, effect="unknown", identity=False):
    reasons = {
        "AUTO_ALLOW": "Literal side-effect-free diagnostic inside permitted scope",
        "IN_SCOPE": "Route this command through guardian first",
        "HARD_DENY": "Policy refuses this operation or cannot establish its bounded effects",
    }
    return dict(
        decision=decision,
        rationale=reasons[decision],
        rule=rule,
        parsed_command=parsed,
        effect=effect,
        identity_required=identity,
    )


def _words(text):
    words, offset = [], 0
    while offset < len(text):
        if not text[offset:].strip():
            break
        if offset and not text[offset].isspace():
            raise ValueError("Concatenated literals are unsupported")
        match = TOKEN.match(text, offset)
        if not match:
            raise ValueError("Unsupported literal syntax")
        words.append(next(value for value in match.groups() if value is not None))
        offset = match.end()
    return words


def _commands(node, source):
    if node.type == "command":
        return [source[node.start_byte : node.end_byte].decode("utf-8")]
    if node.type not in STRUCTURE:
        raise ValueError("Unsupported AST construct")
    commands = []
    for child in node.children:
        if not child.is_named:
            if source[child.start_byte : child.end_byte].decode("utf-8") not in {
                ";",
                "|",
                "&&",
                "||",
            }:
                raise ValueError("Unsupported control operator")
            continue
        commands.extend(_commands(child, source))
    return commands


def _path(value, workspace, directory=False):
    # No provider paths, UNC, ADS, globs, environment expansion, or traversal.
    normal = value.replace("\\", "/")
    parts = normal.lower().split("/")
    reserved = {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{i}" for i in range(1, 10)),
        *(f"lpt{i}" for i in range(1, 10)),
    }
    if value.startswith("-") or any(p.split(".")[0] in reserved for p in parts):
        return False
    if any(p not in {"", "."} and p.endswith((".", " ")) for p in parts):
        return False
    if any(p in SENSITIVE_PARTS or p.startswith(".env") for p in parts):
        return False
    checked = normal
    if __import__("os").name == "nt" and re.match(r"^[A-Za-z]:/", normal):
        checked = normal[2:]
    if normal.startswith("//") or any(p in {"..", "~"} for p in parts) or any(c in checked for c in "*?[]:$%"):
        return False
    path = Path(normal)
    path = path if path.is_absolute() else workspace / path
    try:
        root = workspace.resolve(strict=True)
        resolved = path.resolve(strict=False)
        resolved.relative_to(root)
        current = path
        while current != root:
            if current.is_symlink() or (
                hasattr(current, "is_junction") and current.is_junction()
            ):
                return False
            if current == current.parent:
                return False
            current = current.parent
        if directory:
            return resolved.is_dir()
        if resolved.exists():
            return resolved.is_file() and resolved.stat().st_nlink == 1
        return resolved.parent.is_dir()
    except (OSError, ValueError, RuntimeError):
        return False


def _literal(words, workspace, shell, depth):
    if not words:
        return _result("HARD_DENY", "EMPTY", "")
    name, args = words[0].lower(), words[1:]
    parsed = " ".join(words)
    if name in {
        "bash",
        "sh",
        "pwsh",
        "powershell",
        "powershell.exe",
        "pwsh.exe",
        "cmd",
        "cmd.exe",
    }:
        switches = {"bash": "-c", "sh": "-c", "cmd": "/c", "cmd.exe": "/c"}
        flag = switches.get(name, "-command")
        if len(args) != 2 or args[0].lower() not in {flag, "-c"} or depth >= 3:
            return _result("HARD_DENY", "UNSUPPORTED_WRAPPER", parsed)
        nested_shell = (
            "powershell" if name.startswith(("pwsh", "powershell")) else "bash"
        )
        if name.startswith("cmd") and re.search(r"[\\^%&|<>]", args[1]):
            return _result("HARD_DENY", "UNSUPPORTED_CMD", parsed)
        nested = _evaluate(args[1], nested_shell, workspace, depth + 1)
        if name.startswith("cmd"):
            return _result("HARD_DENY", "UNSUPPORTED_CMD_EFFECT", parsed)
        if nested["decision"] == "AUTO_ALLOW":
            nested.update(decision="IN_SCOPE", rationale="Nested interpreter startup requires guardian review")
        return nested
    if name in {"pwd", "get-date", "get-location", "get-process"} and not args:
        if (shell == "bash" and name == "pwd") or (
            shell == "powershell" and name != "pwd"
        ):
            return _result("AUTO_ALLOW", "DIAGNOSTIC", parsed, "diagnostic")
    if shell == "powershell" and name == "get-childitem":
        target = (
            args[1]
            if len(args) == 2 and args[0].lower() in {"-path", "-literalpath"}
            else args[0]
            if len(args) == 1
            else "."
            if not args
            else None
        )
        if target is not None and _path(target, workspace, directory=True):
            return _result(
                "AUTO_ALLOW", "WORKSPACE_ENUMERATION", parsed, "workspace-enumeration"
            )
    if name == "az":
        # Fixed read-only shapes: no alternate identity, REST, query, extensions, or output file.
        valid = args == ["account", "show"] or args == ["resource", "list"]
        valid = valid or (
            len(args) == 4
            and args[:3] == ["group", "show", "--name"]
            and bool(re.fullmatch(r"[A-Za-z0-9_.-]+", args[3]))
        )
        return _result(
            "IN_SCOPE" if valid else "HARD_DENY",
            "AZURE_READ" if valid else "UNSUPPORTED_CLOUD",
            parsed,
            "azure-read",
            True,
        )
    paths = []
    effect = "workspace-read"
    if (
        shell == "bash"
        and name == "cat"
        and args
        and all(not a.startswith("-") for a in args)
    ):
        paths = args
    elif (
        shell == "bash"
        and name == "cp"
        and len(args) == 2
        and all(not a.startswith("-") for a in args)
    ):
        paths, effect = args, "workspace-write"
    elif shell == "bash" and name == "rg":
        # Require explicit file targets; recursive trees could include secrets or devices.
        rest = list(args)
        while rest and rest[0] in {"-n", "-F", "--fixed-strings", "--line-number"}:
            rest.pop(0)
        if rest and rest[0] == "--":
            rest.pop(0)
        if (
            len(rest) >= 2
            and not rest[0].startswith("-")
            and all(not a.startswith("-") for a in rest[1:])
        ):
            paths = rest[1:]
    elif shell == "powershell" and name in {"get-content", "set-content", "copy-item"}:
        if name == "get-content" and len(args) == 1 and not args[0].startswith("-"):
            paths = args
        elif (
            name == "get-content"
            and len(args) == 2
            and args[0].lower() in {"-path", "-literalpath"}
        ):
            paths = args[1:]
        elif (
            name == "set-content"
            and len(args) == 4
            and args[0].lower() in {"-path", "-literalpath"}
            and args[2].lower() == "-value"
        ):
            paths, effect = [args[1]], "workspace-write"
        elif (
            name == "copy-item"
            and len(args) == 4
            and args[0].lower() in {"-path", "-literalpath"}
            and args[2].lower() == "-destination"
        ):
            paths, effect = [args[1], args[3]], "workspace-write"
    if paths and all(_path(p, workspace) for p in paths):
        return _result("IN_SCOPE", "WORKSPACE_FILE_OPERATION", parsed, effect)
    return _result("HARD_DENY", "UNSUPPORTED_OR_UNSAFE_EFFECT", parsed)


def _encoded_audit(command):
    """Decode a bounded literal payload for audit only; encoded commands stay denied."""
    flag = re.search(
        r"(?:^|\s)[\"']?-(?:encodedcommand|enc|e)[\"']?(?=\s|$)", command, re.IGNORECASE
    )
    if not flag:
        return None
    remainder = command[flag.end() :].strip()
    try:
        words = _words(remainder)
        if not words or len(words[0]) > 8192:
            raise ValueError("Missing or oversized payload")
        decoded = base64.b64decode(words[0], validate=True)
        if len(decoded) > 4096:
            raise ValueError("Oversized decoded payload")
        text = decoded.decode("utf-16-le")
        if "\x00" in text:
            raise ValueError("Decoded payload contains NUL")
        return "Decoded UTF-16LE payload (never executed): " + text
    except (ValueError, binascii.Error, UnicodeError):
        return "Encoded payload could not be safely decoded (never executed)"


def _evaluate(command, shell, workspace, depth):
    if (
        not isinstance(command, str)
        or not command.strip()
        or len(command.encode("utf-8")) > MAX_BYTES
    ):
        return _result("HARD_DENY", "INVALID_INPUT", "")
    decoded_audit = _encoded_audit(command)
    if decoded_audit is not None:
        return _result(
            "HARD_DENY", "ENCODED_OR_EVASION", decoded_audit, "encoded_or_evasion"
        )
    for rule, pattern in DENIALS:
        if re.search(pattern, command, re.IGNORECASE):
            return _result("HARD_DENY", rule, command, rule.lower())
    if shell not in {"bash", "powershell"}:
        return _result("HARD_DENY", "UNSUPPORTED_SHELL", command)
    # Deliberately deny expansions even within quotes: never evaluate submitted code.
    if (
        any(c in command for c in "$`%@{},~*?[]\x00\r")
        or not command.isascii()
        or (shell == "bash" and "\\" in command)
    ):
        return _result("HARD_DENY", "DYNAMIC_OR_NONASCII", command)
    module = tree_sitter_bash if shell == "bash" else tree_sitter_powershell
    try:
        source = command.encode("utf-8")
        tree = Parser(Language(module.language())).parse(source)
        if tree is None or tree.root_node.has_error:
            return _result("HARD_DENY", "PARSE_ERROR", command)
        commands = _commands(tree.root_node, source)
        decisions = [_literal(_words(c), workspace, shell, depth) for c in commands]
    except (ValueError, OSError, RuntimeError, RecursionError):
        return _result("HARD_DENY", "UNSUPPORTED_SYNTAX", command)
    if not decisions:
        return _result("HARD_DENY", "EMPTY", command)
    denied = next((d for d in decisions if d["decision"] == "HARD_DENY"), None)
    if denied:
        return denied
    # Compound approved commands remain in scope, including diagnostic pipelines.
    if len(decisions) > 1:
        return _result(
            "IN_SCOPE",
            "COMPOUND_COMMAND",
            command,
            "+".join(d["effect"] for d in decisions),
            any(d["identity_required"] for d in decisions),
        )
    return decisions[0]


def evaluate(command: str, shell: str, workspace: Path) -> dict:
    """Classify only; callers must bind tokens to exact input, cwd and identity."""
    return _evaluate(command, shell, Path(workspace), 0)
