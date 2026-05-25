#!/usr/bin/env python3
"""Manual stats check for SPEAR Wave 2 sends.

Pulls Postmark stats per tag, computes per-body and combined rates,
checks against the wave-plan kill-switch thresholds, and prints a
verdict (GREEN / RED) per body.

Usage:
  # Check a specific day (1, 2, or 3) — auto-derives the day's tags
  python email/spear/scripts/spear-wave2-check.py --day 1

  # Or check arbitrary tags
  python email/spear/scripts/spear-wave2-check.py --tags 2026-05-26-spear-wave2-day1-bodyA,2026-05-26-spear-wave2-day1-bodyB

  # Or check across all days
  python email/spear/scripts/spear-wave2-check.py --all

Kill-switch thresholds (from email/spear/spear-wave-plan.md):
  - Hard bounce rate > 2%   → RED
  - Spam complaint rate > 0.1% → RED
  - Unsubscribe rate > 4%   → RED (per the cold-list threshold; engaged is 2%)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
POSTMARK_SECRETS_PATH = REPO_ROOT / ".secrets" / "postmark.env"
POSTMARK_BASE = "https://api.postmarkapp.com"
USER_AGENT = "orisha-mailer/1.0 (+https://orisha.io)"

# Day → date map. Update if the schedule shifts.
DAY_DATES = {
    1: "2026-05-26",
    2: "2026-05-27",
    3: "2026-05-28",
}

# Kill-switch thresholds (percent)
BOUNCE_KILL = 2.0
SPAM_KILL = 0.1
UNSUB_KILL = 4.0


def load_key(path: Path, name: str) -> str:
    if os.environ.get(name):
        return os.environ[name]
    if not path.exists():
        sys.exit(f"Missing secrets file: {path} (and env var {name} not set)")
    for line in path.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found in {path} (and env var {name} not set)")


def get_json(token: str, url: str) -> dict:
    request = urllib.request.Request(url, method="GET")
    request.add_header("Accept", "application/json")
    request.add_header("X-Postmark-Server-Token", token)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        return {"_error": f"HTTP {error.code}", "_body": error.read().decode()[:200]}


def fetch_stats(token: str, tag: str) -> dict:
    """Combine overview + bounces + unsubscribes for one tag."""
    overview = get_json(token, f"{POSTMARK_BASE}/stats/outbound?tag={tag}")
    if "_error" in overview:
        return {"tag": tag, "error": overview}
    bounces = get_json(token, f"{POSTMARK_BASE}/stats/outbound/bounces?tag={tag}")
    sent = int(overview.get("Sent", 0))
    tracked = int(overview.get("Tracked", 0))
    opens = int(overview.get("UniqueOpens", 0))
    clicks = int(overview.get("UniqueLinksClicked", 0))
    bounced = int(overview.get("Bounced", 0))
    spam = int(overview.get("SpamComplaints", 0))
    # Postmark doesn't expose unsubscribes per-tag in /stats; pull from suppressions
    return {
        "tag": tag,
        "sent": sent,
        "tracked": tracked,
        "unique_opens": opens,
        "unique_clicks": clicks,
        "bounced": bounced,
        "spam_complaints": spam,
        "open_rate": (opens / sent * 100) if sent else 0,
        "click_rate": (clicks / sent * 100) if sent else 0,
        "bounce_rate": (bounced / sent * 100) if sent else 0,
        "spam_rate": (spam / sent * 100) if sent else 0,
    }


def fetch_unsubscribes_for_stream(token: str, stream: str = "broadcast") -> list[dict]:
    payload = get_json(token, f"{POSTMARK_BASE}/message-streams/{stream}/suppressions/dump")
    if "_error" in payload:
        return []
    return [
        entry for entry in payload.get("Suppressions", [])
        if entry.get("Origin") == "Customer"
    ]


def verdict(stats: dict, day_unsubs: int) -> tuple[str, list[str]]:
    """Returns ('GREEN'|'RED', list of tripped thresholds)."""
    tripped: list[str] = []
    sent = stats["sent"]
    if sent == 0:
        return "PENDING", []
    if stats["bounce_rate"] > BOUNCE_KILL:
        tripped.append(f"bounce rate {stats['bounce_rate']:.2f}% > {BOUNCE_KILL}%")
    if stats["spam_rate"] > SPAM_KILL:
        tripped.append(f"spam rate {stats['spam_rate']:.3f}% > {SPAM_KILL}%")
    unsub_rate = (day_unsubs / sent * 100) if sent else 0
    if unsub_rate > UNSUB_KILL:
        tripped.append(f"unsubscribe rate {unsub_rate:.2f}% > {UNSUB_KILL}%")
    return ("RED" if tripped else "GREEN"), tripped


def print_table(stats_list: list[dict], unsubs_by_tag: dict[str, int]) -> None:
    header = ["tag", "sent", "opens", "open%", "clicks", "click%", "bounces", "bounce%", "spam", "spam%", "unsubs", "verdict"]
    print("  ".join(header))
    print("-" * 140)
    for stats in stats_list:
        if "error" in stats:
            print(f"{stats['tag']}  ERROR: {stats['error']}")
            continue
        unsubs = unsubs_by_tag.get(stats["tag"], 0)
        v, tripped = verdict(stats, unsubs)
        row = [
            stats["tag"],
            str(stats["sent"]),
            str(stats["unique_opens"]),
            f"{stats['open_rate']:.1f}%",
            str(stats["unique_clicks"]),
            f"{stats['click_rate']:.1f}%",
            str(stats["bounced"]),
            f"{stats['bounce_rate']:.2f}%",
            str(stats["spam_complaints"]),
            f"{stats['spam_rate']:.3f}%",
            str(unsubs),
            v,
        ]
        print("  ".join(row))
        if tripped:
            for t in tripped:
                print(f"    ⚠ {t}")


def tags_for_day(day: int) -> list[str]:
    date = DAY_DATES.get(day)
    if not date:
        sys.exit(f"Unknown day {day}. Known: {list(DAY_DATES)}")
    return [
        f"{date}-spear-wave2-day{day}-bodyA",
        f"{date}-spear-wave2-day{day}-bodyB",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--day", type=int, choices=[1, 2, 3], help="check one day's tags")
    group.add_argument("--all", action="store_true", help="check all 3 days")
    group.add_argument("--tags", help="comma-separated explicit tags")
    args = parser.parse_args()

    token = load_key(POSTMARK_SECRETS_PATH, "POSTMARK_SERVER_TOKEN")

    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    elif args.all:
        tags = []
        for day in (1, 2, 3):
            tags.extend(tags_for_day(day))
    else:
        tags = tags_for_day(args.day)

    print(f"Checking {len(tags)} tag(s): {tags}\n")

    stats_list = [fetch_stats(token, tag) for tag in tags]

    # Unsubscribes: Postmark suppressions list doesn't tag-stamp, so we can't
    # cleanly attribute unsubs to a specific tag. Show total customer-origin
    # unsubs on the broadcast stream as a denominator-free signal.
    all_customer_unsubs = fetch_unsubscribes_for_stream(token, "broadcast")
    total_unsubs = len(all_customer_unsubs)
    print(f"Total customer-origin unsubscribes on broadcast stream (all-time, not per-tag): {total_unsubs}\n")

    # Attribute unsubs to tags via CreatedAt window: if unsub happened after the
    # tag's send window started (DAY_DATES[N]), count it against that day.
    unsubs_by_tag: dict[str, int] = {tag: 0 for tag in tags}
    # Best-effort: bucket by date prefix in tag name
    for entry in all_customer_unsubs:
        created = entry.get("CreatedAt", "")
        for tag in tags:
            tag_date = tag[:10]  # YYYY-MM-DD prefix
            if created.startswith(tag_date):
                unsubs_by_tag[tag] += 1
                break

    print_table(stats_list, unsubs_by_tag)

    # Overall verdict for ALL checked tags
    print()
    any_red = False
    for stats in stats_list:
        if "error" in stats:
            continue
        v, _ = verdict(stats, unsubs_by_tag.get(stats["tag"], 0))
        if v == "RED":
            any_red = True
    print("OVERALL:", "RED — kill-switch tripped, do NOT continue" if any_red else "GREEN — safe to continue")


if __name__ == "__main__":
    main()
