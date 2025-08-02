"""Packager for creating .apworld files."""

import tempfile
from pathlib import Path
from typing import List, Optional

from ..models.game_definition import GameDefinition
from ..utils.file_utils import extract_zip, create_zip, ensure_directory, copy_file
from ..generators.locations import LocationsGenerator
from ..generators.items import ItemsGenerator
from ..generators.regions import RegionsGenerator
from ..generators.hooks import HooksGenerator


class ApworldPackager:
    """Packages game files into an .apworld archive."""
    
    def __init__(self, game_definition: GameDefinition, base_apworld_path: Path):
        """Initialize with game definition and base .apworld file."""
        self.game_definition = game_definition
        self.base_apworld_path = base_apworld_path
        self.generators = [
            LocationsGenerator(game_definition),
            ItemsGenerator(game_definition),
            RegionsGenerator(game_definition),
            HooksGenerator(game_definition)
        ]
    
    def create_apworld(self, output_path: Path) -> Path:
        """Create the final .apworld file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract base .apworld
            base_extracted = temp_path / "base"
            extract_zip(self.base_apworld_path, base_extracted)
            
            # Generate override files
            overrides_dir = temp_path / "overrides"
            ensure_directory(overrides_dir)
            
            # Create data directory for JSON files
            data_dir = overrides_dir / "data"
            ensure_directory(data_dir)
            
            generated_files = []
            for generator in self.generators:
                if generator.get_output_filename().endswith('.json'):
                    # JSON files go in data directory
                    output_file = generator.write_to_file(data_dir)
                else:
                    # Other files (like hooks.py) go in root
                    output_file = generator.write_to_file(overrides_dir)
                generated_files.append(output_file)
                print(f"Generated: {output_file.name}")
            
            # Copy generated files to base directory (overlaying)
            final_dir = temp_path / "final"
            self._copy_directory(base_extracted, final_dir)
            self._copy_directory(overrides_dir, final_dir)
            
            # Create the final .apworld
            ensure_directory(output_path.parent)
            create_zip(final_dir, output_path)
            
            print(f"Created .apworld: {output_path}")
            return output_path
    
    def _copy_directory(self, src: Path, dst: Path) -> None:
        """Copy directory contents, overlaying files."""
        ensure_directory(dst)
        
        for item in src.rglob('*'):
            if item.is_file():
                relative_path = item.relative_to(src)
                dest_path = dst / relative_path
                copy_file(item, dest_path)
    
    def get_suggested_output_name(self) -> str:
        """Get a suggested output filename based on game name."""
        sanitized_name = self.game_definition.name.replace(' ', '_')
        # Remove any characters that might be problematic in filenames
        import re
        sanitized_name = re.sub(r'[^\w\-_\.]', '', sanitized_name)
        return f"{sanitized_name}.apworld"


class ApworldBuilder:
    """High-level builder for creating .apworld files from game definitions."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize with optional output directory."""
        self.output_dir = output_dir or Path.cwd()
    
    async def build_apworld(
        self, 
        game_definition: GameDefinition, 
        base_apworld_path: Path,
        output_filename: Optional[str] = None
    ) -> Path:
        """Build an .apworld file from game definition."""
        packager = ApworldPackager(game_definition, base_apworld_path)
        
        # Determine output filename
        if not output_filename:
            output_filename = packager.get_suggested_output_name()
        
        output_path = self.output_dir / output_filename
        
        print(f"Building .apworld for: {game_definition.name}")
        print(f"Chapters: {len(game_definition.chapters)}")
        print(f"Total challenges: {game_definition.total_challenges}")
        print(f"Progression items: {len(game_definition.progression_items)}")
        
        return packager.create_apworld(output_path)