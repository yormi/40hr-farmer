# Email sequence plan

How we plan multi-email sequences for the 40hr Farmer funnel, plus the locked working state for the active welcome sequence.

The voice and conversion logic for these sequences live in [`brand/docs/brand/email-sequences.md`](../../brand/docs/brand/email-sequences.md). That file is "how we write." This file is the project-side companion: process + working state for the sequence currently being built.

**Intent leads everything.**

## The steps

1. **Sequence intent.** The state-change in the reader from Email 1 to Email N. Where this sequence sits in the funnel ladder. What "converted" means for this sequence specifically. Short. Every later step gets measured against it.
2. **Goal cascade.** List every goal you want this sequence to do. Order them as a cascade (each only fires if the previous did). Pick the primary state-change for the email window. Map each secondary goal to where it rides along (which email, P.S., subject line). One ask per email at most; the rest are touches.
3. **Protagonist and voice.** Who carries the arc. The 5-email arc works on a single protagonist per sequence. Pick who; secondary voices (other farmers, Guillaume) only ride along when they don't dilute the line.
4. **Skeleton.** Email count, the one-line job each email does, cadence (days between sends). Map each email to a Brunson beat (stage, wall, epiphany, hidden benefits, invitation). Identify the open loop between consecutive emails.
5. **Per-email plan.** For each email: protagonist, scene, story arc, takeaway, CTA, open loop into the next, P.S. Outline only, no prose.
6. **Subject lines.** Lowercase, conversational, like a text from a friend. Each one promises something the email pays off.
7. **Draft.** Prose that delivers each email's plan. Read aloud. Cut anything that sounds like marketing.
8. **Render HTML.** In `email/NN-name.html`. Style against `brand/docs/brand/visual-design.md`. Verify the no-dashes rule. Verify links and merge tags (`{{contact.firstname}}`, `{{unsubscribe_link}}`).
9. **Approval and ship.** Surface to Guillaume. On approval, install via [`email/HUBSPOT-PROCEDURE.md`](../../email/HUBSPOT-PROCEDURE.md).

Between steps: if a later step exposes a weakness in an earlier one, go back and fix it before moving on. Cheaper than fixing it after render.

## Save-on-lock discipline

Universal rule. The moment anything locks (sequence intent, cascade, protagonist, skeleton, per-email plan, draft prose), write it to the locked-content section of this file before moving on. Never let locked work live only in conversation. Compaction loses it; re-derivation wastes time and invites drift.

| Step | What locks | Where it goes |
|---|---|---|
| 1 | Sequence intent | Locked content: "Sequence intent" |
| 2 | Goal cascade + primary state-change + secondary mappings | Locked content: "Goal cascade" |
| 3 | Protagonist | Locked content: "Protagonist and voice" |
| 4 | Skeleton (count, jobs, cadence, beats, open loops) | Locked content: "Skeleton" |
| 5 | Per-email plan blocks | Locked content: per-email subsection |
| 6 | Subject lines | Locked content: per-email subsection |
| 7 | Locked prose | Locked content: per-email subsection, as **Locked copy** |
| 8 | Rendered HTML | `email/NN-name.html` |

If it's not written down, it's not locked.

---

# Locked content: 40hr Farmer welcome sequence

Working state for the welcome funnel triggered on landing-page form submit. Sequence-wide context: signup → opens → book a call (per `CLAUDE.md` funnel conversions).

## Sequence intent

Turn a fresh 40hr Farmer signup into a believer who's ready and eager for the program to open. **Working target: June 2026; exact date confirmed when known.**

## Goal cascade

Each step only happens if the previous one did:

1. Trust + understand what this is.
2. Believe the greenhouse-yield transformation is real (Drew's story does the heavy lifting).
3. Want it for their own farm.
4. **Excited and waiting eagerly for the program open (target: June 2026).** Primary state-change.
5. *(Optional)* Engage in the meantime: use the virtual consultant, send feedback, book a call.
6. Convert when the program opens.

**Primary state-change for the sequence:** "I signed up, what now?" → "I trust this, I see the transformation is real, I want it for my farm, I'm eager for the open."

**Goal mappings:**

| Goal | Where it rides |
|---|---|
| Trust + understand what this is | Email 1 stages the relationship; Email 2 carries the origin story. Drew's farm appears as the spark that became the Playbook. Reinforced by honest tone across the sequence. |
| Believe the transformation is real | Email 2 (Drew's story, told briefly as origin). Re-anchored in Email 4 when the "what about market?" objection lands. |
| Want it for their own farm | Sub-text of Emails 2–5, made explicit in Emails 6–7. |
| Excited for the program open (target: June 2026) | Email 2 frames the target. Email 6 holds the honest "we'll confirm when we know." Email 7 closes with the same. |
| Set expectations (working target June, still being built, free now / may change) | Load-bearing. Email 1 previews it; Email 2 frames it lightly; Email 6 goes deep (Gordon failure, building as we go, pricing TBD). |
| Use the virtual consultant in the meantime | Email 5 introduces it with access. Soft mention earlier and later. Never the sequence headline. |
| Book a call (free up time) | Email 7, paired with Dan's automation story. |
| Send feedback | Email 6, after engagement. Address: `feedback@orisha.io`. |

**Terminology:** "the course" = "the program." Same thing in our copy.

## Requirements

Each requirement is a yes/no question we can apply to a draft. "No" or "unclear" means the draft fails and gets revised. Tests apply two ways: per-email (does this email satisfy the requirements it's responsible for?) and sequence-wide (is every requirement satisfied somewhere across the full sequence?).

### Primary (must all pass)

- **REQ-P1.** By the final email, does the reader feel eager about the program open (target: June 2026)?
- **REQ-P2.** By the final email, does the reader trust where Orisha and the 40hr Farmer Playbook are going?
- **REQ-P3.** Has the reader encountered at least one concrete farmer story (real name, real scenes) they could recall?
- **REQ-P4.** By the final email, could the reader articulate "this is for my farm"?

### Secondary (coverage, must appear somewhere)

- **REQ-S1.** Does the sequence frame June 2026 as the working target, with the honest note that the exact date will be confirmed when known?
- **REQ-S2.** Does the sequence frame the program as still being built (early-stage)?
- **REQ-S3.** Does the sequence set expectations around free-for-now and access may change later?
- **REQ-S4.** Does the sequence offer the virtual consultant as a meantime option, without making it the headline?
- **REQ-S5.** Does the sequence offer a soft book-a-call option?
- **REQ-S6.** Does the sequence invite feedback, only after engagement?

### Anti-requirements (must NOT happen)

- **ANTI-1.** No fake urgency, scarcity, or "act now" framing.
- **ANTI-2.** No overclaim or hype on results.
- **ANTI-3.** The evolving / early-stage nature must never read as a downside.
- **ANTI-4.** Nothing that could ship from a generic SaaS or lifestyle newsletter.
- **ANTI-5.** Zero stylistic dashes (em-dash, hyphen-dash as punctuation).

## Protagonist and voice

**Protagonist:** Guillaume. Builder, observer.

**Arc shape (observer-builder):** Guillaume saw a pattern across farmers: beautiful work eating their lives. He wasn't farming himself yet; he built Orisha because farmers needed it. Drew's farm in 2024 was the first real proof. Now he's building the Playbook so any market gardener can take the same path. Ferme Décembre (2026) is recent and stays peripheral; the wall belongs to farmers Guillaume worked with, not to his own farm pain.

**Voice:** First-person Guillaume. Quiet, observational, honest, warm. Farmer-adjacent in tone, but the credibility comes from how carefully he tells what he saw, not from his own farm scars.

**Brunson beats mapped to Guillaume's arc (this sequence distributes them across 7 emails; the SOS arc is a default, not a cage):**

| Beat | What it carries | Lands in |
|---|---|---|
| Stage | Welcome, signup confirmation, sequence preview, hook into the origin story. | Email 1 |
| Origin / first proof | Who Guillaume is. Why he started Orisha. Drew's farm in 2024 as the spark that became the Playbook. | Email 2 |
| Wall | The pattern of farmers stuck (beautiful work, no life left). Plus the analytical farmer's "what about market?" objection. | Emails 3, 4 |
| Epiphany | Yield as pressure relief, not volume. Greenhouse climate as the lever. | Email 4 |
| Hidden benefits | What the yield actually bought back: Drew's life, Allison rejoining the farm. Dan's automation story echoes the beat at the call CTA. | Emails 2, 7 |
| Invitation | Where the Playbook is heading. Working target: June. Early-stage frame. Soft consultant + book-a-call asks. | Emails 6, 7 |

**Supporting voices:** Gordon (Ten Mothers) may appear as a quoted aside if a beat needs a second proof point. Dan and Scott reserved for future sequences.

**Why not the reader-farmer as protagonist:** SOS needs a single character the reader maps onto. Making the reader the protagonist forces second-person prose that drifts into instruction-mode, breaking the empathy → trust → action arc. Guillaume's story gives them someone to follow.

## Skeleton

7 emails over 18 days. Cadence Day 0 / 1 / 4 / 7 / 10 / 14 / 18. Voice is first-person Guillaume throughout.

| # | Day | Beat | One-line job | Open loop into next |
|---|---|---|---|---|
| 1 | 0 | Stage | Confirm signup. Brief preview of what's coming over the next weeks. Why I'm sending these. Set up tomorrow's origin story. | "Tomorrow: why I'm building this. It starts with a farm I worked with in 2024." |
| 2 | 1 | Origin (first proof) | Who Guillaume is. Why he started Orisha. Drew's farm in 2024 and what happened (yield doubled, Allison back full-time). That moment became the seed of the 40hr Farmer Playbook. Working target to open: June 2026. | "Next: how the test of putting all this into practice on my own farm is going." |
| 3 | 4 | Vision (Ferme Décembre) | Building a 40hr farm at Ferme Décembre alongside the reader. What it means in practice. Where things stand right now. Adjacency, not spectacle. | "Next: why this matters even if you can't sell more tomatoes." |
| 4 | 7 | Reframe / objection | "What if the market won't take double the yield?" Yield as pressure relief, not volume. Re-anchor in Drew's chapter (the doubled yield bought back his life, not just income). | "Next: there's something we made that you can start using right now, even before launch." |
| 5 | 10 | How you can engage now | Origin of Orisha. The greenhouse-climate problem (rules of thumb existed, but how to apply them all at once?). Why we built the virtual consultant. It's free. Here's your access. | "Next: an honest look at where the program actually is and what that means for you." |
| 6 | 14 | Honest framing | We're building as we go: program content, format, consultant, pricing. Why we started consulting last year. Where we got it wrong with Gordon and what we learned. We progress with you. Send feedback to `feedback@orisha.io`. | "Next: if you'd rather get hands-on help today, not in June, there's a way." |
| 7 | 18 | Invitation | Dan's story (automation as pressure relief, focus protected so the work pays off). If you want help freeing up time on your farm now, book a call. We'll be in touch the moment we know the launch date. | (sequence ends) |

**Notes:**

- **Email 1 stays brief**: confirms the signup worked, previews what's coming, hooks into Email 2. No empty welcome (per [`brand/docs/brand/email-sequences.md`](../../brand/docs/brand/email-sequences.md)).
- **Drew lives in Email 2** as the spark of the Playbook's origin, not as a separate hero email. Email 4 references back to Drew's story when answering the "what about market?" objection.
- **Email 2 will be the densest** (origin + Drew + target). That's fine; the origin email earns the extra weight.
- **Cliffhangers above are sketches.** They'll be sharpened during the per-email plan + draft steps.
- **Pre-launch only.** Once the program opens, signups arrive into a different reality. Emails 6 and 7 will need a small pass at that point ("doors are open, here's how to step in").

## Per-email plan

Not yet locked.
