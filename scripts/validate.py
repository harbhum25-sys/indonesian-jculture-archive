"""
validate.py — Validate all JSON files in the dataset.

Usage:
    python scripts/validate.py
    python scripts/validate.py data/2007.json   # single file
"""

import json
import glob
import sys
from datetime import datetime

REQUIRED_FIELDS = ["Subject", "Start Date", "End Date", "status"]
DATE_FORMAT = "%Y%m%d"
VALID_STATUSES = {
    "Finished", "Completed", "Success", "Past", "Past Event",
    "Cancelled", "Disbanded", "Dropped",
    "Postponed", "Ditunda",
    "Scheduled", "Confirmed", "SCheduled", "SChedulde", "sch", "Schdeuled",
    "No", ""
}

errors = []
warnings = []
total = 0


def check_event(event, source_file, index):
    eid = event.get("_id", f"index:{index}")

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in event:
            errors.append(f"{source_file}[{index}] ({eid}): missing required field '{field}'")

    # Date format
    for date_field in ["Start Date", "End Date"]:
        val = event.get(date_field, "")
        if val:
            try:
                datetime.strptime(str(val), DATE_FORMAT)
            except ValueError:
                errors.append(f"{source_file}[{index}] ({eid}): invalid {date_field} '{val}' — expected YYYYMMDD")

    # Start <= End
    start = event.get("Start Date", "")
    end = event.get("End Date", "")
    if start and end and str(start) > str(end):
        warnings.append(f"{source_file}[{index}] ({eid}): Start Date {start} > End Date {end}")

    # Status
    status = event.get("status", "")
    if status not in VALID_STATUSES:
        warnings.append(f"{source_file}[{index}] ({eid}): unusual status '{status}'")

    # links should be array
    links = event.get("links")
    if links is not None and not isinstance(links, list):
        errors.append(f"{source_file}[{index}] ({eid}): 'links' should be an array, got {type(links).__name__}")

    # Content should be dict or empty
    content = event.get("Content")
    if content is not None and not isinstance(content, dict):
        errors.append(f"{source_file}[{index}] ({eid}): 'Content' should be an object, got {type(content).__name__}")


def validate_file(path):
    global total
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{path}: JSON parse error — {e}")
        return
    except Exception as e:
        errors.append(f"{path}: could not read file — {e}")
        return

    if not isinstance(data, list):
        errors.append(f"{path}: expected a JSON array at top level")
        return

    for i, event in enumerate(data):
        check_event(event, path, i)
        total += 1


# Determine files to validate
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = sorted(glob.glob("data/*.json"))

if not files:
    print("No JSON files found in data/")
    sys.exit(1)

for path in files:
    validate_file(path)

# Report
print(f"\nValidated {total} events across {len(files)} file(s)")

if warnings:
    print(f"\n⚠  {len(warnings)} warning(s):")
    for w in warnings[:20]:
        print(f"   {w}")
    if len(warnings) > 20:
        print(f"   ... and {len(warnings) - 20} more")

if errors:
    print(f"\n✗  {len(errors)} error(s):")
    for e in errors:
        print(f"   {e}")
    sys.exit(1)
else:
    print("✓  No errors found")
