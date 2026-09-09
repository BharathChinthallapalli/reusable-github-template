# Design decisions

Use these questions at the point of change. They are an original application of
the [approved sources](sources.md), not a mandatory architecture.

| Decision | Evidence to look for | Prefer when evidence is absent |
| --- | --- | --- |
| Rename | A reader cannot identify the domain fact or operation; units are ambiguous | Retain the established term |
| Extract a function | A block expresses a useful named concept or mixes orchestration with detail | Keep the readable sequence together |
| Share implementation | The same rule is repeated and its copies must change for the same reason | Allow independently changing code to remain separate |
| Introduce an object | Related data and operations enforce an actual invariant | Use the existing function or record |
| Add an adapter | External representation or failure handling is spreading into application logic | Call the existing interface directly |
| Simplify branching | Nesting obscures a decision or the usual execution path | Retain an explicit local conditional |

Martin's guidance on names, functions, and boundaries informs these questions.
Use domain terms consistently and include units where confusion matters, such
as `timeout_seconds`. Keep a helper only if its name helps explain the caller;
an extraction that moves readers between files without clarifying a concept
may be better inlined. Follow the language and repository rather than copying
another language's class structure.

Cocca's emphasis on clarity, consistency, and authoritative data supports
keeping each business rule in one maintained place. Syntax that looks alike is
insufficient evidence for a configurable framework. Avoid a dependency or an
extension point whose only justification is a possible future requirement.

For a debatable structural change, record briefly: the problem visible in the
current code, why this boundary helps, what behavior stays fixed, and how it
was checked. If no current problem can be named, leave the structure alone.
