import unittest
from hades import Hades
from communication.hermes import Hermes
from control import Zeus
from afrodite import Afrodite
from vision import apolo


class HadesTest(unittest.TestCase):


    def setUp(self):
        self.hades = Hades(0, "bbb")
        # self.hermes = Hermes("/dev/ttyUSB0", 115200)
        self.hermes = None
        self.zeus = None

    '''
    Tests image provider
    '''
    def testCapture(self):
        self.assertIsNotNone(self.hades.summonCapture())
        self.assertIsNone(self.hades.killCapture())
        self.assertIsNotNone(self.hades.refreshCapture())

    '''
    Tests object creation of all modules
    '''
    def testModuleInstances(self):
        #hades instance
        self.assertIsNotNone(self.hades)

        #hermes instance
        self.hermes = Hermes("/dev/ttyUSB0", 115200)
        self.assertIsNotNone(self.hermes)
        del self.hermes

        #zeus instance
        self.zeus = Zeus()
        self.assertIsNotNone(self.zeus)
        del self.zeus

        #afrodite instance
        self.afrodite = Afrodite()
        self.assertIsNotNone(self.afrodite)
        del self.afrodite

        #apolo instance
        self.apolo = apolo()
        self.assertIsNotNone(self.apolo)
        del self.apolo

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

    def testCreateFormation(self):
        self.assertTrue(self.hades.createFormation())

    def testRecordGame(self):
        self.assertTrue(self.hades.recordGame())


if __name__ == '__main__':
    unittest.main()
