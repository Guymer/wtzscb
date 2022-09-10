#!/usr/bin/env python3

# Import standard modules ...
import math

# Import special modules ...
try:
    import cartopy
except:
    raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
try:
    import numpy
except:
    raise Exception("\"numpy\" is not installed; run \"pip install --user numpy\"") from None

# Import my modules ...
try:
    import pyguymer3
    import pyguymer3.geo
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Create list of cities of interest ...
cities = {
    "Beijing" : "CHN",
    "Berlin"  : "DEU",
    "Córdoba" : "ESP",
    "Denver"  : "USA",
    "Kashgar" : "CHN",
    "Lisbon"  : "PRT",
    "London"  : "GBR",
    "Madrid"  : "ESP",
    "Paris"   : "FRA",
    "Warsaw"  : "POL",
}

# ******************************************************************************

# Define function ...
def flt2hhmm(flt):
    hh = int(math.floor(flt))                                                   # [hr]
    mm = int(round(60.0 * (flt % 1.0)))                                         # [min]
    return f"{hh:02d}:{mm:02d}"

# Load axes and arrays ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [rad]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [rad]
diff = numpy.fromfile("noonDiff.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]
tmzn = numpy.fromfile("timeZone.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]

# ******************************************************************************

# Find file containing all the country shapes ...
sfile = cartopy.io.shapereader.natural_earth(
      category = "cultural",
          name = "populated_places",
    resolution = "10m",
)

# Loop over records ...
for record in cartopy.io.shapereader.Reader(sfile).records():
    # Create short-hands ...
    neA3 = pyguymer3.geo.getRecordAttribute(record, "ADM0_A3")
    neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

    # Skip this record if it is not one of the cities of interest ...
    if neName not in cities:
        continue

    # Skip this record if it is not in the correct country ...
    if neA3 != cities[neName]:
        continue

    # Find its location and determine the closest pixel to it ...
    x = math.radians(record.geometry.x)                                         # [rad]
    y = math.radians(record.geometry.y)                                         # [rad]
    ix = abs(lon - x).argmin()
    iy = abs(lat - y).argmin()

    # Guess the correct time zone ...
    gues = 24.0 - diff[iy, ix]                                                  # [hr]

    print(f"{neName:7s} ({neA3:3s}) is at {math.degrees(x):6.1f}° and should be UTC+{flt2hhmm(gues):5s} but it is actually UTC+{flt2hhmm(tmzn[iy, ix]):5s} because noon occurs {flt2hhmm(diff[iy, ix]):5s} after 12:00 UTC.")
