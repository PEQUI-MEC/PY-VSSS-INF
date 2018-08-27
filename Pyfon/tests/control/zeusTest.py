import unittest
from control import Zeus

class ZeusTest(unittest.TestCase):
    def testRobotRiseUp(self):
        zeus = Zeus()
        self.assertTrue(zeus.robotRiseUp(None))

    def testControllAll(self):
        zeus = Zeus()
        self.assertTrue(zeus.controlAll(None))

if __name__ == '__main__':
    unittest.main()

