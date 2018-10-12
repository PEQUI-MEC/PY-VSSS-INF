import sys
from communication.velocity import Velocity
from communication.message import Message
from communication.serialCommunication import SerialCommunication

class Hermes():

	def __init__(self, port, baud=115200):
		self.serialCom = SerialCommunication()
		self.messages = []
		self.startBee(port, baud)
	'''
		#velocities should be received like:
		[	
			#robot 1
			[
				robot_id,
				left_wheel_velocity,
				right_wheel_velocity
	    	],
	    	#robot 2
			[
				robot_id,
			 	left_wheel_velocity,
			 	right wheel_velocity
			],
			#robot 3
			[
				robot_id
			 	left_wheel_velocity
			 	right_wheel_velocity
			],
		]
		'''	
		
	""" Main class method
		
		Receive velocities and manipulate, invoking create,
		send and clear methods.

        Args:
            velocities (vector): All robot velocities

        Returns:

    """
	def fly(self, velocities):
		self.createMessages(velocities)
		self.sendMessages()
		self.clearMessages()

	""" Start xBee connection
		
		Verifies if port is serial, invoking isSerial() and
		create a xbee connection with serialCommunication method
		startBee.

        Args:
            port (string): Computer serial port
            baud (int): transmission speed

        Returns: string containing sucess or failure

    """
	def startBee(self, port, baud):
		if self.isSerial(port):
			self.xbee = self.serialCom.startBee(port, baud)
			return "bee started!"
		else:
			return "bee was not started :("

	""" Close xBee connection
		
		Invokes killBee method from serialCommunication

        Args:

        Returns:

    """
	def killBee(self):
		self.serialCom.killBee()

	""" Send messages
		
		Use messages vector and call sendMessage() method 

        Args:

        Returns:

    """
	def sendMessages(self):
		for message in self.messages:
			self.sendMessage(message)
	
	""" Send message
		
		Receives message, send to robot using serialCommunication
		method sendMessage()

        Args:
            message (Message): Message object to be sent

        Returns:

    """
	def sendMessage(self, message):
		return self.serialCom.sendMessage(message.robotId, message.message)
    
    """ Create all messages
		
		Receives velocities vector and manipulate information creating messages
		for all robots using createMessage() method.
		method sendMessage

        Args:
            message (Message): Message object to be sent

        Returns:

    """
	def createMessages(self, velocities):
		for robot in velocities:
			self.createMessage(robot[0], robot[1], robot[2])
			#self.createMessage(robot.id, robot.left_wheel, robot.right_wheel)

	""" Create a message
		
		Receives robotId, and both wheels velocity, creating a string and 
		putting into messages vector.

        Args:
            robotId (id): Robot id
            left_wheel (float): left wheel velocity
            right_wheel (float): right wheel velocity

        Returns: a string containing created message

    """
	def createMessage(self, robotId, left_wheel, right_wheel):
		message = str(left_wheel) + ";" + str(right_wheel)
		self.messages.append(Message(robotId, message))
		return message
	
	"""Messages vector cleaner
		
		Clear messages vector, to ensure that none messages still are stored.
        
        Args:
        
        Returns:

    """
	def clearMessages(self):
		self.messages = []

	"""Verifies if is Serial port
		
		Based on operation system, verifies if port is serial using ttyUSB or COM patterns
		
		Args:
        
        Returns: Boolean, true if is serial port
        				  false if is not

    """
	def isSerial(self, port):
		if sys.platform.startswith('linux'):
			if 'ttyUSB' in port:
				return True
		elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
			if 'COM' in port:	
				return True
		return False
