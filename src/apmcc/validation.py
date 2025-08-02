"""Validation functions for game definitions."""

import sys
from typing import Dict, Union


def validate_definition(definition: dict) -> None:
    """Validate the game definition structure and content."""
    
    # Basic validation of required fields
    required_fields = ['name', 'progression_items', 'chapters']
    missing_fields = [field for field in required_fields if field not in definition]
    
    if missing_fields:
        print(f"Error: Missing required fields in YAML file: {', '.join(missing_fields)}", file=sys.stderr)
        sys.exit(1)
    
    # Validate name field
    if not isinstance(definition['name'], str) or not definition['name'].strip():
        print("Error: 'name' must be a non-empty string", file=sys.stderr)
        sys.exit(1)
    
    # Validate progression_items
    if not isinstance(definition.get('progression_items'), list):
        print("Error: 'progression_items' must be a list", file=sys.stderr)
        sys.exit(1)
    
    if not definition['progression_items']:
        print("Error: 'progression_items' cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    for item in definition['progression_items']:
        if not isinstance(item, str) or not item.strip():
            print("Error: All progression items must be non-empty strings", file=sys.stderr)
            sys.exit(1)
    
    # Validate chapters
    if not isinstance(definition.get('chapters'), list):
        print("Error: 'chapters' must be a list", file=sys.stderr)
        sys.exit(1)
    
    if not definition['chapters']:
        print("Error: 'chapters' cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    goal_challenges = 0
    
    for i, chapter in enumerate(definition['chapters']):
        if not isinstance(chapter, dict):
            print(f"Error: Chapter {i+1} must be a dictionary", file=sys.stderr)
            sys.exit(1)
        
        if 'name' not in chapter:
            print(f"Error: Chapter {i+1} missing required 'name' field", file=sys.stderr)
            sys.exit(1)
        
        if not isinstance(chapter['name'], str) or not chapter['name'].strip():
            print(f"Error: Chapter {i+1} name must be a non-empty string", file=sys.stderr)
            sys.exit(1)
        
        if 'challenges' not in chapter:
            print(f"Error: Chapter {i+1} missing required 'challenges' field", file=sys.stderr)
            sys.exit(1)
        
        if not isinstance(chapter['challenges'], list):
            print(f"Error: Chapter {i+1} 'challenges' must be a list", file=sys.stderr)
            sys.exit(1)
        
        if not chapter['challenges']:
            print(f"Error: Chapter {i+1} must have at least one challenge", file=sys.stderr)
            sys.exit(1)
        
        # Validate challenges
        for j, challenge in enumerate(chapter['challenges']):
            if not isinstance(challenge, dict):
                print(f"Error: Challenge {j+1} in chapter {i+1} must be a dictionary", file=sys.stderr)
                sys.exit(1)
            
            if 'name' not in challenge:
                print(f"Error: Challenge {j+1} in chapter {i+1} missing required 'name' field", file=sys.stderr)
                sys.exit(1)
            
            if not isinstance(challenge['name'], str) or not challenge['name'].strip():
                print(f"Error: Challenge {j+1} in chapter {i+1} name must be a non-empty string", file=sys.stderr)
                sys.exit(1)
            
            # Validate optional flags
            valid_flags = {'goal', 'excluded', 'priority'}
            for flag in challenge:
                if flag != 'name' and flag not in valid_flags:
                    print(f"Error: Challenge '{challenge['name']}' has invalid flag '{flag}'. Valid flags: {', '.join(valid_flags)}", file=sys.stderr)
                    sys.exit(1)
                
                if flag in valid_flags and not isinstance(challenge[flag], bool):
                    print(f"Error: Challenge '{challenge['name']}' flag '{flag}' must be a boolean", file=sys.stderr)
                    sys.exit(1)
            
            if challenge.get('goal', False):
                goal_challenges += 1
    
    if goal_challenges == 0:
        print("Warning: No challenges marked as 'goal'. At least one challenge should be marked as goal to complete the game.")
    
    # Validate filler_item_categories (optional)
    if 'filler_item_categories' in definition:
        filler_categories = definition['filler_item_categories']
        if not isinstance(filler_categories, dict):
            print("Error: 'filler_item_categories' must be a dictionary", file=sys.stderr)
            sys.exit(1)
        
        for category_name, category in filler_categories.items():
            if not isinstance(category, dict):
                print(f"Error: Filler category '{category_name}' must be a dictionary", file=sys.stderr)
                sys.exit(1)
            
            # Validate weight
            if 'weight' in category:
                if not isinstance(category['weight'], (int, float)) or category['weight'] <= 0:
                    print(f"Error: Filler category '{category_name}' weight must be a positive number", file=sys.stderr)
                    sys.exit(1)
            
            # Validate include_confirmation_locations
            if 'include_confirmation_locations' in category:
                if not isinstance(category['include_confirmation_locations'], bool):
                    print(f"Error: Filler category '{category_name}' include_confirmation_locations must be a boolean", file=sys.stderr)
                    sys.exit(1)
            
            # Validate items
            if 'items' not in category:
                print(f"Error: Filler category '{category_name}' missing required 'items' field", file=sys.stderr)
                sys.exit(1)
            
            if not isinstance(category['items'], list):
                print(f"Error: Filler category '{category_name}' items must be a list", file=sys.stderr)
                sys.exit(1)
            
            if not category['items']:
                print(f"Error: Filler category '{category_name}' must have at least one item", file=sys.stderr)
                sys.exit(1)
            
            for k, item in enumerate(category['items']):
                if isinstance(item, str):
                    # Simple string item
                    if not item.strip():
                        print(f"Error: Item {k+1} in category '{category_name}' cannot be empty", file=sys.stderr)
                        sys.exit(1)
                elif isinstance(item, dict):
                    # Item with properties
                    if 'name' not in item:
                        print(f"Error: Item {k+1} in category '{category_name}' missing required 'name' field", file=sys.stderr)
                        sys.exit(1)
                    
                    if not isinstance(item['name'], str) or not item['name'].strip():
                        print(f"Error: Item {k+1} in category '{category_name}' name must be a non-empty string", file=sys.stderr)
                        sys.exit(1)
                    
                    if 'weight' in item:
                        if not isinstance(item['weight'], (int, float)) or item['weight'] <= 0:
                            print(f"Error: Item '{item['name']}' in category '{category_name}' weight must be a positive number", file=sys.stderr)
                            sys.exit(1)
                else:
                    print(f"Error: Item {k+1} in category '{category_name}' must be a string or dictionary", file=sys.stderr)
                    sys.exit(1)