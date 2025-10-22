# HSD GIT II Problem Sets

This repo is managed with [uv](https://docs.astral.sh/uv)

To install all dependencies run: ```uv sync --all-groups```

[CS50 Documentation](https://cs50.readthedocs.io)

## Formatting

Python files are formatted using ```ruff```, run ```uv run ruff format .``` to format files.

## HTML Generation

To update the HTML files for Moodle run 

```uv run .generator/main.py``` to update all files or ```uv run .generator/main.py problem``` to only update the specified problem