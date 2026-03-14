# Contributing

Thank you for helping grow this archive! There are several ways to contribute.

---

## Ways to contribute

### 1. Add a missing event
Use the [New Event issue template](.github/ISSUE_TEMPLATE/new_event.md) or submit a Pull Request directly.

### 2. Correct existing data
Found a wrong date, name, or location? Open an [issue](.github/ISSUE_TEMPLATE/correction.md) or submit a PR with the fix.

### 3. Fill in Content fields
Many events have basic metadata but no structured Content. If you have details about a specific event (performers, guest stars, ticket prices, rundown, winners), you can add them.

### 4. Add documentation links
Photos, news articles, social media posts, or forum threads that document a specific event can be added to the `links` array.

---

## Submitting a Pull Request

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/indonesian-jculture-archive.git
cd indonesian-jculture-archive
```

### Adding or editing events

1. Open the relevant year file in `data/` (e.g. `data/2015.json`)
2. Add or edit the event object
3. Validate your changes: `python scripts/validate.py`
4. Commit and open a PR

### Event object format

At minimum, a new event needs:

```json
{
  "_id": "unique-id-here",
  "Subject": "Event Name",
  "Start Date": "YYYYMMDD",
  "End Date": "YYYYMMDD",
  "Location": "Venue name",
  "location_city": "City",
  "Online/Offline": "Offline",
  "status": "Finished",
  "attended": "",
  "links": [],
  "Comment": "",
  "Content": {}
}
```

### ID format
Use lowercase slugs: `event-name-year` (e.g. `nihon-no-matsuri-2015`). If unsure, use the auto-generator: `python scripts/generate_id.py "Event Name" 2015`.

### Dates
Always use `YYYYMMDD` string format. Example: `"20150912"`.

---

## Data standards

- **Language**: Field values may be in Indonesian or English. Do not translate existing values.
- **Sources**: Always include a `Content.source` field if you know where the data comes from.
- **Duplicates**: Search the dataset before adding — use `python scripts/search.py "event name"`.
- **Content fields**: Use the field names documented in [`docs/SCHEMA.md`](docs/SCHEMA.md). Do not invent new top-level field names; add structured data inside `Content`.

---

## Updating the dataset (for maintainers)

When new data is added:

```bash
# 1. Validate all files
python scripts/validate.py

# 2. Regenerate statistics
python scripts/stats.py

# 3. Update CHANGELOG.md with version and summary
# 4. Commit with message: "data: add N events (YYYY-MM-DD)"
```

See the full update workflow in [`docs/UPDATE_WORKFLOW.md`](docs/UPDATE_WORKFLOW.md).

---

## What NOT to include

- Events not related to Japanese pop-culture or the J-culture community
- Private or personal events not intended for public documentation
- Unverified rumor-sourced data without a citation

---

## Questions?

Open a [Discussion](../../discussions) or reach out via the contact information in the repository profile.
