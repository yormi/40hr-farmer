#!/usr/bin/env python3
"""Scrape Instagram comments matching a keyword and write them to CSV.

Built for the COACH call-to-action on @orisha_auto posts (collab posts with
@growingformarketmagazine appear on Orisha's own feed, so one account covers
both). Defaults to the last 7 days.

  python scripts/scrape-instagram-keyword-comments.py
  python scripts/scrape-instagram-keyword-comments.py --days 30
  python scripts/scrape-instagram-keyword-comments.py --keyword salsa \
      --account growingformarketmagazine --since 2025-04-01 --until 2025-07-19

Output: CSV with username, post_code, post_url, post_date, comment, is_reply.
Default path instagram-scrape/<keyword>-commenters-<since>_to_<until>.csv.

Auth: uses Instagram's private web API, which needs a logged-in session
cookie. Put yours in .secrets/instagram.env (or set IG_SESSIONID in env):

    IG_SESSIONID=...
    IG_DS_USER_ID=...      # optional, some endpoints want it

Get the values from a logged-in Chrome: DevTools > Application > Cookies >
instagram.com > sessionid / ds_user_id. The cookie expires roughly yearly;
re-copy it when the script starts returning 401.

Rate limits: Instagram throttles hard past a few hundred requests. The script
sleeps between calls and backs off on 429/560. A week of posts takes under a
minute; a full year takes ~30 minutes.
"""

import argparse
import csv
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

import requests

API_ROOT = "https://www.instagram.com/api/v1"
WEB_APP_ID = "936619743392459"
REPO_ROOT = Path(__file__).resolve().parent.parent
SECRETS_FILE = REPO_ROOT / ".secrets" / "instagram.env"
# Scraped lists land next to this script.
OUTPUT_DIR = Path(__file__).resolve().parent

# Comments by the brand accounts themselves are never campaign responses.
OWN_ACCOUNTS = {"orisha_auto", "growingformarketmagazine"}


def load_session():
    sessionid = os.environ.get("IG_SESSIONID")
    ds_user_id = os.environ.get("IG_DS_USER_ID")
    if not sessionid and SECRETS_FILE.exists():
        for line in SECRETS_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            value = value.strip().strip("'\"")
            if key.strip() == "IG_SESSIONID":
                sessionid = value
            elif key.strip() == "IG_DS_USER_ID":
                ds_user_id = value
    if not sessionid:
        sys.exit(
            f"No Instagram session cookie. Set IG_SESSIONID in env or {SECRETS_FILE}.\n"
            "See this script's docstring for where to copy it from."
        )
    session = requests.Session()
    session.headers.update(
        {
            "x-ig-app-id": WEB_APP_ID,
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
        }
    )
    session.cookies.set("sessionid", sessionid, domain=".instagram.com")
    if ds_user_id:
        session.cookies.set("ds_user_id", ds_user_id, domain=".instagram.com")
    return session


def get(session, url, attempts=5):
    """GET with backoff. Returns parsed JSON, or None once attempts run out."""
    for attempt in range(attempts):
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            time.sleep(random.uniform(0.4, 0.9))
            return response.json()
        if response.status_code in (401, 403):
            sys.exit(
                f"Instagram returned {response.status_code}. The session cookie is "
                "expired or invalid; copy a fresh one from your browser."
            )
        time.sleep(2 ** attempt + random.random())
    print(f"  giving up on {url}", file=sys.stderr)
    return None


def iter_posts(session, account, since_ts, until_ts):
    """Yield posts in [since_ts, until_ts). Walks the feed newest-first."""
    max_id = None
    while True:
        url = f"{API_ROOT}/feed/user/{account}/username/?count=12"
        if max_id:
            url += f"&max_id={quote(str(max_id))}"
        payload = get(session, url)
        if not payload:
            return
        items = payload.get("items") or []
        if not items:
            return
        for item in items:
            if since_ts <= item["taken_at"] < until_ts:
                yield item
        if all(item["taken_at"] < since_ts for item in items):
            return
        if not payload.get("more_available"):
            return
        max_id = payload.get("next_max_id")
        if not max_id:
            return


def iter_comments(session, media_id):
    """Yield (username, text, is_reply) for every comment on a post."""
    min_id = None
    pages = 0
    while pages < 20:
        url = f"{API_ROOT}/media/{media_id}/comments/?can_support_threading=true"
        if min_id:
            url += f"&min_id={quote(str(min_id))}"
        payload = get(session, url)
        if not payload:
            return
        for comment in payload.get("comments") or []:
            yield comment.get("user", {}).get("username"), comment.get("text", ""), False
            for reply in comment.get("preview_child_comments") or []:
                yield reply.get("user", {}).get("username"), reply.get("text", ""), True
        min_id = payload.get("next_min_id")
        pages += 1
        if not min_id:
            return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="coach")
    parser.add_argument("--account", default="orisha_auto")
    parser.add_argument("--days", type=int, default=7, help="ignored if --since given")
    parser.add_argument("--since", help="YYYY-MM-DD, inclusive")
    parser.add_argument("--until", help="YYYY-MM-DD, exclusive (default: now)")
    parser.add_argument("--output", help="CSV path (default: ~/Desktop/...)")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    until = (
        datetime.fromisoformat(args.until).replace(tzinfo=timezone.utc)
        if args.until
        else now
    )
    since = (
        datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
        if args.since
        else until - timedelta(days=args.days)
    )
    since_ts, until_ts = int(since.timestamp()), int(until.timestamp())

    output = Path(
        args.output
        or OUTPUT_DIR
        / f"{args.keyword}-commenters-{since:%Y-%m-%d}_to_{until:%Y-%m-%d}.csv"
    )

    # \b so "coach" matches "Coach!" and "COACH pls" but not "coaching".
    pattern = re.compile(rf"\b{re.escape(args.keyword)}\b", re.IGNORECASE)
    session = load_session()

    print(f"Posts by @{args.account}, {since:%Y-%m-%d} to {until:%Y-%m-%d}")
    posts = list(iter_posts(session, args.account, since_ts, until_ts))
    with_comments = [post for post in posts if post.get("comment_count")]
    print(f"  {len(posts)} posts, {len(with_comments)} with comments")

    rows = []
    for index, post in enumerate(with_comments, start=1):
        date = datetime.fromtimestamp(post["taken_at"], timezone.utc).date().isoformat()
        found = 0
        for username, text, is_reply in iter_comments(session, post["pk"]):
            if username and username not in OWN_ACCOUNTS and pattern.search(text):
                rows.append(
                    {
                        "username": username,
                        "post_code": post["code"],
                        "post_url": f"https://www.instagram.com/p/{post['code']}/",
                        "post_date": date,
                        "comment": text.replace("\n", " ").strip(),
                        "is_reply": is_reply,
                    }
                )
                found += 1
        print(f"  [{index}/{len(with_comments)}] {post['code']} {date}: {found}")

    # One account can hit several posts; keep every hit but dedupe exact repeats.
    seen = set()
    deduped = []
    for row in rows:
        key = (row["username"], row["post_code"], row["comment"])
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(deduped[0].keys()) if deduped
                               else ["username", "post_code", "post_url", "post_date",
                                     "comment", "is_reply"])
        writer.writeheader()
        writer.writerows(deduped)

    distinct = len({row["username"] for row in deduped})
    print(f"\n{len(deduped)} comments from {distinct} distinct accounts")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
