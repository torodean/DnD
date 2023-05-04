import os

def create_index_files():
    for root, dirs, files in os.walk("."):
        # Create index file in current directory
        index_file_path = os.path.join(root, "index.html")
        if os.path.exists(index_file_path) or "templates" in index_file_path or "css" in index_file_path or ".git" in index_file_path or ".idea" in index_file_path:
            continue

        directory_name = os.path.basename(root)
        with open(index_file_path, 'w') as f:
            f.write(f"<html>\n<head>\n<title>Index of {directory_name}</title>\n</head>\n<body>\n")
            f.write(f"<h1>Index of {directory_name}</h1>\n</body>\n</html>\n")

create_index_files()
