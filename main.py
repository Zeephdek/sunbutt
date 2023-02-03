import numpy as np
import random as rand


from bodies import *
from utils import *
from constants import * 
from plotter import *

"""

     _______. __    __  .__   __. .______    __    __  .___________.___________.
    /       ||  |  |  | |  \ |  | |   _  \  |  |  |  | |           |           |
   |   (----`|  |  |  | |   \|  | |  |_)  | |  |  |  | `---|  |----`---|  |----`
    \   \    |  |  |  | |  . `  | |   _  <  |  |  |  |     |  |        |  |     
.----)   |   |  `--'  | |  |\   | |  |_)  | |  `--'  |     |  |        |  |     
|_______/     \______/  |__| \__| |______/   \______/      |__|        |__|     

                         _ _           _ 
                        (_) |         | |
 _ __ _____   _____  ___ _| |_ ___  __| |
| '__/ _ \ \ / / _ \/ __| | __/ _ \/ _` |
| | |  __/\ V /  __/\__ \ | ||  __/ (_| |
|_|  \___| \_/ \___||___/_|\__\___|\__,_|


Assumptions for Fucking simplicity's sake.
- Longitude of ascending nodes are assumed to be 0 
    - hence unless defined separately all bodies start at the sun's equator (I know this would be wrong but hey)                                                                    
- All initial distances of satelites from their planets are to be assumed as their periapsis
    - [for known celestial objects]
"""

sim_length = 365*24*3600
sim_interval = 0.1001*24*3600/25


def main():
    sol = system()
    sol.createBody(name="sun", mass=sun_mass)

    #Earth SETUP
    sol.createBody(
        name="earth", mass=earth_mass,
        pos_sphr=(
            earth_Pe,
            np.radians(90.000000001),
            0),
        vel_sphr=(
            earth_spd_Pe,
            np.radians(90-earth_incl),
            np.radians(90.0000000001))
        )
    sol.createBody(
        name="moon", mass=moon_mass,
        pos_sphr=(
            earth_Pe-moon_Pe,
            np.radians(90.000000001),
            0),
        vel_sphr=(
            earth_spd_Pe-moon_spd_avr,
            np.radians(90-earth_incl),
            np.radians(90.0000000001))
        )
    

    # info = sol.bodies[1].returnCurrentBodyInfo()
    # jsonPrint(info)
    sol.startSim(length=sim_length, interval=sim_interval)

    plotter = dataPlot(system=sol)
    # plotter.plotPaths()
    plotter.plotData()


if __name__ == "__main__":
    main()