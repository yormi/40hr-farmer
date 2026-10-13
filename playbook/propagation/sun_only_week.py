#!/usr/bin/env python3
"""First week seedlings can rely on greenhouse sun alone, for any address.

Target = 250 µmol × 16 h = 14.4 mol/m²/day. Sun-only when the 10-year
average inside DLI reaches 90 % of it. Radiation from Open-Meteo ERA5.

  python3 sun_only_week.py "2020 rue du Vignoble, Québec" --covering double
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta

TARGET_MOL = 14.4
SUN_ONLY_FRACTION = 0.9
TRANSMISSION = {"single": 0.7, "double": 0.6}
MOL_PAR_PER_MJ = 2.1
YEARS = 10
USER_AGENT = "orisha-sun-only-week/1.0"


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def geocode(address):
    query = urllib.parse.urlencode({"q": address, "format": "json", "limit": 1})
    results = fetch_json(f"https://nominatim.openstreetmap.org/search?{query}")
    if not results:
        sys.exit(f"Address not found: {address}")
    return float(results[0]["lat"]), float(results[0]["lon"]), results[0]["display_name"]


def weekly_outside_dli(latitude, longitude):
    end = date.today() - timedelta(days=7)
    start = end.replace(year=end.year - YEARS)
    query = urllib.parse.urlencode({
        "latitude": latitude, "longitude": longitude,
        "start_date": start.isoformat(), "end_date": end.isoformat(),
        "hourly": "shortwave_radiation", "timezone": "auto",
    })
    hourly = fetch_json(f"https://archive-api.open-meteo.com/v1/archive?{query}")["hourly"]
    mol = defaultdict(float)
    days = defaultdict(set)
    for stamp, radiation in zip(hourly["time"], hourly["shortwave_radiation"]):
        moment = datetime.fromisoformat(stamp)
        week = min(moment.isocalendar()[1], 52)
        mol[week] += (radiation or 0.0) * 3600 / 1e6 * MOL_PAR_PER_MJ
        days[week].add(moment.date())
    return {week: mol[week] / len(days[week]) for week in sorted(mol)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("address")
    parser.add_argument("--covering", choices=TRANSMISSION, required=True)
    parser.add_argument("--year", type=int, default=date.today().year + 1, help="season year for dates")
    arguments = parser.parse_args()

    latitude, longitude, place = geocode(arguments.address)
    transmission = TRANSMISSION[arguments.covering]
    inside = {week: dli * transmission for week, dli in weekly_outside_dli(latitude, longitude).items()}
    sun_only = next(week for week in range(1, 53) if inside[week] >= SUN_ONLY_FRACTION * TARGET_MOL)

    print(f"{place}\n{latitude:.4f}, {longitude:.4f} | {arguments.covering} poly, {transmission:.0%} transmission | "
          f"target {TARGET_MOL} mol/m²/d\n")
    print(f"{'wk':>3} {'week of':>10} {'inside DLI':>10} {'% target':>8}")
    for week in range(max(1, sun_only - 5), sun_only + 3):
        monday = date.fromisocalendar(arguments.year, week, 1)
        marker = " <- sun only" if week == sun_only else ""
        print(f"{week:>3} {monday.strftime('%b %d'):>10} {inside[week]:>10.1f} {inside[week] / TARGET_MOL:>7.0%}{marker}")
    print(f"\nlights off from ISO week {sun_only}, week of {date.fromisocalendar(arguments.year, sun_only, 1):%b %d, %Y}")


if __name__ == "__main__":
    main()
