rm -rf dummy_directory
rm -rf *.html
Sleep 1
py createDirs.py
py createDummyHTMLFiles.py
py createIndexFiles.py
py updateHeaders.py
py updateNavigation.py
py updateIndexLinks.py
py fixCSSLinks.py
py prettyHTML.py
