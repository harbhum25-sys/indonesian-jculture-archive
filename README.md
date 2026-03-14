# Indonesian J-Culture Event Archive

**Structured dataset documenting the history of Japanese pop-culture events in Indonesia (1973–2026).**

[![Events](https://img.shields.io/badge/events-6%2C145-teal?style=flat-square)](data/)
[![Years](https://img.shields.io/badge/coverage-1973–2026-blue?style=flat-square)](data/)
[![Cities](https://img.shields.io/badge/cities-183-orange?style=flat-square)](data/)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-green?style=flat-square)](LICENSE)

---

## About

This archive documents the growth of Japanese pop-culture communities and events across Indonesia — anime conventions, cosplay gatherings, bunkasai (cultural festivals), idol performances, J-music concerts, and more.

Data collection began in 2017, combining personal attendance records, magazine archives (*Animonster*), community documentation, and social media sources. The earliest recorded event is **Nihongo Nihon Bunkasai** at Fakultas Sastra Unpad in 1973 — widely considered the origin of organized J-culture events in Indonesia.

> Built by a photographer and graphic designer focused on visual culture, cultural documentation, and digital archives.

---

## Dataset at a glance

| Metric | Count |
|--------|-------|
| Total events | **6,145** |
| Year span | **1973 – 2026** |
| JSON files | **28** (one per year) |
| Unique cities | **183** |
| Events with GPS coordinates | **3,944** |
| Events with Google Maps links | **3,966** |
| Events with rich Content data | **1,371** |

### Top cities

| City | Events | City | Events |
|------|--------|------|--------|
| Bandung | 841 | Jakarta | 246 |
| Surabaya | 262 | Yogyakarta | 225 |
| Jakarta Selatan | 252 | Bekasi | 163 |

<details>
<summary>Full per-year breakdown</summary>

| Year | Events | Year | Events |
|------|--------|------|--------|
| 1973 | 1 | 2014 | 49 |
| 2000 | 3 | 2015 | 66 |
| 2001 | 9 | 2016 | 61 |
| 2002 | 18 | 2017 | 75 |
| 2003 | 14 | 2018 | 63 |
| 2004 | 36 | 2019 | 101 |
| 2005 | 41 | 2020 | 35 |
| 2006 | 58 | 2021 | 10 |
| 2007 | 59 | 2022 | 772 |
| 2008 | 42 | 2023 | 2,088 |
| 2009 | 41 | 2024 | 1,704 |
| 2010 | 37 | 2025 | 467 |
| 2011 | 54 | 2026 | 115 |
| 2012 | 40 | | |
| 2013 | 86 | | |

</details>

---

## Repository structure

```
indonesian-jculture-archive/
├── README.md
├── LICENSE                         ← CC BY 4.0
├── CONTRIBUTING.md                 ← how to add or correct data
├── CHANGELOG.md                    ← version history
│
├── data/
│   ├── 1973.json                   ← 1 event (earliest recorded)
│   ├── 2000.json
│   ├── ...
│   └── 2026.json                   ← ongoing
│
├── docs/
│   ├── SCHEMA.md                   ← full field documentation
│   ├── SOURCES.md                  ← data sources & methodology
│   └── NOTABLE_SERIES.md           ← documented recurring event series
│
├── scripts/
│   ├── validate.py                 ← validate JSON structure
│   ├── stats.py                    ← generate dataset statistics
│   └── export_csv.py               ← export all events to CSV
│
└── examples/
    ├── query_by_city.py
    ├── query_by_performer.py
    └── filter_by_year.py
```

---

## Data format

Each year is a JSON array of event objects. Minimal example:

```json
{
  "_id": "yamato_damashii_2_2007",
  "Subject": "Yamato Damashii II",
  "Start Date": "20070901",
  "End Date": "20070902",
  "Location": "Kampus STBA Yapari-ABA",
  "location_city": "Bandung",
  "location_address": "Jl. Cihampelas No. 194, Bandung, Jawa Barat",
  "location_coordinate": "-6.8921, 107.6078",
  "location_gmaps": "https://maps.app.goo.gl/...",
  "Online/Offline": "Offline",
  "status": "Finished",
  "attended": "No",
  "links": ["https://instagram.com/yamatodamashii_official"],
  "Comment": "",
  "Content": {
    "organizer": "HIMADE STBA YAPARI-ABA",
    "performers": ["..."],
    "guest_stars": ["..."],
    "source": "..."
  }
}
```

Full field reference → [`docs/SCHEMA.md`](docs/SCHEMA.md)

---

## Quick start

```python
import json, glob

# Load all events
events = []
for f in sorted(glob.glob("data/*.json")):
    with open(f, encoding="utf-8") as fp:
        events.extend(json.load(fp))

print(f"{len(events)} events loaded")

# Filter by city
bandung = [e for e in events if e.get("location_city") == "Bandung"]

# Filter by year
events_2023 = [e for e in events
               if str(e.get("Start Date", "")).startswith("2023")]

# Get mappable events
geo = [e for e in events
       if (e.get("location_coordinate") or "").strip()]
print(f"{len(geo)} events with GPS coordinates")
```

More examples → [`examples/`](examples/)

---

## Notable recurring series

| Series | Location | Active | Editions |
|--------|----------|--------|----------|
| **Nihongo Nihon Bunkasai** | Unpad, Bandung | 1973– | Earliest documented predecessor of Bunkasai Unpad |
| **Yamato Damashii** | STBA YAPARI-ABA, Bandung | 2006–2025 | I–XVIII (annual) |
| **Gelar Jepang UI** | Universitas Indonesia, Depok | 1995–2023 | Ed. 1–29 |
| **Bunkasai UNPAD / Fesbukan** | PSBJ FIB UNPAD, Jatinangor | 1998– | Various names by era |
| **Anime Festival Asia Indonesia** | Jakarta Convention Center | 2013–2024 | Annual |
| **Jak-Japan Matsuri** | Gelora Bung Karno, Jakarta | 2009–2022 | Annual |

Full list → [`docs/NOTABLE_SERIES.md`](docs/NOTABLE_SERIES.md)

---

## Data quality

| Period | Coverage | Notes |
|--------|----------|-------|
| 1973 | Single event | Sourced from secondary references |
| 2000–2003 | Low | Primary source: *Animonster* magazine |
| 2004–2019 | Moderate–good | Mix of magazine, personal records, community docs |
| 2020–2021 | Partial | COVID-19 gap; online events partially captured |
| 2022–2025 | High volume, partial detail | Social media sourced; ~23% have rich Content data |
| 2026 | Ongoing | Events scheduled through year-end |

**`attended` field:** Personal log. `Yes` = personally attended, `No` = documented not attended, blank = unknown.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit new events or corrections.

**Priority areas:**
- Events from **1973–2010** (low coverage era)
- **Content field** data for 2022–2025 events
- **Bunkasai UNPAD** editions before 2001
- Photo/documentation links for any event

---

## License

© 2017–2025 under [Creative Commons Attribution 4.0 International](LICENSE).

Attribution:
> *Indonesian J-Culture Event Archive* — https://github.com/YOUR_USERNAME/indonesian-jculture-archive

### Citation

```bibtex
@dataset{indonesian_jculture_archive_2025,
  title     = {Indonesian J-Culture Event Archive},
  author    = {Harbhum},
  year      = {2025},
  publisher = {GitHub},
  url       = {https://github.com/harbhum25-sys/indonesian-jculture-archive},
  note      = {Structured dataset of Japanese pop-culture events in Indonesia, 1973--2026}
}
```

---

*Independent archival project. Not affiliated with any event organizer or institution.*
