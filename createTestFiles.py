import os

def create_index_files(file_name):
    for root, dirs, files in os.walk("."):
        directory_name = os.path.basename(root)
        new_file_name = file_name + "_" + directory_name + ".html"
        new_file_name = new_file_name.replace("_.", "")
        
        # Create file in current directory
        file_path = os.path.join(root, new_file_name)
        
        # Skip the template folder.
        if "templates" in file_path or "css" in file_path:
            continue

        with open(file_path, 'w') as f:
            f.write(f"<html>\n<head>\n<title>Test file in {directory_name}</title>\n</head>\n<body>\n")
            f.write(f"<h1>Test file: {new_file_name}</h1>\n</body>\n</html>\n")

create_index_files("test")
create_index_files("test1")
create_index_files("test2")
