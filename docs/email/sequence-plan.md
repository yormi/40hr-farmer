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

Not yet locked. Working on this next.

## Goal cascade

Each step only happens if the previous one did:

1. Trust + understand what this is.
2. Engage with the Playbook / virtual consultant. **Primary state-change for this email window.**
3. Send feedback (because they're now using it).
4. Book a call when stuck or ready for hands-on help.
5. Convert to paid when access tightens.

**Primary state-change for the sequence:** "I signed up, what now?" → "I'm using the virtual consultant, I see the Playbook taking shape, I trust where this is going."

**Secondary goal mappings:**

| Goal | Where it rides |
|---|---|
| Prioritize the program (engage with it) | Primary CTA in Email 1. Reinforced where the story lends itself. |
| Set expectations (new, evolving, free now, may change later) | Subtle threads across all sends. Strongest on a dedicated honest-framing send and on the invitation send. |
| Book a call (free up time on the farm) | Conviction beat on the invitation send. Soft CTA, not the headline. |
| Use virtual consultant + send feedback | Use is the Email 1 CTA. Feedback ask lands once they've used it, late in the sequence. |

**Terminology:** "the course" = "the program." Same thing in our copy.

## Protagonist and voice

Not yet locked.

## Skeleton

Not yet locked. Length is flexible (5+ emails); we'll size to the work.

## Per-email plan

Not yet locked.
