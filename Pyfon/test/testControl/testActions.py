import unittest
from control.actions import Actions
from control.robot import Robot
import math


class TestActions(unittest.TestCase):

    robot = Robot()
    actions = Actions()

    def testSetup(self):
        self.robot.action = "stop"
        robot = self.actions.setup(self.robot)

        self.assertIsNotNone(robot)

    def testStop(self):
        self.robot.action = "stop"
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vMax, 0)
        self.assertEqual(robot.vLeft, 0)
        self.assertEqual(robot.vRight, 0)
        self.assertEqual(robot.target, [-1, -1])

    def testKick(self):
        self.robot.action = "kick"
        self.robot.position = [100, 200]
        self.robot.target = [100, 200]
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, "VECTOR")
        self.assertEqual(robot.transAngle, 0)

    def testlookAt(self):
        # Case 1: when the robot needs to turn in some given orientation
        self.robot.action = "lookAt"
        self.robot.orientation = 0
        self.robot.targetOrientation = math.pi
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, "ORIENTATION")

        # Other cases: when the robot needs to look at some given target(a point)
        # If the target is in front of him, the function is equal to PI
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.position = [100, 200]
        self.robot.target = [300, 200]
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi)

        # If the target is in front of him, the function is equal to 0
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.position = [300, 200]
        self.robot.target = [100, 200]
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, 0)

        # If the target is up, the function is equal to PI/2
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.position = [100, 100]
        self.robot.target = [100, 300]
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi/2)

        # And if the target is down, the function is equal to -Pi/2
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.position = [100, 300]
        self.robot.target = [100, 100]
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, -(math.pi/2))

    def testSpinClockwise(self):
        self.robot.action = "spinClockwise"
        self.robot.vMax = 0.8
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, 0.8)
        self.assertEqual(robot.vRight, -0.8)

    def testSpinCounterClockwise(self):
        self.robot.action = "spinCounterClockwise"
        self.robot.vMax = 0.8
        robot = self.actions.setup(self.robot)

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, -0.8)
        self.assertEqual(robot.vRight, 0.8)


if __name__ == '__main__':
    unittest.main()
