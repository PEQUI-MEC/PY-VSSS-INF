import unittest
# import sys
# sys.path.append("../")
from communication.serialCommunication import SerialCommunication

class SerialCommunicationTest(unittest.TestCase):

    def testSendMessage(self):
        self.assertEqual(SerialCommunication.sendMessage("HERCULES", "0.1;0.3"), True)
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

