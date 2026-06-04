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
  `outline/template.md`. Each video keeps intro / body / conclusion.

## Pre-seed Sources

- Andrew's book: `/home/guillaume/Downloads/The 40hr Farmer/Livre Andrew.pdf` — extracted text in `sources/book-raw.txt`, split by chapter in `sources/chapters/`
- Orisha course (logged-in): https://www.orisha.io/learn/6-steps-to-15000-45n8732bddg8 — full capture in `sources/course-scrape-raw.md`
- `brand/docs/internal/`: `drew-raw-notes.md`, `gordon-raw-notes.md`, `drew-video-transcript.md`
- Orisha Customer stories: https://docs.google.com/document/d/1oyDiEyFvQ3u-YYOu8kxImkteDnklY3d-jh3Zj_hixXE/edit?tab=t.0#heading=h.a6n9uswhqmso

## Emails
* Andrew: andrew@growingformarket.com 
* Antoine: info@jardinsdinverness.com 
* LB: louis-bernard@orisha.io 

## Asking for input
* **[Claude]** Send the email via Postmark, transactional stream, Reply-To guillaume@orisha.io.
* **[Claude]** Include the stage's Google Doc link.
* **[Claude]** Ask for input **inline, in a different colour**.
* **[Guillaume]** Set the Doc's link sharing → anyone with the link can comment.
* **[Claude]** Name the deadline in the email → 3 business days later.
* **[Claude, scheduled +3 business days]** On the deadline → read the marked-up Doc, do the next step from the inline input, Postmark Guillaume a review reminder. Set up with `/schedule` at send time.

## Working files
* Create `outline/<Month>-<Topic>/` for created files.
* Drive folder for Google Docs: https://drive.google.com/drive/folders/1Mb9Sro3XQJXcUq3FwUTkj0dOs6LjvQ_E
* **One Doc per month with three tabs** (Brainstorm / Outline Skeletons / Outline), not a separate Doc per stage. Real Google Doc tabs hold each stage; populate later tabs in place. Supersedes the earlier per-stage-Doc scheme.
* **Formatting + generation standard:** [`gdoc-formatting.md`](gdoc-formatting.md). Built via the `gdocs-uploader` MCP with `blank_between_paragraphs=True`, native styles, default line spacing.

## Pipeline

### Stage 1 — Brainstorm (source-seeded)

1. **[Claude]** Mine candidate tips from the sources → `01-brainstorm.md`, built per `brainstorm-spec.md`.

1. **[Guillaume]** Approve

1. **[Claude]** Create the `Brainstorm` Doc from `01-brainstorm.md`.

1. **[Guillaume]** Set the `Brainstorm` Doc's link sharing to public (anyone with the link can comment).

1. **[Claude]** Ask for input (per `## Asking for input`, using `brainstorm-input-email.md`)
    * `Brainstorm` Doc
    * To Andrew and Antoine
    * Ask for thoughts, additions, related stories, visual ideas

1. **[Claude, scheduled +3 business days]** Read the marked-up
   `Brainstorm` Doc, merge inline input into `01-brainstorm.md`, and
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
    * Write to the `Outline Skeletons` Doc

1. **[Guillaume]** Approve the Skeletons.

1. **[Claude]** Ask for input (per `## Asking for input`)
    * `Outline Skeletons` Doc
    * To Andrew and Antoine
    * Asking to fill the gaps

1. **[Claude, scheduled +3 business days]** Read the marked-up
   `Outline Skeletons` Doc, fold the gap answers into the skeletons, and
   Postmark Guillaume a reminder to review before Stage 4.

### Stage 4 — Finalize

1. **[Claude]** Fill `outline/template.md` per video
    * Hook, body beats with speaker tags, one-action close, next hook + b-roll + casting shot plan
    * Use the input-enriched skeletons
    * Write to the `Outline` Doc
    * Every video = one page

1. **[Guillaume]** Approve

1. **[Claude]** Notify that the outline is ready (Postmark)
    * Send to Andrew, LB and Antoine
    * Share the link of the `Outline` Doc
    * Add that everyone is responsible to arrive to the next shooting session with a good idea of the outline

## Non-negotiables

Per `outline/CLAUDE.md` (story first, never extrapolate, number + felt
meaning, one action per video, no dashes, quiet farm-journal voice).
