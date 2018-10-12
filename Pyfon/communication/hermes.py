import sys
from velocity import Velocity
from message import Message
from serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200):
		self.serialCom = SerialCommunication()
		self.messages = []
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
			],
			#robot 3
			[
				"id": robot_id
			 	"left_wheel": left_wheel_velocity
			 	"right_wheel": right_wheel_velocity
			],
		]
	'''
		self.startBee(port, baud)
			 	"right_wheel": right wheel_velocity

	def fly(self, velocities):
		self.createMessages(velocities)
		self.sendMessages()
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
		for message in self.messages:
			self.sendMessage(message)
	
	def sendMessage(self, message):
		return self.serialCom.sendMessage(message.robotId, message.message)

	def createMessages(self, velocities):
		for robot in velocities:
			self.createMessage(robot[0], robot[1], robot[2])
			#self.createMessage(robot.id, robot.left_wheel, robot.right_wheel)

	def createMessage(self, robotId, left_wheel, right_wheel):
		message = str(left_wheel) + ";" + str(right_wheel)
		self.messages.append(Message(robotId, message))
		return message

	def clearMessages(self):
		self.messages = []

	def isSerial(self, port):
		if sys.platform.startswith('linux'):
			if 'ttyUSB' in port:
				return True
		elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
			if 'COM' in port:	
				return True
		return False
