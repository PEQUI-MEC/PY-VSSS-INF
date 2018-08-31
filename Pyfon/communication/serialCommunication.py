from digi.xbee.devices import XBeeDevice

class SerialCommunication():
	
	def startBee(port_path, baud_rate):
		xbee = XBeeDevice(port, baud_rate)
		xbee.open()
		return xbee

	def sendMessage(id, message):
		return True

	def newRobot(letter, address):
		return True
