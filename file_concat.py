#!/usr/bin/env python3

import os
import sys
import argparse
import fnmatch
from pathlib import Path

def parse_gitignore(gitignore_path):
    """
    Parse a .gitignore file and return a list of ignore patterns.
    """
    patterns = []
    if not gitignore_path.exists():
        return patterns
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Store the pattern as-is for now (we'll handle negation later if needed)
                patterns.append(line)
    except (UnicodeDecodeError, PermissionError):
        # If we can't read the gitignore file, just return empty patterns
        pass
    
    return patterns

def collect_gitignore_patterns(directory):
    """
    Collect all .gitignore patterns from the directory and its parents.
    """
    all_patterns = []
    current_path = Path(directory).resolve()
    
    # Walk up the directory tree looking for .gitignore files
    while current_path != current_path.parent:
        gitignore_path = current_path / '.gitignore'
        if gitignore_path.exists():
            patterns = parse_gitignore(gitignore_path)
            all_patterns.extend(patterns)
        current_path = current_path.parent
    
    return all_patterns

def matches_gitignore_pattern(file_path, pattern, base_dir):
    """
    Check if a file path matches a gitignore pattern.
    """
    # Convert file path to relative path from base directory
    try:
        rel_path = file_path.resolve().relative_to(Path(base_dir).resolve())
        rel_path_str = str(rel_path)
        file_name = file_path.name
    except ValueError:
        # File is not within base directory
        return False
    
    # Handle negation patterns (starting with !)
    if pattern.startswith('!'):
        return False  # For now, we'll implement basic matching without negation
    
    # Handle directory patterns (ending with /)
    if pattern.endswith('/'):
        # This pattern matches directories
        pattern = pattern[:-1]
        return fnmatch.fnmatch(rel_path_str, pattern) or fnmatch.fnmatch(file_name, pattern)
    
    # Handle patterns with path separators
    if '/' in pattern:
        return fnmatch.fnmatch(rel_path_str, pattern)
    else:
        # Pattern matches against filename only
        return fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(rel_path_str, pattern)

def should_ignore(path, ignore_patterns, ignore_files_only=False, gitignore_patterns=None, base_dir=None):
    """
    Check if a path should be ignored based on ignore patterns and gitignore patterns.
    """
    # If ignore_files_only is True and this is a directory, don't ignore it
    if ignore_files_only and path.is_dir():
        return False
    
    # Check gitignore patterns first (if provided)
    if gitignore_patterns and base_dir:
        for pattern in gitignore_patterns:
            if matches_gitignore_pattern(path, pattern, base_dir):
                return True
    
    # Check regular ignore patterns
    if ignore_patterns:
        path_str = str(path)
        name = path.name
        
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(name, pattern):
                return True
    
    return False

def concatenate_files_from_directory(directory, output_format='markdown', extensions=None, include_hidden=False, ignore_patterns=None, ignore_files_only=False, ignore_gitignore=False):
    """
    Concatenates all text files in the given directory into a single prompt.
    """
    # Get all text files in the directory
    path_obj = Path(directory)
    file_paths = []
    
    # Collect gitignore patterns unless ignore_gitignore is True
    gitignore_patterns = None if ignore_gitignore else collect_gitignore_patterns(directory)
    
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
            
            # Check ignore patterns (including gitignore patterns)
            if should_ignore(file_path, ignore_patterns, ignore_files_only, gitignore_patterns, directory):
                continue
                
            file_paths.append(file_path)
    
    return concatenate_files_from_paths(file_paths, output_format, ignore_patterns, ignore_files_only, gitignore_patterns, directory)

def concatenate_files_from_paths(file_paths, output_format='markdown', ignore_patterns=None, ignore_files_only=False, gitignore_patterns=None, base_dir=None):
    """
    Concatenates files from a list of file paths into a single prompt.
    """
    result = []

    for file_path in file_paths:
        file_path = Path(file_path)
        if file_path.is_file():
            # Check ignore patterns (including gitignore patterns)
            if should_ignore(file_path, ignore_patterns, ignore_files_only, gitignore_patterns, base_dir):
                continue
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
    parser.add_argument('--ignore', action='append', help='Pattern to ignore (can be specified multiple times). Examples: --ignore "*.log" --ignore "temp*"')
    parser.add_argument('--ignore-files-only', action='store_true', help='Include directory paths that would otherwise be ignored (only ignore files)')
    parser.add_argument('--ignore-gitignore', action='store_true', help='Ignore .gitignore files and include all files that would otherwise be ignored by git')
    args = parser.parse_args()

    # Determine the mode of operation
    if args.null:
        # Read file paths from stdin with null separation
        file_paths = read_paths_from_stdin(null_separated=True)
        # For stdin mode, we need to determine a base directory for gitignore patterns
        # Use the current working directory as the base
        base_dir = os.getcwd()
        gitignore_patterns = None if args.ignore_gitignore else collect_gitignore_patterns(base_dir)
        result = concatenate_files_from_paths(file_paths, args.format, args.ignore, args.ignore_files_only, gitignore_patterns, base_dir)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = Path("combined.prompt")
    else:
        # Traditional directory mode
        if not args.directory:
            parser.error("directory argument is required when not using -0/--null option")
        
        result = concatenate_files_from_directory(args.directory, args.format, args.extension, args.include_hidden, args.ignore, args.ignore_files_only, args.ignore_gitignore)
        
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