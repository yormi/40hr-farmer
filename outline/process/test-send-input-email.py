#!/usr/bin/env python3
"""Guards send-input-email.py rendering against regressions.

Renders the real brainstorm-input-email.md and asserts the structure that
must hold every send: real <ul>/<ol> lists, stripped list markers, the gray
Next Steps block, a Brainstorm-doc hyperlink, and no leftover placeholders.

Run: python3 test-send-input-email.py   (exits non-zero on failure)
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module():
    spec = importlib.util.spec_from_file_location("sender",
                                                  os.path.join(HERE, "send-input-email.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    m = load_module()
    template = open(os.path.join(HERE, "brainstorm-input-email.md")).read()
    _, subject, body = m.extract_email_block(template)
    values = {"MONTH": "July", "GOAL": "Test goal",
              "DEADLINE": "Tuesday, June 9", "DEADLINE_SHORT": "Tue Jun 9"}
    subject = m.fill(subject, values)
    body = m.fill(body, values)
    link = "https://docs.google.com/document/d/EXAMPLE/edit"
    html = m.render_html(body, link)

    checks = [
        ("bullets render as <ul>", "<ul>" in html and "<li>Actionable tips" in html),
        ("no raw bullet markers leak", "<li>- " not in html),
        ("Next Steps is gray", f'color:{m.GRAY}' in html and "Next Steps" in html),
        ("Next Steps is an <ol>", re.search(r'<ol style="color:%s' % re.escape(m.GRAY), html) is not None),
        ("list numbers stripped", "<li>1. " not in html and "<li>2. " not in html),
        ("doc link is a hyperlink", f'<a href="{link}">Brainstorm doc</a>' in html),
        ("raw URL not shown as text", f"colour: {link}" not in html and f"colour:{link}" not in html),
        ("no leftover placeholders", "{{" not in html and "{{" not in subject),
        ("subject filled", "Tue Jun 9" in subject),
    ]

    failures = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if failures:
        print(f"\n{len(failures)} check(s) failed.")
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
