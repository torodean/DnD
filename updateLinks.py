import os
import re

def find_html_files(directory='.'):
    """
    Finds all HTML files in a directory and its subdirectories.

    :param directory: The directory to search. Defaults to the current directory.
    :return: A list of dictionaries containing the name (without extension), name (with extension), and full path
             of each HTML file found.
    """
    html_file_names = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html') and "index.html" not in filename:
                name_no_ext = os.path.splitext(filename)[0]
                full_path = os.path.join(root, filename)
                if ".git" not in full_path and "templates" not in full_path and "css" not in full_path:
                    html_files.append({
                        'name_no_ext': name_no_ext,
                        'name_with_ext': filename,
                        'full_path': full_path
                    })
    return html_files


def get_relative_path(from_file, to_file):
    return os.path.relpath(to_file, os.path.dirname(from_file))


def search_html_files(html_files):    
    # Search the body text of each HTML file for the search strings
    for file in html_files:
        print("Parsing {0} for link updates!".format(file['full_path']))
        file_path = file['full_path']
        with open(file_path, 'r') as f:
            content = f.read()
            # Use regular expressions to find the body text of the HTML file
            match = re.search("<body.*?>(.*?)</body>", content, flags=re.DOTALL)
            if match:
                body_text = match.group(1)
                # Search the body text for the search string
                for search_word in html_files:
                    search_string = search_word['name_no_ext']
                    if search_string == file['name_no_ext']:
                        continue
                    if re.search(r"(?<!-)(?<!>)\b{}\b(?<!-)".format(search_string), body_text) or re.search(r"(?<!-)(?<!>)\b{}\b(?<!-)".format(search_string.replace('_', ' ')), body_text):
                        if search_string.replace('_', ' ') in body_text:
                            search_string = search_string.replace('_', ' ')
                        print(" -- {0} found in {1}".format(search_string, file_path))
                        link_path = get_relative_path(file_path, search_word['full_path'])
                        # Check if link is already present in body_text
                        link_regex = r'<a href="{0}">{1}</a>'.format(re.escape(link_path), re.escape(search_string))
                        if re.search(link_regex, body_text):
                            print("Link already exists in {0}".format(file_path))
                            continue
                        # Replace the search string with the new string
                        new_string = "<a href=\"{0}\">{1}</a>".format(link_path, search_string)
                        new_body_text = re.sub(search_string, new_string, body_text)
                        body_tags = re.search("<body(.*?)>", content, flags=re.DOTALL)
                        content = re.sub(r"<body[^>]*>(.*?)</body>", "<body>" + new_body_text + "</body>", content, flags=re.DOTALL)
                        content = re.sub(r"<body>", "<body" + body_tags.group(1) + ">", content, flags=re.DOTALL) 
                        print(" -- Replacing {0} with {1}".format(search_string, new_string))

                        # Write the modified HTML file
                        with open(file_path, "w") as f:
                            f.write(content)
                        
                        #reload the content with the updated text.
                        with open(file_path, 'r') as fp:
                            content = fp.read()
  

html_files = [] # Initialize html_files variable as an empty list
html_files = find_html_files()
for file in html_files:
    print(file['name_no_ext'], file['name_with_ext'], file['full_path'])
    
search_html_files(html_files)