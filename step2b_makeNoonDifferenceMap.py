#!/usr/bin/env python3

# Import standard modules ...
import datetime
import math
import os

# Import special modules ...
try:
    import ephem
except:
    raise Exception("run \"pip install --user ephem\"")
try:
    import matplotlib
    matplotlib.use("Agg")                                                       # NOTE: https://matplotlib.org/gallery/user_interfaces/canvasagg.html
    import matplotlib.pyplot
except:
    raise Exception("run \"pip install --user matplotlib\"")
try:
    import numpy
except:
    raise Exception("run \"pip install --user numpy\"")
try:
    import pytz
except:
    raise Exception("run \"pip install --user pytz\"")

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Define functions ...
def horizon(e):
    # Calculate the angle below horizontal down to the horizon due to the
    # observer being above the radius of the Earth ...
    return -math.acos(ephem.earth_radius / (e + ephem.earth_radius))            # [rad]

# ******************************************************************************

# Load elevation map along with axes ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [rad]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [rad]
elev = numpy.fromfile("elev.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [m]

# ******************************************************************************

# Define BIN file name and check if it exists already ...
bfile = "noonDiff.bin"
if not os.path.exists(bfile):
    print("Making \"{:s}\" ...".format(bfile))

    # Make difference map ...
    diff = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)             # [hr]

    # Define the reference time as chronological noon on 20-March-2019 and
    # initialize observer ...
    ref = datetime.datetime(2019, 3, 20, 12, tzinfo = datetime.timezone.utc)
    obs = ephem.Observer()
    obs.date = ephem.Date(ref)

    # Loop over x-axis ...
    for ix in range(lon.size):
        # Loop over y-axis ...
        for iy in range(lat.size):
            # Update the observer's position ...
            obs.lat = lat[iy]                                                   # [rad]
            obs.long = lon[ix]                                                  # [rad]
            obs.elevation = elev[iy, ix]                                        # [m]
            obs.horizon = horizon(elev[iy, ix])                                 # [rad]

            # Find the next time that the Sun will cross the meridian ...
            noon = pytz.timezone("UTC").localize(obs.next_transit(ephem.Sun()).datetime())

            # Find out the difference from the reference time ...
            diff[iy, ix] = (noon - ref).total_seconds() / 3600.0                # [hr]

    # Save difference map ...
    diff.tofile(bfile)
else:
    # Load difference map ...
    diff = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size)   # [hr]

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "noonDiff.png"
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
            val = min(1.0, max(0.0, diff[iy, ix] / 24.0))

            # Determine colours ...
            r, g, b, a = cm(val)

            # Set pixel ...
            img[iy, ix, 0] = 255.0 * r
            img[iy, ix, 1] = 255.0 * g
            img[iy, ix, 2] = 255.0 * b

    # Save PNG ...
    pyguymer3.save_array_as_PNG(img, pfile, ftype_req = 0)
    pyguymer3.optimize_image(pfile, strip = True)
