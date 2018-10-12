# -*- coding: utf-8 -*-
import cv2
import numpy as np
from vision import camera

#Constantes
WIDTH = 640
HEIGHT = 480
MAIN = 0
BALL = 1
ADV = 2
GREEN = 3
ROBOT_RADIUS = 250
TAG_AMIN = 400
BALL_AMIN = 30

#O threshold quando for setado deve estar no formato ((Hmin,HMax),(Smin,SMax),(Vmin,VMax))
class Apolo:
    def __init__(self, callback):
        self.ciclope = camera.Ciclope()

        self.threshList = [None] * 4
        self.thresholdedImages = [None] * 4
        #Por default seta esses valores, deve ser modificado quando der o quickSave
        self.setHSVThresh(((28,30),(0,255),(0,255)), MAIN)
        self.setHSVThresh(((120,250),(0,250),(0,250)), BALL)
        self.setHSVThresh(((120,250),(0,250),(0,250)), ADV)
        self.setHSVThresh(((69,70),(0,255),(0,255)), GREEN)

        print("Apolo summoned")

    def getFrame(self):
        frame = None
        if (self.ciclope.isCameraOpened()):
            _, frame = self.ciclope.getFrame()

        return frame

    def getHSVFrame(self, rawFrame):
        frameHSV = cv2.cvtColor(rawFrame, cv2.COLOR_BGR2HSV);
        return frameHSV

    #hsvThresh deve ser do tipo (hmin,hmax),(smin,smax),(vmin,vmax)
    '''Keyword:
            0 - MAIN
            1 - Ball
            2 - Adv
            3 - Green
    '''

    def setHSVThresh(self, hsvThresh, keyword):
        self.threshList[keyword] = hsvThresh

    def getHSVThresh(self,keyword):
        return self.threshList[keyword]

    def applyThreshold(self,src,keyword):
        thresh = self.getHSVThresh(keyword)

        threshMin = (thresh[0][0], thresh[1][0], thresh[2][0])
        threshMax = (thresh[0][1],thresh[1][1],thresh[2][1])

        maskHSV = cv2.inRange(src,threshMin, threshMax)

        return maskHSV

    #Econtra os robos em uma imagem onde o threshold foi aplicado
    #Se a posiçao for -1, nao encontrou o robo
    def findRobots(self, thresholdedImage, areaMin):
        robotPositionList = list()

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)
            if (M['m00'] > areaMin):
                #Encontra o robo e a sua orientação utilizando o fitLine
                #line = cv2.fitLine(i,2,0,0.01,0.01)
                #orientation = self.findRobotOrientation(line)
                #print ("ROBOT ORIENTATION: ",orientation)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                robotPositionList.extend([(cx,cy)])

            if (len(robotPositionList) == 3): break

        while (len(robotPositionList) < 3):
            robotPositionList.extend([(-1,-1,-1)])

        return robotPositionList

    def findSecondaryTags(self, thresholdedImage, areaMin):
        secondaryTags = list()

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)

            if (M['m00'] > areaMin):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                secondaryTags.extend([(cx,cy)])

            if (len(secondaryTags) == 6): break

        return secondaryTags


    #Econtra a bola em uma imagem onde o threshold foi aplicado
    def findBall(self, imagem, areaMin):
        _, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cx = -1
        cy = -1

        for i in contours:
            M = cv2.moments(i)
            if (M['m00'] > areaMin):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                break

        return (cx,cy)

    #Econtra os robos adversarios em uma imagem onde o threshold foi aplicado
    def findAdvRobots(self, thresholdedImage, areaMin):
        advRobotsPositionList = list()

        _, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
            M = cv2.moments(i)

            if (M['m00'] > areaMin):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                advRobotPositionList.extend([(cx,cy)])

            if (len(advRobotPositionList) == 3): break

        while (len(advRobotPositionList) < 3):
            advRobotPositionList.extend([(-1,-1)])

        return advRobotPositionList

    def inSphere(self,robotPosition,secondaryTagPosition,robotRadius):
        if (abs(robotPosition[0] - secondaryTagPosition[0]) + abs(robotPosition[1] - secondaryTagPosition[1]) <= robotRadius):
            return True
        else: return False

    #Linka as tags secundarias às suas respectivas tags Principais
    def linkTags(self, robotList, secondaryTagsList, robotRadius):
        linkedSecondaryTags = [None] * 3
        linkedMainTags = [None] * 3

        robotID = 0

        for i in robotList:
            auxTagList = list()
            for j in secondaryTagsList:
                if (self.inSphere(i,j,robotRadius)):
                    auxTagList.extend(j)


            linkedSecondaryTags[robotID] = auxTagList

            robotID += 1

        #Coloca o robo 1 na posição 1, o robo 2 na posição 2 e o robo 3 na posição 3
        for i in range(0,3,1):
            menor = i
            for j in range(i+1,3,1):
                if (len(linkedSecondaryTags[i]) > len(linkedSecondaryTags[j])):
                    menor = j

            tempSecondary = linkedSecondaryTags[i]
            linkedSecondaryTags[i] = linkedSecondaryTags[menor]
            linkedSecondaryTags[menor] = tempSecondary

            tempMain = robotList[i]
            robotList[i] = robotList[menor]
            robotList[menor] = tempMain

        return robotList, linkedSecondaryTags

    #TODO: Encontrar orientação dos robos
    def findRobotOrientation(self, line):
        if (line[1] < 0.0001): radAngle = np.arccos(abs(line[0]))
        else: radAngle = np.arcsin(abs(line[1]))

        return radAngle

    #Não é necessario implementar, porém, seria uma melhoria
    def findAdvOrientation(self,previousAdvPosition, currentAdvPosition):
        pass

    #Não é necessario implementar, porém, seria uma melhoria
    def findBallOrientation(self,previousBallPosition, currentBallPosition):
        pass

    #Bota outro nome nessa função por favor
    def seeThroughMyEyes(self, nome, imagem):
        cv2.namedWindow(nome, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(nome,imagem)
        cv2.waitKey(0)

    #Pega os dados dos robos, da bola e dos adversarios e coloca no formato que a Athena requer
    def returnData(self, robotList, robotAdvList,ball):
        output = [
            [
                #OurRobots
                {
                    "position": (robotList[0][0], robotList[0][1]),
                    "orientation": 0.5
                },
                {
                    "position": (robotList[1][0], robotList[1][1]),
                    "orientation": 0.5
                },
                {
                    "position": (robotList[2][0], robotList[2][1]),
                    "orientation": 0.5
                }
            ],
            [
                #EnemyRobots
                {
                    "position": (robotAdvList[0][0], robotAdvList[0][1]),
                },
                {
                    "position": (robotAdvList[1][0], robotAdvList[1][1]),
                },
                {
                    "position": (robotAdvList[2][0], robotAdvList[2][1]),
                }
            ],
            #Ball
            {
                "position": (ball[0], ball[1])
            }
        ]

        return output


    #Funçao principal da visao
    def run(self):
        '''TO DO:
            Identificar qual robo é qual, identificar orientação dos robos
        '''

        #Pega o frame
        #frame = self.getFrame()
        frame = cv2.imread("Tags/newTag.jpeg")

        if frame is None:
            print ("Nao há câmeras ou o dispositivo está ocupado")
            return None

        #Transforma de BRG para HSV
        frameHSV = self.getHSVFrame(frame)

        #Aplica todos os thresholds (pode adicionar threads)
        for i in range(0,4,1):
            self.thresholdedImages[i] = self.applyThreshold(frameHSV, i)

        #Mostra a imagem (nao tem necessidade, so ta ai pra debug)
        self.seeThroughMyEyes("Original",frame)
        self.seeThroughMyEyes("Main",self.thresholdedImages[MAIN])
        self.seeThroughMyEyes("GREEN",self.thresholdedImages[GREEN])

        #Procura os robos
        robotList = self.findRobots(self.thresholdedImages[MAIN],TAG_AMIN)

        #Procura as tags Secundarias
        secondaryTagsList = self.findSecondaryTags(self.thresholdedImages[GREEN],TAG_AMIN)

        #Organiza as tags secundarias para corresponderem à ordem das tags primarias
        '''
            Exemplo: Fazer exemplo
        
        '''

        '''
            Coloca as tags primarias e secundarias do robo 1 na poição 1,
            do robo 2 na posição 2 e do robo 3 na posição 3    
        '''
        robotList, linkedSecondaryTags = self.linkTags(robotList,secondaryTagsList,ROBOT_RADIUS)

        #Procura a bola
        ball = self.findBall(self.thresholdedImages[BALL],BALL_AMIN)

        #Procura os adversarios
        robotAdvList = robotList

        cv2.imshow("frame",frame)
        cv2.waitKey(0)
        #Modela os dados para o formato que a Athena recebe e retorna
        #return self.returnData(robotList,robotAdvList, ball)