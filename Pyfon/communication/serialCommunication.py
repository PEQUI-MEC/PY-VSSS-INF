import time
from xbee import XBee
from serial import Serial
from digi.xbee.devices import XBeeDevice

class SerialCommunication():

	def __init__(self):
		self.xbee = None
		self.serial = None
		self.messages = {}

	def startBee(self, port, baud):
		self.serial = Serial(port, baud)
		self.xbee = XBee(self.serial)
		return self.xbee

	def killBee(self):
		self.serial.close()

	def sendMessage(self, robotId, message):
		start_time = time.time()

		if robotId==1:
			self.xbee.send("tx", frame = 'A',command='MY',dest_addr='\x56\x0D',data=message)
		elif robotId==2:
			self.xbee.send("tx",frame = 'A',command='MY',dest_addr='\x6B\x0D',data=message)
		elif robotId==3:
			self.xbee.send("tx", frame = 'A',command='MY',dest_addr='\x21\x5C',data=message)
		else:
			raise ValueError("Robot ID not found")

		elapsed_time = time.time() - start_time

		print(str(robotId) + " " + str(elapsed_time))

		#return True

	def newRobot(letter, address):
		return True
