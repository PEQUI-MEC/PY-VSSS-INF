import sys
import os
import cv2  # Somente para testes

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget,QFileDialog,QGroupBox
from PyQt5.uic import loadUi

from datetime import datetime
import interface.icons_rc
import serial, glob
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

        # PLAY BUTTON
        self.pushButtonVideoViewStart.clicked.connect(self.clickedPlay)

        # VISION

        # VideoView #
        # CheckBoxVideoViewDisableDrawing
        self.checkBoxVideoViewDisableDrawing.clicked.connect(self.getStateCheckBoxVideoViewDisableDrawing)

        #Capture
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

        # Capture
        ##DeviceInformation
        self.pushButtonCaptureDeviceInformationStart.clicked.connect(self.getPushButtonCaptureDeviceInformationStart)
        self.updateComboBoxCaptureDeviceInformation()
        self.getComboBoxCaptureDeviceInformation()

        ##Warp
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
        self.spinBoxRobotSpeedAttack.setValue(0)
        self.spinBoxRobotSpeedAttack.setMinimum(0)
        self.spinBoxRobotSpeedAttack.setMaximum(140)
        self.horizontalSliderRobotSpeedAttack.setMinimum(0)
        self.horizontalSliderRobotSpeedAttack.setMaximum(140)

        self.spinBoxRobotSpeedDefense.setValue(0)
        self.spinBoxRobotSpeedDefense.setMinimum(0)
        self.spinBoxRobotSpeedDefense.setMaximum(140)
        self.horizontalSliderRobotSpeedDefense.setMinimum(0)
        self.horizontalSliderRobotSpeedDefense.setMaximum(140)

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
        '''
        self.getPushButtonControlSerialDeviceStart.clicked.connect(self.startSerialConnection)
        self.getPushButtonControlSerialSend.clicked.connect(self.sendWheelVelocities)
        self.getPushButtonControlSerialSendCommand.clicked.connect(self.sendCommand)
        
        #serial
        self.updateComboBoxControlSerialDevice()
        
        # Serial
        self.pushButtonControlSerialDeviceStart.clicked.connect(self.getPushButtonControlSerialDeviceStart)
        self.pushButtonControlSerialDeviceRefresh.clicked.connect(self.getPushButtonControlSerialDeviceRefresh)
        self.pushButtonControlSerialSend.clicked.connect(self.getPushButtonControlSerialSend)
        self.pushButtonControlSerialSendCommand.clicked.connect(self.getPushButtonControlSerialSendCommand)
        self.pushButtonControlSerialSetSkippedFrames.clicked.connect(self.getPushButtonControlSerialSetSkippedFrames)
        '''

        # RobotStatus
        self.pushButtonControlRobotStatusRobotUpdate.clicked.connect(self.getPushButtonControlRobotStatusRobotUpdate)

        # id
        self.pushButtonRobotIDEdit.clicked.connect(self.getPushButtonRobotIDEdit)
        self.pushButtonRobotIDDone.clicked.connect(self.getPushButtonRobotIDDone)

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

        return self.spinBoxRobotSpeedAttack.value(), self.spinBoxRobotSpeedDefense.value(), self.spinBoxRobotSpeedGoalkeeper.value()

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
        self.hades.eventUpdateSpeeds(self.spinBoxRobotSpeedAttack.value()/100.0,
                                     self.spinBoxRobotSpeedDefense.value()/100.0,
                                     self.spinBoxRobotSpeedGoalkeeper.value()/100.0)

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
    def updateLabelVideoViewPositionsRobot1(self,x,y,z):
        self.labelVideoViewPositionsRobot1.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

    def updateLabelVideoViewPositionsRobot2(self,x,y,z):
        self.labelVideoViewPositionsRobot2.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

    def updateLabelVideoViewPositionsRobot3(self,x,y,z):
        self.labelVideoViewPositionsRobot3.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

    def updateLabelVideoViewPositionsBall(self,x,y,z):
        self.labelVideoViewPositionsBall.setText("(" + str(x) + "," + str(y) + "," + str(z) + ")")

    # CheckBoxVideoViewDisableDrawing
    def getStateCheckBoxVideoViewDisableDrawing(self):
        return self.checkBoxVideoViewDisableDrawing.isTristate()

    # FPS
    def setLabelVideoViewFPS(self, fps):
        self.labelVideoViewFPS.setText("FPS: " + str(fps))

    #LoadImage

    def updateFrameVideoView(self, image):
        self.image = image

        #Desenhar na tela
        if self.checkBoxVideoViewDisableDrawing.isChecked():
            self.drawingImageVideoView()

        self.displayImageVideoView(1)

        return None

    def displayImageVideoView(self, window=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if self.image.shape[2] == 4:
                qformat=QImage.Format_RGBA888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)

        outImage=outImage.rgbSwapped()

        if window == 1:
            self.graphicsViewVideoViewVideo.setPixmap(QPixmap.fromImage(outImage))
            self.graphicsViewVideoViewVideo.setScaledContents(True)

    def graphicsViewVideoViewVideoClicked(self, event):
        point = QtGui.QCursor.pos()
        print("X:" + str(point.x()) + " | " + "Y:" + str(point.y())) 

    def getBallPosition(self):
        self.cont+=1
        return (447,self.cont)

    '''-----------------------DESENHO SOBRA A IMAGEM------------------'''

    def drawingImageVideoView(self):
        #Desenho da Bola
        cv2.circle(self.image, self.getBallPosition(), 7,  (255,255,255), 2)

        #TEST
        cv2.circle(self.image, self.getBallPosition(), 50,  (67,255,255), 6)
        cv2.rectangle(self.image,(384,50),(510,128),(0,255,0),3)
        ######

        self.nRobots = setAmountRobots() #??????
        self.robots = setRobots() #??????
        self.advRobots = setAdvRobots()
        '''
        #TODO GET POSITIONk
        for i in range(0, nRobots):
            #Orientação do robô
            line(self.image, Robots::get_position(i), Robots::get_secondary_tag(i),cv::Scalar(255,255,0), 2);
            #id do robô
            putText(self.image, std::to_string(i+1),cv::Point(Robots::get_position(i).x-5,Robots::get_position(i).y-17),cv::FONT_HERSHEY_PLAIN,1,cv::Scalar(255,255,0),2);
            #marcação do robô
            circle(self.image, Robots::get_position(i), 15, cv::Scalar(255,255,0), 2);

            // vetor que todos os robos estão executando
            cv::Point aux_point;
            aux_point.x = int(100*cos(Robots::get_transAngle(i)));
            aux_point.y = - int(100*sin(Robots::get_transAngle(i)));
            aux_point += Robots::get_position(i);
            arrowed_line(self.image, Robots::get_position(i), aux_point, cv::Scalar(255, 0, 0), 2);

        for (int i = 0; i < Robots::SIZE; i++)
            

        // adversários
        for(int i = 0; i < advRobots.size(); i++)
            circle(self.image, advRobots.at(i), 15, cv::Scalar(0,0,255), 2);

        // ----------- DESENHOS DA ESTRATÉGIA ---------- //

        if(interface.get_start_game_flag())
            // desenha a estimativa da bola
            circle(cameraFlow, Ball_Est, 7, cv::Scalar(255,140,0), 2);

            // desenha os alvos dos robôs
            for(int i = 0; i < Robots::SIZE; i++)
                circle(cameraFlow, Robots::get_target(i), 7, cv::Scalar(127,255,127), 2);
                putText(cameraFlow, std::to_string(i+1), cv::Point(Robots::get_target(i).x-5, Robots::get_target(i).y-17),cv::FONT_HERSHEY_PLAIN,1,cv::Scalar(127,255,127),2);

        // ----------- DESENHOS DO CONTROLE ---------- //

        if(strategyGUI.formation_flag)
            // exibe os robos virtuais
            for(int i = 0; i < Robots::SIZE; i++)
                if(virtual_robot_selected == i)
                    circle(cameraFlow,virtual_robots_positions[i], 20, cv::Scalar(0,255,100), 3);

                // posição
                circle(cameraFlow,virtual_robots_positions[i], 17, cv::Scalar(0,255,0), 2);
                // orientação
                arrowed_line(cameraFlow, virtual_robots_positions[i], virtual_robots_orientations[i], cv::Scalar(0, 255, 0), 2);
                // identificação
                putText(cameraFlow, std::to_string(i+1),virtual_robots_positions[i] + cv::Point(-14,10),cv::FONT_HERSHEY_PLAIN,1,cv::Scalar(0,255,0),2);


        if (interface.imageView.PID_test_flag)
            for(int i = 0; i < Robots::SIZE; i++)
                if(Robots::is_target_set(i)) {
                    // linha branca no alvo sendo executado
                    line(cameraFlow, Robots::get_position(i), Robots::get_target(i), cv::Scalar(255,255,255),2);

                // círculo branco no alvo sendo executado
                circle(cameraFlow,Robots::get_target(i), 9, cv::Scalar(255,255,255), 2);

            if(Selec_index != -1)
                circle(cameraFlow, Robots::get_position(Selec_index), 17, cv::Scalar(255,255,255), 2);

    '''
    #########################################################

    # Capture
    # DeviceInformation
    def getPushButtonCaptureDeviceInformationStart(self):
        print("Botton: DeviceInformationStart : Clicked")
        cameraId = self.getComboBoxCaptureDeviceInformation()
        #TODO: trocar a camera de acordo com o que for selecionado

        self.hades.eventStartVision()

    def updateComboBoxCaptureDeviceInformation(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/video[0-9]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/*')
        else:
            raise EnvironmentError('Unsuported plaftorm')

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
            self.hades.setHSVVision(0)
            getHSVcalibThread = threading.Thread(target=self.getHSVCalibration)
            getHSVcalibThread.start()

    def getPushButtonVisionHSVCalibrationNext(self):
        if self.stackedWidgetVisionHSVCalibration.currentIndex() < 3:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(self.stackedWidgetVisionHSVCalibration.currentIndex() + 1)

    def getPushButtonVisionHSVCalibrationPrev(self):
        if self.stackedWidgetVisionHSVCalibration.currentIndex() > 0:
            self.stackedWidgetVisionHSVCalibration.setCurrentIndex(self.stackedWidgetVisionHSVCalibration.currentIndex() - 1)

    def getHSVCalibration(self):
        while self.stackedWidgetVisionHSVCalibration.isEnabled():
            print("TA INO")
        self.hades.setHSVVision(10)

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

        print(((Hmin, Hmax), (Smin, Smax),(Vmin, Vmax)), Erode, Blur, Dilate, Amin)

    # Ball
    def getVisionHSVCalibrationBall(self):
        Hmin = self.spinBoxVisionHSVCalibrationBallHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationBallnSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationBallVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationBallErode.value()
        Blur = self.spinBoxVisionHSVCalibrationBallBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationBallHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationBallSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationBallVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationBallDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationBallAmin.value()

        return ((Hmin, Hmax), (Smin, Smax),(Vmin, Vmax)), Erode, Blur, Dilate, Amin

    # Opponent
    def getVisionHSVCalibrationOpponent(self):
        Hmin = self.spinBoxVisionHSVCalibrationOpponentHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationOpponentnSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationOpponentVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationOpponentErode.value()
        Blur = self.spinBoxVisionHSVCalibrationOpponentBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationOpponentHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationOpponentSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationOpponentVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationOpponentDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationOpponentAmin.value()

        return ((Hmin, Hmax), (Smin, Smax),(Vmin, Vmax)), Erode, Blur, Dilate, Amin

    # Green
    def getVisionHSVCalibrationGreen(self):
        Hmin = self.spinBoxVisionHSVCalibrationGreenHmin.value()
        Smin = self.spinBoxVisionHSVCalibrationGreennSmin.value()
        Vmin = self.spinBoxVisionHSVCalibrationGreenVmin.value()
        Erode = self.spinBoxVisionHSVCalibrationGreenErode.value()
        Blur = self.spinBoxVisionHSVCalibrationGreenBlur.value()
        Hmax = self.spinBoxVisionHSVCalibrationGreenHmax.value()
        Smax = self.spinBoxVisionHSVCalibrationGreenSmax.value()
        Vmax = self.spinBoxVisionHSVCalibrationGreenVmax.value()
        Dilate = self.spinBoxVisionHSVCalibrationGreenDilate.value()
        Amin = self.spinBoxVisionHSVCalibrationGreenAmin.value()

        return ((Hmin, Hmax), (Smin, Smax),(Vmin, Vmax)), Erode, Blur, Dilate, Amin

    # Control
    # Serial
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

    def getPushButtonControlSerialDeviceStart(self):
        device = self.comboBoxControlSerialDevice.currentText()

    def getPushButtonControlSerialDeviceRefresh(self):
        self.updateComboBoxControlSerialDevice()

    def getPushButtonControlSerialSend(self):
        pass

    def getPushButtonControlSerialSendCommand(self):
        pass

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
        self.labelControlRobotStatusLastUpdate.setText("Last Update: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))

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
        return self.getStrategyTestParametersGoalieLine(), self.getStrategyTestParametersGoalieOffset(), self.getStrategyTestParametersName3(), self.getStrategyTestParametersName4(), self.getStrategyTestParametersName5()

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
