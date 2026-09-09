# Test persistence through its contract

Use this reference for saved state, caches, checkpoints, generated artifacts or
database changes. Identify the canonical representation, actual writer/reader
and promised compatibility. A human-readable display may intentionally omit
information that the canonical saved artifact must preserve.

| Changed contract | Useful case and observable evidence |
| --- | --- |
| Save/load | Save a known object, load it through the consumer and compare meaningful values, types and behavior against an independent expectation; two functions sharing the same bug can still round-trip |
| Version compatibility | Read supported prior versions and apply the documented migration; reject or explicitly handle unsupported versions without silently misinterpreting state |
| Malformed/truncated state | Exercise relevant missing fields, corruption, partial files and invalid values; verify the declared error or recovery behavior and absence of unintended partial effects |
| Failed save | Inject the relevant write/publish failure and check the state readers can observe, cleanup behavior and preservation of the last valid artifact where the contract promises it |
| Publication visibility | When the storage supports atomic replacement, verify that readers see a complete permitted version rather than a partly written artifact |
| Crash recovery/durability | Test the storage-specific durability/recovery promise where required; successful replacement or a passing ordinary save test alone does not establish survival after a crash |
| Concurrent writers | Exercise the documented ownership, lock, compare-and-swap, version check or conflict-resolution contract; atomic replacement alone does not prevent lost updates |
| Identity and reuse | Ensure the consumer loads the intended artifact/version, and relevant repeated loads or process restarts preserve the promised behavior |

Choose cases from demonstrated risks and documented support; not every project
needs migrations, concurrent writes or a crash-injection harness. Inspect the
selected filesystem/database/object-store's current guarantees before asserting
atomicity or durability. Keep simulated failure evidence distinct from an actual
storage or process-crash test.

Use task-owned temporary directories and distinct paths for parallel tests.
Ensure a failed assertion or malformed artifact propagates through the command's
exit status. Inspect the produced artifact through its real consumer when that
boundary changed; checking a serializer's return value alone misses publication
and compatibility failures.

Add chosen cases to the skill's behavior matrix with the artifact/version,
independent expected result, failure injection if used, observable outcome and
coverage limit. Keep the project format and tooling unless a concrete need
justifies a change.

This adapts [minbpe's persistence tests](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/tests/test_tokenizer.py)
and the [arxiv-sanity-lite artifact-publication review](../../../../docs/research/repository-inventory/karpathy-notes.md).
Use [clean-code](../../clean-code/SKILL.md) for code-quality decisions; source
examples do not establish universal storage guarantees.
