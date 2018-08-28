import sys
import unittest

sys.path.append("../../../")
from Pyfon.hades import Hades


class HadesTest(unittest.TestCase):


    def setUp(self):
        self.hades = Hades(0, "bbb")

    '''
    Tests image provider
    '''
    def testCapture(self):
        self.assertIsNotNone(self.hades.summonCapture())
        self.assertIsNone(self.hades.killCapture())
        self.assertIsNone(self.hades.refreshCapture())

    '''
    Tests communication provider
    '''
    def testCommunication(self):
        self.assertTrue(self.hades.summonCommunication())

    '''
    Tests idle loop
    '''
    def testPuppetLoop(self):
        self.assertTrue(self.hades.puppetLoop())

    def testUpdatePositions(self):
        self.assertTrue(self.hades.updateFormation())

    def testUpdateFormation(self):
        self.assertTrue(self.hades.updateFormation())

    def testCreateFormatio(self):
        self.assertTrue(self.hades.createFormation())

    def testRecordGame(self):
        self.assertTrue(self.hades.recordGame())


if __name__ == '__main__':
    unittest.main()
