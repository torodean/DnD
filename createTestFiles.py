import os

def create_index_files(file_name):
    for root, dirs, files in os.walk("."):
        # Create index file in current directory
        file_path = os.path.join(root, file_name)
        
        # Skip the template folder.
        if "Template" in file_path or "css" in file_path:
            continue

        directory_name = os.path.basename(root)
        with open(file_path, 'w') as f:
            f.write(f"<html>\n<head>\n<title>Test file in {directory_name}</title>\n</head>\n<body>\n")
            f.write(f"<h1>Test file: {file_name}</h1>\n</body>\n</html>\n")

create_index_files("test.html")
create_index_files("test1.html")
create_index_files("test2.html")