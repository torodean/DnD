from bs4 import BeautifulSoup
import os

# Define the directory path to prettify HTML files
directory_path = os.getcwd()

# Loop through all files and subdirectories in the directory
for root, directories, files in os.walk(directory_path):
    # Loop through all HTML files in the current directory
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            # Read in the HTML file
            with open(file_path, "r") as f:
                contents = f.read()
            # Use BeautifulSoup to parse the HTML and prettify it
            soup = BeautifulSoup(contents, "html.parser")
            prettified_html = soup.prettify()
            # Write the prettified HTML back to the file
            with open(file_path, "w") as f:
                f.write(prettified_html)
