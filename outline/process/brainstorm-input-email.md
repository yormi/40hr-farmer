# Brainstorm input email (template)

Stage 1 outreach to Andrew and Antoine. Sent via Postmark, From + Reply-To
`guillaume@orisha.io`, one shared email to both. Fill the `{{...}}` slots.

- `{{MONTH}}` — release month (e.g. July)
- `{{GOAL}}` — the month goal, from `01-brainstorm.md`
- `{{BRAINSTORM_DOC_LINK}}` — link to the `{{MONTH}}-<Topic> — Brainstorm` Doc
- `{{DEADLINE}}` — 3 business days from actual send, named (e.g. Tuesday, June 9)

---

**To:** andrew@growingformarket.com, info@jardinsdinverness.com
**Subject:** Next outline brainstorm - by {{DEADLINE_SHORT}}

Hi both,

What do you think would be relevant to add to the {{MONTH}} outline brainstorm ?

**{{MONTH}} Goal:** {{GOAL}}

**What I'm after:**
- Actionable tips to tackle the goal
- Related stories that show the stakes and gotchas
- Visual or b-roll ideas

Write inline in the doc, in a different colour: {{BRAINSTORM_DOC_LINK}}

If you can both get to it by end of day **{{DEADLINE}}**, that keeps us on schedule.

Thanks guys,

Guillaume


**Next Steps**
1. I build video outline skeletons
2. You comment/help me fill the gap of the skeletons
3. I send you the final outline

---

## Rendering (HTML email)

The body goes out as HTML. One style choice, reused every send:

* **Next Steps block = secondary.** Render it lighter and smaller so the
  ask and the Doc link stay primary. Wrap the heading + list in:
  `style="color:#9aa0a6;font-size:13px;margin-top:24px;"` (repeat
  `color:#9aa0a6` on the inner `<p>` and `<ol>` so clients honour it).
* Everything above Next Steps renders at normal weight/size.
