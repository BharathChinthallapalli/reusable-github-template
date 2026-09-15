"""Offline approval issuer. Deploy under a separate trusted identity, never a worker."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import sys
import time
import uuid

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from gate import audit_record, binding, classify, request_from, utc
from ledger import canonical, locked


def append_decision(proposal: dict, workspace: Path, private_key: Ed25519PrivateKey) -> dict:
    config = json.loads((workspace / ".guardian/policy.json").read_text())
    public_hex = private_key.public_key().public_bytes_raw().hex()
    if config.get("approval_public_key") != public_hex:
        raise ValueError("Issuer key does not match managed public key")
    request = request_from(proposal["payload"], proposal["runtime"], proposal["surface"], workspace)
    result = classify(request, workspace)
    if result["decision"] != "IN_SCOPE" or result.get("identity_required"):
        raise ValueError("Only supported non-cloud in-scope requests may be approved")
    answers = proposal["answers"]
    for name in ("command", "purpose", "necessity", "impact"):
        if not isinstance(answers.get(name), str) or not answers[name].strip():
            raise ValueError(f"Missing review answer: {name}")
    exact = request["raw_command"] or canonical(request["tool_input"]).decode()
    if answers["command"] != exact:
        raise ValueError("Review command differs from exact proposed tool input")
    verdict = proposal.get("decision")
    if verdict not in {"APPROVED", "DENIED"}:
        raise ValueError("Guardian must explicitly decide APPROVED or DENIED")
    rationale = proposal.get("rationale", "")
    if not isinstance(rationale, str) or not rationale.strip() or "\n" in rationale:
        raise ValueError("One-line rationale is required")
    now = time.time()
    record = audit_record(request, result, config["policy_version"], now)
    record.update(layer=2, answers=answers, rationale=rationale, decision="GUARDIAN_DENIED")
    if verdict == "APPROVED":
        token = {"request_hash": binding(request, config["policy_version"]),
                 "issued_at": now, "expires_at": now + min(config["approval_ttl_seconds"], 600),
                 "token_id": str(uuid.uuid4()), "answers": answers, "identity": None}
        record.update(decision="APPROVAL_ISSUED", token=token,
                      signature=base64.b64encode(private_key.sign(canonical(token))).decode(),
                      token_id=token["token_id"], token_expiry=utc(token["expires_at"]))
    with locked(workspace / config["ledger"], config["max_ledger_bytes"]) as journal:
        journal.append(record)
    return {"decision": verdict, "rationale": rationale, "token_id": record["token_id"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--private-key", required=True, type=Path,
                        help="Protected 32-byte Ed25519 key; must be outside worker-accessible storage")
    args = parser.parse_args()
    try:
        # Explicit operator invocation only. No key discovery, generation or environment dump.
        if args.private_key.resolve().is_relative_to(args.workspace.resolve()):
            raise ValueError("Approval private key must be outside the workspace")
        key = Ed25519PrivateKey.from_private_bytes(args.private_key.read_bytes())
        data = sys.stdin.buffer.read(65537)
        if len(data) > 65536:
            raise ValueError("Proposal exceeds limit")
        result = append_decision(json.loads(data), args.workspace.resolve(), key)
        print(json.dumps(result))
        return 0
    except Exception as error:
        print(f"Approval denied: {type(error).__name__}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
