#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import json
    import math
    import os
    import pathlib

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : pathlib.PosixPath("~/.local/share/cartopy").expanduser(),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
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
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Make a map of time zones.",
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
              category = "cultural",
                  name = "time_zones",
            resolution = "10m",
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
                            255.0 * tmzn[iy, ix] / 24.0,
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
