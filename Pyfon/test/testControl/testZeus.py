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
            "command": "spin",
            "data": {
                "velocity": 0.8,
                "direction": "counter"
            }
        },
        {
            "command": "goTo",
            "data": {
                "obstacles": [(0, 200), (10, 100)],
                "pose": {
                    "position": (100, 100),
                    "orientation": 0
                },
                "target": {
                    "orientation": math.pi,
                    "position": (200, 100)
                },
                "velocity": 1.0,
                "before": 5
            }
        }
    ]

    def testGetVelocities(self):
        pass

    def testGetRobots(self):
        robots = self.zeus.getRobots(self.info)

        #for robot in robots:
            #print(vars(robot))

        self.assertEqual(len(robots), 3)
        self.assertEqual(robots[0].action, ["lookAt", "orientation"])
        self.assertEqual(robots[1].action, ["spin", "counter"])
        self.assertEqual(robots[2].action, ["goTo", 5])

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        pass


if __name__ == '__main__':
    unittest.main()
