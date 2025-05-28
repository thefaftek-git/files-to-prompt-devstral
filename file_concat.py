#!/usr/bin/env python3

import os
import argparse
from pathlib import Path

def concatenate_files(directory, output_format='markdown'):
    """
    Concatenates all text files in the given directory into a single prompt.
    """
    result = []

    # Get all text files in the directory
    path_obj = Path(directory)
    for file_path in path_obj.iterdir():
        if file_path.is_file() and file_path.suffix in ['.js', '.cs', '.py', '.txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Format the content based on output format
                if output_format == 'markdown':
                    # Add code fence for markdown
                    language = file_path.suffix[1:]  # Get extension without dot
                    result.append(f"```{language}\n{content}\n```")
                elif output_format == 'claude_xml':
                    # Format as Claude XML
                    language = file_path.suffix[1:]  # Get extension without dot
                    result.append(f'<document>\n  <document_content>{content}</document_content>\n  <source>{file_path.name}</source>\n  <language>{language}</language>\n</document>')
                else:
                    # Plain text format
                    result.append(f"--- {file_path.name} ---\n{content}\n")

    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description='Concatenate files in a directory into a single prompt.')
    parser.add_argument('directory', type=str, help='Directory containing the files to concatenate')
    parser.add_argument('-f', '--format', type=str, choices=['markdown', 'text', 'claude_xml'], default='markdown',
                        help='Output format (default: markdown)')
    args = parser.parse_args()

    result = concatenate_files(args.directory, args.format)

    # Output to a .prompt file in the same directory
    output_path = Path(args.directory) / "combined.prompt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Output written to {output_path}")

if __name__ == '__main__':
    main()