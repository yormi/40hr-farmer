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
8. **Render HTML.** In `email/welcome-sequence/NN-name.html`. Style against `brand/docs/brand/visual-design.md`. Verify the no-dashes rule. Verify links and merge tags (`{{contact.firstname}}`, `{{unsubscribe_link}}`).
9. **Approval and ship.** Surface to Guillaume. On approval, install per the welcome sequence delivery plan ([`in-progress/resend-welcome-migration-plan.md`](../in-progress/resend-welcome-migration-plan.md)).

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
| 1 | 0 | Stage | Confirm signup. Frame the sequence as a personal note from Guillaume, not a marketing funnel. Invite the reader to share why they signed up. Set up tomorrow's origin. | "Tomorrow: why I'm building this. It starts with a farm I worked with in 2024." |
| 2 | 1 | Origin | Guillaume's 10-year pattern. The 5-step trap every farmer falls into. The "do more with less" reframe. Greenhouse leverage angle. Andrew Mefferd partnership. Program birth. Cliffhanger into Ferme Décembre. | "One year in, the picture is messier than the plan. Next email: what's actually happening." |
| 3 | 4 | Vision (Ferme Décembre) | Building a 40hr farm at Ferme Décembre alongside the reader. What it means in practice. Where things stand right now. Adjacency, not spectacle. | "Next: why this matters even if you can't sell more tomatoes." |
| 4 | 7 | Orisha origin + Drew + consultant *(combined; may split later)* | Story of starting Orisha. Conversation with Climax. Climate / irrigation rule-of-thumb subtleties → why we built the virtual consultant. Drew's farm in 2024 as proof the approach works (REQ-P3 lands here). Consultant access. | TBD (depends on whether Email 4 splits into two emails or stays combined). |
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

### Email 1 — Stage (Day 0)

**Point** *(Schwartzberg, locked 2026-05-06)*: I believe a real conversation will serve you better than a landing page can.

**Subject:** "you're in, here's what's coming"

**Reader state on arrival:** Just submitted the form. Wondering "did that work?"

**Reader state on departure:** Read the founder's conviction first, logistics last. Knows this is a real person writing. Curious about tomorrow. Already invited into a dialogue.

**Protagonist:** Guillaume, narrator. No second character.

**Scene:** Quiet note. Plain-text feel.

**Beats (final shape):**

1. Greeting.
2. **Conviction up front:** mission framing for the program (slowly reinventing small farming).
3. **Vulnerability about the medium:** hating that a landing page strips too much for the conviction to land.
4. **Promise:** use the next few emails to tell why we started, introduce the program as if face to face.
5. **Tease into Email 2:** how we stumbled into building this program.
6. **Reciprocity / CTA:** ask the reader why they signed up + what they'd like to achieve.
7. Sign-off.
8. **P.S. (logistics):** waiting-list confirmation + release-date posture.

**Locked copy (rendered in `email/welcome-sequence/01-welcome.html`, locked 2026-05-04):**

> Hi {{contact.firstname}},
>
> I believe that, with the 40hr Farmer program, we can slowly reinvent small farming so it works better for everyone who chooses it.
>
> I hate that a landing page can hardly convey that conviction. Trying to be that concise strips out so much that my enthusiasm doesn't come through.
>
> I'd like to take the next few emails to tell you why we started this program and introduce it to you as if we were face to face.
>
> Next email starts with how we stumbled into building this program.
>
> First, though, I'd like to learn about you. Why did you sign up? What would you like to achieve?
>
> Talk soon,
> Guillaume
>
> *P.S. You're on the waiting list. I'll let you know once we have a release date.*

~120 words.

**Anti-requirements verified:**
- ANTI-1 (no fake urgency): pass
- ANTI-2 (no overclaim): "I believe ... we can slowly" qualifies; passes
- ANTI-3 (early-stage as downside): waiting list framed as honest expectation, not as a delay
- ANTI-4 (SaaS filler): pass — leads with mission, not platitude
- ANTI-5 (no stylistic dashes): pass

**Sequence REQs touched:** Implicit start on REQ-P2 (trust where this is going) via the conviction + real-human authorship + relational ask.

### Email 2 — Origin (Day 1)

**Point** *(Schwartzberg, locked 2026-05-06)*: I believe running a small farm profitably can be done on a 40hr week.

**Subject:** "5 steps every farmer falls into"

**Preview text:** "And the playbook the few who escaped used."

**Reader state on arrival:** Read Email 1 yesterday. Maybe replied to "why did you sign up?". Curious about the origin story Guillaume teased.

**Reader state on departure:** Recognizes the 5-step trap as their own story. Sees the "do more with less" reframe. Understands why a Program (mix of content, tools, coaching) exists rather than just a tool. Curious how Ferme Décembre is going.

**Protagonist:** Guillaume. Drew is no longer in this email; Andrew Mefferd enters as the catalyst for the partnership.

**Scene:** Guillaume reflecting on 10 years of patterns across market gardeners.

**Beats (final shape):**

1. **Conviction up front:** running a small farm profitably can be done on a 40hr week.
2. **The 5-step trap:** the recurring story Guillaume hears from farmers.
3. **The reframe:** the few who got out used the same rough playbook — do more with less.
4. **The click:** the greenhouse leverage angle is the greatest "do more with less" opportunity available now.
5. **The leverage:** one greenhouse bed brings what 20 field beds bring; reinvent the farm in a healthier way.
6. **The gap:** consultants help, but most farmers will never have one.
7. **Andrew Mefferd partnership:** the catalyst. Videos + tools + coaching, none alone are enough; a mix might work.
8. **Program birth:** that's how The 40hr Farmer Program was born. Honest "we don't have it figured out, starts with greenhouse tomatoes" frame.
9. **Décembre cliffhanger:** Last year I started a farm to test the ideas. Plan: $700K with 2 employees. Greenhouse at the center. *"One year in, the picture is messier than the plan. Next email: what's actually happening."*

**Locked copy (rendered in `email/welcome-sequence/02-origin.html`, locked 2026-05-06):**

> Hi {{contact.firstname}},
>
> I believe running a small farm profitably can be done on a 40hr week.
>
> There are a lot of challenges and tough calls to make to get there.
>
> I've worked alongside market gardeners for almost 10 years now and keep hearing the same story from every farmer:
>
> 1. Start a farm to build a better future for the planet, the community and ourselves
> 2. Face financial pressure, scale the farm to increase sales
> 3. Expenses hike faster than sales
> 4. Bridge the gap with our own free labor
> 5. The hours crush us
>
> Yet, very few farmers continue the story with how they got out of that trap.
>
> Those who did all used the same rough playbook: hunt every opportunity to do more with less.
>
> Easier said than done, right?
>
> Well, recently, something clicked! What we've been working on for years is probably the greatest opportunity to do more with less.
>
> The gap between the best small-scale greenhouse growers and the average grower is huge. And everything leads me to believe we can bridge that gap.
>
> A greenhouse bed that brings what 20 field beds bring changes the possibilities for small farms. It gives us so much more power to reinvent our farm in a healthier way.
>
> Greenhouse consultants help small growers in Quebec get there. But doing it without their experience is quite an ask.
>
> I was wondering how Orisha could best support farmers to do it, when Andrew Mefferd offered to partner on a video course. Talking it through, we landed somewhere bigger: videos alone aren't enough, better tools alone aren't either, and we don't have the capacity to coach everyone. Maybe a mix would work?
>
> That's how The 40hr Farmer Program was born.
>
> We don't have it all figured out, but it has to start somewhere, and it'll get better as we go! Slowly but surely paving the way to doing more with less. Starting with greenhouse tomatoes.
>
> Last year, I started a farm to test the do-more-with-less ideas I've gathered over the years. The initial plan: $700,000 with 2 employees. The greenhouse is at the center of it.
>
> One year in, the picture is messier than the plan. Next email: what's actually happening.
>
> Guillaume

~380 words. Page-turner length explicitly accepted.

**Anti-requirements verified:**
- ANTI-1 (no fake urgency): pass
- ANTI-2 (no overclaim): "probably the greatest opportunity," "everything leads me to believe" — qualifiers in place; passes
- ANTI-3 (early-stage as downside): "we don't have it all figured out, but it has to start somewhere" frames evolving as honest, not weakness; passes
- ANTI-4 (SaaS filler): pass — 5-step trap is specific to market gardeners, no generic newsletter language
- ANTI-5 (no stylistic dashes): pass

**Sequence REQs touched:**
- **REQ-S1** (June 2026 working target): NOT here. Held for later (Email 6 honest framing).
- **REQ-S2** (still being built): partial — "we don't have it all figured out... gets better as we go."
- **REQ-P2** (trust where this is going): major — Guillaume's 10-year observation + Andrew partnership + honest frame.

**Open question:** Drew is now out of this email and the locked sequence carries no concrete farmer story (REQ-P3) until we decide. Candidate placements: Email 4 (reframe / what if you can't sell more), Email 6 (honest framing / Gordon failure), or a new dedicated email. TBD.

### Email 2.1 — Origin (Day 1) — Alternate: John + Antoine *(draft 2026-05-19, not locked)*

**Status:** Alternate to the locked Email 2. Pending Path A (polish locked) vs Path B (re-lock around this variant). See Open questions below before sending.

**Point** *(working, not yet Schwartzberg-locked)*: I believe a small farm can be turned around by working smarter, not harder.

**Subject (recommended):** "the trap, and one way out"

**Preview text:** "And the farmer who turned it around."

**Reader state on arrival:** Same as locked Email 2 — read Email 1 yesterday, curious about the origin Guillaume teased.

**Reader state on departure:** Sees themselves in John's arc. Recognizes "work smarter, not harder" as the reframe. Knows Antoine as the farmer-proof voice. Curious about Décembre.

**Protagonist:** Guillaume (narrator) + John (composite trap character) + Antoine (named turnaround proof). Mefferd absent in this variant.

**Scene:** Guillaume narrating 10 years of farmer conversations; John's composite arc; Antoine's turnaround at his farm + move to coach at Orisha.

**Beats (draft):**

1. **Origin frame:** 10 years listening, same story repeating.
2. **John's trap:** vision → management drift → financial pressure → doubling hours → exhaustion → powerlessness.
3. **Recognition prompt:** "Familiar?"
4. **The reframe:** the few who escaped used "work smarter, not harder."
5. **Antoine intro:** named proof; depression + near-sell decision; cut workload, +15% sales with half the team in a year; now drives 2h to coach at Orisha.
6. **Mission:** level the playing field by sharing greenhouse leverage technique.
7. **Antoine's numbers:** $10K profit per tomato bed; precision over time.
8. **Program birth (lite):** "That's where we'll start the program."
9. **Soft leverage link:** to `the40hourfarmer.orisha.io/#leverage`.
10. **Encouragement beat:** "we need to be crazy enough to dream…"
11. **Décembre cliffhanger:** $700,000 plan with 2 employees; messier than expected. *"Next email: what to expect in a year."*

**Draft copy (mechanical fixes from 2026-05-19 critique applied; stylistic choices preserved):**

> Hello there,
>
> Me again.
>
> I started Orisha almost 10 years ago with no knowledge of market gardening whatsoever.
>
> To fix that, I took every opportunity I had to talk to farmers. And over the years, the same story came over and over again.
>
> John starts a farm with a vision. To connect with nature, steward the land, support their community.
>
> As he gets the farm off the ground, John takes on more and more responsibilities: building everything the farm needs, hiring help, delivering for customers...
>
> He gets pushed more and more toward management stuff, aka not why he started farming.
>
> Meanwhile the financial pressure builds.
>
> To fix this John doubles the hours to make ends meet: growing more beds, adding products, adding drop-off points, going to more markets, a transformation kitchen maybe?
>
> At a point, he reaches his limits and realizes that even if he's working 12h a day, 7 days a week. And there's no more money coming in.
>
> Exhaustion catches up. Tensions rise on the farm. Everything feels heavy. The fun isn't there anymore. And the worst part: if working more doesn't help, John feels powerless.
>
> Familiar?
>
> Over the years, I met a few farmers who managed to get out of that trap.
>
> And they all came up with a variation of the same solution: "work smarter, not harder".
>
> Antoine, who'll be with us on the program, is one of them.
>
> I met him when I installed Orisha on his farm in our humble beginning. Since then, Antoine went through the exact same pattern as I described. He fell into depression. Told himself that if he went through another season like the one he'd just had, he'd sell the farm.
>
> And that's when he turned around his farm. He aggressively cut in the workload and ended up increasing his sales 15% with half the team size. All that within a year.
>
> Now, he's freed himself so much that he decided to drive 2 hours a day, 3 days a week to work with us at Orisha to help others build farms that work for them.
>
> If we want small-scale farming to thrive, we need to find techniques to make it easier to run profitable farms. To do more with less.
>
> That's what the program is about.
>
> We see so many ways to support small farms but realistically, to have a real impact, we have to tackle them one at a time.
>
> And the first way we'll do that is to level the playing field. Antoine had the unfair advantage of being coached to grow in greenhouses. He makes $10,000 PROFIT on a single tomato bed after paying for time, propane and input. Those results require precision but not more time. In fact, probably less time, since being proactive saves a lot of problems.
>
> That's where we'll start the program.
>
> And if you think growing more won't help you reduce the hours on the farm, [here's how to use higher yields to work your way toward a 40hr farm](https://the40hourfarmer.orisha.io/#leverage).
>
> I hope this makes you excited about your dream farm. We need to be crazy enough to dream to gather the courage to make changes on top of the already infinite todo list.
>
> All these do-more-with-less ideas made me cocky enough to start a farm last year. The plan was $700,000 sales with 2 employees. It convinced the bank. One year in, though, and... well, it's messier than expected. Next email: what to expect in a year.
>
> Take care,
>
> Guillaume

~520 words. Longer than the locked Email 2 (~380) — driven by the John narrative and Antoine's intro.

**Mechanical fixes applied (from 2026-05-19 critique):**

| Original | Corrected |
|---|---|
| "knowledge on market gardening" | "of market gardening" |
| "takes more and more responsibilities" | "takes on more and more responsibilities" |
| "the farm need" | "the farm needs" |
| "for Customers" | "for customers" |
| "he reach his limits and realize" | "he reaches his limits and realizes" |
| "there's not more money" | "there's no more money" |
| "Familiar ?" | "Familiar?" |
| "same solution :" | "same solution:" |
| "2hours a day" | "2 hours a day" |
| "if it'd go through another season like he'd just had" | "if he went through another season like the one he'd just had" |
| "he had free himself" | "he's freed himself" |
| "to strive" | "to thrive" |
| "That kind of results require" | "Those results require" |
| "won't lower help you reduce" | "won't help you reduce" |
| "$700k" | "$700,000" |

**Stylistic choices preserved (flagged but not auto-fixed):**

- "Hello there, / Me again." opener loses the `{{contact.firstname}}` continuity from Email 1.
- "$10,000 PROFIT" all-caps emphasis runs against the quiet-voice norm.

**Open questions / decisions needed before this variant can ship:**

1. **Path A vs Path B.** Re-locking around this variant means redoing the Schwartzberg arc across Emails 1-2-3, finding a new home (or cut) for the Mefferd partnership beat, and dropping the load-bearing "1 greenhouse bed = 20 field beds" image from Email 2's body.
2. **Antoine consent.** Public-naming-consent list per memory currently covers Drew, Gordon, Ten Mothers Farm. Antoine needs explicit sign-off for: (a) named appearance in welcome-sequence broadcast, (b) the depression reference, (c) the 15% / half team / $10K-per-bed numbers.
3. **Number verification.** Per "never extrapolate farmer's story," the three quantitative claims about Antoine need to be his words, not inferred.
4. **Schwartzberg lock.** Working Point above is not yet locked. If Path B chosen, lock formally and re-check Email 1 and Email 3 Points for chain coherence.
5. **Mefferd beat fate.** Currently absent. Decide: re-introduce later, or remove from program narrative entirely.
6. **Voice flags.** Two lines drift preachy — "I hope this makes you excited about your dream farm. We need to be crazy enough to dream…" and "If we want small-scale farming to thrive…". Tighten before send.
7. **Cliffhanger phrasing.** "what to expect in a year" (forecast) vs locked "what's actually happening" (present-tense Décembre scene). Email 3's deliverable depends on this choice.

### Email 3 — Vision / Ferme Décembre (Day 4)

**Point** *(Schwartzberg, locked 2026-05-06)*: I believe greenhouse leverage gives market gardeners many ways to reinvent their farm.

The Décembre story is the lived demonstration of this Point. Guillaume's farm is built around the greenhouse as the central leverage; the email shows what the leverage looks like in practice (and where the plan met messy reality).

Prose not yet drafted.

### Email 4 — Orisha origin + Drew + virtual consultant (Day 7)

Combined beat absorbing what was previously Email 4 (Drew's reframe) and Email 5 (consultant intro). May split into two emails later.

**Direction (per Guillaume, 2026-05-06):** "Story of when I started Orisha. Talking to Climax. Bunch of subtleties and rule of thumb to reconcile → Consultant access."

**Sketch of beats:**

1. Story of starting Orisha. Why a tool company, what gap I was trying to close.
2. **Climax** — early conversation / collaborator (need Guillaume to fill in: who, when, what was said).
3. The technical reality: greenhouse climate + irrigation have rules of thumb, but applying them all simultaneously is hard. Most farmers can't.
4. That's what Orisha automated.
5. Drew's farm in 2024: the proof. Yield doubled, Allison rejoined the farm full-time. (REQ-P3 lands here — concrete farmer story with real names + scenes.)
6. But Orisha-the-tool wasn't enough on its own — too many subtleties beyond climate that farmers still had to navigate.
7. So we built the virtual consultant: a way to put years of accumulated subtleties into a place farmers can ask. It's free, here's your access.

**Open questions before drafting:**
- Who is Climax? (name, context, what conversation Guillaume is referring to)
- Should Drew get a few sentences or a full paragraph?
- Length target — if combined Email 4 runs >500 words, split into 4a (Orisha origin + Drew) and 4b (consultant access).
- New cliffhanger into Email 5 (honest framing) — TBD.

**Status:** beats outlined, prose not yet drafted. Decide split-or-stay after first draft hits ~word count.

### Email 5 — How you can engage now (Day 10)

Not yet locked.

### Email 6 — Honest framing (Day 14)

Not yet locked.

### Email 7 — Invitation (Day 18)

Not yet locked.
