import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

import PySpice
from PySpice.Spice.Netlist import Circuit

from PySpice.Unit import *

circuit = Circuit('Resistor Bridge')



circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.R(1, 1, 2, 2@u_kΩ)
circuit.R(2, 1, 3, 1@u_kΩ)
circuit.R(3, 2, circuit.gnd, 1@u_kΩ)
circuit.R(4, 3, circuit.gnd, 2@u_kΩ)
circuit.R(5, 3, 2, 2@u_kΩ)

print(circuit)

simulator = circuit.simulator(temperature=25)
print(simulator)

analysis = simulator.operating_point()
print(analysis)