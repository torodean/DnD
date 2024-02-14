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
  - This app is a tool for making characters with the assistance of AI. 
