#!/usr/bin/env python3

import os
import re
from bs4 import BeautifulSoup


def load_links(filename):
    """
    Loads a list of words and their corresponding links from a file.

    Each line in the file should contain a word and a link separated by a comma.
    The function creates a dictionary with words (converted to lowercase) as keys and links as values.

    Args:
        filename (str): The path to the file containing the words and links.

    Returns:
        dict: A dictionary where the keys are words (in lowercase) and the values are the corresponding links.
    """
    with open(filename, 'r') as file:
        links = {}
        for line in file:
            word, link = line.strip().split(',')
            links[word.lower()] = link.strip()
    return links
    

def find_html_files(directory):
    """
    Recursively finds all HTML files in a given directory and its subdirectories.

    Args:
        directory (str): The root directory to search for HTML files.

    Returns:
        list of str: A list of paths to HTML files found within the given directory and its subdirectories.
    """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files
    

def replace_words_in_html(file_path, links):
    """
    Replaces specified words with corresponding links in an HTML file.

    This function reads an HTML file, replaces specified words with HTML anchor tags containing 
    the corresponding links, and writes the modified content back to the file. The words are only 
    replaced if they are not already part of an existing link, and the case of the words is preserved.

    Args:
        file_path (str): The path to the HTML file to be processed.
        links (dict): A dictionary where the keys are words (in lowercase) and the values are the 
                      corresponding links.

    Returns:
        None
    """
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    doctype = ''
    if content.lstrip().startswith('<!DOCTYPE html>'):
        doctype = '<!DOCTYPE html>'
        content = content.lstrip()[len(doctype):]

    soup = BeautifulSoup(content, 'html.parser')

    # Iterate over all text elements in the HTML
    for text_element in soup.find_all(string=True):
        parent = text_element.parent
        if parent.name != 'a':  # Only replace if not inside an anchor tag
            new_text = text_element
            for word, link in links.items():
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                if pattern.search(new_text):
                    print(f"Found word '{word}' for replacement.")
                new_text = pattern.sub(lambda m: f'<a href="{link}">{m.group(0)}</a>', new_text)
            text_element.replace_with(BeautifulSoup(new_text, 'html.parser'))

    with open(file_path, 'w', encoding='utf-8') as file:
        if doctype:
            file.write(doctype + '\n')
        file.write(str(soup))
        print(f"Finished processing file: {file_path}")
        

# Main function
def main():
    # This is the file containing external links to add.
    links = load_links('lists/links.list')
    # This is the campaign folder containing our html files.
    html_files = find_html_files('../campaign')

    for html_file in html_files:
        replace_words_in_html(html_file, links)

if __name__ == "__main__":
    main()
