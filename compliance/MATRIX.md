# Compliance support matrix

Checked 2026-09-16. **Artifacts support an assessment; their presence does not
satisfy a law or establish certification.** Determine system, intended purpose,
risk class, provider/deployer role, entity scope, effective dates and actual
processing first. Owners below are roles to assign, not approvals already obtained.
See [source evidence](../.guardian/READING-LOG.md) and [open findings](../docs/sdlc/ACTIVATION.md).

## AI Act

Source: [Regulation2024/1689, consolidated27July2026](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng).
These high-risk duties are conditional; do not apply all of them to every chatbot.
Article113 delays ChapterIII sections1–3 (except6(5)) to2December2027 for6(2)
and2August2028 for6(1). This is not a blanket delay of ChapterIX Article72.
Assess Article111 transition rules separately.

| Requirement | Artifact / gate supporting it | Automation / current limit | Evidence location | Owner |
| --- | --- | --- | --- | --- |
| Arts6/25 classification and role | Per-system intended-use assessment | Required compliance fields; legal judgment human | ai-act/system-assessment.md; intent/design | System + legal |
| Art9 risk management | Threat/risk lifecycle and residual-risk review | Required design section; reviewerL10; no automatic legal finding | design.md; review evidence | Risk owner |
| Art10 data governance | Provenance, representative splits, quality/bias controls | Data-card and eval review; applicable data scope assessed | mlops/data-card.md | Data owner |
| Art11 technical documentation | AnnexIV documentation index | Spec source hashes; index completeness human | ai-act/technical-documentation.md; specs; ADD; model cards | Provider |
| Art12 logging capability | Traceable relevant lifecycle events | Existing Guardian plus planned tracing; not full system logging coverage | Guardian ledger; tracing | Platform/provider |
| Art13 information for deployers | Capabilities, limitations, input/oversight instructions | Model-card/handover review | mlops/model-card.md; docs/HANDOVER.md | Provider |
| Art14 oversight | Competence, interpretation, intervention, override/stop | Approval/kill-switch design; runtime proof still required | ai-act/oversight-and-post-market.md | Provider + deployer |
| Art15 accuracy, robustness, cybersecurity | Measured targets, adversarial/regression evals | Test/eval admission; Guardian defense in depth | evals; model card; guardian evidence | ML + security |
| Art26 deployer duties | Instruction compliance, inputs, oversight, monitoring and escalation | Operational readiness review; notices and reporting not automated | handover; runbooks; data/processing records | Deployer |
| Art27 conditional FRIA | Scope-specific impact assessment | Human gate for covered AnnexIII deployers; no universal FRIA inference | system-assessment.md | Deployer + legal |
| Art50(1) interaction notice | User-facing AI notice unless exception applies | UX review; notice/evidence test per project | user docs; UX tests | Provider |
| Art50(2) synthetic marking | Detectable machine-readable marking when applicable | Versioned marking/effectiveness eval | model/prompt cards; evals | Provider |
| Art50(3)/(4) deployer disclosure | Relevant emotion/biometric, deepfake and public-interest-text notices | Substantive human/editorial exception assessed, not AI-only review | disclosure evidence | Deployer/editorial |
| Art72 post-market monitoring | Active monitoring plan and corrective loop | Bands proposals + incidents; production collector not activated | monitoring; runbooks/incident.md | High-risk provider |

Retention is record-specific: Arts19/26(6) logs under operator control ordinarily
at least six months, subject to the stated other-law qualifications; Art18 and
47 specify ten-year provider documents/declarations, not all prompts. No fixed
`auditRetentionDays` is inferred for every system. Draft AnnexIII guidance is
nonbinding; missing AnnexI guidance is explicitly excepted. Uploaded Article50
content approval does not establish later formal adoption.

## Other frameworks

| Requirement / version | Artifact / gate supporting it | Automation / current limit | Evidence location | Owner |
| --- | --- | --- | --- | --- |
| [NIST AI RMF1.0 GOVERN](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) | Roles, policy, escalation, review | DoR/protected-path checks; accountability human | AGENTS; ADD; policies | Governance |
| RMF MAP | Context, intended purpose and affected groups | Required intent/design sections | intent; design | Product |
| RMF MEASURE | Quality, safety, validity and limitations | Comparable eval evidence; not checklist scoring | evals; metrics; model cards | Evaluation lead |
| RMF MANAGE | Treatment, monitoring, retirement | Proposal-only monitoring, authorized runbooks | monitoring; runbooks | Operations |
| [NIST AI600-1 (2024) GenAI profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Context-selected information-integrity, privacy, security, supply-chain and human-oversight actions | Record applicable action IDs during project assessment; no invented universal action set | nist-rmf/control-map.md | AI risk owner |
| [GDPR Art5/6](https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng) | Purpose, minimisation, storage limitation, valid legal basis | Required compliance metadata; legal basis assessed by controller | gdpr/records-and-dpia.md | Controller |
| GDPR Art13 | Collection-time transparency incl retention criteria | Notice review and user-flow tests | user notices | Controller |
| GDPR Art30 | Role-appropriate records of processing | Ledger and every personal-data system evaluated separately | gdpr/records-and-dpia.md | Controller/processor |
| GDPR Art35 | High-risk processing DPIA trigger | Intake checklist; DPO advice where designated, not universal DPO approval | DPIA record | Controller + DPO advice |
| [BetrVG87(1)(6)](https://www.gesetze-im-internet.de/betrvg/__87.html) | Co-determination for applicable employee monitoring | Assessment before monitoring; no fixed statutory log days invented | betrvg/co-determination.md | Employer + works council |
| [NIS2 Arts20/21/23](https://eur-lex.europa.eu/eli/dir/2022/2555/2022-12-27/eng) | Entity scope, management, cybersecurity and incident duties | Human scope decision; national implementation required | posture; incident records | Entity management |
| [BSIG28/30/32/38](https://www.gesetze-im-internet.de/bsig_2025/) | German entity/management/controls/reporting | Do not equate24h/72h/1month reporting with retention | posture; incident records | German entity owner |
| [ISO/IEC42001:2023](https://www.iso.org/standard/81230.html) | Management-system mapping pending official clause list | **Unverified by user exception; no clause numbers or certification claim** | iso42001/CLAUSES-UNVERIFIED.md | Compliance |
| [OSPS Baseline2026.08.28](https://baseline.openssf.org/versions/2026-08-28/) | Access, change/review and dependency controls | Existing CI plus planned required-check rollout; nonauthor human review | CI; ruleset; review records | Repository admin |
| [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md) | Repository-risk evidence | Real Scorecard run pending; no generated score asserted | CI artifacts when enabled | Security |

## OWASP LLM risks

Source: [OWASP LLM Top10, current2026 edition](https://genai.owasp.org/llm-top-10/),
not the differently numbered2025 list. These are candidate controls requiring tests.

| ID / risk | Artifact / gate | Automation / evidence | Owner |
| --- | --- | --- | --- |
| LLM01 Prompt injection | External tool authorization, untrusted input boundaries | Guardian fixtures + project injection evals | Security |
| LLM02 Sensitive information disclosure | Data minimisation, retrieval authorization, log redaction | Data contracts and leakage evals | Data/security |
| LLM03 Excessive agency | Minimal tools, approval, budgets | Guardian and declared roster; runtime validation pending | Platform |
| LLM04 Supply-chain failures | Pin models/prompts/dependencies; provenance | AI supply-chain inventory and scanning | Platform |
| LLM05 Data/model poisoning | Dataset provenance and validated splits | Data-card review and poisoning evals | ML |
| LLM06 Unbounded consumption | Time, steps, tokens and cost ceilings | Budget tests and calibrated bands | Operations |
| LLM07 Misinformation | Grounding and supported claims | Groundedness/error-analysis evals | Evaluation lead |
| LLM08 Hidden context risks | Scoped memory/context; trust between agents | Memory review and cross-agent injection cases | AI engineer |
| LLM09 Vector/embedding weaknesses | Retrieval access and index integrity | Tenant-filter and retrieval-quality tests | Retrieval owner |
| LLM10 Improper output handling | Validate before rendering/querying/executing | Contract/injection tests; no direct model-to-shell path | Application owner |

Agentic guidance adds inter-agent trust, identity, tool permissions and containment;
use the [read agentic source](https://genai.owasp.org/download/52117/?tmstv=1765059207).
ReviewerL9 rechecks these controls. A deployment claim requires actual evidence,
not merely this mapping.
