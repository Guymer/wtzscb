#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.11/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import os

    # Import special modules ...
    try:
        import cartopy
        import cartopy.crs
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                   "backend" : "Agg",                                           # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                "figure.dpi" : 300,
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
        import pyguymer3.geo
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Configure Cartopy ...
    os.environ["CARTOPY_USER_BACKGROUNDS"] = os.getcwd()

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step1a.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step1a", resolution = "step1a")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[0.0, 6000.0]]), cmap = "jet")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Elevation [m]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, colorName = "white", resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step2a.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step2a", resolution = "step2a")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Time Until Sunrise After 12:00 UTC [hr]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, colorName = "white", resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step2b.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step2b", resolution = "step2b")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Time Until Noon After 12:00 UTC [hr]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, colorName = "white", resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step2c.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step2c", resolution = "step2c")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Time Until Sunset After 12:00 UTC [hr]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, colorName = "white", resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step3a.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step3a", resolution = "step3a")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Time Zone Difference From UTC [hr]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, colorName = "white", resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)

    # **************************************************************************

    # Define PNG file name and check if it exists already ...
    pfile = "step4a.png"
    if not os.path.exists(pfile):
        print(f"Making \"{pfile}\" ...")

        # Create figure ...
        fg = matplotlib.pyplot.figure(figsize = (9, 4))

        # Create axis ...
        ax = fg.add_subplot(projection = cartopy.crs.Robinson())

        # Configure axis ...
        ax.set_global()
        pyguymer3.geo.add_map_background(ax, name = "step4a", resolution = "step4a")

        # Add (fake) foreground images ...
        im = ax.imshow(numpy.array([[-3.0, 3.0]]), cmap = "seismic")
        im.set_visible(False)

        # Add colour bar ...
        cb = fg.colorbar(im, orientation = "vertical", ax = ax)

        # Configure colour bar ...
        cb.set_label("Difference Between Noon & Time Zone [hr]")

        # Configure axis ...
        pyguymer3.geo.add_coastlines(ax, resolution = "i")

        # Configure figure ...
        fg.tight_layout()

        # Save figure ...
        fg.savefig(pfile)
        matplotlib.pyplot.close(fg)

        # Optimize PNG ...
        pyguymer3.image.optimize_image(pfile, strip = True)
