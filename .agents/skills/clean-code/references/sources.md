# Sources and interpretation

This skill contains original operational guidance. It does not bundle book
chapters, article passages, or source examples. These works inform code-quality
decisions; they do not supersede requirements or repository contracts.

| Source | Use in this skill |
| --- | --- |
| German Cocca, [How to Write Clean Code – Tips and Best Practices (Full Handbook)](https://www.freecodecamp.org/news/how-to-write-clean-code/), 2023 | Readability, consistent conventions, clear flow, and authoritative representations of rules |
| Robert C. Martin, [Clean Code: A Handbook of Agile Software Craftsmanship](https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884), 2008 | Meaningful names, cohesive functions, useful comments, controlled boundaries, and readable tests |
| Martin Fowler, [Refactoring: Improving the Design of Existing Code, Second Edition](https://martinfowler.com/books/refactoring.html), 2018; [official catalog](https://refactoring.com/catalog/) | Small verified transformations that preserve observable behavior; choosing an appropriate transformation for a concrete problem |

Apply the intent in the project's language. Examples are not benchmark results
or universal blueprints. This skill does not prescribe Clean Architecture,
blanket SOLID rules, numerical function-size limits, or a ban on nulls, loops,
comments, exceptions, or repeated syntax.

Use official platform documentation to establish runtime facts. For a
code-quality trade-off, prefer the option supported by present code that keeps
the contract stable and the main execution path understandable.
