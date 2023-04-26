import os

css_path = "css/openai.css"

# Loop through all files and subdirectories in the current directory
for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        # Check if the file is an HTML file and not a template
        if filename.endswith(".html") and "Template" not in filename:
            filepath = os.path.join(dirpath, filename)

            # Read the contents of the HTML file
            with open(filepath, "r") as f:
                html = f.read()
                
            # Determine the relative path to the CSS file
            css_relative_path = os.path.relpath(css_path, start=dirpath)
            
            # Determine the number of subdirectories between the HTML file and the CSS file
            num_subdirs = css_relative_path.count(os.sep) - 1
            
            # Create the correct link path for the CSS file
            link_path = "../" * num_subdirs + css_path
            
            # Replace the placeholder with the link to the CSS file
            html = html.replace("%OPENAICSS%", f'<link href="{link_path}" rel="stylesheet"/>')
            
            # Overwrite the HTML file with the updated contents 
            with open(filepath, "w") as f:
                f.write(html)
            
            print(f"Updated css in {filepath}")  # Print progress update
