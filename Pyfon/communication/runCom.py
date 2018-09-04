from hermes import Hermes

hermes = Hermes("COM3")
hermes.sendMessage("HERCULES", "0.3;0.8")

for x in range(1,2):
	message = input('Enter your input:')
	hermes.sendMessage("HERCULES", message)
	