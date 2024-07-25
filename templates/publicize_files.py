#!/usr/bin/env python3

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
        The name of the output file.
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
        
    return output_file


def remove_links(public_file_path):
    """
    Update or remove all <a> tags in an html file. If a public version of the linked file exists,
    update the link to point to the public file. Otherwise, remove the link entirely.

    Args:
        public_file_path: The public file path.

    Returns:
        None
    """
    # Read the content of the HTML file
    with open(public_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')
    
    # Get the directory of the original file
    original_dir = os.path.dirname(public_file_path)
    
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and href.endswith('.html'):
            # Skip the already public links.
            if "_public" in href:
                print(f"Ignoring link for {href}")
                continue
                
            # Construct the public version filename
            public_version = href[:-5] + '_public.html'
            public_path = os.path.join(original_dir, public_version)

            if os.path.exists(public_path):
                print(f"Public link exists for {public_path}")
                # Update the href to the public version
                a_tag['href'] = public_version
            else:                
                print(f"Removing link for {href}")
                # Remove the link but keep the text
                a_tag.replace_with(a_tag.text)    
                
    # Write the modified HTML back to the file
    with open(public_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


def get_file_list(public_files_list):
    """
    Process a text file containing a list of HTML file paths and returns the list of valid files.

    Args:
        public_files_list (str): The path to the text file containing the list of HTML files.

    Returns:
        The list of files to process.
    """
    files = []
    
    # Read the list of filenames from the file
    with open(public_files_list, 'r', encoding='utf-8') as file:
        file_list = file.readlines()

    # Process each file in the list
    for file_path in file_list:
        # Remove any leading/trailing whitespace characters, including newlines
        file_path = current_script_dir + "/" + file_path.strip()

        # Check if the file exists
        if os.path.exists(file_path):
            print(f'File found: {file_path}')
            files.append(file_path)
        else:
            print(f'File not found: {file_path}')
    
    return files


def process(files):
    # Store a list of the public files.
    public_files = []
    
    # First, publicize the files.
    for file in files:
        public_file = publicize_file(file)
        public_files.append(public_file)
        
    print(public_files)
    
    # Now go through and remove all links.
    for file in public_files:
        remove_links(file)
        

if __name__ == '__main__':
    # Path to the text file containing the list of HTML files
    public_files_list = 'lists/public_files.list'
    
    # Check if the file exists
    if os.path.exists(public_files_list):
        print(f'Public Files list file: {public_files_list}')

        # Process the files listed in the file
        files = get_file_list(public_files_list)
        process(files)
    else:
        print(f'ERROR: Please specify a public files list named {public_files_list}')
