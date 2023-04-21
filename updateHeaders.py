import os
import re

# Define the template file path
template_file = "templates/headerTemplate.html"

# Define the regular expression to match the header section
header_regex = re.compile(r"<head>.*?</head>", re.DOTALL)

# Loop through all HTML files in the current directory and its subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") and "Template" not in file:
            # Read the contents of the HTML file
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                contents = f.read()

            # Read the contents of the template file
            with open(template_file, "r") as f:
                template = f.read()

            # Replace the header section with the contents of the template
            contents = re.sub(header_regex, template, contents)

            # Write the updated contents back to the file
            with open(file_path, "w") as f:
                f.write(contents)
