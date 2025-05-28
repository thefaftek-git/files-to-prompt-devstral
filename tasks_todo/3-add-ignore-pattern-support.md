# Add Ignore Pattern Support

## Description
Add support for ignoring files and directories using patterns with the `--ignore` option.

## Implementation Plan
1. Modify `file_concat.py` to add a `--ignore` option that can be used multiple times
2. Use fnmatch module to match patterns against file paths
3. Implement `--ignore-files-only` option to include directory paths that would otherwise be ignored

## Example Usage
```bash
# Ignore .log files and directories starting with temp
./file_concat.py ./ --ignore "*.log" --ignore "temp*"
```