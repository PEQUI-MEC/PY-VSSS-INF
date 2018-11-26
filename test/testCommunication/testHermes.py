import unittest
from communication.hermes import Hermes

class HermesTest(unittest.TestCase):
    def testSetup(self):
        self.assertTrue("/dev/ttyUSB0", 115200)
        self.assertFalse("/dev/ttyUSB999", 115200)

    def testSendMessage(self):
        self.assertEqual(Hermes.sendMessage(1, "0.7;0.6"), "0.7;0.6")
        self.assertEqual(Hermes.sendMessage(2, "0.7;0.6"), "0.7;0.6")
        self.assertEqual(Hermes.sendMessage(3, "0.8;0.1"), "0.8;0.1")
        self.assertEqual(Hermes.sendMessage(7, "0.8;0.1"), None)
        self.assertRaises(KeyError, Hermes.sendMessage(4, "0.2;0.3"))
        self.assertRaises(KeyError, Hermes.sendMessage(5, "0.7;-0.6"))
        #self.assertEqual(hermes.sendMessage(4, "0.4, 0.2"), True)
        #self.assertEqual(hermes.sendMessage(7, "0.4, 0.2"), False)

    def testFly(self):
        self.assertEqual(Hermes.fly([[1,"0.7","0.7"],[2,"0.4","0.4"],[3,"0.4","0.4"]]),
                         [[1, "0.7;0.7"],[2, "0.7;0.7"],[3, "0.3;0.3"]])
        self.assertEqual(Hermes.fly([[1,"0.7","0.7"]]),
                         [[1, "0.7;0.7"]])
        self.assertEqual(Hermes.fly([[2,"0.4","0.4"],[3,"0.4","0.4"]]),
                         [[2, "0.7;0.7"],[3, "0.3;0.3"]])
        
