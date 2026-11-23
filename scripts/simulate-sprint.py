#!/usr/bin/env python3
"""Sprint simulation: Iteration field, statuses on the Project, burndown + tables for progress-report.md.

Source of truth: sprints/sprint-1-simulation.yaml (SIMULATED data, not real progress).
Commands (each idempotent):
  iteration  create the Iteration field (Sprint 1..N, 14 days each) if missing
  apply      set Iteration + Status + Phụ trách on sprint items; close Done issues, reopen others;
             parents/epics touched by the sprint -> In Progress
  report     write reports/sprint-1-burndown.svg and print the markdown tables
  verify     read the Project back and compare every sprint item with the YAML
Usage: python3 scripts/simulate-sprint.py <command>
"""
import datetime as dt, importlib.util, json, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("push", ROOT / "scripts" / "push-backlog-to-github-project.py")
push = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(push)
SIM = yaml.safe_load((ROOT / "sprints" / "sprint-1-simulation.yaml").read_text(encoding="utf-8"))
EST = json.loads((ROOT / "backlog" / "estimates.json").read_text())["items"]
NODES = {n["key"]: n for n in push.nodes()}
STATUSES = ["Done", "In Review", "In Progress", "Blocked", "Todo"]
REPO = f"{push.OWNER}/{push.REPO}"


def create_iteration(st):
    cfg, sprint = SIM["iteration"], SIM["sprint"]
    if cfg["field"] in st["fields"] and st["fields"][cfg["field"]].get("iterations"):
        print("iteration field exists"); return
    start = dt.date.fromisoformat(str(cfg["start"]))
    its = ",".join(f'{{title:"Sprint {k + 1}",startDate:"{start + dt.timedelta(days=14 * k)}",duration:{cfg["duration_days"]}}}'
                   for k in range(cfg["count"]))
    f = push.gql("mutation($p:ID!){createProjectV2Field(input:{projectId:$p,dataType:ITERATION,"
                 f'name:"{cfg["field"]}",iterationConfiguration:{{startDate:"{start}",duration:{cfg["duration_days"]},'
                 f"iterations:[{its}]}}}}){{projectV2Field{{... on ProjectV2IterationField{{id "
                 "configuration{iterations{id title startDate}}}}}}", p=st["project_id"])["createProjectV2Field"]["projectV2Field"]
    st["fields"][cfg["field"]] = {"id": f["id"], "options": {},
                                  "iterations": {i["title"]: i["id"] for i in f["configuration"]["iterations"]}}
    push.save_state(st)
    print("iteration field:", ", ".join(f"{i['title']} {i['startDate']}" for i in f["configuration"]["iterations"]), sprint["title"])


def set_iteration(st, item_id, title):
    f = st["fields"][SIM["iteration"]["field"]]
    push.gql("mutation($p:ID!,$i:ID!,$f:ID!,$v:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,"
             "itemId:$i,fieldId:$f,value:{iterationId:$v}}){projectV2Item{id}}}",
             p=st["project_id"], i=item_id, f=f["id"], v=f["iterations"][title])


def issue_state(num, want_closed):
    cur = push.gh("issue", "view", str(num), "-R", REPO, "--json", "state")["state"]
    if want_closed and cur == "OPEN":
        push.gh("issue", "close", str(num), "-R", REPO, "--reason", "completed", parse=False)
    elif not want_closed and cur == "CLOSED":
        push.gh("issue", "reopen", str(num), "-R", REPO, parse=False)


def apply(st):
    title = SIM["sprint"]["title"]
    for it in SIM["items"]:
        rec, n = st["issues"][it["key"]], NODES[it["key"]]
        set_iteration(st, rec["item"], title)
        push.set_select(st, rec["item"], "Status", it["status"])
        push.set_select(st, rec["item"], "Phụ trách (giả định)", n["role"])
        issue_state(rec["number"], it["status"] == "Done")
        print(f"#{rec['number']:>3} {it['key']:<8} {it['status']:<12} {n['role']}")
    touched = set(SIM.get("parents_in_progress", [])) | {NODES[it["key"]]["epic"]["key"] for it in SIM["items"]}
    for k in sorted(touched):
        push.set_select(st, st["issues"][k]["item"], "Status", "In Progress")
        if k in SIM.get("parents_in_progress", []):
            set_iteration(st, st["issues"][k]["item"], title)
    print("parents/epics In Progress:", ", ".join(sorted(touched)))


def rows():
    issues = push.load_state()["issues"]
    return [dict(it, role=NODES[it["key"]]["role"], swp=EST[it["key"]]["swp"], hours=EST[it["key"]]["hours"],
                 num=issues[it["key"]]["number"], constraint=NODES[it["key"]]["constraint"],
                 fe_rate=NODES[it["key"]]["node"]["title"].startswith("[FE")) for it in SIM["items"]]


def burndown(rs):
    days = SIM["sprint"]["workdays"]
    tot_s, tot_h = sum(r["swp"] for r in rs), sum(r["hours"] for r in rs)
    out = []
    for d in range(len(days) + 1):  # d = 0 is sprint start
        done = [r for r in rs if r.get("done_day") and r["done_day"] <= d]
        out.append(dict(day=d, date=str(days[d - 1]) if d else "bắt đầu", ideal=round(tot_s * (1 - d / len(days)), 1),
                        swp=tot_s - sum(r["swp"] for r in done), hours=tot_h - sum(r["hours"] for r in done)))
    return out


def svg(bd, path):
    W, H, L, R, T, B = 720, 380, 60, 24, 36, 64
    top = max(p["swp"] for p in bd)
    x = lambda d: L + (W - L - R) * d / (len(bd) - 1)
    y = lambda v: T + (H - T - B) * (1 - v / top)
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{L}" y="22" font-size="14" font-weight="bold" fill="#1f2328">Sprint 1 バーンダウン（模擬・残SWP）</text>']
    for v in range(0, top + 1, 10):
        g += [f'<line x1="{L}" y1="{y(v):.1f}" x2="{W - R}" y2="{y(v):.1f}" stroke="#d0d7de" stroke-width="1"/>',
              f'<text x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end" fill="#57606a">{v}</text>']
    for p in bd:
        lab = "開始" if p["day"] == 0 else p["date"][5:].replace("-", "/")
        g.append(f'<text x="{x(p["day"]):.1f}" y="{H - B + 18}" text-anchor="middle" fill="#57606a">{lab}</text>')
    pts = lambda k: " ".join(f'{x(p["day"]):.1f},{y(p[k]):.1f}' for p in bd)
    g += [f'<polyline points="{pts("ideal")}" fill="none" stroke="#8c959f" stroke-width="2" stroke-dasharray="6 5"/>',
          f'<polyline points="{pts("swp")}" fill="none" stroke="#cf222e" stroke-width="2.5"/>',
          *[f'<circle cx="{x(p["day"]):.1f}" cy="{y(p["swp"]):.1f}" r="3.5" fill="#cf222e"/>' for p in bd],
          f'<text x="{x(len(bd) - 1) - 4:.1f}" y="{y(bd[-1]["swp"]) - 10:.1f}" text-anchor="end" fill="#cf222e" '
          f'font-weight="bold">残 {bd[-1]["swp"]} SWP</text>',
          f'<line x1="{L}" y1="{H - 22}" x2="{L + 28}" y2="{H - 22}" stroke="#8c959f" stroke-width="2" stroke-dasharray="6 5"/>',
          f'<text x="{L + 34}" y="{H - 18}" fill="#1f2328">理想線</text>',
          f'<line x1="{L + 110}" y1="{H - 22}" x2="{L + 138}" y2="{H - 22}" stroke="#cf222e" stroke-width="2.5"/>',
          f'<text x="{L + 144}" y="{H - 18}" fill="#1f2328">実績（Done になった時点で減算）</text>', "</svg>"]
    path.write_text("\n".join(g) + "\n", encoding="utf-8")


def report(_st):
    rs, cap = rows(), SIM["sprint"]["capacity_hours_per_person"]
    print("| Status | Issue | SWP | Giờ ước lượng | Mục |\n|---|---|---|---|---|")
    for s in STATUSES:
        g = [r for r in rs if r["status"] == s]
        print(f"| {s} | {len(g)} | {sum(r['swp'] for r in g)} | {sum(r['hours'] for r in g):g} | "
              + ", ".join(f"#{r['num']} {r['key']}" for r in g) + " |")
    print(f"| Tổng | {len(rs)} | {sum(r['swp'] for r in rs)} | {sum(r['hours'] for r in rs):g} | |")
    print("\n| Vai | Nhận (giờ) | Capacity | Done (giờ ước) | Giờ thực tế của mục Done |\n|---|---|---|---|---|")
    for role in SIM["sprint"]["team"]:
        g = [r for r in rs if r["role"] == role]; d = [r for r in g if r["status"] == "Done"]
        print(f"| {role} | {sum(r['hours'] for r in g):g} | {cap} | {sum(r['hours'] for r in d):g} | {sum(r['actual'] for r in d)} |")
    bd = burndown(rs)
    print("\n| Ngày | Ngày làm | Lý tưởng (SWP) | Còn lại SWP | Còn lại giờ |\n|---|---|---|---|---|")
    for p in bd:
        print(f"| {p['date']} | {p['day']} | {p['ideal']:g} | {p['swp']} | {p['hours']:g} |")
    done = [r for r in rs if r["status"] == "Done"]
    est, act = sum(r["hours"] for r in done), sum(r["actual"] for r in done)
    print(f"\nDone: {sum(r['swp'] for r in done)} SWP · giờ ước {est:g} · thực tế {act} · thực tế/ước = {act / est:.2f}")
    for lab, f in (("Mục do BE làm", lambda r: r["role"].startswith("BE")), ("Mục do FE làm (việc [BE])", lambda r: r["role"].startswith("FE")),
                   ("BrSE/QA", lambda r: r["role"] in ("BrSE", "QA-1"))):
        g = [r for r in done if f(r)]
        print(f"  {lab}: ước {sum(r['hours'] for r in g):g} · thực tế {sum(r['actual'] for r in g)}")
    con = [r for r in rs if r["constraint"]]
    print("Ràng buộc giờ lái 2024 trong sprint:", ", ".join(f"#{r['num']} {r['key']} ({r['status']})" for r in con))
    svg(bd, ROOT / "reports" / "sprint-1-burndown.svg")
    print("written reports/sprint-1-burndown.svg")


def verify(st):
    q = ("query($p:ID!,$c:String){node(id:$p){... on ProjectV2{items(first:100,after:$c){pageInfo{hasNextPage endCursor} "
         "nodes{id fieldValues(first:30){nodes{... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}} "
         "... on ProjectV2ItemFieldIterationValue{title field{... on ProjectV2FieldCommon{name}}}}}}}}}}")
    vals, cur = {}, None
    while True:
        args = {"p": st["project_id"], **({"c": cur} if cur else {})}
        page = push.gql(q, **args)["node"]["items"]
        for it in page["nodes"]:
            vals[it["id"]] = {v["field"]["name"]: v.get("name") or v.get("title") for v in it["fieldValues"]["nodes"] if v}
        if not page["pageInfo"]["hasNextPage"]:
            break
        cur = page["pageInfo"]["endCursor"]
    bad = []
    for it in SIM["items"]:
        v = vals[st["issues"][it["key"]]["item"]]
        want = {"Status": it["status"], "Iteration": SIM["sprint"]["title"], "Phụ trách (giả định)": NODES[it["key"]]["role"]}
        bad += [f"{it['key']} {k}: {v.get(k)} != {w}" for k, w in want.items() if v.get(k) != w]
    in_sprint = sum(1 for v in vals.values() if v.get("Iteration") == SIM["sprint"]["title"])
    print(f"project items: {len(vals)} · in {SIM['sprint']['title']}: {in_sprint} · mismatches: {len(bad)}")
    print("\n".join(bad) or "all sprint items match the YAML")


if __name__ == "__main__":
    state = push.load_state()
    {"iteration": create_iteration, "apply": apply, "report": report, "verify": verify}[sys.argv[1]](state)
