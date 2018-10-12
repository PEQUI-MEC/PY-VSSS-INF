import unittest
import numpy as np
import sys
from vision import apolo as Vision

apolo = Vision.Apolo()

WIDTH = 640 #X-axys
HEIGHT = 480 #Y-axys

class TestOrientationMethods(unittest.TestCase):
    def testFindRobotOrientation(self):
        self.assertEqual(np.arctan2(3,4) * 180 / np.pi ,apolo.findRobotOrientation((10, 10), (13, 6)))

    def testFindAdvOrientation(self):
        pass

    def testFindBallOrientation(self):
        pass


if __name__ == '__main__':
    unittest.main()