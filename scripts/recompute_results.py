#!/usr/bin/env python3
"""Reproduce every headline statistic of the GE103 papers from this release's files.

Run from anywhere:  python3 scripts/recompute_results.py

Analysis population = students present in roster.csv (branch-assigned) AND in both
claim grids: n = 203. Weighted mastery uses the depth weights in docs/task_ladder.md.

Expected output (papers' canonical numbers):
  self-reported  weighted mastery: mean 83.4  median 84.6
  viva-demonstrated               : mean 81.8  median 79.0
  viva confirmation rate          : 10885/11093 = 98.1% (208 over-claims)
"""
import csv, os, re, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
DATA = os.path.join(PKG, "data")


def load(name):
    rows = list(csv.reader(open(os.path.join(DATA, name))))
    return rows[0], rows[1:]


# depth weights from docs/task_ladder.md
W = [float(m.group(1)) for m in
     re.finditer(r"^\| O\d\d \| ([\d.]+) \|", open(os.path.join(PKG, "docs", "task_ladder.md")).read(), re.M)]
assert len(W) == 60
TOT = sum(W)

_, roster = load("roster.csv")
branch_of = {r[0]: r[1] for r in roster}

def grid(name):
    _, rows = load(name)
    return {r[0]: [c in ("Yes", "1") for c in r[1:61]] for r in rows}

SS, MM = grid("self_reported_claims.csv"), grid("viva_verified.csv")
students = sorted(s for s in branch_of if s in SS and s in MM)

def wpct(mask):
    return 100.0 * sum(W[i] for i in range(60) if mask[i]) / TOT

self_s, viva_s = [], []
claimed = confirmed = 0
for s in students:
    sm, mm = SS[s], MM[s]
    self_s.append(wpct(sm))
    viva_s.append(wpct([sm[i] and mm[i] for i in range(60)]))
    claimed += sum(sm)
    confirmed += sum(sm[i] and mm[i] for i in range(60))

print(f"population n={len(students)}")
for name, vals in (("self-reported ", self_s), ("viva-demonstr.", viva_s)):
    print(f"{name}: mean {statistics.mean(vals):.1f}  median {statistics.median(vals):.1f}  "
          f"sd {statistics.pstdev(vals):.1f}")
print(f"confirmation  : {confirmed}/{claimed} = {100*confirmed/claimed:.1f}%  "
      f"({claimed-confirmed} over-claims)")

print("\nbranch-wise weighted mastery (claimed / demonstrated):")
for b in ("CSE", "AI", "Mathematics & Computing", "Civil", "Chemical"):
    ids = [s for s in students if branch_of[s] == b]
    cl = statistics.mean(wpct(SS[s]) for s in ids)
    de = statistics.mean(wpct([SS[s][i] and MM[s][i] for i in range(60)]) for s in ids)
    print(f"  {b:24s} n={len(ids):3d}  {cl:5.1f} / {de:5.1f}")
