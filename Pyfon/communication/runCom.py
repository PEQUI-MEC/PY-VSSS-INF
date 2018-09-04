from hermes import Hermes
import time

hermes = Hermes("/dev/ttyUSB0")


for x in range(0,9):

	if x%2==0:
		message = "0."+str(x) +";"+ "-0." + str(x)
	else:
		message = "-0."+str(x) +";"+ "-0." + str(x) 
	hermes.sendMessage(1, message)
	#time.sleep(1)
	hermes.sendMessage(2, message)
	#time.sleep(1)
	hermes.sendMessage(3, message)
	time.sleep(0.1)

hermes.killBee()