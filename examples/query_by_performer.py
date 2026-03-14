"""
query_by_performer.py — Find all events featuring a specific performer or guest star.
"""

import json
import glob
import sys

PERFORMER_KEYS = [
    "performers", "Performers", "performer", "featured_performers",
    "band", "bands", "lineup", "Lineup", "line_up",
    "special_performer", "special_performers",
]

GUEST_KEYS = [
    "guest_star", "guest_stars", "Guest Star", "Guest Stars",
    "GUEST STAR", "GUEST STARS", "GuestStar", "guestStars",
    "bintang_tamu", "special_guest", "special_guests",
    "Special Guest Star", "Special Guest Stars",
    "Headliners", "featured_artist", "featuring_artists",
]


def flatten(val):
    if isinstance(val, str):
        return [val]
    if isinstance(val, list):
        result = []
        for item in val:
            result.extend(flatten(item))
        return result
    if isinstance(val, dict):
        result = []
        for v in val.values():
            result.extend(flatten(v))
        return result
    return []


def search_content(event, query):
    c = event.get("Content") or {}
    if not isinstance(c, dict):
        return False, None
    for key in PERFORMER_KEYS + GUEST_KEYS:
        val = c.get(key)
        if not val:
            continue
        names = flatten(val)
        for name in names:
            if query.lower() in name.lower():
                role = "Guest Star" if key in GUEST_KEYS else "Performer"
                return True, (role, name)
    return False, None


query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Perfect Blue"

events = []
for f in sorted(glob.glob("data/*.json")):
    with open(f, encoding="utf-8") as fp:
        events.extend(json.load(fp))

results = []
for e in events:
    found, match = search_content(e, query)
    if found:
        results.append((e, match))

results.sort(key=lambda x: str(x[0].get("Start Date", "")))

print(f"Found '{query}' in {len(results)} event(s)\n")
for e, (role, name) in results:
    d = str(e.get("Start Date", ""))
    date = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d
    city = e.get("location_city", "")
    print(f"  {date}  [{role}] {e.get('Subject', '')}  ({city})")
    print(f"          matched: {name}")
