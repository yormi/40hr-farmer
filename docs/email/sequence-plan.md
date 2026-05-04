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

Turn a fresh 40hr Farmer signup into a believer who's ready and eager for the program's **June 2026 open**.

## Goal cascade

Each step only happens if the previous one did:

1. Trust + understand what this is.
2. Believe the greenhouse-yield transformation is real (Drew's story does the heavy lifting).
3. Want it for their own farm.
4. **Excited and waiting eagerly for the June 2026 program open.** Primary state-change.
5. *(Optional)* Engage in the meantime: use the virtual consultant, send feedback, book a call.
6. Convert when the program opens.

**Primary state-change for the sequence:** "I signed up, what now?" → "I trust this, I see the transformation is real, I want it for my farm, I'm eager for June."

**Goal mappings:**

| Goal | Where it rides |
|---|---|
| Trust + understand what this is | Email 1 frame; reinforced through honest tone across the sequence. |
| Believe the transformation is real | Story emails (wall, epiphany, hidden benefits). Drew's arc carries this. |
| Want it for their own farm | Sub-text of the story emails, made explicit late in the sequence. |
| Excited for the June 2026 program open | Stated explicitly in Email 1 (anchor) and the invitation send. |
| Set expectations (June launch, still being built, free now / may change) | Load-bearing. Email 1 frames it; a dedicated honest-framing send goes deep. |
| Use the virtual consultant in the meantime | Soft option in Email 1 P.S. and a later send. Never the headline. |
| Book a call (free up time) | Soft conviction beat on the invitation send. |
| Send feedback | Late-sequence ask after they've engaged. |

**Terminology:** "the course" = "the program." Same thing in our copy.

## Requirements

Each requirement is a yes/no question we can apply to a draft. "No" or "unclear" means the draft fails and gets revised. Tests apply two ways: per-email (does this email satisfy the requirements it's responsible for?) and sequence-wide (is every requirement satisfied somewhere across the full sequence?).

### Primary (must all pass)

- **REQ-P1.** By the final email, does the reader feel eager about the June 2026 program open?
- **REQ-P2.** By the final email, does the reader trust where Orisha and the 40hr Farmer Playbook are going?
- **REQ-P3.** Has the reader encountered at least one concrete farmer story (real name, real scenes) they could recall?
- **REQ-P4.** By the final email, could the reader articulate "this is for my farm"?

### Secondary (coverage, must appear somewhere)

- **REQ-S1.** Does the sequence state the program launches in June 2026?
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

**Brunson beats mapped to Guillaume's arc:**

| Beat | What it carries |
|---|---|
| Stage | Welcome. Who Guillaume is, where he's writing from, why he's building this. |
| Wall | The pattern Guillaume saw across farmers. Beautiful work eating people's lives. Empathy + mission. |
| Epiphany | The reframe: yield as pressure relief. The moment Guillaume realized greenhouse climate was the lever. |
| Hidden benefits | Drew's chapter. Ghost House 2024. Yield doubled. Allison joining full-time. What the yield actually bought back. |
| Invitation | Where Guillaume is taking it. The Playbook. June 2026 open. They're early, here's what that means. |

**Supporting voices:** Gordon (Ten Mothers) may appear as a quoted aside if a beat needs a second proof point. Dan and Scott reserved for future sequences.

**Why not the reader-farmer as protagonist:** SOS needs a single character the reader maps onto. Making the reader the protagonist forces second-person prose that drifts into instruction-mode, breaking the empathy → trust → action arc. Guillaume's story gives them someone to follow.

## Skeleton

Not yet locked. Length is flexible (5+ emails); we'll size to the work.

## Per-email plan

Not yet locked.
