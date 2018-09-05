from control import Zeus
from control.robot import Robot
import unittest


class TestZeus(unittest.TestCase):
    info = [
        {
            "action": "lookAt",
            "orientation": 1.0
        },
        {
            "action": "lookAt",
            "position": [300, 200],
            "target": [100, 200]
        },
        {
            "action": "stop",
        }
    ]

    def testSetup(self):
        pass

    def testGetRobots(self):
        robots = Zeus().getRobots(self.info)
        self.assertEqual(len(robots), 3)
        self.assertEqual(str(type(robots[0])), "<class 'control.robot.Robot'>")
        self.assertEqual(str(type(robots[1])), "<class 'control.robot.Robot'>")
        self.assertEqual(str(type(robots[2])), "<class 'control.robot.Robot'>")

    def testGenerateOutput(self):
        pass

    def testControlRoutine(self):
        pass

if __name__ == '__main__':
    unittest.main()
