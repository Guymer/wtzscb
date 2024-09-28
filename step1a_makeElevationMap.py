#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import math
    import os
    import zipfile

    # Import special modules ...
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

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Check if the BIN file does not exist yet ...
    if not os.path.exists("elev.bin"):
        print("Making \"elev.bin\" ...")

        # Define constants ...
        bins = [
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
        nx = 43200                                                              # [px]
        ny = 21600                                                              # [px]

        # Make map ...
        elev = numpy.zeros((ny, nx), dtype = numpy.int16)                       # [m]

        # Set the scale that everything else will be done at ...
        sc = 100
        if nx % sc != 0:
            raise Exception("\"nx\" must be an integer multiple of \"sc\"") from None
        if ny % sc != 0:
            raise Exception("\"ny\" must be an integer multiple of \"sc\"") from None

        # Initialize arrays ...
        lon = numpy.zeros(nx // sc, dtype = numpy.float64)                      # [rad]
        lat = numpy.zeros(ny // sc, dtype = numpy.float64)                      # [rad]
        scElev = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)       # [m]

        # Load dataset ...
        with zipfile.ZipFile("all10g.zip", "r") as fObj:
            # Initialize index ...
            iy = 0                                                              # [px]

            # Loop over y-axis ...
            for i in range(4):
                # Initialize index ...
                ix = 0                                                          # [px]

                # Loop over x-axis ...
                for j in range(4):
                    # Define tile size ...
                    if i in [0, 3]:
                        nrows = 4800                                            # [px]
                    else:
                        nrows = 6000                                            # [px]
                    ncols = 10800                                               # [px]

                    # Load tile ...
                    tile = numpy.frombuffer(
                        fObj.read(bins[j + i * 4]),
                        dtype = numpy.int16
                    ).reshape(nrows, ncols)                                     # [m]

                    # Fill map ...
                    elev[iy:iy + tile.shape[0], ix:ix + tile.shape[1]] = tile[:, :] # [m]

                    # Increment index ...
                    ix += ncols                                                 # [px]

                # Increment index ...
                iy += nrows                                                     # [px]

        # Rise everywhere up to sea level ...
        numpy.place(elev, elev < 0, 0)                                          # [m]

        # Scale the elevation map ...
        for ix in range(lon.size):
            for iy in range(lat.size):
                scElev[iy, ix] = elev[sc * iy:sc * (iy + 1), sc * ix:sc * (ix + 1)].sum()   # [m]
        scElev /= float(sc * sc)                                                # [m]

        # Make longitude axis ...
        for ix in range(lon.size):
            lon[ix] = math.radians(360.0 * (float(ix) + 0.5) / float(lon.size) - 180.0) # [°]

        # Make latitude axis ...
        for iy in range(lat.size):
            lat[lat.size - 1 - iy] = math.radians(180.0 * (float(iy) + 0.5) / float(lat.size) - 90.0)   # [°]

        # Save elevation map along with axes ...
        lon.tofile("lon.bin")
        lat.tofile("lat.bin")
        scElev.tofile("elev.bin")
    else:
        # Load elevation map along with axes ...
        lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                  # [rad]
        lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                  # [rad]
        scElev = numpy.fromfile("elev.bin", dtype = numpy.float64).reshape(lat.size, lon.size)  # [m]

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "elev.png"
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
                val = min(1.0, max(0.0, scElev[iy, ix] / 6000.0))

                # Determine colours ...
                r, g, b, a = cm(val)

                # Set pixel ...
                img[iy, ix, 0] = 255.0 * r
                img[iy, ix, 1] = 255.0 * g
                img[iy, ix, 2] = 255.0 * b

        # Save PNG ...
        pyguymer3.image.save_array_as_PNG(img, pfile, ftype_req = 0)
        pyguymer3.image.optimize_image(pfile, strip = True)
