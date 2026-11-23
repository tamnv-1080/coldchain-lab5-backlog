#!/usr/bin/env python3
"""Publish backlog/backlog.yaml to a GitHub repo + user ProjectV2 (idempotent).

Steps (each safe to re-run; state kept in backlog/github-issue-map.json):
  project  create/link the Project, its custom fields and labels
  issues   create epics, issues, sub-issues in dependency order; add to Project;
           set single-select fields; link parent/sub-issue and blocked-by
Usage: python3 scripts/push-backlog-to-github-project.py project|issues
Needs: gh authenticated with scopes repo + project.
"""
import json, subprocess, sys, time
from pathlib import Path

import yaml

OWNER, REPO = "tamnv-1080", "coldchain-lab5-backlog"
PROJECT_TITLE = "Product B — LAB-5 Backlog (cold chain)"
ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "backlog" / "github-issue-map.json"
DATA = yaml.safe_load((ROOT / "backlog" / "backlog.yaml").read_text(encoding="utf-8"))
SELECT_FIELDS = {  # field name -> options
    "Phụ trách (giả định)": DATA["meta"]["roles"],
    "Release": ["R1", "R1.1"],
    "Ràng buộc đặc thù": ["Giờ lái 2024", "Không"],
    "Loại": ["Epic", "Issue", "Sub-issue"],
}
NUMBER_FIELDS = ["SWP", "Giờ ước lượng"]
LABELS = {"epic": "5319e7", "constraint:driving-2024": "d93f0b", "release:R1": "0e8a16",
          "release:R1.1": "fbca04", "clarification": "c5def5", "spike": "bfdadc",
          **{f"layer:{x}": "ededed" for x in ["db", "be", "fe", "qa", "infra", "doc", "brse"]}}


def gh(*args, parse=True):
    for attempt in range(4):  # retry transient network errors only
        proc = subprocess.run(["gh", *args], capture_output=True, text=True)
        if proc.returncode == 0 or not any(w in proc.stderr for w in ("connection reset", "timeout", "EOF", "502", "503")):
            break
        time.sleep(3 * (attempt + 1))
    out = proc.stdout
    if proc.returncode != 0 and not (args[:2] == ("api", "graphql") and out.strip().startswith("{")):
        raise RuntimeError(f"gh {' '.join(args[:3])}: {proc.stderr.strip()}")
    return json.loads(out) if parse and out.strip() else out


def gql(query, **variables):
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, (int, float)) else "-f", f"{k}={v}"]
    res = gh(*args)
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    return res["data"]


def gql_link(query, **variables):
    """Relationship mutations: ignore 'already linked' on re-run."""
    try:
        gql(query, **variables)
    except RuntimeError as err:
        if not any(w in str(err).lower() for w in ("already", "duplicate", "taken")):
            raise


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {"issues": {}}


def save_state(st):
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1) + "\n")


def setup_project(st):
    if "project_id" not in st:
        p = gh("project", "create", "--owner", OWNER, "--title", PROJECT_TITLE, "--format", "json")
        st.update(project_id=p["id"], project_number=p["number"], project_url=p["url"])
        save_state(st)
    num = str(st["project_number"])
    gh("project", "edit", num, "--owner", OWNER, "--visibility", "PUBLIC", parse=False)
    subprocess.run(["gh", "project", "link", num, "--owner", OWNER, "--repo", f"{OWNER}/{REPO}"],
                   capture_output=True)
    existing = {f["name"]: f for f in gh("project", "field-list", num, "--owner", OWNER,
                                         "--format", "json", "--limit", "50")["fields"]}
    for name, options in SELECT_FIELDS.items():
        if name not in existing:
            gh("project", "field-create", num, "--owner", OWNER, "--name", name,
               "--data-type", "SINGLE_SELECT", "--single-select-options", ",".join(options), parse=False)
    for name in NUMBER_FIELDS:
        if name not in existing:
            gh("project", "field-create", num, "--owner", OWNER, "--name", name,
               "--data-type", "NUMBER", parse=False)
    for name, color in LABELS.items():
        gh("label", "create", name, "--color", color, "--force", "-R", f"{OWNER}/{REPO}", parse=False)
    st["fields"] = {f["name"]: {"id": f["id"], "options": {o["name"]: o["id"] for o in f.get("options", [])}}
                    for f in gh("project", "field-list", num, "--owner", OWNER,
                                "--format", "json", "--limit", "50")["fields"]}
    save_state(st)
    print("project:", st["project_url"])


def nodes():
    """Yield dicts: key, kind, title, parent, epic, node (yaml), role, deps."""
    for e in DATA["epics"]:
        ec = bool(e.get("constraint"))
        yield dict(key=e["key"], kind="Epic", parent=None, epic=e, node=e, role=None, deps=[], constraint=ec)
        for i in e["issues"]:
            ic = ec or bool(i.get("constraint"))
            yield dict(key=i["key"], kind="Issue", parent=e["key"], epic=e, node=i,
                       role=i.get("role"), deps=i.get("deps", []), constraint=ic)
            for s in i.get("subs", []):
                yield dict(key=s["key"], kind="Sub-issue", parent=i["key"], epic=e, node=s,
                           role=s.get("role", i.get("role")), deps=s.get("deps", []),
                           constraint=ic or bool(s.get("constraint")))


def creation_order(all_nodes):
    """Parents before children, deps before dependants (stable by file order)."""
    by_key, done, order = {n["key"]: n for n in all_nodes}, set(), []
    def visit(n):
        if n["key"] in done:
            return
        done.add(n["key"])
        for k in ([n["parent"]] if n["parent"] else []) + n["deps"]:
            visit(by_key[k])
        order.append(n)
    for n in sorted(all_nodes, key=lambda x: x["kind"] != "Epic"):  # epics get #1..#12
        visit(n)
    return order


def layer_of(title):
    tag = title.split("]")[0].strip("[").split("+")[0].lower() if title.startswith("[") else "be"
    return "brse" if tag == "brse" else tag


def body_of(n, st):
    node, e, iss = n["node"], n["epic"], st["issues"]
    ref = lambda k: f"#{iss[k]['number']} `{k}`"
    lines = []
    if n["kind"] == "Epic":
        lines += [f"**Mục tiêu:** {e['goal']}", "", f"**Release:** {e['release']}"]
        if e.get("constraint"):
            lines += ["", "> ★ Epic chịu ràng buộc giới hạn giờ lái xe tải từ 2024: mỗi quy tắc một issue/sub-issue. "
                      "Việc ở epic khác cũng bị ràng buộc này chi phối mang label `constraint:driving-2024` "
                      "(lọc theo field \"Ràng buộc đặc thù\")."]
    else:
        lines += [f"**{'Epic' if n['kind'] == 'Issue' else 'Issue cha'}:** {ref(n['parent'])} · "
                  f"**Phụ trách (giả định):** {n['role']} · **Release:** {e['release']}"
                  + (" · **★ Ràng buộc giờ lái 2024**" if n["constraint"] else "")]
    if node.get("scope"):
        lines += ["", "### Phạm vi", *[f"- {x}" for x in node["scope"]]]
    if node.get("ac"):
        lines += ["", "### Điều kiện nghiệm thu", *[f"- [ ] {x}" for x in node["ac"]]]
    if n["deps"]:
        lines += ["", "### Phụ thuộc (phải xong trước)", *[f"- {ref(k)}" for k in n["deps"]]]
    if node.get("subs"):
        lines += ["", "Issue này chỉ gom các sub-issue; SWP và giờ ước lượng nằm ở sub-issue."]
    lines += ["", "### Tài liệu thiết kế LAB-4", *[f"- {x}" for x in node.get("spec", [])],
              "", "---", f"Mã backlog: `{n['key']}` · Định nghĩa xong: xem `task-breakdown.md` §1 trong repo."]
    return "\n".join(lines)


def labels_of(n):
    e = n["epic"]
    out = [f"release:{e['release']}"] + (["constraint:driving-2024"] if n["constraint"] else [])
    if n["kind"] == "Epic":
        return out + ["epic"]
    return out + [f"layer:{layer_of(n['node']['title'])}"] + n["node"].get("labels", [])


def set_select(st, item_id, field, option):
    f = st["fields"][field]
    gql("mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,"
        "itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}}",
        p=st["project_id"], i=item_id, f=f["id"], o=f["options"][option])


def push_issues(st):
    all_nodes = list(nodes())
    for n in creation_order(all_nodes):
        k, rec = n["key"], st["issues"].get(n["key"])
        if rec and rec.get("done"):
            continue
        if not rec:
            title = f"{k} · {n['node']['title']}"
            url = gh("issue", "create", "-R", f"{OWNER}/{REPO}", "--title", title,
                     "--body", body_of(n, st), *sum((["--label", x] for x in labels_of(n)), []),
                     parse=False).strip()
            num = int(url.rsplit("/", 1)[1])
            node_id = gh("issue", "view", str(num), "-R", f"{OWNER}/{REPO}", "--json", "id")["id"]
            rec = st["issues"][k] = {"number": num, "id": node_id}
            save_state(st)
            time.sleep(1.2)  # stay under the content-creation secondary rate limit
        if "item" not in rec:
            rec["item"] = gql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c})"
                              "{item{id}}}", p=st["project_id"], c=rec["id"])["addProjectV2ItemById"]["item"]["id"]
            save_state(st)
        set_select(st, rec["item"], "Loại", n["kind"])
        set_select(st, rec["item"], "Release", n["epic"]["release"])
        set_select(st, rec["item"], "Ràng buộc đặc thù", "Giờ lái 2024" if n["constraint"] else "Không")
        if n["role"]:
            set_select(st, rec["item"], "Phụ trách (giả định)", n["role"])
        if n["parent"]:
            gql_link("mutation($a:ID!,$b:ID!){addSubIssue(input:{issueId:$a,subIssueId:$b}){issue{id}}}",
                a=st["issues"][n["parent"]]["id"], b=rec["id"])
        for d in n["deps"]:
            gql_link("mutation($a:ID!,$b:ID!){addBlockedBy(input:{issueId:$a,blockingIssueId:$b}){issue{id}}}",
                a=rec["id"], b=st["issues"][d]["id"])
        rec["done"] = True
        save_state(st)
        print(f"#{rec['number']:>3} {k}")


def report_payload(html_path):
    """Read the validated payload embedded in the estimate-swp HTML report."""
    import re
    text = Path(html_path).read_text(encoding="utf-8")
    return json.loads(re.search(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', text, re.S).group(1))


def set_number(st, item_id, field, value):
    gql("mutation($p:ID!,$i:ID!,$f:ID!,$v:Float!){updateProjectV2ItemFieldValue(input:{projectId:$p,"
        "itemId:$i,fieldId:$f,value:{number:$v}}){projectV2Item{id}}}",
        p=st["project_id"], i=item_id, f=st["fields"][field]["id"], v=value)


def set_swp(st, html_path):
    """Write reviewed finalSWP (leaves) and derived rollups (parents) to the SWP field."""
    pl = report_payload(html_path)
    by_number = {v["number"]: v for v in st["issues"].values()}
    rows = [(r["issueRef"], r["finalSWP"]) for r in pl["issues"] + pl["parents"] if r.get("finalSWP") is not None]
    for ref, swp in rows:
        set_number(st, by_number[int(ref.rsplit("#", 1)[1])]["item"], "SWP", swp)
    print(f"SWP written: {len(rows)} items, leaf total {sum(r['finalSWP'] for r in pl['issues'])}")


def preview(st, key):
    """Print title, labels and body of one node using placeholder issue numbers."""
    fake = {"issues": {n["key"]: {"number": i + 1} for i, n in enumerate(nodes())}}
    n = next(x for x in nodes() if x["key"] == key)
    print(f"{key} · {n['node']['title']}\nlabels: {labels_of(n)}\n\n{body_of(n, fake)}")


if __name__ == "__main__":
    state = load_state()
    if sys.argv[1] == "preview":
        preview(state, sys.argv[2])
    elif sys.argv[1] == "set-swp":
        set_swp(state, sys.argv[2])
    else:
        {"project": setup_project, "issues": push_issues}[sys.argv[1]](state)
