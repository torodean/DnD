import os

def find_html_files(directory='.'):
    """
    Finds all HTML files in a directory and its subdirectories.

    :param directory: The directory to search. Defaults to the current directory.
    :return: A list of dictionaries containing the name (without extension), name (with extension), and full path
             of each HTML file found.
    """
    html_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html'):
                name_no_ext = os.path.splitext(filename)[0]
                full_path = os.path.join(root, filename)
                html_files.append({
                    'name_no_ext': name_no_ext,
                    'name_with_ext': filename,
                    'full_path': full_path
                })
    return html_files
    
html_files = find_html_files()
for file in html_files:
    print(file['name_no_ext'], file['name_with_ext'], file['full_path'])