from control import Zeus
from control.robot import Robot
from collections import namedtuple

import unittest
import json

_robot_location = "database/robots.json"


class TestZeus(unittest.TestCase):
    @staticmethod
    def getRobots():
        robots = []
        robots.append(Robot([400, 100], [100, 300], None, 0.5, 0, None, 0.8, 0, 0, "lookAt"))
        robots.append(Robot([10, 24], [100, 300], None, 0.5, 0, None, 0.8, 0, 0, "lookAt"))
        robots.append(Robot([100, 200], [100, 300], 1.3, None, 0, None, 0.8, 0, 0, "lookAt"))

        if len(robots) == 0:
            return False
        else:
            return robots

    def testSetup(self):
        self.assertTrue(Zeus().setup(TestZeus().getRobots()))

    def testGenerateOutput(self):
        Zeus().generateOutput()

    def testControlRoutine(self):
        Zeus().controlRoutine(TestZeus().getRobots())


if __name__ == '__main__':
    unittest.main()
