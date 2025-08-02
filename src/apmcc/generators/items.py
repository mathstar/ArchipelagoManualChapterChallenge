"""Generator for items.json file."""

from typing import Any, Dict

from .base_generator import BaseGenerator


class ItemsGenerator(BaseGenerator):
    """Generates the items.json file for progression and filler items."""
    
    def get_output_filename(self) -> str:
        """Get the output filename."""
        return "items.json"
    
    def generate(self) -> Dict[str, Any]:
        """Generate items data from game definition."""
        items = []
        item_id_counter = 0
        
        # Add progression items
        for progression_item in self.game_definition.progression_items:
            # Create one item per chapter (except the last one gets extra for victory)
            num_chapters = len(self.game_definition.chapters)
            count = num_chapters  # One to unlock each chapter + extra for victory
            
            item = {
                "name": progression_item,
                "id": self._get_item_id(item_id_counter),
                "category": ["progression"],
                "count": count
            }
            items.append(item)
            item_id_counter += 1
        
        # Add filler items from categories
        for category in self.game_definition.filler_item_categories:
            for item in category.items:
                item_data = {
                    "name": item.name,
                    "id": self._get_item_id(item_id_counter),
                    "category": [category.name],
                    "weight": item.weight
                }
                
                # Set count based on category weight and total challenges
                # This is a rough estimate - actual counts would be calculated during generation
                base_count = max(1, int(self.game_definition.total_challenges * category.weight / 10))
                item_data["count"] = base_count
                
                items.append(item_data)
                item_id_counter += 1
        
        # Add a default filler item if no filler categories defined
        if not self.game_definition.filler_item_categories:
            default_filler = {
                "name": "Filler",
                "id": self._get_item_id(item_id_counter),
                "category": ["filler"],
                "count": max(1, self.game_definition.total_challenges - len(self.game_definition.progression_items))
            }
            items.append(default_filler)
        
        return {"items": items}