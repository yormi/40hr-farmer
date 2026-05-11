# UTM links for the 40hr Farmer waitlist

Operational reference. Any link to the landing page from a controlled surface (newsletter, social, partner placement) should use one of these tagged URLs. Untagged links collapse into "Direct" in GA4 and become invisible to attribution.

## Scheme

| Bucket | utm_source | utm_medium | utm_campaign |
|---|---|---|---|
| GFM (Andrew) | `gfm` | `referral` | `40-hr-farmer-waitlist-2026` |
| Orisha Instagram | `orisha-instagram` | `social` | `40-hr-farmer-waitlist-2026` |
| Orisha email sends | `orisha-email` | `email` | `40-hr-farmer-waitlist-2026` |

## Canonical tagged URLs

Base URL: `https://the40hourfarmer.orisha.io/` (custom domain; `https://yormi.github.io/40hr-farmer/` also redirects here while preserving query params, but link to the custom domain directly to skip the redirect).

- **GFM:**
  `https://the40hourfarmer.orisha.io/?utm_source=gfm&utm_medium=referral&utm_campaign=40-hr-farmer-waitlist-2026`
- **Instagram:**
  `https://the40hourfarmer.orisha.io/?utm_source=orisha-instagram&utm_medium=social&utm_campaign=40-hr-farmer-waitlist-2026`
- **Email sends:**
  `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=40-hr-farmer-waitlist-2026`

## How to read results

**GA4** (acquisition view, by traffic source):
- Reports → Acquisition → Traffic acquisition
- Filter by `session_source` or `session_medium`
- The custom `waitlist_signup` event also carries `utm_source`, `utm_medium`, `utm_campaign` as event params (Reports → Engagement → Events → `waitlist_signup`).

**HubSpot** (per-contact attribution):
- Contacts → All contacts
- Filter by `UTM source` (or medium / campaign) property
- Build a saved view per bucket if needed.

## When to add a new source

1. Add a new row to the scheme table above.
2. Append the canonical tagged URL to the list.
3. Use the tagged URL anywhere you publish a link to the landing page.

Pick source slugs that are short, lowercase, hyphenated, and unmistakable about the surface. Reuse `utm_campaign` for everything pointing at this waitlist round (so all 40hr Farmer signups roll up under one campaign in GA4 and HubSpot).

## Attribution model

Last-touch within 30 days. The landing page stores the most recent `utm_*` triple in `localStorage` (key `orisha_utm`) and replays it on form submit. A visit with no UTM params does not overwrite a stored attribution; a visit with any UTM param replaces the prior one and resets the 30-day clock. After 30 days of inactivity, attribution clears.

## Field plumbing

- HubSpot custom contact properties: `utm_source`, `utm_medium`, `utm_campaign` (single-line text, group `contactinformation`).
- HubSpot form `7f28cb26-8aea-432e-bf7f-c50a1484d0a3`: 3 hidden fields, one per property.
- Landing page: capture script near the GA4 init in `index.html`; form-submit handler populates the 3 hidden fields and the `waitlist_signup` GA4 event.
