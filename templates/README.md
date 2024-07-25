# [MMORPDND]

# WARNING: If you are one of my DnD players, leave this repository now!

This folder contains various apps that are used within the MMORPDND system. View the official docs for more information about these apps.
## Table of Contents

- [Folders](#folders)
- [Apps](#apps)

## Folders

The various folders in this directory server purposes for the various MMORPDND apps and features.

- img
  - This folder is for storing images that will be detected by the creator.py app.
- input_files
  - This folder is where all .char and .input files are located for the creator app.
- lists
  - This folder contians various lists that are used for various features of the MMORPDND system.
- languages
  - This folder is a place to store custom languages. These often contain many files (fonts, docs, and applications for assitance in translating or creating puzzles).
- stockpile
  - Files relating to the stockpile system.
- tests
  - This is where automated python unit tests are stored.
- trash
  - This is a folder to store files that have already been 'finished' or converted using the creator.py app but are to be kept around in case future additions or changes are made. 

## Apps

The apps in this folder are sub-apps of the MMORPDND system and each serve a specific purpose or serve as a tool for developers.

- creator.py
  - The main MMORPDND creator tool for adding input files to the HTML database and performing various other tasks.
- stockpile.py
  - The main app for running and updating the stockpile system (see docs for description) 
- stockpile/stockpile_plot.py
  - This app will plot the data generated using the stockpile system over time.
- char_maker.py
  - This app is a tool for making characters with the optional assistance of AI (AI features not yet implemented).
- reset_all_files.py
  - This will reset all images, delete all HTML files, and move trash files back to input_files to be re-deployed.
- publicize_files.py
  - This will create a copy of an HTML file with the navigation header and links removed for public release. The new file will have an appended '_public' to the file name. The files to publicize are determined by the public_files.list file.
- add_external_links.py
  - This script will update all html files in the specified folder (../campaign in this case) with external links specified in the links.list file (located in the lists folder).
- visualize_nodes.py
  - This script will create a plot of all linked HTML files for visualization.
- trash/img/cleanup_trash_images.py
  - This script retrieves a list of image files from the script's directory, then searches a specified database folder (the campaign folder) and its subdirectories for images that match the filenames from the script's directory. It deletes any matching image files found in the script's directory. The database folder path is specified relative to the script's location. This ensures that the trash does not contain duplicate images.
