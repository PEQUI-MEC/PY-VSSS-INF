import unittest
from control.translate import Translate
from control.robot import Robot
import math


class TestTranslate(unittest.TestCase):
    robot = Robot()
    translate = Translate()

    def testRun(self):
        self.robot.cmdType = "SPEED"
        self.robot.vMax = 0.8

        robot = self.translate.run(self.robot)
        self.assertIsNotNone(robot)

    def testUvfControl(self):
        pass

    def testVectorControl(self):
        pass

    def testPositionControl(self):
        '''
        translate = Translate()
        robot = Robot([100, 200], [100, 200], 0, math.pi, 0, "POSITION", 0.8, 1, 1, None)
        robot = translate.setup(robot)
        self.assertEqual([robot[0], robot[1]], [0, 0])
        '''
        pass

    def testOrientationControl(self):
        self.robot.cmdType = "ORIENTATION"
        self.robot.orientation = 0
        self.robot.targetOrientation = math.pi
        robot = self.translate.run(self.robot)

        self.assertEqual([robot[0], robot[1]], [0, 0])

        self.robot.cmdType = "ORIENTATION"
        self.robot.orientation = math.pi
        self.robot.targetOrientation = math.pi
        robot = self.translate.run(self.robot)

        self.assertEqual([robot[0], robot[1]], [0, 0])


if __name__ == '__main__':
    unittest.main()
