#!/usr/bin/env python3

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
    matplotlib.use("Agg")                                                       # NOTE: https://matplotlib.org/gallery/user_interfaces/canvasagg.html
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
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Configure cartopy ...
os.environ["CARTOPY_USER_BACKGROUNDS"] = os.getcwd()

# Configure matplotlib ...
matplotlib.pyplot.rcParams.update({"font.size" : 8})

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step1a.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step1a", resolution = "step1a")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[0.0, 6000.0]]), cmap = "jet")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Elevation [m]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "white", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step2a.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step2a", resolution = "step2a")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Time Until Sunrise After 12:00 UTC [hr]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "white", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step2b.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step2b", resolution = "step2b")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Time Until Noon After 12:00 UTC [hr]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "white", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step2c.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step2c", resolution = "step2c")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Time Until Sunset After 12:00 UTC [hr]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "white", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step3a.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step3a", resolution = "step3a")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[0.0, 24.0]]), cmap = "jet")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Time Zone Difference From UTC [hr]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "white", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)

# ******************************************************************************

# Define PNG file name and check if it exists already ...
pfile = "step4a.png"
if not os.path.exists(pfile):
    print("Making \"{:s}\" ...".format(pfile))

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (9, 4), dpi = 300)
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()

    # Add background images ...
    pyguymer3.add_map_background(ax, name = "step4a", resolution = "step4a")

    # Add (fake) foreground images ...
    im = ax.imshow(numpy.array([[-3.0, 3.0]]), cmap = "seismic")
    im.set_visible(False)

    # Add colorbars ...
    cb = matplotlib.pyplot.colorbar(im, orientation = "vertical", ax = ax)
    cb.set_label("Difference Between Noon & Time Zone [hr]")

    # Add coastlines ...
    ax.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

    # Save plot ...
    fg.savefig(pfile, bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.optimize_image(pfile, strip = True)
    matplotlib.pyplot.close(fg)
