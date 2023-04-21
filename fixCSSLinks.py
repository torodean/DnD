import os

css_path = "css/openai.css"

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if filename.endswith(".html") and "Template" not in filename:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, "r") as f:
                html = f.read()
            css_relative_path = os.path.relpath(css_path, start=dirpath)
            num_subdirs = css_relative_path.count(os.sep) - 1 
            link_path = "../" * num_subdirs + css_path
            html = html.replace("%OPENAICSS%", f'<link href="{link_path}" rel="stylesheet"/>')
            with open(filepath, "w") as f:
                f.write(html)
