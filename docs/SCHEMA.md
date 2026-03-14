# Schema Reference

Full documentation for all fields in the dataset.

---

## Top-level fields

| Field | Type | Coverage | Description |
|-------|------|----------|-------------|
| `_id` | string | ~99% | Unique identifier for the event. Format varies: some are slugs (`yamato_damashii_2_2007`), some are short random IDs (`tfmekb_9`). |
| `Subject` | string | 100% | Event name/title. |
| `Start Date` | string | 100% | Start date in `YYYYMMDD` format. |
| `End Date` | string | 100% | End date in `YYYYMMDD` format. Same as Start Date for single-day events. |
| `Start Time` | string | ~45% | Start time, free-text (e.g. `"10:00"`, `"8:00 AM"`). Empty if unknown. |
| `End Time` | string | ~21% | End time, free-text. Empty if unknown. |
| `Location` | string | ~99% | Venue name and/or address as written. |
| `location_city` | string | ~78% | Normalized city name. |
| `location_address` | string | ~72% | Full address. |
| `location_coordinate` | string | ~64% | GPS coordinates as `"lat, lng"` string. |
| `location_gmaps` | string | ~66% | Google Maps URL. |
| `Online/Offline` | string | ~99% | `"Offline"`, `"Online"`, or `"Hybrid"`. |
| `status` | string | ~99% | Event status. See values below. |
| `attended` | string | ~50% | Personal attendance log. `"Yes"`, `"No"`, or blank. |
| `links` | array | ~98% | Array of URLs (social media, event pages, ticketing). May include empty strings. |
| `Comment` | string | ~92% | Free-text notes, personal memories, or raw source text. |
| `Content` | object | ~22% | Structured event details. See Content fields below. |
| `Reminder On/Off` | string | ~50% | Calendar reminder flag. `"Yes"` or `"No"`. |
| `Reminder Date` | string | ~11% | Reminder date in `YYYYMMDD` format. |
| `Reminder Time` | string | ~11% | Reminder time. |
| `Importance` | string | ~12% | Calendar importance flag. `"High"`, `"Normal"`, or empty. |

### `status` values

| Value | Meaning |
|-------|---------|
| `Finished` | Event completed successfully |
| `Completed` | Synonym for Finished |
| `Cancelled` | Event was cancelled |
| `Postponed` | Event was postponed (may have new date in Content) |
| `Disbanded` | Organizing group disbanded |
| `Dropped` | Event dropped without further information |
| `Scheduled` | Upcoming/planned event |
| *(blank)* | Unknown |

---

## Content field

The `Content` field is a flexible object containing structured event details. Not all events have it, and field names vary. The most common fields are:

### Identity & organization

| Field | Description |
|-------|-------------|
| `organizer` / `Organizer` / `organized_by` | Organizing group or individual |
| `presenter` | Presenting organization (sometimes different from organizer) |
| `co_organizer` | Co-organizing group |
| `theme` | Event theme |
| `edition` | Edition number (for recurring events) |
| `event_type` | Category label (e.g. `"Cosplay Festival"`, `"Cultural Festival"`) |
| `event_description` | Description of the event |
| `source` | Source citation (e.g. `"Animonster 63 - Juni 2004"`) |
| `sumber` | Indonesian-language source citation |

### People

| Field | Description |
|-------|-------------|
| `performers` / `Performers` | Performer list |
| `guest_star` / `Guest Star` / `guest_stars` | Guest star list (many variants) |
| `mc` / `MC` / `emcee` | Master of ceremony |
| `judges` / `Judges` | Competition judges |
| `contact_person` / `CP` | Contact person(s) |
| `organizers` | List of organizing members |

### Schedule & logistics

| Field | Description |
|-------|-------------|
| `Rundown` / `rundown` / `schedule` | Event rundown or schedule |
| `HTM` / `htm` / `ticket_price` / `harga_tiket` | Ticket pricing |
| `entry_fee` / `admission` | Competition/event entry fee |
| `registration` | Registration details |
| `registration_link` | Registration URL |

### Activities & competitions

| Field | Description |
|-------|-------------|
| `activities` / `Activities` | List of activities |
| `competitions` | Competition details |
| `prizes` / `prize_pool` | Prize information |
| `winners` / `pemenang` | Competition results |
| `cosplay_competition` | Cosplay competition details |

### Media & partnerships

| Field | Description |
|-------|-------------|
| `media_partner` / `Media Partner` | Media partners |
| `sponsors` / `Sponsors` | Sponsors |
| `supported_by` / `Supported by` | Supporting organizations |
| `hashtags` | Official event hashtags |
| `social_media` | Social media handles |

### Experience & review

| Field | Description |
|-------|-------------|
| `review` / `Review` | Post-event review |
| `laporan_acara` | Event report |
| `testimoni` | Testimonials |
| `pengalaman_day1` / `pengalaman_day2` | Personal day-by-day experience notes |
| `memories` | Memory notes |

---

## Notes on field consistency

The dataset evolved organically over many years. As a result:

- **Field names are not fully normalized** — the same concept may appear as `guest_star`, `Guest Star`, `GUEST STAR`, or `guestStars`. Scripts that need performer data should check multiple variants.
- **Dates are always strings** in `YYYYMMDD` format, not ISO dates. Parse with `datetime.strptime(d, "%Y%m%d")`.
- **Coordinates** are `"lat, lng"` strings, not separate fields. Split on comma to get float values.
- **`links` arrays** may contain empty strings `""` — filter before use.
- **Content field names are in mixed Indonesian and English** — this reflects the bilingual nature of the community.

---

## Parsing examples

```python
from datetime import datetime

# Parse date
date_str = "20070901"
dt = datetime.strptime(date_str, "%Y%m%d")

# Parse coordinates
coord_str = "-6.8921, 107.6078"
lat, lng = map(float, coord_str.split(","))

# Clean links
links = [l for l in event.get("links", []) if l and l.strip()]

# Get guest stars (multi-variant)
def get_guest_stars(event):
    c = event.get("Content") or {}
    for key in ["guest_stars", "guest_star", "Guest Star", "Guest Stars",
                "GUEST STAR", "GUEST STARS", "guestStars", "bintang_tamu"]:
        val = c.get(key)
        if val:
            return val
    return None
```
