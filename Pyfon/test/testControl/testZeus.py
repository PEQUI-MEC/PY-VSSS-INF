from control import Zeus
from control.robot import Robot
import unittest
import math


class TestZeus(unittest.TestCase):
    zeus = Zeus()
    zeus = zeus.setup(3)

    info = [
        {
            "command": "lookAt",
            "data": {
                "pose": {
                    "orientation": 0
                },
                "target": math.pi
            }
        },
        {
            "command": "lookAt",
            "data": {
                "pose": {
                    "position": [300, 200],
                    "orientation": 1.0
                },
                "target": [100, 200]
            }
        },
        {
            "command": "lookAt",
            "data": {
                "pose": {
                    "orientation": 0
                },
                "target": math.pi
            }
        }
    ]

    def testGetVelocities(self):
        pass

    def testGetRobots(self):
        robots = self.zeus.getRobots(self.info)

        self.assertEqual(len(robots), 3)
        self.assertEqual(robots[0].action, ['lookAt', 'orientation'])
        self.assertEqual(robots[1].action, ['lookAt', 'target'])
        self.assertEqual(robots[2].action, ['lookAt', 'orientation'])

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        pass


if __name__ == '__main__':
    unittest.main()
