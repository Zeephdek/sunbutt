import numpy as np
import json

global triEmptyArray
triEmptyArray = np.zeros([3])

def getSphr(cart=triEmptyArray):
    """
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#Conventions
    returns r, theta, phi (ISO/Physics convention), the latter 2 referring to elevation and azimuth
    cart should be a tuple (x,y,z)

    https://stackoverflow.com/questions/4116658/faster-numpy-cartesian-to-spherical-coordinate-conversion for non realtime use
    """

    x, y, z = cart[0], cart[1], cart[2]
    r = np.sqrt(x * x + y * y + z * z)
    if r == 0:
        return triEmptyArray

    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return np.array((r, theta, phi))

def printSph(sph):
    r, theta, phi = sph[0], np.degrees(sph[1]), np.degrees(sph[2])
    print("r = {:.1f} | θ = {:.3f} | φ = {:.3f}".format(r, theta, phi))

def getCart(sph=triEmptyArray):
    """
    sph is given in (r, theta, phi)
    returns (x, y, z)
    """

    r, theta, phi = sph[0], sph[1], sph[2]

    x = r * np.cos(phi) * np.sin(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(theta)

    return np.array((x, y, z))

def getDistance(a=triEmptyArray, b=triEmptyArray):
    """
    distance between points a and b.
    DISTANCE. For simple uses.
    """

    return np.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2 +
        (a[2]-b[2])**2
    )

def getDir(a=triEmptyArray, b=triEmptyArray):
    """
    Direction of b from a (aka vector AB)
    """
    return getSphr(b - a)

def jsonPrint(data, print_data=True):
    """It gets PRINTED. Otherwise, change `print_data`"""
    if print_data:
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        return json.dumps(data, indent=4, sort_keys=True)

### gravity calculations
def g_force(G, m_1, m_2, r):
    return G * m_1 * m_2 / (r**2)