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
		xbee = XBeeDevice(port, baud)
		#xbee.open() 
		self.ser = Serial(port, baud)
		xbee2 = XBee(self.ser)
		self.xbee = xbee
		
		return xbee

	def killBee(self):

		pass

	def sendMessage(self, robotId, message):
		xbee_network = self.xbee.get_network()
		remote_device = xbee_network.discover_device(robotId)
		
		if remote_device is None:
			return False
		
		print("Sending data to %s-[%s] >> %s..." % (robotId, remote_device.get_64bit_addr(), message))
		


		self.xbee.set_sync_ops_timeout(15)
		
		start_time = time.time()
		self.xbee2.send("tx", command="MY",dest_addr=remote_device.get_16bit_addr(),data=message)
		#self.xbee.send_data(remote_device, message)
		print(xbee.wait_read_frame())		
		elapsed_time = time.time() - start_time
		print(elapsed_time)	
		self.ser.close()

		return True

	def newRobot(letter, address):
		return True
