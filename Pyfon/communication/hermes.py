from serialCommunication import SerialCommunication

class Hermes():

	serialCom = SerialCommunication()

	def __init__(self, port, baud=115200):
		self.xbee = self.serialCom.startBee(port, baud)
		pass

	def startBee(port, baud):
		return True

	def killBee():
		serialCom.killBee()

	def sendMessage(self, robotId, message):
		return self.serialCom.sendMessage(robotId, message)

	def createMessage(i, lw, rw):
		return "0.3;0.8"

	def isBee(port_path):
		return True
