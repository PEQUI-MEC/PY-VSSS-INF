# coding=utf-8
import sys
import os
import cv2  # Somente para testes

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import serial
import glob
import interface.icons_rc
import serial.tools.list_ports as list_ports
import hades


class Afrodite(QMainWindow):
    """ Interface do programa. Instancia Hades e chama seus métodos ao receber disparos de eventos. """

    def __init__(self):
        super(Afrodite, self).__init__()

        self.hades = hades.Hades()
        self.hades.setup()
        self.hades.sigFps.connect(self.setLabelPlayFPS)
        self.hades.sigDraw.connect(self.updateObjectsToDraw)
        self.hades.sigDisplay.connect(self.updateFrameVideoView)
        self.hades.sigPositions.connect(self.updateLabelPlayPositions)
        self.hades.start()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'interface/mainwindow.ui')
        loadUi(filename, self)

        self.image = None
        self.objectsToDraw = {}

        # PLAY
        self.pushButtonPlayStart.clicked.connect(self.clickedPlay)
        self.pushButtonPlayConnect.clicked.connect(self.clickedConnect)
        #self.pushButtonPlayStart.clicked.connect(self.record)  # A gravação será feita aqui
        # self.pushButtonPlayConnect.clicked.connect(self.record)  # Para testar a gravação

        # VISION
        self.recordFlag = False
        self.cameraIsRunning = False

        # Capture
        self.spinBoxCaptureDevicePropertiesBrightness.valueChanged.connect(self.camConfigsChanged)
        self.spinBoxCaptureDevicePropertiesSaturation.valueChanged.connect(self.camConfigsChanged)
        self.spinBoxCaptureDevicePropertiesGain.valueChanged.connect(self.camConfigsChanged)
        self.spinBoxCaptureDevicePropertiesContrast.valueChanged.connect(self.camConfigsChanged)
        self.spinBoxCaptureDevicePropertiesExposure.valueChanged.connect(self.camConfigsChanged)
        self.spinBoxCaptureDevicePropertiesWhiteBalance.valueChanged.connect(self.camConfigsChanged)

        # ModeView

        # HSVCalibration
        # Main
        self.horizontalSliderVisionHSVCalibrationMainVmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainBlur.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainErode.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainHmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainSmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainAmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainDilate.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainHmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainSmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationMainVmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)

        # Ball
        self.horizontalSliderVisionHSVCalibrationBallBlur.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallErode.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallHmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallSmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallVmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallAmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallDilate.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallHmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallSmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationBallVmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)

        # Opponent
        self.horizontalSliderVisionHSVCalibrationOpponentBlur.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentErode.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentHmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentSmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentVmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentAmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentDilate.valueChanged.connect(
            self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentHmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentSmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationOpponentVmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)

        # Green
        self.horizontalSliderVisionHSVCalibrationGreenBlur.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenErode.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenHmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenSmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenVmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenAmin.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenDilate.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenHmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenSmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.horizontalSliderVisionHSVCalibrationGreenVmax.valueChanged.connect(self.visionHSVCalibrationSliderChanged)
        self.pushButtonVisionHSVCalibrationSwap.clicked.connect(self.getPushButtonVisionHSVCalibrationSwap)
        self.pushButtonVisionHSVCalibrationEdit.clicked.connect(self.getPushButtonVisionHSVCalibrationEdit)
        self.pushButtonVisionHSVCalibrationPrev.clicked.connect(self.getPushButtonVisionHSVCalibrationPrev)
        self.pushButtonVisionHSVCalibrationNext.clicked.connect(self.getPushButtonVisionHSVCalibrationNext)

        # Capture
        # DeviceInformation
        self.pushButtonCaptureDeviceInformationStart.clicked.connect(self.getPushButtonCaptureDeviceInformationStart)
        self.pushButtonCaptureDeviceInformationRefresh.clicked.connect(self.updateComboBoxCaptureDeviceInformation)
        self.updateComboBoxCaptureDeviceInformation()

        # Warp
        self.checkBoxInvertImage.clicked.connect(self.toggleInvertImage)

        self.pushButtonCaptureWarpWarp.clicked.connect(self.getPushButtonCaptureWarpWarp)
        self.pushButtonCaptureWarpReset.clicked.connect(self.getPushButtonCaptureWarpReset)
        self.pushButtonCaptureWarpAdjust.clicked.connect(self.getPushButtonCaptureWarpAdjust)

        # STRATEGY

        # transitions
        self.checkBoxStrategyTransitionsEnableTransistions.clicked.connect(self.toggleTransitions)

        # roles
        self.pushButtonStrategyRobotFunctionsEdit.clicked.connect(self.clickEditRoles)
        self.pushButtonStrategyRobotFunctionsDone.clicked.connect(self.clickDoneRoles)

        '''
        # formation load
        self.pushButtonStrategyFormationLoad.clicked.connect(self.getPushButtonStrategyFormationLoad)
        self.pushButtonStrategyFormationDelete.clicked.connect(self.getPushButtonStrategyFormationDelete)
        self.pushButtonStrategyFormationCreate.clicked.connect(self.getPushButtonStrategyFormationCreate)
        self.pushButtonStrategyFormationSave.clicked.connect(self.getPushButtonStrategyFormationSave)
        '''

        # CONTROL

        # speeds
        self.pushButtonRobotSpeedEdit.clicked.connect(self.getPushButtonRobotSpeedEdit)
        self.pushButtonRobotSpeedDone.clicked.connect(self.getPushButtonRobotSpeedDone)

        # pid test
        self.pushButtonComunicationRobotFunctionsPIDTest.clicked.connect(self.getPushButtonControlRobotFunctionsPIDTest)

        # COMMUNICATION

        self.pushButtonControlSerialDeviceStart.clicked.connect(self.getPushButtonControlSerialDeviceStart)
        self.pushButtonControlSerialDeviceRefresh.clicked.connect(self.getPushButtonControlSerialDeviceRefresh)
        self.pushButtonControlSerialSend.clicked.connect(self.getPushButtonControlSerialSend)
        self.updateComboBoxControlSerialDevice()
        self.getComboBoxControlSerialDevice()
        '''     
        self.pushButtonControlSerialSetSkippedFrames.clicked.connect(self.getPushButtonControlSerialSetSkippedFrames)
        # RobotStatus
        self.pushButtonControlRobotStatusRobotUpdate.clicked.connect(self.getPushButtonControlRobotStatusRobotUpdate)
        '''

        # id
        self.pushButtonRobotIDEdit.clicked.connect(self.getPushButtonRobotIDEdit)
        self.pushButtonRobotIDDone.clicked.connect(self.getPushButtonRobotIDDone)

        # MENUBAR

        # MenuBar - Arquivo
        self.actionExit.triggered.connect(self.actionExitTriggered)
        self.actionLoadConfigs.triggered.connect(self.actionLoadConfigsTriggered)
        self.actionSaveConfigs.triggered.connect(self.actionSaveConfigsTriggered)
        self.loadConfigs(file="quicksave")

        '''        
        # MenuBar - Help
        self.actionRulesVSSS.triggered.connect(self.actionRulesVSSSTriggered)
        self.actionAbout.triggered.connect(self.actionAboutTriggered)
        '''

        print("Afrodite summoned")

    def closeEvent(self, QCloseEvent):
        self.saveConfigs(file="quicksave")
        QCloseEvent.accept()
        self.hades.exit()

    '''
    def mouseReleaseEvent(self, QMouseEvent):
           print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')           
    '''

    # PLAY BUTTON
    def clickedPlay(self):
        icon = QIcon()
        if self.hades.eventStartGame():
            icon.addPixmap(QPixmap('interface/Imgs/Pause.png'))
            self.pushButtonPlayStart.setIcon(icon)
        else:
            icon.addPixmap(QPixmap('interface/Imgs/Play.png'))
            self.pushButtonPlayStart.setIcon(icon)
        self.record()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space and self.pushButtonPlayStart.isEnabled():
            self.clickedPlay()

    def clickedConnect(self):
        lastCamera = self.comboBoxCaptureDeviceInformation.itemText(self.comboBoxCaptureDeviceInformation.count() - 1)
        if lastCamera:
            self.comboBoxCaptureDeviceInformation.setCurrentText(lastCamera)
            self.getPushButtonCaptureDeviceInformationStart()

        lastComm = self.comboBoxControlSerialDevice.itemText(self.comboBoxControlSerialDevice.count() - 1)
        if lastComm:
            self.comboBoxControlSerialDevice.setCurrentText(lastComm)
            self.getPushButtonControlSerialDeviceStart()

        self.pushButtonPlayConnect.setEnabled(False)

    def record(self):
        if not self.recordFlag:
            self.recordFlag = True
        else:   
            self.recordFlag = False

        print(self.recordFlag)

        self.hades.eventRecordVideo(self.recordFlag)  # nome será gerado de outras maneiras depois

    # VideoView
    # Positions
    def updateLabelPlayPositions(self, positions):
        self.labelPlayPositionsRobot1.setText(
            "(" + str(positions[0][0][0]) + ", " + str(positions[0][0][1]) + ", " +
            str(positions[0][1]) + " rad)")
        self.labelPlayPositionsRobot2.setText(
            "(" + str(positions[1][0][0]) + ", " + str(positions[1][0][1]) + ", " +
            str(positions[1][1]) + " rad)")
        self.labelPlayPositionsRobot3.setText(
            "(" + str(positions[2][0][0]) + ", " + str(positions[2][0][1]) + ", " +
            str(positions[2][1]) + " rad)")
        self.labelPlayPositionsBall.setText("(" + str(positions[3][0]) + ", " + str(positions[3][1]) + ")")

    # FPS
    def setLabelPlayFPS(self, fps):
        self.labelPlayFPSValue.setText(str(fps))

    # LoadImage
    def updateFrameVideoView(self, image):
        self.image = image

        # desenhar na tela
        if not self.checkBoxPlayDisableDrawing.isChecked():
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

    def updateObjectsToDraw(self, newObjects):
        self.objectsToDraw = newObjects

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
                        cv2.line(self.image, objectToDraw["position"], objectToDraw["target"],
                                 objectToDraw["color"], 2)
                        cv2.circle(self.image, objectToDraw["target"], 5, objectToDraw["color"], 2)

                elif objectToDraw["shape"] == "circle":
                    cv2.circle(self.image, objectToDraw["position"], objectToDraw["radius"], objectToDraw["color"],
                               2)

                    if "label" in objectToDraw:
                        cv2.putText(self.image, objectToDraw["label"], objectToDraw["position"],
                                    cv2.FONT_HERSHEY_PLAIN, 1, objectToDraw["color"], 2)

                elif objectToDraw["shape"] == "rect":
                    cv2.rectangle(self.image, objectToDraw["position"], objectToDraw["limit"],
                                  objectToDraw["color"], 2)

    # MENU BAR
    # MenuBarArquivo

    def actionLoadConfigsTriggered(self):
        self.loadConfigs()

    def loadConfigs(self, file="save"):
        self.hades.SetFileSave(file)
        self.horizontalSliderCaptureDevicePropertiesBrightness.setValue(self.hades.eventLoadConfigs("brightness"))
        self.horizontalSliderCaptureDevicePropertiesSaturation.setValue(self.hades.eventLoadConfigs("saturation"))
        self.horizontalSliderCaptureDevicePropertiesGain.setValue(self.hades.eventLoadConfigs("gain"))
        self.horizontalSliderCaptureDevicePropertiesContrast.setValue(self.hades.eventLoadConfigs("contrast"))
        self.horizontalSliderCaptureDevicePropertiesSharpness.setValue(self.hades.eventLoadConfigs("sharpness"))
        self.horizontalSliderCaptureDevicePropertiesWhiteBalance.setValue(self.hades.eventLoadConfigs("balance"))
        self.checkBoxCaptureDevicePropertiesWhiteBalanceAuto.setChecked(self.hades.eventLoadConfigs("balanceauto"))
        self.horizontalSliderCaptureDevicePropertiesZoom.setValue(self.hades.eventLoadConfigs("zoom"))
        self.horizontalSliderCaptureDevicePropertiesExposure.setValue(self.hades.eventLoadConfigs("exposure"))
        self.horizontalSliderCaptureDevicePropertiesExposureAuto.setValue(self.hades.eventLoadConfigs("exposureauto"))
        self.checkBoxCaptureDevicePropertiesExposureAutoPriority.\
            setChecked(self.hades.eventLoadConfigs("exposureautopriority"))
        self.horizontalSliderCaptureDevicePropertiesTilt.setValue(self.hades.eventLoadConfigs("tilt"))
        self.horizontalSliderCaptureDevicePropertiesPan.setValue(self.hades.eventLoadConfigs("pan"))
        self.horizontalSliderCaptureDevicePropertiesFocus.setValue(self.hades.eventLoadConfigs("focus"))
        self.checkBoxCaptureDevicePropertiesFocusAuto.setChecked(self.hades.eventLoadConfigs("focusauto"))

        self.comboBoxStrategyRobotFunctionsRobot1.setCurrentText(str(self.hades.eventLoadConfigs("robot1")))
        self.comboBoxStrategyRobotFunctionsRobot2.setCurrentText(str(self.hades.eventLoadConfigs("robot2")))
        self.comboBoxStrategyRobotFunctionsRobot3.setCurrentText(str(self.hades.eventLoadConfigs("robot3")))

        self.horizontalSliderVisionHSVCalibrationMainBlur.setValue(self.hades.eventLoadConfigs("mainBlur"))
        self.horizontalSliderVisionHSVCalibrationMainErode.setValue(self.hades.eventLoadConfigs("mainErode"))
        self.horizontalSliderVisionHSVCalibrationMainHmin.setValue(self.hades.eventLoadConfigs("mainHmin"))
        self.horizontalSliderVisionHSVCalibrationMainSmin.setValue(self.hades.eventLoadConfigs("mainSmin"))
        self.horizontalSliderVisionHSVCalibrationMainVmin.setValue(self.hades.eventLoadConfigs("mainVmin"))
        self.horizontalSliderVisionHSVCalibrationMainAmin.setValue(self.hades.eventLoadConfigs("mainAmin"))
        self.horizontalSliderVisionHSVCalibrationMainDilate.setValue(self.hades.eventLoadConfigs("mainDilate"))
        self.horizontalSliderVisionHSVCalibrationMainHmax.setValue(self.hades.eventLoadConfigs("mainHmax"))
        self.horizontalSliderVisionHSVCalibrationMainSmax.setValue(self.hades.eventLoadConfigs("mainSmax"))
        self.horizontalSliderVisionHSVCalibrationMainVmax.setValue(self.hades.eventLoadConfigs("mainVmax"))

        self.horizontalSliderVisionHSVCalibrationGreenBlur.setValue(self.hades.eventLoadConfigs("greenBlur"))
        self.horizontalSliderVisionHSVCalibrationGreenErode.setValue(self.hades.eventLoadConfigs("greenErode"))
        self.horizontalSliderVisionHSVCalibrationGreenHmin.setValue(self.hades.eventLoadConfigs("greenHmin"))
        self.horizontalSliderVisionHSVCalibrationGreenSmin.setValue(self.hades.eventLoadConfigs("greenSmin"))
        self.horizontalSliderVisionHSVCalibrationGreenVmin.setValue(self.hades.eventLoadConfigs("greenVmin"))
        self.horizontalSliderVisionHSVCalibrationGreenAmin.setValue(self.hades.eventLoadConfigs("greenAmin"))
        self.horizontalSliderVisionHSVCalibrationGreenDilate.setValue(self.hades.eventLoadConfigs("greenDilate"))
        self.horizontalSliderVisionHSVCalibrationGreenHmax.setValue(self.hades.eventLoadConfigs("greenHmax"))
        self.horizontalSliderVisionHSVCalibrationGreenSmax.setValue(self.hades.eventLoadConfigs("greenSmax"))
        self.horizontalSliderVisionHSVCalibrationGreenVmax.setValue(self.hades.eventLoadConfigs("greenVmax"))

        self.horizontalSliderVisionHSVCalibrationBallBlur.setValue(self.hades.eventLoadConfigs("ballBlur"))
        self.horizontalSliderVisionHSVCalibrationBallErode.setValue(self.hades.eventLoadConfigs("ballErode"))
        self.horizontalSliderVisionHSVCalibrationBallHmin.setValue(self.hades.eventLoadConfigs("ballHmin"))
        self.horizontalSliderVisionHSVCalibrationBallSmin.setValue(self.hades.eventLoadConfigs("ballSmin"))
        self.horizontalSliderVisionHSVCalibrationBallVmin.setValue(self.hades.eventLoadConfigs("ballVmin"))
        self.horizontalSliderVisionHSVCalibrationBallAmin.setValue(self.hades.eventLoadConfigs("ballAmin"))
        self.horizontalSliderVisionHSVCalibrationBallDilate.setValue(self.hades.eventLoadConfigs("ballDilate"))
        self.horizontalSliderVisionHSVCalibrationBallHmax.setValue(self.hades.eventLoadConfigs("ballHmax"))
        self.horizontalSliderVisionHSVCalibrationBallSmax.setValue(self.hades.eventLoadConfigs("ballSmax"))
        self.horizontalSliderVisionHSVCalibrationBallVmax.setValue(self.hades.eventLoadConfigs("ballVmax"))

        self.horizontalSliderVisionHSVCalibrationOpponentBlur.setValue(self.hades.eventLoadConfigs("oppBlur"))
        self.horizontalSliderVisionHSVCalibrationOpponentErode.setValue(self.hades.eventLoadConfigs("oppErode"))
        self.horizontalSliderVisionHSVCalibrationOpponentHmin.setValue(self.hades.eventLoadConfigs("oppHmin"))
        self.horizontalSliderVisionHSVCalibrationOpponentSmin.setValue(self.hades.eventLoadConfigs("oppSmin"))
        self.horizontalSliderVisionHSVCalibrationOpponentVmin.setValue(self.hades.eventLoadConfigs("oppVmin"))
        self.horizontalSliderVisionHSVCalibrationOpponentAmin.setValue(self.hades.eventLoadConfigs("oppAmin"))
        self.horizontalSliderVisionHSVCalibrationOpponentDilate.setValue(self.hades.eventLoadConfigs("oppDilate"))
        self.horizontalSliderVisionHSVCalibrationOpponentHmax.setValue(self.hades.eventLoadConfigs("oppHmax"))
        self.horizontalSliderVisionHSVCalibrationOpponentSmax.setValue(self.hades.eventLoadConfigs("oppSmax"))
        self.horizontalSliderVisionHSVCalibrationOpponentVmax.setValue(self.hades.eventLoadConfigs("oppVmax"))

    def actionSaveConfigsTriggered(self):
        self.saveConfigs()

    def saveConfigs(self, file="save"):
        self.hades.SetFileSave(file)
        value = {
            "brightness": self.horizontalSliderCaptureDevicePropertiesBrightness.value(),
            "saturation": self.horizontalSliderCaptureDevicePropertiesSaturation.value(),
            "gain": self.horizontalSliderCaptureDevicePropertiesGain.value(),
            "contrast": self.horizontalSliderCaptureDevicePropertiesContrast.value(),
            "sharpness": self.horizontalSliderCaptureDevicePropertiesSharpness.value(),
            "balance": self.horizontalSliderCaptureDevicePropertiesWhiteBalance.value(),
            "balanceAuto": self.checkBoxCaptureDevicePropertiesWhiteBalanceAuto.isChecked(),
            "zoom": self.horizontalSliderCaptureDevicePropertiesZoom.value(),
            "exposure": self.horizontalSliderCaptureDevicePropertiesExposure.value(),
            "exposureauto": self.horizontalSliderCaptureDevicePropertiesExposureAuto.value(),
            "exposureautopriority": self.checkBoxCaptureDevicePropertiesExposureAutoPriority.isChecked(),
            "tilt": self.horizontalSliderCaptureDevicePropertiesTilt.value(),
            "pan": self.horizontalSliderCaptureDevicePropertiesPan.value(),
            "focus": self.horizontalSliderCaptureDevicePropertiesFocus.value(),
            "focusauto": self.checkBoxCaptureDevicePropertiesFocusAuto.isChecked(),

            "robot1": self.comboBoxStrategyRobotFunctionsRobot1.currentText(),
            "robot2": self.comboBoxStrategyRobotFunctionsRobot2.currentText(),
            "robot3": self.comboBoxStrategyRobotFunctionsRobot3.currentText(),

            "mainBlur": self.horizontalSliderVisionHSVCalibrationMainBlur.value(),
            "mainErode": self.horizontalSliderVisionHSVCalibrationMainErode.value(),
            "mainHmin": self.horizontalSliderVisionHSVCalibrationMainHmin.value(),
            "mainSmin": self.horizontalSliderVisionHSVCalibrationMainSmin.value(),
            "mainVmin": self.horizontalSliderVisionHSVCalibrationMainVmin.value(),
            "mainAmin": self.horizontalSliderVisionHSVCalibrationMainAmin.value(),
            "mainDilate": self.horizontalSliderVisionHSVCalibrationMainDilate.value(),
            "mainHmax": self.horizontalSliderVisionHSVCalibrationMainHmax.value(),
            "mainSmax": self.horizontalSliderVisionHSVCalibrationMainSmax.value(),
            "mainVmax": self.horizontalSliderVisionHSVCalibrationMainVmax.value(),

            "greenBlur": self.horizontalSliderVisionHSVCalibrationGreenBlur.value(),
            "greenErode": self.horizontalSliderVisionHSVCalibrationGreenErode.value(),
            "greenHmin": self.horizontalSliderVisionHSVCalibrationGreenHmin.value(),
            "greenSmin": self.horizontalSliderVisionHSVCalibrationGreenSmin.value(),
            "greenVmin": self.horizontalSliderVisionHSVCalibrationGreenVmin.value(),
            "greenAmin": self.horizontalSliderVisionHSVCalibrationGreenAmin.value(),
            "greenDilate": self.horizontalSliderVisionHSVCalibrationGreenDilate.value(),
            "greenHmax": self.horizontalSliderVisionHSVCalibrationGreenHmax.value(),
            "greenSmax": self.horizontalSliderVisionHSVCalibrationGreenSmax.value(),
            "greenVmax": self.horizontalSliderVisionHSVCalibrationGreenVmax.value(),

            "ballBlur": self.horizontalSliderVisionHSVCalibrationBallBlur.value(),
            "ballErode": self.horizontalSliderVisionHSVCalibrationBallErode.value(),
            "ballHmin": self.horizontalSliderVisionHSVCalibrationBallHmin.value(),
            "ballSmin": self.horizontalSliderVisionHSVCalibrationBallSmin.value(),
            "ballVmin": self.horizontalSliderVisionHSVCalibrationBallVmin.value(),
            "ballAmin": self.horizontalSliderVisionHSVCalibrationBallAmin.value(),
            "ballDilate": self.horizontalSliderVisionHSVCalibrationBallDilate.value(),
            "ballHmax": self.horizontalSliderVisionHSVCalibrationBallHmax.value(),
            "ballSmax": self.horizontalSliderVisionHSVCalibrationBallSmax.value(),
            "ballVmax": self.horizontalSliderVisionHSVCalibrationBallVmax.value(),

            "oppBlur": self.horizontalSliderVisionHSVCalibrationOpponentBlur.value(),
            "oppErode": self.horizontalSliderVisionHSVCalibrationOpponentErode.value(),
            "oppHmin": self.horizontalSliderVisionHSVCalibrationOpponentHmin.value(),
            "oppSmin": self.horizontalSliderVisionHSVCalibrationOpponentSmin.value(),
            "oppVmin": self.horizontalSliderVisionHSVCalibrationOpponentVmin.value(),
            "oppAmin": self.horizontalSliderVisionHSVCalibrationOpponentAmin.value(),
            "oppDilate": self.horizontalSliderVisionHSVCalibrationOpponentDilate.value(),
            "oppHmax": self.horizontalSliderVisionHSVCalibrationOpponentHmax.value(),
            "oppSmax": self.horizontalSliderVisionHSVCalibrationOpponentSmax.value(),
            "oppVmax": self.horizontalSliderVisionHSVCalibrationOpponentVmax.value()
        }

        self.hades.eventSaveConfigs(value)

    def actionExitTriggered(self):
        self.saveConfigs(file="quicksave")
        if self.recordFlag == True:
            self.record() # end video writing

        return self.close()

    # MenuBarHelp
    '''
    def actionRulesVSSSTriggered(self):
        pass

    def actionAboutTriggered(self):
        pass
    '''

    # CAPTURE TAB

    # DeviceInformation
    def getPushButtonCaptureDeviceInformationStart(self):
        cameraId = self.comboBoxCaptureDeviceInformation.currentText()
        enable = self.hades.eventStartVision(cameraId)

        self.groupBoxCaptureDeviceInformation.setEnabled(not enable)
        self.groupBoxCaptureDeviceProperties.setEnabled(enable)
        self.groupBoxCaptureWarp.setEnabled(enable)
        self.checkBoxPlayDisableDrawing.setEnabled(enable)

        if enable:
            self.labelCameraState.setText("<font color='green'>Online</font>")
            if "Online" in self.labelCommunicationState.text():
                self.pushButtonPlayStart.setEnabled(True)
                self.groupBoxStrategyFormation.setEnabled(True)
        else:
            self.labelCameraState.setText("Error")

    def updateComboBoxCaptureDeviceInformation(self):
        # if sys.platform.startswith('win'):
        cams = []
        try:
            for i in range(0, 2):
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
    # TODO pegar e setar esses valores corretamente
    def camConfigsChanged(self):
        # self.comboBoxCaptureDevicePropertiesFrameSize.currentText()
        self.hades.eventCamConfigs(
            self.spinBoxCaptureDevicePropertiesBrightness.value(),
            self.spinBoxCaptureDevicePropertiesSaturation.value(),
            self.spinBoxCaptureDevicePropertiesGain.value(),
            self.spinBoxCaptureDevicePropertiesContrast.value(),
            self.spinBoxCaptureDevicePropertiesExposure.value(),
            self.spinBoxCaptureDevicePropertiesWhiteBalance.value()
        )

    def initCamConfigs(self):
        newBrightness, newSaturation, newGain, newContrast, \
        newExposure, newWhiteBalance = self.hades.getCameraConfigs()

        self.hades.eventCamConfigs(
            self.spinBoxCaptureDevicePropertiesBrightness.value(newBrightness),
            self.spinBoxCaptureDevicePropertiesSaturation.value(newSaturation),
            self.spinBoxCaptureDevicePropertiesGain.value(newGain),
            self.spinBoxCaptureDevicePropertiesContrast.value(newContrast),
            self.spinBoxCaptureDevicePropertiesExposure.value(newExposure),
            self.spinBoxCaptureDevicePropertiesWhiteBalance.value(newWhiteBalance)
        )

    # Warp
    def toggleInvertImage(self):
        self.checkBoxInvertImage.setChecked(self.hades.eventInvertImage(self.checkBoxInvertImage.isChecked()))

    def getPushButtonCaptureWarpWarp(self):
        pass

    def getPushButtonCaptureWarpReset(self):
        pass

    def getPushButtonCaptureWarpAdjust(self):
        pass

    def getCaptureWarpOffsetLeft(self):
        pass

    def getCaptureWarpOffsetRight(self):
        pass

    # ROBOT TAB

    # role
    def clickEditRoles(self):
        self.pushButtonStrategyRobotFunctionsEdit.setEnabled(False)
        self.pushButtonStrategyRobotFunctionsDone.setEnabled(True)
        self.comboBoxStrategyRobotFunctionsRobot1.setEnabled(True)
        self.comboBoxStrategyRobotFunctionsRobot2.setEnabled(True)
        self.comboBoxStrategyRobotFunctionsRobot3.setEnabled(True)

    def clickDoneRoles(self):
        self.pushButtonStrategyRobotFunctionsEdit.setEnabled(True)
        self.pushButtonStrategyRobotFunctionsDone.setEnabled(False)
        self.comboBoxStrategyRobotFunctionsRobot1.setEnabled(False)
        self.comboBoxStrategyRobotFunctionsRobot2.setEnabled(False)
        self.comboBoxStrategyRobotFunctionsRobot3.setEnabled(False)

        self.hades.eventSelectRoles([self.comboBoxStrategyRobotFunctionsRobot1.currentText(),
                                     self.comboBoxStrategyRobotFunctionsRobot2.currentText(),
                                     self.comboBoxStrategyRobotFunctionsRobot3.currentText()])

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

        robotLetter = [
            self.lineEditRobotIDRobot1.text().upper(),
            self.lineEditRobotIDRobot2.text().upper(),
            self.lineEditRobotIDRobot3.text().upper()
        ]

        changedLetters = self.hades.changeRobotLetters(robotLetter)
        if changedLetters is not None:
            self.lineEditRobotIDRobot1.setText(changedLetters[0])
            self.lineEditRobotIDRobot2.setText(changedLetters[1])
            self.lineEditRobotIDRobot3.setText(changedLetters[2])


    # VISION TAB

    # Capture
    def getVisionVideoCapturePictureName(self):
        return self.lineEditVisionVideoCapturePictureName.text()

    def getVisionVideoCaptureVideoName(self):
        return self.lineEditVisionVideoCaptureVideoName.text()

    # ModeView
    def getVisionModeViewSelectMode(self):
        if self.radioButtonVisionModeViewOriginal.isChecked():
            return "Original"
        else:
            return "Split"

    # HSVCalibration
    def callHadesCalibEvent(self, current):
        if current == 0:
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

        elif current == 1:
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

        elif current == 2:
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

        else:  # current = 3
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

        self.hades.eventCalibration(current, ((Hmin, Hmax), (Smin, Smax), (Vmin, Vmax), Erode, Blur, Dilate, Amin))

    def getPushButtonVisionHSVCalibrationSwap(self):
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

        self.spinBoxVisionHSVCalibrationOpponentHmin.setValue(self.spinBoxVisionHSVCalibrationMainHmin.value())
        self.spinBoxVisionHSVCalibrationOpponentSmin.setValue(self.spinBoxVisionHSVCalibrationMainSmin.value())
        self.spinBoxVisionHSVCalibrationOpponentVmin.setValue(self.spinBoxVisionHSVCalibrationMainVmin.value())
        self.spinBoxVisionHSVCalibrationOpponentErode.setValue(self.spinBoxVisionHSVCalibrationMainErode.value())
        self.spinBoxVisionHSVCalibrationOpponentBlur.setValue(self.spinBoxVisionHSVCalibrationMainBlur.value())
        self.spinBoxVisionHSVCalibrationOpponentHmax.setValue(self.spinBoxVisionHSVCalibrationMainHmax.value())
        self.spinBoxVisionHSVCalibrationOpponentSmax.setValue(self.spinBoxVisionHSVCalibrationMainSmax.value())
        self.spinBoxVisionHSVCalibrationOpponentVmax.setValue(self.spinBoxVisionHSVCalibrationMainVmax.value())
        self.spinBoxVisionHSVCalibrationOpponentDilate.setValue(self.spinBoxVisionHSVCalibrationMainDilate.value())
        self.spinBoxVisionHSVCalibrationOpponentAmin.setValue(self.spinBoxVisionHSVCalibrationMainAmin.value())

        self.horizontalSliderVisionHSVCalibrationMainBlur.setValue(Blur)
        self.horizontalSliderVisionHSVCalibrationMainErode.setValue(Erode)
        self.horizontalSliderVisionHSVCalibrationMainHmin.setValue(Hmin)
        self.horizontalSliderVisionHSVCalibrationMainSmin.setValue(Smin)
        self.horizontalSliderVisionHSVCalibrationMainVmin.setValue(Vmin)
        self.horizontalSliderVisionHSVCalibrationMainAmin.setValue(Amin)
        self.horizontalSliderVisionHSVCalibrationMainDilate.setValue(Dilate)
        self.horizontalSliderVisionHSVCalibrationMainHmax.setValue(Hmax)
        self.horizontalSliderVisionHSVCalibrationMainSmax.setValue(Smax)
        self.horizontalSliderVisionHSVCalibrationMainVmax.setValue(Vmax)

        # atualiza os valores do apolo para o main e oponente
        print("HSV Swapped Main<->Opponent")
        self.callHadesCalibEvent(0)
        self.callHadesCalibEvent(3)

    def getPushButtonVisionHSVCalibrationEdit(self):
        enable = not self.stackedWidgetVisionHSVCalibration.isEnabled()

        self.pushButtonVisionHSVCalibrationEdit.setText("Done" if enable else "Edit")
        self.stackedWidgetVisionHSVCalibration.setEnabled(enable)
        self.pushButtonVisionHSVCalibrationPrev.setEnabled(enable)
        self.pushButtonVisionHSVCalibrationNext.setEnabled(enable)

        self.callHadesCalibEvent(self.stackedWidgetVisionHSVCalibration.currentIndex())

    def getPushButtonVisionHSVCalibrationNext(self):
        current = self.stackedWidgetVisionHSVCalibration.currentIndex()
        self.stackedWidgetVisionHSVCalibration.setCurrentIndex((current + 1) % 4)

        self.callHadesCalibEvent(current)

    def getPushButtonVisionHSVCalibrationPrev(self):
        current = self.stackedWidgetVisionHSVCalibration.currentIndex()
        if current > 0:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(current - 1)
        else:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(3)

            self.callHadesCalibEvent(current)

    def visionHSVCalibrationSliderChanged(self):
        self.callHadesCalibEvent(self.stackedWidgetVisionHSVCalibration.currentIndex())

    # CONTROL TAB

    # PIDTest
    def getPushButtonControlRobotFunctionsPIDTest(self):
        if self.pushButtonComunicationRobotFunctionsPIDTest.palette().button().color().name() == '#efefef':
            self.pushButtonComunicationRobotFunctionsPIDTest.setStyleSheet('background-color:#ff0000')
            self.hades.enablePIDTest()

        elif self.pushButtonComunicationRobotFunctionsPIDTest.palette().button().color().name() == '#ff0000':
            self.pushButtonComunicationRobotFunctionsPIDTest.setStyleSheet('background-color:#efefef')
            self.hades.disablePIDTest()

    def sendWheelVelocities(self):
        # TODO robotId = getControlSerialRobots()
        robotId = None
        leftWheel = self.controlSerialSpeedLeft.currentText()
        rightWheel = self.controlSerialSpeedRight.currentText()
        self.hades.eventCreateAndSendMessage(robotId, leftWheel, rightWheel)

    def sendCommand(self):
        message = self.controlSerialSendCommand.currentText()
        self.hades.eventSendMessage(message)

    # Serial
    def getPushButtonControlSerialDeviceStart(self):
        device = self.getComboBoxControlSerialDevice()
        enable = self.hades.eventStartXbee(device)

        self.groupComunicationSerialDevice.setEnabled(not enable)
        self.groupComunicationSerial.setEnabled(enable)
        self.pushButtonPlayRobotStatusRobotUpdate.setEnabled(enable)

        if enable:
            self.labelCommunicationState.setText("<font color='green'>Online</font>")
            if "Online" in self.labelCameraState.text():
                self.pushButtonPlayStart.setEnabled(True)
                self.groupBoxStrategyFormation.setEnabled(True)
        else:
            self.labelCommunicationState.setText("Error")

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
        message = self.lineEditControlSerialSend.text()
        if robotId is not None and message != "":
            self.hades.eventSendMessage(robotId, message)

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

    # STRATEGY TAB

    # transitions
    def toggleTransitions(self):
        self.hades.eventToggleTransitions(self.checkBoxStrategyTransitionsEnableTransistions.isTristate())

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
