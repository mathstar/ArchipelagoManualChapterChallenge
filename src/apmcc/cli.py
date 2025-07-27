import argparse
import sys
from pathlib import Path
import yaml


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
    
    # Basic validation of required fields
    required_fields = ['name', 'progression_items', 'chapters']
    missing_fields = [field for field in required_fields if field not in definition]
    
    if missing_fields:
        print(f"Error: Missing required fields in YAML file: {', '.join(missing_fields)}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Successfully parsed definition for: {definition['name']}")
    print(f"Found {len(definition['chapters'])} chapters")
    print(f"Progression items: {', '.join(definition['progression_items'])}")
    
    # TODO: Implement game generation logic here


if __name__ == '__main__':
    main()