import unittest
import sys
sys.path.append("../")
import communication.hermes
import communication.serial_communication

class CommunicationTest(unittest.TestCase):
	def test_createMessage(self):
		self.assertEqual(hermes.createMessage(1, 0.3, 0.8), "0.3;0.8")
		#self.assertEqual(hermes.createMessage(2, 0.1, 0.3), "0.1;0.3")
		#self.assertEqual(hermes.createMessage(3, 0.5, 0.7), "0.5;0.7")
		#self.assertEqual(hermes.createMessage(13, 0.3, 0.1), "invalid")


	#unicast
	def test_sendMessages(self):
		self.assertEqual(hermes.sendMessages(1, "0.7;0.6"), true)
		#self.assertEqual(hermes.sendMessages(2, "0.7;0.6"), true)
		#self.assertEqual(hermes.sendMessages(3, "0.8;0.1"), true)
		#self.assertEqual(hermes.sendMessages(4, "0.4, 0.2"), false)
	
	#multicast
'''
	def test_sendMessages(self):
		self.assertEqual(hermes.sendMessages(1, "INF@R1@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(2, "INF@R2@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(3, "INF@R3@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(4, "INF@R4@0.7;0.3"), false)
'''
	
	def test_startBee(self):
		self.assertEqual(hermes.startBee("endereço_porta_usb",115200), true)

	def test_sendMessage(self):
		self.assertEqual(serial_communication.sendMessage(-1, 1), -1)
		#self.assertEqual(serial_communication.sendMessage(4, 4), 1)
		#self.assertEqual(serial_communication.sendMessage(-3, 2), -1.5)
		#self.assertEqual(serial_communication.sendMessage(6, 2), 3)
		#self.assertEqual(serial_communication.sendMessage(6, 3), 2)


	def test_newRobot(self):
		self.assertEqual(serial_communication.sendMessage('A', 0x88a0), true)
		#self.assertEqual(serial_communication.sendMessage('A', 0xb14c), false)
		#self.assertEqual(serial_communication.sendMessage('B', 0xb24a), true)
		#self.assertEqual(serial_communication.sendMessage('C', 0x215c), true)
		#self.assertEqual(serial_communication.sendMessage('D', 0x35f6), true)
		#self.assertEqual(serial_communication.sendMessage('E', 0x97e7), true)
		#self.assertEqual(serial_communication.sendMessage('F', 0x6b0d), true)
		#self.assertEqual(serial_communication.sendMessage('G', 0x56bc), true)
		#self.assertEqual(serial_communication.sendMessage('H', 0x13da), false)

			
'''
	def test_pow(self):
		result = basic_operations.pow(2, 3)
		self.assertEqual(result, 8)
'''
if __name__ == '__main__':
	unittest.main()
