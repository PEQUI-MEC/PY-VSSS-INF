from control.eunomia import Eunomia
from control.warrior import Warrior

from math import pi
import unittest


class TestActions(unittest.TestCase):

    actions = Eunomia()
    actions.setup()
    warrior = None

    def testRun(self):
        pass

    def testStop(self):
        self.warrior = Warrior()

        self.warrior.action.append("stop")
        self.warrior.before = 0
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, "SPEED")
        self.assertEqual(warrior.vLeft, 0)
        self.assertEqual(warrior.vRight, 0)

        del self.warrior

    def testlookAt(self):
        self.warrior = Warrior()

        # Case 1: when the warrior needs to turn in some given orientation
        self.warrior.action.append("lookAt")
        self.warrior.action.append("orientation")
        self.warrior.orientation = 0
        self.warrior.targetOrientation = pi
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, "ORIENTATION")

        # Other cases: when the warrior needs to look at some given target(a point)
        # If the target is in front of him, the function is equal to PI
        self.warrior.targetOrientation = None
        self.warrior.cmdType = None
        self.warrior.action[1] = "target"
        self.warrior.position = (100, 200)
        self.warrior.target = (300, 200)
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, 'ORIENTATION')
        self.assertEqual(warrior.targetOrientation, pi)

        # If the target is in front of him, the function is equal to 0
        self.warrior.targetOrientation = None
        self.warrior.cmdType = None
        self.warrior.action[1] = "target"
        self.warrior.position = (300, 200)
        self.warrior.target = (100, 200)
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, 'ORIENTATION')
        self.assertEqual(warrior.targetOrientation, 0)

        # If the target is up, the function is equal to PI/2
        self.warrior.targetOrientation = None
        self.warrior.cmdType = None
        self.warrior.action[1] = "target"
        self.warrior.position = (100, 100)
        self.warrior.target = (100, 300)
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, 'ORIENTATION')
        self.assertEqual(warrior.targetOrientation, pi/2)

        # And if the target is down, the function is equal to -Pi/2
        self.warrior.targetOrientation = None
        self.warrior.cmdType = None
        self.warrior.action[1] = "target"
        self.warrior.position = (100, 300)
        self.warrior.target = (100, 100)
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, 'ORIENTATION')
        self.assertEqual(warrior.targetOrientation, -(pi/2))
        del self.warrior

    def testSpin(self):
        self.warrior = Warrior()

        self.warrior.action.append("spin")
        self.warrior.action.append("clockwise")
        self.warrior.vMax = 0.8
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, "SPEED")
        self.assertEqual(warrior.vLeft, 0.8)
        self.assertEqual(warrior.vRight, -0.8)

        self.warrior.action[1] = "counter"
        warrior = self.actions.run(self.warrior)

        self.assertEqual(warrior.cmdType, "SPEED")
        self.assertEqual(warrior.vLeft, -0.8)
        self.assertEqual(warrior.vRight, 0.8)

        del self.warrior

    def testGoTo(self):
        self.warrior = Warrior()

        self.warrior.action.append("goTo")
        self.warrior.position = (200, 200)
        self.warrior.orientation = 0
        # self.warrior.targetOrientation = -((pi/2.0) + ((pi/2.0)/2.0))
        self.warrior.targetOrientation = (500, 500)
        self.warrior.target = (400, 400)
        self.warrior.vMax = 1.0

        warrior = self.actions.run(self.warrior)
        self.assertEqual(warrior.cmdType, "VECTOR")

        del self.warrior


if __name__ == '__main__':
    unittest.main()
