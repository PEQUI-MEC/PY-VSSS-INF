import unittest
from strategy import Athena


class TestBasicInterface(unittest.TestCase):

    def testSetup(self):
        def callback():
            pass

        athena = Athena(callback)

        self.assertTrue(athena.setup(3, 100, 100, 0.8))

    def testGetTargets(self):
        def callback():
            pass

        athena = Athena(callback)

        positions = [
            [
                {
                    "position": (0, 200),
                    "orientation": 0.5
                },
                {
                    "position": (0, 200),
                    "orientation": 0.5
                },
                {
                    "position": (0, 200),
                    "orientation": 0.5
                }
            ],
            [
                {
                    "position": (0, 200)
                },
                {
                    "position": (0, 200)
                },
                {
                    "position": (0, 200)
                }
            ],
            {
                "position": (0, 200)
            }
        ]

        athena.getTargets(positions)


if __name__ == '__main__':
    unittest.main()
