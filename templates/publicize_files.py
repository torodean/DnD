#!/bin/python3

import os
from bs4 import BeautifulSoup

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the directory of the current script
current_script_dir = os.path.dirname(current_script_path)

def publicize_file(file_path):
    """
    Remove the navigation bar from an HTML file and save the modified content.
    This will save the updated content to a file with '_public' appended before
    the html prefix.
    
    Note: This method assumes that the file is an HTML file.

    Args:
        file_path (str): The path to the HTML file to be processed.

    Returns:
        None
    """
    # Read the content of the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')

    # Find the navigation bar
    nav_bar = soup.find('div', class_='navigation')

    # Remove the navigation bar if it exists
    if nav_bar:
        nav_bar.decompose()

    output_file = file_path[0:-5] + "_public.html"
    # Write the modified HTML back to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def get_file_list(public_files_list):
    """
    Process a list of HTML file paths to remove the navigation bar from each.

    Args:
        public_files_list (str): The path to the text file containing the list of HTML files.

    Returns:
        None
    """
    # Read the list of filenames from the file
    with open(public_files_list, 'r', encoding='utf-8') as file:
        file_list = file.readlines()

    # Process each file in the list
    for file_path in file_list:
        # Remove any leading/trailing whitespace characters, including newlines
        file_path = current_script_dir + "/" + file_path.strip()

        # Check if the file exists
        if os.path.exists(file_path):
            print(f'Processing file: {file_path}')
            publicize_file(file_path)
        else:
            print(f'File not found: {file_path}')

if __name__ == '__main__':
    # Path to the text file containing the list of HTML files
    public_files_list = 'public_files.list'
    
    # Check if the file exists
    if os.path.exists(public_files_list):
        print(f'Public Files list file: {file_path}')
    else:
        print(f'ERROR: Please specify a public files list named {public_files_list}')

    # Process the files listed in the file
    get_file_list(public_files_list)
