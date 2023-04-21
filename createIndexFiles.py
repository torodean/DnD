import os

def create_index_files():
    for root, dirs, files in os.walk("."):
        # Create index file in current directory
        index_file_path = os.path.join(root, "index.html")
        if os.path.exists(index_file_path) or "Template" in index_file_path or "css" in index_file_path:
            continue

        directory_name = os.path.basename(root)
        with open(index_file_path, 'w') as f:
            f.write(f"<html>\n<head>\n<title>Index of {directory_name}</title>\n</head>\n<body>\n")
            f.write(f"<h1>Index of {directory_name}</h1>\n")
            f.write("<ul>\n")

            # Loop through each file in directory and add to index
            for file in files:
                if file != "index.html":
                    file_path = os.path.join(root, file)
                    f.write(f'<li><a href="{file_path}">{file}</a></li>\n')

            f.write("</ul>\n")
            f.write("</body>\n</html>\n")

create_index_files()
