#!/usr/bin/env python3

# Define function ...
def horizon(e, /):
    # Import standard modules ...
    import math

    # Import special modules ...
    try:
        import ephem
    except:
        raise Exception("\"ephem\" is not installed; run \"pip install --user ephem\"") from None

    # Calculate the angle below horizontal down to the horizon due to the
    # observer being above the radius of the Earth ...
    return -math.acos(ephem.earth_radius / (e + ephem.earth_radius))            # [rad]
