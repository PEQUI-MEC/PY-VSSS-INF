import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
import icons_rc
import serial, glob



class mainWindow (QMainWindow):
	"""docstring for mainWindow """
	def __init__(self):
		super(mainWindow , self).__init__()
		loadUi('mainwindow.ui', self)

		#MenubarArquivo
		self.actionLoadConfigs.triggered.connect(self.actionLoadConfigsTriggered)
		self.actionSaveConfigs.triggered.connect(self.actionSaveConfigsTriggered)
		self.actionSaveasConfigs.triggered.connect(self.actionSaveasConfigTriggered)
		self.actionExit.triggered.connect(self.actionExitTriggered)

		#MenuBarHelp
		self.actionRulesVSSS.triggered.connect(self.actionRulesVSSSTriggered)
		self.actionAbout.triggered.connect(self.actionAboutTriggered)

		#VideoView
		#CheckBoxVideoViewDisableDrawing
		self.checkBoxVideoViewDisableDrawing.clicked.connect(self.getStateCheckBoxVideoViewDisableDrawing)

		#pushButtonVideoViewStart
		self.pushButtonVideoViewStart.clicked.connect(self.pushButtonVideoViewStartCLicked)

		self.updateComboBoxCaptureDeviceInformation()
		self.updateComboBoxControlSerialDevice()

	#MenuBarArquivo
	def actionLoadConfigsTriggered(self):
		return self.close()
	def actionSaveConfigsTriggered(self):
		return self.close()
	def actionSaveasConfigTriggered(self):
		return self.close()
	def actionExitTriggered(self):
		return self.close()

	#MenuBarHelp
	def actionRulesVSSSTriggered(self):
		return self.close()
	def actionAboutTriggered(self):
		return self.close()

	#VideoView
	##Positions
	def updateLabelVideoViewPositionsRobotA(self,x,y,z):
		self.labelVideoViewPositionsRobotA.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")
	def updatelabelVideoViewPositionsRobotB(self,x,y,z):
		self.labelVideoViewPositionsRobotB.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")
	def updateLabelVideoViewPositionsRobotC(self,x,y,z):
		self.labelVideoViewPositionsRobotC.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")
	def updateLabelVideoViewPositionsBall(self,x,y,z):
		self.labelVideoViewPositionsBall.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

	##CheckBoxVideoViewDisableDrawing
	def getStateCheckBoxVideoViewDisableDrawing(self):
		return self.checkBoxVideoViewDisableDrawing.isTristate()

	#FPS
	def uptadeLabelVideoViewFPS(self,fps):
		self.labelVideoViewFPS.setText("FPS: " + str(fps))

	#StartButton
	def pushButtonVideoViewStartCLicked(self):
		print("PushButton")

	#Capture
	##DeviceInformation
	def updateComboBoxCaptureDeviceInformation(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i+1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = glob.glob('/dev/video[0-9]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/.*')
		else:
			raise EnvironmentError('Unsuported plaftorm')

		self.comboBoxCaptureDeviceInformation.clear()

		for port in ports:
			self.comboBoxCaptureDeviceInformation.addItem(port)

	#Control
	#Serial
	def updateComboBoxControlSerialDevice(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i+1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = glob.glob('/dev/ttyU[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsuported plaftorm')

		self.comboBoxControlSerialDevice.clear()

		for port in ports:
			self.comboBoxControlSerialDevice.addItem(port)



def main():
	app=QApplication(sys.argv)
	window=mainWindow()
	window.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()