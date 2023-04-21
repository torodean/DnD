#!/bin/bash

if [[ $(uname) == CYGWIN* ]]; then
    echo "Running in Cygwin"
	py createIndexFiles.py
	py updateHeaders.py
	py updateNavigation.py
	py updateIndexLinks.py
	py fixCSSLinks.py
	py prettyHTML.py
else
    echo "Running in Linux terminal"
fi
