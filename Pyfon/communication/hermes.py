from serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200, battery=None):
		self.battery = battery
		self.serialCom = SerialCommunication()
		self.xbee = self.serialCom.startBee(port, baud)
		self.messages = {}
	
	def fly(self, velocities):
		self.createMessage(velocities)
		self.sendMessage(messages)
		return

	def startBee(port, baud):
		return True

	def killBee(self):
		self.serialCom.killBee()

	def sendMessage(self, robotId, message):
		return self.serialCom.sendMessage(robotId, message)

	def createMessage(i, lw, rw):
		return "0.3;0.8"

	def isBee(port_path):
		return True
