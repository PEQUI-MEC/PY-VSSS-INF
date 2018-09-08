import time
from robot import Robot
from xbee import XBee
from serial import Serial
from digi.xbee.devices import XBeeDevice

class SerialCommunication():

	def __init__(self):
		self.xbee = None
		self.serial = None
		self.robots = Robot().robots

	def startBee(self, port, baud):
		self.serial = Serial(port, baud)
		self.xbee = XBee(self.serial)
		#return self.xbee

	def killBee(self):
		self.serial.close()

	def sendMessage(self, robotId, message):
		start_time = time.time()

		self.xbee.send("tx", frame = 'A',command='MY',dest_addr=self.robots[robotId],data=message)
		
		elapsed_time = time.time() - start_time

		print(str(robotId) + " " + str(elapsed_time))

		#return True

	def newRobot(letter, address):
		return True