#!/usr/bin/env python3

# Import modules ...
import math
import numpy

# Import special modules ...
try:
    import cartopy
except:
    raise Exception("run \"pip install --user cartopy\"")

# ******************************************************************************

# Create list of cities of interest ...
cities = {
    "Beijing" : "CHN",
    "Berlin"  : "DEU",
    "Córdoba" : "ESP",
    "Kashgar" : "CHN",
    "Lisbon"  : "PRT",
    "London"  : "GBR",
    "Paris"   : "FRA",
    "Denver"  : "USA",
    "Warsaw"  : "POL",
}

# ******************************************************************************

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
    guess = 24.0 - diff[iy, ix]                                                 # [hr]
    guess_hr = int(math.floor(guess))                                           # [hr]
    guess_mn = int(round(60.0 * (guess % 1.0)))                                 # [min]

    print("{:3s} {:7s} {:02d}:{:02d} {:4.1f}".format(record.attributes["ADM0_A3"], record.attributes["name_en"], guess_hr, guess_mn, tmzn[iy, ix]))
