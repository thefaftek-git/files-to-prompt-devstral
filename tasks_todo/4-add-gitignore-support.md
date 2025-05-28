# Add GitIgnore Support

## Description
Add support for ignoring `.gitignore` files using the `--ignore-gitignore` option.

## Implementation Plan
1. Modify `file_concat.py` to add a `--ignore-gitignore` option
2. By default, respect `.gitignore` files
3. When `--ignore-gitignore` is specified, include all files

## Example Usage
```bash
# Include all files, ignoring .gitignore
./file_concat.py ./ --ignore-gitignore
```