# -*- coding: utf-8 -*-
import cv2
import numpy as np
import random
import math

# Constantes
WIDTH = 640
HEIGHT = 480
MAIN = 0
GREEN = 1
BALL = 2
ADV = 3


class Apolo:
    """
    O threshold quando for setado deve estar no formato ((Hmin,HMax),(Smin,SMax),(Vmin,VMax))
    Criar função pra retonar a imagem com threshold para fazer a calibração
    """

    def __init__(self, cameraId=0):
        self.camera = cv2.VideoCapture(cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.threshList = [None] * 4
        self.thresholdedImages = [None] * 4
        self.robotRadius = 0

        self.robotPositions = [(0, 0, 0, True), (0, 0, 0, True), (0, 0, 0, True)]
        self.ballPosition = [0, 0]
        self.advRobotPositions = [(0, 0), (0, 0), (0, 0)]
    
        # Por default seta esses valores, deve ser modificado quando der o quickSave
        self.setHSVThresh(((28, 30), (0, 255), (0, 255), 0, 0, 0, 30), MAIN)
        self.setHSVThresh(((120, 250), (0, 250), (0, 250), 0, 0, 0, 30), BALL)
        self.setHSVThresh(((120, 250), (0, 250), (0, 250), 0, 0, 0, 30), ADV)
        self.setHSVThresh(((69, 70), (0, 255), (0, 255), 0, 0, 0, 30), GREEN)

        self.resetWarp()

        self.imageId = -1
        self.invertImage = False
        self.robotLetter = ['A', 'B', 'C']
        self.warpMatrizGoal = [(0,0),(WIDTH,0),(WIDTH,HEIGHT),(0,HEIGHT)]

        self.positions = self.returnData(
            self.robotPositions,
            self.advRobotPositions,
            self.ballPosition,
            self.robotLetter
        )

        print("Apolo summoned")

    def setRobotRadius(self, radius):
        self.robotRadius = radius

    def setWarpOffset(self, offLeft, offRight):
        newShape = np.float32([(self.shape[0][0] - offLeft, self.shape[0][1]),
                               (self.shape[1][0] + offRight, self.shape[1][1]),
                               (self.shape[2][0] - offLeft, self.shape[2][1]),
                               (self.shape[3][0] + offRight, self.shape[3][1])])

        plot = np.float32([[0,0],[WIDTH,0],[0,HEIGHT],[WIDTH,HEIGHT]])
        self.perspective = cv2.getPerspectiveTransform(newShape,plot)

    def resetWarp(self):
        self.setWarpPoints((0,0),(WIDTH,0),(WIDTH,HEIGHT),(0,HEIGHT))
        self.warpMatrizGoal = [(0,0),(WIDTH,0),(WIDTH,HEIGHT),(0,HEIGHT)]

    @staticmethod
    def ordenaWarp(points):
        largura = WIDTH/2
        altura = HEIGHT/2

        for i in range(0, 4, 1):
            if points[i][0] - largura < 0:
                if points[i][1] - altura < 0:
                    # Quadrante 1
                    pt1 = points[i]
                else:
                    # Quadrante 4
                    pt4 = points[i]
            else:
                if points[i][1] - altura < 0:
                    # Quadrante 2
                    pt2 = points[i]
                else:
                    # Quadrante 3
                    pt3 = points[i]

        return pt1, pt2, pt3, pt4

    def setWarpPoints(self,pt1, pt2, pt3, pt4):
        try:
            pt1, pt2, pt3, pt4 = self.ordenaWarp([pt1, pt2, pt3, pt4])

            self.shape = np.float32([pt1,pt2,pt4,pt3])
            plot = np.float32([[0,0],[WIDTH,0],[0,HEIGHT],[WIDTH,HEIGHT]])
            self.perspective = cv2.getPerspectiveTransform(self.shape,plot)
        except:
            pass
            
    def setWarpGoalMatriz(self, warpMatrix):
        self.warpMatrizGoal = warpMatrix

    def warpGoalFrame(self, frame):
        try:
            pt1, pt2, pt3, pt4 = self.ordenaWarp(self.warpMatrizGoal)
            cv2.rectangle(frame, (0,0), (pt1[0],pt1[1]), (0, 0, 0), -1)
            cv2.rectangle(frame, (pt2[0], 0), (WIDTH, pt2[1]), (0, 0, 0), -1)
            cv2.rectangle(frame, (pt3[0], pt3[1]), (WIDTH, HEIGHT), (0, 0, 0), -1)
            cv2.rectangle(frame, (0, pt4[1]), (pt4[0], HEIGHT), (0, 0, 0), -1)

            return frame
        except:
            pass

    def changeCamera(self, cameraId):
        self.camera.release()
        self.camera = cv2.VideoCapture(cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def closeCamera(self):
        self.camera.release()

    def getCamConfigs(self):
        return self.camera.get(cv2.CAP_PROP_BRIGHTNESS), \
               self.camera.get(cv2.CAP_PROP_SATURATION), \
               self.camera.get(cv2.CAP_PROP_GAIN), \
               self.camera.get(cv2.CAP_PROP_CONTRAST), \
               self.camera.get(cv2.CAP_PROP_HUE), \
               self.camera.get(cv2.CAP_PROP_EXPOSURE), \
               self.camera.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U)

    def updateCamConfigs(self, newBrightness, newSaturation, newGain, newContrast,
                         newExposure, newWhiteBalance):
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, newBrightness)
        self.camera.set(cv2.CAP_PROP_SATURATION, newSaturation)
        self.camera.set(cv2.CAP_PROP_GAIN, newGain)
        self.camera.set(cv2.CAP_PROP_CONTRAST, newContrast)
        self.camera.set(cv2.CAP_PROP_EXPOSURE, newExposure)
        self.camera.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, newWhiteBalance)
        # adicionar cv2.CAP_PROP_APERTURE, cv2.CAP_PROP_AUTO_EXPOSURE, cv2.CAP_PROP_BACKLIGHT, cv2.CAP_PROP_AUTOFOCUS,
        # cv2.CAP_PROP_GAMMA

    def setInvertImage(self, state):
        self.invertImage = state
        return state

    def getFrame(self):
        frame = None
        if self.camera.isOpened():
            _, frame = self.camera.read()
            if self.invertImage:
                cv2.flip(frame, -1, frame)

        return frame

    @staticmethod
    def getHSVFrame(rawFrame):
        frameHSV = cv2.cvtColor(rawFrame, cv2.COLOR_BGR2HSV)
        return frameHSV

    def setHSVThresh(self, hsvThresh, imageId):
        """
        Args:
            hsvThresh: deve ser do tipo (hmin,hmax),(smin,smax),(vmin,vmax)
            imageId:
                0 - MAIN
                1 - Green
                2 - Ball
                3 - Adv
        """
        self.imageId = imageId

        if self.imageId >= 0:
            self.threshList[imageId] = hsvThresh

    def applyThreshold(self, src, keyword):
        thresh = self.threshList[keyword]

        threshMin = (thresh[0][0], thresh[1][0], thresh[2][0])
        threshMax = (thresh[0][1], thresh[1][1], thresh[2][1])

        maskHSV = cv2.inRange(src, threshMin, threshMax)

        return maskHSV


    def findRobots(self, thresholdedImage):
        """
        Econtra os robos em uma imagem onde o threshold foi aplicado
        Se a posiçao for -1, nao encontrou o robo
        Args:
            thresholdedImage:
            areaMin:

        Returns:

        """
        robotPositionList = list()

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)

            if M['m00'] > self.threshList[MAIN][6]:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                robotPositionList.extend([(cx, cy, 0, False)])

            if len(robotPositionList) == 3:
                break

        if len(robotPositionList) < 3:

            while len(robotPositionList) < 3:
                robotPositionList.extend([(-1, -1, -1, False)])

        return robotPositionList

    def findSecondaryTags(self, thresholdedImage):
        secondaryTags = list()

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)

            if M['m00'] > self.threshList[GREEN][6]:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                secondaryTags.extend([(cx, cy)])

        return secondaryTags

    def findBall(self, imagem):
        """
        Econtra a bola em uma imagem onde o threshold foi aplicado
        Args:
            imagem:
            areaMin:

        Returns:

        """
        _, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        okFlag = False
        cx = cy = 0

        for i in contours:
            M = cv2.moments(i)
            if M['m00'] > self.threshList[BALL][6]:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                okFlag = True
                break

        if okFlag:
            return cx, cy
        else:
            return None

    def findAdvRobots(self, thresholdedImage):
        """
        Econtra os robos adversarios em uma imagem onde o threshold foi aplicado
        Args:
            thresholdedImage:
            areaMin:

        Returns:

        """
        advRobotsPositionList = []

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)

            if M['m00'] > self.threshList[ADV][6]:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                advRobotsPositionList.extend([(cx, cy)])

            if len(advRobotsPositionList) == 3:
                break

        while len(advRobotsPositionList) < 3:
            advRobotsPositionList.extend([(-1, -1)])

        return advRobotsPositionList

    def inSphere(self, robotPosition, secondaryTagPosition):
        if abs(robotPosition[0] - secondaryTagPosition[0]) + abs(
                robotPosition[1] - secondaryTagPosition[1]) <= self.robotRadius:
            return True
        else:
            return False

    def linkTags(self, robotList, secondaryTagsList):
        """
        Linka as tags secundarias às suas respectivas tags Principais
        Args:
            robotList:
            secondaryTagsList:
            robotRadius:
        Returns:

        """
        secondaryTags = [None] * 3
        linkedSecondaryTags = [None] * 3
        robotID = 0

        for i in robotList:
            if i != (-1, -1, -1):
                auxTagList = list()

                for j in secondaryTagsList:
                    if self.inSphere(i, j):
                        auxTagList.extend(j)
                secondaryTags[robotID] = auxTagList

            robotID += 1

        for i in range(0, 3, 1):
            if len(secondaryTags[i]) == 2:
                linkedSecondaryTags[0] = [robotList[i], secondaryTags[i]]

            elif len(secondaryTags[i]) == 4:
                linkedSecondaryTags[1] = [robotList[i], secondaryTags[i]]

            elif len(secondaryTags[i]) == 6:
                linkedSecondaryTags[2] = [robotList[i], secondaryTags[i]]

        #print(linkedSecondaryTags)

        return linkedSecondaryTags

    def posProcess(self, frame, id):
        # Blur
        blurWindow = self.threshList[id][4]

        if blurWindow % 2 == 0:
            blurWindow += 1
        frame = cv2.GaussianBlur(frame, (blurWindow, blurWindow), 0)

        # Erode
        if self.threshList[id][3] > 0:
            kernel = np.ones((self.threshList[id][3], self.threshList[id][3]), np.uint8)
            frame = cv2.erode(frame, kernel, iterations=1)

        # Dilate
        if self.threshList[id][5] > 0:
            kernel = np.ones((self.threshList[id][5], self.threshList[id][5]), np.uint8)
            frame = cv2.dilate(frame, kernel, iterations=1)

        return frame


    @staticmethod
    def findRobotOrientation(robotPos, secondaryTagPosition):
        """
        Args:
            robotPos:
            secondaryTagPosition:

        Returns:

        """
        # h² = c1² + c2² -> Teorema Pitágoras

        distance = ((robotPos[0] - secondaryTagPosition[0]) * (robotPos[0] - secondaryTagPosition[0])) + (
                    (robotPos[1] - secondaryTagPosition[1]) * (robotPos[1] - secondaryTagPosition[1]))
        distance = np.sqrt(distance)

        '''
        Calculo da posição relativa:
        xFinal - xInicial , yFinal - yInicial
        
        Como na imagem o Y cresce pra baixo, então é necessário inverter, ficando entao yInicial - yFinal
        
        '''
        orientation = math.atan2(robotPos[1] - secondaryTagPosition[1], -robotPos[0] + secondaryTagPosition[0])

        orientation += 0.9928943898326508

        if orientation > math.pi:
            orientation = -math.pi + (orientation - math.pi)

        return orientation

    @staticmethod
    def findInterestPoint(robotPosition, tag1, tag2):
        # Queremos achar a bola verde mais à esquerda, pra jogar na mesma função que calcula a orientação do robo de 1 bola

        # Como o Y cresce pra baixo, tem q inverter
        secondary1 = [tag1[0] - robotPosition[0], robotPosition[1] - tag1[1]]
        secondary2 = [tag2[0] - robotPosition[0], robotPosition[1] - tag2[1]]

        if secondary1[0] >= 0 and secondary1[1] >= 0:
            # Quadrante 1
            if secondary2[0] < 0 <= secondary2[1]:
                # Quadrante 2
                return tag1
            elif secondary2[0] >= 0 > secondary2[1]:
                # Quadrante 4
                return tag2
        elif secondary1[0] < 0 <= secondary1[1]:
            # Quadrante 2
            if secondary2[0] < 0 and secondary2[1] < 0:
                # Quadrante 3
                return tag1
            elif secondary2[0] >= 0 and secondary2[1] >= 0:
                # Quadrante 1
                return tag2
        elif secondary1[0] < 0 and secondary1[1] < 0:
            # Quadrante 3
            if secondary2[0] >= 0 > secondary2[1]:
                # Quadrante 4
                return tag1
            elif secondary2[0] < 0 <= secondary2[1]:
                # Quadrante 3
                return tag2
        elif secondary1[0] >= 0 > secondary1[1]:
            # Quadrante 4
            if secondary2[0] >= 0 and secondary2[1] >= 0:
                # Quadrante 1
                return tag1
            elif secondary2[0] < 0 and secondary2[1] < 0:  # Arrumar esses menor e <= pra condizer com o esperado
                # Quadrante 1
                return tag2

        # Caso de bosta
        return None

    # Não é necessario implementar, porém, seria uma melhoria
    def findAdvOrientation(self, previousAdvPosition, currentAdvPosition):
        pass

    # Não é necessario implementar, porém, seria uma melhoria
    def findBallOrientation(self, previousBallPosition, currentBallPosition):
        pass

    # Bota outro nome nessa função por favor
    @staticmethod
    def seeThroughMyEyes(nome, imagem):
        cv2.namedWindow(nome, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(nome, imagem)
        cv2.waitKey(0)

    # Pega os dados dos robos, da bola e dos adversarios e coloca no formato que a Athena requer
    @staticmethod
    def returnData(robotList, robotAdvList, ball, robotLetter):
        output = [
            [
                # OurRobots
                {
                    "position": (robotList[0][0], HEIGHT - robotList[0][1]),
                    "orientation": robotList[0][2],
                    "robotLetter": robotLetter[0]
                },
                {
                    "position": (robotList[1][0], HEIGHT - robotList[1][1]),
                    "orientation": robotList[1][2],
                    "robotLetter": robotLetter[1]
                },
                {
                    "position": (robotList[2][0], HEIGHT - robotList[2][1]),
                    "orientation": robotList[2][2],
                    "robotLetter": robotLetter[2]
                }
            ],
            [
                # EnemyRobots
                {
                    "position": (robotAdvList[0][0], HEIGHT - robotAdvList[0][1]),
                },
                {
                    "position": (robotAdvList[1][0], HEIGHT - robotAdvList[1][1]),
                },
                {
                    "position": (robotAdvList[2][0], HEIGHT - robotAdvList[2][1]),
                }
            ],
            # Ball
            {
                "position": (ball[0], HEIGHT - ball[1])
            }
        ]

        return output

    # Função altera a sequencia das letras dos robos
    def changeLetters(self, robotLetter):
        if robotLetter is not None:
            self.robotLetter = robotLetter
        return self.robotLetter

    # Funçao principal da visao
    def run(self):
        """TO DO:
            Identificar qual robo é qual, identificar orientação dos robos
        """

        # Pega o frame
        frame = self.getFrame()

        #frame = cv2.imread("./vision/Tags/newTag.png",cv2.IMREAD_COLOR)
        #frame = cv2.imread("./vision/Tags/Q3.png", cv2.IMREAD_COLOR)

        if frame is None:
            print("Nao há câmeras ou o dispositivo está ocupado")
            return self.positions, None

        frame = cv2.warpPerspective(frame, self.perspective, (640,480))

        #WarpGoal
        frame = self.warpGoalFrame(frame)

        # Transforma de BRG para HSV
        frameHSV = self.getHSVFrame(frame)

        # Aplica todos os thresholds (pode adicionar threads)
        for i in range(0, 4, 1):
            self.thresholdedImages[i] = self.warpGoalFrame(self.posProcess(self.applyThreshold(frameHSV, i), i))

        # Procura os robos
        tempRobotPosition = self.findRobots(self.thresholdedImages[MAIN])

        #print(tempRobotPosition)

        # Procura as tags Secundarias
        secondaryTagsList = self.findSecondaryTags(self.thresholdedImages[GREEN])

        #print(secondaryTagsList)

        # Organiza as tags secundarias para corresponderem à ordem das tags primarias
        linkedSecondaryTags = self.linkTags(tempRobotPosition, secondaryTagsList)

        for i in range(0, 3, 1):
            try:
                if tempRobotPosition[i][0] != -1:
                    if len(linkedSecondaryTags[i][1]) == 2:
                        orientation = self.findRobotOrientation(linkedSecondaryTags[i][0], linkedSecondaryTags[i][1])
                        tempRobotPosition[i] = [linkedSecondaryTags[i][0][0], linkedSecondaryTags[i][0][1], orientation,
                                                True]
                    elif len(linkedSecondaryTags[i][1]) == 4:
                        tag1 = [linkedSecondaryTags[i][1][0], linkedSecondaryTags[i][1][1]]
                        tag2 = [linkedSecondaryTags[i][1][2], linkedSecondaryTags[i][1][3]]

                        interestSecondaryTag = self.findInterestPoint(linkedSecondaryTags[i][0], tag1, tag2)

                        orientation = self.findRobotOrientation(linkedSecondaryTags[i][0], interestSecondaryTag)
                        tempRobotPosition[i] = [linkedSecondaryTags[i][0][0], linkedSecondaryTags[i][0][1], orientation,
                                                True]
                    elif len(linkedSecondaryTags[i][1]) == 6:
                        tag1 = [linkedSecondaryTags[i][1][0], linkedSecondaryTags[i][1][1]]
                        tag2 = [linkedSecondaryTags[i][1][2], linkedSecondaryTags[i][1][3]]
                        tag3 = [linkedSecondaryTags[i][1][4], linkedSecondaryTags[i][1][5]]

                        stepTag1 = self.findInterestPoint(linkedSecondaryTags[i][0], tag1, tag2)

                        if stepTag1 is None:
                            interestSecondaryTag = self.findInterestPoint(linkedSecondaryTags[i][0], tag1, tag3)

                        else:
                            stepTag2 = self.findInterestPoint(linkedSecondaryTags[i][0], stepTag1, tag3)

                            if stepTag2 is None:
                                interestSecondaryTag = stepTag1
                            else:
                                interestSecondaryTag = stepTag2

                        orientation = self.findRobotOrientation(linkedSecondaryTags[i][0], interestSecondaryTag)
                        tempRobotPosition[i] = [linkedSecondaryTags[i][0][0], linkedSecondaryTags[i][0][1], orientation,
                                                True]
            except:
                pass

        # Procura a bola
        tempBallPosition = self.findBall(self.thresholdedImages[BALL])

        # Procura os adversarios
        tempAdvRobots = self.findAdvRobots(self.thresholdedImages[ADV])

        if tempBallPosition is not None:
            self.ballPosition = tempBallPosition

        for i in range(0, 3, 1):
            if tempRobotPosition[i][3]:
                self.robotPositions[i] = tempRobotPosition[i]

            if tempAdvRobots[i][0] != -1:
                self.advRobotPositions[i] = tempAdvRobots[i]

        # Modela os dados para o formato que a Athena recebe e retorna
        self.positions = self.returnData(
            self.robotPositions,
            self.advRobotPositions,
            self.ballPosition,
            self.robotLetter
        )

        if self.imageId != -1:
            frame = self.thresholdedImages[self.imageId]

        #print(self.positions)
        return self.positions, frame
