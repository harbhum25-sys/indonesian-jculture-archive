"""
update_dataset.py — Merge new or updated events into the dataset.

This is the main script for updating the archive when new data arrives.
It handles adding new events, updating existing ones, and generating
a summary of what changed.

Usage:
    # Merge a single new JSON file (e.g. a new year file)
    python scripts/update_dataset.py --input new_data/2026.json

    # Merge a zip containing multiple year files
    python scripts/update_dataset.py --zip new_dataset.zip

    # Dry run — show what would change without writing
    python scripts/update_dataset.py --zip new_dataset.zip --dry-run

    # Replace entire dataset from zip (full refresh)
    python scripts/update_dataset.py --zip new_dataset.zip --replace
"""

import json
import glob
import sys
import shutil
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

parser = argparse.ArgumentParser(description="Update the j-culture dataset")
parser.add_argument("--input", help="Single JSON file to merge")
parser.add_argument("--zip", help="ZIP archive containing year JSON files")
parser.add_argument("--replace", action="store_true",
                    help="Replace entire dataset (full refresh, not incremental merge)")
parser.add_argument("--dry-run", action="store_true",
                    help="Show changes without writing to disk")
args = parser.parse_args()

DATA_DIR = Path("data")
BACKUP_DIR = Path(".backups")


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_existing():
    """Load all current events keyed by _id."""
    by_id = {}
    by_year = defaultdict(list)
    for f in sorted(glob.glob(str(DATA_DIR / "*.json"))):
        yr = Path(f).stem
        with open(f, encoding="utf-8") as fp:
            events = json.load(fp)
        for e in events:
            eid = e.get("_id")
            if eid:
                by_id[eid] = e
        by_year[yr] = events
    return by_id, by_year


def get_year(event):
    d = str(event.get("Start Date", ""))
    return d[:4] if len(d) >= 4 else "unknown"


def backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / ts
    dest.mkdir(parents=True, exist_ok=True)
    for f in glob.glob(str(DATA_DIR / "*.json")):
        shutil.copy(f, dest / Path(f).name)
    print(f"  Backup saved to {dest}")
    return dest


# ── Load incoming data ──────────────────────────────────────────────────────────

incoming = []

if args.input:
    path = Path(args.input)
    if not path.exists():
        print(f"File not found: {args.input}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        incoming = json.load(f)
    print(f"Loaded {len(incoming)} events from {args.input}")

elif args.zip:
    zip_path = Path(args.zip)
    if not zip_path.exists():
        print(f"ZIP not found: {args.zip}")
        sys.exit(1)
    with zipfile.ZipFile(zip_path) as zf:
        json_files = [n for n in zf.namelist() if n.endswith(".json")]
        for name in sorted(json_files):
            with zf.open(name) as f:
                events = json.load(f)
                incoming.extend(events)
    print(f"Loaded {len(incoming)} events from {len(json_files)} files in {args.zip}")

else:
    print("Error: specify --input or --zip")
    parser.print_help()
    sys.exit(1)


# ── Full replace mode ───────────────────────────────────────────────────────────

if args.replace:
    # Group incoming by year
    by_year = defaultdict(list)
    for e in incoming:
        yr = get_year(e)
        if yr != "unknown":
            by_year[yr].append(e)

    print(f"\nFull replace: {len(incoming)} events across {len(by_year)} year files")
    for yr, evs in sorted(by_year.items()):
        print(f"  {yr}: {len(evs)} events")

    if not args.dry_run:
        backup()
        for yr, evs in by_year.items():
            out = DATA_DIR / f"{yr}.json"
            with open(out, "w", encoding="utf-8") as f:
                json.dump(evs, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Dataset replaced with {len(incoming)} events")
    else:
        print("\n[dry-run] No files written")
    sys.exit(0)


# ── Incremental merge mode ──────────────────────────────────────────────────────

existing_by_id, existing_by_year = load_existing()
existing_total = sum(len(v) for v in existing_by_year.values())

added = []
updated = []
unchanged = []
no_id = []

for e in incoming:
    eid = e.get("_id")
    if not eid:
        no_id.append(e)
        continue

    if eid not in existing_by_id:
        added.append(e)
    elif e != existing_by_id[eid]:
        updated.append(e)
    else:
        unchanged.append(e)

# Summary
print(f"\nExisting dataset: {existing_total} events")
print(f"Incoming events : {len(incoming)}")
print(f"\nChanges:")
print(f"  ✚ Added   : {len(added)}")
print(f"  ✎ Updated : {len(updated)}")
print(f"  — Unchanged: {len(unchanged)}")
if no_id:
    print(f"  ⚠ No _id  : {len(no_id)} (skipped)")

if added:
    print(f"\nNew events:")
    for e in added:
        print(f"  {e.get('Start Date','')} | {e.get('Subject','')} | {e.get('location_city','')}")

if updated:
    print(f"\nUpdated events:")
    for e in updated:
        print(f"  {e.get('_id','')} | {e.get('Subject','')}")

if not added and not updated:
    print("\nNo changes — dataset is already up to date.")
    sys.exit(0)

if args.dry_run:
    print("\n[dry-run] No files written")
    sys.exit(0)

# Apply changes
print("\nApplying changes...")
backup()

# Merge into year buckets
for e in added + updated:
    yr = get_year(e)
    eid = e.get("_id")
    if yr == "unknown" or not eid:
        continue
    # Remove old version if updating
    existing_by_year[yr] = [x for x in existing_by_year[yr] if x.get("_id") != eid]
    existing_by_year[yr].append(e)

# Sort each year by date and write
new_total = 0
for yr, evs in sorted(existing_by_year.items()):
    evs_sorted = sorted(evs, key=lambda x: str(x.get("Start Date", "")))
    out = DATA_DIR / f"{yr}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(evs_sorted, f, ensure_ascii=False, indent=2)
    new_total += len(evs_sorted)

print(f"\n✓ Done — dataset updated")
print(f"  Before: {existing_total} events")
print(f"  After : {new_total} events (+{new_total - existing_total})")
print(f"\nNext steps:")
print(f"  1. Run: python scripts/validate.py")
print(f"  2. Update CHANGELOG.md with version and summary")
print(f"  3. git add data/ CHANGELOG.md && git commit -m 'data: add {len(added)} events'")
print(f"  4. git push")
