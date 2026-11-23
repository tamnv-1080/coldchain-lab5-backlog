#!/usr/bin/env python3
"""Validate backlog/backlog.yaml and print a Markdown summary.

Checks: unique keys, every dep points to an existing key, role in meta.roles,
leaf items have scope + ac. Exit code 1 when any check fails.
Usage: python3 scripts/validate-and-summarize-backlog.py [--full]
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
data = yaml.safe_load((ROOT / "backlog" / "backlog.yaml").read_text(encoding="utf-8"))
roles = set(data["meta"]["roles"])
errors, items = [], {}


def walk():
    """Yield (epic, issue, sub_or_None) for every node."""
    for epic in data["epics"]:
        for issue in epic["issues"]:
            yield epic, issue, None
            for sub in issue.get("subs", []):
                yield epic, issue, sub


for epic, issue, sub in walk():
    node = sub or issue
    if node["key"] in items:
        errors.append(f"duplicate key {node['key']}")
    items[node["key"]] = node
    role = node.get("role", issue.get("role"))
    if role not in roles:
        errors.append(f"{node['key']}: unknown role {role}")
    is_leaf = sub is not None or not issue.get("subs")
    if is_leaf and (not node.get("scope") or not node.get("ac")):
        errors.append(f"{node['key']}: leaf missing scope/ac")

for key, node in items.items():
    for dep in node.get("deps", []):
        if dep not in items:
            errors.append(f"{key}: dep {dep} not found")

def leaves(issue, inherited):
    """(key, constrained) of estimable leaves; flags inherit epic -> issue -> sub."""
    flag = inherited or bool(issue.get("constraint"))
    subs = issue.get("subs", [])
    return [(s["key"], flag or bool(s.get("constraint"))) for s in subs] or [(issue["key"], flag)]


print("| Epic | Tên | Issue | Sub-issue | Lá (đơn vị ước lượng) | Lá chịu ràng buộc giờ lái 2024 |")
print("|---|---|---|---|---|---|")
tot = [0, 0, 0, 0]
for epic in data["epics"]:
    n_issue = len(epic["issues"])
    n_sub = sum(len(i.get("subs", [])) for i in epic["issues"])
    lv = [x for i in epic["issues"] for x in leaves(i, bool(epic.get("constraint")))]
    n_con = sum(c for _, c in lv)
    tot = [tot[0] + n_issue, tot[1] + n_sub, tot[2] + len(lv), tot[3] + n_con]
    print(f"| {epic['key']} | {epic['title']} | {n_issue} | {n_sub} | {len(lv)} | {n_con or ''} |")
print(f"| **Tổng** | {len(data['epics'])} epic | {tot[0]} | {tot[1]} | {tot[2]} | {tot[3]} |")

if "--full" in sys.argv:
    for epic in data["epics"]:
        print(f"\n### {epic['key']} — {epic['title']}\n")
        for issue in epic["issues"]:
            print(f"- `{issue['key']}` {issue['title']} · {issue.get('role')}")
            for sub in issue.get("subs", []):
                print(f"  - `{sub['key']}` {sub['title']}")

if errors:
    print("\nERRORS:", *errors, sep="\n- ")
    sys.exit(1)
