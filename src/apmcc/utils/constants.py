"""Constants used throughout the application."""

# GitHub URLs
MANUAL_REPO_URL = "https://api.github.com/repos/ManualForArchipelago/Manual/releases/latest"
MANUAL_RELEASES_URL = "https://github.com/ManualForArchipelago/Manual/releases/latest"

# File extensions and names
APWORLD_EXTENSION = ".apworld"
CACHE_DIR = ".apmcc_cache"
BASE_APWORLD_NAME = "Manual.apworld"

# Archipelago Manual file structure
MANUAL_FILES = {
    "items": "data/items.json",
    "locations": "data/locations.json", 
    "regions": "data/regions.json",
    "hooks": "hooks.py"
}

# HTTP settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3