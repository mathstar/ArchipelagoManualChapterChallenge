"""File utility functions for the application."""

import json
import shutil
import zipfile
from pathlib import Path
from typing import Any, Dict


def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def safe_remove(path: Path) -> None:
    """Safely remove a file or directory."""
    if path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def write_json(data: Dict[str, Any], file_path: Path) -> None:
    """Write data to a JSON file with proper formatting."""
    ensure_directory(file_path.parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(file_path: Path) -> Dict[str, Any]:
    """Read data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_zip(zip_path: Path, extract_to: Path) -> None:
    """Extract a zip file to the specified directory."""
    ensure_directory(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def create_zip(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from a directory."""
    ensure_directory(zip_path.parent)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(source_dir)
                zip_ref.write(file_path, arc_name)


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file from source to destination."""
    ensure_directory(dst.parent)
    shutil.copy2(src, dst)