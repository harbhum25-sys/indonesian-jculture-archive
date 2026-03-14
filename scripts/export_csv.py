"""
export_csv.py — Export all events to a flat CSV file.

Usage:
    python scripts/export_csv.py
    python scripts/export_csv.py --output my_export.csv
    python scripts/export_csv.py --year 2007
"""

import json
import glob
import csv
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Export dataset to CSV")
parser.add_argument("--output", default="jculture_events.csv", help="Output filename")
parser.add_argument("--year", help="Export single year only (e.g. 2007)")
args = parser.parse_args()

pattern = f"data/{args.year}.json" if args.year else "data/*.json"
files = sorted(glob.glob(pattern))

if not files:
    print(f"No files found matching: {pattern}")
    sys.exit(1)

events = []
for f in files:
    with open(f, encoding="utf-8") as fp:
        events.extend(json.load(fp))

events.sort(key=lambda e: str(e.get("Start Date", "")))


def fmt_date(d):
    d = str(d)
    if len(d) == 8 and d.isdigit():
        return f"{d[:4]}-{d[4:6]}-{d[6:]}"
    return d


def get_content_value(event, *keys):
    c = event.get("Content") or {}
    if not isinstance(c, dict):
        return ""
    for k in keys:
        v = c.get(k)
        if v:
            if isinstance(v, (list, dict)):
                return json.dumps(v, ensure_ascii=False)
            return str(v)
    return ""


COLUMNS = [
    "id", "subject", "start_date", "end_date", "start_time", "end_time",
    "city", "location", "address", "coordinate", "gmaps_url",
    "online_offline", "status", "attended",
    "organizer", "theme", "performers", "guest_stars", "ticket_price",
    "source", "links", "comment"
]

with open(args.output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()

    for e in events:
        links = e.get("links") or []
        links_str = " | ".join(l for l in links if l and str(l).strip())

        writer.writerow({
            "id":            e.get("_id", ""),
            "subject":       e.get("Subject", ""),
            "start_date":    fmt_date(e.get("Start Date", "")),
            "end_date":      fmt_date(e.get("End Date", "")),
            "start_time":    e.get("Start Time", ""),
            "end_time":      e.get("End Time", ""),
            "city":          e.get("location_city", ""),
            "location":      e.get("Location", ""),
            "address":       e.get("location_address", ""),
            "coordinate":    e.get("location_coordinate", ""),
            "gmaps_url":     e.get("location_gmaps", ""),
            "online_offline": e.get("Online/Offline") or e.get("Offline/Online", ""),
            "status":        e.get("status", ""),
            "attended":      e.get("attended", ""),
            "organizer":     get_content_value(e, "organizer", "Organizer", "organized_by", "presenter"),
            "theme":         get_content_value(e, "theme", "Tema", "tema"),
            "performers":    get_content_value(e, "performers", "Performers", "performer", "lineup"),
            "guest_stars":   get_content_value(e, "guest_stars", "guest_star", "Guest Star", "Guest Stars", "bintang_tamu"),
            "ticket_price":  get_content_value(e, "HTM", "htm", "ticket_price", "harga_tiket", "Harga Tiket"),
            "source":        get_content_value(e, "source", "Source", "sumber"),
            "links":         links_str,
            "comment":       (e.get("Comment") or "").replace("\n", " "),
        })

print(f"✓ Exported {len(events)} events to {args.output}")
