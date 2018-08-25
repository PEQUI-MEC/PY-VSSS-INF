import sys
import unittest
import cv2

sys.path.append("../../")
from Pyfon.hades import Hades

class HadesTest(unittest.TestCase):

    def setUp(self):
        pass

    def testRiseUpCapture(self):
        self.assertTrue(Hades.riseUpCapture())

    def testRiseUpCommunication(self):
        self.assertTrue(Hades.riseUpCommunication())

    def testPuppetLoop(self):
        self.assertTrue(Hades.puppetLoop())

    def testUpdatePositions(self):
        self.assertTrue(Hades.updateFormation())

    def testUpdateFormation(self):
        self.assertTrue(Hades.updateFormation())

    def testCreateFormatio(self):
        self.assertTrue(Hades.createFormation())


if __name__ == '__main__':
    unittest.main()