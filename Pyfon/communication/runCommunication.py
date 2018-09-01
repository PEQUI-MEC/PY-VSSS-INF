from hermes import Hermes

hermes = Hermes("/dev/ttyUSB0")
hermes.sendMessage("HERCULES", "0.8;0.3")