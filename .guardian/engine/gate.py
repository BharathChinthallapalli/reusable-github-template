"""Deterministic policy and signed-review gate. No command is executed here."""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from ledger import canonical, digest, locked
from policy import evaluate, _path

SHELL_TOOLS = {"bash", "powershell", "exec_command", "shell", "runterminalcommand",
               "run_in_terminal", "terminal"}
READ_TOOLS = {"read", "read_file", "readfile", "glob", "grep", "search", "list_dir"}
EDIT_TOOLS = {"write", "edit", "create_file", "replace_string_in_file", "write_file",
              "edit_file", "notebookedit", "apply_patch"}
DENY_DECISIONS = {"HARD_DENY", "IN_SCOPE", "PIVOT_ATTEMPT", "GUARDIAN_DENIED"}
PROTECTED = {".guardian", ".github", ".claude", ".codex", "hooks", "agents.md", "claude.md", ".git", ".vscode", "tools"}


def utc(epoch: float | None = None) -> str:
    return datetime.fromtimestamp(time.time() if epoch is None else epoch, timezone.utc).isoformat()


def request_from(payload: dict, runtime: str, surface: str, workspace: Path) -> dict:
    tool = payload.get("tool_name", payload.get("toolName", ""))
    args = payload.get("tool_input", payload.get("toolArgs", {}))
    if isinstance(args, str):
        args = json.loads(args)
    session = payload.get("session_id", payload.get("sessionId", ""))
    if not isinstance(args, dict) or not isinstance(tool, str) or not isinstance(session, str) or not session:
        raise ValueError("Malformed request or missing session id")
    if runtime not in {"copilot", "claude", "codex"}:
        raise ValueError("Unsupported runtime")
    cwd = args.get("workdir", args.get("cwd", payload.get("cwd", str(workspace))))
    cwd_path = Path(cwd)
    if not cwd_path.is_absolute():
        cwd_path = workspace / cwd_path
    cwd_path = cwd_path.resolve()
    if not cwd_path.is_relative_to(workspace.resolve()):
        raise ValueError("Working directory escapes workspace")
    command = args.get("command", args.get("input", ""))
    if not isinstance(command, str):
        raise ValueError("Command must be text")
    if len(canonical(payload)) > 65536:
        raise ValueError("Request exceeds 64 KiB")
    return {"runtime": runtime, "surface": surface, "session_id": session,
            "tool_use_id": payload.get("tool_use_id", payload.get("toolCallId")),
            "agent": payload.get("agent_id", payload.get("agentName", payload.get("agent_type"))),
            "tool_name": tool, "tool_input": args, "raw_command": command,
            "cwd": str(cwd_path), "workspace": str(workspace.resolve())}


def reject(reason: str, rule: str, command: str = "") -> dict:
    return {"decision": "HARD_DENY", "rationale": reason, "rule": rule,
            "parsed_command": command, "effect": rule, "identity_required": False}


def file_policy(request: dict, workspace: Path) -> dict:
    tool, args = request["tool_name"].lower(), request["tool_input"]
    paths = []
    if tool in {"glob", "grep", "search", "list_dir"}:
        return reject("Recursive native discovery lacks a bounded file contract", "UNBOUNDED_FILE_TOOL")
    if tool == "apply_patch":
        patch = request["raw_command"]
        lines = patch.splitlines()
        if len(lines) < 3 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
            return reject("Malformed patch", "UNPARSEABLE_PATCH")
        for line in lines[1:-1]:
            match = re.fullmatch(r"\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)", line)
            if match:
                paths.append(match[1])
            elif line.startswith("***") or not line.startswith(("+", "-", " ", "@")):
                if line != "*** End of File":
                    return reject("Unsupported patch syntax", "UNPARSEABLE_PATCH")
    else:
        for key in ("file_path", "filePath", "path", "notebook_path", "directory"):
            if key in args:
                paths.append(args[key])
    if not paths:
        return reject("Explicit file paths are required", "UNBOUNDED_FILE_TOOL")
    sensitive = re.compile(r"(?i)(?:\.ost$|\.pst$|(?:^|[/\\])\.env(?:$|\.)|credentials|vault|"
                           r"login data|web data|cookies|local state|consolehost_history|\.(?:pem|pfx|key)$|"
                           r"(?:^|[/\\])\.ssh|\.aws|\.azure|\.kube|appdata|id_rsa|id_ed25519)")
    for raw in paths:
        if not isinstance(raw, str) or sensitive.search(raw):
            return reject("Sensitive file material is prohibited", "SENSITIVE_FILE")
        if "\\" in raw and Path().anchor != "\\":
            # Windows alternate separators on Linux must not become innocent filenames.
            if __import__("os").name != "nt":
                return reject("Foreign path syntax", "PATH_SYNTAX")
        path = Path(raw)
        target = path if path.is_absolute() else Path(request["cwd"]) / path
        if not _path(str(target), workspace) or not target.resolve().is_relative_to(workspace.resolve()):
            return reject("File tool target escapes workspace", "OUTSIDE_WORKSPACE")
        relative = target.resolve().relative_to(workspace.resolve())
        if tool in EDIT_TOOLS and any(part.lower() in PROTECTED for part in relative.parts):
            return reject("Agents cannot modify guardian or runtime policy", "POLICY_TAMPER")
    return {"decision": "AUTO_ALLOW" if tool in READ_TOOLS else "IN_SCOPE",
            "rationale": "Scoped native read" if tool in READ_TOOLS else "File edit requires guardian review",
            "rule": "WORKSPACE_FILE", "parsed_command": canonical(args).decode(),
            "effect": "workspace-file", "identity_required": False}


def classify(request: dict, workspace: Path) -> dict:
    tool = request["tool_name"].lower()
    if tool in SHELL_TOOLS:
        if not request["raw_command"]:
            return reject("Missing shell command", "MISSING_COMMAND")
        extra = set(request["tool_input"]) - {"command", "workdir", "cwd", "timeout", "timeout_ms", "yield_time_ms", "max_output_chars", "max_output_tokens", "description"}
        if extra:
            return reject("Unsupported shell options or interactive execution", "SHELL_OPTIONS")
        shell = "powershell" if tool == "powershell" else "bash"
        return evaluate(request["raw_command"], shell, Path(request["cwd"]))
    if tool in READ_TOOLS | EDIT_TOOLS:
        return file_policy(request, workspace)
    return reject("Unsupported tool or interactive continuation; no reviewed effect contract", "UNKNOWN_TOOL")


def binding(request: dict, policy_version: str) -> str:
    # Full inputs and exact bytes are bound, not a lossy whitespace or case transform.
    return digest({**request, "policy_version": policy_version})


def audit_record(request: dict, result: dict, policy_version: str, now: float) -> dict:
    return {"timestamp": utc(now), **request, "parsed_command": result.get("parsed_command", ""),
            "command_hash": hashlib.sha256(request["raw_command"].encode()).hexdigest(),
            "request_hash": binding(request, policy_version), "policy_version": policy_version,
            "answers": None, "decision": result["decision"], "rationale": result["rationale"],
            "triggering_rule": result.get("rule"), "effect": result.get("effect"), "layer": 1,
            "identity": None, "pivot_flag": False, "heightened_suspicion": False,
            "defender_verdict": "not_observed", "token_expiry": None, "token_id": None}


def token_valid(entry: dict, request_hash: str, public_key: str | None, now: float) -> bool:
    if not public_key or entry.get("decision") != "APPROVAL_ISSUED":
        return False
    token = entry.get("token", {})
    try:
        if (token["request_hash"] != request_hash or token["issued_at"] > now or
                token["expires_at"] <= now or token["expires_at"] - token["issued_at"] > 600 or
                token["expires_at"] <= token["issued_at"] or not token["token_id"]):
            return False
        answers = token["answers"]
        if any(not isinstance(answers.get(k), str) or not answers[k].strip()
               for k in ("command", "purpose", "necessity", "impact")):
            return False
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key)).verify(
            base64.b64decode(entry["signature"], validate=True), canonical(token))
        return True
    except (KeyError, ValueError, TypeError, InvalidSignature):
        return False


def apply_history(journal, record: dict, public_key: str | None, now: float) -> None:
    recent = []
    for entry in journal.records:
        try:
            elapsed = now - datetime.fromisoformat(entry["timestamp"]).timestamp()
        except (KeyError, ValueError, TypeError):
            raise ValueError("Ledger entry timestamp invalid") from None
        if 0 <= elapsed <= 600:
            recent.append(entry)
    session = [e for e in journal.records if e.get("session_id") == record["session_id"]
               and e.get("runtime") == record["runtime"] and (e.get("layer") == 1 or e.get("decision") == "GUARDIAN_DENIED")]
    record["heightened_suspicion"] = any(e.get("decision") in DENY_DECISIONS for e in session[-3:])
    for previous in recent + session[-3:]:
        if previous.get("decision") not in DENY_DECISIONS:
            continue
        cross_runtime = previous.get("runtime") != record["runtime"]
        same_command = previous.get("command_hash") == record["command_hash"] and bool(record["raw_command"])
        same_denied_effect = (record["decision"] == "HARD_DENY" and
                              previous.get("effect") == record.get("effect"))
        explicit_retry = (previous.get("decision") == "GUARDIAN_DENIED" and
                          (same_command or previous.get("parsed_command") == record["parsed_command"]))
        if (same_command and cross_runtime) or (record["heightened_suspicion"] and (same_denied_effect or explicit_retry)):
            record.update(decision="PIVOT_ATTEMPT", pivot_flag=True,
                          rationale="Denied effect retried within the pivot window", triggering_rule="NO_PIVOT")
            return
    if record["decision"] != "IN_SCOPE":
        return
    consumed = {e.get("token_id") for e in journal.records if e.get("decision") == "APPROVED"}
    for entry in reversed(recent):
        if token_valid(entry, record["request_hash"], public_key, now):
            token = entry["token"]
            if token["token_id"] in consumed:
                continue
            record.update(decision="APPROVED", rationale="Signed guardian approval; normal host permissions still apply",
                          token_id=token["token_id"], token_expiry=utc(token["expires_at"]),
                          answers=token["answers"], identity=token.get("identity"))
            return
    record["rationale"] = "Route this command through guardian first"


def decide(payload: dict, runtime: str, surface: str, workspace: Path) -> dict:
    started = time.monotonic()
    workspace = workspace.resolve()
    config = json.loads((workspace / ".guardian/policy.json").read_text())
    request = request_from(payload, runtime, surface, workspace)
    result = classify(request, workspace)
    if result.get("identity_required"):
        # A model-supplied identity or signed label cannot prove active az/Az/Graph context.
        result = reject("Verified execution-time Azure/Entra identity broker is not installed",
                        "IDENTITY_UNVERIFIED", result.get("parsed_command", ""))
    if time.monotonic() - started > 1.0:
        result = reject("Policy evaluation budget exceeded", "DEADLINE")
    record = audit_record(request, result, config["policy_version"], time.time())
    ledger_path = workspace / config["ledger"]
    with locked(ledger_path, config["max_ledger_bytes"]) as journal:
        if str(payload.get("_guardian_event", "")).lower() == "permissionrequest" and record["decision"] == "IN_SCOPE":
            record.update(decision="AUTO_ALLOW", rationale="Supplemental hard-deny check passed; defer to host permissions and mandatory PreToolUse token check")
        else:
            apply_history(journal, record, config.get("approval_public_key"), time.time())
        if time.monotonic() - started > 1.5:
            record.update(decision="HARD_DENY", rationale="Audit deadline exceeded", triggering_rule="DEADLINE")
        journal.append(record)
    return record
