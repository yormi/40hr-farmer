"""Validate + lint a decision tree, then run an offline demo conversation.
Usage: python validate.py profit-funnel.json [--publish] [--demo]"""
import json, re, sys
from jsonschema import Draft202012Validator
from interpreter import parse_expr, Interpreter, TPL, WAITING

def refs(nid, n):
    for k in ("next", "on_fail", "else", "on_error"):
        if k in n: yield k, n[k]
    for b in n.get("branches", []): yield "branch", b["next"]
    for o in n.get("options", []): yield f"option:{o['id']}", o["next"]
    if "on_fail" in n.get("no_match", {}): yield "no_match", n["no_match"]["on_fail"]

def lint(t, publish):
    errs, warns, nodes = [], [], t["nodes"]
    consts, vars_ = t.get("constants", {}), t.get("variables", {})
    starts = [t["start"]] + [x["start"] for x in t.get("triggers", [])] + [g["goto"] for g in t.get("global_intents", [])]
    for s in starts:
        if s not in nodes: errs.append(f"entry point -> missing node '{s}'")
    for nid, n in nodes.items():
        for k, tgt in refs(nid, n):
            if tgt not in nodes: errs.append(f"{nid}.{k} -> missing node '{tgt}'")
        for v in [n.get("var")] + list(n.get("save", {}).values()) + list(n.get("assign", {}).keys()):
            if v and v not in vars_: errs.append(f"{nid}: undeclared variable '{v}'")
        exprs = list(n.get("assign", {}).values()) + [b["when"] for b in n.get("branches", [])]
        for e in exprs:
            try: parse_expr(e)
            except Exception as ex: errs.append(f"{nid}: bad expression {e!r}: {ex}")
        texts = json.dumps(n)
        for name in set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", " ".join(exprs)) + [m[0] for m in TPL.findall(texts)]):
            if name.isupper() and name in consts and consts[name] is None:
                (errs if publish else warns).append(f"{nid}: constant {name} is not set")
            elif not name.isupper() and not name.startswith(("contact.", "sys.")) and name not in vars_:
                errs.append(f"{nid}: unknown name in template '{name}'")
        qr = len([o for o in n.get("options", []) if o.get("show", True)]) + len(n.get("quick_replies", []))
        if n["type"] in WAITING and not n.get("hide_persistent"): qr += len(t.get("persistent_quick_replies", []))
        if qr > 13: errs.append(f"{nid}: {qr} quick replies (max 13)")
    PASS = {"message", "set", "condition", "action"}  # cycles made only of pass-through nodes never wait -> infinite loop
    def cyc(x, path):
        if x in path: errs.append("pass-through cycle: " + " -> ".join(path[path.index(x):] + [x])); return
        if x in nodes and nodes[x]["type"] in PASS:
            for _, tgt in refs(x, nodes[x]): cyc(tgt, path + [x])
    for x in nodes: cyc(x, [])
    seen, todo = set(), list(starts)           # reachability
    while todo:
        x = todo.pop()
        if x in seen or x not in nodes: continue
        seen.add(x); todo += [tgt for _, tgt in refs(x, nodes[x])]
    warns += [f"unreachable node '{x}'" for x in nodes if x not in seen]
    return list(dict.fromkeys(errs)), warns

def demo(t):
    t = json.loads(json.dumps(t))
    t["constants"].update(BOOKING_URL="https://cal.example/guillaume", MASTERCLASS_URL="https://mc.example",
                          BENCHMARK_PER_SQFT=12,
                          SLACK_HANDOFF_WEBHOOK_URL="https://hooks.slack.com/example", SLACK_PHIL_USER_ID="U000PHIL")
    def ai(kind, node, text, scope, option_ids):          # stub standing in for Claude
        if kind == "classify":
            return {"status": "ok", "value": "greenhouse_tomatoes"} if "tomato" in text.lower() else {"status": "none"}
        if "save" in node: return {"status": "ok", "value": {"country": "CA", "region": "Ontario", "is_english": True}}
        m = re.search(r"([\d.]+)\s*k", text.lower())
        return {"status": "ok", "value": float(m.group(1)) * 1000 * (0.73 if node["var"] == "season_sales" else 1)} if m else \
               {"status": "retry", "followup": "Could you give me a rough number, e.g. $120k?"}
    def mc(method, body):
        if method == "sendContent":
            c = body["data"]["content"]
            print("  BOT:", " | ".join(m.get("text", m.get("url", "")) for m in c["messages"]),
                  ("  [" + ", ".join(q["caption"] for q in c.get("quick_replies", [])) + "]") if c.get("quick_replies") else "")
        elif method == "pace":
            print(f"  (wait {body.get('delay_ms')}ms · {body.get('reason', 'pace')})")
        elif method == "typing_on":
            print("  (typing… — verify Instagram support)")
        elif method == "notify_slack":
            print("  SLACK:")
            print("\n".join("    " + ln for ln in body.get("text", "").splitlines()))
        elif method != "setCustomFieldByName": print(f"  ({method}: {body.get('tag') or body.get('event') or ''})")
    store = {}; it = Interpreter(t, store, mc, ai)
    print("--- happy path ---")
    for ev in [{"trigger": "profit_comment", "text": "PROFIT"}, {"text": "we grow tomatoes in 2 greenhouses"},
               {"text": "Ontario"}, {"text": "decent"}, {"text": "about 200k"}, {"text": "30k sq ft"}, {"text": "Refine my numbers"}]:
        print("LEAD:", ev["text"]); it.handle_inbound({"contact_id": "123", "name": "Sam", "ig_handle": "samfarms", **ev})
    print("final vars:", store["123"]["vars"])
    print("--- handoff path ---")
    for ev in [{"trigger": "profit_comment", "text": "PROFIT"}, {"text": "Talk to Guillaume"}]:
        print("LEAD:", ev["text"]); it.handle_inbound({"contact_id": "456", "name": "Alex", "ig_handle": "alextomatoes", **ev})
    print("handoff flag:", store["456"]["human_handoff"])

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "profit-funnel.json"
    tree, schema = json.load(open(path)), json.load(open("decision-tree.schema.json"))
    Draft202012Validator.check_schema(schema)
    schema_errs = sorted(Draft202012Validator(schema).iter_errors(tree), key=lambda e: list(e.path))
    for e in schema_errs: print("SCHEMA:", "/".join(map(str, e.path)), "-", e.message[:200])
    errs, warns = lint(tree, "--publish" in sys.argv)
    for e in errs: print("LINT ERROR:", e)
    for w in warns: print("LINT WARN:", w)
    print("VALID" if not schema_errs and not errs else "INVALID", f"({len(tree['nodes'])} nodes)")
    if "--demo" in sys.argv: demo(tree)
    sys.exit(1 if schema_errs or errs else 0)
