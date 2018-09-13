import unittest
from control.actions import Actions
from control.robot import Robot
import math


class TestActions(unittest.TestCase):

    actions = Actions()
    robot = Robot()

    def testRun(self):
        self.robot.action.append("stop")
        robot = self.actions.run(self.robot)
        del self.robot.action[0]

        self.assertIsNotNone(robot)

    def testStop(self):
        self.robot.action.append("stop")
        robot = self.actions.run(self.robot)
        del self.robot.action[0]

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vMax, 0)
        self.assertEqual(robot.vLeft, 0)
        self.assertEqual(robot.vRight, 0)
        self.assertEqual(robot.target, [-1, -1])

    def testlookAt(self):
        # Case 1: when the robot needs to turn in some given orientation
        self.robot.action.append("lookAt")
        self.robot.action.append("orientation")
        self.robot.orientation = 0
        self.robot.targetOrientation = math.pi
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, "ORIENTATION")

        # Other cases: when the robot needs to look at some given target(a point)
        # If the target is in front of him, the function is equal to PI
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.action[1] = "target"
        self.robot.position = (100, 200)
        self.robot.target = (300, 200)
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi)

        # If the target is in front of him, the function is equal to 0
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.action[1] = "target"
        self.robot.position = (300, 200)
        self.robot.target = (100, 200)
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, 0)

        # If the target is up, the function is equal to PI/2
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.action[1] = "target"
        self.robot.position = (100, 100)
        self.robot.target = (100, 300)
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi/2)

        # And if the target is down, the function is equal to -Pi/2
        self.robot.targetOrientation = None
        self.robot.cmdType = None
        self.robot.action[1] = "target"
        self.robot.position = (100, 300)
        self.robot.target = (100, 100)
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, -(math.pi/2))

        del self.robot.action[1]
        del self.robot.action[0]

    def testSpin(self):
        self.robot.action.append("spin")
        self.robot.action.append("clockwise")
        self.robot.vMax = 0.8
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, 0.8)
        self.assertEqual(robot.vRight, -0.8)

        self.robot.action[1] = "counter"
        robot = self.actions.run(self.robot)

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, -0.8)
        self.assertEqual(robot.vRight, 0.8)

        del self.robot.action[1]
        del self.robot.action[0]

    def testGoTo(self):
        pass


if __name__ == '__main__':
    unittest.main()
