#!/bin/bash

# This script will run the setup needed for the mmorpdnd package!
if [[ $(uname) == Linux ]]; then
    echo "Running setup for Linux!"
    sudo apt-get install python3
    sudo apt-get install python3-pip
    sudo apt-get install python3-tk
    sudo apt-get install python3-pil python3-pil.imagetk
    pip3 install bs4
    pip install lxml
    pip3 install regex
    pip3 install BeautifulSoup
    pip3 install cssbeautifier
    pip3 install tqdm
    pip3 install pytube
    pip3 install moviepy
    pip3 install matplotlib
    pip3 install prettytable
    pip3 install networkx
    pip3 install plotly
    pip3 install scipy

else
    echo "Setup not yet configured for your system!"
fi
