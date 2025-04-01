#!/usr/bin/env python3
import os

"""
Script to display the directory structure of the current working directory.

When executed, this script identifies its own location using the real path of the
file and passes that directory to the print_directory_contents function to list
all directories and files in a hierarchical format.
"""

def print_directory_contents(path):
    """
    Prints the contents of a directory and its subdirectories in a tree-like structure.
    
    This function recursively traverses the directory specified by 'path', printing
    each directory and file with indentation to represent the hierarchy. Directories
    are denoted with a trailing slash, and files are listed beneath their parent
    directories.

    Args:
        path (str): The path to the directory whose contents will be printed.
    """
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print('{}{}'.format(sub_indent, file))

# Get the current working directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Print the contents of the current working directory
print_directory_contents(dir_path)
