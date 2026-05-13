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

## Wave 1 — locked 2026-05-13

**Subject:** Cutting farm hours without cutting income (Wave 0 Variant B)

**Body (Yield, locked):**

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

**CTA:** the bracketed sentence is the link. Target: `https://the40hourfarmer.orisha.io/#leverage` (+ SPEAR UTM params per [`spear-wave-plan.md`](spear-wave-plan.md)).

**Sending platform:** Loops.so. Contact list built dynamically in HubSpot (engaged remainder minus Wave 0 recipients), exported to Loops.

**A/B partner body:** pending. If a second body is locked, it goes here as "Body (X, locked)" and Wave 1 splits 50/50 between the two.

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
