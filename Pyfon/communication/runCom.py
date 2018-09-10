from hermes import Hermes
import time

hermes = Hermes("/dev/ttyUSB0")

velocities = [
	[1, 0.4,-0.4],
	[2, 0.7, -0.7],
	[3, 0.1, -0.1]
]

hermes.fly(velocities)