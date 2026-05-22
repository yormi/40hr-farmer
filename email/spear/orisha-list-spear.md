# Orisha list, 40hr Farmer program announcement (SPEAR)

**Audience:** existing Orisha email list (warm, not cold).
**Framework:** Dan Martell's SPEAR.
**Send plan:** [`spear-wave-plan.md`](spear-wave-plan.md) (3-wave structure: canary → engaged remainder → cold).

---

## Wave 0 — sent 2026-05-12

**Subject lines (3-way, 50/cell):**

| Variant | Subject | Angle |
|---|---|---|
| A | A path to your dream farm? | Emotional / aspirational |
| B | Cutting farm hours without cutting income | Analytical / promise |
| C | Farming with energy left at the end of the day? | Felt / lifestyle |

**Body (identical across A/B/C), opener as recalled by Guillaume:**

> Farming is great. But the hours leave little energy for the people in your life?

(Remainder of the sent body, program announcement and CTA, to be confirmed against the HubSpot send record if needed.)

**Results (24h window):**

| Variant | Open | Click |
|---|---|---|
| A | 34% | 0% |
| B | 38% | 6% |
| C | 34% | 6% |

**Read:** Subject B leads on opens. B and C tie on click. Body underperformed (0 to 6% CTR). Subject was off-axis from the body (subjects promised hours/income/energy, body opened on energy-for-people only). Conclusion: lock subject B for Wave 1; ship a new body that aligns with the subject's promise.

---

## Wave 1 — locked 2026-05-14

**Subject A:** Cutting farm hours without cutting income

**Body A (Mechanism / How, locked 2026-05-14):**

> Hey {{firstName | default: "there"}},
>
> Are you looking to do more with less, but aren't sure how ?
>
> We're launching a program to guide farmers to do that. Starting with the most underappreciated opportunity on the farm.
>
> Worth a look? [Check how it works!](https://the40hourfarmer.orisha.io/#leverage)
>
> Guillaume

**Subject B:** Making the farm pay for the life you want

**Body B (Flip / Drew & Allison, locked 2026-05-14):**

> Hey {{firstName | default: "there"}},
>
> A balanced life for a farmer? Possible? Some make it.
>
> Drew & Allison at Ghost House Farm made the farm pay to replace Allison's off-farm paycheck.
>
> [Check how they did it and what the techniques they used can do for you!](https://the40hourfarmer.orisha.io/#story)
>
> Guillaume
>

**CTA:** the bracketed sentence in each body is the link, with SPEAR UTM params per [`spear-wave-plan.md`](spear-wave-plan.md). Anchor + `utm_content` differ per body:

- Body A: `https://the40hourfarmer.orisha.io/#leverage`, `utm_content=wave1-howto`
- Body B: `https://the40hourfarmer.orisha.io/#story`, `utm_content=wave1-flip`

**Sending platform:** TBD (Loops → Sequenzy → Resend all dropped; evaluating Postmark as of 2026-05-22; see `spear-wave-plan.md`). Wave 1 send is paused until an ESP is locked. Contact list still built in HubSpot (engaged remainder minus Wave 0 recipients); 852-contact audience splits 50/50 between Body A and Body B.

### Retired (locked 2026-05-13, replaced 2026-05-14)

Replaced 2026-05-14 by the two bodies above, alongside a subject change ("Cutting farm hours without cutting income" → "Making the farm pay for the life you want"). Never sent.

**Body (Yield, retired):**

> Hey FIRST_NAME,
>
> One way to do more with less is to increase yield per bed.
>
> Our beds pull twice the harvest, and we stop needing more hours to make the math work.
>
> [Check the 4 ways increasing our bed yields transform our farms to protect our energy for what else matters.]
>
> Cheers,
> Guillaume
>
> PS: Andrew Mefferd, Antoine and I are launching a program to help other diversified farmers leverage their yield to pay for the life we're after. Worth a look, check the link above :)

---

## Earlier exploration (not sent)

Drafts considered before Wave 0. Retained for reference, not shipped.

### Workload (pragmatic, short)

Hey FIRST_NAME,

Need to cut your farm workload?

We're launching a program with Andrew Mefferd at Growing for Market to work with farmers toward profitable 40hr farms.

Worth a look? [Learn about it here](orisha-email utm link).

Cheers,

### Calling (felt, longer)

Hey FIRST_NAME,

Farming is your calling but the hours keep you from the life you envisioned when you started? Your dream farm needs to leave energy in the tank to appreciate time with the people in your life?

We're launching a program with Andrew Mefferd at Growing for Market to work with farmers toward profitable 40hr farms.

Worth a look? [Learn about it here](orisha-email utm link).

Cheers,

---

**Personalization token:** HubSpot first-name token with `there` fallback when first name is missing.
