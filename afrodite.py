# coding=utf-8
import sys
import os
import cv2  # Somente para testes

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMenuBar, QDockWidget, QCheckBox, QStackedWidget, \
    QFileDialog, QGroupBox
from PyQt5.uic import loadUi

from datetime import datetime
import interface.icons_rc
import serial, glob
import serial.tools.list_ports as list_ports
import hades
import threading


class Afrodite(QMainWindow):
    """ Interface do programa. Instancia Hades e chama seus métodos ao receber disparos de eventos. """

    def __init__(self):
        super(Afrodite, self).__init__()

        self.hades = hades.Hades(self)
        self.hades.setup()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'interface/mainwindow.ui')
        loadUi(filename, self)

        self.image = None
        self.objectsToDraw = {}

        # PLAY BUTTON
        self.pushButtonVideoViewStart.clicked.connect(self.clickedPlay)

        # VISION

        # VideoView #
        # CheckBoxVideoViewDisableDrawing
        self.checkBoxVideoViewDisableDrawing.clicked.connect(self.getStateCheckBoxVideoViewDisableDrawing)

        # Capture
        self.pushButtonVisionVideoCapturePictureNameSave.clicked.connect(
            self.getPushButtonVisionVideoCapturePictureNameSave)
        self.pushButtonVisionVideoCaptureVideoNameSave.clicked.connect(
            self.getPushButtonVisionVideoCaptureVideoNameSave)

        # ModeView

        # HSVCalibration
        self.pushButtonVisionHSVCalibrationSwap.clicked.connect(self.getPushButtonVisionHSVCalibrationSwap)
        self.pushButtonVisionHSVCalibrationEdit.clicked.connect(self.getPushButtonVisionHSVCalibrationEdit)
        self.pushButtonVisionHSVCalibrationPrev.clicked.connect(self.getPushButtonVisionHSVCalibrationPrev)
        self.pushButtonVisionHSVCalibrationNext.clicked.connect(self.getPushButtonVisionHSVCalibrationNext)

        # MAIN

        self.spinBoxVisionHSVCalibrationMainHmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainHmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainHmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainHmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainSmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainSmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainSmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainSmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainVmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainVmin.setMaximum(255)
        # self.horizontalSliderVisionHSVCalibrationMainVmin.setMinimum(0)
        # self.horizontalSliderVisionHSVCalibrationMainVmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainErode.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainErode.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainErode.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainErode.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainBlur.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainBlur.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainBlur.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainBlur.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainHmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainHmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainHmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainHmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainSmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainSmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainSmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainSmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainVmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainVmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainVmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainVmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainDilate.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainDilate.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainDilate.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainDilate.setMaximum(255)

        self.spinBoxVisionHSVCalibrationMainAmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationMainAmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationMainAmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationMainAmin.setMaximum(255)

        # BALL

        self.spinBoxVisionHSVCalibrationBallHmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallHmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallHmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallHmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallSmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallSmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallSmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallSmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallVmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallVmin.setMaximum(255)
        # self.horizontalSliderVisionHSVCalibrationBallVmin.setMinimum(0)
        # self.horizontalSliderVisionHSVCalibrationBallVmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallErode.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallErode.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallErode.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallErode.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallBlur.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallBlur.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallBlur.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallBlur.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallHmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallHmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallHmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallHmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallSmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallSmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallSmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallSmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallVmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallVmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallVmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallVmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallDilate.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallDilate.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallDilate.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallDilate.setMaximum(255)

        self.spinBoxVisionHSVCalibrationBallAmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationBallAmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationBallAmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationBallAmin.setMaximum(255)

        # Green
        self.spinBoxVisionHSVCalibrationGreenHmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenHmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenHmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenHmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenSmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenSmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenSmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenSmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenVmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenVmin.setMaximum(255)
        # self.horizontalSliderVisionHSVCalibrationGreenVmin.setMinimum(0)
        # self.horizontalSliderVisionHSVCalibrationGreenVmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenErode.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenErode.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenErode.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenErode.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenBlur.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenBlur.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenBlur.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenBlur.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenHmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenHmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenHmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenHmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenSmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenSmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenSmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenSmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenVmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenVmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenVmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenVmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenDilate.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenDilate.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenDilate.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenDilate.setMaximum(255)

        self.spinBoxVisionHSVCalibrationGreenAmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationGreenAmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationGreenAmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationGreenAmin.setMaximum(255)

        # Opponent

        self.spinBoxVisionHSVCalibrationOpponentHmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentHmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentHmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentHmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentSmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentSmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentSmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentSmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentVmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentVmin.setMaximum(255)
        # self.horizontalSliderVisionHSVCalibrationOpponentVmin.setMinimum(0)
        # self.horizontalSliderVisionHSVCalibrationOpponentVmin.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentErode.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentErode.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentErode.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentErode.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentBlur.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentBlur.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentBlur.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentBlur.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentHmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentHmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentHmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentHmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentSmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentSmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentSmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentSmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentVmax.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentVmax.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentVmax.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentVmax.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentDilate.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentDilate.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentDilate.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentDilate.setMaximum(255)

        self.spinBoxVisionHSVCalibrationOpponentAmin.setMinimum(0)
        self.spinBoxVisionHSVCalibrationOpponentAmin.setMaximum(255)
        self.horizontalSliderVisionHSVCalibrationOpponentAmin.setMinimum(0)
        self.horizontalSliderVisionHSVCalibrationOpponentAmin.setMaximum(255)

        # Capture
        # DeviceInformation
        self.pushButtonCaptureDeviceInformationStart.clicked.connect(self.getPushButtonCaptureDeviceInformationStart)
        self.updateComboBoxCaptureDeviceInformation()
        self.getComboBoxCaptureDeviceInformation()

        # Warp
        self.pushButtonCaptureWarpWarp.clicked.connect(self.getPushButtonCaptureWarpWarp)
        self.pushButtonCaptureWarpReset.clicked.connect(self.getPushButtonCaptureWarpReset)
        self.pushButtonCaptureWarpAdjust.clicked.connect(self.getPushButtonCaptureWarpAdjust)

        # STRATEGY

        # transitions
        self.checkBoxStrategyTransitionsEnableTransistions.clicked.connect(self.toggleTransitions)

        # roles
        self.pushButtonRobotRobotFunctionsEdit.clicked.connect(self.clickEditRoles)
        self.pushButtonRobotRobotFunctionsDone.clicked.connect(self.clickDoneRoles)

        '''
        # formation load
        self.pushButtonStrategyFormationLoad.clicked.connect(self.getPushButtonStrategyFormationLoad)
        self.pushButtonStrategyFormationDelete.clicked.connect(self.getPushButtonStrategyFormationDelete)
        self.pushButtonStrategyFormationCreate.clicked.connect(self.getPushButtonStrategyFormationCreate)
        self.pushButtonStrategyFormationSave.clicked.connect(self.getPushButtonStrategyFormationSave)
        '''

        # CONTROL

        # speeds
        self.progressBarRobotSpeedAttack.setValue(0)
        self.spinBoxRobotSpeedAttack.setValue(0)
        self.spinBoxRobotSpeedAttack.setMinimum(0)
        self.spinBoxRobotSpeedAttack.setMaximum(140)
        self.horizontalSliderRobotSpeedAttack.setMinimum(0)
        self.horizontalSliderRobotSpeedAttack.setMaximum(140)

        self.progressBarRobotSpeedDefense.setValue(0)
        self.spinBoxRobotSpeedDefense.setValue(0)
        self.spinBoxRobotSpeedDefense.setMinimum(0)
        self.spinBoxRobotSpeedDefense.setMaximum(140)
        self.horizontalSliderRobotSpeedDefense.setMinimum(0)
        self.horizontalSliderRobotSpeedDefense.setMaximum(140)

        self.progressBarRobotSpeedGoalkeeper.setValue(0)
        self.spinBoxRobotSpeedGoalkeeper.setValue(0)
        self.spinBoxRobotSpeedGoalkeeper.setMinimum(0)
        self.spinBoxRobotSpeedGoalkeeper.setMaximum(140)
        self.horizontalSliderRobotSpeedGoalkeeper.setMinimum(0)
        self.horizontalSliderRobotSpeedGoalkeeper.setMaximum(140)

        self.pushButtonRobotSpeedEdit.clicked.connect(self.getPushButtonRobotSpeedEdit)
        self.pushButtonRobotSpeedDone.clicked.connect(self.getPushButtonRobotSpeedDone)

        # pid test
        self.pushButtonControlRobotFunctionsPIDTest.clicked.connect(self.getPushButtonControlRobotFunctionsPIDTest)

        # COMMUNICATION
        self.pushButtonControlSerialDeviceStart.clicked.connect(self.getPushButtonControlSerialDeviceStart)
        self.pushButtonControlSerialDeviceRefresh.clicked.connect(self.getPushButtonControlSerialDeviceRefresh)

        self.pushButtonControlSerialSend.clicked.connect(self.getPushButtonControlSerialSend)
        self.pushButtonControlSerialSendCommand.clicked.connect(self.getPushButtonControlSerialSendCommand)
        self.updateComboBoxControlSerialDevice()
        self.getComboBoxControlSerialDevice()

        '''
        # Serial        
        self.pushButtonControlSerialSetSkippedFrames.clicked.connect(self.getPushButtonControlSerialSetSkippedFrames)
        

        # RobotStatus
        self.pushButtonControlRobotStatusRobotUpdate.clicked.connect(self.getPushButtonControlRobotStatusRobotUpdate)

        # id
        self.pushButtonRobotIDEdit.clicked.connect(self.getPushButtonRobotIDEdit)
        self.pushButtonRobotIDDone.clicked.connect(self.getPushButtonRobotIDDone)
        '''
        # MENUBAR

        # MenuBar - Arquivo
        self.actionExit.triggered.connect(self.actionExitTriggered)
        '''
        self.actionLoadConfigs.triggered.connect(self.actionLoadConfigsTriggered)
        self.actionSaveConfigs.triggered.connect(self.actionSaveConfigsTriggered)
        self.actionSaveasConfigs.triggered.connect(self.actionSaveasConfigTriggered)
        
        # MenuBar - Help
        self.actionRulesVSSS.triggered.connect(self.actionRulesVSSSTriggered)
        self.actionAbout.triggered.connect(self.actionAboutTriggered)
        '''

        print("Afrodite summoned")

    '''
    def mouseReleaseEvent(self, QMouseEvent):
           print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')           
    '''

    # PLAY BUTTON
    def clickedPlay(self):
        self.hades.eventStartGame()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.hades.eventStartGame()

    # STRATEGY

    # transitions
    def toggleTransitions(self):
        self.hades.eventToggleTransitions(self.checkBoxStrategyTransitionsEnableTransistions.isTristate())

    # role
    def clickEditRoles(self):
        self.pushButtonRobotRobotFunctionsEdit.setEnabled(False)
        self.pushButtonRobotRobotFunctionsDone.setEnabled(True)
        self.comboBoxRobotRobotFunctionsRobot1.setEnabled(True)
        self.comboBoxRobotRobotFunctionsRobot2.setEnabled(True)
        self.comboBoxRobotRobotFunctionsRobot3.setEnabled(True)

    def clickDoneRoles(self):
        self.pushButtonRobotRobotFunctionsEdit.setEnabled(True)
        self.pushButtonRobotRobotFunctionsDone.setEnabled(False)
        self.comboBoxRobotRobotFunctionsRobot1.setEnabled(False)
        self.comboBoxRobotRobotFunctionsRobot2.setEnabled(False)
        self.comboBoxRobotRobotFunctionsRobot3.setEnabled(False)

        self.hades.eventSelectRoles([self.comboBoxRobotRobotFunctionsRobot1.currentText(),
                                     self.comboBoxRobotRobotFunctionsRobot2.currentText(),
                                     self.comboBoxRobotRobotFunctionsRobot3.currentText()])

    # CONTROL

    # speeds
    def getPushButtonRobotSpeedEdit(self):
        self.pushButtonRobotSpeedEdit.setEnabled(False)
        self.pushButtonRobotSpeedDone.setEnabled(True)
        self.spinBoxRobotSpeedAttack.setEnabled(True)
        self.horizontalSliderRobotSpeedAttack.setEnabled(True)
        self.spinBoxRobotSpeedDefense.setEnabled(True)
        self.horizontalSliderRobotSpeedDefense.setEnabled(True)
        self.spinBoxRobotSpeedGoalkeeper.setEnabled(True)
        self.horizontalSliderRobotSpeedGoalkeeper.setEnabled(True)

    def getPushButtonRobotSpeedDone(self):
        self.pushButtonRobotSpeedEdit.setEnabled(True)
        self.pushButtonRobotSpeedDone.setEnabled(False)
        self.spinBoxRobotSpeedAttack.setEnabled(False)
        self.horizontalSliderRobotSpeedAttack.setEnabled(False)
        self.spinBoxRobotSpeedDefense.setEnabled(False)
        self.horizontalSliderRobotSpeedDefense.setEnabled(False)
        self.spinBoxRobotSpeedGoalkeeper.setEnabled(False)
        self.horizontalSliderRobotSpeedGoalkeeper.setEnabled(False)
        self.updateRobotSpeeds()

        return self.spinBoxRobotSpeedAttack.value(), \
               self.spinBoxRobotSpeedDefense.value(), \
               self.spinBoxRobotSpeedGoalkeeper.value()

    def setRobotSpeedAttackCurrent(self, speed):
        self.progressBarRobotSpeedAttack.setValue(speed)

    def setRobotSpeedDefenseCurrent(self, speed):
        self.progressBarRobotSpeedDefense.setValue(speed)

    def setRobotSpeedGoalkeeperCurrent(self, speed):
        self.progressBarRobotSpeedGoalkeeper.setValue(speed)

    def setRobotSpeeds(self, speedAtack, speedDefense, speedGoalKeeper):
        self.setRobotSpeedAttackCurrent(speedAtack)
        self.setRobotSpeedDefenseCurrent(speedDefense)
        self.setRobotSpeedGoalkeeperCurrent(speedGoalKeeper)

    def updateRobotSpeeds(self):
        self.hades.eventUpdateSpeeds(self.spinBoxRobotSpeedAttack.value() / 100.0,
                                     self.spinBoxRobotSpeedDefense.value() / 100.0,
                                     self.spinBoxRobotSpeedGoalkeeper.value() / 100.0)

    # PIDTest
    def getPushButtonControlRobotFunctionsPIDTest(self):
        if self.pushButtonControlRobotFunctionsPIDTest.palette().button().color().name() == '#efefef':
            self.pushButtonControlRobotFunctionsPIDTest.setStyleSheet('background-color:#ff0000')
            self.hades.enablePIDTest()

        elif self.pushButtonControlRobotFunctionsPIDTest.palette().button().color().name() == '#ff0000':
            self.pushButtonControlRobotFunctionsPIDTest.setStyleSheet('background-color:#efefef')
            self.hades.disablePIDTest()

    # COMMUNICATION

    def startSerialConnection(self):
        port = self.comboBoxControlSerialDevice.currentText()
        self.hades.eventStartXbee(port)

    def sendWheelVelocities(self):
        # TODO robotId = getControlSerialRobots()
        robotId = None
        leftWheel = self.controlSerialSpeedLeft.currentText()
        rightWheel = self.controlSerialSpeedRight.currentText()
        self.hades.eventCreateAndSendMessage(robotId, leftWheel, rightWheel)

    def sendCommand(self):
        message = self.controlSerialSendCommand.currentText()
        self.hades.eventSendMessage(message)

    # MENU BAR
    # MenuBarArquivo
    '''
    def actionLoadConfigsTriggered(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/', "Json files (*.json)")
        self.loadConfigCallback()

    def actionSaveConfigsTriggered(self):
        # TODO falta implementar o save
        self.saveConfigCallback()

    def actionSaveasConfigTriggered(self):
        QFileDialog.getSaveFileNames(self, 'Save as file', '/',"Json files (*.json)")
        pass
    '''

    def actionExitTriggered(self):
        return self.close()

    # MenuBarHelp
    '''
    def actionRulesVSSSTriggered(self):
        pass

    def actionAboutTriggered(self):
        pass
    '''

    # VideoView
    # Positions
    def updateLabelVideoViewPositionsRobot1(self, position, orientation):
        self.labelVideoViewPositionsRobot1.setText("(" + str(position[0]) + ", " + str(position[1]) + ", " +
                                                   str(orientation) + " rad)")

    def updateLabelVideoViewPositionsRobot2(self, position, orientation):
        self.labelVideoViewPositionsRobot2.setText("(" + str(position[0]) + ", " + str(position[1]) + ", " +
                                                   str(orientation) + " rad)")

    def updateLabelVideoViewPositionsRobot3(self, position, orientation):
        self.labelVideoViewPositionsRobot3.setText("(" + str(position[0]) + ", " + str(position[1]) + ", " +
                                                   str(orientation) + " rad)")

    def updateLabelVideoViewPositionsBall(self, position):
        self.labelVideoViewPositionsBall.setText("(" + str(position[0]) + ", " + str(position[1]) + ")")

    # CheckBoxVideoViewDisableDrawing
    def getStateCheckBoxVideoViewDisableDrawing(self):
        return self.checkBoxVideoViewDisableDrawing.isTristate()

    # FPS
    def setLabelVideoViewFPS(self, fps):
        self.labelVideoViewFPS.setText("FPS: " + str(fps))

    # LoadImage

    def updateFrameVideoView(self, image):
        self.image = image

        # desenhar na tela
        if not self.checkBoxVideoViewDisableDrawing.isChecked():
            self.drawImageVideoView()

        self.displayImageVideoView(1)

        return None

    def displayImageVideoView(self, window=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if self.image.shape[2] == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)

        outImage = outImage.rgbSwapped()

        if window == 1:
            self.graphicsViewVideoViewVideo.setPixmap(QPixmap.fromImage(outImage))
            self.graphicsViewVideoViewVideo.setScaledContents(True)

    @staticmethod
    def graphicsViewVideoViewVideoClicked():  # event
        point = QtGui.QCursor.pos()
        print("X:" + str(point.x()) + " | " + "Y:" + str(point.y()))

    def drawImageVideoView(self):
        """Itera sobre o self.objectsToDraw e desenha cada objeto
        Os objetos nessa lista devem ser do tipo:
        {
            "shape": "circle" | "rect" | "robot",
            "position": (x, y),
            "color": (r, g, b),
            "label": # string - rótulo do objeto (opcional)
            "radius": # number - se shape = circle
            "limit": (x1, y1) # se shape = rect
            "orientation": # number - se shape = robot (opcional)
            "target": (x2, y2) # se shape = robot (opcional)
            "targetOrientation": (x3, y3) # se shape = robot (opcional)
        }
        """
        if self.image is not None:
            for key, objectToDraw in self.objectsToDraw.items():
                if objectToDraw["shape"] == "robot":
                    cv2.rectangle(self.image, objectToDraw["position"],
                                  (objectToDraw["position"][0] + 10, objectToDraw["position"][1] + 10),
                                  objectToDraw["color"], 2)

                    if "label" in objectToDraw:
                        cv2.putText(self.image, objectToDraw["label"], objectToDraw["position"],
                                    cv2.FONT_HERSHEY_PLAIN, 1, objectToDraw["color"], 2)

                    if "target" in objectToDraw:
                        cv2.line(self.image, objectToDraw["position"], objectToDraw["target"], objectToDraw["color"], 2)
                        cv2.circle(self.image, objectToDraw["target"], 5, objectToDraw["color"], 2)

                elif objectToDraw["shape"] == "circle":
                    cv2.circle(self.image, objectToDraw["position"], objectToDraw["radius"], objectToDraw["color"], 2)

                    if "label" in objectToDraw:
                        cv2.putText(self.image, objectToDraw["label"], objectToDraw["position"],
                                    cv2.FONT_HERSHEY_PLAIN, 1, objectToDraw["color"], 2)

                elif objectToDraw["shape"] == "rect":
                    cv2.rectangle(self.image, objectToDraw["position"], objectToDraw["limit"], objectToDraw["color"], 2)

    # Capture
    # DeviceInformation
    def getPushButtonCaptureDeviceInformationStart(self):
        print("Botton: DeviceInformationStart : Clicked")
        cameraId = self.getComboBoxCaptureDeviceInformation()
        # TODO: trocar a camera de acordo com o que for selecionado

        self.hades.eventStartVision(cameraId)

    def updateComboBoxCaptureDeviceInformation(self):
        # if sys.platform.startswith('win'):
        cams = []
        try:
            for i in range(0, 3):
                cam = cv2.VideoCapture(i)
                if cam.isOpened():
                    cams.append(str(i))  # 'CAM' + str(i)
                    cam.release()
                else:
                    break
        except:
            pass

        ports = cams
        # cams.clear()
        # elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        #    ports = glob.glob('/dev/video[0-9]*')
        # elif sys.platform.startswith('darwin'):
        #    ports = glob.glob('/dev/*')
        # else:
        #    raise EnvironmentError('Unsuported plaftorm')

        self.comboBoxCaptureDeviceInformation.clear()

        for port in ports:
            self.comboBoxCaptureDeviceInformation.addItem(port)

    def getComboBoxCaptureDeviceInformation(self):
        return self.comboBoxCaptureDeviceInformation.currentText()

    def setlabelCaptureDeviceInformation(self, device, driver, card, bus):
        self.labelCaptureDeviceInformationDevice.setText(device)
        self.labelCaptureDeviceInformationDriver.setText(driver)
        self.labelCaptureDeviceInformationCard.setText(card)
        self.labelCaptureDeviceInformationBus.setText(bus)

    # DeviceProperties
    # Properties
    def getCaptureDevicePropertiesInput(self):
        return self.comboBoxCaptureDevicePropertiesInput.currentText()

    def getCaptureDevicePropertiesFormat(self):
        return self.comboBoxCaptureDevicePropertiesFormat.currentText()

    def getCaptureDevicePropertiesIntervals(self):
        return self.comboBoxCaptureDevicePropertiesIntervals.currentText()

    def getCaptureDevicePropertiesStandard(self):
        return self.comboBoxCaptureDevicePropertiesStandard.currentText()

    def getCaptureDevicePropertiesFrameSize(self):
        return self.comboBoxCaptureDevicePropertiesFrameSize.currentText()

    # CamConfig
    def getCaptureDevicePropertiesBrightness(self):
        return self.spinBoxCaptureDevicePropertiesBrightness.value()

    def getCaptureDevicePropertiesSaturation(self):
        return self.spinBoxCaptureDevicePropertiesSaturation.value()

    def getCaptureDevicePropertiesGain(self):
        return self.spinBoxCaptureDevicePropertiesGain.value()

    def getCaptureDevicePropertiesFrequency(self):
        return self.comboBoxCaptureDevicePropertiesFrequency.currentText()

    def getCaptureDevicePropertiesContrast(self):
        return self.spinBoxCaptureDevicePropertiesContrast.value()

    def getCaptureDevicePropertiesHue(self):
        return self.spinBoxCaptureDevicePropertiesHue.value()

    def getCaptureDevicePropertiesGamma(self):
        return self.spinBoxCaptureDevicePropertiesGamma.value()

    def getCaptureDevicePropertiesWhiteBalanceCheckBox(self):
        return self.checkBoxCaptureDevicePropertiesWhiteBalance.isTristate()

    def getCaptureDevicePropertiesWhiteBalance(self):
        return self.spinBoxCaptureDevicePropertiesWhiteBalance.value()

    def getCaptureDevicePropertiesBacklight(self):
        return self.spinBoxCaptureDevicePropertiesBacklight.value()

    def getCaptureDevicePropertiesEsposure(self):
        return self.spinBoxCaptureDevicePropertiesEsposure.value()

    def getCaptureDevicePropertiesSharpness(self):
        return self.spinBoxCaptureDevicePropertiesSharpness.value()

    # Warp
    def getPushButtonCaptureWarpWarp(self):
        self.startWarpCallback()

    def getPushButtonCaptureWarpReset(self):
        pass

    def getPushButtonCaptureWarpAdjust(self):
        pass

    def getCaptureWarpOffsetLeft(self):
        pass

    def getCaptureWarpOffsetRight(self):
        pass

    # ID
    def getPushButtonRobotIDEdit(self):
        self.pushButtonRobotIDEdit.setEnabled(False)
        self.pushButtonRobotIDDone.setEnabled(True)
        self.lineEditRobotIDRobot1.setEnabled(True)
        self.lineEditRobotIDRobot2.setEnabled(True)
        self.lineEditRobotIDRobot3.setEnabled(True)

    def getPushButtonRobotIDDone(self):
        self.pushButtonRobotIDEdit.setEnabled(True)
        self.pushButtonRobotIDDone.setEnabled(False)
        self.lineEditRobotIDRobot1.setEnabled(False)
        self.lineEditRobotIDRobot2.setEnabled(False)
        self.lineEditRobotIDRobot3.setEnabled(False)

        return self.lineEditRobotIDRobot1.text(), self.lineEditRobotIDRobot2.text(), self.lineEditRobotIDRobot3.text()

    # Vision
    # Capture
    def getVisionVideoCapturePictureName(self):
        return self.lineEditVisionVideoCapturePictureName.text()

    def getVisionVideoCaptureVideoName(self):
        return self.lineEditVisionVideoCaptureVideoName.text()

    def getPushButtonVisionVideoCapturePictureNameSave(self):
        pass

    def getPushButtonVisionVideoCaptureVideoNameSave(self):
        pass

    # ModeView
    def getVisionModeViewSelectMode(self):
        if self.radioButtonVisionModeViewOriginal.isChecked():
            return "Original"
        else:
            return "Split"

    # HSVCalibration
    def getHSVCalibrationOption(self):
        return self.stackedWidgetVisionHSVCalibration.isEnabled()

    def getHSVIndex(self):
        return self.stackedWidgetVisionHSVCalibration.currentIndex()

    def getPushButtonVisionHSVCalibrationSwap(self):
        stringAux = self.labelVisionHSVCalibrationSwap.text()
        self.labelVisionHSVCalibrationSwap.setText(self.pushButtonVisionHSVCalibrationSwap.text())
        self.pushButtonVisionHSVCalibrationSwap.setText(stringAux)

        return self.pushButtonVisionHSVCalibrationSwap.text()

    def getPushButtonVisionHSVCalibrationEdit(self):
        if self.stackedWidgetVisionHSVCalibration.isEnabled():
            self.stackedWidgetVisionHSVCalibration.setEnabled(False)
        else:
            self.stackedWidgetVisionHSVCalibration.setEnabled(True)

        self.hades.calibrationEvent()

    def getPushButtonVisionHSVCalibrationNext(self):
        if self.stackedWidgetVisionHSVCalibration.currentIndex() < 3:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(
                self.stackedWidgetVisionHSVCalibration.currentIndex() + 1
            )

    def getPushButtonVisionHSVCalibrationPrev(self):
        if self.stackedWidgetVisionHSVCalibration.currentIndex() > 0:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(
                self.stackedWidgetVisionHSVCalibration.currentIndex() - 1
            )

    def getHSVCalibration(self, index):
        if index == 0:
            return self.getVisionHSVCalibrationMain()
        elif index == 1:
            return self.getVisionHSVCalibrationBall()
        elif index == 2:
            return self.getVisionHSVCalibrationOpponent()
        elif index == 3:
            return self.getVisionHSVCalibrationGreen()

    # Main
    def getVisionHSVCalibrationMain(self):
        Hmin = self.spinBoxVisionHSVCalibrationMainHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationMainSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationMainVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationMainErode.value()
        Blur = self.spinBoxVisionHSVCalibrationMainBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationMainHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationMainSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationMainVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationMainDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationMainAmin.value()

        return (Hmin, Hmax), (Smin, Smax), (Vmin, Vmax), Erode, Blur, Dilate, Amin

    # Ball
    def getVisionHSVCalibrationBall(self):
        Hmin = self.spinBoxVisionHSVCalibrationBallHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationBallSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationBallVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationBallErode.value()
        Blur = self.spinBoxVisionHSVCalibrationBallBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationBallHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationBallSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationBallVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationBallDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationBallAmin.value()

        return (Hmin, Hmax), (Smin, Smax), (Vmin, Vmax), Erode, Blur, Dilate, Amin

    # Opponent
    def getVisionHSVCalibrationOpponent(self):
        Hmin = self.spinBoxVisionHSVCalibrationOpponentHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationOpponentSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationOpponentVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationOpponentErode.value()
        Blur = self.spinBoxVisionHSVCalibrationOpponentBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationOpponentHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationOpponentSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationOpponentVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationOpponentDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationOpponentAmin.value()

        return (Hmin, Hmax), (Smin, Smax), (Vmin, Vmax), Erode, Blur, Dilate, Amin

    # Green
    def getVisionHSVCalibrationGreen(self):
        Hmin = self.spinBoxVisionHSVCalibrationGreenHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationGreenSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationGreenVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationGreenErode.value()
        Blur = self.spinBoxVisionHSVCalibrationGreenBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationGreenHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationGreenSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationGreenVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationGreenDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationGreenAmin.value()

        return (Hmin, Hmax), (Smin, Smax), (Vmin, Vmax), Erode, Blur, Dilate, Amin

    # Control
    # Serial
    def getPushButtonControlSerialDeviceStart(self):
        device = self.getComboBoxControlSerialDevice()
        self.hades.eventStartXbee(device)

    def updateComboBoxControlSerialDevice(self):
        if sys.platform.startswith('win'):
            serial_ports = list_ports.comports()
            result = []
            for port in serial_ports:
                try:
                    s = serial.Serial(port.device)
                    s.close()
                    result.append(port.device)
                except (OSError, serial.SerialException):
                    pass
            ports = result
            # result.clear()
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/ttyU[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsuported plaftorm')

        self.comboBoxControlSerialDevice.clear()

        for port in ports:
            self.comboBoxControlSerialDevice.addItem(port)

    def getComboBoxControlSerialDevice(self):
        return self.comboBoxControlSerialDevice.currentText()

    def getPushButtonControlSerialDeviceRefresh(self):
        self.updateComboBoxControlSerialDevice()

    def getPushButtonControlSerialSend(self):
        robotId = self.comboBoxControlSerialRobots.currentText()
        left = self.lineEditControlSerialSpeedLeft.text()
        right = self.lineEditControlSerialSpeedRight.text()
        if robotId is not None and left != "" and right != "":
            self.hades.eventCreateAndSendMessage(robotId, left, right)

    def getPushButtonControlSerialSendCommand(self):
        command = self.lineEditControlSerialSendCommand.text()
        if command != "":
            self.hades.eventSendMessage(command)

    '''
    def getControlSerialSetSkippedFrames(self):
        pass

    def getPushButtonControlSerialSetSkippedFrames(self):
        pass

    def setLabelControlSerialDelay(self, delay):
        pass

    # Robot
    def getPushButtonControlRobotStatusRobotUpdate(self):
        self.setLabelControlRobotStatusLastUpdate()

    def setLabelControlRobotStatusLastUpdate(self):
        now = datetime.now()
        self.labelControlRobotStatusLastUpdate.setText("Last Update: " + str(now.hour) + ":" + str(now.minute) + ":" + 
        str(now.second))

    def setControlRobotStatusRobotA(self, status):
        self.progressBarControlRobotStatusRobotA.setValue(status)

    def setControlRobotStatusRobotB(self, status):
        self.progressBarControlRobotStatusRobotB.setValue(status)

    def setControlRobotStatusRobotC(self, status):
        self.progressBarControlRobotStatusRobotC.setValue(status)

    def setControlRobotStatusRobotD(self, status):
        self.progressBarControlRobotStatusRobotD.setValue(status)

    def setControlRobotStatusRobotF(self, status):
        self.progressBarControlRobotStatusRobotF.setValue(status)

    def setControlRobotStatusRobotG(self, status):
        self.progressBarControlRobotStatusRobotG.setValue(status)

    def setContolRobotStatus(self, statusA, statusB, statusC, statusD, statusF, statusG):
        self.setControlRobotStatusRobotA(statusA)
        self.setControlRobotStatusRobotB(statusB)
        self.setControlRobotStatusRobotC(statusC)
        self.setControlRobotStatusRobotD(statusD)
        self.setControlRobotStatusRobotF(statusF)
        self.setControlRobotStatusRobotG(statusG)
    '''

    # Strategy
    # Formation
    def updateComboBoxStrategyFormationLoadStrategy(self, strategys):
        self.comboBoxStrategyFormationLoadStrategy.clear()
        for strategy in strategys:
            self.comboBoxStrategyFormationLoadStrategy.addItem(strategy)

    def getStrategyFormationLoadStrategy(self):
        pass

    def getPushButtonStrategyFormationLoad(self):
        pass

    def getPushButtonStrategyFormationDelete(self):
        pass

    def getStrategyFormationNewStrategy(self):
        pass

    def getPushButtonStrategyFormationCreate(self):
        pass

    def getPushButtonStrategyFormationSave(self):
        pass

    # TestParameters
    def getStrategyTestParameters(self):
        return self.getStrategyTestParametersGoalieLine(), \
               self.getStrategyTestParametersGoalieOffset(), \
               self.getStrategyTestParametersName3(), \
               self.getStrategyTestParametersName4(), \
               self.getStrategyTestParametersName5()

    def getStrategyTestParametersGoalieLine(self):
        return self.spinBoxStrategyTestParametersGoalieLine.value()

    def getStrategyTestParametersGoalieOffset(self):
        return self.spinBoxStrategyTestParametersGoalieLine.value()

    def getStrategyTestParametersName3(self):
        return self.spinBoxStrategyTestParametersGoalieLine.value()

    def getStrategyTestParametersName4(self):
        return self.spinBoxStrategyTestParametersGoalieLine.value()

    def getStrategyTestParametersName5(self):
        return self.spinBoxStrategyTestParametersGoalieLine.value()


def main():
    app = QApplication(sys.argv)
    window = Afrodite()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
