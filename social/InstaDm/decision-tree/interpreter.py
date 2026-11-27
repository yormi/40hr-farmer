"""Reference interpreter sketch for InstaDM DSL v1 (not production). ManyChat + Claude are injected callables (demo: validate.py)."""
import ast, re, time, hashlib
WAITING = {"ask", "choice"}

# ---------- expressions: a safe subset parsed with Python's ast + whitelist ----------
_FUNCS = {"min": min, "max": max, "abs": abs, "len": len, "round": lambda x, n=0: round(x, n) if n else round(x),
          "lower": lambda s: str(s).lower(), "is_set": lambda v: v is not None,
          "coalesce": lambda *a: next((x for x in a if x is not None), None)}
_OK = (ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.BinOp, ast.Add, ast.Sub,
       ast.Mult, ast.Div, ast.Mod, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn,
       ast.Constant, ast.List, ast.Name, ast.Load, ast.Call, ast.Attribute)

def parse_expr(src):
    tree = ast.parse(src, mode="eval")
    for n in ast.walk(tree):
        bad_call = isinstance(n, ast.Call) and not (isinstance(n.func, ast.Name) and n.func.id in _FUNCS)
        bad_dot = isinstance(n, ast.Attribute) and not (isinstance(n.value, ast.Name) and n.value.id in ("contact", "sys"))
        if not isinstance(n, _OK) or bad_call or bad_dot: raise ValueError(f"not allowed in expression: {ast.dump(n)[:60]}")
    return tree

KW = {"true": True, "false": False, "null": None}
def eval_expr(src, scope):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.List): return [ev(e) for e in n.elts]
        if isinstance(n, ast.Name): return KW[n.id] if n.id in KW else scope.get(n.id)
        if isinstance(n, ast.Attribute): return scope.get(f"{n.value.id}.{n.attr}")
        if isinstance(n, ast.BoolOp): return (all if isinstance(n.op, ast.And) else any)(ev(v) for v in n.values)
        if isinstance(n, ast.UnaryOp): v = ev(n.operand); return (not v) if isinstance(n.op, ast.Not) else -v
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if None in (a, b): raise ValueError("arithmetic on null")
            return {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b,
                    ast.Div: lambda: a / b, ast.Mod: lambda: a % b}[type(n.op)]()
        if isinstance(n, ast.Compare):
            left = ev(n.left)
            for op, rc in zip(n.ops, n.comparators):
                right = ev(rc)
                if isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) and None in (left, right): return False
                ok = {ast.Eq: lambda: left == right, ast.NotEq: lambda: left != right, ast.Lt: lambda: left < right,
                      ast.LtE: lambda: left <= right, ast.Gt: lambda: left > right, ast.GtE: lambda: left >= right,
                      ast.In: lambda: left in (right or []), ast.NotIn: lambda: left not in (right or [])}[type(op)]()
                if not ok: return False
                left = right
            return True
        if isinstance(n, ast.Call): return _FUNCS[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(type(n).__name__)
    return ev(parse_expr(src))

# ---------- templates: {{ name | filter:"arg" }} ----------
TPL = re.compile(r"\{\{\s*([A-Za-z_][\w.]*)\s*((?:\|\s*\w+(?::\"[^\"]*\")?\s*)*)\}\}")
FILTERS = {"money": lambda v, a: f"${v:,.0f}" if isinstance(v, (int, float)) else "", "number": lambda v, a: f"{v:,.0f}",
           "upper": lambda v, a: str(v).upper(), "lower": lambda v, a: str(v).lower(),
           "default": lambda v, a: a if v in (None, "") else v}

def render(text, scope):
    def sub(m):
        v = scope.get(m.group(1))
        for f in re.findall(r"\|\s*(\w+)(?::\"([^\"]*)\")?", m.group(2) or ""): v = FILTERS[f[0]](v, f[1])
        return "" if v is None else str(v)
    return TPL.sub(sub, text)

# ---------- interpreter ----------
class Interpreter:
    def __init__(self, tree, store, manychat, ai, sleep=None):
        self.t, self.store, self.mc, self.ai = tree, store, manychat, ai
        self.nodes, self.cfg = tree["nodes"], tree.get("config", {})
        self.sleep = sleep or (lambda ms: None)          # production sleeps; the demo prints delays only

    def scope(self, st):
        s = dict(self.t.get("constants", {})); s.update(st["vars"])
        s.update({"contact.id": st["contact_id"], "contact.first_name": st.get("name"),
                  "contact.ig_handle": st.get("ig_handle"),
                  "sys.tries": st["tries"], "sys.last_input": st.get("last_input")})
        return s

    def set_var(self, st, name, value):
        st["vars"][name] = value
        field = self.t.get("variables", {}).get(name, {}).get("manychat_field")
        if field: self.mc("setCustomFieldByName", {"subscriber_id": st["contact_id"], "field_name": field, "field_value": value})

    def handle_inbound(self, ev):                      # called from the queue worker, after the 200 was returned
        cid, text = ev["contact_id"], (ev.get("text") or "").strip()
        st = self.store.get(cid) or {"contact_id": cid, "node": None, "vars": {}, "tries": 0, "seen": {},
                                     "human_handoff": False, "transcript": []}
        st.setdefault("transcript", [])
        now = time.time()
        # v1: process events as they arrive (no dedup / per-contact queue; see Phase 2)
        st["send_gen"] = st.get("send_gen", 0) + 1        # cancels any in-flight paced send for this contact
        st["last_inbound_at"], st["name"], st["last_input"] = now, ev.get("name"), text
        if ev.get("ig_handle"): st["ig_handle"] = ev["ig_handle"]
        if text: st["transcript"].append(f"LEAD: {text}")
        st["transcript"] = st["transcript"][-self.cfg.get("transcript_size", 20):]
        if st["human_handoff"] or ev.get("human_handoff") in (True, "true", "yes"):        # 2. human has the conversation
            st["human_handoff"] = True; self.store[cid] = st; return  # never send; clear only via admin reset
        out = []
        trig = next((t for t in self.t.get("triggers", []) if t["id"] == ev.get("trigger") or
                     (t["type"] == "dm_keyword" and text.lower() == t["keyword"].lower())), None)
        if trig:                                                                            # 3. triggers restart the tree
            if trig.get("reset_variables", True): st["vars"] = {}
            self.advance(st, trig["start"], out)
        elif (g := self.match_global(st, text)):                                            # 4. global intents
            self.advance(st, g["goto"], out)
        elif st["node"] and self.nodes[st["node"]]["type"] in WAITING:                     # 5. answer to current node
            self.advance(st, self.resolve_input(st, self.nodes[st["node"]], text, out), out)
        elif st["node"] is None:
            self.advance(st, self.t["start"], out)
        self.flush(st, out); self.store[cid] = st

    def match_global(self, st, text):
        low = text.lower()
        node = self.nodes.get(st["node"] or "", {})
        if any(o["caption"].lower() == low for o in node.get("options", [])): return None  # node captions win
        for g in self.t.get("global_intents", []):
            if g.get("when") and not eval_expr(g["when"], self.scope(st)): continue
            for k in g.get("keywords", []):
                if (low == k.lower()) if g.get("match") == "exact" else re.search(rf"\b{re.escape(k.lower())}\b", low):
                    return g

    def resolve_input(self, st, node, text, out):
        """Returns the next node id, or None to stay on the current node (after queueing a retry message)."""
        sc = self.scope(st)
        if node["type"] == "choice":
            opts = [o for o in node["options"] if not o.get("when") or eval_expr(o["when"], sc)]
            hit = next((o for o in opts if text.lower() in [o["caption"].lower()] + [s.lower() for s in o.get("synonyms", [])]), None)
            if not hit and node.get("ai_match"):
                r = self.ai("classify", node, text, sc, [o["id"] for o in opts])  # -> {"status": "ok"|"none"|"intent", ...}
                if r.get("status") == "intent": return self.goto_intent(r["intent"])
                hit = next((o for o in opts if o["id"] == r.get("value")), None)
            if hit:
                if node.get("var"): self.set_var(st, node["var"], hit["id"])
                return hit["next"]
            nm = node.get("no_match", {}); st["tries"] += 1
            if st["tries"] >= nm.get("max_tries", self.cfg.get("default_max_tries", 2)): return nm.get("on_fail", st["node"])
            out += [render(m if isinstance(m, str) else m.get("text", ""), sc) for m in nm.get("say", node["say"])]
            return None
        r = self.ai("extract", node, text, sc, None)  # -> {"status":"ok","value":..} | {"status":"retry","followup":..} | intent
        if r.get("status") == "intent": return self.goto_intent(r["intent"])
        o = node["extract"]["output"]; v = r.get("value")
        if r.get("status") == "ok" and o["type"] in ("number", "integer"):
            if not isinstance(v, (int, float)) or v < o.get("min", float("-inf")) or v > o.get("max", float("inf")): r = {"status": "retry"}
        if r.get("status") == "ok":
            for f, var in node.get("save", {}).items(): self.set_var(st, var, (v or {}).get(f))
            if "var" in node: self.set_var(st, node["var"], v)
            return node["next"]
        st["tries"] += 1
        if st["tries"] >= node.get("max_tries", self.cfg.get("default_max_tries", 2)): return node["on_fail"]
        retry = node.get("retry", {})
        follow = r.get("followup") if retry.get("mode", "ai_followup") == "ai_followup" else None
        out += [follow] if follow else [render(m if isinstance(m, str) else m["text"], sc) for m in retry.get("say", node["say"])]
        return None

    def goto_intent(self, iid): return next(g["goto"] for g in self.t["global_intents"] if g["id"] == iid)

    def advance(self, st, nid, out):
        """Auto-advance loop: run non-waiting nodes until a waiting node (prompt sent) or a terminal node."""
        if nid is None: return                              # stay on current node; retry text already queued
        for _ in range(100):                                # guard against cycles of non-waiting nodes
            nid = self.t.get("tree", {}).get("redirects", {}).get(nid, nid)
            node, sc = self.nodes[nid], self.scope(st)
            st["node"], st["tries"] = nid, 0
            say = lambda: out.extend(self.render_say(m, sc) for m in node.get("say", []))
            k = node["type"]
            if k == "message": say(); nid = node["next"]
            elif k == "set":
                for var, ex in node["assign"].items(): self.set_var(st, var, eval_expr(ex, self.scope(st)))
                nid = node["next"]
            elif k == "condition":
                nid = next((b["next"] for b in node["branches"] if eval_expr(b["when"], sc)), node["else"])
            elif k == "action":
                self.flush(st, out)                          # keep ordering: messages queued so far go out first
                for a in node["actions"]:
                    if a["type"] == "notify_slack": self.notify_slack(st, node, a)
                    else: self.mc(a["type"], {"subscriber_id": st["contact_id"], **a})
                nid = node["next"]
            elif k in WAITING: say(); return
            elif k == "end":
                say()
                for tg in node.get("tags", []): self.mc("add_tag", {"subscriber_id": st["contact_id"], "tag": tg})
                self.mc("remove_tag", {"subscriber_id": st["contact_id"], "tag": "profit_active"})
                return
            elif k == "handoff":
                say(); self.flush(st, out)                   # holding message goes out before the bot goes silent
                for tg in node.get("tags", []): self.mc("add_tag", {"subscriber_id": st["contact_id"], "tag": tg})
                self.mc("remove_tag", {"subscriber_id": st["contact_id"], "tag": "profit_active"})
                self.mc("setCustomFieldByName", {"subscriber_id": st["contact_id"], "field_name": "human_handoff", "field_value": True})
                st["human_handoff"] = True                   # all further bot sends blocked until admin reset
                for ntf in node.get("notify", []):
                    if ntf.get("type") == "notify_slack": self.notify_slack(st, node, ntf)
                return
        raise RuntimeError("auto-advance limit reached (cycle?)")

    def quick_replies(self, st):
        node = self.nodes.get(st["node"] or "", {}); sc = self.scope(st)
        items = [{"caption": o["caption"]} for o in node.get("options", []) if o.get("show", True) and (not o.get("when") or eval_expr(o["when"], sc))]
        items += [q for q in node.get("quick_replies", []) if not q.get("when") or eval_expr(q["when"], sc)]
        if node.get("type") in WAITING and not node.get("hide_persistent"): items += self.t.get("persistent_quick_replies", [])
        url = self.cfg.get("inbound_url")
        return [{"type": "dynamic_block_callback", "caption": q["caption"], "url": url, "method": "post",
                 "payload": {"contact_id": st["contact_id"], "text": q["caption"]}} for q in items][:13]

    def notify_slack(self, st, node, ntf):
        """Compose a handoff alert and POST it to a Slack incoming webhook (via the injected ManyChat-or-HTTP callable)."""
        sc = self.scope(st)
        mention = render(ntf.get("mention_user_id") or "", sc).strip("<>@")
        head = render(ntf.get("text") or "PROFIT lead needs a human. Please reply swiftly.", sc)
        lines = []
        if mention: lines.append(f"<@{mention}>")
        lines.append(head)
        lines.append("Please reply swiftly — the lead is waiting.")
        name = st.get("name") or "(unknown)"
        handle = st.get("ig_handle")
        lines.append(f"*Lead:* {name}" + (f" (IG @{handle})" if handle else ""))
        lines.append(f"*Reason:* {node.get('reason') or '(none given)'}")
        captured = []
        for v in ntf.get("include_vars") or []:
            val = st["vars"].get(v)
            captured.append(f"• {v}: {val if val is not None else '—'}")
        if captured:
            lines.append("*Captured:*"); lines += captured
        nmsg = ntf.get("last_messages", 6)
        recent = (st.get("transcript") or [])[-nmsg:]
        if recent:
            lines.append("*Recent messages:*")
            lines += [f"• {m}" for m in recent]
        tmpl = self.cfg.get("livechat_url_template") or self.t.get("constants", {}).get("LIVECHAT_URL_TEMPLATE")
        if tmpl:
            lines.append(f"*Conversation:* {render(tmpl, sc)}")
        else:
            lines.append("No Live Chat link configured. You can reply directly in the Instagram app (no 24h limit for native app replies).")
        text = chr(10).join(lines)
        self.mc("notify_slack", {"url": render(ntf["webhook_url"], sc), "text": text, "body": {"text": text}})

    def render_say(self, m, sc):
        """Normalize a say item to a dict, rendering templates and keeping any delay_ms override."""
        if isinstance(m, str):
            return {"text": render(m, sc)}
        item = {}
        for k, v in m.items():
            item[k] = render(v, sc) if isinstance(v, str) else v
        return item

    def pace_ms(self, previous_text, override=None, first=False):
        p = self.cfg.get("pacing") or {}
        if override is not None:
            return int(override)
        if first:
            return int(p.get("thinking_ms", 1500))
        raw = int(p.get("base_ms", 800)) + int(p.get("per_char_ms", 40)) * len(previous_text or "")
        return max(int(p.get("min_ms", 1200)), min(int(p.get("max_ms", 4000)), raw))

    def flush(self, st, out, gen=None):
        """Send each queued message as its own sendContent, with human-paced delays. Quick replies on the last only."""
        if not out: return
        if gen is None: gen = st.get("send_gen")
        cap = self.cfg.get("max_messages_per_send", 10)
        items = []
        for m in out[:cap]:
            if isinstance(m, str):
                items.append({"type": "text", "text": m})
            elif "image_url" in m:
                items.append({"type": "image", "url": m["image_url"], "delay_ms": m.get("delay_ms")})
            else:
                items.append({"type": "text", "text": m.get("text", ""), "delay_ms": m.get("delay_ms")})
        out.clear()
        prev = ""
        for i, msg in enumerate(items):
            if gen is not None and st.get("send_gen") != gen:
                return                                       # lead wrote again: drop the rest of this sequence
            if st.get("human_handoff"):
                return
            if time.time() - st.get("last_inbound_at", 0) > self.cfg.get("window_hours", 24) * 3600:
                return
            wait = self.pace_ms(prev, override=msg.get("delay_ms"), first=(i == 0))
            reason = "thinking" if i == 0 else "reading time"
            self.mc("pace", {"delay_ms": wait, "reason": reason})
            # Typing indicator between messages — verify ManyChat/Instagram support before relying on it.
            self.mc("typing_on", {"subscriber_id": st["contact_id"], "verify": "instagram_typing"})
            self.sleep(wait)
            if gen is not None and st.get("send_gen") != gen:
                return
            if st.get("human_handoff"):
                return
            payload = {k: v for k, v in msg.items() if k != "delay_ms"}
            content = {"type": "instagram", "messages": [payload]}
            if i == len(items) - 1:
                qrs = self.quick_replies(st)
                if qrs: content["quick_replies"] = qrs
            self.mc("sendContent", {"subscriber_id": st["contact_id"], "data": {"version": "v2", "content": content}})
            if payload.get("text"):
                st.setdefault("transcript", []).append(f"BOT: {payload['text']}")
                st["transcript"] = st["transcript"][-self.cfg.get("transcript_size", 20):]
            prev = payload.get("text") or prev
