#!/usr/bin/env python3
"""Compute SWP + hours for every backlog node and print the per-epic summary.

SWP source: finalSWP of leaves in the estimate-swp HTML report (reviewed), plus
backlog/swp-overrides.yaml for sub-issues split after scoring. Parents = sum of
children (no re-scoring). Leaf hours = SWP x HOURS_PER_SWP[layer], layer = title tag
([FE...] -> FE, else default); parent hours = sum of children (see estimate.md §3).
Writes backlog/estimates.json (read by the push script and the sprint simulation).
Usage: python3 scripts/compute-estimates.py <report.html>
"""
import json, re, sys
from pathlib import Path

import yaml

HOURS_PER_SWP = {"FE": 5.5, "default": 3.0}  # calibrated from 11 direct-estimated samples
ROOT = Path(__file__).resolve().parent.parent
DATA = yaml.safe_load((ROOT / "backlog" / "backlog.yaml").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "backlog" / "github-issue-map.json").read_text())
OVERRIDES = yaml.safe_load((ROOT / "backlog" / "swp-overrides.yaml").read_text(encoding="utf-8"))


def report_payload(html_path):
    """The validated JSON payload embedded in the estimate-swp HTML report."""
    text = Path(html_path).read_text(encoding="utf-8")
    return json.loads(re.search(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', text, re.S).group(1))


def leaf_swp(html_path):
    num2key = {v["number"]: k for k, v in STATE["issues"].items()}
    out = {num2key[int(r["issueRef"].rsplit("#", 1)[1])]: r["finalSWP"]
           for r in report_payload(html_path)["issues"] if r.get("finalSWP") is not None}
    for parent, subs in OVERRIDES["split_from_report"].items():
        assert sum(s["swp"] for s in subs.values()) == out.pop(parent), f"{parent}: split must keep total"
        out.update({k: s["swp"] for k, s in subs.items()})
    return out


def layer_rate(title):
    return HOURS_PER_SWP["FE"] if title.startswith("[FE") else HOURS_PER_SWP["default"]


def compute(html_path):
    """items: key -> (swp, hours); epics: per-epic totals incl. driving-2024 share."""
    leaf = leaf_swp(html_path)
    items, epics = {}, []
    for e in DATA["epics"]:
        tot = dict(swp=0, hours=0.0, leaves=0, constraint_swp=0, constraint_hours=0.0, fe_swp=0)
        for i in e["issues"]:
            con = bool(e.get("constraint") or i.get("constraint"))
            for n in i.get("subs") or [i]:
                swp = leaf[n["key"]]
                items[n["key"]] = (swp, swp * layer_rate(n["title"]))
                tot["leaves"] += 1
                tot["fe_swp"] += swp if n["title"].startswith("[FE") else 0
                if con or n.get("constraint"):
                    tot["constraint_swp"] += swp
                    tot["constraint_hours"] += items[n["key"]][1]
            if i.get("subs"):
                kids = [items[s["key"]] for s in i["subs"]]
                items[i["key"]] = (sum(k[0] for k in kids), sum(k[1] for k in kids))
            tot["swp"] += items[i["key"]][0]
            tot["hours"] += items[i["key"]][1]
        items[e["key"]] = (tot["swp"], tot["hours"])
        epics.append(dict(key=e["key"], title=e["title"], release=e["release"], issues=len(e["issues"]), **tot))
    missing = set(leaf) - set(items)
    assert not missing, f"report rows not in backlog: {missing}"
    return items, epics


def main():
    items, epics = compute(sys.argv[1])
    out = {"hours_per_swp": HOURS_PER_SWP, "source_report": Path(sys.argv[1]).name,
           "items": {k: {"swp": s, "hours": round(h, 1)} for k, (s, h) in items.items()},
           "epics": epics}
    (ROOT / "backlog" / "estimates.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print("| Epic | Số issue (lá) | Tổng SWP | Tổng giờ | Trong đó giờ lái 2024: SWP / giờ |")
    print("|---|---|---|---|---|")
    for e in epics:
        con = f"{e['constraint_swp']} / {e['constraint_hours']:,.0f}" if e["constraint_swp"] else ""
        print(f"| {e['key']} {e['title']} | {e['issues']} ({e['leaves']}) | {e['swp']} | {e['hours']:,.0f} | {con} |")
    tot = lambda f: sum(e[f] for e in epics)
    print(f"| **Tổng** | {tot('issues')} ({tot('leaves')}) | {tot('swp')} | {tot('hours'):,.0f} | "
          f"{tot('constraint_swp')} / {tot('constraint_hours'):,.0f} |")
    r1 = [e for e in epics if e["release"] == "R1"]
    print(f"\nR1: {sum(e['swp'] for e in r1)} SWP = {sum(e['hours'] for e in r1):,.0f} giờ; "
          f"FE {tot('fe_swp')} SWP · R1.1 (chỉ viết spec): {tot('swp') - sum(e['swp'] for e in r1)} SWP")


if __name__ == "__main__":
    main()
