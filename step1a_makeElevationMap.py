#!/usr/bin/env python3

# Import standard modules ...
import math
import os
import zipfile

# Import special modules ...
try:
    import matplotlib
    matplotlib.use("Agg")                                                       # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
    import matplotlib.pyplot
except:
    raise Exception("run \"pip install --user matplotlib\"")
try:
    import numpy
except:
    raise Exception("run \"pip install --user numpy\"")

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH")

# ******************************************************************************

# Check if the BIN file does not exist yet ...
if not os.path.exists("elev.bin"):
    print("Making \"elev.bin\" ...")

    # Set raw elevation map size and the scale that everything else will be done
    # at ...
    nx = 43200                                                                  # [px]
    ny = 21600                                                                  # [px]
    sc = 100
    if nx % sc != 0:
        raise Exception("\"nx\" must be an integer multiple of \"sc\"")
    if ny % sc != 0:
        raise Exception("\"ny\" must be an integer multiple of \"sc\"")

    # Define tile names ...
    tiles = [
        "all10/a11g",
        "all10/b10g",
        "all10/c10g",
        "all10/d10g",
        "all10/e10g",
        "all10/f10g",
        "all10/g10g",
        "all10/h10g",
        "all10/i10g",
        "all10/j10g",
        "all10/k10g",
        "all10/l10g",
        "all10/m10g",
        "all10/n10g",
        "all10/o10g",
        "all10/p10g",
    ]

    # Initialize arrays ...
    lon = numpy.zeros(nx // sc, dtype = numpy.float64)                          # [rad]
    lat = numpy.zeros(ny // sc, dtype = numpy.float64)                          # [rad]
    raw = numpy.zeros((ny, nx), dtype = numpy.int16)                            # [m]
    elev = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)             # [m]

    # Load dataset ...
    with zipfile.ZipFile("all10g.zip", "r") as fobj:
        # Initialize index ...
        iy = 0                                                                  # [px]

        # Loop over y-axis ...
        for i in range(4):
            # Initialize index ...
            ix = 0                                                              # [px]

            # Loop over x-axis ...
            for j in range(4):
                # Define tile size ...
                if i == 0 or i == 3:
                    ncols = 4800                                                # [px]
                else:
                    ncols = 6000                                                # [px]
                nrows = 10800                                                   # [px]

                # Load tile and fill map ...
                raw[iy:iy + ncols, ix:ix + nrows] = numpy.frombuffer(
                    fobj.read(tiles[j + i * 4]),
                    dtype = numpy.int16
                ).reshape(ncols, nrows)[:, :]                                   # [m]

                # Increment index ...
                ix += nrows                                                     # [px]

            # Increment index ...
            iy += ncols                                                         # [px]

    # Rise everywhere up to sea level ...
    numpy.place(raw, raw < 0, 0)                                                # [m]

    # Scale the elevation map ...
    for ix in range(lon.size):
        for iy in range(lat.size):
            elev[iy, ix] = raw[sc * iy:sc * (iy + 1), sc * ix:sc * (ix + 1)].sum()  # [m]
    elev /= float(sc * sc)                                                      # [m]

    # Make longitude axis ...
    for ix in range(lon.size):
        lon[ix] = math.radians(360.0 * (float(ix) + 0.5) / float(lon.size) - 180.0) # [deg]

    # Make latitude axis ...
    for iy in range(lat.size):
        lat[lat.size - 1 - iy] = math.radians(180.0 * (float(iy) + 0.5) / float(lat.size) - 90.0)   # [deg]

    # Save elevation map along with axes ...
    lon.tofile("lon.bin")
    lat.tofile("lat.bin")
    elev.tofile("elev.bin")
else:
    # Load elevation map along with axes ...
    lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                      # [rad]
    lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                      # [rad]
    elev = numpy.fromfile("elev.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [m]

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "elev.png"
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
            val = min(1.0, max(0.0, elev[iy, ix] / 6000.0))

            # Determine colours ...
            r, g, b, a = cm(val)

            # Set pixel ...
            img[iy, ix, 0] = 255.0 * r
            img[iy, ix, 1] = 255.0 * g
            img[iy, ix, 2] = 255.0 * b

    # Save PNG ...
    pyguymer3.save_array_as_PNG(img, pfile, ftype_req = 0)
    pyguymer3.exiftool(img)
    pyguymer3.optipng(img)
