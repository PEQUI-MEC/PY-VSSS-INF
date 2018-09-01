import unittest
from control.translate import Translate
from control import constants
import math


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
        translate = Translate()
        robot = [[100, 200], [100, 200], 0, math.pi, 0, "POSITION", 0.8, 1, 1, None]
        robot = translate.setup(robot)
        self.assertEqual([robot[0], robot[1]], [0, 0])

    def testOrientationControl(self):
        translate = Translate()
        robot = [[100, 200], [300, 200], 0, math.pi, 0, "ORIENTATION", 0.8, 0, 0, "lookAt"]
        robot = translate.setup(robot)
        self.assertEqual([robot[0], robot[1]], [1, -1])

        robot = [[100, 200], [300, 200], math.pi, math.pi, 0, "ORIENTATION", 0.8, 0, 0, "lookAt"]
        robot = translate.setup(robot)
        self.assertEqual([robot[0], robot[1]], [0, 0])


if __name__ == '__main__':
    unittest.main()
