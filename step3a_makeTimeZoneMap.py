#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.11/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import math
    import os

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : os.path.expanduser("~/.local/share/cartopy_cache"),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                       "backend" : "Agg",                                       # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                    "figure.dpi" : 300,
                "figure.figsize" : (9.6, 7.2),                                  # NOTE: See https://github.com/Guymer/misc/blob/main/README.md#matplotlib-figure-sizes
                     "font.size" : 8,
            }
        )
        import matplotlib.pyplot
    except:
        raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None
    try:
        import numpy
    except:
        raise Exception("\"numpy\" is not installed; run \"pip install --user numpy\"") from None
    try:
        import shapely
        import shapely.geometry
    except:
        raise Exception("\"shapely\" is not installed; run \"pip install --user Shapely\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Load axes ...
    lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                      # [rad]
    lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                      # [rad]

    # **************************************************************************

    # Define BIN file name and check if it exists already ...
    bfile = "timeZone.bin"
    if not os.path.exists(bfile):
        print(f"Making \"{bfile}\" ...")

        # Make time zone map ...
        tmzn = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)         # [hr]

        # Create 2D list of Shapely points ...
        pnt = []
        for iy in range(lat.size):
            tmp = []
            for ix in range(lon.size):
                tmp.append(shapely.geometry.Point(math.degrees(lon[ix]), math.degrees(lat[iy])))
            pnt.append(tmp)

        # Find file containing all the country shapes ...
        sfile = cartopy.io.shapereader.natural_earth(
            resolution = "10m",
              category = "cultural",
                  name = "time_zones"
        )

        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neZone = pyguymer3.geo.getRecordAttribute(record, "ZONE")           # [hr]
            if neZone < 0.0:
                neZone += 24.0                                                  # [hr]

            # Loop over x-axis ...
            for ix in range(lon.size):
                # Loop over y-axis ...
                for iy in range(lat.size):
                    # Skip this pixel if it is not within the geometry ...
                    if not record.geometry.contains(pnt[iy][ix]):
                        continue

                    # Set pixel to time zone ...
                    tmzn[iy, ix] = neZone                                       # [hr]

        # Save time zone map ...
        tmzn.tofile(bfile)
    else:
        # Load time zone map ...
        tmzn = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "timeZone.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

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
        pyguymer3.image.save_array_as_PNG(img, pfile, ftype_req = 0)
        pyguymer3.image.optimize_image(pfile, strip = True)
