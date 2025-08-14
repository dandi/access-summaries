# DANDI Access Visualization Tools

This repository contains tools for creating geographic visualizations of DANDI data access patterns, including choropleth maps and scatter plots showing data download patterns by country and region.

## Features

- **Choropleth Maps**: Country-level data visualization with color-coded regions
- **Scatter Maps**: Region-level visualization with proportional point sizes
- **Cartopy Integration**: Professional cartographic projections and map features
- **Centralized Styling**: Consistent color schemes across all visualizations
- **Publication Quality**: High-resolution SVG and PDF outputs
- **Flexible Scaling**: Linear and logarithmic scale options


## Installation

Navigate to the visualization directory and install dependencies:

```bash
cd visualization
pip install -r requirements.txt
```

### Dependencies
- **pandas**: Data manipulation
- **matplotlib**: Plotting framework
- **numpy**: Numerical operations
- **cartopy**: Geographic projections and mapping
- **pyyaml**: YAML configuration file parsing

## Usage

### Choropleth Maps (Country-level)

```bash
cd visualization

# Basic usage (linear scale)
python create_choropleth.py

# With logarithmic scale (recommended)
python create_choropleth.py --log-scale

# Custom output file
python create_choropleth.py --log-scale --output my_choropleth.svg

# View help
python create_choropleth.py --help
```

### Scatter Maps (Region-level)

```bash
cd visualization

# Basic usage
python create_scatter_map.py

# Custom output file
python create_scatter_map.py --output my_scatter_map.svg

# View help
python create_scatter_map.py --help
```

## Output Files

Both scripts generate:
- **SVG files**: Vector format for publications (300 DPI equivalent)
- **PDF files**: Alternative format for presentations
- **Console output**: Summary statistics and processing information

## Visualization Features

### Choropleth Maps
- **Color-coded countries** based on total download volume
- **Logarithmic/linear scales** to handle wide data ranges
- **Natural Earth integration** for professional cartography
- **Country name matching** handles common naming variations

### Scatter Maps
- **Color and size coding**: Points show both location and download volume
- **Proportional legends**: Legend dot sizes match actual scatter plot
- **Regional precision**: Sub-country level geographic detail
- **Categorized display**: Four download volume categories with counts

## Data Processing

The tools automatically:
1. **Scan** all `content/summaries/*/by_region.tsv` files
2. **Extract** geographic regions from access data
3. **Exclude** non-geographic regions (AWS/, GCP/, GitHub, VPN, etc.)
4. **Aggregate** data by country (choropleth) or region (scatter)