#!/usr/bin/env python3
"""Send the brainstorm input email from brainstorm-input-email.md via Postmark.

Reads the template, fills {{...}} slots, renders the markdown subset to HTML
(Next Steps block in secondary gray per the template's Rendering note), and
sends on Postmark's transactional stream with Reply-To guillaume@orisha.io.

Defaults to a safe test send to guillaume@orisha.io with a [TEST] subject.
Pass --send to deliver to the real recipients in the template's To: line.

Env (from .secrets/postmark.env): POSTMARK_SERVER_TOKEN, POSTMARK_FROM.

Example:
  python3 send-input-email.py \
    --month July \
    --goal "Taking control of plant vigor through the summer" \
    --doc-link "https://docs.google.com/document/d/.../edit" \
    --deadline "Tuesday, June 9" --deadline-short "Tue Jun 9"
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "brainstorm-input-email.md")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ENV_FILE = os.path.join(REPO_ROOT, ".secrets", "postmark.env")
GDOCS_PYTHON = os.path.expanduser(
    "~/.local/share/mcp-servers/gdocs-uploader/venv/bin/python")
GDOCS_DIR = os.path.expanduser("~/.local/share/mcp-servers/gdocs-uploader")

GRAY = "#9aa0a6"
DOC_LINK_SLOT = "{{BRAINSTORM_DOC_LINK}}"
# type=anyone with any of these roles = publicly accessible.
# Shared Drives report "Editor" general access as fileOrganizer/organizer.
PUBLIC_ROLES = {"reader", "commenter", "writer", "fileOrganizer", "organizer"}


def doc_id_from_link(link):
    match = re.search(r"/document/d/([A-Za-z0-9_-]+)", link)
    if not match:
        sys.exit(f"Could not parse a Google Doc id from --doc-link: {link}")
    return match.group(1)


def doc_public_status(doc_id):
    """Return (is_public, detail). Queries Drive via the gdocs venv (it has creds)."""
    snippet = (
        "import json, server\n"
        "drive = server._drive()\n"
        f"perms = drive.permissions().list(fileId='{doc_id}',"
        " fields='permissions(type,role)', supportsAllDrives=True).execute()\n"
        "print(json.dumps(perms.get('permissions', [])))\n"
    )
    try:
        output = subprocess.run(
            [GDOCS_PYTHON, "-c", snippet],
            cwd=GDOCS_DIR, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, f"permission check failed to run: {error}"
    if output.returncode != 0:
        return False, f"permission check error: {output.stderr.strip()[-300:]}"
    line = [l for l in output.stdout.splitlines() if l.startswith("[")]
    if not line:
        return False, f"unexpected permission output: {output.stdout.strip()[-300:]}"
    perms = json.loads(line[-1])
    public = [p for p in perms if p.get("type") == "anyone"
              and p.get("role") in PUBLIC_ROLES]
    if public:
        return True, f"anyone/{public[0]['role']}"
    anyone_roles = [p.get("role") for p in perms if p.get("type") == "anyone"]
    found = f"anyone roles: {anyone_roles}" if anyone_roles else "no anyone-with-link permission"
    return False, f"need anyone with {sorted(PUBLIC_ROLES)}; {found}"


def load_env(path):
    env = {}
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def extract_email_block(template_text):
    """Return (to_line, subject_line, body) from between the first two `---`."""
    parts = template_text.split("\n---\n")
    if len(parts) < 2:
        sys.exit("Template missing the `---` email block.")
    block = parts[1].strip("\n").splitlines()
    to_line = subject_line = None
    body_start = 0
    for index, line in enumerate(block):
        if line.startswith("**To:**"):
            to_line = line.split("**To:**", 1)[1].strip()
        elif line.startswith("**Subject:**"):
            subject_line = line.split("**Subject:**", 1)[1].strip()
        else:
            body_start = index
            break
    if to_line is None or subject_line is None:
        sys.exit("Template block missing To:/Subject: lines.")
    body = "\n".join(block[body_start:]).strip("\n")
    return to_line, subject_line, body


def fill(text, values):
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def inline(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def render_lines(text):
    """Render the markdown subset line by line: paragraphs, `- ` bullets,
    `1.` numbered lists. A heading line glued to a list still splits cleanly."""
    html, paragraph, items, list_tag = [], [], [], None

    def flush_paragraph():
        if paragraph:
            html.append(f"<p>{inline('<br>'.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list():
        nonlocal list_tag
        if items:
            body = "".join(f"<li>{inline(item)}</li>" for item in items)
            html.append(f"<{list_tag}>{body}</{list_tag}>")
            items.clear()
            list_tag = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            flush_paragraph()
            flush_list()
        elif line.startswith("- "):
            flush_paragraph()
            if list_tag != "ul":
                flush_list()
                list_tag = "ul"
            items.append(line[2:])
        elif re.match(r"^\d+\.\s", line):
            flush_paragraph()
            if list_tag != "ol":
                flush_list()
                list_tag = "ol"
            items.append(re.sub(r"^\d+\.\s", "", line))
        else:
            flush_list()
            paragraph.append(line)
    flush_paragraph()
    flush_list()
    return "\n".join(html)


def render_html(body, doc_link):
    """Render to HTML. The Next Steps heading + its list render in gray."""
    marker = "**Next Steps**"
    if marker in body:
        main, next_steps = body.split(marker, 1)
        steps = [re.sub(r"^\d+\.\s", "", l.strip())
                 for l in next_steps.strip().splitlines() if l.strip()]
        gray_items = "".join(f"<li>{inline(s)}</li>" for s in steps)
        gray_block = (
            f'<div style="color:{GRAY};font-size:13px;margin-top:24px;">'
            f'<p style="color:{GRAY};margin-bottom:4px;"><strong>Next Steps</strong></p>'
            f'<ol style="color:{GRAY};margin-top:0;">{gray_items}</ol></div>'
        )
        html = render_lines(main.strip()) + "\n" + gray_block
    else:
        html = render_lines(body)
    anchor = f'<a href="{doc_link}">Brainstorm doc</a>'
    return html.replace(DOC_LINK_SLOT, anchor)


def post(env, payload):
    request = urllib.request.Request(
        "https://api.postmarkapp.com/email",
        data=json.dumps(payload).encode(),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": env["POSTMARK_SERVER_TOKEN"],
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            print("HTTP", response.status, response.read().decode())
    except urllib.error.HTTPError as error:
        print("HTTP", error.code, error.read().decode())
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--doc-link", required=True)
    parser.add_argument("--deadline", required=True, help='e.g. "Tuesday, June 9"')
    parser.add_argument("--deadline-short", required=True, help='e.g. "Tue Jun 9"')
    parser.add_argument("--send", action="store_true",
                        help="Deliver to the real To: recipients. Default is a test send to POSTMARK_FROM.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the rendered HTML and exit without sending.")
    args = parser.parse_args()

    env = load_env(ENV_FILE)
    template_text = open(TEMPLATE).read()
    to_line, subject_line, body = extract_email_block(template_text)

    # Fill everything except the doc link; the link slot is rendered last
    # (anchor in HTML, raw URL in plain text).
    values = {
        "MONTH": args.month,
        "GOAL": args.goal,
        "DEADLINE": args.deadline,
        "DEADLINE_SHORT": args.deadline_short,
    }
    subject = fill(subject_line, values)
    body = fill(body, values)

    text_body = body.replace(DOC_LINK_SLOT, args.doc_link).replace("**", "")
    html_body = render_html(body, args.doc_link)

    if args.dry_run:
        print(html_body)
        return

    # Verify the linked Doc is publicly commentable before sending.
    is_public, detail = doc_public_status(doc_id_from_link(args.doc_link))
    print(f"Doc public check: {'OK' if is_public else 'NOT PUBLIC'} ({detail})")
    if args.send and not is_public:
        sys.exit("Refusing to --send: the Doc is not publicly accessible. "
                 "Set the Doc or its folder to 'anyone with the link can comment', "
                 "then retry.")

    if args.send:
        recipient = to_line
    else:
        recipient = env["POSTMARK_FROM"]
        subject = "[TEST] " + subject

    payload = {
        "From": env["POSTMARK_FROM"],
        "To": recipient,
        "ReplyTo": "guillaume@orisha.io",
        "Subject": subject,
        "HtmlBody": html_body,
        "TextBody": text_body,
        "MessageStream": "outbound",
    }
    print(f"{'SEND' if args.send else 'TEST'} → {recipient}")
    print(f"Subject: {subject}")
    post(env, payload)


if __name__ == "__main__":
    main()
