#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import json
    import os

    # Import special modules ...
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

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Make a map of the difference between noon and the time zone.",
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
    coolwarm = numpy.array(colourTables["coolwarm"]).astype(numpy.uint8)

    # **************************************************************************

    # Load both time maps along with axes ...
    lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                      # [rad]
    lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                      # [rad]
    diff = numpy.fromfile("noonDiff.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]
    tmzn = numpy.fromfile("timeZone.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]

    # **************************************************************************

    # Define BIN file name and check if it exists already ...
    bfile = "timeZoneDiff.bin"
    if not os.path.exists(bfile):
        print(f"Making \"{bfile}\" ...")

        # Make time zone difference map ...
        offs = numpy.zeros((lat.size, lon.size), dtype = numpy.float64)         # [hr]

        # Loop over x-axis ...
        for ix in range(lon.size):
            # Loop over y-axis ...
            for iy in range(lat.size):
                # Calculate difference ...
                offs[iy, ix] = diff[iy, ix] + tmzn[iy, ix] - 24.0               # [hr]

                # Make sure that the values loop back around correctly ...
                if offs[iy, ix] < -12.0:
                    offs[iy, ix] += 24.0                                        # [hr]
                if offs[iy, ix] > +12.0:
                    offs[iy, ix] -= 24.0                                        # [hr]

        # Save time zone difference map ...
        offs.tofile(bfile)
    else:
        # Load time zone difference map ...
        offs = numpy.fromfile(bfile, dtype = numpy.float64).reshape(lat.size, lon.size) # [hr]

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "timeZoneDiff.png"
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
                            255.0 * (0.5 + offs[iy, ix] / 6.0),
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
                palUint8 = coolwarm,
              strategies = None,
                  wbitss = [15,],
        )
        with open(pfile, "wb") as fObj:
            fObj.write(src)
