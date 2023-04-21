import os

# Define the number of HTML files to create in each subdirectory
num_files_per_subdirectory = 3

# Get the current directory
current_dir = os.getcwd()

# Create an index.html file in the current directory
with open(os.path.join(current_dir, "index.html"), "w") as f:
    f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")

# Recursively walk through the directory structure and create HTML files in each subdirectory
for dirpath, dirnames, filenames in os.walk(current_dir):
    for dirname in dirnames:
        if "templates" not in dirname and "css" not in dirname:
            # Create an index.html file in each subdirectory
            with open(os.path.join(dirpath, dirname, "index.html"), "w") as f:
                f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")
            for i in range(num_files_per_subdirectory):
                # Use the current directory name as part of the filename
                filename = f"{dirname}_{i}.html"
                with open(os.path.join(dirpath, dirname, filename), "w") as f:
                    f.write(f"<html><head></head><body><h1>This is {filename} in {dirname} directory!</h1></body></html>")

# Create additional HTML files in the script directory
for i in range(num_files_per_subdirectory):
    # Use the script directory name as part of the filename
    filename = f"{os.path.basename(current_dir)}_{i}.html"
    with open(os.path.join(current_dir, filename), "w") as f:
        f.write(f"<html><head></head><body><h1>This is {filename} in {current_dir} directory!</h1></body></html>")

print("HTML files created successfully!")
