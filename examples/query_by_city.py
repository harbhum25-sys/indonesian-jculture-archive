"""
query_by_city.py — Find all events in a specific city.
"""

import json
import glob
import sys

city = sys.argv[1] if len(sys.argv) > 1 else "Bandung"

events = []
for f in sorted(glob.glob("data/*.json")):
    with open(f, encoding="utf-8") as fp:
        events.extend(json.load(fp))

results = [
    e for e in events
    if city.lower() in (e.get("location_city") or "").lower()
]

results.sort(key=lambda e: str(e.get("Start Date", "")))

print(f"Found {len(results)} events in '{city}'\n")
for e in results:
    d = str(e.get("Start Date", ""))
    date = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d
    print(f"  {date}  {e.get('Subject', '')}")
