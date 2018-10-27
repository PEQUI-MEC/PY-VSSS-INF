from helpers.plutus import Plutus
import unittest
import os


class TestPlutus(unittest.TestCase):
    saveLocation = "helpers/test.json"

    def testInit(self):
        plutus = Plutus(self.saveLocation)

    def testSet(self):
        plutus = Plutus(self.saveLocation)
        plutus.set("test", "tested")
        os.unlink(self.saveLocation)

    def testGet(self):
        plutus = Plutus(self.saveLocation)
        plutus.set("test", "tested")
        self.assertEqual(plutus.get("test"), "tested")
        os.unlink(self.saveLocation)

    def testNonExistant(self):
        plutus = Plutus(self.saveLocation)
        self.assertEqual(plutus.get("notTest"), None)


if __name__ == '__main__':
    unittest.main()
