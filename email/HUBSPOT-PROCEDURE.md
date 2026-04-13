# HubSpot Email & Workflow Setup via API

How we got the welcome email sequence into HubSpot. Browser automation didn't work (the email editor renders in an iframe that blocks drag-and-drop). The API works, but has quirks.

## Prerequisites

- HubSpot Private App API key with scopes: `content`, `automation`, `forms`
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
| `"0-1"` | Delay | `delta` (minutes as string), `time_unit: "MINUTES"` |

### Delay math

| Desired delay | delta (minutes) |
|---|---|
| 2 days | `"2880"` |
| 3 days | `"4320"` |
| 4 days | `"5760"` |
| 7 days | `"10080"` |

### Chaining actions

Each action needs a `connection` object pointing to the next action — except the last one. Pattern: send email -> delay -> send email -> delay -> ... -> send email (no trailing delay).

### Required fields

`isEnabled` and `flowType` are required or the API returns a 400. Create with `isEnabled: false`, then enable manually in the UI when ready.

## Current IDs (April 2026)

| Email | HubSpot ID | Subject |
|---|---|---|
| 01 Welcome | 210995615298 | You're in — here's what's coming |
| 02 Why | 210995615301 | Why we're building this |
| 03 Greenhouse | 210993395305 | The greenhouse trick nobody talks about |
| 04 Drew | 210995615304 | How Drew got his wife back on the farm |
| 05 How It Works | 210993395308 | Here's how it works, simply |

Workflow ID: `1804689064`
Form ID: `036c50fb-2650-48ba-a1af-eb12a8f1074e`

## Sequence timing

1. Form submit -> Email 01 (immediate)
2. 3 days -> Email 02
3. 3 days -> Email 03
4. 3 days -> Email 04
5. 4 days -> Email 05
