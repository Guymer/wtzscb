#!/usr/bin/env python3

# Import standard modules ...
import os
import subprocess

# Import special modules ...
try:
    import cartopy
    import cartopy.crs
except:
    raise Exception("run \"pip install --user cartopy\"")
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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))

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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))

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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))

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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))

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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))

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
    matplotlib.pyplot.close("all")
    subprocess.check_call(["exiftool", "-overwrite_original", "-all=", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))
    subprocess.check_call(["optipng", pfile], stderr = open(os.devnull, "wt"), stdout = open(os.devnull, "wt"))