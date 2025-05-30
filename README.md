# files-to-prompt

A Python script that concatenates text files from a directory into a single prompt file, with support for various output formats and filtering options.

## Usage

### Basic Usage

To use the script, provide the path to a directory containing the files you want to concatenate:

```bash
python3 file_concat.py path/to/directory
```

This will create a `combined.prompt` file in the specified directory containing all text files (`.js`, `.cs`, `.py`, `.txt` by default) formatted as Markdown code blocks.

### Reading from stdin

The script can also read file paths from standard input using the `-0/--null` option:

```bash
find . -name "*.py" -print0 | python3 file_concat.py -0
```

### Options

- `-f/--format <format>`: Output format. Choices: `markdown` (default), `text`, `claude_xml`.

  ```bash
  python3 file_concat.py path/to/directory -f claude_xml
  python3 file_concat.py path/to/directory -f text
  ```

- `-e/--extension <extension>`: File extension to include. Can be specified multiple times. Extensions can be with or without dots.

  ```bash
  python3 file_concat.py path/to/directory -e txt -e py
  python3 file_concat.py path/to/directory -e .md -e .js
  ```

- `-o/--output <file>`: Output file path. Default is `combined.prompt` in the specified directory.

  ```bash
  python3 file_concat.py path/to/directory -o output.txt
  ```

- `--include-hidden`: Include hidden files (files starting with `.`).

  ```bash
  python3 file_concat.py path/to/directory --include-hidden
  ```

- `--ignore <pattern>`: Pattern to ignore. Can be specified multiple times. Uses [fnmatch](https://docs.python.org/3/library/fnmatch.html) syntax.

  ```bash
  python3 file_concat.py path/to/directory --ignore "*.log" --ignore "temp*"
  ```

- `--ignore-files-only`: Only ignore files matching patterns, not directories.

  ```bash
  python3 file_concat.py path/to/directory --ignore-files-only --ignore "*test*"
  ```

- `--ignore-gitignore`: Ignore `.gitignore` files and include all files that would otherwise be ignored by git.

  ```bash
  python3 file_concat.py path/to/directory --ignore-gitignore
  ```

- `-n/--line-numbers`: Include line numbers in the output.

  ```bash
  python3 file_concat.py path/to/directory -n
  ```

- `-0/--null`: Read file paths from stdin, separated by NUL characters (for use with `find -print0`).

  ```bash
  find . -name "*.py" -print0 | python3 file_concat.py -0
  ```



## Examples

### Basic Example

Suppose you have a directory structure like this:

```
my_directory/
├── script.py
├── config.js
├── .hidden_file.txt
├── temp.log
└── subdirectory/
    └── utils.py
```

Running `python3 file_concat.py my_directory` will create a `combined.prompt` file containing:

````markdown
```py
# Contents of script.py
print("Hello, world!")
```
```js
// Contents of config.js
const config = { debug: true };
```
```py
# Contents of utils.py
def helper_function():
    return "utility"
```
````

Note that only files with default extensions (`.js`, `.cs`, `.py`, `.txt`) are included, and `.hidden_file.txt` and `temp.log` are excluded because hidden files are ignored by default and `.log` files don't match the default extensions.

### Including Hidden Files

To include hidden files:

```bash
python3 file_concat.py my_directory --include-hidden
```

### Custom Extensions

To include only specific file types:

```bash
python3 file_concat.py my_directory -e py -e js -e md
```

### Ignoring Patterns

To exclude files matching certain patterns:

```bash
python3 file_concat.py my_directory --ignore "*.log" --ignore "temp*"
```

### Line Numbers

To include line numbers in the output:

```bash
python3 file_concat.py my_directory -n
```

This will add line numbers to each file's content:

````markdown
```py
  1  # Contents of script.py
  2  print("Hello, world!")
```
````

## Output Formats

### Markdown Format (Default)

The default output format creates Markdown with fenced code blocks. The language is inferred from the file extension:

```bash
python3 file_concat.py my_directory -f markdown
```

### Text Format

Plain text format with file separators:

```bash
python3 file_concat.py my_directory -f text
```

This produces output like:
```
--- script.py ---
print("Hello, world!")

--- config.js ---
const config = { debug: true };
```

### Claude XML Format

Structured XML format optimized for Claude AI, following Anthropic's [guidelines](https://docs.anthropic.com/claude/docs/long-context-window-tips):

```bash
python3 file_concat.py my_directory -f claude_xml
```

This produces output like:
```xml
<document>
  <document_content>print("Hello, world!")</document_content>
  <source>script.py</source>
  <language>py</language>
</document>
<document>
  <document_content>const config = { debug: true };</document_content>
  <source>config.js</source>
  <language>js</language>
</document>
```

## Advanced Usage

### Reading from stdin with find

The script can read file paths from stdin when using the `-0/--null` option:

```bash
# Find all Python files and concatenate them
find . -name "*.py" -print0 | python3 file_concat.py -0

# Find files modified in the last day
find . -mtime -1 -name "*.txt" -print0 | python3 file_concat.py -0 -o recent_files.prompt
```

### Git Integration

The script automatically respects `.gitignore` files. To include all files regardless of `.gitignore`:

```bash
python3 file_concat.py my_directory --ignore-gitignore
```

### Custom Output Location

By default, the output file is created in the target directory. You can specify a custom location:

```bash
python3 file_concat.py my_directory -o /path/to/output.prompt
```

## Requirements

This script requires Python 3.6 or later and uses only standard library modules:
- `os`
- `sys` 
- `argparse`
- `fnmatch`
- `pathlib`

No additional dependencies need to be installed.

## Development

To contribute to this tool:

1. Clone the repository
2. The script is self-contained and requires no additional setup
3. Test your changes by running the script with various options
4. Make sure to test both directory mode and stdin mode (`-0` option)

## Features

- **Automatic gitignore support**: Respects `.gitignore` files by default
- **Multiple output formats**: Markdown, plain text, and Claude XML
- **Flexible file filtering**: Custom extensions, ignore patterns, hidden files
- **Line numbering**: Optional line numbers for better code reference
- **stdin integration**: Works with `find` and other command-line tools
- **Cross-platform**: Works on Windows, macOS, and Linux