#!/bin/python3

import os
import glob
from bs4 import BeautifulSoup

def get_all_html_files(root_folder):
    return glob.glob(os.path.join(root_folder, '**', '*.html'), recursive=True)

def is_valid_link(link, base_path):
    return os.path.isfile(os.path.join(base_path, link))

def process_html_file(file_path, root_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    base_path = os.path.dirname(file_path)
    invalid_links = []
    
    for tag in soup.find_all('a', href=True):
        link = tag['href']
        if link == "#" or "/music/" in link:
            continue
        if not link.startswith(('http://', 'https://')) and not is_valid_link(link, base_path):
            invalid_links.append(link)
            tag.decompose()  # Remove the invalid link from the document

    if invalid_links:
       # with open(file_path, 'w', encoding='utf-8') as file:
        #    file.write(str(soup))
        for link in invalid_links:
            print(f"Invalid link {link} found and removed from {file_path}")

def main(root_folder):
    html_files = get_all_html_files(root_folder)
    for html_file in html_files:
        process_html_file(html_file, root_folder)


if __name__ == "__main__":
    root_folder = '../campaign'
    main(root_folder)

