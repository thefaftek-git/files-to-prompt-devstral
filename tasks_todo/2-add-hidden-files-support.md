# Add Hidden Files Support

## Description
Add support for including hidden files (those starting with `.`) using the `--include-hidden` option.

## Implementation Plan
1. Modify `file_concat.py` to add a `--include-hidden` option
2. By default, exclude hidden files
3. When `--include-hidden` is specified, include them

## Example Usage
```bash
# Include hidden files
./file_concat.py ./ --include-hidden
```