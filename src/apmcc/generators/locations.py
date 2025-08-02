"""Generator for locations.json file."""

from typing import Any, Dict

from .base_generator import BaseGenerator


class LocationsGenerator(BaseGenerator):
    """Generates the locations.json file for challenges."""
    
    def get_output_filename(self) -> str:
        """Get the output filename."""
        return "locations.json"
    
    def generate(self) -> Dict[str, Any]:
        """Generate locations data from game definition."""
        locations = []
        
        for chapter_index, chapter in enumerate(self.game_definition.chapters):
            for challenge_index, challenge in enumerate(chapter.challenges):
                location_id = self._get_location_id(chapter_index, challenge_index)
                
                location = {
                    "name": f"{chapter.name}: {challenge.name}",
                    "id": location_id,
                    "region": self._sanitize_name(chapter.name)
                }
                
                # Add metadata for special challenge types
                if challenge.goal:
                    location["category"] = ["goal"]
                elif challenge.excluded:
                    location["category"] = ["excluded"] 
                elif challenge.priority:
                    location["category"] = ["priority"]
                
                locations.append(location)
        
        # Add confirmation locations for filler items if requested
        for category in self.game_definition.filler_item_categories:
            if category.include_confirmation_locations:
                for item in category.items:
                    # Generate unique IDs for confirmation locations
                    location_id = self._get_location_id(999, len(locations))
                    
                    location = {
                        "name": f"Received {item.name}",
                        "id": location_id,
                        "region": "Confirmation_Locations",
                        "category": ["confirmation"]
                    }
                    locations.append(location)
        
        return {"locations": locations}
    
    def _get_location_id(self, chapter_index: int, challenge_index: int) -> int:
        """Override to handle confirmation locations."""
        if chapter_index == 999:  # Special case for confirmation locations
            return 3000000 + challenge_index
        return super()._get_location_id(chapter_index, challenge_index)