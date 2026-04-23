# docs/landing/

Everything for the 40hr Farmer landing page rework.

## Three concerns, three kinds of file

| Concern | File | What lives here |
|---|---|---|
| **Process** — how we build | [`process.md`](process.md) | Method only. Reader-type-first section design, Brunson-Mefferd voice, fit-determination CTA logic, step sequence, voice rules. Reusable across future pages. No page-specific content. |
| **Working doc** — what this page is | [`outline.md`](outline.md) | The page top to bottom: section order, beats, visual layout notes, reader-type per section, subsection intents, status per subsection, **and locked copy verbatim**. This is the source of truth for what ships. |
| **Raw material** — what we draft FROM | [`sources/`](sources/) | Curated landing-specific extracts of quotes and source material (Dan's pull-quotes, Drew's video quotes). Full transcripts and raw notes live in the `brand/` submodule; this directory holds the landing pull. |

## Working discipline

- When a subsection locks, write the prose into `outline.md` under the matching section **immediately**. Don't let locked work live only in conversation memory.
- When the outline and locked prose drift on facts (personnel, numbers, cadence), locked prose wins. Update the outline's beat text to match and flag the change with a `**Drift note:**` line.
- `process.md` describes method only. Don't store page-specific drafts or locked copy there. If `outline.md` ever feels too crowded with method, revisit the split.
- Brand/story canon (Drew raw notes, Gordon raw notes, Scott Sigurdson, story-and-origin) stays in `brand/docs/internal/` in the brand submodule. Don't duplicate it here; extract pull-quotes into `sources/` when a quote is being used in landing copy.

## Future pages

If we rework a different asset (email sequence, sales page), mirror this structure: `docs/<asset>/process.md` + `outline.md` + `sources/`. Same three-concern split, same save-on-lock discipline.
