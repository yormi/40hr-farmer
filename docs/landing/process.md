# Landing page iteration process

How we rework sections of the landing page. Stepwise. Each step can send us back to the previous one if going back would make the current step materially better. **Intent leads everything.**

## The steps

1. **Page intent.** The one job the whole page has to do. Who it's aimed at, what they should understand or decide by the end, and what "converted" means for this page. Short. Every later step gets measured against this.
2. **Section intentions.** What each section must accomplish so the page intent lands. One line per section. No copy yet.
3. **Succinct draft.** Shortest honest way to communicate each intent. Plain sentences. Still no visual structure.
4. **Scannable structure + progressive disclosure.** Break the draft into a layered shape the eye can walk: headline → one-line hook → optional detail. No text-walls. Nothing load-bearing buried below the fold of the section.
   - 4.1 **Refine the draft** inside the new shape. Words often shrink once structure is clear.
5. **Render HTML.** Build it in `index.html`. Style-check against `brand/docs/brand/visual-design.md`.

Between steps: if the next step exposes a weakness in the previous one, go back and fix it before moving forward. It's cheaper than fixing it after render.

## Working state

Tracked below. Each step has its own section. We overwrite as we iterate.

---

## Step 1 — Page intent

*Locked 2026-04-20.*

**Who it's for (single persona):**
Current greenhouse-tomato grower, small-scale market gardener, a few years in, already growing greenhouse indeterminate tomatoes, feeling the weight of the work against the life they want with the people around them. Growing for Market reader. Allergic to hype. The program is built for this reader; the page is written to this reader.

**What the reader should decide — by the end or at any fit-decision beat before it:**
Whether the 40hr Farmer program is for them. A clean yes puts them on the waiting list; a clean no sends them away without wasting their season. Both outcomes are success for a fit-leaning page.

**What "converted" means:**
Waitlist form submit. No Orisha product surface on the page; the 5-email sequence introduces Helper / Chief Grower later, after trust is built.

**Success metric:**
Fit-leaning. 50 right-fit farmers beats 200 mixed. The "Who this is for" gate is firm and earns a higher-up position in the page than the current outline gives it.

**Voice:**
Aspiration-first hero ("Farming is beautiful…"). Mefferd quiet-journal voice throughout. Brunson conversion logic reframed to fit-determination: quiet inline signposts at each fit-decision beat, two actual CTA bands (mid-page + final form), no hype patterns (no arrows, no stacking bold, no "but wait," no urgency hacks). A clean no is a right outcome of this page.

**Implication for the 5-email sequence:**
The page now carries more of the conviction work. Emails shift from *keep warm until May* toward *deepen the relationship and pull toward the Helper / Chief Grower sales call.*

---

## Step 2 — Section intentions (by reader-type)

*Locked 2026-04-20. Method: reader-type-first section design (see `feedback_reader_type_first_sections.md`). Instead of ordering by topic, main sections serve specific sub-personas within the primary persona, ordered easiest → most demanding so content accumulates.*

### 2.0 — The five sub-personas, in order

Within the primary persona (current greenhouse-tomato grower, feeling the pressure), five reader-types need to convert. Each later one needs everything the earlier ones got, plus their own specific thing.

1. **Gut reader.** Resonates with the hero + tone, doesn't need more. Needs: *permission*.
2. **Peer reader.** Wants to see someone like them who lived it. Needs: *proof in a single farmer*.
3. **Analytical reader.** Wants the mechanism to check out and the source to be credible. Needs: *the numbers and the provenance*.
4. **Practical reader.** Wants to know how the program fits into their week, and what the other side looks like. Needs: *method and imagined future*.
5. **Committer.** Past the argument; hesitates on fit, logistics, and timing. Needs: *explicit invitation, mechanical next step, reason to act today*.

### 2.1 — Mapping from the current outline

Nothing from the existing outline is lost, it's just relabeled by who each section serves.

- **Gut reader section** ← Hero.
- **Peer reader section** ← Drew arc + "What a bed can buy back" (the projection from Drew's outcome onto the reader's life).
- **Analytical reader section** ← Tomato lever + Techniques/translation.
- **Practical reader section** ← The Program + What it starts to feel like.
- **Committer section** ← Who-this-is-for (fit gate) + How to join + FAQ + Team + Why add your name now + Final CTA. The mid-page CTA band is absorbed — each sub-persona section has its own CTA, so a generic rest stop is redundant.

### 2.2 — What each sub-persona needs

For each, lead with a one-sentence fit-decision intent ("Let the reader decide if…"), then the gap, register notes, shape, fit-decision beat, CTA, and what does not belong.

*Shape here is narrow on purpose:* just enough sequence to locate the fit-decision beat relative to the other pieces. Lead placement, block-level scannability, pull-quotes, `<details>` mechanics belong to step 4.

**1. Gut reader** *(first section, no earlier sections to lean on)*

*One-sentence intent:* Let the reader decide if this page's worldview fits what they want from farming life.

*Needs:*
- Emotional mirror. Feel seen immediately.
- A name for the offer. A container to commit to.
- One-line shape of what it does. No proof, no claim.
- A quiet open door.
- Permission to stop reading if already sold.

*Register:* Aspiration-first, *resolute*. Not wistful (reads self-pitying), not warm (reads greeting-card). Quiet determination.

*Shape:* mirror → named-container paragraph (beat lands in its closing line) → CTA.

*Fit-decision beat:* closing line of the descriptive paragraph, where the emotional recognition and the named container come together.

*CTA:* `Join the waiting list →`. Whisper register, not a clear door. Truly gut-sold readers find it; uncertain readers scroll past into the Peer section without being yanked out of the flow.

*What does not belong:* peer proof, numbers, credibility, program mechanics, outcome projection, fit gate, pricing, logistics, timing. All reserved for later sub-personas.

**2. Peer reader**

*One-sentence intent:* Let the reader decide if a farmer in a situation like theirs has actually lived this path.

*Needs (given Gut delivered emotional mirror, offer name and shape, one quiet CTA):*
- A single named farmer, not a composite. Real, recognizable, picturable.
- A before-state the reader recognizes. The same kind of pressure the primary persona carries now, shown honestly.
- A concrete, earned climb told through *lifestyle markers, not yield metrics.* Lived progression (decisions, shifts, things the farmer can now do that they couldn't before) so the outcome reads as earned, not lucky. Production numbers are reserved for the Analytical section; Peer stays lived.
- A life-flip moment. The emotional climax where the farmer's relief translates into a specific, nameable life change bigger than any metric.
- A bridge from that farmer to the reader's own farm. A thesis-level line that lets the reader project the flip without it reading as a promise.
- A CTA that acknowledges the conviction this reader just gained, plus a secondary depth-ramp link for readers who want to stay longer in the farmer's story before deciding.

*Register:* Quiet, observational, field-note. One raw unvarnished sentence in the farmer's own voice; no stacking of raw quotes. Sequential narrative (before → climb → flip), not flip-first testimonial hook.

*Shape:* one named farmer → before-state → climb in lifestyle markers → life-flip (beat) → thesis bridge → CTA.

*Fit-decision beat:* the life-flip moment, where yield-turning-into-life stops being abstract.

*CTA:* peer-aware primary signpost (wording that recognizes the reader just saw proof, not generic "join") + secondary depth-ramp link for readers who want to live longer in the farmer's story before committing. Exact wording in step 3.

*What does not belong:* leverage math, institutional credibility, program mechanics, in-the-greenhouse outcome projection, fit gate, pricing, logistics, timing.

**3. Analytical reader**

*One-sentence intent:* Let the reader decide if the strategic thesis applies to the farm they run.

*Needs (given Gut delivered emotional mirror + offer shape, and Peer delivered one farmer's lived arc in lifestyle terms):*
- The leverage mechanism named concretely. Which structural lever produces disproportionate returns, and why this one.
- **The generalized number, arriving already translated into felt significance.** Not a raw ratio. A number paired with scale the reader can picture (bed-to-bed comparison, revenue share, what it replaces in the farm's shape). The audience is feeling-driven and doesn't have yield references; a standalone number closes conviction instead of opening it. See `feedback_numbers_felt_translation.md`.
- External credibility lineage. Established practitioners, institutional backers, prior publications. Pure external authority for this section; team credibility belongs to the Committer section later.
- One honest line acknowledging what the established sources *don't* solve. This line opens into why the program exists.
- A thesis-aware CTA that names the lever the reader just verified.

*Register:* Sober and grounded, not cold. Numbers only when paired with translated significance, no raw numbers left hanging. Credibility pieces factual but unflashy. Mechanism first, credibility second.

*Shape:* leverage claim → translated number → external credibility → open-problem line (beat) → CTA.

*Fit-decision beat:* the honest-limit line that names what published sources don't solve. The Analytical reader's final check — the moment they see the program isn't repackaged content but is aimed at the actual open problem.

*CTA:* thesis-aware primary signpost that names the lever the reader just verified. Wording recognizes the conviction mode they used (mechanism + credibility verified). Exact wording in step 3.

*What does not belong:* program mechanics (Practical), in-greenhouse outcome projection (Practical), fit gate (Committer), pricing / logistics / timing (Committer), another farmer's full arc (Peer already did that job), emotional register shift back to hero tone (Gut).

**4. Practical reader**

*One-sentence intent:* Let the reader decide if this program fits the life they already have.

*Needs (given Gut delivered worldview mirror, Peer delivered one lived arc, Analytical delivered thesis-applies-to-my-farm):*
- An honest production fit gate first. Who this is for, who this isn't, binary enough that a wrong-production reader (no greenhouse tomatoes yet, industrial-scale, theory-only) disqualifies fast and doesn't invest in reading the rest. This is the hard gate hoisted from the bottom of the old outline — it lives here because production-fit is part of whether the program fits the farmer's life.
- The smallest-number answer next: time per week. The single dimension that most often disqualifies or confirms fit for a working farmer who cleared the gate.
- Cost in plain terms, with the GFM path named first since that's how most farmers join.
- A rhythm that reads as additive, not imposing: monthly cycle, rolling admission, leave anytime. A farmer carrying a full season needs to know this won't trap them.
- A pictureable month: what lands in their inbox on the 1st, what the live call is, what happens on their actual plants. Picturable beats comprehensive.
- Remaining dimensions (language, what comes next after tomatoes, full month-by-month) reachable in one click or in the first waitlist email. They matter for fit, but leading with them buries the "this fits your week" message.
- A quiet out for readers who discover the fit isn't right. Progressive disclosure doesn't just hide detail, it lets the unfit reader find their disqualifier and move on without a fight.

*Register:* Grounded, logistical, uncolored. The "math checks out" register. No more climbing. Numbers about the week in small units the reader can test against their own schedule (`2 to 3 hours a week`, not `10 hours a month`). Felt-translation still applies (time → "phone-watchable between rows," cost → "the magazine you're already reading"), but the prose itself is quieter than earlier sections — field-note about program mechanics, not another climb.

*Shape:* production fit gate (who / who not) → filtering numbers (time, cost, rhythm) → pictureable month (beat) → depth offloaded → CTA.

*Fit-decision beat:* the pictureable-month line. The moment the reader imagines the actual month and it either slots into their week or doesn't. Not the time number, not the cost — the picture.

*CTA:* practical-aware primary signpost acknowledging the reader just checked week-fit. Secondary depth-ramp: either "See the full rhythm" (opens `<details>`) or "We'll send the full rhythm in the first email" (folds the depth into the waitlist itself — converts the uncertain-but-curious reader by moving detail past the form instead of before it). Exact choice in step 3.

*What does not belong:* first-in-line urgency (Committer), team credibility (Committer — trust-before-the-form is Committer's job, not Practical's), a curriculum roadmap (program is a living Playbook; a detailed map reads as overcommitted and drifts from brand voice), price comparison to other programs, another round of thesis (Analytical), outcome imagery ("what the greenhouse becomes" is a separate beat — anchoring it here vs. to Committer is a step-4 decision).

**5. Committer**

*One-sentence intent:* Let the reader decide if today is the day to add their name.

*Needs (given Gut, Peer, Analytical, and Practical have delivered worldview + lived arc + thesis-applies + week-fit-and-production-fit — the reader is ready, only timing is left):*
- An honest reason today beats later. Rolling admission + real live-call capacity → a genuine priority-queue dynamic. Framed as "your place in line costs nothing today," not "act now or lose out." Any urgency beyond the honest math breaks the brand.
- A frictionless mechanical step. What "joining today" means (waitlist), what arrives after the click, when the program opens. Reassurance that acting today is small and reversible.
- Compact team naming. Trust still has to clear right before the form even for a ready reader — the named humans who'll actually show up on the live calls (Guillaume, Antoine, Andrew, LB), plus Orisha as backer. Not badge-stacking, just: here are the people you'd be working with.
- The form itself. Minimal fields, the page's accumulated weight carried by the submit button.
- A short disclosure block next to the form for residual logistics nits (mid-program join, leave anytime, language, what arrives after signup). Answers objections without re-arguing earlier sections.

*Register:* Direct and warm. Past persuasion. The "come join us" register, said quietly. Named humans. Plain operational language around joining. Confident opening of the door, not a hard close — the reader is ready; you're standing aside.

*Shape:* priority-queue honesty (beat) → mechanical next step → team → form → disclosure block.

*Fit-decision beat:* the priority-queue honesty line. Where the reader sees that today-vs-later actually matters in a non-manipulative way and tips from "I'll come back" to "I'll do it now." The form records the decision; this line is where it's made.

*CTA:* the final form. No secondary link — terminal section. Submit-button signpost carries the page's accumulated weight (exact wording in step 3). All earlier CTAs pointed here.

*What does not belong:* the fit gate (now in Practical), new program mechanics (Practical), thesis or peer proof (Analytical, Peer), aspiration re-heated at length (Gut), a founder-origin story (team credibility here is about who'll show up on the calls, not where the company started), urgency patterns beyond honest priority-queue math, "limited seats forever" or "one-time offer" framing (contradicts rolling admission).

## Step 3 — Succinct draft

*Not started.*

## Step 4 — Scannable structure + progressive disclosure

*Not started.*

## Step 5 — Render HTML

*Not started.*

---

## Step 3 — Succinct draft

*Not started.*

## Step 4 — Scannable structure + progressive disclosure

*Not started.*

## Step 5 — Render HTML

*Not started.*
