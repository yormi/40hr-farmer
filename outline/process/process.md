# Monthly outline process

Reusable for any month. The month's goal and release window are set per
month at the top of that month's `01-brainstorm.md` (per `brainstorm-spec.md`);
this file is the goal-agnostic procedure that turns that goal into shot-ready
outlines.

## Cast

- **Antoine** — farmers who's done it / practitioner / lean lens.
- **Andrew Mefferd** — wrote a book / used to be a farmer / work with/for farmers.
- **Guillaume** — brand-voice spine when on camera.

(Full bios: `docs/project-state.md`.)

## Output shape

- **4-12 short videos**, 3 min ideal / 5 max. Brainstorm clusters decide
  the count.
- Casting + per-beat speaker tags + b-roll shot plan: see
  `outline/process/template.md`. Each video keeps intro / body / conclusion.

## Pre-seed Sources

- Andrew's book: `/home/guillaume/Downloads/The 40hr Farmer/Livre Andrew.pdf` — extracted text in `sources/book-raw.txt`, split by chapter in `sources/chapters/`
- Heuvelink (ed.), *Tomatoes*, 2nd ed., CABI 2018: `sources/Heuvelink2018_Tomatoes_CABI_2ndEd.pdf` — extracted text in `sources/heuvelink-raw.txt`, split by chapter in `sources/heuvelink-chapters/`
- Turcotte et al., *Production de la tomate de serre au Québec* (2015): `sources/Production de la tomate de serre.pdf`
- Orisha course (logged-in): https://www.orisha.io/learn/6-steps-to-15000-45n8732bddg8 — full capture in `sources/course-scrape-raw.md`
- `brand/docs/internal/`: `drew-raw-notes.md`, `gordon-raw-notes.md`, `drew-video-transcript.md`
- Orisha Customer stories: https://docs.google.com/document/d/1oyDiEyFvQ3u-YYOu8kxImkteDnklY3d-jh3Zj_hixXE/edit?tab=t.0#heading=h.a6n9uswhqmso

## Emails
* Andrew: andrew@growingformarket.com 
* Antoine: info@jardinsdinverness.com 
* LB: louis-bernard@orisha.io 

## Asking for input
* **[Claude]** Send via `send-input-email.py` (Postmark transactional stream,
  Reply-To guillaume@orisha.io). It fills `brainstorm-input-email.md`, renders
  the lists + gray Next Steps, and links the Doc as "Brainstorm doc". Run order:
  `test-send-input-email.py` → `--dry-run` → `--send` (default with no `--send`
  is a `[TEST]` send to guillaume@orisha.io).
* **[Claude]** Ask for input **inline, in a different colour** (in the template).
* **[Guillaume]** Set the Doc's link sharing → anyone with the link can comment.
* **[Claude]** Name the deadline → 3 business days later (`--deadline`).
* **[Claude]** Generate a Google Calendar add-event link to continue the work
  at **9:30 AM the next business day after the deadline** (Claude can't write
  the calendar directly; Drive is the only connected Google tool). Guillaume
  clicks it to add. Convert the local time (America/Toronto) to UTC in the
  link's `dates`.
* **[Guillaume]** On that calendar nudge → start a session. Claude reads the
  marked-up Doc, folds the inline input into the source markdown, and Postmarks
  Guillaume a review reminder before the next stage.

## Working files
* Create `outline/<Month>-<Topic>/` for created files.
* Drive folder for Google Docs: https://drive.google.com/drive/folders/1Mb9Sro3XQJXcUq3FwUTkj0dOs6LjvQ_E
* **One Doc per month with three tabs** (Brainstorm / Outline Skeletons / Outline), not a separate Doc per stage. Real Google Doc tabs hold each stage; populate later tabs in place. Supersedes the earlier per-stage-Doc scheme.
* **Formatting + generation standard:** [`gdoc-formatting.md`](gdoc-formatting.md). Built via the `gdocs-uploader` MCP with `blank_between_paragraphs=True`, native styles, default line spacing.

## Pipeline

### Stage 1 — Brainstorm (source-seeded)

1. **[Claude]** Mine candidate tips from the sources → `01-brainstorm.md`, built per `brainstorm-spec.md`.

1. **[Guillaume]** Approve

1. **[Claude]** Create the month Doc with 3 tabs via `create_tabbed_gdoc` (per `gdoc-formatting.md`); populate the `Brainstorm` tab from `01-brainstorm.md`, leave the other tabs empty.

1. **[Guillaume]** Set the Doc's link sharing to public (anyone with the link can comment).

1. **[Claude]** Ask for input (per `## Asking for input`, using `brainstorm-input-email.md`)
    * `Brainstorm` tab
    * To Andrew and Antoine
    * Ask for thoughts, additions, related stories, visual ideas

1. **[Claude, scheduled +3 business days]** Read the marked-up
   `Brainstorm` tab, merge inline input into `01-brainstorm.md`, and
   Postmark Guillaume a reminder to review the merge before Stage 2.

### Stage 2 — Organize

1. **[Claude]** Cluster the input-enriched tips into 4-12 video topics → `02-video-cuts.md`
    * a working title
    * 2-4 body points
    * a proposed casting (who, one-line why)

1. **[Guillaume]** Approve

### Stage 3 — Stories + gaps

1. **[Claude]** Build outline skeletons
    * Use `02-video-cuts.md`
    * Make the asks concrete
    * per video, story prompts (where a hook is needed) and open gaps (number to verify, fuzzy step)
    * Populate the `Outline Skeletons` tab in place

1. **[Guillaume]** Approve the Skeletons.

1. **[Claude]** Ask for input (per `## Asking for input`)
    * `Outline Skeletons` tab
    * To Andrew and Antoine
    * Asking to fill the gaps

1. **[Claude, scheduled +3 business days]** Read the marked-up
   `Outline Skeletons` tab, fold the gap answers into the skeletons, and
   Postmark Guillaume a reminder to review before Stage 4.

### Stage 4 — Finalize

1. **[Claude]** Fill `outline/process/template.md` per video
    * Hook, body beats with speaker tags, one-action close, next hook + b-roll + casting shot plan
    * Use the input-enriched skeletons
    * Populate the `Outline` tab in place
    * Every video = one page

1. **[Guillaume]** Approve

1. **[Claude]** Notify that the outline is ready (Postmark)
    * Send to Andrew, LB and Antoine
    * Share the link of the `Outline` tab
    * Add that everyone is responsible to arrive to the next shooting session with a good idea of the outline

## Non-negotiables

Per `outline/CLAUDE.md` (story first, never extrapolate, number + felt
meaning, one action per video, no dashes, quiet farm-journal voice).
