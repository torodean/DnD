#!/bin/phthon3
import tkinter as tk
from tkinter import PhotoImage
import os
import re
import random

class MMORPDND_VARS:
    """
    This is a class for storing variables used by MMORPDND* classes.
    """
    def __init__(self):
        """
        Initialization method.
        """
        # Define the directory structure
        self.directory_structure = {
            "campaign": {
                "locations": {
                    "regions": {},
                    "dungeons": {},
                    "cities": {},
                    "landmarks": {},
                    "towns": {}
                },
                "items": {
                    "consumables": {
                        "potions": {},
                        "food": {},
                        "drink": {}
                    },
                    "magic": {},
                    "weapons": {},
                    "armor": {},
                    "trinkets": {}
                },
                "notes": {},
                "creatures": {
                    "animals": {},
                    "monsters": {}
                },
                "lore": {
                    "history": {},
                    "factions": {},
                    "races": {},
                    "classes": {},
                    "backgrounds": {},
                    "deities": {}
                },
                "quests": {},
                "characters": {
                    "player": {},
                    "non-player": {}
                },
                "spells": {
                    "level_0": {},
                    "level_1": {},
                    "level_2": {},
                    "level_3": {},
                    "level_4": {},
                    "level_5": {},
                    "level_6": {},
                    "level_7": {},
                    "level_8": {},
                    "level_9": {},
                }
            }
        }
        
        # Define the number of HTML files to create in each subdirectory
        self.num_dummy_files_per_subdir = 3# Stores all files created so far.
        self.all_index_files = []
        
        # Define the root directory
        self.root_dir = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.directories_to_exclude = ["templates", "css", ".git", ".idea"]
        
        # Define the regular expression to match the header section
        self.header_regex = re.compile(r"<head>.*?</head>", re.DOTALL)

        # Define the regular expression to match the header section
        self.title_regex = re.compile(r"<title>.*?</title>", re.DOTALL)
        
        # Define the template file paths
        self.header_template_file = "templates/headerTemplate.html"
        self.css_path = "css/mmorpdnd.css"


# Define a global variable containing the declared vars. Use this so they are all only defined once and can be updated/stored throughout the applications lifetime.
global_vars = MMORPDND_VARS()

class MMORPDND:
    """
    A class for all the main MMORPDND features.
    """
    def __init__(self):
        """
        Initialization method.
        """
        
    # Define a function to create directories recursively
    def create_directories(self, path: str, structure: dict) -> None:
        """
        Recursively creates directories in the given path according to the structure specified in the dictionary.
        
        Args:
            path (str): The root path where directories will be created.
            structure (dict): A dictionary representing the structure of the directories to be created.
            
        Returns:
            None
        """
        for key in structure:
            subpath = os.path.join(path, key)
            if not os.path.exists(subpath):
                os.makedirs(subpath)
                print(f"Created directory: {subpath}")
            if structure[key]:
                self.create_directories(os.path.join(path, key), structure[key])
                
                
    def create_dummy_html_files(self, directory = global_vars.root_dir):
        """
        Create dummy html files in all directories and sub-directories for testing. Each file will be randomly linked to another file.
        """
        all_dummy_files = []
        # Create an index.html file in the current directory
        with open(os.path.join(directory, "index.html"), "w") as f:
            f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")

        # Recursively walk through the directory structure and create HTML files in each subdirectory
        for root, dirnames, filenames in os.walk(directory):
            for dirname in dirnames:
            
                # Check if we are looking at a file in our exclude list.
                if any(exclude in root for exclude in global_vars.directories_to_exclude):
                    continue
                if any(exclude in dirname for exclude in global_vars.directories_to_exclude):
                    continue

                # Create an index.html file in each subdirectory
                with open(os.path.join(root, dirname, "index.html"), "w") as f:
                    f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")
                    
                for i in range(global_vars.num_dummy_files_per_subdir):
                    # Use the current directory name as part of the filename
                    filename = f"{dirname}_{i}.html"
                    all_dummy_files.append(filename.split('.html')[0])  
                    random_one = random.choice(all_dummy_files)
                    random_two = random.choice(all_dummy_files)
                    with open(os.path.join(root, dirname, filename), "w") as f:
                        f.write(f"<html><head></head><body><h1>This is {filename} in {dirname} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")
                        print(f"HTML file {directory}/{filename} created successfully!")

        # Create additional HTML files in the script directory
        for i in range(global_vars.num_dummy_files_per_subdir):
            # Use the script directory name as part of the filename
            filename = f"{os.path.basename(directory)}_{i}.html"
            all_dummy_files.append(filename.split('.html')[0])
            random_one = random.choice(all_dummy_files)
            random_two = random.choice(all_dummy_files)
            with open(os.path.join(directory, filename), "w") as f:
                f.write(f"<html><head></head><body><h1>This is {filename} in {directory} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")
                print(f"HTML file {directory}/{filename} created successfully!")

        print("HTML files created successfully!")


    def create_index_files(self, directory = global_vars.root_dir):
        """
        This will create index files for all subdirectories.
        """    
        # Loop through all directories and files starting from the specified directory.
        for root, dirnames, filenames in os.walk(directory):
            # Create index file in current directory.
            index_file_path = os.path.join(root, "index.html")
            
            # Skip this directory if index.html already exists.
            if os.path.exists(index_file_path):
                continue
            # Check if we are looking at a file in our exclude list.
            if any(exclude in index_file_path for exclude in global_vars.directories_to_exclude):
                continue

            # Create the index.html file and write the HTML content to it
            directory_name = os.path.basename(root)
            with open(index_file_path, 'w') as f:
                f.write(f"<html>\n<head>\n<title>Index of {directory_name}</title>\n</head>\n<body>\n")
                f.write(f"<h1>Index of {directory_name}</h1>\n</body>\n</html>\n")
            print(f"Created index file at {index_file_path}")
            
            
    def update_index_files(self):
        """
        This will update all index files to include links to the other files in that directory.
        """
        
        print("Updating index files...")
        
        # Get list of all HTML index files in directory and subdirectories
        for root, dirnames, filenames in os.walk("."):
            for file in filenames:
            
                # Check if we are looking at a file in our exclude list.
                if any(exclude in root for exclude in global_vars.directories_to_exclude):
                    continue               
                
                if file.endswith("index.html"):
                    global_vars.all_index_files.append(os.path.join(root, file))

        # Loop through each index file found
        for file in global_vars.all_index_files:
            with open(file, 'r+') as f:
                file_data = f.read()

                # Find all HTML files in same directory as current file
                dir_path = os.path.dirname(file)
                html_files_in_dir = []
                
                # Add each html file to the list of html files in that directory.
                for file_name in os.listdir(dir_path):
                    if file_name.endswith(".html"):
                        html_files_in_dir.append(file_name)

                # Create index links div section if it does not exist
                index_links_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*>.*?</div>'
                index_links_match = re.search(index_links_pattern, file_data, re.DOTALL)
                if not index_links_match:
                    index_links_div = '<div class="indexLinks"><ul></ul></div>'
                    file_data = re.sub(r'</body>', index_links_div + '\n</body>', file_data)

                # Update index links
                index_links_div_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*><ul>'
                index_links_div_match = re.search(index_links_div_pattern, file_data, re.DOTALL)
                index_links_div = index_links_div_match.group(0) if index_links_div_match else '<div class="indexLinks"><ul>'
                index_links = ''
                for html_file in html_files_in_dir:
                    if html_file != 'index.html':
                        link_text = html_file.replace('.html', '')
                        link = f'<li><a href="{html_file}">{link_text}</a></li>'
                        index_links += f'{link}\n'

                # Replace index links in file
                updated_data = re.sub(index_links_pattern, index_links_div + '\n' + index_links + '</ul></div>', file_data, flags=re.DOTALL)
                
                # Write updated file data to file
                f.seek(0)
                f.write(updated_data)
                f.truncate()
                print(f"{file} updated")
            print("All index.html files updated.")
            
            
    def update_headers(self, directory = global_vars.root_dir):
        """
        This will update the headers of the html files to match the template.
        """
        # Loop through all HTML files in the current directory and its subdirectories
        for root, dirnames, filenames in os.walk(directory):
            for file in filenames:
                # check for html file and if "Template" is in filename.
                if file.endswith(".html") and "Template" not in file:
                    # Read the contents of the HTML file
                    file_path = os.path.join(root, file)
                    
                    # Check if we are looking at a file in our exclude list.
                    if any(exclude in file_path for exclude in global_vars.directories_to_exclude):
                        continue
                        
                    with open(file_path, "r") as f:
                        contents = f.read()

                    # Read the contents of the template file
                    with open(global_vars.header_template_file, "r") as f:
                        template = f.read()

                    # Replace the header section with the contents of the template
                    contents = re.sub(global_vars.header_regex, template, contents)
                    
                    title = "<title>" + file.split('.')[0].replace('_', ' ') + "</title>"
                    print(title)
                    
                    # Replace the title section with the file name
                    contents = re.sub(global_vars.title_regex, title, contents)
                        
                    # Determine the relative path to the CSS file
                    css_relative_path = os.path.relpath(global_vars.css_path, start=root)
                    
                    # Determine the number of subdirectories between the HTML file and the CSS file
                    num_subdirs = css_relative_path.count(os.sep) - 1
                    
                    # Create the correct link path for the CSS file
                    link_path = "../" * num_subdirs + global_vars.css_path
                    
                    # Replace the placeholder with the link to the CSS file
                    contents = contents.replace("%OPENAICSS%", f'<link href="{link_path}" rel="stylesheet"/>')
                    
                    # Overwrite the HTML file with the updated contents 
                    with open(file_path, "w") as f:
                        f.write(contents)
                    
                    print(f"Updated head and css in {file_path}")  # Print progress update
            
        
class MMORPDND_GUI:
    """
    Class to store GUI functions and operations.
    """
    def __init__(self):
        """
        Initialization method.
        """
        self.mmorpdnd = MMORPDND()
        self.gui = tk.Tk()    
        self.gui.title("MMORPDND")
        self.gui.geometry("300x400")
        
        # Load icon image
        icon = PhotoImage(file='{}/mmorpdnd.png'.format(global_vars.root_dir))
        # Set icon image
        self.gui.tk.call('wm', 'iconphoto', self.gui._w, icon)
        
        blue_button_style = {"font": ("Arial", 14), "bg": "#4287f5", "fg": "#ffffff", "activebackground": "#ffffff", "activeforeground": "#4287f5"}
        
        red_button_style = {"font": ("Arial", 14), "bg": "#f54251", "fg": "#ffffff", "activebackground": "#ffffff", "activeforeground": "#f54251"}

        test_all_button = tk.Button(self.gui, text="Test All", command=self.test_all, **red_button_style)
        test_all_button.pack(pady=5)
        
        update_all_button = tk.Button(self.gui, text="Update All", command=self.update_all, **red_button_style)
        update_all_button.pack(pady=5)

        create_directories_button = tk.Button(self.gui, text="Create Directories", command=self.create_directories, **blue_button_style)
        create_directories_button.pack(pady=5)
        
        create_dummy_html_files_button = tk.Button(self.gui, text="Create Dummy HTML Files", command=self.create_dummy_html_files, **blue_button_style)
        create_dummy_html_files_button.pack(pady=5)
        
        create_index_files_button = tk.Button(self.gui, text="Create Index Files", command=self.create_index_files, **blue_button_style)
        create_index_files_button.pack(pady=5)
        
        update_index_links_button = tk.Button(self.gui, text="Update Index File Links", command=self.update_index_links, **blue_button_style)
        update_index_links_button.pack(pady=5)
        
        update_headers_button = tk.Button(self.gui, text="Update HTML Headers", command=self.update_headers, **blue_button_style)
        update_headers_button.pack(pady=5)

        
    def run(self):
        """
        This method will run/open the GUI.
        """
        self.gui.mainloop()
        
    def test_all(self):
        """
        This method will update all files.
        """
        self.create_directories()
        self.create_dummy_html_files()
        self.create_index_files()
        self.update_index_links()
        self.update_headers()
        
    def update_all(self):
        """
        This method will update all files.
        """
        self.create_directories()
        self.create_index_files()
        self.update_index_links()
        self.update_headers()
        
    def create_directories(self):
        self.mmorpdnd.create_directories(global_vars.root_dir, global_vars.directory_structure)
        
    def create_dummy_html_files(self):
        self.mmorpdnd.create_dummy_html_files(global_vars.root_dir)
        
    def create_index_files(self):
        self.mmorpdnd.create_index_files(global_vars.root_dir)
        
    def update_index_links(self):
        self.mmorpdnd.update_index_files()
                
    def update_headers(self):
        self.mmorpdnd.update_headers(global_vars.root_dir)
        
def main():
    # main method code here
    gui = MMORPDND_GUI()
    gui.run()


if __name__ == '__main__':
    main()
