import sys
from PyQt5.QtWidgets import QApplication
import unittest

'''
voltei só mais um tiquinho xD
'''
sys.path.append("../..")
import afrodite

app = QApplication(sys.argv)

class TestAfrodite(unittest.TestCase):
    def setUp(self):
        '''Create the GUI'''
        self.af = afrodite.Afrodite()


if __name__ == "__main__":
    unittest.main()
