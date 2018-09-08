from control import Zeus
from control.robot import Robot
import unittest
import math


class TestZeus(unittest.TestCase):
    zeus = Zeus()

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
        '''
        outPuts = self.zeus.run(self.info)

        self.assertEqual(outPuts[0], {'vLeft': -1.0, 'vRight': 1.0})
        self.assertEqual(outPuts[1], {'vLeft': 0.8, 'vRight': -0.8})
        self.assertEqual(outPuts[2], {'vLeft': 0.0, 'vRight': 0.0})
        '''
        pass

    def testGetRobots(self):
        robots = self.zeus.getRobots(self.info)

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
        robots = self.zeus.getRobots(self.info)
        velocities = self.zeus.controlRoutine(robots)

        self.assertEqual(len(velocities), 3)
        self.assertEqual(type(velocities[0]), list)
        self.assertEqual(type(velocities[1]), list)
        self.assertEqual(type(velocities[2]), list)


if __name__ == '__main__':
    unittest.main()
