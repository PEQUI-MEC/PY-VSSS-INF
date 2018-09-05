from serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200, battery=None):
		self.battery = battery
		self.serialCom = SerialCommunication()
		self.xbee = self.serialCom.startBee(port, baud)
		self.messages = {}
	
	def fly(self, velocities):
		self.createMessages(velocities)
		self.sendMessages(messages)
		return

	def startBee(port, baud):
		return True

	def killBee(self):
		self.serialCom.killBee()

	def sendMessages(self):
		# rodar um for para enviar todas as mensagens, chamando o método sendMessage(self, robotId, message)
	def sendMessage(self, robotId, message):
		return self.serialCom.sendMessage(robotId, message)

	def createMessages(velocities):
		for robotId in range(0,3):
			if velocities[robotId] == None :
				continue

			createMessage(robotId, velocities[robotId].left_wheel, velocities[robotId].right_wheel)

	def createMessage(robotId, left_wheel, right_wheel):
		messages[i] = left_wheel + ";" + right_wheel
		return messages[robotId]

	def isBee(port_path):
		return True
