# Update Workflow

Step-by-step guide for updating the dataset when new data is available.

---

## When you have a new ZIP file (most common)

This is the standard workflow when you receive a new version of the dataset as a `.zip` file.

```bash
# 1. Go to your local repo folder
cd indonesian-jculture-archive

# 2. Pull latest from GitHub first
git pull

# 3. Run the update script (dry run to preview changes)
python scripts/update_dataset.py --zip /path/to/_j_event_.zip --dry-run

# 4. If the preview looks correct, apply the update
python scripts/update_dataset.py --zip /path/to/_j_event_.zip

# 5. Validate the result
python scripts/validate.py

# 6. Check stats
python scripts/stats.py

# 7. Update CHANGELOG.md
#    Add a new entry at the top with: version, date, summary of changes

# 8. Commit and push
git add data/ CHANGELOG.md
git commit -m "data: add N events (YYYY-MM-DD)"
git push
```

---

## When you want a full dataset replace

Use this when you have a completely rebuilt dataset (not just additions):

```bash
python scripts/update_dataset.py --zip /path/to/_j_event_.zip --replace

# Then validate, update changelog, and push as above
```

---

## When adding a single event manually

1. Open `data/YYYY.json` for the relevant year
2. Add the new event object (follow the schema in `docs/SCHEMA.md`)
3. Make sure the `_id` is unique — check with:
   ```bash
   grep -r "your-new-id" data/
   ```
4. Validate and commit:
   ```bash
   python scripts/validate.py
   git add data/YYYY.json CHANGELOG.md
   git commit -m "data: add EventName (YYYY)"
   git push
   ```

---

## When correcting existing data

1. Find the event in the relevant `data/YYYY.json`
2. Edit the field(s)
3. Validate and commit:
   ```bash
   python scripts/validate.py
   git add data/YYYY.json CHANGELOG.md
   git commit -m "fix: correct EventName date/location/etc"
   git push
   ```

---

## Backups

The update script automatically creates a timestamped backup in `.backups/` before writing any changes. These are not committed to Git (`.gitignore` excludes them).

To restore from a backup:
```bash
cp .backups/20250314_103000/*.json data/
```

---

## Badge updates

The README badges (event count, cities) are hardcoded. After a significant update, update them manually in `README.md`:

```markdown
[![Events](https://img.shields.io/badge/events-6%2C145-teal...)](data/)
[![Cities](https://img.shields.io/badge/cities-183-orange...)](data/)
```

Run `python scripts/stats.py` to get the latest numbers.

---

## Releasing a new version

After any dataset update, add a version entry to `CHANGELOG.md`:

```markdown
## [1.1.0] 2025-04-01 — April update

- Added 47 new events (2025 Q1)
- Corrected 3 dates in 2007 records
- Added Content data for 12 events from 2011
```

Use semantic versioning:
- `PATCH` (1.0.x): corrections and small additions
- `MINOR` (1.x.0): 50+ new events or new year file
- `MAJOR` (x.0.0): schema changes or complete overhaul
