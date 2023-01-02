#!/usr/bin/env python3

# Import standard modules ...
import os

# Import special modules ...
try:
    import matplotlib
    matplotlib.use("Agg")                                                       # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
    import matplotlib.pyplot
    matplotlib.pyplot.rcParams.update({"font.size" : 8})
except:
    raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None
try:
    import numpy
except:
    raise Exception("\"numpy\" is not installed; run \"pip install --user numpy\"") from None

# Import my modules ...
try:
    import pyguymer3
    import pyguymer3.image
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Load both time maps along with axes ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [rad]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [rad]
diff = numpy.fromfile("noonDiff.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]
tmzn = numpy.fromfile("timeZone.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]

# ******************************************************************************

# Define BIN file name and check if it exists already ...
bfile = "timeZoneDiff.bin"
if not os.path.exists(bfile):
    print(f"Making \"{bfile}\" ...")

    # Make time zone difference map ...
    offs = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)             # [hr]

    # Loop over x-axis ...
    for ix in range(lon.size):
        # Loop over y-axis ...
        for iy in range(lat.size):
            # Calculate difference ...
            offs[iy, ix] = diff[iy, ix] + tmzn[iy, ix] - 24.0                   # [hr]

            # Make sure that the values loop back around correctly ...
            if offs[iy, ix] < -12.0:
                offs[iy, ix] += 24.0                                            # [hr]
            if offs[iy, ix] > +12.0:
                offs[iy, ix] -= 24.0                                            # [hr]

    # Save time zone difference map ...
    offs.tofile(bfile)
else:
    # Load time zone difference map ...
    offs = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "timeZoneDiff.png"
if not os.path.exists(pfile):
    print(f"Making \"{pfile}\" ...")

    # Create short-hand ...
    cm = matplotlib.pyplot.get_cmap("seismic")

    # Make image ...
    img = numpy.zeros((lat.size, lon.size, 3), dtype = numpy.uint8)

    # Loop over y-axis ...
    for iy in range(lat.size):
        # Loop over x-axis ...
        for ix in range(lon.size):
            # Find normalized value ...
            val = min(1.0, max(0.0, 0.5 + offs[iy, ix] / 6.0))

            # Determine colours ...
            r, g, b, a = cm(val)

            # Set pixel ...
            img[iy, ix, 0] = 255.0 * r
            img[iy, ix, 1] = 255.0 * g
            img[iy, ix, 2] = 255.0 * b

    # Save PNG ...
    pyguymer3.image.save_array_as_PNG(img, pfile, ftype_req = 0)
    pyguymer3.image.optimize_image(pfile, strip = True)
