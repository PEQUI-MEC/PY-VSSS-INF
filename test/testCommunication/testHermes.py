import unittest
# import sys
# sys.path.append("../")
from communication.hermes import Hermes

class HermesTest(unittest.TestCase):

    def testCreateMessage(self):
        self.assertEqual(Hermes.createMessage(1, 0.3, 0.8), "0.3;0.8")
        #self.assertEqual(hermes.createMessage(2, 0.1, 0.3), "0.1;0.3")
        #self.assertEqual(hermes.createMessage(3, 0.5, 0.7), "0.5;0.7")
        #self.assertEqual(hermes.createMessage(13, 0.3, 0.1), "invalid")


    #unicast
    def testSendMessage(self):
        self.assertEqual(Hermes.sendMessage("HERCULES", "0.7;0.6"), True)
        #self.assertEqual(hermes.sendMessage(2, "0.7;0.6"), True)
        #self.assertEqual(hermes.sendMessage(3, "0.8;0.1"), True)
        #self.assertEqual(hermes.sendMessage(4, "0.4, 0.2"), True)
        #self.assertEqual(hermes.sendMessage(7, "0.4, 0.2"), False)

    def testInit(self):
        self.assertTrue("/dev/ttyUSB0", 115200)

    #multicast
    '''
    def test_sendMessages(self):
        self.assertEqual(hermes.sendMessages(1, "INF@R1@0.7;0.3"), True)
        self.assertEqual(hermes.sendMessages(2, "INF@R2@0.7;0.3"), True)
        self.assertEqual(hermes.sendMessages(3, "INF@R3@0.7;0.3"), True)
        self.assertEqual(hermes.sendMessages(4, "INF@R4@0.7;0.3"), False)
    '''