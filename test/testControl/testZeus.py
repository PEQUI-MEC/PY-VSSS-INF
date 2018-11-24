from control.zeus import Zeus
from helpers.endless import Endless

from math import pi
import unittest


class TestZeus(unittest.TestCase):
    zeus = Zeus()
    zeus = zeus.setup(3)
    Endless.setup(640, 480)

    info = [
        {
            "robotLetter": "A",
            "command": "goTo",
            "data": {
                "pose": {
                    "position": (644, 1199), "orientation": 0.5
                },
                "target": {
                    "position": (300, 300), "orientation": (282, 150.0)
                },
                "velocity": 1.0,
                "obstacles": [
                    (644, 1199), (611, 1243), (602, 1121), (644, 1199), (611, 1243), (602, 1121)
                ]
            }
        },

        {
            "robotLetter": "B",
            "command": "stop",
            "data": {"before": 0}
         },

        {
            "robotLetter": "C",
            "command": "goTo",
            "data": {
                "pose": {
                    "position": (602, 1121), "orientation": 0.5
                },
                "target": {
                    "position": (300, 300), "orientation": (32, 0)
                },
                "velocity": 1.0
            }
        }
    ]

    info2 = [
        {
            "robotLetter": "A",
            "command": "lookAt",
            "data": {
                "pose": {
                    "orientation": 0
                },
                "target": pi
            }
        },
        {
            "robotLetter": "B",
            "command": "spin",
            "data": {"velocity": 1.0, "direction": "clockwise"}

        },
        {
            "robotLetter": "C",
            "command": "goTo",
            "data": {
                "obstacles": [(0, 200), (10, 100)],
                "pose": {
                    "position": (100, 100),
                    "orientation": 0
                },
                "target": {
                    "orientation": pi,
                    "position": (200, 100)
                },
                "velocity": 1.0,
                "before": 5
            }
        }
    ]

    def testGetVelocities(self):
        velocities = self.zeus.getVelocities(self.info)
        print(velocities)

    def testGetWarriors(self):
        warriors = self.zeus.getWarriors(self.info)

        self.assertEqual(len(warriors), 3)
        self.assertEqual(warriors[0].action, ["goTo"])
        self.assertEqual(warriors[1].action, ["stop"])
        self.assertEqual(warriors[2].action, ["goTo"])

        warriors = self.zeus.getWarriors(self.info2)

        self.assertEqual(len(warriors), 3)
        self.assertEqual(warriors[0].action, ["lookAt", "orientation"])
        self.assertEqual(warriors[1].action, ["spin", "clockwise"])
        self.assertEqual(warriors[2].action, ["goTo"])

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        pass


if __name__ == "__main__":
    unittest.main()
