#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import datetime
    import os

    # Import special modules ...
    try:
        import ephem
    except:
        raise Exception("\"ephem\" is not installed; run \"pip install --user ephem\"") from None
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
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # Import local modules ...
    import funcs

    # **************************************************************************

    # Load elevation map along with axes ...
    lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                      # [rad]
    lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                      # [rad]
    elev = numpy.fromfile("elev.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [m]

    # **************************************************************************

    # Define BIN file name and check if it exists already ...
    bfile = "noonDiff.bin"
    if not os.path.exists(bfile):
        print(f"Making \"{bfile}\" ...")

        # Make difference map ...
        diff = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)         # [hr]

        # Define the reference time as chronological noon on 20-March-2019 and
        # initialize observer ...
        ref = datetime.datetime(2019, 3, 20, 12, tzinfo = datetime.UTC)
        obs = ephem.Observer()
        obs.date = ephem.Date(ref)

        # Loop over x-axis ...
        for ix in range(lon.size):
            # Loop over y-axis ...
            for iy in range(lat.size):
                # Update the observer's position ...
                obs.lat = lat[iy]                                               # [rad]
                obs.long = lon[ix]                                              # [rad]
                obs.elevation = elev[iy, ix]                                    # [m]
                obs.horizon = funcs.horizon(elev[iy, ix])                       # [rad]

                # Find the next time that the Sun will cross the meridian (as an
                # 'aware' datetime object in UTC) ...
                noon = obs.next_transit(ephem.Sun()).datetime().replace(tzinfo = datetime.UTC)

                # Find out the difference from the reference time ...
                diff[iy, ix] = (noon - ref).total_seconds() / 3600.0            # [hr]

        # Save difference map ...
        diff.tofile(bfile)
    else:
        # Load difference map ...
        diff = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "noonDiff.png"
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
                val = min(1.0, max(0.0, diff[iy, ix] / 24.0))

                # Determine colours ...
                r, g, b, a = cm(val)

                # Set pixel ...
                img[iy, ix, 0] = 255.0 * r
                img[iy, ix, 1] = 255.0 * g
                img[iy, ix, 2] = 255.0 * b

        # Save PNG ...
        pyguymer3.image.save_array_as_PNG(img, pfile, ftype_req = 0)
        pyguymer3.image.optimize_image(pfile, strip = True)
