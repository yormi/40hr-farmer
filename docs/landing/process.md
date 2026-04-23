# Landing page iteration process

How we rework sections of the landing page. Stepwise. Each step can send us back to the previous one if going back would make the current step materially better. **Intent leads everything.**

This doc is **method only** — reusable across any fit-determination asset (landing pages, sales pages, long-form emails). Page-specific working state lives in [`outline.md`](outline.md). Raw material used for drafting lives in [`sources/`](sources/). The [`README.md`](README.md) explains the three-concern split.

## The steps

1. **Page intent.** The one job the whole page has to do. Who it's aimed at, what they should understand or decide by the end, and what "converted" means for this page. Short. Every later step gets measured against this.
2. **Section intentions.** What each section must accomplish so the page intent lands. One line per section. No copy yet. Use the reader-type-first method: order sections by sub-persona, easiest to most demanding, so content accumulates and each later reader gets everything the earlier ones got plus their own specific thing.
3. **Subsections and their intents.** For each section, the subsection count and each subsection's one-line intent. Decides how the section's argumentative moves split before any drafting.
   - **Count.** Based on distinct argumentative moves the section makes to deliver its fit-decision beat. One clean move = one subsection.
   - **One-line intent per subsection.** What this subsection uniquely contributes to the section's fit-decision intent. If it can't be stated in one line, the decomposition isn't clean yet — split further or merge.
   - **Ownership of needs.** Walk each step-2 need against the subsections. Every need owned by exactly one subsection. Nothing orphaned, nothing re-litigated.
   - **Ordering.** Usually mirrors the section's step-2 Shape.
   - **Signpost placement.** The conversion CTA lands on the subsection that owns the fit-decision beat.
4. **Succinct draft.** Shortest honest way to communicate each intent. Plain sentences. No visual structure yet.

   **Iteration loop, every time content is proposed or revised:**
   1. Restate the section's fit-decision intent.
   2. Restate the subsection's intent.
   3. Restate the needs this subsection owns (from step 2 + step 3 ownership).
   4. Walk the proposed content against each need. Note what's covered, missing, redundant, or drifting into step-5 structure.
   5. Adjust. Repeat until every owned need is answered with the fewest honest words.

   Do this every iteration, not just the first. Don't rely on remembering — lay out intent + needs explicitly every time, then evaluate. Keeps drift out.
5. **Scannable structure + progressive disclosure.** Break each locked draft into a layered shape the eye can walk: headline → one-line hook → optional detail. No text-walls. Nothing load-bearing buried below the fold of the section.
   - 5.1 **Refine the draft** inside the new shape. Words often shrink once structure is clear.
6. **Render HTML.** Build it in `index.html`. Style-check against `brand/docs/brand/visual-design.md`.

Between steps: if the next step exposes a weakness in the previous one, go back and fix it before moving forward. It's cheaper than fixing it after render.

## Save-on-lock discipline

**Universal rule, applies to every step.** The moment anything locks — page intent, section intent, subsection intent, subsection copy, visual structure decision, shipped HTML — write it to its canonical home before moving on. Never let locked work live only in conversation memory; compaction loses it, and re-derivation wastes time and invites drift.

| Step | What locks | Where it goes |
|---|---|---|
| 1 | Page intent (persona, decision to reach, success metric, voice) | `outline.md`, top block |
| 2 | Section intentions by reader-type (sub-persona ladder, per-section needs + shape + fit-decision beat + CTA) | `outline.md`, under page intent |
| 3 | Subsection count + intents + ownership per section | `outline.md`, under the matching section |
| 4 | Succinct draft prose per subsection | `outline.md`, under the matching section, as **Locked copy** |
| 5 | Visual structure decisions per section | `outline.md`, under the matching section, as **Beats (visual layout)** |
| 6 | Rendered HTML | `index.html` |

Write the lock before proposing or drafting the next thing. If it's not written down, it's not locked.
