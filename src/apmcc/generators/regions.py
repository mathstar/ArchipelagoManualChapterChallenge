"""Generator for regions.json file."""

from typing import Any, Dict, List

from .base_generator import BaseGenerator


class RegionsGenerator(BaseGenerator):
    """Generates the regions.json file for chapter-based regions."""
    
    def get_output_filename(self) -> str:
        """Get the output filename."""
        return "regions.json"
    
    def generate(self) -> Dict[str, Any]:
        """Generate regions data from game definition."""
        regions = []
        
        # Create Menu region (starting point)
        menu_region = {
            "name": "Menu",
            "locations": [],
            "exits": []
        }
        
        # Add exit to first chapter if chapters exist
        if self.game_definition.chapters:
            first_chapter_name = self._sanitize_name(self.game_definition.chapters[0].name)
            menu_region["exits"].append(first_chapter_name)
        
        regions.append(menu_region)
        
        # Create regions for each chapter
        for chapter_index, chapter in enumerate(self.game_definition.chapters):
            region_name = self._sanitize_name(chapter.name)
            
            # Get all location names for this chapter
            locations = []
            for challenge in chapter.challenges:
                location_name = f"{chapter.name}: {challenge.name}"
                locations.append(location_name)
            
            # Determine exits (connections to next chapter)
            exits = []
            if chapter_index < len(self.game_definition.chapters) - 1:
                next_chapter = self.game_definition.chapters[chapter_index + 1]
                next_region_name = self._sanitize_name(next_chapter.name)
                exits.append(next_region_name)
            
            chapter_region = {
                "name": region_name,
                "locations": locations,
                "exits": exits
            }
            
            # Add requirements for accessing this region
            if chapter_index > 0:
                # Require progression items to access chapters after the first
                required_items = []
                for progression_item in self.game_definition.progression_items:
                    # Need one progression item per chapter to access the next
                    required_items.extend([progression_item] * chapter_index)
                
                if required_items:
                    chapter_region["requires"] = required_items
            
            regions.append(chapter_region)
        
        # Add confirmation locations region if needed
        confirmation_locations = self._get_confirmation_locations()
        if confirmation_locations:
            confirmation_region = {
                "name": "Confirmation_Locations", 
                "locations": confirmation_locations,
                "exits": []
            }
            regions.append(confirmation_region)
            
            # Add exit from menu to confirmation region
            menu_region["exits"].append("Confirmation_Locations")
        
        return {"regions": regions}
    
    def _get_confirmation_locations(self) -> List[str]:
        """Get list of confirmation location names."""
        locations = []
        for category in self.game_definition.filler_item_categories:
            if category.include_confirmation_locations:
                for item in category.items:
                    locations.append(f"Received {item.name}")
        return locations