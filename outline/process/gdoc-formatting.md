# Google Doc formatting standard (outline process)

Every Google Doc in the outline pipeline is built the same way. Generated
via the local `gdocs-uploader` MCP (see
`~/.local/share/mcp-servers/gdocs-uploader/`, and memory
`reference_gdocs_uploader_mcp`).

## Standard

- **One Doc per month**, in the Shared Drive folder
  `1Mb9Sro3XQJXcUq3FwUTkj0dOs6LjvQ_E` ("The 40 Hour Farmer Program").
- **Three tabs**, in order: `Brainstorm`, `Outline Skeletons`, `Outline`
  (Stages 1, 3, 4 of `process.md`).
- **Native named styles** from Markdown: `#` → Title, `##` → Heading 1,
  `###` → Heading 2, `**bold**` → bold, `- ` → native bullet list.
- **Blank line between every paragraph** (headings, body, and bullets).
- **Default line spacing.** No custom line spacing, no before/after
  paragraph spacing. Do not call `set_paragraph_spacing`.

## How to generate

```python
create_tabbed_gdoc(
    tabs=[{"title": "Brainstorm", "markdown": md},
          {"title": "Outline Skeletons", "markdown": ""},
          {"title": "Outline", "markdown": ""}],
    title="<Month> - <Topic>",
    folder_id="1Mb9Sro3XQJXcUq3FwUTkj0dOs6LjvQ_E",
    blank_between_paragraphs=True,
)
```

Strip any repo-only `Status:` line from the Markdown before sending.
Populate the Skeletons / Outline tabs in place in later stages.
