import unittest
import sys
sys.path.append("../")
from communication.hermes import Hermes
from communication.serial_communication import SerialCommunication

class CommunicationTest(unittest.TestCase):

	def testStartBee(self):
		self.assertEqual(Hermes.startBee("endereço_porta_usb",115200), True)

	def testCreateMessage(self):
		self.assertEqual(Hermes.createMessage(1, 0.3, 0.8), "0.3;0.8")
		#self.assertEqual(hermes.createMessage(2, 0.1, 0.3), "0.1;0.3")
		#self.assertEqual(hermes.createMessage(3, 0.5, 0.7), "0.5;0.7")
		#self.assertEqual(hermes.createMessage(13, 0.3, 0.1), "invalid")


	#unicast
	def testSendMessage(self):
		self.assertEqual(Hermes.sendMessage(1, "0.7;0.6"), True)
		#self.assertEqual(hermes.sendMessage(2, "0.7;0.6"), True)
		#self.assertEqual(hermes.sendMessage(3, "0.8;0.1"), True)
		#self.assertEqual(hermes.sendMessage(4, "0.4, 0.2"), True)
		#self.assertEqual(hermes.sendMessage(7, "0.4, 0.2"), False)
	
	#multicast
	'''
	def test_sendMessages(self):
		self.assertEqual(hermes.sendMessages(1, "INF@R1@0.7;0.3"), True)
		self.assertEqual(hermes.sendMessages(2, "INF@R2@0.7;0.3"), True)
		self.assertEqual(hermes.sendMessages(3, "INF@R3@0.7;0.3"), True)
		self.assertEqual(hermes.sendMessages(4, "INF@R4@0.7;0.3"), False)
	'''

	def testSendMessage(self):
		self.assertEqual(SerialCommunication.sendMessage(1, "0.1;0.3"), True)
		#self.assertEqual(SerialCommunication.sendMessage(2, "0.3;0.2"), True)
		#self.assertEqual(SerialCommunication.sendMessage(3, "0.6;0.1"), True)
		#self.assertEqual(SerialCommunication.sendMessage(4, "0.4, 0.2"), True)
		#self.assertEqual(SerialCommunication.sendMessage(9, "0.3, 0.9"), False)

	def testNewRobot(self):
		self.assertEqual(SerialCommunication.newRobot('A', 0x88a0), True)
		#self.assertEqual(SerialCommunication.newRobot('A', 0xb14c), False)
		#self.assertEqual(SerialCommunication.newRobot('B', 0xb24a), True)
		#self.assertEqual(SerialCommunication.newRobot('C', 0x215c), True)
		#self.assertEqual(SerialCommunication.newRobot('D', 0x35f6), True)
		#self.assertEqual(SerialCommunication.newRobot('E', 0x97e7), True)
		#self.assertEqual(SerialCommunication.newRobot('F', 0x6b0d), True)
		#self.assertEqual(SerialCommunication.newRobot('G', 0x56bc), True)
		#self.assertEqual(SerialCommunication.newRobot('H', 0x13da), False)

			
'''
	def test_pow(self):
		result = basic_operations.pow(2, 3)
		self.assertEqual(result, 8)
'''
if __name__ == '__main__':
	unittest.main()
