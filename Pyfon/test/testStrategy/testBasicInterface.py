import unittest
from strategy import Athena

class TestBasicInterface(unittest.TestCase):

    def testSetup(self):
        athena = Athena()

        def callback():
            pass

        self.assertTrue(athena.setup(640, 480, callback))

    def testGetTargets(self):
        athena = Athena()

        positions = [
            [100, 200, 1.3],  # allie 1
            [10, 240, 0.4],  # allie 2
            [400, 100, 0.4],  # allie 3
            [100, 300],  # adv 1
            [40, 100],  # adv 2
            [550, 220],  # adv 3
            [10, 200]  # ball
        ]

        athena.getTargets(positions)

    def testInterpretJSON(self):
        athena = Athena()

        positions = [
            [100, 200, 1.3],  # allie 1
            [10, 240, 0.4],  # allie 2
            [400, 100, 0.4],  # allie 3
            [100, 300],  # adv 1
            [40, 100],  # adv 2
            [550, 220],  # adv 3
            [10, 200]  # ball
        ]

        athena.interpretJSON(positions)

    def testGenerateResponse(self):
        athena = Athena()
        athena.generateResponse()

    def testAnalyzeState(self):
        athena = Athena()
        athena.analyzeState()

    def testSetRoles(self):
        athena = Athena()
        athena.setRoles()

    def testSelectTactics(self):
        athena = Athena()
        athena.selectTactics()

    def testSelectActions(self):
        athena = Athena()
        athena.selectActions()


if __name__ == '__main__':
    unittest.main()