#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path

def concatenate_files_from_directory(directory, output_format='markdown', extensions=None, include_hidden=False):
    """
    Concatenates all text files in the given directory into a single prompt.
    """
    # Get all text files in the directory
    path_obj = Path(directory)
    file_paths = []
    
    # Default extensions if none specified
    if extensions is None:
        extensions = ['.js', '.cs', '.py', '.txt']
    
    # Add dots to extensions if not present and convert to lowercase for comparison
    normalized_extensions = []
    for ext in extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        normalized_extensions.append(ext.lower())
    
    for file_path in path_obj.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in normalized_extensions:
            # Skip hidden files unless include_hidden is True
            if not include_hidden and file_path.name.startswith('.'):
                continue
            file_paths.append(file_path)
    
    return concatenate_files_from_paths(file_paths, output_format)

def concatenate_files_from_paths(file_paths, output_format='markdown'):
    """
    Concatenates files from a list of file paths into a single prompt.
    """
    result = []

    for file_path in file_paths:
        file_path = Path(file_path)
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Format the content based on output format
                    if output_format == 'markdown':
                        # Add code fence for markdown
                        language = file_path.suffix[1:] if file_path.suffix else 'text'
                        result.append(f"```{language}\n{content}\n```")
                    elif output_format == 'claude_xml':
                        # Format as Claude XML
                        language = file_path.suffix[1:] if file_path.suffix else 'text'
                        result.append(f'<document>\n  <document_content>{content}</document_content>\n  <source>{file_path.name}</source>\n  <language>{language}</language>\n</document>')
                    else:
                        # Plain text format
                        result.append(f"--- {file_path.name} ---\n{content}\n")
            except (UnicodeDecodeError, PermissionError) as e:
                # Skip files that can't be read as text
                print(f"Skipping {file_path}: {e}", file=sys.stderr)
                continue

    return "\n".join(result)

def read_paths_from_stdin(null_separated=False):
    """
    Read file paths from stdin, either newline or null-separated.
    """
    if null_separated:
        # Read all input and split by null character
        input_data = sys.stdin.buffer.read()
        paths = input_data.decode('utf-8').split('\0')
    else:
        # Read line by line
        paths = [line.strip() for line in sys.stdin]
    
    # Filter out empty paths
    return [path for path in paths if path.strip()]

def main():
    parser = argparse.ArgumentParser(description='Concatenate files into a single prompt.')
    parser.add_argument('directory', type=str, nargs='?', help='Directory containing the files to concatenate (optional when using -0/--null)')
    parser.add_argument('-f', '--format', type=str, choices=['markdown', 'text', 'claude_xml'], default='markdown',
                        help='Output format (default: markdown)')
    parser.add_argument('-0', '--null', action='store_true',
                        help='Read file paths from stdin, separated by NUL characters (for use with find -print0)')
    parser.add_argument('-o', '--output', type=str, help='Output file path (default: combined.prompt in directory or current directory)')
    parser.add_argument('-e', '--extension', action='append', help='File extension to include (can be specified multiple times). Examples: -e txt -e py')
    parser.add_argument('--include-hidden', action='store_true', help='Include hidden files (files starting with .)')
    args = parser.parse_args()

    # Determine the mode of operation
    if args.null:
        # Read file paths from stdin with null separation
        file_paths = read_paths_from_stdin(null_separated=True)
        result = concatenate_files_from_paths(file_paths, args.format)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = Path("combined.prompt")
    else:
        # Traditional directory mode
        if not args.directory:
            parser.error("directory argument is required when not using -0/--null option")
        
        result = concatenate_files_from_directory(args.directory, args.format, args.extension, args.include_hidden)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = Path(args.directory) / "combined.prompt"

    # Write the result to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Output written to {output_path}")

if __name__ == '__main__':
    main()