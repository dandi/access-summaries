[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17148099-blue)](https://doi.org/10.5281/zenodo.17148099)

# Dandiset access summaries

Summaries of access stats (full downloads &amp; streaming) for each Dandiset on the DANDI archive.

## Getting the data

A GZIP archive of the `content/` directory is published daily to the [`dist` branch](https://github.com/dandi/access-summaries/tree/dist) via a scheduled GitHub Actions workflow.

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
# Later, to update:
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

The examples below assume you have already extracted the archive into the current directory (so that `content/` exists locally).
They use [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/), which you can install with:

```bash
pip install pandas matplotlib
```

### Plot bytes sent over time for a single dandiset

```python
import pandas as pd
import matplotlib.pyplot as plt

dandiset_id = "000003"
df = pd.read_csv(f"content/summaries/{dandiset_id}/by_day.tsv", sep="\t", parse_dates=["date"])
df = df.sort_values("date")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["date"], df["bytes_sent"] / 1e9)
ax.set_xlabel("Date")
ax.set_ylabel("Data transferred (GB)")
ax.set_title(f"Daily data transfer for dandiset {dandiset_id}")
plt.tight_layout()
plt.show()
```

### Plot top regions accessing a dandiset

```python
import pandas as pd
import matplotlib.pyplot as plt

dandiset_id = "000003"
df = pd.read_csv(f"content/summaries/{dandiset_id}/by_region.tsv", sep="\t")
top = df.nlargest(15, "bytes_sent")

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top["region"], top["bytes_sent"] / 1e9)
ax.invert_yaxis()
ax.set_xlabel("Data transferred (GB)")
ax.set_title(f"Top regions by data transfer for dandiset {dandiset_id}")
plt.tight_layout()
plt.show()
```

### Compare top dandisets by total bytes sent

```python
import json
import pandas as pd
import matplotlib.pyplot as plt

with open("content/totals.json") as f:
    totals = json.load(f)

df = pd.DataFrame(
    [{"dandiset": k, "bytes_sent": v["total_bytes_sent"]} for k, v in totals.items()]
)
top = df.nlargest(20, "bytes_sent")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top["dandiset"], top["bytes_sent"] / 1e12)
ax.invert_yaxis()
ax.set_xlabel("Data transferred (TB)")
ax.set_title("Top 20 dandisets by total data transfer")
plt.tight_layout()
plt.show()
```

### Geographic access map

Uses the `region_codes_to_coordinates.yaml` file to place access counts on a world map.
Requires [PyYAML](https://pyyaml.org/) and [cartopy](https://scitools.org.uk/cartopy/docs/latest/) in addition to pandas and matplotlib:

```bash
pip install pyyaml cartopy
```

```python
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

dandiset_id = "000003"

# Load region access data
df = pd.read_csv(f"content/summaries/{dandiset_id}/by_region.tsv", sep="\t")

# Load coordinates lookup
with open("content/region_codes_to_coordinates.yaml") as f:
    coords = yaml.safe_load(f)

# Build a DataFrame with lat/lon
rows = []
for _, row in df.iterrows():
    if row["region"] in coords:
        c = coords[row["region"]]
        rows.append({"region": row["region"], "bytes_sent": row["bytes_sent"],
                     "lat": c["latitude"], "lon": c["longitude"]})
geo = pd.DataFrame(rows)

# Plot
fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN, facecolor="white")
ax.add_feature(cfeature.BORDERS, linewidth=0.3)
ax.set_global()

sc = ax.scatter(
    geo["lon"], geo["lat"],
    s=geo["bytes_sent"] / geo["bytes_sent"].max() * 300,
    c=geo["bytes_sent"],
    cmap="YlOrRd",
    alpha=0.7,
    transform=ccrs.PlateCarree(),
)
plt.colorbar(sc, ax=ax, label="Bytes sent", shrink=0.5)
ax.set_title(f"Geographic distribution of data transfers for dandiset {dandiset_id}")
plt.tight_layout()
plt.show()
```
