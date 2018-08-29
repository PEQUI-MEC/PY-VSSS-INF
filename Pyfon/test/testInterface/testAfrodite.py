import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget,QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import serial, glob
import unittest

sys.path.append("../../")
from interface import icons_rc
from interface import afrodite

app = QApplication(sys.argv)

class TestAfrodite(unittest.TestCase):
    def setUp(self):
        '''Create the GUI'''
        self.af = afrodite.Afrodite()

    def testClear(self):
        self.assertTrue(True)
        print("\n")

    #VideoView
    ##Positions
    def testUpdateLabelVideoViewPositionsRobot1(self):
        self.af.updateLabelVideoViewPositionsRobot1(1,2,3)
        self.string = self.af.labelVideoViewPositionsRobot1.text()
        self.assertEqual("(1,2,3)", self.string)

    def testUpdateLabelVideoViewPositionsRobot2(self):
        self.af.updateLabelVideoViewPositionsRobot2(1,2,3)
        self.string = self.af.labelVideoViewPositionsRobot2.text()
        self.assertEqual("(1,2,3)", self.string)

    def testUpdateLabelVideoViewPositionsRobot3(self):
        self.af.updateLabelVideoViewPositionsRobot3(1,2,3)
        self.string = self.af.labelVideoViewPositionsRobot3.text()
        self.assertEqual("(1,2,3)", self.string)

    ##CheckBoxVideoViewDisableDrawing
    def testGetStateCheckBoxVideoViewDisableDrawingTrue(self):
        self.af.checkBoxVideoViewDisableDrawing.setTristate(True)
        self.assertTrue(self.af.getStateCheckBoxVideoViewDisableDrawing())

    def testGetStateCheckBoxVideoViewDisableDrawingFalse(self):
        self.af.checkBoxVideoViewDisableDrawing.setTristate(False)
        self.assertFalse(self.af.getStateCheckBoxVideoViewDisableDrawing())

    #FPS
    def testUptadeLabelVideoViewFPS(self):
        self.af.uptadeLabelVideoViewFPS(13)
        self.string = self.af.labelVideoViewFPS.text()
        self.assertEqual("FPS: 13", self.string)


if __name__ == "__main__":
    unittest.main()
