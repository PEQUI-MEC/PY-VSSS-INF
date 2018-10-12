from hermes import Hermes
import time

hermes = Hermes("COM4")

for x in range(0,9):

    velocities = [
		[1, (x+1.0)/10.0,-(x+1.0)/10.0],
		[2, (x-3.0)/10.0, -(x-3.0)/10.0],
		[3,(x-6.0)/10.0, -(x-6.0)/10.0]
	]
    time.sleep(1)
    hermes.fly(velocities)