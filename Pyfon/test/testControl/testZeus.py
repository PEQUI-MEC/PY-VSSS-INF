from control import Zeus
from control.robot import Robot
import unittest
import math


class TestZeus(unittest.TestCase):
    zeus = Zeus()
    zeus.setup()

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

    def testRun(self):
        outPuts = self.zeus.run(self.info)

        self.assertEqual(outPuts[0], {'vLeft': -1.0, 'vRight': 1.0})
        self.assertEqual(outPuts[1], {'vLeft': 0.8, 'vRight': -0.8})
        self.assertEqual(outPuts[2], {'vLeft': 0.0, 'vRight': 0.0})

        pass

    def testGetRobots(self):
        robots = self.zeus.getRobots(self.info)

        self.assertEqual(len(robots), 3)

        self.assertEqual(robots[0].action, "lookAt")
        self.assertEqual(robots[1].action, "lookAt")
        self.assertEqual(robots[2].action, "stop")

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        self.zeus.getRobots(self.info)
        velocities = self.zeus.controlRoutine()

        self.assertEqual(len(velocities), 3)
        self.assertEqual(velocities[0], [-1.0, 1.0])
        self.assertEqual(velocities[1], [0.8, -0.8])
        self.assertEqual(velocities[2], [0.0, 0.0])


if __name__ == '__main__':
    unittest.main()
