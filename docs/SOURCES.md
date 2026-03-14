# Data Sources & Methodology

---

## Primary sources

### Animonster magazine
The most significant primary source for events from 2000–2009. *Animonster* was Indonesia's leading anime and J-culture magazine, publishing event coverage, previews, and reviews.

Events sourced from Animonster are cited in the `Content.source` field, e.g.:
- `"Animonster 63 - Juni 2004"`
- `"Animonster 74 - Mei 2005"`

### Personal attendance records
The archive owner attended many events directly. These are marked with `attended: "Yes"` and often contain first-hand `Comment` notes and `Content` detail.

### Community documentation
Event flyers, forum posts (wgaul.com, kaskus), and community websites captured at time of event or retroactively documented.

### Social media
Instagram and Facebook pages of event organizers, captured via links in the `links` field. Primary source for 2017–present events.

### Secondary references
Academic papers, news articles, and institutional websites used to verify or supplement event records. Cited in `Content.source` or `Content.sumber`.

---

## Methodology

### Event selection criteria
An event is included if it meets at least one of:
- Primarily Japanese pop-culture themed (anime, manga, cosplay, J-music, Japanese language/culture)
- Organized by or for a J-culture community in Indonesia
- Historically significant to the development of J-culture in Indonesia

### Data entry
Events are entered as structured JSON. The `Content` field contains whatever information was available at time of entry — this varies significantly by era and source quality.

### ID format
`_id` values follow no single convention. Older entries use descriptive slugs; newer entries may use short random IDs. IDs are unique within the dataset.

### Date format
All dates use `YYYYMMDD` string format for consistency and easy sorting.

### Coverage gaps
- **Pre-2000**: Very limited. Only the 1973 Unpad event is currently documented.
- **2000–2003**: Partial. Primarily reconstructed from Animonster archive.
- **2020–2021**: Partial. COVID-19 severely reduced events; online events are inconsistently captured.
- **Content field**: Only ~22% of events have structured Content data. The rest have basic metadata only.

---

## Known limitations

1. **Jakarta-centric bias in early years** — most documented events from 2000–2010 are in Jakarta, Bandung, and Depok. Regional events outside Java are underrepresented until 2015+.

2. **Social media sourcing bias (2022+)** — the rapid increase in events from 2022 reflects growth in social media documentation, not necessarily a proportional growth in actual events.

3. **Name variants** — the same event may appear under slightly different names (organizer's name vs. public name, Indonesian vs. Japanese title). Deduplication is ongoing.

4. **Content field inconsistency** — field names within `Content` are not fully normalized. The same data type (e.g. guest stars) may appear under 20+ different key names.

---

## Contributing sources

If you have documentation for events not yet in the archive — especially pre-2010 events — see [CONTRIBUTING.md](../CONTRIBUTING.md).

Particularly valuable:
- Scans or photos of *Animonster* event coverage pages
- Screenshots or archives of now-deleted forum posts (kaskus, wgaul, friendster)
- Event programs or flyers (physical or digital)
- Photography from events
