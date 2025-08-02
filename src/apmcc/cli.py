import argparse
import asyncio
import sys
from pathlib import Path
import yaml

from .validation import validate_definition
from .models.game_definition import GameDefinition
from .downloaders.base_downloader import BaseDownloader
from .packaging.apworld_packager import ApworldBuilder


def parse_yaml_file(file_path: Path) -> dict:
    """Parse a YAML file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Archipelago Manual game implementation from YAML definition"
    )
    
    parser.add_argument(
        'input_file',
        type=Path,
        help='Path to the YAML definition file (e.g., ExampleDefinition.yaml)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists and has correct extension
    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if args.input_file.suffix.lower() not in ['.yaml', '.yml']:
        print(f"Warning: Input file '{args.input_file}' does not have a .yaml or .yml extension.")
    
    # Parse the YAML file
    definition = parse_yaml_file(args.input_file)
    
    # Validate the definition
    validate_definition(definition)
    
    print(f"Successfully parsed and validated definition for: {definition['name']}")
    print(f"Found {len(definition['chapters'])} chapters")
    print(f"Progression items: {', '.join(definition['progression_items'])}")
    
    if 'filler_item_categories' in definition:
        print(f"Filler item categories: {', '.join(definition['filler_item_categories'].keys())}")
    
    # Generate the .apworld file
    asyncio.run(generate_apworld(definition))


async def generate_apworld(definition_data: dict) -> None:
    """Generate the .apworld file from validated definition data."""
    # Convert dict to typed model
    game_definition = GameDefinition.from_dict(definition_data)
    
    # Download base .apworld
    print("\nDownloading base Manual .apworld...")
    downloader = BaseDownloader()
    base_apworld_path = await downloader.download_base_apworld()
    
    # Build the final .apworld
    print("\nGenerating game files...")
    builder = ApworldBuilder()
    output_path = await builder.build_apworld(game_definition, base_apworld_path)
    
    print(f"\n✅ Successfully created: {output_path}")
    print(f"You can now use this .apworld file with Archipelago!")


if __name__ == '__main__':
    main()