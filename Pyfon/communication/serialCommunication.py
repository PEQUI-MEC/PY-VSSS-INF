import time
from xbee import XBee
from serial import Serial
from digi.xbee.devices import XBeeDevice

class SerialCommunication():
	xbee = "not initialized"
	xbee2 = ""
	ser = ""
	def __init__(self):
		pass

	def startBee(self, port, baud):
		#xbee = XBeeDevice(port, baud)
		#xbee.open() 
		self.ser = Serial(port, baud)
		self.xbee2 = XBee(self.ser)
		#self.xbee = xbee
		
		return self.xbee2

	def killBee(self):
		self.ser.close()

	def sendMessage(self, robotId, message):
		start_time = time.time()

		if robotId==1:
			self.xbee2.tx(frame = 'A',command='MY',dest_addr='\x6B\x0D',data=message)
		elif robotId==2:
			self.xbee2.tx(frame = 'A',command='MY',dest_addr='\x56\xBC',data=message)
		else:
			self.xbee2.tx(frame = 'A',command='MY',dest_addr='\x21\x5C',data=message)

		elapsed_time = time.time() - start_time

		print(str(robotId) + " " + str(elapsed_time))

		return True

	def newRobot(letter, address):
		return True
