import unittest
from control.translate import Translate
from control import constants


class TestTranslate(unittest.TestCase):

    def testSetup(self):
        translate = Translate()
        robot = [[100, 200], [100, 300], 1.3, None, 0, "SPEED", 0.8, 0, 0, "stop"]
        robot = translate.setup(robot)
        self.assertIsNotNone(robot)

    def testUvfControl(self):
        pass

    def testVectorControl(self):
        pass

    def testPositionControl(self):
        pass

    def testOrientationControl(self):
        pass

    def testSpeedControl(self):
        pass


if __name__ == '__main__':
    unittest.main()
