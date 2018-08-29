import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget,QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
import icons_rc
import serial, glob

class Afrodite(QMainWindow):
	"""docstring for Afrodite """
	def __init__(self):
		super(Afrodite , self).__init__()
		loadUi('mainwindow.ui', self)

		##MenuBar
		#MenuBarArquivo
		self.actionLoadConfigs.triggered.connect(self.actionLoadConfigsTriggered)
		self.actionSaveConfigs.triggered.connect(self.actionSaveConfigsTriggered)
		self.actionSaveasConfigs.triggered.connect(self.actionSaveasConfigTriggered)
		self.actionExit.triggered.connect(self.actionExitTriggered)

		#MenuBarHelp
		self.actionRulesVSSS.triggered.connect(self.actionRulesVSSSTriggered)
		self.actionAbout.triggered.connect(self.actionAboutTriggered)

		##VideoView
		#CheckBoxVideoViewDisableDrawing
		self.checkBoxVideoViewDisableDrawing.clicked.connect(self.getStateCheckBoxVideoViewDisableDrawing)

		#pushButtonVideoViewStart
		self.pushButtonVideoViewStart.clicked.connect(self.pushButtonVideoViewStartCLicked)

		##Capture
		#DeviceInformation
		self.updateComboBoxCaptureDeviceInformation()

		##Control
		#Serial
		self.updateComboBoxControlSerialDevice()

	'''def mouseReleaseEvent(self, QMouseEvent):
   		print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')
	'''

	##MenuBar
	#MenuBarArquivo
	def actionLoadConfigsTriggered(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', '/',"Json files (*.json)")

	def actionSaveConfigsTriggered(self):
		pass

	def actionSaveasConfigTriggered(self):
		QFileDialog.getSaveFileNames(self, 'Save as file', '/',"Json files (*.json)")
		pass

	def actionExitTriggered(self):
		return self.close()

	#MenuBarHelp
	def actionRulesVSSSTriggered(self):
		pass

	def actionAboutTriggered(self):
		pass

	#VideoView
	##Positions
	def updateLabelVideoViewPositionsRobot1(self,x,y,z):
		self.labelVideoViewPositionsRobot1.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")	

	def updateLabelVideoViewPositionsRobot2(self,x,y,z):
		self.labelVideoViewPositionsRobot2.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

	def updateLabelVideoViewPositionsRobot3(self,x,y,z):
		self.labelVideoViewPositionsRobot3.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

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
		print("clicked")
		return True

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

	def getPushButtonCaptureDeviceInformationStart():
		pass

	def updatelabelCaptureDeviceInformation(self, device, driver, card, bus):
		pass

	##DeviceProperties
	###Properties
	def getCaptureDevicePropertiesInput():
		pass

	def getCaptureDevicePropertiesFormat():
		pass

	def getCaptureDevicePropertiesIntervals():
		pass

	def getCaptureDevicePropertiesStandard():
		pass

	def getCaptureDevicePropertiesFrameSize():
		pass

	###CamConfig
	def getCaptureDevicePropertiesBrightness():
		pass

	def getCaptureDevicePropertiesSaturation():
		pass

	def getCaptureDevicePropertiesGain():
		pass

	def getCaptureDevicePropertiesFrequency():
		pass

	def getCaptureDevicePropertiesContrast():
		pass

	def getCaptureDevicePropertiesHue():
		pass

	def getCaptureDevicePropertiesGamma():
		pass

	def getCaptureDevicePropertiesWhiteBalanceCheckBox():
		pass

	def getCaptureDevicePropertiesWhiteBalance():
		pass

	def getCaptureDevicePropertiesBacklight():
		pass

	def getCaptureDevicePropertiesEsposure():
		pass

	def getCaptureDevicePropertiesSharpness():
		pass

	###Warp
	def getPushButtonCaptureWarpWarp():
		pass

	def getPushButtonCaptureWarpReset():
		pass

	def getCaptureWarpOffsetLeft():
		pass

	def getCaptureWarpOffsetRight():
		pass

	#Robot
	##RobotFunctions
	def getPushButtonRobotRobotFunctionsEdit():
		pass

	def getPushButtonRobotRobotFunctionsDone():
		pass

	def getRobotRobotFunctionsRobot():
		pass

	##Speed
	def getPushButtonRobotSpeedEdit():
		pass

	def getPushButtonRobotSpeedDone():
		pass

	def getRobotSpeedAttack():
		pass

	def setRobotSpeedAttackCurrent(speed):
		pass

	def getRobotSpeedDefense():
		pass

	def setRobotSpeedDefenseCurrent(speed):
		pass

	def getRobotSpeedGoalkeeper():
		pass

	def setRobotSpeedGoalkeeperCurrent(speed):
		pass

	##ID
	def getPushButtonRobotIDEdit():
		pass
	
	def getPushButtonRobotIDDone():
		pass

	def setRobotIDRobot1():
		pass

	def setRobotIDRobot2():
		pass

	def setRobotIDRobot3():
		pass

	#Vision
	##Capture
	def getVisionVideoCapturePictureName():
		pass

	def getVisionVideoCaptureVideoName():
		pass

	def getPushButtonVisionVideoCapturePictureNameSave():
		pass

	def getPushButtonVisionVideoCaptureVideoNameSave():
		pass

	##ModeView
	def getVisionModeViewSelectMode():
		pass

	##HSVCalibration
	def getPushButtonVisionHSVCalibrationAdversary():
		pass

	def getPushButtonVisionHSVCalibrationEdit():
		pass

	def getPushButtonVisionHSVCalibrationNext():
		pass

	def getPushButtonVisionHSVCalibrationPrev():
		pass

	###Main
	def getVisionHSVCalibrationMainHmin():
		pass

	def getVisionHSVCalibrationMainSmin():
		pass

	def getVisionHSVCalibrationMainVmin():
		pass

	def getVisionHSVCalibrationMainErode():
		pass

	def getVisionHSVCalibrationMainBlur():
		pass

	def getVisionHSVCalibrationMainSmax():
		pass

	def getVisionHSVCalibrationMainVmax():
		pass
		
	def getVisionHSVCalibrationMainDilate():
		pass

	def getVisionHSVCalibrationMainAmin():
		pass

	###Ball
	def getVisionHSVCalibrationBallHmin():
		pass

	def getVisionHSVCalibrationBallSmin():
		pass

	def getVisionHSVCalibrationBallVmin():
		pass

	def getVisionHSVCalibrationBallErode():
		pass

	def getVisionHSVCalibrationBallBlur():
		pass

	def getVisionHSVCalibrationBallSmax():
		pass

	def getVisionHSVCalibrationBallVmax():
		pass
		
	def getVisionHSVCalibrationBallDilate():
		pass

	def getVisionHSVCalibrationBallAmin():
		pass

	###Opponent
	def getVisionHSVCalibrationOpponentHmin():
		pass

	def getVisionHSVCalibrationOpponetSmin():
		pass

	def getVisionHSVCalibrationOpponetVmin():
		pass

	def getVisionHSVCalibrationOpponentErode():
		pass

	def getVisionHSVCalibrationOpponentBlur():
		pass

	def getVisionHSVCalibrationOpponentSmax():
		pass

	def getVisionHSVCalibrationOpponentVmax():
		pass
		
	def getVisionHSVCalibrationOpponentDilate():
		pass

	def getVisionHSVCalibrationOpponentAmin():
		pass

	###Green
	def getVisionHSVCalibrationGreenHmin():
		pass

	def getVisionHSVCalibrationGreenSmin():
		pass

	def getVisionHSVCalibrationGreenVmin():
		pass

	def getVisionHSVCalibrationGreenErode():
		pass

	def getVisionHSVCalibrationGreenBlur():
		pass

	def getVisionHSVCalibrationGreenSmax():
		pass

	def getVisionHSVCalibrationGreenVmax():
		pass
		
	def getVisionHSVCalibrationGreenDilate():
		pass

	def getVisionHSVCalibrationGreenAmin():
		pass
	
	#Control
	##Serial
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
	
	def getPushButtonControlSerialDeviceStart():
		pass

	def getPushButtonControlSerialDeviceRefresh():
		pass

	def getControlSerialRobots():
		pass

	def getControlSerialSpeedLeft():
		pass

	def getControlSerialSpeedRight():
		pass

	def getControlSerialSendCommand():
		pass

	def getPushButtonControlSerialSendCommand():
		pass

	def getControlSerialSetSkippedFrames():
		pass

	def getPushButtonControlSerialSetSkippedFrames():
		pass

	def setLabelControlSerialDelay(self, delay):
		pass

	##Robot
	def getPushButtonControlRobotStatusRobotUpdate():
		pass

	def setLabelControlRobotStatusLastUpdate():
		pass

	def setControlRobotStatusRobotA():
		pass

	def setControlRobotStatusRobotB():
		pass

	def setControlRobotStatusRobotC():
		pass

	def setControlRobotStatusRobotD():
		pass

	def setControlRobotStatusRobotF():
		pass

	def setControlRobotStatusRobotG():
		pass

	##RobotFunctions
	def getPushButtonControlRobotFunctionsPIDTest():
		pass

	#Strategy
	##Formation
	def getStrategyFormationLoadStrategy():
		pass

	def getPushButtonStrategyFormationLoad():
		pass

	def getPushButtonStrategyFormationDelete():
		pass

	def getStrategyFormationNewStrategy():
		pass

	def getPushButtonStrategyFormationCreate():
		pass

	def getPushButtonStrategyFormationSave():
		pass

	##Transitions
	def getStrategyTransitionsEnableTransistions():
		pass

	##TestParameters
	def getStrategyTestParametersGoalieLine():
		pass

	def getStrategyTestParametersGoalieOffset():
		pass

	def getStrategyTestParametersName3():
		pass

	def getStrategyTestParametersName4():
		pass

	def getStrategyTestParametersName5():
		pass

	def vaiPassar(self):
		pass



def main():
	app=QApplication(sys.argv)
	window=Afrodite()
	window.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()