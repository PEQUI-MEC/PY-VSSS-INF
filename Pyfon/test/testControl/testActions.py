import unittest
from control.actions import Actions
from control.robot import Robot
import math


class TestActions(unittest.TestCase):

    actions = Actions()
    robot = None

    def testRun(self):
        self.robot = Robot()
        self.robot.action.append("stop")
        robot = self.actions.run(self.robot)

        self.assertIsNotNone(robot)

    def testStop(self):
        self.robot = Robot()

        self.robot.action.append("stop")
        robot = self.actions.run(self.robot)
        # del self.robot.action[0]

        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vMax, 0)
        self.assertEqual(robot.vLeft, 0)
        self.assertEqual(robot.vRight, 0)

    def testlookAt(self):
        self.robot = Robot()

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


    def testSpin(self):
        self.robot = Robot()

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

    def testGoTo(self):
        '''
        self.robot = Robot()

        self.robot.action.append("goTo")
        self.robot.obstacles = [(0, 200), (10, 100)]
        self.robot.position = (100, 100)
        self.robot.orientation = 0
        self.robot.targetOrientation = (100, 300)
        self.robot.target = (0, 0)
        self.robot.vMax = 1.0

        robot = self.actions.run(self.robot)
        self.assertEqual(robot.cmdType, "VECTOR")
        '''


if __name__ == '__main__':
    unittest.main()
