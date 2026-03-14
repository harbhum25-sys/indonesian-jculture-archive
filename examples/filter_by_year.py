"""
filter_by_year.py — List all events in a year range with summary.
"""

import json
import glob
import sys

start_year = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
end_year = int(sys.argv[2]) if len(sys.argv) > 2 else start_year

events = []
for f in sorted(glob.glob("data/*.json")):
    with open(f, encoding="utf-8") as fp:
        events.extend(json.load(fp))

results = [
    e for e in events
    if start_year <= int(str(e.get("Start Date", "0"))[:4] or 0) <= end_year
]
results.sort(key=lambda e: str(e.get("Start Date", "")))

print(f"Events {start_year}–{end_year}: {len(results)} total\n")
for e in results:
    d = str(e.get("Start Date", ""))
    date = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d
    city = e.get("location_city", "")
    print(f"  {date}  {e.get('Subject', ''):<50}  {city}")
