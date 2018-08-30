import unittest
from control import Zeus


class TestZeus(unittest.TestCase):

    def testSetup(self):
        self.assertTrue(Zeus().setup())

    def testGetRobots(self):
        robots = [
            [[100, 200], [100, 300], 1.3, 0.5, 0, 'orientation', 0.8, 0, 0, 'lookAt'], # robot 1
            [[10, 24], [100, 300], 0.4, 0.5, 0, 'orientation', 0.8, 0, 0, 'lookAt'], # robot 2
            [[400, 100], [100, 300], 0.7, 0.5, 0, 'orientation', 0.8, 0, 0, 'lookAt'], # robot 3
        ]
        Zeus().getRobots()

    def testGenerateJson(self):
        Zeus().generateJson()

    def testControlRoutine(self):
        Zeus().controlRoutine()


if __name__ == '__main__':
    unittest.main()
