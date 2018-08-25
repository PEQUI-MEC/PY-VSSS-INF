import unittest
import sys
sys.path.append("../")
import communication.hermes

class CommunicationTest(unittest.TestCase):
	#unicast
	def test_sendMessages(self):
		self.assertEqual(hermes.sendMessages(1, "0.7;0.6"), true)
		self.assertEqual(hermes.sendMessages(2, "0.7;0.6"), true)
		self.assertEqual(hermes.sendMessages(3, "0.8;0.1"), true)
		self.assertEqual(hermes.sendMessages(4, "0.4, 0.2"), false)
	#multicast
	def test_sendMessages(self):
		self.assertEqual(hermes.sendMessages(1, "INF@R1@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(2, "INF@R2@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(3, "INF@R3@0.7;0.3"), true)
		self.assertEqual(hermes.sendMessages(4, "INF@R4@0.7;0.3"), false)

	def test_subtract(self):
		self.assertEqual(hermes.subtract(-1, 1), -2)
		self.assertEqual(hermes.subtract(4, 4), 0)
		self.assertEqual(hermes.subtract(-3, 2), -5)
		self.assertEqual(hermes.subtract(1, 7), -6)
		self.assertEqual(hermes.subtract(6, 3), 3)

	def test_multiply(self):
		self.assertEqual(hermes.multiply(-1, 1), -1)
		self.assertEqual(hermes.multiply(4, 4), 16)
		self.assertEqual(hermes.multiply(-3, 2), -6)
		self.assertEqual(hermes.multiply(1, 7), 7)
		self.assertEqual(hermes.multiply(6, 3), 18)

	def test_divide(self):
		self.assertEqual(hermes.divide(-1, 1), -1)
		self.assertEqual(hermes.divide(4, 4), 1)
		self.assertEqual(hermes.divide(-3, 2), -1.5)
		self.assertEqual(hermes.divide(6, 2), 3)
		self.assertEqual(hermes.divide(6, 3), 2)
'''
	def test_pow(self):
		result = basic_operations.pow(2, 3)
		self.assertEqual(result, 8)
'''
if __name__ == '__main__':
	unittest.main()
