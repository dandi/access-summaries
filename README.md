[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17148099-blue)](https://doi.org/10.5281/zenodo.17148099)

# Dandiset access summaries

Summaries of access stats (full downloads &amp; streaming) for each Dandiset on the DANDI archive.
This is the underlying data for the [DANDI usage dashboard](https://usage.dandiarchive.org/).

## Getting the data

A GZIP archive of the `content/` directory is published daily to the [`dist`](https://github.com/dandi/access-summaries/tree/dist) branch via a scheduled GitHub Actions workflow.

### One-time download

Use one of the following methods for a one-time snapshot of the data.

#### Using `curl`

```bash
curl -fsSL https://github.com/dandi/access-summaries/raw/dist/content.tar.gz | tar -xz
```

#### Using Python `urllib`

```python
import io
import tarfile
import urllib.request

url = "https://github.com/dandi/access-summaries/raw/dist/content.tar.gz"
with urllib.request.urlopen(url) as response:
    with tarfile.open(fileobj=io.BytesIO(response.read()), mode="r:gz") as tar:
        tar.extractall(filter="data")  # requires Python 3.12+; omit filter= on older versions
```

### Recurring / up-to-date usage

For recurring usage where you want to stay up to date with the latest data, clone the repository and pull regularly to get the newest `content/`:

```bash
git clone https://github.com/dandi/access-summaries.git
cd access-summaries

# Keep up-to-date over time with:
git pull
```

## Data layout

After extracting the archive, the `content/` directory has the following structure:

```
content/
├── archive_totals.json           # Archive-wide totals
├── totals.json                   # Per-dandiset totals
├── region_codes_to_coordinates.yaml  # Lat/lon for each region code
└── summaries/
    └── {dandiset_id}/
        ├── by_day.tsv            # bytes_sent per day
        ├── by_region.tsv         # bytes_sent per region
        ├── by_asset.tsv          # bytes_sent per asset (all-time)
        ├── by_asset_per_week.tsv # bytes_sent per asset per week
        └── by_asset_type_per_week.tsv  # bytes_sent per asset type per week
```

## Usage examples

The example below assumes you have already extracted the archive into the current directory (so that `content/` exists locally).
It uses [matplotlib](https://matplotlib.org/), which you can install with:

```bash
pip install matplotlib
```

### Plot bytes sent over time for a single dandiset

```python
import csv
from datetime import datetime
import matplotlib.pyplot as plt

dandiset_id = "000003"
dates, bytes_sent = [], []
with open(f"content/summaries/{dandiset_id}/by_day.tsv", newline="") as f:
    for row in sorted(csv.DictReader(f, delimiter="\t"), key=lambda r: r["date"]):
        dates.append(datetime.strptime(row["date"], "%Y-%m-%d"))
        bytes_sent.append(int(row["bytes_sent"]) / 1e9)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(dates, bytes_sent)
ax.set_xlabel("Date")
ax.set_ylabel("Data transferred (GB)")
ax.set_title(f"Daily data transfer for dandiset {dandiset_id}")
plt.tight_layout()
plt.show()
```
