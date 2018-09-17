import sys
# from velocityInfo import VelocityInfo
# from messageInfo import MessageInfo
from .serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200):
		self.serialCom = SerialCommunication()
		self.startBee(port, baud)
		self.messages = []

		print("Hermes summoned.")
	'''
		#velocities should be received like:
		[	
			#robot 1
			[
				"id": robot_id
				"left_wheel": left_wheel_velocity
				"right_wheel": right_wheel_velocity
	    	],
	    	#robot 2
			[
				"id": robot_id
			 	"left_wheel": left_wheel_velocity
			 	"right_wheel": right wheel_velocity
			],
			#robot 3
			[
				"id": robot_id
			 	"left_wheel": left_wheel_velocity
			 	"right_wheel": right_wheel_velocity
			],
		]
	'''

	def fly(self, velocities):
		self.createMessages(velocities)
		self.sendMessages(messages)
		self.clearMessages()

	def startBee(self, port, baud):
		if self.isSerial(port):
			self.xbee = self.serialCom.startBee(port, baud)
			return "bee started!"
		else:
			return "bee was not started :("

	def killBee(self):
		self.serialCom.killBee()

	def sendMessages(self):
		for message in messages:
			self.serialCom.sendMessage(message)

		#rodar um for para enviar todas as mensagens, chamando o método sendMessage(self, robotId, message)
	
	def sendMessage(self, message):
		return self.serialCom.sendMessage(message)

	def createMessages(self, velocities):
		for robot in velocities:
			createMessage(robot.id, robot.left_wheel, robot.right_wheel)

	def createMessage(self, robotId, left_wheel, right_wheel):
		message = left_wheel + ";" + right_wheel
		messages.append(Message(robotId, message))
		return message

	def clearMessages():
		messages = []

	def isSerial(self, port):
		if sys.platform.startswith('linux'):
			if 'ttyUSB' in port:
				return True
		elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
			if 'COM' in port:	
				return True
		return False
