from serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200):
		xbee = SerialCommunication.startBee(port, baud)
		pass

	def startBee(port, baud):
		return True

	def sendMessage(id, message):
		return True

	def createMessage(i, lw, rw):
		return "0.3;0.8"

	def isBee(port_path):
		return True
