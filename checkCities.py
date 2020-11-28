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
    return "{:02d}:{:02d}".format(hh, mm)

# Load axes and arrays ...
lon = numpy.fromfile("lon.bin", dtype = numpy.float64)                          # [rad]
lat = numpy.fromfile("lat.bin", dtype = numpy.float64)                          # [rad]
diff = numpy.fromfile("noonDiff.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]
tmzn = numpy.fromfile("timeZone.bin", dtype = numpy.float64).reshape(lat.size, lon.size)    # [hr]

# ******************************************************************************

# Find file containing all the country shapes ...
shape_file = cartopy.io.shapereader.natural_earth(
    resolution = "10m",
      category = "cultural",
          name = "populated_places"
)

# Loop over records ...
for record in cartopy.io.shapereader.Reader(shape_file).records():
    # Skip this record if it is not one of the cities of interest ...
    if record.attributes["NAME"] not in cities.keys():
        continue

    # Skip this record if it is not in the correct country ...
    if record.attributes["ADM0_A3"] != cities[record.attributes["NAME"]]:
        continue

    # Find its location and determine the closest pixel to it ...
    x = math.radians(record.geometry.x)                                         # [rad]
    y = math.radians(record.geometry.y)                                         # [rad]
    ix = abs(lon - x).argmin()
    iy = abs(lat - y).argmin()

    # Guess the correct time zone ...
    gues = 24.0 - diff[iy, ix]                                                  # [hr]

    print("{:7s} ({:3s}) is at {:6.1f}° and should be UTC+{:5s} but it is actually UTC+{:5s} because noon occurs {:5s} after 12:00 UTC.".format(record.attributes["name_en"], record.attributes["ADM0_A3"], math.degrees(x), flt2hhmm(gues), flt2hhmm(tmzn[iy, ix]), flt2hhmm(diff[iy, ix])))