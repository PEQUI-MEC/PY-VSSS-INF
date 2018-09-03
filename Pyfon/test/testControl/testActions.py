import unittest
from control.actions import Actions
from control.robot import Robot
import math


class TestActions(unittest.TestCase):

    def testSetup(self):
        actions = Actions()
        robot = Robot([100, 200], [100, 300], 1.3, None, 0, None, 0.8, 0, 0, "stop")
        robot = actions.setup(robot)
        self.assertIsNotNone(robot)

    def testStop(self):
        actions = Actions()
        robot = Robot([100, 200], [100, 300], 1.3, None, 0, None, 0.8, 0, 0, "stop")

        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vMax, 0)
        self.assertEqual(robot.vLeft, 0)
        self.assertEqual(robot.vRight, 0)
        self.assertEqual(robot.target, [-1, -1])

    def testKick(self):
        actions = Actions()
        robot = Robot([100, 200], [100, 200], 1.3, None, 0, None, 0.8, 0, 0, "kick")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, "VECTOR")
        self.assertEqual(robot.transAngle, 0)

    def testlookAt(self):
        actions = Actions()

        ''' Case 1: when the robot needs to turn in some given orientation '''
        robot = Robot([100, 200], [100, 200], 1.3, None, 0, None, 0.8, 0, 0, "lookAt")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, "ORIENTATION")
        self.assertEqual(robot.targetOrientation, 1.3)

        '''
        Other cases: when the robot needs to look at some given target(a point) 
        If the target is in front of him, the function is equal to PI
        If the target is behind, the function is equal to zero
        If the target is up, the function is equal to PI/2
        And if the target is down, the function is equal to -Pi/2
        
        '''
        robot = Robot([100, 200], [300, 200], None, 0, 0, None, 0.8, 0, 0, "lookAt")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi)

        robot = Robot([300, 200], [100, 200], None, 0, 0, None, 0.8, 0, 0, "lookAt")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, 0)

        robot = Robot([100, 100], [100, 300], None, 0, 0, None, 0.8, 0, 0, "lookAt")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, math.pi/2)

        robot = Robot([100, 300], [100, 100], None, 0, 0, None, 0.8, 0, 0, "lookAt")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, 'ORIENTATION')
        self.assertEqual(robot.targetOrientation, -(math.pi/2))

    def testSpinClockwise(self):
        actions = Actions()
        robot = Robot([100, 200], [100, 300], 1.3, None, 0, None, 0.8, 0, 0, "spinClockwise")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, 0.8)
        self.assertEqual(robot.vRight, -0.8)

    def testSpinCounterClockwise(self):
        actions = Actions()
        robot = Robot([100, 200], [100, 300], 1.3, None, 0, None, 0.8, 0, 0, "spinCounterClockWise")
        robot = actions.setup(robot)
        self.assertEqual(robot.cmdType, "SPEED")
        self.assertEqual(robot.vLeft, -0.8)
        self.assertEqual(robot.vRight, 0.8)


if __name__ == '__main__':
    unittest.main()
