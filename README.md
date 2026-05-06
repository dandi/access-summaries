[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17148099-blue)](https://doi.org/10.5281/zenodo.17148099)

# Dandiset access summaries

Summaries of access stats (full downloads &amp; streaming) for each Dandiset on the DANDI archive.

## Downloading the data

A GZIP archive of the `content/` directory is published daily to the [`dist` branch](https://github.com/dandi/access-summaries/tree/dist) via a scheduled GitHub Actions workflow.

### Using `curl`

```bash
curl -fsSL https://github.com/dandi/access-summaries/raw/dist/content.tar.gz | tar -xz
```

### Using Python `urllib`

```python
import io
import tarfile
import urllib.request

url = "https://github.com/dandi/access-summaries/raw/dist/content.tar.gz"
with urllib.request.urlopen(url) as response:
    with tarfile.open(fileobj=io.BytesIO(response.read()), mode="r:gz") as tar:
        tar.extractall(filter="data")  # requires Python 3.12+; omit filter= on older versions
```
