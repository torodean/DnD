# [MMORPDND]

# WARNING: If you are one of my DnD players, leave this repository now!

This application and software suite is designed for storage of DnD information with capabilities for automatic linking and organization. It contains various scripts and features for use. See the manual for a complete list and description of features.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

See the manual located in docs/ for a more comprehensive set of instructions!

Note: These installation instructions are for Linux based operating systems.

- Clone the git repo.
- Run the setup.sh script (sudo required for installations)
    - The `chmod a+x mmorpdnd-setup.sh` command makes the script executable, and `./mmorpdnd-setup.sh` runs the script.
- Run the desired application or sub-program.
    - The `chmod a+x app.py` command makes the script executable, and `./app.py` or `python3 app.py` runs the script.

## Usage

Each app serves a specific purpose and can be ran to accomplish that purpose. The `chmod a+x app.py` command makes an app executable. The apps can then either be ran via `./app.py` or `python3 app.py`.

## Features

See the manual located in docs/ for a list of features! This main repo contains various folders and scripts that have very specific purposes.

- campaign: This folder is the main database of information. It contains all the html files created by and formatted by the other scripts and tools.
- css: This folder contains the css for formatting the various html files.
- docs: This folder contains the main documentation for the entire MMORPDND project.
- scripts: This folder conains various automated pipeline scripts.
- templates: This folder contains various scripts and tools used for the MMORPDND system. It also contains the template files and input files that were used to create the campaign folder.
- mmorpdnd.py: This is the main python gui for formatting and updating linking (one of the main features of the MMORPDND system).
- mmorpdnd-setup.sh: This script is designed to help automate the setup of the MMORPDND system by installing dependencies that are used by the python scripts.
- link_scraper.py: This is a simple dev tool used for gathering links from various sources. This is part of an in development feature.
- printDirectoryStructure.py: This tool is used to print out the directory structure of the folders (mainly for testing).
- purge_index_files.py: This tool is used to delete/purge all the index files so they can be recreated.


## Contributing

See the home page at https://mmorpdnd.github.io/ for information on how to contribute to this project!

## License

TODO - [Information about the license under which the application is released, along with any relevant disclaimers or warranties] 

## Contact

Please send all comments or inquiries to mmorpdnd@gmail.com
