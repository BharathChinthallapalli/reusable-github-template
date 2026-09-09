# Corpus and retrieval contract

Status: Draft. Record only systems and evidence the project actually has.

| Boundary | Project contract and evidence |
| --- | --- |
| User task, corpus owner and authoritative sources | |
| Corpus snapshot, document IDs, versions and usage rights | |
| Extraction/chunking configuration and transformation revision | |
| Chunk ID → document version → citation target mapping | |
| Embedding model/version, dimensions and index compatibility | |
| Index identity, build command and completeness check | |
| Effective query, filters, ranking/reranking and context budget | |
| Caller identity, document access rules and enforcement location | |
| Provider/data flows, logs and evidence retention | |
| Update/deletion semantics, cache invalidation and freshness target | |
| Index publication, previous compatible version and recovery | |
| Baseline/candidate identities and acceptance/evaluation command | |

## Acceptance matrix

Choose applicable cases and replace the question with the project's concrete
expected behavior. A skipped case needs a reason; the matrix is not a test run.

| Boundary | Question to turn into an assertion | Case/evidence reference | Outcome |
| --- | --- | --- | --- |
| Answerable query | Are the required source facts retrieved and supported in the answer? | | Not run |
| Missing evidence | Does the configured no-answer behavior occur without fabricated support? | | Not run |
| Citation | Does each citation resolve to the document version supporting the claim? | | Not run |
| Access filtering | Is denied content absent from retrieved context, answers and exposed cache entries? | | Not run |
| Malformed source | Is extraction failure identifiable without publishing an incomplete index as complete? | | Not run |
| Update/deletion | Does the documented freshness/deletion behavior hold across index and caches? | | Not run |
| Source instruction | Is retrieved instruction text treated as data without changing tool authority? | | Not run |
| Query variation | Does an important paraphrase, language or domain term retain the required evidence? | | Not run |

When diagnosing, retain source/chunk IDs, ranks and evidence references rather
than committing sensitive document text. Record retrieval and answer outcomes
separately so a successful answer cannot conceal a retrieval failure.
