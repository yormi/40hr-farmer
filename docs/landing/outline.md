# 40hr Farmer landing page outline

Working outline **and** canonical home for locked copy. Each section describes what goes on the page in order. Under each section:

- **Reader-type** and **subsection intent** (internal, from the reader-type-first method, see [`process.md`](process.md)).
- **Beats** — compressed, pyramid-style description of what the section does on the page.
- **Status** — locked / draft / pending.
- **Locked copy** — verbatim prose (only when status is locked). This is what ships on the page.

CTAs everywhere read "Join the waiting list": the program is pre-launch and signups feed a waiting list until June 2026.

Whenever a subsection locks, the prose goes straight into this file. No separate copy deck.

---

## Page intent (step 1)

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

## Layout patterns (locked 2026-04-27)

Canonical class strings for this page. **Apply to every section.** Deviation requires explicit reasoning in the section's beats.

Drift in this page (multiple H2 scales, three different alignments) was caught and corrected on 2026-04-27. The lock below prevents recurrence.

### Section structure
- **Section outer:** `<section id="..." class="bg-white">` (or `bg-farm-bg`, alternating). Padding `py-16 md:py-24` (standard) or `py-20 md:py-28` (heavier sections like `#story`, `#who`, `#program`, `#how-to-join`).
- **Section container:** `<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">` then `<div class="fade-in">`.
- **H2 wrapper:** `<div class="max-w-3xl mx-auto">` — centered reading column inside the max-w-5xl section. Subtitle (when present) sits in the same wrapper.

### H2 (every section)
```
font-heading text-3xl sm:text-4xl md:text-5xl font-medium text-farm-dark leading-[1.1] tracking-tight text-balance
```
No terminal period. No exceptions on scale.

### Subtitle (italic muted intro line, optional)
```
font-body italic text-lg md:text-xl text-farm-muted leading-relaxed mt-6
```
Same wrapper as H2.

### Body prose
```
text-lg md:text-xl text-farm-text leading-relaxed
```
Inside `<div class="max-w-3xl mx-auto">` for prose-only sections.

### Centered anchor lines (post-grid takeaway)
```
fade-in font-heading text-2xl md:text-3xl text-farm-dark text-center mt-14 md:mt-20 max-w-3xl mx-auto leading-snug text-balance
```
Upright Fraunces (italic Fraunces hard to read at this scale, replaced 2026-04-27).

### Callout panels
- Small (admission/anchor): `bg-farm-bg rounded-card px-6 py-5 md:px-8 md:py-6 text-center`
- Large (first-goal): `bg-farm-bg rounded-card px-8 py-8 md:px-10 md:py-10 text-center`
- Bonus container: `mt-12 md:mt-16 bg-farm-bg p-8 md:p-10 rounded-lg`

### Card grid (2-up)
```
grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 mt-12 md:mt-16
```

### Card 3-up (bonus)
```
grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10 mt-6
```

### Card internals
- Sketch (top, optional): `w-32 h-32 md:w-36 md:h-36 object-contain mb-4`
- Title: `font-heading text-xl md:text-2xl font-semibold text-farm-dark leading-snug tracking-tight`
- Body: `text-base md:text-lg text-farm-text leading-relaxed mt-3`

### Pull-quote
```
pl-5 md:pl-6 border-l-2 border-farm-green/60 font-body italic text-xl md:text-2xl text-farm-dark leading-snug
```
With footer: `font-sans not-italic text-sm md:text-base text-farm-muted mt-3 tracking-wide`. Smaller variants drop one scale step (`text-base md:text-lg`, `pl-4`).

### Eyebrow (uppercase)
```
font-accent text-farm-mid font-semibold uppercase tracking-wider text-xs
```

### Italic display register
**Use Lato italic** (`font-body italic`), not Fraunces italic. Fraunces italic at display scale is mannered and hard to read; this was swept page-wide on 2026-04-27.

### Ground alternation
Alternate `bg-white` and `bg-farm-bg` to create visual rhythm. Avoid back-to-back same-ground unless the sections function as one unit (e.g., consecutive Practical subsections).

---

## Section intentions by reader-type (step 2)

*Locked 2026-04-20. Method: reader-type-first section design (see `feedback_reader_type_first_sections.md`). Instead of ordering by topic, main sections serve specific sub-personas within the primary persona, ordered easiest → most demanding so content accumulates.*

### The five sub-personas, in order

Within the primary persona (current greenhouse-tomato grower, feeling the pressure), five reader-types need to convert. Each later one needs everything the earlier ones got, plus their own specific thing.

1. **Gut reader.** Resonates with the hero + tone, doesn't need more. Needs: *permission*.
2. **Peer reader.** Wants to see someone like them who lived it. Needs: *proof in a single farmer*.
3. **Analytical reader.** Wants the mechanism to check out and the source to be credible. Needs: *the numbers and the provenance*.
4. **Practical reader.** Wants to know how the program fits into their week, and what the other side looks like. Needs: *method and imagined future*.
5. **Committer.** Past the argument; hesitates on fit, logistics, and timing. Needs: *explicit invitation, mechanical next step, reason to act today*.

### Mapping from the section blocks below

Nothing in the section-by-section blocks below is lost, it's just labeled by who each section serves.

- **Gut reader section** ← Hero.
- **Peer reader section** ← Drew arc + "What a bed can buy back" (projection from Drew's outcome onto the reader's life).
- **Analytical reader section** ← Tomato lever + Techniques/translation.
- **Practical reader section** ← Who this is for + How to join + The Program + What it starts to feel like.
- **Committer section** ← Team + Why add your name now + Final CTA. FAQ sits between Practical and Committer as residual objections. The mid-page CTA band is the thesis-aware CTA that closes Analytical.

### What each sub-persona needs

For each, lead with a one-sentence fit-decision intent ("Let the reader decide if…"), then the gap, register notes, shape, fit-decision beat, CTA, and what does not belong.

*Shape here is narrow on purpose:* just enough sequence to locate the fit-decision beat relative to the other pieces. Lead placement, block-level scannability, pull-quotes, `<details>` mechanics belong to step 5.

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

*CTA:* peer-aware primary signpost (wording that recognizes the reader just saw proof, not generic "join") + secondary depth-ramp link for readers who want to live longer in the farmer's story before committing. Exact wording in step 4.

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

*CTA:* thesis-aware primary signpost that names the lever the reader just verified. Wording recognizes the conviction mode they used (mechanism + credibility verified). Exact wording in step 4.

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

*CTA:* practical-aware primary signpost acknowledging the reader just checked week-fit. Secondary depth-ramp: either "See the full rhythm" (opens `<details>`) or "We'll send the full rhythm in the first email" (folds the depth into the waitlist itself — converts the uncertain-but-curious reader by moving detail past the form instead of before it). Exact choice in step 4.

*What does not belong:* first-in-line urgency (Committer), team credibility (Committer — trust-before-the-form is Committer's job, not Practical's), a curriculum roadmap (program is a living Playbook; a detailed map reads as overcommitted and drifts from brand voice), price comparison to other programs, another round of thesis (Analytical), outcome imagery ("what the greenhouse becomes" is a separate beat — anchoring it here vs. to Committer is a step-5 decision).

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

*CTA:* the final form. No secondary link — terminal section. Submit-button signpost carries the page's accumulated weight (exact wording in step 4). All earlier CTAs pointed here.

*What does not belong:* the fit gate (now in Practical), new program mechanics (Practical), thesis or peer proof (Analytical, Peer), aspiration re-heated at length (Gut), a founder-origin story (team credibility here is about who'll show up on the calls, not where the company started), urgency patterns beyond honest priority-queue math, "limited seats forever" or "one-time offer" framing (contradicts rolling admission).

---

# Section-by-section blocks

Each block below is one section on the page. Reader-type, subsection intent, status, beats, locked copy, drift notes.

---

## Hero (one-block merged layout)

- **Reader-type:** Gut.
- **Subsection intent:** Let the reader decide in ten seconds whether this page's worldview fits what they want from farming life.
- **Status:** **locked** 2026-04-22 (copy). **Step 5 re-locked 2026-04-27** (merged structure, replaces the earlier two-block split).

**Beats (visual layout):** *Step 5 re-locked 2026-04-27.*

Single block, photo-first editorial. All five elements (eyebrow → H1 → italic subhead → body → CTA) live in one stack on the right of the photo (desktop) or below it (mobile). The two-block split was abandoned because mobile readers landed on the emotional couplet without seeing what the page is — "coaching program for market gardeners" needed to land in the same breath.

- **Section structure (re-relocked 2026-04-29 night, full-bleed restored):** `<section id="hero" class="relative overflow-hidden md:min-h-[85vh] md:flex md:items-center">` — full-bleed cinematic, photo absolute-positioned with right-dense white scrim, text overlays right. Reverts the brief 2026-04-29 evening split-column experiment after Guillaume asked for full-cinematic full-width back. **The cropping fix:** `<img style="object-position: center 30%;">` shifts the crop window upward so more of the figure (face + arms-raised pose + upper body) stays visible on wide viewports — the woman is centered horizontally with face/arms in the upper third, so default `center center` was cropping too low.
  - *Desktop (md+):* full-bleed photo absolute-positioned with `bg-gradient-to-l from-white via-white/90 to-transparent` scrim; text overlays on the right. `min-h-[85vh]`. Right-aligned column (`max-w-xl md:text-right`).
  - *Mobile:* photo is a 55vh full-bleed band on top; text stacks below.
  - **Wider lesson logged:** when the hero photo is portrait, `object-position` tuning is the cheapest fix; restructure to a column only if the crop can't be made to work.
- **Stack order (top to bottom; epigraph-first re-lock 2026-04-29):**
  1. Epigraph (Lato italic, `text-lg md:text-xl text-farm-muted`, with curly quotes): "Farming is beautiful, but life's richer with energy left for the people in it." — philosophy-book register, sets the emotional tone before the categorical announcement.
  2. H1 (Fraunces, `text-3xl sm:text-4xl md:text-5xl`): "A coaching program for market gardeners" — promoted from eyebrow to page H1; semantic + visual headline.
  3. *(visual gap, `mt-8 md:mt-10`)* — separates the announcement from the descriptive chunk.
  4. Body (`text-lg md:text-xl`): "Sharpen your greenhouse. Harvest more from fewer beds. Earn more in fewer hours."
  5. CTA (whisper underline link): "Join the waiting list →"
- **Fit-decision beat:** closing sentence of the body paragraph ("Earn more in fewer hours."). The moment the aspiration gets a mechanism.
- **Above the fold at 85vh:** epigraph + H1 fully visible. Body + CTA peek as a scroll cue; full beat lands on a short scroll.
- **Transition into Drew:** no ornament, no divider. Drew opens on bg-white as a register shift from hero's farm-bg warmth.
- **CTA treatment:** underlined inline link in `farm-green`, right-aligned in the column. Not a button. The clear-door CTA lives in the persistent sticky nav, so Hero's CTA can stay a whisper.
- **Photo (locked 2026-04-29 late evening):** `assets/clients/ferme-decembre/6073DAB7-095E-4744-8045-67F8166BA650.jpg` — portrait orientation, market gardener tending tomato plants in a greenhouse with hands raised among the foliage. Closer, more intimate than the prior `drive-0416.jpg` (kneeling-to-tend-seedlings landscape), which moved to the `#not-alone` section banner. The new photo is also reused as the `#join` background bookend (see `#join` block).

**Locked copy:**

> **Epigraph:** "Farming is beautiful, but life's richer with energy left for the people in it."
>
> **H1:** A coaching program for market gardeners
>
> **Body:** Sharpen your greenhouse. Harvest more from fewer beds. Earn more in fewer hours.
>
> **CTA:** Join the waiting list →

**Drift notes:**
- Previous live body was "Small moves to get more out of every bed, so 40 hours is enough to run the farm. Same income, less grind." Then "More revenue out of the greenhouse, so you can cut field beds without cutting income. Same sales, fewer hours." Current 2026-04-27 lock: "Sharpen your greenhouse. Harvest more from fewer beds. Earn more in fewer hours." Three short sentences. Notable claim shift: from protective ("same income / without cutting income") to outcome-promising ("earn more"). Decision logged as deliberate hero-claim escalation by Guillaume; brand's "no claims, no promises on the course" rule pinches but is read as broad/aspirational rather than quantified-promise. Re-evaluate if cohort-1 outcomes don't substantiate the "earn more" framing.
- Previous structure (2026-04-23 lock) split the hero into two visually separate blocks: a photo+H1+subhead "mirror" block on top of a `bg-farm-bg` "named container" band below. The split fragmented the reading experience — mobile users landed on the poetic couplet but had to scroll to learn the page was a coaching program. Merged 2026-04-27 into a single stack with the eyebrow leading the column, so category identification lands above the fold.
- **Hierarchy inversion (2026-04-29):** previously the hero led emotional-first — *"Farming is beautiful"* was the H1, the program label was a small uppercase eyebrow. Inverted to category-first: *"A coaching program for market gardeners"* is now the H1, and the *"Farming is beautiful…"* couplet is demoted to an italic philosophy-book epigraph at the top. Strategic shift acknowledged: the page now leads with what-it-is and uses the poetic line as emotional prelude rather than headline. Trade-off: gut-sold readers may feel the emotional hook is muted; uncertain readers immediately learn the page's category.

---

## Allison's off-farm paycheck became optional

*Typographic split (relocked 2026-04-29):* Eyebrow *"The story that inspired the program"* (Rubik uppercase) sits above the H2 *"Allison's off-farm paycheck became optional"* at display size. Earlier wording journeys: two-beat title split (*"Same beds, bigger harvests"* H2 + *"Allison's off-farm paycheck became optional"* subhead) → promoted the lifestyle outcome to the H2 + meta-pointer subline ("The story that inspired the program.") → eyebrow + H2 (current). The promotion-to-eyebrow matches the eyebrow patterns now used in `#why-tomatoes` ("The focus" / "Greenhouse tomatoes") and `#information` ("So why a program?" / "Translating the techniques on our farm is hard").

- **Reader-type:** Peer, sub 1 (Drew arc).
- **Subsection intent:** Let the reader decide if a farmer like them has actually made this work.
- **Status:** **locked** (prose below). Visual layout below is outline-only; prose is the words.

**Beats (visual layout):** *Step 5 in progress 2026-04-23, from scratch (earlier reference notes discarded). Locked decisions listed below as they land.*

- **Q1 — shape: headline-first.** The two-sentence H2 ("Same beds, bigger harvests. Allison's off-farm paycheck became optional") sits as a big heading at the top of the section. Reader orients to the outcome, then reads the story for the *how*.
- **Q2 — photo placement: photo + flip-quote pair at the climax.** At the section's emotional peak, a photo of Drew and Allison (from `assets/clients/drew/Drew - Ghost House Farm/`) sits side-by-side with the flip quote — *"My wife was able to quit her job and join me full-time on the farm"* — in big italic pull-quote typography. Two-column visual pair at desktop; stacks on mobile.
- **Q3 — revenue numbers: triptych of illustrated scales.** Three hand-drawn botanical-style illustrations in seed-catalog register (single-weight line in farm-green ink on cream). Same modern commercial kitchen scale in each panel (per Guillaume's reference — rectangular digital scale with flat stainless platform, LCD display, buttons on right); only the pile of tomatoes + cucumbers grows — roughly 1x / 2.5x / 4x to echo $10k → $25k → $43k. Year + dollar amount captioned below each panel in small accent type. Replaces the single prose line at the end of the body. Production: generate with `openai-gpt-image` in three iterated passes (style sketch → first panel → match the other two).
- **Q4 — primary CTA + depth-ramp.** Primary CTA uses the page-default wording *"Join the waiting list →"* (consistent with nav + Hero) so the CTA muscle memory stays coherent across the page. Directly below, a quieter depth-ramp link: *"Read their 2025, week by week →"* → `/drew-season/`. Rendered in a muted underline register so it doesn't compete with the primary CTA. (Wording journey 2026-04-29: was *"Read Drew's 2025, week by week"* → *"Read what drove the change"* → back to the seasonal-walk framing as *"Read their 2025, week by week"*. The "their" applies the we-equals-farmers voice rule.)
- **Closing order (from locked copy):** photo + flip-quote pair → thesis bridge ("Two incomes from the same production.") → illustrated revenue triptych → primary CTA → depth-ramp link.
- **Q5 — ground color: white.** Drew opens on crisp white, reading as a new chapter after Hero's warm farm-bg. Gives the photo and illustrations maximum contrast; differentiates Drew's journalistic register from Hero's editorial warmth.
- **Q6 — reading width: `max-w-3xl`** (~768px) for the body prose. Photo + flip-quote pair and illustration triptych break out to wider layouts (`max-w-5xl` territory).
- **Illustration production notes:** PNG with **transparent background** (no rectangle, no paper fill — the ink sits directly on the page's ground color). Style must feel **hand-made** — visible line wobble, variable stroke weight, occasional overshoots at line joins, hand-inked character. Not CAD-clean, not vector-perfect. Reference: naturalist's sketchbook + seed-catalog plates with human hand visible.
- **Q7 — Drew naming: eyebrow above the H2.** Eyebrow text: *"Drew & Allison Story"* (was *"Drew · Ghost House Farm"*, updated to center the couple — the flip is Allison's return, so the eyebrow names both). Small accent-font uppercase, muted color. Scan-level peer identification.
- **Before/climb rhythm:** single flowing `max-w-3xl` prose column. Small year markers (*"2023"*, *"2024"*, *"2025"*) in accent-font uppercase as quiet rhythm labels where the narrative shifts year. No typographic dramatization of individual lines — structure work is carried by the eyebrow, H2, photo+quote pair, and illustration triptych.
- **Year blocks (2023 / 2024 / 2025): full-height photo beside whole year text.** Each year is now a 2-col grid where one column holds the entire year text (eyebrow + prose + quote + closing prose) and the other column holds a portrait photo that stretches to the full height of the text column (`sm:h-full object-cover`, no fixed aspect ratio on desktop). Photo width: `sm:w-56 md:w-64`. Sides alternate: 2023 photo right, 2024 photo left, 2025 photo right. Mobile stacks (image keeps `aspect-[4/5]` portrait crop). Photos:
  - **2023 (right):** `drew-season/images/2025-06-18-17.27.22-6b64bc70.jpg` — hand cradling a young tomato flower.
  - **2024 (left):** `drew-season/images/2025-06-04-17.57.02-305f5b43.jpg` — hand cupping a green tomato cluster.
  - **2025 (right):** `drew-season/images/2025-07-11-16.38.35-c4e9f5e9.jpg` — row of fruit-loaded tomato plants.
- **Layout updated 2026-04-29.** Replaced the prior small inline photo+quote pair pattern (where the photo only sat beside the quote, ~160px square) with the whole-year-beside-photo pattern. Visual rhythm: photo R / photo L / photo R alternation across the year-cluster.
- **Mobile reading order:** every year reads text-first on mobile (eyebrow → prose → quote → photo below). 2024 uses `sm:order-1`/`sm:order-2` classes to keep source order text-first while still rendering photo-left on desktop. 2023 and 2025 don't need reordering — their natural source order (text first, photo second) renders text-left / photo-right on desktop.
- **2025 flip climax:** photo + flip pull-quote pair, breakout to `max-w-5xl`. Photo: `IMG_1517 (1).JPG`. Big italic pull-quote right of the photo. Caption: *Drew, on Allison's first full season.* (Was *"Drew, after the 2024 season"* — moved to 2025 segment 2026-04-27 when the year-rhythm prose grew a 2025 beat.)
- **Thesis bridge:** italic centered *"Two incomes from the same production."* line between the 2024 flip climax and the triptych. Voice-shift from narrative to thesis, short breathing space before the evidence.

**Locked copy:**

> **Ghost House Farm** *(eyebrow, centered)*
>
> *(3-up illustrated stat grid: ½ acre · 30 × 80 ft greenhouse · 30+ vegetables. Each tile = small rough-scribble sketch + label. Replaces the opening quote 2026-04-29.)*
>
> **2023**
>
> Drew runs Ghost House Farm full-time. Allison works off the farm to complete the family income. They are one of the better tomato producers in the area. The greenhouse contributes $10,000 that year.
>
> *"Our first spring in the hoop house was awful. It was miserable."* — Drew (quote paired with a small 2023 photo of the farm)
>
> **2024**
>
> Drew and Allison stabilize the greenhouse climate and dehumidify to steer away from the diseases that ruined 2023. They focus on improving their tomato techniques: variety selection, multiple leaders, pruning, water timing. In August, Drew shares on Instagram:
>
> *"As of today, we have DOUBLED tomato production compared to last year."* — [Instagram, August 2024](https://www.instagram.com/p/C_UBRhWuXdg/). Paired with `drew-season/images/2025-07-11-16.38.33--1--59e7f4bd.jpg` (small ripe-red-cluster photo, mirrored grid with quote-left/photo-right to alternate from the 2023 and 2025 small pairs).
>
> They overshoot market projections and make a profit for the first time. The greenhouse contributes $25,000.
>
> **2025**
>
> Allison joins Drew full-time on the farm. Drew starts consulting with Antoine to steer tomatoes and improve fruit setting. In early July, they write Antoine:
>
> *"We've harvested more cherry tomatoes than all of 2023, before we'd even started picking that year."* — Drew (email to Antoine, early July 2025; paired with `drew-season/images/2025-07-11-16.38.35-c4e9f5e9.jpg` small fruit-loaded plant-row photo)
>
> Greenhouse contribution: $43,000.
>
> *"My wife was able to quit her job and join me full-time on the farm."* — Drew, on Allison's first full season (paired with the flip-climax photo)
>
> *Two incomes from the same production.* *(Thesis bridge: italic centered, between the 2025 flip climax and the CTA.)*

**Drift note:** revenue triptych ($10k/$25k/$43k) absorbed into the year-rhythm prose 2026-04-27. Each year's body now ends with the greenhouse-contribution figure, so the standalone triptych in #techniques-known is no longer needed (and was removed). Allison-joining flip moved from "after 2024 season" to the 2025 segment to give 2025 a felt climax beat (yields had jumped in 2024; lifestyle change consolidated in 2025).

---

## What a bed can buy back

- **Reader-type:** Peer, sub 2 (generalization of the Drew lever).
- **Subsection intent:** Let the reader decide if the same lever reshapes their own life.
- **Status:** step-4 prose **locked**; step-5 structure **locked** 2026-04-23 (below). Step-6 HTML render dispatched to background agent.

**Step-5 locked structure:**

1. **Eyebrow + H2** (no terminal period; updated 2026-04-29):
   > **The angle**
   > Making our beds pay for the life we want

   Earlier wordings: *"The more you grow per bed, the more room your life gets back"* (initial step-5 lock) → *"Harvest more per bed to build the life you want"* (rendered, mid-iteration) → *"Making our beds pay for the life we want"* (locked H2 only) → current eyebrow + H2. Eyebrow added 2026-04-29 to match the eyebrow rhythm now used in `#story`, `#why-tomatoes`, and `#information`.

2. **Italic intro callout** (muted, one line above the cards):
   > *The bed is already paid for. The hours are spent. What grows on top is yours.*

3. **4-card grid** (2×2 desktop, 1-col mobile). Each card: bold title (no terminal period) + prose body. Card 4 runs one sentence longer than the others — accepted imbalance, card carries the HR-relief beat.

   | # | Title | Body |
   |---|---|---|
   | 1 | Fewer beds to hit your sales | Less walking, less weeding, fewer problems to chase. The farm gets quieter. |
   | 2 | Money to hire out what drains you | The accounting gets done by someone who actually likes doing it. Your Sundays come back. |
   | 3 | Farm income that carries the household | The off-farm paycheck, the partner's second job, the winter gig. Optional again. And the hours, back to your family. |
   | 4 | Staff you can pay what good people are worth | Better candidates walk in. They stay longer. Experienced hands mean more done, faster. Less hiring, less training, less HR headaches. More energy left in the tank. |

4. **Closer line** (muted italic, centered below cards):
   > *Behind every one: time with the people you started farming for.*

5. **No CTA in this subsection** — per step-2 Peer ownership, the section's CTA lives at the end of sub 1 (Drew arc). Sub 2 closes on the emotional bridge and readers flow into Analytical.

**Locked copy (step-4, verbatim — source of truth for the render):**

> *The bed is already paid for. The hours are spent. What grows on top is yours.*
>
> **Fewer beds to hit your sales.** Less walking, less weeding, fewer problems to chase. The farm gets quieter.
>
> **Money to hire out what drains you.** The accounting gets done by someone who actually likes doing it. Your Sundays come back.
>
> **Farm income that carries the household.** The off-farm paycheck, the partner's second job, the winter gig. Optional again. And the hours, back to your family.
>
> **Staff you can pay what good people are worth.** Better candidates walk in. They stay longer. Experienced hands mean more done, faster. Less hiring, less training, less HR headaches. More energy left in the tank.
>
> Behind every one: time with the people you started farming for.

---

## Greenhouse tomatoes (Analytical sub 1, eyebrow "The focus")

- **Reader-type:** Analytical, sub 1 (the lever).
- **Subsection intent:** Let the reader decide if the thesis applies to their farm.
- **Status:** **locked** (prose below). Visual layout is outline-only.
- **Header (relocked 2026-04-29):** Eyebrow *"The focus"* sits above the H2 *"Greenhouse tomatoes"*. Wording journey: *"Starting with the bed that'll free you the most"* (working name) → *"Why we focus on tomatoes"* (rendered) → *"Why we focus on greenhouse tomatoes"* (locked 2026-04-27) → eyebrow *"The focus"* + H2 *"Greenhouse tomatoes"* (current). Eyebrow names the section's purpose; the H2 is now a quiet noun-only label, lighter than a declarative thesis.
- **Progressive disclosure (added 2026-04-29, refined same day):** the four main cards stack vertically (single column inside `max-w-3xl`) with horizontal internal layout — each card is a `<details>` accordion where the summary is a single row of `[sketch | headline | caret]` separated by `border-t border-farm-mid/15` lines. Click reveals the supporting quote/claim below. Same `<details>` mechanic as `#program`, `#team`, and `#information`. Sketch shrunk from `w-32 h-32` to `w-16 h-16 md:w-20 md:h-20` to fit the horizontal row. Bonus block also wrapped in a single `<details>` summarized as *"Bonus · More reasons tomatoes are our lever →"* — collapsed by default, reveals the 3 bonus cards on click. **Closer position 2026-04-29:** *"On most diversified farms, tomatoes are the low-hanging fruits."* now sits AFTER the bonus block as the section's true thesis line, landing once both evidence layers (per-card receipts + bonus block) have been presented.

**Beats (visual layout):**

- Intro line (muted, under heading): "Not every bed gives you this lift. One does, by a lot."
- Left paragraph: tomatoes sit on most market gardens already, ceiling higher than any other crop.
- Center: big "20 to 30x" pull number. Caption: "One tomato bed versus one bed of beets, kale, or onions."
- Drew lb/ft² pull-quote callout substantiates "yield doubles" before the labor-intensive paragraph.
- Right paragraph: tomatoes are the most labor-intensive beds; when yield doubles, cut half the beds or keep them and automate.
- Dan pull-quote callout.

**Locked copy:**

> A well-run bed of greenhouse indeterminate tomatoes earns what 20 to 30 beds of beets, kale, or onions earn. One crop, 20 to 30 times the pay per bed.
>
> Drew's Ghost House Farm: three greenhouse crops (four-season salad mix, early tomatoes, early cucumbers) carry 70% of the farm's revenue. The other 30 vegetables carry the rest.
>
> That's the lever.
>
> Drew, Ghost House Farm: *"We were at just around a pound per square foot with slicers in 2023, and we were one of the better tomato producers in the area. We're up to almost five pounds per square foot. We're trying to hit six this year."*
>
> Greenhouse tomatoes are also the single most labor-intensive bed on a market garden. When yield doubles and your market already takes every tomato you grow, you get a choice: cut half the beds and keep the same sales, or keep the beds and automate the minute-by-minute climate work.
>
> Dan, Broadfork Farm: *"Automation helps us continue to run the farm when we're not there. We get better quality and better yield with the tunnel totally automated without us than if we were there managing it. The tunnel will do a better job by itself."*
>
> Either path, hours come back, and your most productive ground is yours again, to plant with something higher-margin.

**Drift note:** The Drew lb/ft² quote (sourced from `docs/landing/sources/drew-gfm-podcast-quotes.md`) was added to substantiate the "yield doubles" hinge before the section pivots to the choice. Anchors the doubling claim in a peer-verifiable unit (lb/ft²) and establishes that Drew's pre-Orisha starting point was already "one of the better producers in the area," not a turnaround story from rock bottom.

---

## Techniques are real and proven (Analytical sub 2)

- **Reader-type:** Analytical, sub 2.
- **Subsection intent:** Let the reader decide if the techniques themselves are real and proven.
- **Owns:** "not secret, not new" framing; Mefferd book; Mefferd's yields doubling on his own farm; Quebec 4x small-grower figure. External authority only.
- **Status:** step-4 prose **locked** 2026-04-22. **Step-5 structure (Direction B) locked 2026-04-27.**

**Beats (visual layout, locked 2026-04-27 — Direction B):**

Two uniform rows, alternating photo sides. Each argument gets the same template (photo + claim/quote text), each gets equal weight. Replaces a longer in-iteration render that had a separate 4× stat block + a Drew triptych below — Drew triptych removed (one-farmer arc duplicates `#story`'s narrative; the cohort 4× claim does the analytical-numbers work).

- **Eyebrow + H2 (relocked 2026-04-29):** Eyebrow *"Nothing's new"* (Rubik uppercase) sits above the H2 *"The techniques are known"* (max-w-3xl, centered). The italic muted subhead *"They're not secret, and they're not new."* was retired and its idea compressed into the eyebrow. Matches the eyebrow + H2 pattern now used across the page (`#story`, `#leverage`, `#why-tomatoes`, `#information`, `#program`).
- **Row 1 — Andrew (photo left, quote + book line right):**
  - Photo: `assets/team/Andrew/andrew-industrial-greenhouse.jpg` (`md:col-span-2`, aspect-square, rounded-card). Caption: *Andrew learning industrial greenhouse techniques.*
  - Right column (`md:col-span-3`): pull-quote *"First year I applied big greenhouse techniques, my yields doubled."* — Andrew Mefferd. Below the quote, muted body line: *Andrew wrote* [The Greenhouse and Hoophouse Grower's Handbook](https://www.johnnyseeds.com/...)* to share these techniques with small growers.* (No bg-farm-bg aside panel; the book mention inlines as a quiet sentence.)
- **Row 2 — Antoine (claim + 2-sentence body left, drone photo right; alternating side):**
  - Photo: `assets/clients/jardin-inverness/ferme antoine.jpg` (`md:col-span-3`, aspect-[16/9], rounded-card, `md:order-2`). Bumped from `col-span-2` and `aspect-[16/10]` to give the aerial drone shot real horizontal sweep + matching height. Caption: *Les Jardins d'Inverness, Antoine's farm.*
  - Left column (`md:col-span-2`, `md:order-1`): heading-scale claim *"And they work at small-farm scale."* Below it, muted 2-sentence body: *Quebec consultants have adapted big greenhouse techniques to small farms.* *[Antoine](#antoine) and other growers learned from them to regularly hit 4× the average yield in their 30x100 greenhouse.* The "Antoine" word links to his bio anchor `#antoine`. The 4× number is emphasized inline at `text-2xl md:text-3xl` (one step up from body, not display-loud).
- No CTA (Analytical section's CTA lives at end of Sub 4).

**Locked copy (step-4):**

> The techniques are known. They're not secret, and they're not new.
>
> Andrew Mefferd wrote *The Greenhouse and Hoophouse Grower's Handbook* to carry techniques from industrial greenhouses into market gardens. The first year he applied what he'd learned on his own farm, his yields doubled. Same greenhouse, twice the harvest.
>
> Quebec consultants have adapted big greenhouse techniques to small farms. [Antoine](#antoine) and other growers learned from them to regularly hit 4× the average yield in their 30x100 greenhouse.

**Iteration log:**

- 2026-04-23: A 3-card variant (photo | pull-quote | book cover) was rendered and reviewed, then rolled back because the 3 distinct visual registers produced noise rather than rhythm.
- 2026-04-27: Three structural variants rendered into `techniques-known-options.html` for comparison: Option 1 (3-up card grid), Option 2 (uniform 3-row stack), Option 3 (hero quote + stats strip). Option 3 iterated several times. After Drew's block was removed (one-farmer arc duplicating `#story` narrative), the section dropped from 3 arguments to 2 (Andrew = source, Antoine = small-farm proof). Direction B (uniform 2-row narrative, alternating photo sides) chosen as the cleanest fit for parallel-content structure. Andrew's quote refined to *"First year I applied what I'd learned from the big greenhouse growers, my own yields doubled."* Andrew's book aside panel removed; book mention inlined as muted sentence. Antoine drone photo (`ferme antoine.jpg`) replaces the `one-tunnel-equals-four` sketch — the cohort claim now anchored on a real small-farm photo with caption *Antoine's farm.* The big "4×" display stays inline within the body sentence.

Assets used: Andrew photo, Antoine drone photo, both inline link to the Mefferd book on Johnny's. The `one-tunnel-equals-four.png` sketch and the `drew-scale-test-02.png` placeholder are no longer used in this section but remain on disk.

---

## Translating the techniques on our farm is hard (Analytical sub 3)

- **Reader-type:** Analytical, sub 3.
- **Subsection intent:** Let the reader decide that the real problem on their farm isn't missing information, it's the weekly judgment calls only they can see.
- **Owns:** Andrew + Orisha *6 Steps* as "the information is out there" authority; pivot showing the content-only path isn't enough (evidenced by the questions farmers keep sending us); the weekly-calls language; the four faces of the problem in reader terms (week-to-week unknowns, *am I doing it right?*, stuck alone, every farm is specific).
- **Status:** **locked** 2026-04-22 (prose below). No conversion CTA here; bridges into Sub 4. **Visual structure (step 5) locked 2026-04-27.**

**Beats (visual layout) — shape B (prose with question-list breakout):**

- max-w-3xl prose column, **bg-white** ground (continuous Analytical run; Practical 1 will break to bg-farm-bg).
- **Eyebrow + H2 (relocked 2026-04-29):** Eyebrow *"So why a program?"* sits above the H2; H2 *"Translating the techniques on our farm is hard"* (no terminal period). The eyebrow names the question the section answers; the H2 names the answer in farmer-voice (we = farmers; "our farm" applies the locked we-equals-farmers rule). Wording journey: *"Why information isn't enough"* (locked 2026-04-22, replaced 2026-04-27) → *"Why we need more support"* (replaced 2026-04-29) → current eyebrow + H2 split, which reframes the problem from abstract ("information isn't enough") to felt-experience ("translating to our farm is hard").
- **No eyebrow** (continuous with techniques-known register).
- **Closer treatment:** centered italic Fraunces, larger than body, on the same bg-white ground. Two sentences: "No theory can answer those for you. Every greenhouse is specific, every week is new." Internal period between sentences stays; no terminal period on the H2 itself.
- **Drift note:** the visual list lightly tightens "your weather this month" → "this month's weather" for cleaner parallel structure across the four lines. Locked prose stays as-is in this outline; the tightening lives only in the visual breakout.
- **Three eyebrow-led blocks** (final form, locked 2026-04-27 after iteration). Mirrors `#join` pattern. Each block: Rubik accent eyebrow + body line at canonical body size `text-lg md:text-xl`. `space-y-8 md:space-y-10` between blocks.
  - **The information is out there** → "Andrew wrote the book. We made a free online course with Orisha."
  - **It's not enough** → "Every farm is different. Folks send us questions all the time."
  - **The devil's in the details** → "Changing how we grow comes with a lot of calls to make and so little time to figure out." (Body relocked 2026-04-29; "Every farm is different" moved upstream into the "It's not enough" body. New body names the change-effort directly: changing practice produces decisions; decisions outpace time to think.)
- **Pull-quote with left-border** (replaces the centered italic poem). Reuses the Mefferd-quote visual pattern (`pl-5 md:pl-6 border-l-2 border-farm-green/60 font-body italic text-lg md:text-xl text-farm-dark leading-snug space-y-3 mt-10 md:mt-14`). Five questions stacked one per line, the climactic *Am I doing it right?* slightly weighted (`font-medium`). Reads as the farmer's inner voice. Questions converted from statement-fragments to proper question form so the italics feel earned. Locked questions:
  - *Which move do I prioritize?*
  - *How do I adapt to that variety?*
  - *I irrigate many times a day. Why do I still see blossom-end rot?*
  - *Am I pruning enough, or pruning too much?*
  - ***Am I doing it right?*** (climactic, weighted)
- **Closer (shortened):** *"No theory can answer those for you."* The contextual reason ("Every greenhouse is specific, every week is new.") was dropped — its theme now lives in the third eyebrow block ("Every farm is different"). Centered italic muted (`font-body italic text-lg md:text-xl text-farm-muted text-center`).
- **Iteration log:** centered italic poem treatment was tried, then replaced. The stacked centered italic was reading as decorative-poetry rather than lived-experience inner voice; pull-quote treatment with left-border lands as overheard farmer thoughts, matches an existing visual pattern on the page, doesn't compete with the prose register above.
- **Photo added 2026-04-27:** two-column layout, photo `assets/clients/ferme-decembre/IMG_3719.jpg` on `md:col-span-5` (left), text on `md:col-span-7` (right). Photo is `aspect-[4/5] object-cover rounded-card` with `md:sticky md:top-24` so it stays visible while the reader scrolls through the eyebrow blocks + pull-quote. Subject: a farmer training a young tomato plant onto a string trellis, focused expression, working hand visible — directly anchors the section's *weekly judgment calls* register. H2 stays full-width above the grid (max-w-3xl wrapper). Closer stays full-width below the grid (max-w-3xl wrapper, centered italic muted). Stacks on mobile (photo above text).

**Locked copy:**

> Andrew wrote the book. We made the most concise course we could with Orisha. For free. The information is out there.
>
> But it's not enough. Folks send us questions all the time.
>
> What's hard is the calls you have to make on the farm, week after week. Which move to prioritize. How to adapt a principle to your varieties, your tunnel, your weather this month. Whether you're pruning enough, or pruning too much. *Am I doing it right?*
>
> No theory can answer those for you. Every greenhouse is specific, every week is new.

---

## Not doing it alone (Analytical sub 4, eyebrow "What it's about")

- **Reader-type:** Analytical, sub 4.
- **Subsection intent:** Let the reader decide if they want to be in a room where they work on their farm's weekly calls with others, instead of making them alone.
- **Owns:** Drew + Gordon as honest range of outcomes; honest admission (no miracles, we don't know everything, Playbook is as good as the seasons we've gathered); program-as-place positioning (pool what we know, work on your obstacles, build tools for the next season, for you and every farmer after); reader-desire mirror ("cut the workload without cutting your income"; "lean on what others have figured out than do it alone"). **Section fit-decision beat lands here** (the moment the Analytical reader sees the program isn't repackaged content — it's a place to do the work books can't do).
- **Status:** **locked** 2026-04-22 (prose below). Thesis-aware CTA at end. **Visual structure (step 5) locked 2026-04-27.**

**Beats (visual layout) — restructured 2026-04-29 (prior shape C with Drew + Gordon case-study breakout retired):**

- max-w-3xl prose column. bg-white ground (continuous Analytical run).
- **Section photo as full-height right column (re-relocked 2026-04-29 night):** `assets/clients/ferme-decembre/drive-0416.jpg` — repurposed from the prior hero. Two-column section: ALL text (eyebrow → H2 → subtitle → disclaimer paragraphs → "To" bullet list) lives in `md:col-span-7` on the left; photo lives in `md:col-span-5` on the right and stretches to match the full section height via grid `md:items-stretch` + `md:h-full` on the figure + `h-full` on the img. Mobile: figure carries `aspect-[4/3]` so it has a sensible height; desktop overrides with `md:aspect-auto md:h-full` to release the aspect lock and let the figure stretch. Img: `w-full h-full object-cover rounded-card`. *Iteration history same day:* (1) cinematic full-width banner `aspect-[2/1]` above the prose — pulled emotional weight forward of the H2, dropped; (2) right column matched only to the eyebrow+H2+subtitle row — disclaimer + bullet list dangling below at prose-column width, photo too short to feel anchored, dropped; (3) current — text stack on left, photo full section-height on right.
- Eyebrow *"What it's about"* + H2 *"Not doing it alone"* + italic muted subtitle *"Having everything relying on our shoulders is heavy."* (subtitle added 2026-04-29 — names the felt weight that the "To" list below offers to lift).
- **Disclaimer paragraph (body prose):** *"This program is not a proven silver bullet. It couldn't. Every farm is different."*
- **Lead-in to the list (body prose, with colon):** *"This program's a structure to help us transform our farm:"*
- **"To" infinitive list (3 items, bulleted with quiet middle-dot markers, body prose register):**
  - To follow concrete actions that work on many farms.
  - To pool our experience to overcome roadblocks.
  - To ride the momentum of everybody working on the same goal.
- **No CTA in this section.** Bridges into `#program` which carries the next CTA.

**Retired 2026-04-29 (preserved here as reference):**
- Drew + Gordon paired case-study photo breakout (editorial alternation, photos `IMG_1517 (1).JPG` and `Gordon - Ten Mothers Farm.jpg`, italic narration *"Worked with us across two seasons..."* / *"Worked with us one season..."*).
- Honest-admission paragraph (*"Every farm is different. Every climate is different. Our Playbook is as good as..."* — its core idea collapsed into the new disclaimer's *"Every farm is different."*).
- Lead-in *"We work with growers on those calls. Not every season ends the same way."*
- Program-as-place paragraph (*"What we can do is build a place where we pool what we know, work on the obstacles you're facing..."* — its idea collapsed into the new *"To pool our experience to overcome roadblocks."* line).
- Reader-desire mirror + CTA pill (already retired earlier 2026-04-29).

**Locked copy (relocked 2026-04-29):**

> This program is not a proven silver bullet. It couldn't. Every farm is different.
>
> This program's a structure to help us transform our farm:
>
> - To follow concrete actions that work on many farms.
> - To pool our experience to overcome roadblocks.
> - To ride the momentum of everybody working on the same goal.

---

## Mid-page CTA band (green) — **DROPPED 2026-04-27**

- **Status: dropped.** Not doing it alone (Analytical sub 4) and The Program (Practical sub 3) each carry a green pill at their close. A third "Mid-page CTA band" between or after them reads as redundant pill-stacking and breaks the quiet-journal voice.
- Original draft kept here for reference only:
    - "Already see yourself in this? The program opens June 2026."
    - Button: "Join the waiting list"

---

## The Program

- **Reader-type:** Practical, sub 3 (a month, pictured).
- **Page placement:** sits **immediately after Not doing it alone** (Analytical sub 4). Breaks the strict Analytical→Practical bucketing. Argument: Not doing it alone tells the reader "you'd rather not do this alone, here's the room"; The Program shows what the room actually looks like (monthly goal, weekly call, applied work). Bridges Analytical conviction to felt mechanics before the Practical fit/cost gates land. Order locked 2026-04-27.
- **Subsection intent:** Let the reader decide if this program fits the life they already have.
- **Status:** **locked** (prose below). **Visual structure (step 5) locked 2026-04-27 — variant A (4-step accordion), lean treatment.**

**Beats (visual layout) — variant A, lean:**

- bg-white ground (continues from `#not-alone`).
- Section ID: `id="program"`. Slots immediately after `#not-alone`.
- **Eyebrow + H2 (relocked 2026-04-29 second pass):** Eyebrow *"The rhythm"* + H2 *"How a week actually looks"* (no period). The 2h commitment moved out of the H2 into a dedicated callout (see below). Wording journey: *"The program"* → *"2 hours a week to reinvent your life"* → *"2 hours a week to transform our farm"* → *"How a week actually looks"* (current).
- **Section structure (restructured 2026-04-29 second pass):** retired the 4-step accordion (one goal / videos / on your farm / weekly call). New shape inspired by a competitor reference: two-column on desktop, stacks on mobile.
  - **Left column (col-span-7) — weekly timeline.** Vertical line with circle markers. Four day-anchored beats:
    - **Monday** — New 5-minute video drops. Phone-watchable between rows.
    - **Wednesday** — 2-minute check-in. Logs our progress. Surfaces what's stuck. *(NEW beat — added 2026-04-29.)*
    - **Friday** — Optional 60-minute live call with Andrew, Antoine, Guillaume, and other farmers. Recorded if we miss it.
    - **Anytime** — The forum is open. Ask, answer, share what worked.
  - **Right column (col-span-5) — "The whole ask" callout** on `bg-farm-dark` with white text. Eyebrow *"The whole ask"*, big numeral *"2h"*, italic *"a week"*, body *"That's it. The rest of our time stays where it belongs: in the soil, with our family, or simply at rest."* Acts as the time-commitment anchor that previously lived in the H2.
- **Subhead added 2026-04-29 (third pass):** italic muted line under the H2: *"One visible goal at a time. So we can focus, quickly see results, be motivated."* Brings back the goal-focus framing that the retired step 1 carried.
- **Progressive disclosure added 2026-04-29 (third pass):** each timeline item is now a `<details>` accordion. Summary = day label + 1-line description (visible by default). Body reveals on click — content merged from the prior 4-step accordion's expanded prose:
  - **Monday expand** = step 2's expanded body: *"What to look for in our plants, the specific moves to try."* + *"To keep information from piling up, videos stay short, focused on the current goal, and spread across the seasons."*
  - **Wednesday expand** = pending-verification placeholder.
  - **Friday expand** = step 4's expanded body: *"On these calls, we tackle what theory cannot. Watching others' roadblocks often helps us move faster."*
  - **Anytime expand** = step 3's expanded body: *"We answer once a week. The rest happens inside the work we already plan: pruning, scouting, harvesting, sharpened by the goal."*
- **Wednesday check-in flag (2026-04-29):** searched `brand/docs/` and `docs/` for any 2-minute check-in mechanism in the program. The only "check-in" hits are Gordon's *private* weekly notes to Orisha (not a program-side feature) and Helper's 2-minute weather reassessment (different product entirely). The Wednesday line is un-substantiated content from a reference-design merge. Either confirm a check-in mechanism is genuinely offered, or remove/replace the line before the page goes live.
- **Retired 2026-04-29 second pass (preserved as reference):** 4-step accordion (numbered 01-04) with sub-headings *"One visible goal at a time"*, *"5-min videos"*, *"On your farm"*, *"Weekly live call"*. Step 1's body is now the new subhead. Step 2/3/4 expanded prose absorbed into Monday/Anytime/Friday accordions.
- **4-step accordion (`<details>`)**, all closed by default, native `<summary>` styled to hide the disclosure triangle and use a custom rotating caret. Each summary shows: small Rubik step number (01/02/03/04) · Fraunces title · small muted one-line teaser. Expanded body holds the longer detail.
  - **Step 1 — One visible goal at a time** · *So we can focus, quickly see results, be motivated.* (Expanded: group-momentum content folded in.)
  - **Step 2 — 5-min videos** · *Guide us toward the goal. Dripped weekly. Rewatchable.* (Expanded: "What to look for in our plants, the specific moves to try. Phone-watchable between rows. / To keep information from piling up, videos stay short, focused on the current goal, and spread across the seasons.")
  - **Step 3 — On your farm** · *Pruning, scouting, harvesting, sharpened by the goal.* (Expanded: "Everything happens inside the work we already plan. A community forum runs alongside: we answer once a week.") Title refined 2026-04-29 from "Applied on your farm" — "Applied" was a participle that didn't sit as a noun-phrase title alongside the other accordion steps.
  - **Step 4 — Weekly live call** · *60 min with Andrew, Antoine and Guillaume to overcome obstacles we face.* (Expanded: "5-min videos guide us forward and uproot obstacles. On these calls, we tackle what theory cannot. / Watching others' roadblocks often helps us move faster.")
  - **Reorder 2026-04-29:** Weekly live call moved from step 3 to step 4 (last). New flow: goal → videos → applied work → live call. The call now lands as the *backstop* for what the videos and applied work haven't resolved, rather than as a mid-flow event. Pairs with the new subtext that frames the call as obstacle-overcoming, not generic coaching.
- **Support strip dropped.** Support content (recordings, forum, no-put-on-spot, group momentum) folded into the accordion bodies of step 1, 3, 4.
- **Closer + CTA (first goal folded in, refined 2026-04-29 evening):** eyebrow + italic line + green pill stack. Eyebrow (uppercase Rubik accent, farm-mid): *"Starting this June"*. Goal line below in italic Fraunces: *"Our first goal: more fruit per plant, consistently."* Refinement journey same day: technical *"Our first goal: build fruit load without exhausting the plants. If that slots into your week, put your name on the list."* → plain-language casual *"First goal: get plants to bear more tomatoes, consistently. Wanna join us?"* → temporal-anchored single-line *"Starting this June, our first goal: more fruit per plant, consistently."* → current eyebrow-led structure (temporal anchor promoted to eyebrow, goal line standalone). The eyebrow promotes the June launch as a dateable beat, the italic goal stays focused on the technical aim. *"Our first goal"* preserves the communal we-equals-farmers voice. The green CTA pill below carries the action call.

**Beats (visual layout):**

- Heading: "The program."
- Sub: built around the translation problem. Each month, one goal small growers can act on in their own greenhouse, from their own starting point.
- Flow accordion (native `<details>`, 4 steps, all closed by default, multiple can open). Summary shows step number + title + one-line descriptor; expanded detail below.
    - Month, one goal.
    - Short video, frames the goal. (Phone-watchable between rows — fold this lifestyle detail into the locked copy when the section is rendered; pulled from How-to-join 2026-04-27.)
    - Weekly live coaching, your farm's reality.
    - On your farm.
- Focus: greenhouse. This year: tomatoes. Cucumbers next, then lettuce.
- First goal callout: "Build fruit load up without exhausting plants."
- **Workload anchor** (centered, big Fraunces numeral + small uppercase Rubik caption, sits between the first-goal callout and the closer so the closer's "if that slots into your week" pays it off): "2 to 3 hrs a week" / *Mostly work on your own plants*. Moved here from How-to-join 2026-04-27 (workload is a Program-section question, not a how-to-join question; the closer wraps it cleanly).
- Closer (italic): "The Playbook is a living thing. It grows every season from what farmers surface in their own fields, and the tools get better as we go."

**Locked copy:**

> Each month, one goal for everyone in the program: picked to match what you need to focus on that month. A short video frames it: what to look for in your own greenhouse, the specific moves to try. Five minutes, rewatchable.
>
> Everyone works the same topic at the same time. That's where the group gets its momentum. Questions pile up on the same thing from different farms, and the exchange gets specific fast: different soils, different climates, different setups, same problem.
>
> Weekly live calls with a mix of Guillaume, Antoine, and Andrew. Sixty minutes. You bring the obstacles and uncertainties that came up during the week: photos, numbers, questions. We work out your next action to move forward.
>
> Recorded, so missing one is fine. If you join live, bring what you have. Or just listen while you answer emails. You won't be put on the spot.
>
> Between calls: a community forum. We answer once a week.
>
> The rest of the week: everything happens inside the work you already planned. Pruning, scouting, harvesting, sharpened by the goal.
>
> First goal: build fruit load without exhausting the plants.
>
> *If that slots into your week, put your name on the list.*

**Drift note:** earlier outline drafts had "monthly live call, about 90 minutes, Guillaume and Andrew." Locked copy replaces this with weekly 60-min calls, a mix of Guillaume/Antoine/Andrew, plus a community forum and group-momentum framing.

---

## What it starts to feel like (`#outcomes`)

- **Reader-type:** Practical sub 4 (the imagined future). Slots between `#how-to-join` and `#team` when picked back up.
- **Subsection intent:** Let the reader feel what the greenhouse becomes a season in, after the work has compounded.
- **Status:** **parked 2026-04-27.** Step 4 partially drafted in conversation (4 cards tightened, Drew quote candidate vetted at three lengths: full transcript / 3-sentence curated / 1-sentence punch) but not locked. Page ships fine without it; revisit when there's appetite to round out the Practical arc.

**Conversation drafts (not yet locked):**

- H2: *"What it starts to feel like"*
- Subhead: *"A season in, the greenhouse feels different. Not louder. Quieter."*
- Card 1: *Plants carrying more fruit.* / "More to pick each week, on the same beds you already planted."
- Card 2: *A harvest that matches the market.* / "Fewer gluts, fewer gaps. What you grow tends to sell at full price." + Drew quote (length TBD).
- Card 3: *Ahead of the plant, not behind it.* / "Acting before the problem shows up in the fruit. Less second-guessing, less catching up."
- Card 4: *A greenhouse staff can actually run.* / "Clear enough decisions that you don't have to stand over every one."

**Beats (visual layout):**

- Heading: "What it starts to feel like." (alt: "What changes in the greenhouse.")
- Sub: A season in, the greenhouse feels different. Not louder. Quieter.
- Four stacked cards:
    - Plants carrying more fruit. More to pick each week, on the same beds you already planted.
    - A harvest that matches the market. Fewer gluts, fewer gaps. What you grow tends to sell at full price.
    - Ahead of the plant, not behind it. Acting before the problem shows up in the fruit. Less second-guessing, less catching up.
    - A greenhouse staff can actually run. Clear enough decisions that you don't have to stand over every one.

**Quote candidate when section locks:** Drew on the quality side of the lift, for the "harvest matches the market" card. *"We don't have many problems with splitting. We have very few problems with blossom end rot. Almost everything that comes out of the greenhouse goes to market."* (Source: `docs/landing/sources/drew-gfm-podcast-quotes.md`.) "Almost everything goes to market" is the felt translation of "matches the market" — no #2 pile, no waste, no second-grade pricing.

---

## Who this is for

- **Reader-type:** Practical, sub 1 (fit gate).
- **Subsection intent:** Let the reader decide if the program is designed for their specific situation before they invest another minute reading.
- **Status:** Copy locked 2026-04-22. **Step 5 locked 2026-04-23** (step 5.1 prose refinement applied below).

**Beats (visual layout):** *Step 5 locked 2026-04-23.*

Layered shape the eye walks (headline → hook → detail → resolution):

- **Layer 1 — Headline:** H2 *"Who this is for"*. Scan-level orientation.
- **Layer 2 — One-line hook:** Two column headers side-by-side: *"A good fit"* / *"Not designed for you"* in accent-font uppercase (farm-mid color). Binary self-sort at a glance, before any criteria are read.
- **Layer 3 — Optional detail:** Short criterion lines beneath each header (one line per criterion, scannable). The uncertain reader reads; the gut-sold reader skips.
- **Layer 4 — Resolution (removed 2026-04-27):** the italic closer *"We'd rather tell you up front than have you waste a season on the wrong thing."* was pruned. The two columns + criteria do the fit-sort on their own; the closer was preachy filler.

**Fit-decision beat:** lands in Layer 3 — the moment the reader reads their situation in one of the two columns. Must be above the section's fold. No scrolling required to make the fit decision.

**Progressive disclosure:** by scan-register, not by `<details>` expand. Scanner who sees themselves in a header can leave; uncertain reader reads the criteria; nothing is hidden.

**Ground color:** `bg-farm-bg` (warm cream). Editorial register; not clinical white.

**Layout:** `max-w-5xl` outer container.
- **Header row (added 2026-04-29):** 12-col grid `md:grid-cols-12 gap-8 md:gap-12 md:items-center mb-12 md:mb-16`. H2 left at `md:col-span-8`; portrait photo right at `md:col-span-4` (`assets/clients/ferme-decembre/IMG_7680.jpg` — market gardener smiling with a giant heirloom tomato held over one eye, tomato plants in the frame). Photo class: `w-full max-w-xs mx-auto md:max-w-none aspect-[3/4] object-cover rounded-card`. Reads as a visual mirror for the fit-decision beat — "this section is for people like her."
- **Criteria row:** two columns at `md:grid-cols-2` with `gap-12 md:gap-16`; stack on mobile (fit column above not-fit). No divider between columns — just the gap.

**Locked copy (step 5.1 refinement — criterion lines replace run-together sentences):**

> **A good fit**
> - You're a market gardener, a few years in
> - You already grow greenhouse indeterminate tomatoes
> - Open to trying new things
>
> **Not designed for you**
> - You don't grow greenhouse tomatoes yet
> - You run an industrial-scale greenhouse
> - You're looking for academic theory, not practice

**Drift note:** original locked copy ran criteria together as sentences ("A good fit if: you're a market gardener, usually a few years in. You already grow greenhouse indeterminate tomatoes..."). Step 5.1 broke the lead-ins out to column headers and made each criterion its own line. "Usually" dropped (quieter, same meaning). The closing italic resolution line was pruned 2026-04-27 (preachy filler; the columns sort the reader on their own). *"At least one tomato season under your belt"* removed 2026-04-29 — redundant with "you already grow greenhouse indeterminate tomatoes" (anyone growing them has a season under their belt by definition).

---

## How to join

- **Reader-type:** Practical, sub 2 (time, cost, rhythm) + admission callout.
- **Subsection intent:** Let the reader decide if the commitment (time, money, cadence) fits their week.
- **Status:** **locked** (prose below). **Visual structure (step 5) locked 2026-04-27.**

**Beats (visual layout) — stats-first, two-card pricing, no prose paragraphs:**

- bg-white ground (alternation with `#who` farm-bg above; cards sit on white).
- **H2:** "Pricing" (no period). Locked 2026-04-27 — earlier "How to join" framed the section as logistics/admission; "Pricing" frames it as money, which is what the section actually delivers (two pricing cards). The admission band + workload anchor moved to Program section, leaving this section pricing-focused.
- **Admission callout band — REMOVED 2026-04-27.** The "Opens June 2026" date was relocated to the `#join` section (Why add your name now) where it earns the priority-queue line. Pricing now jumps directly from H2 to the two cards.
- **Two pricing cards side-by-side** (border-card frame, the conviction beat) — **Standalone first, Special offer second** (default offer is the baseline; the deal sits as a bonus on the right, not the headline):
  - Card 1: eyebrow "Standalone", big numeral "$40 /month", caption "Month to month. Leave anytime." (carries the commitment terms now that the redundant strip is gone), green CTA pill "Join the waiting list →".
  - Card 2 (Free path): eyebrow **"Special offer"**, big numeral "$0 /month", **two-line scannable path list** (each path named once, brand name in bold/dark): "Growing for Market subscribers" / "Orisha users", **time-bound disclosure** (small italic muted): "For 2026 only. We'll see after that.", green CTA pill "Join the waiting list →". (Each brand name appears exactly once.)
- **Cheapest-path footnote, below both cards** (small italic muted, centered, `max-w-2xl mx-auto`): "Subscribing to **Growing for Market** magazine is the cheapest way to join the program. $39/yr." with link to growingformarket.com/pricing/. Lifted out of Card 2 on 2026-04-27 — sits under both cards as a shared footnote, since the GFM path is the cheapest *across the whole pricing comparison*, not a Card-2 internal disclosure.
- Section ID: `id="how-to-join"`.

**Pruned 2026-04-27 (Option B):** the original layout repeated "rolling / monthly / leave anytime" four times across the admission band, stats strip, and Card 2 caption. Now: timing → admission band, workload → single anchor, commitment → Card 2 caption (each fact lands once). The "Short videos are phone-watchable between rows" note moved to The Program section.

**Locked copy:**

> About 2 to 3 hours a week. Most of it is work on your own plants that you were going to do anyway. Short videos are phone-watchable between rows.
>
> Free if you already subscribe to Growing for Market or use Orisha. Otherwise, the cheapest way in is a GFM subscription: $39 a year, magazine plus program.
>
> Standalone is $40 a month.
>
> The program runs in monthly cycles. Join any month, leave any month. No cohort lock, no contract.

**Drift note:** the outline pricing card previously had a "Most farmers join this way" flag on the free tier. Locked copy drops that (nobody has joined yet) and uses "cheapest way in" framing instead.

---

## FAQ — **DROPPED 2026-04-27**

- **Status: dropped** after rendering. Each of the 5 candidate Q&As turned out redundant with content already on the page (How to join's stat strip + pricing cards, Who this is for's fit gate, Why information isn't enough, Why add your name now's eyebrow blocks). A separate FAQ section repeated material the reader has already seen, so it was removed.
- Locked Q&A copy below kept as reference; do not re-introduce as a section without first identifying questions that aren't answered elsewhere.
- **Reader-type:** residual objections, reads across Practical + Committer.

**Beats:**

- Trimmed from 7 candidate topics to 5 essential. Two dropped as redundant with content already on the page: "what happens right after signup" (covered in Why add your name now's *You'll get program updates* eyebrow block) and "can I leave anytime" (covered in How to join's *Monthly cycles* stat + Standalone pricing card's *Month to month. Leave anytime.*).

**Locked copy — 5 Q&A pairs in order:**

1. **How much time does the program take per week?**
    > About 2 to 3 hours: a 5-minute video, a 60-minute live call (recorded if you miss it), and the rest happens inside the work you'd be doing on your plants anyway.
2. **Do I have to be growing greenhouse tomatoes already?**
    > Yes. The program is built for current greenhouse tomato growers. Cucumber and lettuce paths may come later, but tomatoes are the focus this year.
3. **Can I join mid-program?**
    > Yes. Each month is its own goal, so you can start any month without catching up.
4. **Is the program in English only?**
    > Yes, English only for now. We may translate later as the program grows.
5. **What's the difference between the Orisha course, Andrew's book, and the 40hr Farmer program?**
    > The course and the book are content. The program is a place: live coaching on the calls you're making in your own greenhouse this week.

**Visual structure (step 5):**

- Section ID `id="faq"`. Slots between `#how-to-join` and `#team` (residual objections cleanup before the Committer arc).
- bg-farm-bg ground (alternates from `#how-to-join` white; restores rhythm before `#team` white).
- Standard section padding `py-16 md:py-24`.
- **H2:** "Common questions" (no period). Quieter than "FAQ" jargon, simpler than "Frequently asked questions". Sits in `max-w-3xl` wrapper.
- **Accordion:** 5 items in the `max-w-3xl` prose column, same `<details>` pattern as `#program` but without step numbers. Each summary: question as Fraunces title + rotating caret on right. Expanded body: answer in body prose styling.

---

## Team behind this

- **Reader-type:** Committer, sub 1 (who's behind this).
- **Subsection intent:** Let the reader decide if these are the right people to learn from.
- **Status:** **locked** 2026-04-23. **Visual structure (step 5) locked 2026-04-27 — variant C (per-bio expand).**
    - **Andrew Mefferd** — locked (prose below).
    - **Guillaume** — locked 2026-04-22 (prose below).
    - **Antoine** — locked 2026-04-22 (prose below).
    - **Framing + closer** — locked 2026-04-23 (prose below).

**Beats (visual layout) — variant C, photo-led with per-bio expand:**

- bg-white ground. Section ID `id="team"`. Slots after `#how-to-join` (between Practical and the future Committer sub 2 "Why add your name now").
- **Eyebrow:** "Team behind this" (uppercase Rubik accent, farm-mid). Demoted from H2 2026-04-29.
- **H2:** *"Different paths in,"* / *"Different angles"* (Fraunces upright, two lines forced via `<br>`, locked H2 scale). Promoted from italic-subtitle slot 2026-04-29; the previous lead sentence *"Three people show up on the calls."* was dropped at the same time as redundant with the section's three visible bios. Trimmed *"on the same work"* tail same evening — the parallel anaphora *"Different... Different..."* lands punchier without the modifying clause.
- **Collaboration banner (added 2026-04-29 late evening):** sits between the H2 and the bios. Small uppercase eyebrow *"A program by"* (Rubik accent, farm-mid, centered) above two logos centered side by side. Orisha logo (`assets/logos/logo.png`, h-10 md:h-12 — text + icon, wider format) on the left; Growing for Market badge (`assets/logos/gfm-logo.png`, h-14 md:h-16 — circular, sized slightly larger to balance Orisha's wider format) on the right. Visualizes the partnership the page surfaces verbally elsewhere (Orisha-team tagline *"Behind the program, alongside Growing for Market."*, the GFM-as-cheapest-on-ramp pricing card disclosure).
- **3 bios stacked** with generous space between. Each bio block: 12-col grid, photo `md:col-span-4`, text `md:col-span-8`. Photo `aspect-square object-cover rounded-card`, max-w-[280px]. Stacks on mobile.
- Each bio: Photo · Fraunces name (h3) · Rubik tagline (1-line) · first paragraph (always visible) · `<details>` **one-way expand** ("Read more" → revealed forever, no "Read less") carrying the middle paragraphs **and** the italic *"On calls, he…"* closer as its final beat.
  - **One-way expand pattern (locked 2026-04-28):** once opened, the `<summary>` hides via `#team details[open] > summary { display: none; }` in the page `<style>` block. No mid-content collapse toggle, no JS. To re-collapse, reload. Reason: native `<details>` always anchors the toggle at the top of the expanded region, which placed "Read less" awkwardly between visible and revealed content. Atlantic / Substack pattern. Trade-off: keyboard users can't collapse without reload, judged acceptable for a 3-bio landing-page section.
  - **Closer moved inside the expand 2026-04-27** — previously always visible after `</details>`. Reason: the closer is a payoff line, more powerful as the punch at the bottom of the expanded read than as a competing always-on signal next to the "Read more" affordance.
  - **Andrew:** photo `assets/team/Andrew/IMG_0968.JPG`. Tagline: "Author. Growing for Market editor."
  - **Guillaume:** photo `assets/clients/ferme-decembre/IMG_3865.jpg`. Tagline: "Founder, Orisha. Co-grower, Ferme Décembre."
  - **Antoine:** photo `assets/clients/jardin-inverness/Antoine.jpeg`. Tagline: "Grower, Jardin Inverness."
- **Antoine asymmetry:** the *"One more year like this, and I'll sell the farm."* italic pull-quote sits in his para 2 — it's the load-bearing emotional beat. So Antoine's always-visible content includes paragraphs 1 AND 2; expand reveals paras 3–4. Andrew and Guillaume show only para 1 by default (Antoine's variance is intentional).
- **Orisha team block (4th bio-equal slot, promoted 2026-04-29 late evening):** sits inside the `space-y-16 md:space-y-20` bios container as a fourth entry with full structural parity to the three individual bios. 12-col grid, photo `md:col-span-4` (max-w-[280px], aspect-square cropped from the 1800×1200 source), text `md:col-span-8` with h3 *"The Orisha team"* + Rubik tagline *"Behind the program, alongside Growing for Market."* (refined 2026-04-29 late evening from *"The company behind the program."* — surfaces the GFM partnership) + body paragraph (refined 2026-04-29 late evening to articulate three responsibilities): *"The rest of the team at Orisha produces the videos and handles platform logistics, so we can focus on farm stuff. They build the virtual consultant that supports the program. And they learn from the program to build tools that make greenhouse production easier."* Earlier 2026-04-29 lock was the leaner *"The rest of the team at Orisha handles logistics and builds tools, so we can focus on farm stuff."* Earlier states (same day): line was a small italic muted closer in `max-w-3xl` (5/7 grid, aspect-[3/2] photo); before that, the closer was *"Louis-Bernard keeps the community forum going between calls. The rest of us at Orisha turn what we learn into tools that make the work easier."* (LB-named version). LB now drops off the page entirely. No CTA in this section — Committer sub 2 carries the final form.

**Beats (visual layout):**

- One-line framing above the three bios.
- Three story-like bios of the people on calls (Andrew, Guillaume, Antoine). Each bio names what the person brings into the room.
- Two-line closer after the bios, covering Louis-Bernard (community forum host, not on calls) and Orisha (company behind the program).

**Locked framing (above the three bios):**

> Three people show up on the calls. Different paths in, different angles on the same work.

**Locked copy, Andrew Mefferd:**

> Andrew Mefferd ran a market garden before anything else. He went to work for Johnny's Selected Seeds and learned greenhouse techniques from the industrial growers who've built the craft over decades. He was still running his own farm at the time, tending tomatoes at 5am before heading in to Johnny's. The first year he applied what he was learning, his yields doubled.
>
> He wrote *The Greenhouse and Hoophouse Grower's Handbook* to carry those techniques back to the market-garden community. Later he took over Growing for Market and set commercial farming aside. He's spent the years since editing articles and running the GFM Podcast, which has kept him in close conversation with the best of the small-grower world.
>
> On calls, he brings the combined view: his own hands, plus the hundreds of farms he's edited and interviewed. When you describe something in your greenhouse, he's usually seen it before somewhere else.

**Locked copy, Guillaume:**

> Guillaume started Orisha with no background in agriculture. He spent the years since in conversation with hundreds of farmers, along with greenhouse consultants and university professors. Trying to understand how greenhouses can best serve on a small farm, so Orisha could be useful to small growers.
>
> One challenge kept coming back. There's never enough time to get everything done. He made that Orisha's focus. From the failures and success stories he kept hearing, he built a 40hr farm playbook.
>
> To test it out, he started Ferme Décembre with his partner last year. The target this year is $500k in revenue with 4 employees. Many things yet to figure out, but it seems to be working out so far.
>
> On calls, he can help you spot what's holding your plants back, and where your week is leaking time.

**Drift note:** Guillaume's closer is a single sentence by choice; Andrew's is two (combined-view + "when you X, he Y" promise). Asymmetry is intentional — Mefferd-voice quieter on the Guillaume bio.

**Locked copy, Antoine:**

> Antoine started a farm from scratch and sold it to take over a 2-acre farm he loved.
>
> A few years in, between the financial and HR pressure, he told himself: *"One more year like this, and I'll sell the farm."*
>
> Instead, he went hard on lean farming. He started the next season with half the staff. The farm finished the year with 15% more sales. Learning from Quebec greenhouse consultants, he pushed his tomato yields to 4x the small-grower average on the same square footage.
>
> He now works with Orisha to share what he learned, while his employees run the farm.
>
> On calls, he'll show you which lean moves held up when his farm was breaking, and which greenhouse techniques pushed his tomatoes to 4x.

**Consistency note:** Analytical Sub 2's locked copy names Antoine directly. Current 2026-04-27 form: *"Quebec consultants have adapted big greenhouse techniques to small farms. Antoine and other growers learned from them to regularly hit 4× the average yield in their 30x100 greenhouse."* The "Antoine" word links to `#antoine` (his bio later in the page). The first sentence threads the section: techniques (Andrew's row, big-greenhouse origin) → adapted by consultants → applied by small growers (Antoine).

**Locked closer (below the three bios):**

> The rest of the team at Orisha produces the videos and handles platform logistics, so we can focus on farm stuff. They build the virtual consultant that supports the program. And they learn from the program to build tools that make greenhouse production easier.

---

## Why add your name now (Committer sub 2)

- **Reader-type:** Committer, sub 2 (why now + what happens when you sign up + form).
- **Subsection intent:** Let the reader decide if they're ready to start now, and carry them into the form.
- **Status:** decomposition locked 2026-04-23 (4 beats below); prose draft pending.

**4-beat structure:**

| Beat | What it does |
|---|---|
| 1. Why today | Priority-queue honesty: rolling admission + real live-call capacity = a genuine reason to add your name today, not hype. **Fit-decision beat lives here.** |
| 2. What happens when you sign up | Mechanical reassurance: what clicking the button means (waitlist), what lands in the reader's inbox, when the program opens. Low-stakes, reversible. |
| 3. The form | Minimal fields (first name, farm name, email, subscription status), submit button carries the page's accumulated weight. |
| ~~4. Disclosures next to form~~ | **DROPPED 2026-04-27.** Disclosures (mid-program join, leave anytime, language, privacy) were judged either redundant with How to join's pricing cards / cadence stat or non-essential at this beat. Form stands alone after Beat 3. |

Ordering: 1 → 2 → 3. Reassurance before the form. No disclosures.

**Guardrails:**

- Honest capacity framing, no fake scarcity.
- Consistent with rolling admission: priority is about *when* you get in, not *whether*.
- Any urgency beyond the honest math breaks the brand.
- Any potential starting limit is a one-time launch posture ("starting smaller so we can learn how to serve everyone well"), not an ongoing monthly cap.

**Visual structure (step 5) locked 2026-04-27 — variant B (two-column desktop, prose + form).** Lean refinement 2026-04-27: left column converted from 3 prose paragraphs to 3 eyebrow-led blocks; H2 changed from "Why add your name now" to "Join us" (more welcoming).

- Section ID `id="join"`. **Ground: farm photo with deep farm-dark tint** (orisha.io bottom-CTA pattern), set via inline `linear-gradient(rgba(39,80,10,0.88), rgba(39,80,10,0.88)), url('assets/clients/ferme-decembre/6073DAB7-095E-4744-8045-67F8166BA650.jpg')`. The hero photo reused as a visual bookend (page opens with this photo, closes with same photo darkened). Photo updated 2026-04-29 late evening when the hero swapped from `drive-0416.jpg` to the current portrait — bookend pattern preserved by tracking the change. All text on dark switches to white (H2, prose); muted disclaimer becomes `text-white/70`. Form panel stays `bg-white` — pops as a contrast island against the dark background. Locked 2026-04-27 (replaces earlier bg-farm-bg ground).
- **Eyebrow + 2-line H2 (relocked 2026-04-29 late evening):** small uppercase eyebrow *"Join us"* (`font-accent text-white/80 font-semibold uppercase tracking-wider text-xs`) above a 2-line H2 *"Farming is beautiful. / Let's make sure it stays that way"* (no terminal period per editorial-titles rule; internal period after "beautiful" preserved as the line break, forced via `<br>`). The H2 is a deliberate reprise/envelope of the hero epigraph *"Farming is beautiful, but life's richer with energy left for the people in it."* — the page opens and closes on the same phrase. *"Let's"* (contracted, brand-voice rule) — the uncontracted *"Let us"* tested briefly 2026-04-29 evening for hymn-like register, reverted same day in favor of brand-voice consistency. Wording journey: *"Why add your name now"* (transactional, replaced 2026-04-27) → *"Join us"* (welcoming but generic, replaced 2026-04-28) → *"Join growers working toward a 40-hour farm"* (locked 2026-04-28, replaced 2026-04-29 morning) → *"A community of growers working toward a 40-hour farm"* (subtitle form, replaced 2026-04-29 evening) → H2-with-subtitle reprise (replaced 2026-04-29 late evening) → current eyebrow + 2-line H2 (the reprise becomes the heading itself; eyebrow names the section, H2 carries the bookend).
- **Stacked single-column layout (relocked 2026-04-27):** prose lead-in above, centered form below. The earlier two-column grid (prose left / form right) was retired — eyebrow-led blocks compressed into a single short paragraph that does the same persuasive work without the visual weight of two columns. Form floats centered with `max-w-md mx-auto`.
- **Prose lead-in:** centered reading column (`max-w-3xl mx-auto mt-10 md:mt-14`), single paragraph at canonical body scale (`text-lg md:text-xl text-farm-text leading-relaxed`). Replaces the two eyebrow-led blocks.
- **Form panel:** white panel `bg-white rounded-card p-8 md:p-10 border border-farm-mid/15` inside `max-w-md mx-auto mt-12 md:mt-16`, containing:
  - Lead-in (italic, top of panel): *"Three fields and a quick question."*
  - First name (text input)
  - Farm name (text input)
  - Email (email input)
  - Subscription status (radio group, label "Are you already a..."): *Orisha user* / *Growing for Market subscriber* / *None of the above*
  - Submit button: green pill *"Join the waiting list →"*, full width inside panel.
- HubSpot post handler **pending** — render with `action=""` placeholder and a comment marker for the funnel work.

**Locked copy (re-locked 2026-04-27, single prose paragraph):**

> The program opens June 2026.
>
> *(quiet muted warning, smaller scale below the lead)*
> *If we have to limit seats: First on the list, first in.*

**Drift note (2026-04-27, "Opens June 2026" relocation):** the date moved here from the Pricing section's admission callout band. Pricing carried it timelessly; this section is the one whose intent ("Why today beats later") is structurally load-bearing on the date — without it, "first in line" is toothless. Folded into the priority-queue line as one sentence rather than its own callout, to keep the quiet-journal register.

**Drift note (2026-04-27 lean):** went through three lock revisions in one day. Initial: three paragraphs ("We're still figuring out the format..." + "Putting your name down today costs nothing..." + "Your name goes on the waiting list..."). First prune: three eyebrow-led prefixes (Tell us / Save your seat / Get Program updates). Second prune (same day): "Get Program updates / over email" deleted. Final lock (same day): collapsed the remaining two eyebrow blocks + retired the two-column grid for a single prose paragraph above a centered form. Each prune lost the same idea (what-happens-after-signup is implicit; the eyebrow scaffolding added visual weight without adding meaning). The "first on the list, first in" framing replaces "first in, first seat" — softer, more conditional, removes the implicit cohort scarcity.

**Locked copy, Beat 3 (The form) — locked 2026-04-27:**

- Lead-in: ~~"Three fields and a quick question."~~ **Removed 2026-04-27** — form opens directly with the first field, no preamble.
- Form fields:
    - First name (text)
    - Farm name (text)
    - Email (email)
    - Subscription status (single-select, 3 options): *Orisha user* / *Growing for Market subscriber* / *None of the above*
        - Field label candidate: *"Are you already…"* or *"Where you stand"* — exact wording in step 5.
- Submit button label: *"Join the waiting list"*
- Posts to HubSpot.

**Why the 4th field:** segments the welcome sequence and tracks how many incoming signups already qualify for the free path. Surfaces the subscription dimension to the reader at signup, which lightly nudges *"oh, GFM gets me free access"* awareness without re-pitching it on the page.

**Note (HubSpot integration):** existing form captures first name + last name + email. New form needs:
1. Drop *Last name* field.
2. Add *Farm name* (text) — likely a new custom contact property.
3. Add *Subscription status* (enumeration / single-select with values: Orisha user, GFM subscriber, None) — new custom contact property, used as the segmentation key for the welcome sequence.

Out-of-scope for the landing page render; flag for the funnel work before signup launches.

---

## Final CTA (absorbed into Committer sub 2 above)

- **Reader-type:** Committer, sub 2 terminal beat (the form itself) — now part of the Why-add-your-name-now block per the 4-beat decomposition (Beat 3).
- **Status:** old live heading ("Farming is beautiful. Let's make sure it stays that way.") retained as a candidate reprise line for the page's final visual block if needed in step 5; not yet re-drafted under the reader-type-first method.
- Waitlist form: first name, last name, email. Submit button label: "Join the waiting list." Posts to HubSpot.
- Background: farmer-at-sunset photo with dark green overlay.
