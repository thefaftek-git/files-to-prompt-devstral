# Add Extension Filtering

## Description
Add support for filtering files by extension using the `-e/--extension` option.

## Implementation Plan
1. Modify `file_concat.py` to accept multiple `-e/--extension` options
2. Store extensions in a list
3. When processing files, only include those that match the specified extensions

## Example Usage
```bash
# Include only .txt and .md files
./file_concat.py ./ -e txt -e md
```