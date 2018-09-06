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
		for robot in velocities:
			createMessage(robot.id, velocity.left_wheel, robot.right_wheel)

	def createMessage(robotId, left_wheel, right_wheel):
		message = left_wheel + ";" + right_wheel
		messages.append(robotId, message)
		return message

	def clearMessages():
		messages = {}
	def isBee(port_path):
		return True
