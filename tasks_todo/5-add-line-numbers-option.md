# Add Line Numbers Option

## Description
Add support for including line numbers in the output using the `-n/--line-numbers` option.

## Implementation Plan
1. Modify `file_concat.py` to add a `-n/--line-numbers` option
2. When this option is specified, include line numbers in the output

## Example Usage
```bash
# Include line numbers in the output
./file_concat.py ./ -n
```

## Example Output
```
files_to_prompt/cli.py
---
  1  import os
  2  from fnmatch import fnmatch
  3
  4  import click
  5  ...
```