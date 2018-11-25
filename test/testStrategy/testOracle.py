import unittest
from strategy.oracle import Oracle


class TestOracle(unittest.TestCase):

    def testPushState(self):
        oracle = Oracle(10)

        stateTime = ((10, 10), 0)
        self.assertEqual(oracle.pushState(stateTime[0], 0), stateTime)

    def testPredict(self):
        oracle = Oracle(10)

        oracle.pushState((0, 0), 0)
        oracle.pushState((0, 10), 1)
        prediction = oracle.predict(1)  # deve ser (0, 20)

        self.assertAlmostEqual(prediction[0], 0)
        self.assertAlmostEqual(prediction[1], 20)

    def testGetY(self):
        oracle = Oracle(10)

        oracle.pushState((0, 0), 0)
        oracle.pushState((10, 30), 1)
        prediction = oracle.predict(1)
        # usa a predição pois seu cálculo está supostamente correto
        self.assertAlmostEqual(oracle.getY(prediction[0]), prediction[1])


if __name__ == '__main__':
    unittest.main()
