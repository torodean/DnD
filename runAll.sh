rm -rf dummy_directory
rm -rf *.html
Sleep 1
py createDummyDirs.py
Sleep 1
py createDummyHTMLFiles.py
Sleep 1
py updateHeaders.py
Sleep 1
py fixCSSLinks.py
Sleep 1
py updateNavigation.py
Sleep 1
py updateIndexLinks.py
Sleep 1
py prettyHTML.py
