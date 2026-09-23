# GE103 Mastery Dashboard Dataset (2023)

Self-reported vs viva-verified task mastery from a large first-year programming
course (GE103, 2023) run on a no-cost Google Sheets mastery dashboard. Students
worked through a 60-task ladder ("Ocean 1"–"Ocean 60"), self-reported completion,
and every claim was examined by a teaching assistant in a viva. The dataset pairs
the full self-report grid with the full viva-verdict grid, plus roster, TA
workload, a cell-edit audit trail, and a one-month activity time series.

## At a glance

| | |
|---|---|
| Learners (analysis population) | 203 (first-year B.Tech, five branches) |
| Task ladder | 60 tasks, depth-weighted (capstones O45, O60) |
| Self-report cells | 12,180 (11,093 claimed `1` / 1,087 `0`; zero blanks) |
| Viva-verdict cells | 12,660 across 211 TA-tracked rows (zero blanks) |
| Over-claims (claimed, not demonstrated at viva) | 208 (confirmation rate 98.1%) |
| Teaching assistants | 12 (16–18 mentees each, ≈1:17 ratio) |
| Activity log window | 24 Aug – 25 Sep 2023 (1,740 snapshots) |
| Edit audit trail | 499 timestamped cell edits |
| License | MIT — fully open download, no access request |

## Files

| File | Rows | Contents |
|---|---|---|
| `data/self_reported_claims.csv` | 203 | student × O01–O60 self-reported claim (1/0) |
| `data/viva_verified.csv` | 211 | student × O01–O60 TA viva verdict (1/0) |
| `data/branch_leaderboards.csv` | 203 | per-branch rank-ordered standings as shown on the live dashboard |
| `data/roster.csv` | 203 | branch, mentor, self-reported %, predicted-grade band |
| `data/mentor_load.csv` | 12 | per-TA mentee count, progress %, evaluated %, pending % |
| `data/edit_history.csv` | 499 | timestamped sheet edits (who changed which cell to what) |
| `data/activity_log.csv` | 1,740 | cumulative self-reported-Yes count over time |
| `docs/task_ladder.md` | 60 | per-task depth weights + 500-scale cumulative credit |
| `docs/DESCRIPTIVE_STATS.md` | — | descriptive statistics for every file |
| `docs/CHALLENGE_QUESTIONS.md` | — | reference challenge tasks (C1–C3) |
| `scripts/recompute_results.py` | — | reproduces every published headline statistic |

## Schema and coverage

**`self_reported_claims.csv`** — `student_id` (G####), `O01`…`O60` ∈ {1, 0}.
100% coverage, no blanks. A 1 means the student marked the task complete on the
dashboard.

**`viva_verified.csv`** — `student_id`, `O01`…`O60` ∈ {1, 0}. 100% coverage.
A 1 means the TA confirmed mastery at viva. **Verification was gated on the
claim**: TAs examined every claimed task, so `verified & ~claimed = 0` by
construction — students can only over-claim, never under-claim. Contains 8 rows
for students TAs tracked who never appear in the self-report grid; the analysis
population is the 203-student join (see `scripts/recompute_results.py`).

**`roster.csv`** — `student_id`, `branch` (CSE 84 / M&C 35 / Chemical 33 / Civil 31 /
AI 20), `mentor_id` (M##), `pct_complete_self_reported`,
`pct_demonstrated_viva`, `predicted_grade` (dashboard's informal band: Average /
Below Average / Needs Attention / Needs More Attention). The band is a simple
threshold on the self-reported completion percentage reached — observed ranges:
Average 80.25–100, Below Average 57.41–79.63, Needs Attention 37.65–54.94,
Needs More Attention below that. It is an instructor heuristic ("only for fun"
in the original sheet), not an official grade, and is unrelated to viva results.
100% coverage on all columns. Both percentage columns use the same depth-weighted convention
(weights in `docs/task_ladder.md`): the self-reported column is the dashboard's
own figure over claimed tasks; `pct_demonstrated_viva` was **derived during
release preparation** (it appears in no source sheet) over tasks both claimed
and TA-confirmed at viva. Their per-student difference is the self-assessment
calibration gap studied in the companion paper.

**`mentor_load.csv`** — `mentor_id`, `students_mentored` (16–18; the 12 counts
sum to the 211 TA-tracked students), `pct_progress_mean`, `pct_evaluated_mean`,
`pct_pending`. Snapshot at export time; the source sheet's computed summary rows
(totals, averages, slope, per-branch mean/SD) are not released.

**`edit_history.csv`** — `timestamp` (ISO 8601), `action` (Edit), `sheet`, `cell`,
`new_value`, `editor_id` (G####/M##/XE001 tokens). Spans 2023-08-30 to 2025-07-25;
edits after Sep 2023 are post-course instructor housekeeping.

**`activity_log.csv`** — `timestamp`, `total_yes_count`, `yes_since_log_start`,
`new_yes_since_previous`. Running total of self-reported Yes cells across the
whole grid. Logging started mid-course, when 5,579 Yes cells already existed,
and ran for one month (total 5,579 → 11,093); `yes_since_log_start` counts Yes
cells recorded since the first log snapshot (`total_yes_count` − 5,579 on every
row). `new_yes_since_previous` is the Yes cells added since the preceding
snapshot (0 on the first row); the source sheet stored this delta only for the
most recent 998 snapshots — the remainder were computed by differencing the
totals, and every stored value was verified to match. A constant "Seen"
review-marker column from the source sheet was dropped. Cumulative snapshots,
not per-edit events.

## Collection and preparation

The course dashboard was a Google Sheet with Apps Script automation: students
edited their own row of the self-report grid; TAs recorded viva verdicts in a
mirrored grid; summary tabs derived progress, per-branch views, and TA workload.
The dataset is a cleaned export of that workbook:

- Sheets carried as-is (values only): the two claim grids, roster, TA progress,
  edit history, activity log.
- Spreadsheet artifacts removed: footer weight/index rows (moved to
  `docs/task_ladder.md`), padded blank rows, stray computed cells, a reversed
  duplicate copy of the activity-log series.
- **Not released**: a "Peer-Instruction" tab (its data columns were never filled
  in — 100% empty) and a "Dashboard-Mentors" tab (exact duplicate of the roster
  columns).
- The five per-branch leaderboard tabs are released as
  `data/branch_leaderboards.csv` (rank order preserved, identifiers tokenized).
  Note: rank positions were visible to the class while the course ran, so a
  classmate who remembers standings could in principle locate a peer's row;
  tokens still resolve to no real-world identity.
- Every CSV also ships as a Parquet mirror in `data/parquet/` for
  `load_dataset()`-style loading. There are **no train/test splits** by design
  (n=203; use cross-validation — see `docs/CHALLENGE_QUESTIONS.md`).

## Anonymization

All person identifiers are opaque tokens assigned by the export pipeline:
students `G####`, teaching assistants `M##`, instructor `XE001`. Real names,
registration numbers, and email addresses were removed and the release was swept
against the full identity keymap (zero residuals). The tokens **cannot be
resolved to public profiles and are not suitable for individual-level
identification**; they exist only to join rows across files.

## Suggested uses / benchmark tasks

Published baselines exist for each (see Citation):

1. **Calibration / over-claim modelling** — predict which claims fail viva.
   Over-claiming is heavily concentrated (Gini 0.847; the worst decile of
   students accounts for 67% of over-claims) and rises with task difficulty
   (all top-drift tasks in the O52–O60 tail).
2. **Verification-effort targeting** — all 208 over-claims sit on capstone-tail
   rungs; verifying ~12–20% of claims catches 100% of them. Can smarter
   policies do better with less?
3. **Early-signal prediction** — predict final demonstrated mastery from the
   first weeks of `activity_log.csv` + `edit_history.csv`.
4. **Psychometrics** — the 60-item grid supports scale/IRT analysis (KR-20 0.94
   but heavily ceilinged; discrimination lives in O45–O60).

## Limitations

- Person tokens are opaque; no demographics beyond branch. Not suitable for
  individual-level analysis.
- Verification is gated on claims: under-claiming is unobservable, so agreement
  statistics like Cohen's κ are degenerate by design.
- The activity log covers ~1 month of a longer course — the core of the
  intervention, not its entirety.
- Dashboard participation counted toward 50% of the course grade; engagement
  numbers should not be read as purely voluntary behaviour.
- Single course, single institution, 2023 cohort; the structure transfers, the
  numbers are local.
- Depth weights are instructor judgement, not a validated difficulty metric.

## Ethics and access

Fully open download. Every person identifier is an opaque token (see Anonymization); no names, registration numbers or email addresses exist anywhere in the release. Institutional ethics review for public release is in process at IIT Ropar.

## Citation

> GE103 Mastery Dashboard Dataset (2023). Vicharanashala, IIT Ropar. 2026. https://github.com/vicharanashala/ge103-mastery-dashboard-dataset

Companion papers (under review):

1. *Mastery-Based Learning with a No-Cost Spreadsheet Dashboard in a Large First-Year Programming Course: A Practice Report.*
2. *Self-Reported versus Viva-Verified Mastery in a Large First-Year Programming Course.*

## License

MIT License. You are free to use, modify and distribute the data, including for commercial purposes, subject to the standard MIT terms (see `LICENSE`).

## About

Maintained by Vicharanashala, the learning-systems lab at IIT Ropar. Mirrors of this dataset: Kaggle, Hugging Face and AIKosh (links added as each goes live).
