from control.dice import Dice
from control.warrior import Warrior

from math import pi
import unittest


class TestTranslate(unittest.TestCase):
    warrior = Warrior()
    translate = Dice()

    def testRun(self):
        self.warrior.cmdType = "SPEED"
        self.warrior.vLeft = 0.8
        self.warrior.vRight = 0.8

        warrior = self.translate.run(self.warrior)
        self.assertIsNotNone(warrior)

    def testUvfControl(self):
        pass

    def testVectorControl(self):
        pass

    def testPositionControl(self):
        '''
        translate = Translate()
        warrior = warrior([100, 200], [100, 200], 0, math.pi, 0, "POSITION", 0.8, 1, 1, None)
        warrior = translate.setup(warrior)
        self.assertEqual([warrior[0], warrior[1]], [0, 0])
        '''
        pass

    def testOrientationControl(self):
        self.warrior.cmdType = "ORIENTATION"
        self.warrior.orientation = 0
        self.warrior.targetOrientation = pi
        self.warrior.vMax=0.8
        warrior = self.translate.run(self.warrior)

        self.assertEqual([warrior[0], warrior[1]], [0, 0])

        self.warrior.cmdType = "ORIENTATION"
        self.warrior.orientation = pi
        self.warrior.targetOrientation = pi
        warrior = self.translate.run(self.warrior)

        self.assertEqual([warrior[0], warrior[1]], [0, 0])


if __name__ == '__main__':
    unittest.main()
