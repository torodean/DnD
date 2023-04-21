import os

# define a function to recursively search for html files in a directory
def find_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                yield os.path.join(root, file)

# define a function to replace text in an html file
def replace_text_in_file(filepath, search_text, replace_text):
    with open(filepath, "r") as file:
        content = file.read()
    content = content.replace(search_text, replace_text)
    with open(filepath, "w") as file:
        file.write(content)

# define the search and replace logic
def replace_html_links(directory):
    html_files = list(find_html_files(directory))
    for html_file in html_files:
    	if "index.html" not in html_file:
		    print(f"Processing file: {html_file}")
		    with open(html_file, "r") as file:
		        content = file.read()
		    for other_html_file in html_files:
		        other_html_file_name = os.path.splitext(os.path.basename(other_html_file))[0]
		        if other_html_file != html_file:  # skip current html file
		            for root, dirs, files in os.walk(os.path.dirname(html_file)):
		                for file in files:
		                    if file.endswith(".html") and file != os.path.basename(html_file):
		                        file_name = os.path.splitext(os.path.basename(file))[0]
		                        search_text = f"{file_name.replace('_', ' ')}"
		                        replace_text = f"<a href='{file_name}.html'>{file_name.replace('_', ' ')}</a>"
		                        if search_text != file_name:
		                            with open(os.path.join(root, file), "r") as other_file:
		                                other_content = other_file.read()
		                            if search_text in other_content:
		                                print(f"Replacing '{search_text}' in '{other_file.name}' with '{replace_text}'")
		                                other_content = other_content.replace(search_text, replace_text)
		                                with open(os.path.join(root, file), "w") as other_file:
		                                    other_file.write(other_content)
		                        if search_text in content:
		                            print(f"Replacing '{search_text}' in '{html_file}' with '{replace_text}'")
		                            content = content.replace(search_text, replace_text)
		    with open(html_file, "w") as file:
		        file.write(content)



# call the function to replace the links in all html files in the directory
replace_html_links(".")

