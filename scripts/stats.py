"""
stats.py — Print dataset statistics.

Usage:
    python scripts/stats.py
"""

import json
import glob
from collections import Counter
from datetime import datetime

events = []
for f in sorted(glob.glob("data/*.json")):
    with open(f, encoding="utf-8") as fp:
        year_events = json.load(fp)
        events.extend(year_events)

total = len(events)
years = sorted(set(str(e.get("Start Date", ""))[:4] for e in events if e.get("Start Date")))
cities = Counter(e.get("location_city", "").strip() for e in events if e.get("location_city", "").strip())
statuses = Counter(e.get("status", "") for e in events)
has_coords = sum(1 for e in events if (e.get("location_coordinate") or "").strip())
has_content = sum(1 for e in events if e.get("Content") and e.get("Content") != {})
has_gmaps = sum(1 for e in events if (e.get("location_gmaps") or "").strip())
attended_yes = sum(1 for e in events if (e.get("attended") or "").lower() == "yes")
per_year = Counter(str(e.get("Start Date", ""))[:4] for e in events)

print("=" * 50)
print("Indonesian J-Culture Event Archive — Stats")
print("=" * 50)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print()
print(f"Total events    : {total:,}")
print(f"Year span       : {years[0]} – {years[-1]}")
print(f"Unique cities   : {len(cities):,}")
print(f"With coordinates: {has_coords:,} ({has_coords/total*100:.1f}%)")
print(f"With GMaps link : {has_gmaps:,} ({has_gmaps/total*100:.1f}%)")
print(f"With Content    : {has_content:,} ({has_content/total*100:.1f}%)")
print(f"Personally att. : {attended_yes:,}")
print()

print("Events per year:")
for yr in sorted(per_year):
    bar = "█" * min(40, int(per_year[yr] / 60))
    print(f"  {yr}  {per_year[yr]:>5}  {bar}")
print()

print("Top 10 cities:")
for city, count in cities.most_common(10):
    print(f"  {city:<25} {count:>5}")
print()

print("Status breakdown:")
for status, count in statuses.most_common():
    if status:
        print(f"  {status:<20} {count:>5}")
