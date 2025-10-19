#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import json
    import datetime
    import os

    # Import special modules ...
    try:
        import ephem
    except:
        raise Exception("\"ephem\" is not installed; run \"pip install --user ephem\"") from None
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

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Make a map of the difference between 12 o'clock UTC and sunset.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action = "store_true",
          help = "print debug messages",
    )
    args = parser.parse_args()

    # **************************************************************************

    # Load colour tables and create short-hand ...
    with open(f"{pyguymer3.__path__[0]}/data/json/colourTables.json", "rt", encoding = "utf-8") as fObj:
        colourTables = json.load(fObj)
    turbo = numpy.array(colourTables["turbo"]).astype(numpy.uint8)

    # **************************************************************************

    # Load elevation map along with axes ...
    lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                      # [rad]
    lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                      # [rad]
    elev = numpy.fromfile("elev.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [m]

    # **************************************************************************

    # Define BIN file name and check if it exists already ...
    bfile = "sunsetDiff.bin"
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

                # Find the next time that the Sun will set (as an 'aware'
                # datetime object in UTC) ...
                try:
                    noon = obs.next_setting(ephem.Sun()).datetime().replace(tzinfo = datetime.UTC)
                except ephem.AlwaysUpError:
                    diff[iy, ix] = -1.0                                         # [hr]
                    continue

                # Find out the difference from the reference time ...
                diff[iy, ix] = (noon - ref).total_seconds() / 3600.0            # [hr]

        # Save difference map ...
        diff.tofile(bfile)
    else:
        # Load difference map ...
        diff = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "sunsetDiff.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Make image ...
        img = numpy.zeros(
            (lat.size, lon.size, 1),
            dtype = numpy.uint8,
        )

        # Loop over y-axis ...
        for iy in range(lat.size):
            # Loop over x-axis ...
            for ix in range(lon.size):
                # Set pixel ...
                img[iy, ix, 0] = numpy.uint8(
                    min(
                        255.0,
                        max(
                            0.0,
                            255.0 * diff[iy, ix] / 24.0,
                        ),
                    )
                )

        # Save PNG ...
        src = pyguymer3.image.makePng(
            img,
            calcAdaptive = True,
             calcAverage = True,
                calcNone = True,
               calcPaeth = True,
                 calcSub = True,
                  calcUp = True,
                 choices = "all",
                   debug = args.debug,
                     dpi = None,
                  levels = [9,],
               memLevels = [9,],
                 modTime = None,
                palUint8 = turbo,
              strategies = None,
                  wbitss = [15,],
        )
        with open(pfile, "wb") as fObj:
            fObj.write(src)
