# Data Manipulation Scripts

This directory contains Python scripts used to web scrape and process data into JSON format for the Azeroth Tour Guide project. These scripts were developed iteratively to build and refine the `regions.json` dataset.

## Scripts Overview

The scripts were executed in the following order to transform and enhance the data:

1. **`convert_regions.py`**  
   Converts initial region data into a standardized JSON format. I had it as a markdown list originally. 
2. **`scrape_info.py`**  
   Scrapes additional details from web sources to enrich the dataset.
3. **`add_links.py`**  
   Adds hyperlinks to related resources in the JSON data. I then realized they were the old wiki.
4. **`check_links.py`**  
   Changes to the new wiki, validates the links for accuracy (favoring _(Classic) links).
5. **`redo_ids.py`**  
   I deleted a few items from the JSON, so this reassigns region IDs for consistency.
6. **`fix_factions.py`**  
   Data was missing proper faction listings, so this adjusts faction-related data, but also adds template activities and screenshots.

> **Note**: These were written as separate steps because each task revealed new requirements. A single script could consolidate this in the future, but this modular approach made development manageable.

## Running the Scripts

### Prerequisites
- Python 3.12 or higher.
- Poetry (version 2.1.1 or later) for dependency management.

### Setup
1. Navigate to the `scripts/` directory (one level up):
   ```bash
   cd ../scripts
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
   This sets up a virtual environment with `beautifulsoup4` and `requests` as specified in pyproject.toml.

### Execution

Run each script individually from the scripts/ directory:
```bash
poetry run python data-manipulation/convert_regions.py
poetry run python data-manipulation/scrape_info.py
poetry run python data-manipulation/add_links.py
poetry run python data-manipulation/check_links.py
poetry run python data-manipulation/redo_ids.py
poetry run python data-manipulation/fix_factions.py
```
- Working Directory: Scripts assume data/ is at ../backend/data/. TODO: Adjust paths (e.g., using pathlib as in the backend fix).

