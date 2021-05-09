#!/usr/bin/env python3

# Import standard modules ...
import math
import os

# Import special modules ...
try:
    import cartopy
    import cartopy.io
    import cartopy.io.shapereader
except:
    raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
try:
    import matplotlib
    matplotlib.use("Agg")                                                       # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
    import matplotlib.pyplot
except:
    raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None
try:
    import numpy
except:
    raise Exception("\"numpy\" is not installed; run \"pip install --user numpy\"") from None
try:
    import shapely
except:
    raise Exception("\"shapely\" is not installed; run \"pip install --user Shapely\"") from None

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Load axes ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [rad]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [rad]

# ******************************************************************************

# Define BIN file name and check if it exists already ...
bfile = "timeZone.bin"
if not os.path.exists(bfile):
    print("Making \"{:s}\" ...".format(bfile))

    # Make time zone map ...
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
    # Load time zone map ...
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
    pyguymer3.optimize_image(pfile, strip = True)
