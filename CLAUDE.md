# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Archipelago Manual Chapter Challenge CLI** (APMCC), a Python tool that generates Archipelago Manual game implementations from YAML definition files. The tool converts chapter-based game definitions into Archipelago Manual format for use in the multi-world randomizer system.

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies (uses uv package manager)
uv install

# Run the CLI tool
python -m src.apmcc.cli ExampleDefinition.yaml
```

### Project Status
- **Python requirement**: >=3.13
- **Dependencies**: PyYAML>=6.0 only
- **Current state**: Validation complete, game generation logic not yet implemented (marked as TODO in cli.py:217)

## Architecture Overview

### Core Components

**Input Processing (`cli.py`)**:
- `parse_yaml_file()`: YAML parsing with comprehensive error handling
- `validate_definition()`: Multi-level validation of game definition structure
- `main()`: CLI entry point using argparse

**YAML Definition Structure**:
Game definitions must include:
- `name`: Game title
- `progression_items`: List of items required to unlock next chapter
- `chapters`: List containing chapter objects with `name` and `challenges`
- `filler_item_categories` (optional): Weighted item categories for non-progression slots

**Challenge Flags**:
- `goal`: Required to complete the game
- `excluded`: Always filled with non-progression items
- `priority`: AP attempts to fill with progression items

### Data Flow
1. CLI accepts YAML file path
2. File parsed and validated against expected structure
3. **TODO**: Game generation logic to create Archipelago Manual implementation
4. **TODO**: Output file generation

### Key Validation Rules
- Each chapter must have at least one challenge
- Progression items must be non-empty strings
- Challenge flags must be booleans
- Filler item weights must be positive numbers
- Warns if no challenges marked as `goal`

## Current Implementation Status

**Completed**:
- Robust YAML parsing and validation system
- CLI interface with clear error messages
- Example definition file structure

**Missing (TODO)**:
- Core game generation logic (cli.py:217)
- Output file creation
- Entry point configuration in pyproject.toml
- Testing infrastructure

## File Structure Notes

- `ExampleDefinition.yaml`: Reference implementation showing all supported features
- `src/apmcc/cli.py`: Single-file implementation containing all logic
- No testing framework currently configured
- Uses modern Python packaging with `pyproject.toml` and `uv.lock`