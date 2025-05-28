# Add Null Separator Option

## Description
Add support for using NUL character as separator when reading paths from stdin with the `-0/--null` option.

## Implementation Plan
1. Modify `file_concat.py` to add a `-0/--null` option
2. When this option is specified, use NUL character as separator instead of newlines

## Example Usage
```bash
# Use NUL separator when reading paths from stdin
find . -name "*.py" -print0 | ./file_concat.py --null
```