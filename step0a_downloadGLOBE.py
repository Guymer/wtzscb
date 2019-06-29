#!/usr/bin/env python3

# Import modules ...
import os

# Import special modules ...
try:
    import requests
except:
    raise Exception("run \"pip install --user requests\"")

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH")

# ******************************************************************************

# Check if the ZIP file does not exist yet ...
if not os.path.exists("all10g.zip"):
    print("Downloading \"all10g.zip\" ...")

    # Start session ...
    sess = requests.Session()
    sess.allow_redirects = True
    sess.max_redirects = 5

    # Download the ZIP file ...
    if not pyguymer3.download_file(sess, "https://www.ngdc.noaa.gov/mgg/topo/DATATILES/elev/all10g.zip", "all10g.zip"):
        raise Exception("download failed", "https://www.ngdc.noaa.gov/mgg/topo/DATATILES/elev/all10g.zip")

    # End session ...
    sess.close()
