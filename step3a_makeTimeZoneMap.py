#!/usr/bin/env python3

# Import modules ...
import math
import matplotlib
matplotlib.use("Agg")                                                           # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
import matplotlib.pyplot
import numpy
import os
import subprocess

# Import special modules ...
try:
    import cartopy
    import cartopy.io.shapereader
except:
    raise Exception("run \"pip install --user cartopy\"")
try:
    import shapely
except:
    raise Exception("run \"pip install --user shapely\"")

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH")

# ******************************************************************************

# Load axes ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [m]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [m]

# ******************************************************************************

# Define BIN file name and check if it exists already ...
bfile = "timeZone.bin"
if not os.path.exists(bfile):
    print("Making \"{:s}\" ...".format(bfile))

    # Map time zone map ...
    tmzn = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)             # [hr]

    # Create 2D list of Shapely points ...
    pnt = []
    for iy in range(lat.size):
        tmp = []
        for ix in range(lon.size):
            tmp.append(shapely.geometry.Point(math.degrees(lon[ix]), math.degrees(lat[iy])))
        pnt.append(tmp)

    # Find file containing all the country shapes ...
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "time_zones"
    )

    # Loop over records ...
    for record in cartopy.io.shapereader.Reader(shape_file).records():
        # Calculate offset ...
        off = record.attributes["zone"]                                         # [hr]
        if off < 0.0:
            off += 24.0                                                         # [hr]

        # Loop over x-axis ...
        for ix in range(lon.size):
            # Loop over y-axis ...
            for iy in range(lat.size):
                # Skip this pixel if it is not within the geometry ...
                if not record.geometry.contains(pnt[iy][ix]):
                    continue

                # Set pixel to time zone ...
                tmzn[iy, ix] = off                                              # [hr]

    # Save time zone map ...
    tmzn.tofile(bfile)
else:
    # Load time zone map
    tmzn = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "timeZone.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create short-hand ...
    cm = matplotlib.pyplot.get_cmap("jet")

    # Make image ...
    img = numpy.zeros((lat.size, lon.size, 3), dtype = numpy.uint8)

    # Loop over y-axis ...
    for iy in range(lat.size):
        # Loop over x-axis ...
        for ix in range(lon.size):
            # Find normalized value ...
            val = min(1.0, max(0.0, tmzn[iy, ix] / 24.0))

            # Determine colours ...
            r, g, b, a = cm(val)

            # Set pixel ...
            img[iy, ix, 0] = 255.0 * r
            img[iy, ix, 1] = 255.0 * g
            img[iy, ix, 2] = 255.0 * b

    # Save PNG ...
    pyguymer3.save_array_as_PNG(img, pfile, ftype_req = 0)
    subprocess.check_call(
        ["exiftool", "-overwrite_original", "-all=", pfile],
        stderr = open(os.devnull, "wt"),
        stdout = open(os.devnull, "wt")
    )
    subprocess.check_call(
        ["optipng", pfile],
        stderr = open(os.devnull, "wt"),
        stdout = open(os.devnull, "wt")
    )
