import unittest
from control import Zeus

class TestZeus(unittest.TestCase):
    zeus = Zeus()

    def testSetup(self):
        self.assertTrue(__class__.zeus.setup())

    def testGetRobots(self):
        __class__.zeus.getRobots()

    def testGenerateJson(self):
        __class__.zeus.generateJson()

    def testControlRoutine(self):
        __class__.zeus.controlRoutine()


if __name__ == '__main__':
    unittest.main()