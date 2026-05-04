---
name: extend-email-sequence
description: Extend the 40hr Farmer welcome email sequence in HubSpot. Use when the user wants to ship the next email, add Email N+1, append to the welcome sequence, insert a delay, swap an email ID, or otherwise modify the workflow's structure (not its content). Wraps the v4 workflow GET → strip server-managed fields → splice → PUT dance, which is finicky enough to bite if re-derived from memory each time. Builds on `email/HUBSPOT-PROCEDURE.md` (single source of truth for HubSpot quirks).
---

# Extend the email sequence

## When this triggers

User asks to:
- Ship the next email / add Email 6 / Email N+1
- Append to / extend the welcome sequence
- Insert a delay or change the cadence between two emails
- Swap an email ID in the workflow
- Apply the build-as-you-go primitives (delay edit longer/shorter, delete delay) to the live workflow

NOT for: drafting the email copy, rendering the HTML, or creating the email shell. Those are upstream steps in `docs/email/sequence-plan.md`. By the time this skill triggers, you should already have the new email's HubSpot ID.

## Pre-flight

1. **API key.** The script auto-reads `.secrets/hubspot.env` from the project root. No sourcing needed. (Falls back to `$HUBSPOT_API_KEY` if set.)
2. **Confirm the new email's HubSpot ID exists AND it's an AUTOMATED_EMAIL.** Workflows reject `BATCH_EMAIL` as "selected email is invalid." Per the critical caveat at the top of `email/HUBSPOT-PROCEDURE.md`, automated emails cannot be created via API on plans without the `marketing-email` granular scope (verified 2026-05-04 — Guillaume's portal blocks it). They must be built in the HubSpot UI: **Marketing → Email → Create email → Automated → paste body HTML, set subject + preview text + from/reply-to → Save for automation**. Verify the type:
   ```bash
   curl -s -H "Authorization: Bearer $HUBSPOT_API_KEY" \
     "https://api.hubapi.com/marketing/v3/emails/<EMAIL_ID>" | jq '.id, .name, .subject, .type'
   ```
   `.type` must be `AUTOMATED_EMAIL`. If it's `BATCH_EMAIL`, the workflow PUT will succeed but the workflow editor will flag the email as invalid and the email won't send.
3. **Note the workflow's enabled state.** If currently enabled, the edit goes live the moment you PUT — in-flight contacts will pick up the change per the delay primitives in the procedure doc. If currently disabled, the edit stages cleanly but you'll need to re-enable in the HubSpot UI (no API for that — see `HUBSPOT-PROCEDURE.md` "Enabling is UI-only").
4. **Show the current sequence first.** Always run `--show` and surface it to the user before mutating.
5. **After applying, run the E2E smoke test.** `./scripts/test-welcome-funnel.sh` from the repo root submits a tagged contact, verifies all properties + marketing flag + Email 01 delivery, then cleans up. Confirms the change didn't break the live pipeline.

## Recipe

The helper script lives at `.claude/skills/extend-email-sequence/scripts/extend_sequence.py`. It uses Python stdlib only (no install needed).

### Show current sequence

```bash
python3 .claude/skills/extend-email-sequence/scripts/extend_sequence.py --show
```

Pretty-prints the chain: `Email 1 (id) → 3d delay → Email 2 (id) → ...`. Default workflow ID is the production one (`1804689064`).

### Append a new email at the tail

```bash
python3 .claude/skills/extend-email-sequence/scripts/extend_sequence.py \
  --workflow-id 1804689064 \
  --append-email --email-id <NEW_EMAIL_ID> --delay-days 3 \
  --dry-run
```

Always start with `--dry-run`. It prints the current chain, the proposed new chain, and the diff. Drop `--dry-run` to apply (PUT). Reports the new `revisionId` on success.

**Default behavior parks contacts at the tail** for build-as-you-go. Every `--append-email` adds three actions: a cadence delay (your `--delay-days`), the new email, and a 365-day parking delay marked `[PARKING]` in `--show`. Contacts who finish the new email then sit in the parking delay — they don't exit the workflow. When you append the *next* email, the script auto-strips the existing parking delay first, so the chain stays clean across many extensions.

If you're appending the genuinely-final email of a sequence (no more emails ever coming), pass `--final` to skip the parking delay:

```bash
python3 .claude/skills/extend-email-sequence/scripts/extend_sequence.py \
  --append-email --email-id <ID> --delay-days 3 --final
```

You can also strip a parking delay later by appending the next email (auto), or by `--remove-tail`-ing it (which removes the last `delay + email + parking` triple).

### Remove the tail

```bash
python3 .claude/skills/extend-email-sequence/scripts/extend_sequence.py \
  --workflow-id 1804689064 \
  --remove-tail \
  --dry-run
```

Drops the last email plus its preceding cadence delay, plus any trailing parking delay if present. Useful for rollback or roundtrip testing. Errors out if the chain is too short to remove safely (need ≥3 actions, or ≥4 if there's parking).

### Insert in the middle, edit a delay, swap an email ID

The script intentionally only supports append + remove-tail today. For more invasive edits (insert mid-chain, edit a delay's `delta`, swap a `content_id`), GET the workflow JSON, edit by hand, strip server-managed fields, and PUT — patterns documented in `email/HUBSPOT-PROCEDURE.md` "Updating the workflow trigger after a form swap". Surface the proposed new JSON to Guillaume before PUT.

## Server-managed fields to strip before PUT

`createdAt`, `updatedAt`, `crmObjectCreationStatus`, `id`. The script handles this automatically; mention it if you ever PUT by hand.

## Build-as-you-go primitives (reference)

From `email/HUBSPOT-PROCEDURE.md`, the in-flight contact behaviors:

| Maneuver | Effect on contacts already parked in the delay |
|---|---|
| Edit "set amount of time" delay longer | Rescheduled: wait `new_duration − already_elapsed` |
| Edit "set amount of time" delay shorter than elapsed | Fires immediately |
| Edit "until day or time" delay | Recalculated to new future date |
| Delete the delay step | Contacts immediately advance to the next action |

These are documented in HubSpot's KB but not yet portal-verified for `5156324`. When making the first invasive edit on a live-enabled workflow, do it on a low-stakes step and verify the result matches before relying on it broadly.

## After applying

1. Note the new `revisionId` somewhere visible (the user will see it in the script output).
2. If the workflow was disabled, remind Guillaume he needs to re-enable in the HubSpot UI.
3. Confirm in HubSpot UI that the chain looks right, especially the connection arrows. The API doesn't lint shape errors — a missing `connection.nextActionId` in the middle of the chain creates a dead-end branch silently.

## Related files

- `email/HUBSPOT-PROCEDURE.md` — single source of truth for HubSpot API quirks (delay primitives, V4-form trap, custom property creation, workflow PUT requirements).
- `docs/email/sequence-plan.md` — process for drafting + locking each email before it's ready to install.
- `brand/docs/brand/email-sequences.md` — voice + structural guidance for the welcome sequence.
