# Protected evaluation contract

Each suite names requirement/incident IDs, dataset version/hash, prompt hashes,
pinned model/deployment, grading rubric, evaluator version, calibrated threshold,
sample size, known limitations and protected owner. Every incident adds a
regression case under human-authorized review.

Cover task success, groundedness, leakage/injection, safety, adversarial/edge
robustness, fairness where relevant and baseline regressions. Missing labels,
execution errors and partial results are separate from failing or passing quality.
Record grader calibration with human-labeled examples; do not tune away failures
on the same held-out set. No application eval outcomes are asserted by this scaffold.
