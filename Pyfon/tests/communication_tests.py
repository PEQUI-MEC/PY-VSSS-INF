import unittest
import basic_operations

class CommunicationTest(unittest.TestCase):

	def test_add(self):
		self.assertEqual(basic_operations.add(-1, 1), 0)
		self.assertEqual(basic_operations.add(4, 4), 8)
		self.assertEqual(basic_operations.add(-3, 2), -1)
		self.assertEqual(basic_operations.add(1, 7), 8)
		self.assertEqual(basic_operations.add(6, 3), 9)


	def test_subtract(self):
		self.assertEqual(basic_operations.subtract(-1, 1), -2)
		self.assertEqual(basic_operations.subtract(4, 4), 0)
		self.assertEqual(basic_operations.subtract(-3, 2), -5)
		self.assertEqual(basic_operations.subtract(1, 7), -6)
		self.assertEqual(basic_operations.subtract(6, 3), 3)

	def test_multiply(self):
		self.assertEqual(basic_operations.multiply(-1, 1), -1)
		self.assertEqual(basic_operations.multiply(4, 4), 16)
		self.assertEqual(basic_operations.multiply(-3, 2), -6)
		self.assertEqual(basic_operations.multiply(1, 7), 7)
		self.assertEqual(basic_operations.multiply(6, 3), 18)

	def test_divide(self):
		self.assertEqual(basic_operations.divide(-1, 1), -1)
		self.assertEqual(basic_operations.divide(4, 4), 1)
		self.assertEqual(basic_operations.divide(-3, 2), -1.5)
		self.assertEqual(basic_operations.divide(6, 2), 3)
		self.assertEqual(basic_operations.divide(6, 3), 2)
'''
	def test_pow(self):
		result = basic_operations.pow(2, 3)
		self.assertEqual(result, 8)
'''
if __name__ == '__main__':
	unittest.main()
