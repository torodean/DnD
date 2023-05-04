#!/bin/bash

# This script will run the setup needed for the mmorpdnd package!
if [[ $(uname) == Linux ]]; then
    echo "Running setup for Linux!"
    sudo apt-get install python3-pip
    pip3 install bs4
    pip3 install regex
    pip3 install BeautifulSoup
    pip3 install cssbeautifier
    sudo apt-get install python3-tk

else
    echo "Setup not yet configured for your system!"
fi
