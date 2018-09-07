from control import Zeus
from control.robot import Robot
import unittest
import math

class TestZeus(unittest.TestCase):
    info = [
        {
            "action": "lookAt",
            "orientation": 0,
            "targetOrientation": math.pi
        },
        {
            "action": "lookAt",
            "orientation": 1.0,
            "position": [300, 200],
            "target": [100, 200]
        },
        {
            "action": "stop",
        }
    ]

    def testSetup(self):
        Zeus().setup(self.info)

    def testGetRobots(self):
        robots = Zeus().getRobots(self.info)

        self.assertEqual(len(robots), 3)
        self.assertEqual(type(robots[0]), type(Robot()))
        self.assertEqual(type(robots[1]), type(Robot()))
        self.assertEqual(type(robots[2]), type(Robot()))
        self.assertEqual(robots[0].action, "lookAt")
        self.assertEqual(robots[1].action, "lookAt")
        self.assertEqual(robots[2].action, "stop")

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        robots = Zeus().getRobots(self.info)
        velocitys = Zeus().controlRoutine(robots)

        self.assertEqual(len(velocitys), 3)
        self.assertEqual(type(velocitys[0]), list)
        self.assertEqual(type(velocitys[1]), list)
        self.assertEqual(type(velocitys[2]), list)


if __name__ == '__main__':
    unittest.main()
