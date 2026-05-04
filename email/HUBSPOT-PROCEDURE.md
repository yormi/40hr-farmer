# HubSpot Email, Form & Workflow Setup via API

How we got the welcome email sequence, the waitlist form, and the enrollment workflow into HubSpot. Browser automation didn't work (the email editor renders in an iframe that blocks drag-and-drop). The API works, but has quirks. The general pattern: **create an empty shell, then PATCH content into it.**

**Critical caveat (verified 2026-05-04):** This procedure produces emails of type `BATCH_EMAIL`, which **cannot be used in workflows**. Workflows require `AUTOMATED_EMAIL`, and HubSpot silently forces all API-created emails to `BATCH_EMAIL` unless the private app has the `marketing-email` granular scope. That scope is plan-tier-gated and often unavailable (Guillaume's portal blocks it). Setting `type: "AUTOMATED_EMAIL"` on POST is silently ignored; PATCH to convert is rejected with `Cannot perform subcategory updates for this email type`.

- **For workflow emails (the welcome sequence):** create the shell in the HubSpot UI as **Automated** (Marketing → Email → Create email → choose "Automated"). Set name, subject, preview text, from/reply-to, and paste body HTML in the rich-text module. Click **Save for automation**. The body of this procedure can still be used to PATCH content into UI-created automated emails by ID.
- **For one-off marketing blasts (not in a workflow):** the API-only procedure below works fine.

## Prerequisites

- HubSpot Private App API key with scopes: `content`, `automation`, `forms`, `crm.schemas.contacts.read`, `crm.schemas.contacts.write`, `crm.objects.contacts.read`, `crm.objects.contacts.write` (last one is needed to delete smoke-test contacts).
- Portal ID: `5156324`
- API base: `https://api.hubapi.com`
- Auth header: `Authorization: Bearer <API_KEY>`

## Step 1: Create empty email shells

Create each email with **no widget content**. Let HubSpot initialize the drag-and-drop template structure itself. This is critical — if you try to specify widgets during creation, the editor crashes or content doesn't render.

```bash
curl -X POST "https://api.hubapi.com/marketing/v3/emails" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "40hr Farmer - 01 Welcome",
    "subject": "You'\''re in — here'\''s what'\''s coming",
    "from": {
      "fromName": "Guillaume Lambert",
      "replyTo": "guillaume@orisha.io"
    },
    "language": "en"
  }'
```

The response gives you the email ID and — importantly — the widget structure HubSpot created. Save the ID.

**Do NOT set** `subcategory: "automated_email"` — it throws "Creating an email with invalid subcategory is not allowed".

## Step 2: PATCH each email with content

The template HubSpot creates uses the `@hubspot/email/dnd/Plain_email.html` layout. The main content widget is named `module-0-0-0` (not `primary_rich_text_module` as older docs suggest).

```bash
curl -X PATCH "https://api.hubapi.com/marketing/v3/emails/<EMAIL_ID>" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "widgets": {
        "module-0-0-0": {
          "body": {
            "html": "<p>Hi {{contact.firstname | default(\"there\")}},</p><p>Your email body here...</p><p>Guillaume</p>",
            "css_class": "dnd-module",
            "hs_enable_module_padding": true,
            "module_id": 1155639,
            "path": "@hubspot/rich_text",
            "schema_version": 2
          },
          "id": "module-0-0-0",
          "module_id": 1155639,
          "name": "module-0-0-0",
          "type": "module",
          "order": 2
        },
        "preview_text": {
          "body": {"value": "Your preview text here"},
          "id": "preview_text",
          "name": "preview_text",
          "type": "text",
          "order": 0
        }
      }
    }
  }'
```

Key details:
- `module_id: 1155639` = rich_text module
- `path: "@hubspot/rich_text"` is required
- `schema_version: 2` is required
- `order: 2` for content, `order: 0` for preview text
- HTML goes in `body.html` — use inline styles, `<p>` tags with `margin-bottom:10px`
- Use `{{contact.firstname | default("there")}}` for personalization
- For bold text, use `<strong>` tags inside the HTML
- For CTA buttons, use an inline-styled `<a>` tag (no HubSpot CTA module needed)

### What NOT to do

- Don't set `content.htmlBody` — it conflicts with widget content
- Don't set `emailTemplateMode: "CUSTOM"` — it crashes the editor
- Don't specify widgets during email creation (Step 1) — only during PATCH (Step 2)

### Publishing emails (added 2026-05-04)

The v3 publish endpoint `POST /marketing/v3/emails/{id}/publish` requires the `marketing-email` granular scope (plan-tier-gated, often unavailable on lower-tier portals).

**Workaround that works on `content` scope:**

```bash
curl -X PUT "https://api.hubapi.com/content/api/v2/emails/<EMAIL_ID>" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "PUBLISHED"}'
```

The legacy v2 PUT bypasses the v3-side scope gate. Verified 2026-05-04: works for `BATCH_EMAIL`. Untested on `AUTOMATED_EMAIL` (those use UI-only "Save for automation" anyway).

## Step 3: Create the workflow

```bash
curl -X POST "https://api.hubapi.com/automation/v4/flows" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "40hr Farmer - Welcome Email Sequence",
    "type": "CONTACT_FLOW",
    "objectTypeId": "0-1",
    "isEnabled": false,
    "flowType": "WORKFLOW",
    "startActionId": "1",
    "nextAvailableActionId": "10",
    "actions": [
      {
        "actionId": "1",
        "actionTypeId": "0-4",
        "type": "SINGLE_CONNECTION",
        "connection": {"edgeType": "STANDARD", "nextActionId": "2"},
        "fields": {"content_id": "<EMAIL_01_ID>"}
      },
      {
        "actionId": "2",
        "actionTypeId": "0-1",
        "type": "SINGLE_CONNECTION",
        "connection": {"edgeType": "STANDARD", "nextActionId": "3"},
        "fields": {"delta": "4320", "time_unit": "MINUTES"}
      },
      {
        "actionId": "3",
        "actionTypeId": "0-4",
        "type": "SINGLE_CONNECTION",
        "connection": {"edgeType": "STANDARD", "nextActionId": "4"},
        "fields": {"content_id": "<EMAIL_02_ID>"}
      }
    ],
    "enrollmentCriteria": {
      "shouldReEnroll": false,
      "listFilterBranch": {
        "filterBranches": [{
          "filterBranches": [],
          "filters": [{
            "formId": "<FORM_ID>",
            "operator": "FILLED_OUT",
            "filterType": "FORM_SUBMISSION"
          }],
          "filterBranchType": "AND",
          "filterBranchOperator": "AND"
        }],
        "filters": [],
        "filterBranchType": "OR",
        "filterBranchOperator": "OR"
      },
      "unEnrollObjectsNotMeetingCriteria": false,
      "reEnrollmentTriggersFilterBranches": [],
      "type": "LIST_BASED"
    }
  }'
```

### Action types

| actionTypeId | Purpose | Fields |
|---|---|---|
| `"0-4"` | Send email | `content_id` (the email ID as string) |
| `"0-1"` | Delay | `delta` (string), `time_unit: "MINUTES"` or `"DAYS"` (verified 2026-05-04) |

### Delay math

| Desired delay | delta + time_unit |
|---|---|
| 2 days | `"2880"` MINUTES, or `"2"` DAYS |
| 3 days | `"4320"` MINUTES, or `"3"` DAYS |
| 4 days | `"5760"` MINUTES, or `"4"` DAYS |
| 7 days | `"10080"` MINUTES, or `"7"` DAYS |
| 365 days | `"365"` DAYS (avoids overflow risk in MINUTES) |

`DAYS` is preferred for human-readable workflow JSON. Both are accepted by the API.

### Chaining actions

Each action needs a `connection` object pointing to the next action — except the last one. Pattern: send email -> delay -> send email -> delay -> ... -> send email (no trailing delay).

### Required fields

`isEnabled` and `flowType` are required or the API returns a 400. Create with `isEnabled: false`, then enable manually in the UI when ready.

### Enabling is UI-only (verified 2026-05-04)

There is no public API endpoint that flips a v4 workflow from disabled to enabled. `PUT /automation/v4/flows/{id}` with `isEnabled: true` on a previously-disabled flow returns a generic `FLOW_UPDATE_BAD_REQUEST` 400 with no field-level detail. No `/publish`, `/activate`, `/enable`, or `/start` sub-endpoints exist (POST/PUT/PATCH all 404). v3 `/automation/v3/workflows/{id}` is read-only (mutations return 405). **Practical implication:** sequence edits on an already-enabled workflow (adding emails, editing delays, swapping IDs) work fine via PUT, but creating-and-enabling, or re-enabling after a disable, must go through the HubSpot UI.

### Editing delays in flight (per HubSpot docs, not yet portal-verified)

| Maneuver | Effect on contacts already parked in the delay |
|---|---|
| Edit "set amount of time" delay longer | Rescheduled: wait `new_duration − already_elapsed` |
| Edit "set amount of time" delay shorter than elapsed | Fires immediately |
| Edit "until day or time" delay | Recalculated to new future date; in-flight contacts wait until then |
| Delete the delay step | Contacts immediately advance to the next action |

These are the build-as-you-go primitives for extending a live sequence. Confirmed in HubSpot's official knowledge base (`knowledge.hubspot.com/workflows/use-delays`); not yet smoke-tested in this portal due to the UI-only enablement constraint above.

### v4 ↔ v3 workflow ID mapping

The same workflow has different IDs in `automation/v4/flows/{id}` and `automation/v3/workflows/{id}`. Mutations and current shape live on v4; enrollment and contact-counts (`contactCounts.active`) live on v3. The mapping appears in the v3 GET as `migrationStatus.flowId`.

## Forms (added 2026-05-04)

The waitlist form lives at `POST /marketing/v3/forms` + `PATCH /marketing/v3/forms/{id}`. Same shell-then-PATCH pattern as emails. Hard-won quirks:

### V4 forms are read-only via the public API

A form created in the HubSpot UI is born with `configuration.embedType: "V4"`. PATCH against a V4 form returns:

```
HTTP 403 — "The client is not allowlisted to perform an operation to v4 forms"
```

There is no public v4 forms write endpoint, and DELETE is also blocked (so V4 forms cannot be archived via API either — only via the UI). **If you need to mutate a form via API, create it via API.** Forms created via `POST /marketing/v3/forms` are born `V3` and remain mutable. We hit this wall on 2026-05-04 trying to add `farm_name` + `forty_hour_farmer_deal` to the original UI-created form. Solution: created a new V3 form, swapped the workflow trigger and the JS form GUID over. The retired V4 form `036c50fb-…` should be archived manually in Marketing → Forms.

### Step 1: Create empty form shell

```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
curl -X POST "https://api.hubapi.com/marketing/v3/forms" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"<form name>\",
    \"formType\": \"hubspot\",
    \"createdAt\": \"$NOW\",
    \"updatedAt\": \"$NOW\",
    \"archived\": false,
    \"fieldGroups\": [{
      \"groupType\": \"default_group\",
      \"richTextType\": \"text\",
      \"fields\": [{
        \"objectTypeId\": \"0-1\",
        \"name\": \"email\",
        \"label\": \"Email\",
        \"fieldType\": \"email\",
        \"required\": true,
        \"hidden\": false,
        \"validation\": {\"blockedEmailDomains\": [], \"useDefaultBlockList\": false}
      }]
    }],
    \"configuration\": {
      \"language\": \"en\", \"cloneable\": true, \"editable\": true, \"archivable\": true,
      \"recaptchaEnabled\": false, \"notifyContactOwner\": false, \"notifyRecipients\": [],
      \"createNewContactForNewEmail\": false, \"prePopulateKnownValues\": true,
      \"allowLinkToResetKnownValues\": false,
      \"postSubmitAction\": {\"type\": \"thank_you\", \"value\": \"\"}
    },
    \"displayOptions\": {\"renderRawHtml\": false, \"theme\": \"default_style\", \"submitButtonText\": \"<button label>\", \"style\": {}},
    \"legalConsentOptions\": {\"type\": \"none\"}
  }"
```

Quirks:
- `createdAt` and `updatedAt` are required on POST even though they're server-managed. Send any ISO timestamp; HubSpot overwrites with its own.
- The response confirms `embedType: "V3"` — that's the marker that the API can write to it later.

### Step 2: PATCH fields into the shell

```bash
curl -X PATCH "https://api.hubapi.com/marketing/v3/forms/<FORM_ID>" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "fieldGroups": [<groups>] }'
```

Quirks:
- **Each field needs a `validation` block**, even non-email fields. Send `{"blockedEmailDomains": [], "useDefaultBlockList": false}` to satisfy the schema.
- **Max 3 fields per group.** A group with 4 returns `FormFieldError.FIELD_GROUP_TOO_MANY_FIELDS`. Split into multiple `fieldGroups`.
- For multi-checkbox enumeration properties, `fieldType` is `multiple_checkboxes`. The HubSpot property must already exist (see Custom Contact Properties below) or the PATCH succeeds but the field has no options.

### Custom contact properties (for new form fields)

Properties live on the contact schema, separate from the form. Create them before patching them onto a form.

```bash
# Single-line text
curl -X POST "https://api.hubapi.com/crm/v3/properties/contacts" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "farm_name",
    "label": "Farm name",
    "type": "string",
    "fieldType": "text",
    "groupName": "contactinformation"
  }'

# Multiple-checkbox enumeration
curl -X POST "https://api.hubapi.com/crm/v3/properties/contacts" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "forty_hour_farmer_deal",
    "label": "40-hour farmer deal",
    "type": "enumeration",
    "fieldType": "checkbox",
    "groupName": "contactinformation",
    "options": [
      {"label": "Orisha user", "value": "orisha", "displayOrder": 1, "hidden": false},
      {"label": "Growing for Market subscriber", "value": "gfm", "displayOrder": 2, "hidden": false}
    ]
  }'
```

Quirks:
- **Internal name cannot start with a digit.** `40_hour_farmer_deal` is rejected. Use `forty_hour_farmer_deal` (or any letter prefix).
- Multi-checkbox values are stored as a **`;`-joined string** when they arrive via the Forms Submissions API: a contact with both options checked has `forty_hour_farmer_deal: "orisha;gfm"`.
- **Boolean property shape:** `type: "bool"`, `fieldType: "booleancheckbox"`, with `options: [{"label":"Yes","value":"true","displayOrder":0},{"label":"No","value":"false","displayOrder":1}]`.
- **Deletion blocked while a workflow references the property.** `DELETE /crm/v3/properties/contacts/{name}` returns 400 `PROPERTY_USAGE` until every referencing workflow is deleted (no caching delay once they are).

### Submitting from the page (Forms Submissions API)

Browser-side, no API key required:

```js
fetch(`https://api.hsforms.com/submissions/v3/integration/submit/${PORTAL_ID}/${FORM_ID}`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    fields: [
      {objectTypeId: '0-1', name: 'firstname', value: '...'},
      {objectTypeId: '0-1', name: 'farm_name', value: '...'},
      {objectTypeId: '0-1', name: 'email', value: '...'},
      {objectTypeId: '0-1', name: 'forty_hour_farmer_deal', value: 'orisha;gfm'}
    ],
    context: {pageUri: location.href, pageName: document.title}
  })
});
```

A field that is not listed on the form is silently rejected (the contact gets created but only with the recognized fields). So the form mapping is the contract.

### Auto-marking form contacts as marketing (added 2026-05-04)

By default, contacts created via form submission are NOT marked as marketing contacts and **cannot receive workflow emails**. HubSpot's workflow editor surfaces this as: *"Only marketing contacts can receive this email."*

The fix is **per-form, in the form editor UI** (not exposed via the public API):

Marketing → Forms → open the waitlist form → form settings panel → enable **"Set newly created contacts as marketing contacts"** (exact label varies by portal version, sometimes under an "Options" or "What happens after a visitor submits" tab).

**No public API exposure for this.** The `marketableContactStatus` field is not on `marketing/v3/forms/{id}`. The workflow-side alternative (action type `0-31` "Set marketing contact status") is also v4-API-blocked: every PUT that adds a `0-31` action returns the opaque `FLOW_UPDATE_BAD_REQUEST` 400. UI-only.

**Backfill non-marketing contacts** (e.g., test signups created before the toggle was on): contacts list → select rows → Actions → Set as marketing contacts.

### Updating the workflow trigger after a form swap

If you replaced a form, point the workflow at the new GUID. The endpoint is `PUT` (not `PATCH`):

```bash
# 1. GET the workflow first
curl -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  "https://api.hubapi.com/automation/v4/flows/<FLOW_ID>" > wf.json

# 2. Edit wf.json: swap formId in enrollmentCriteria.listFilterBranch.filterBranches[*].filters[*]
#    where filterType == "FORM_SUBMISSION". Strip server-managed fields:
#    createdAt, updatedAt, crmObjectCreationStatus, id.

# 3. PUT the whole document back
curl -X PUT "https://api.hubapi.com/automation/v4/flows/<FLOW_ID>" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  --data @wf.json
```

Quirks:
- `PATCH` returns 405. The endpoint requires `PUT`.
- `PUT` requires the **full document**, not a partial. Missing `type`, `isEnabled`, `flowType`, etc. → 400.
- Server-managed fields (`createdAt`, `updatedAt`, `crmObjectCreationStatus`, `id`) must be stripped before PUT or the request fails validation.
- `revisionId` increments on each successful PUT.

## Current IDs (May 2026)

| Email | HubSpot ID | Subject |
|---|---|---|
| 01 Welcome | 210995615298 | You're in — here's what's coming |
| 02 Why | 210995615301 | Why we're building this |
| 03 Greenhouse | 210993395305 | The greenhouse trick nobody talks about |
| 04 Drew | 210995615304 | How Drew got his wife back on the farm |
| 05 How It Works | 210993395308 | Here's how it works, simply |

Workflow ID: `1804689064` (still disabled — enable in UI when ready)
Form ID: `7f28cb26-8aea-432e-bf7f-c50a1484d0a3` (V3, API-managed; replaces V4 form `036c50fb-…` retired 2026-05-04)
Custom contact properties: `farm_name` (text), `forty_hour_farmer_deal` (multi-checkbox: `orisha`, `gfm`)

## End-to-end smoke test (added 2026-05-04)

Before pushing changes that touch `email/` or the workflow, run:

```bash
./scripts/test-welcome-funnel.sh
```

Submits a tagged contact (`guillaume+e2e+<timestamp>@orisha.io`) via the public Forms Submissions endpoint, polls for contact creation, verifies firstname / farm_name / forty_hour_farmer_deal / `hs_marketable_status=true`, polls `email/public/v1/events` for a `DELIVERED` event on Email 01, then deletes the test contact. Pass/fail per step. Total runtime ≤60s.

The script auto-loads `HUBSPOT_API_KEY` from `.secrets/hubspot.env`.

## Sequence timing

1. Form submit -> Email 01 (immediate)
2. 3 days -> Email 02
3. 3 days -> Email 03
4. 3 days -> Email 04
5. 4 days -> Email 05
