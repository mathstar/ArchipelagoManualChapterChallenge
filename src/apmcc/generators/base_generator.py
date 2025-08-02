"""Base class for game file generators."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from ..models.game_definition import GameDefinition


class BaseGenerator(ABC):
    """Abstract base class for game file generators."""
    
    def __init__(self, game_definition: GameDefinition):
        """Initialize with game definition."""
        self.game_definition = game_definition
    
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        """Generate the file content as a dictionary."""
        pass
    
    @abstractmethod
    def get_output_filename(self) -> str:
        """Get the output filename for this generator."""
        pass
    
    def write_to_file(self, output_dir: Path) -> Path:
        """Generate content and write to file in output directory."""
        from ..utils.file_utils import write_json
        
        content = self.generate()
        output_path = output_dir / self.get_output_filename()
        write_json(content, output_path)
        return output_path
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name for use as an identifier."""
        # Replace spaces and special characters with underscores
        import re
        return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
    
    def _get_location_id(self, chapter_index: int, challenge_index: int) -> int:
        """Generate a unique location ID for a challenge."""
        # Use a base offset to avoid conflicts with other games
        # Format: CCCCII where CCCC is chapter (1-based) and II is challenge (0-based)
        base_id = 1000000  # Base offset for this game type
        return base_id + (chapter_index + 1) * 100 + challenge_index
    
    def _get_item_id(self, item_index: int) -> int:
        """Generate a unique item ID."""
        # Use a different base offset for items
        base_id = 2000000
        return base_id + item_index