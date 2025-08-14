#!/usr/bin/env python3
"""
Shared utilities for creating DANDI access maps.
"""

import pandas as pd
from pathlib import Path
import json
import yaml

# Single dictionary for all color specifications
COLOR_SPECS = {
    'low': {
        'fill': '#26c6da',       # Cyan
        'stroke': '#0097a7',     # Dark cyan
        'name': 'Cyan',
        'label': '< 10 MB',
        'size': 20
    },
    'medium': {
        'fill': '#66bb6a',       # Light green
        'stroke': '#388e3c',     # Dark green
        'name': 'Green',
        'label': '10 MB - 10 GB',
        'size': 40
    },
    'high': {
        'fill': '#ffca28',       # Yellow
        'stroke': '#f57f17',     # Dark yellow
        'name': 'Yellow',
        'label': '10 GB - 10 TB',
        'size': 60
    },
    'very-high': {
        'fill': '#ff7043',       # Orange-red
        'stroke': '#d84315',     # Dark orange-red
        'name': 'Orange',
        'label': '> 10 TB',
        'size': 80
    }
}


def load_region_data():
    """Load and aggregate data from all by_region.tsv files."""
    region_totals = {}
    
    # Find all by_region.tsv files
    summaries_dir = Path('../content/summaries')
    
    if not summaries_dir.exists():
        print("Error: content/summaries directory not found!")
        return {}
    
    for dandiset_dir in summaries_dir.iterdir():
        if dandiset_dir.is_dir():
            region_file = dandiset_dir / 'by_region.tsv'
            if region_file.exists():
                try:
                    df = pd.read_csv(region_file, sep='\t')
                    
                    for _, row in df.iterrows():
                        region = row['region']
                        bytes_sent = row['bytes_sent']
                        
                        # Skip non-geographic regions but keep detailed regions
                        non_geographic = ['GitHub', 'VPN', 'bogon', 'unknown']
                        if region in non_geographic:
                            continue
                            
                        region_totals[region] = region_totals.get(region, 0) + bytes_sent
                            
                except Exception as e:
                    print(f"Error processing {region_file}: {e}")
                    continue
    
    return region_totals


def extract_country_code(region):
    """Extract country code from region string."""
    # Skip non-geographic regions
    non_geographic = ['AWS/', 'GCP/', 'GitHub', 'VPN', 'bogon', 'unknown']
    if any(region.startswith(ng) for ng in non_geographic):
        return None
    
    # Extract country code (everything before the first '/')
    if '/' in region:
        return region.split('/')[0]
    else:
        # Handle cases where region is just a country code
        return region


def load_country_data():
    """Load and aggregate data by country from all by_region.tsv files."""
    country_totals = {}
    
    # Get region data first
    region_data = load_region_data()
    
    # Aggregate by country
    for region, bytes_sent in region_data.items():
        country = extract_country_code(region)
        if country:
            country_totals[country] = country_totals.get(country, 0) + bytes_sent
    
    return country_totals


def load_coordinates():
    """Load coordinate data from YAML file."""
    try:
        with open('../content/region_codes_to_coordinates.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: region_codes_to_coordinates.yaml file not found!")
        return {}
    except yaml.YAMLError:
        print("Error: Invalid YAML in region_codes_to_coordinates.yaml!")
        return {}


def load_country_mapping():
    """Load country mapping from JSON file."""
    try:
        with open('country_mapping.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: country_mapping.json file not found!")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON in country_mapping.json!")
        return {}


def format_bytes(bytes_value):
    """Format bytes in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} EB"


def get_point_color_and_size(bytes_value):
    """Get color and size for point based on download volume."""
    # Color thresholds
    mb_10 = 10 * 1024 * 1024  # 10 MB
    gb_10 = 10 * 1024 * 1024 * 1024  # 10 GB
    tb_10 = 10 * 1024 * 1024 * 1024 * 1024  # 10 TB
    
    if bytes_value < mb_10:
        return COLOR_SPECS['low']['fill'], COLOR_SPECS['low']['stroke'], COLOR_SPECS['low']['size']
    elif bytes_value < gb_10:
        return COLOR_SPECS['medium']['fill'], COLOR_SPECS['medium']['stroke'], COLOR_SPECS['medium']['size']
    elif bytes_value < tb_10:
        return COLOR_SPECS['high']['fill'], COLOR_SPECS['high']['stroke'], COLOR_SPECS['high']['size']
    else:
        return COLOR_SPECS['very-high']['fill'], COLOR_SPECS['very-high']['stroke'], COLOR_SPECS['very-high']['size']
