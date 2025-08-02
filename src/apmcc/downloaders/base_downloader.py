"""Downloader for base Manual .apworld files from GitHub releases."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import aiohttp
import aiofiles

from ..utils.constants import (
    MANUAL_REPO_URL, 
    CACHE_DIR, 
    BASE_APWORLD_NAME,
    REQUEST_TIMEOUT,
    MAX_RETRIES
)
from ..utils.file_utils import ensure_directory


class BaseDownloader:
    """Downloads and caches the base Manual .apworld file."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the downloader with optional cache directory."""
        self.cache_dir = cache_dir or Path.cwd() / CACHE_DIR
        ensure_directory(self.cache_dir)
    
    async def get_latest_release_info(self) -> dict:
        """Get information about the latest release from GitHub API."""
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        
        for attempt in range(MAX_RETRIES):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(MANUAL_REPO_URL) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            print(f"GitHub API returned status {response.status}", file=sys.stderr)
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to fetch release info after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                    sys.exit(1)
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return {}
    
    async def download_file(self, url: str, destination: Path) -> None:
        """Download a file from URL to destination."""
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT * 3)  # Longer timeout for file downloads
        
        for attempt in range(MAX_RETRIES):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            async with aiofiles.open(destination, 'wb') as f:
                                async for chunk in response.content.iter_chunked(8192):
                                    await f.write(chunk)
                            return
                        else:
                            print(f"Download failed with status {response.status}", file=sys.stderr)
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to download file after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                    sys.exit(1)
                await asyncio.sleep(2 ** attempt)
    
    def get_cached_apworld_path(self) -> Path:
        """Get the path to the cached .apworld file."""
        return self.cache_dir / BASE_APWORLD_NAME
    
    def is_cached(self) -> bool:
        """Check if base .apworld file is already cached."""
        return self.get_cached_apworld_path().exists()
    
    async def download_base_apworld(self, force_download: bool = False) -> Path:
        """Download the latest Manual .apworld file."""
        cached_path = self.get_cached_apworld_path()
        
        # Check if we already have it cached and don't need to force download
        if self.is_cached() and not force_download:
            print(f"Using cached base .apworld: {cached_path}")
            return cached_path
        
        print("Fetching latest Manual release information...")
        release_info = await self.get_latest_release_info()
        
        if not release_info:
            print("Error: Could not fetch release information", file=sys.stderr)
            sys.exit(1)
        
        # Find the .apworld asset
        apworld_asset = None
        for asset in release_info.get('assets', []):
            if asset['name'].endswith('.apworld'):
                apworld_asset = asset
                break
        
        if not apworld_asset:
            print("Error: No .apworld file found in latest release", file=sys.stderr)
            sys.exit(1)
        
        download_url = apworld_asset['browser_download_url']
        file_size = apworld_asset.get('size', 0)
        
        print(f"Downloading {apworld_asset['name']} ({file_size} bytes)...")
        await self.download_file(download_url, cached_path)
        
        print(f"Downloaded base .apworld to: {cached_path}")
        return cached_path
    
    def clear_cache(self) -> None:
        """Clear the download cache."""
        if self.cache_dir.exists():
            import shutil
            shutil.rmtree(self.cache_dir)
            print("Cache cleared")


async def main():
    """CLI interface for the downloader."""
    downloader = BaseDownloader()
    await downloader.download_base_apworld(force_download=True)


if __name__ == "__main__":
    asyncio.run(main())