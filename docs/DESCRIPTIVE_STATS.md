# Descriptive statistics — GE103 Mastery Dashboard Dataset

Generated from the release files by the maintainers (reproduce any headline with
`scripts/recompute_results.py`). Analysis population: the **n=203** students present
in both grids (203 self-report rows, 211 viva rows).

## Mastery (unweighted task counts, n=203)
| metric | self-reported | viva-verified |
|---|---|---|
| mean tasks marked done (of 60) | 54.6 | 53.6 |
| median | 58.0 | 56.0 |
| sd | 7.1 | 7.2 |
| total Yes cells | 11093 | 10885 |

Weighted (depth-weighted ladder credit) headline: self mean 83.4 / median 84.6 / sd 18.1;
viva mean 81.8 / median 79.0 / sd 18.3; weighted median gap 5.6 pts.

## Over-claiming
- 208 over-claimed cells (claimed but not demonstrated) = 1.9% of 11093 claims → **98.1% confirmation rate**.
- 44/203 students (22%) have at least one over-claim.
- Most over-claimed tasks: O59 (34), O54 (33), O58 (31), O52 (27), O53 (27).
- By construction `verified & ~claimed = 0` (TAs examined claimed tasks only).

## Task ladder difficulty profile
- Task-level claim rate ranges 99/203 (O60) to 203/203 (O01).
- Sharpest participation drop after O42 (−45 students).

## Cohort composition (n=203)
- Branch: {'CSE': 84, 'AI': 20, 'Civil': 31, 'Chemical': 33, 'Mathematics & Computing': 35}
- Predicted-grade bands: {'Needs Attention': 14, 'Below Average': 72, 'Average': 116, 'Needs More Attention': 1}
- Mentors: 12 TAs, 16–18 mentees each.

## Leaderboards, edits, activity
- `branch_leaderboards.csv`: 203 rows across 5 branch tabs, rank order preserved from the live dashboard.
- `edit_history.csv`: 499 timestamped edits by 17 editors.
- `activity_log.csv`: 1740 snapshots, 24 Aug–25 Sep 2023 (one month of live usage).
