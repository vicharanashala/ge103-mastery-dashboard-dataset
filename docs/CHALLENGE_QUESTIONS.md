# Challenge questions

Reference tasks for users of the dataset. There are deliberately **no train/test
splits** — n=203 is too small for pre-cut competition splits, so use
cross-validation and report your protocol. Baselines for C1 are published in the
accompanying paper; `scripts/recompute_results.py` reproduces the headline
numbers every challenge builds on.

## C1 — Predict viva-verified mastery from self-reports alone
Given a student's self-report row (O01–O60) and roster covariates (branch,
mentor), predict their viva-verified weighted mastery score. How much does the
self-report gap (the 1.9% over-claim rate) limit attainable accuracy? Report MAE
of the weighted score and cell-level F1 for over-claim detection.

## C2 — Where does the ladder break?
Using the task-level claim/verification profiles and the depth weights in
`docs/task_ladder.md`, locate the discontinuities in the 60-task ladder: which
tasks show the sharpest participation drops, and are the drops explained by task
depth, position, or something else? Propose (and justify) where a "relief rung"
should be inserted.

## C3 — Early-warning from the activity stream
`activity_log.csv` gives one month of cumulative-completion snapshots and
`edit_history.csv` the cell-level audit trail. Using only data up to day k, how
early can the final predicted-grade band (roster) be recovered? Report band
accuracy vs k.
