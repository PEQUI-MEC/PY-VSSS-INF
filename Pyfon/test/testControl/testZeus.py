import unittest
from control import Zeus


class TestZeus(unittest.TestCase):

    def testSetup(self):
        self.assertTrue(Zeus().setup())

    def testGetRobots(self):
        self.assertEqual(len(Zeus().getRobots()), 3)

    def testGenerateJson(self):
        Zeus().generateJson()

    def testControlRoutine(self):
        Zeus().controlRoutine()


if __name__ == '__main__':
    unittest.main()
