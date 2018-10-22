# -*- coding: utf-8 -*-
import cv2
import numpy as np
#from vision import camera
#import camera

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
#Criar função pra retonar a imagem com threshold para fazer a calibração
class Apolo:
    def __init__(self, callback, camera):
        self.callback = callback
        self.ciclope = camera

        self.ciclope = camera

        self.threshList = [None] * 4
        self.thresholdedImages = [None] * 4

        self.robotPositions = [(0,0,0,True),(0,0,0,True),(0,0,0,True)]
        self.ballPosition = [0,0]
        self.advRobotPositions = self.robotPositions
        self.positions = self.returnData(self.robotPositions,self.advRobotPositions, self.ballPosition)

        #Por default seta esses valores, deve ser modificado quando der o quickSave
        self.setHSVThresh(((28,30),(0,255),(0,255)), MAIN)
        self.setHSVThresh(((120,250),(0,250),(0,250)), BALL)
        self.setHSVThresh(((120,250),(0,250),(0,250)), ADV)
        self.setHSVThresh(((69,70),(0,255),(0,255)), GREEN)

        self.imageId = -1

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
    ''''Keyword:
        0 - MAIN
        1 - Ball
        2 - Adv
        3 - Green
    '''
    def resetImageId(self):
        self.imageId = -1

    def setHSVThresh(self, hsvThresh, keyword):
        self.imageId = keyword
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

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                robotPositionList.extend([(cx,cy,0,False)])

            if (len(robotPositionList) == 3): break

        if len(robotPositionList) < 3:

            while (len(robotPositionList) < 3):
                robotPositionList.extend([(-1, -1, -1, False)])


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

        okFlag = False

        for i in contours:
            M = cv2.moments(i)
            if (M['m00'] > areaMin):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                okFlag = True
                break

        if okFlag:
            return (cx,cy)
        else:
            return None

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

        robotID = 0

        for i in robotList:
            if (i != (-1,-1,-1)):
                auxTagList = list()
                for j in secondaryTagsList:
                    if (self.inSphere(i,j,robotRadius)):
                        auxTagList.extend(j)

                linkedSecondaryTags[robotID] = auxTagList

            robotID += 1

        return linkedSecondaryTags


    #Refatorar e documentar
    def findRobotOrientation(self, robotPos, secondaryTagPosition):
        # h² = c1² + c2² -> Teorema Pitágoras

        distance = ((robotPos[0] - secondaryTagPosition[0]) * (robotPos[0] - secondaryTagPosition[0])) + ((robotPos[1] - secondaryTagPosition[1]) * (robotPos[1] - secondaryTagPosition[1]))
        distance = np.sqrt(distance)

        '''
        Calculo da posição relativa:
        xFinal - xInicial , yFinal - yInicial
        
        Como na imagem o Y cresce pra baixo, então é necessário inverter, ficando entao yInicial - yFinal
        
        '''

        relativePosition = [(secondaryTagPosition[0] - robotPos[0])/distance, (robotPos[1] - secondaryTagPosition[1])/distance]

        if (abs(relativePosition[0]) == 0):
            #Quando a variação em X é zero, arctg é indefino (divisão por zero). Sendo assim, deve utilizar arcsin
            #Porém, a função arcsin para 90º demora mto (mais de 1,5 segundos), entao já seto o valor de 90º radianos direto
            orientation = 1.5708
        else:
            orientation = np.arctan(relativePosition[1]/relativePosition[0])

        #Corrige a orientação para o seu devido quadrante
        if (relativePosition[0] < 0):
            if (relativePosition[1] >= 0):
                #Quadrante 2
                orientation = np.pi - abs(orientation)
            elif (relativePosition[1] < 0):
                #Quadrante 3
                orientation = np.pi + orientation
        elif (relativePosition[0] >= 0):
            if (relativePosition[1] < 0):
                #Quadrante 4
                orientation = 2 * np.pi - abs(orientation)

        #Nesse ponto, temos a orientação da tag Verde, porém, a orientação do robo fica à 135 graus anti-horario
        #Por isso, devemos subtrair 135º radianos

        orientation = ((orientation - 2.35619) % 6.28319)

        #Nesse ponto, temos a orientação entre 0 - 2pi, porém, o controle precisa dela no intervalo de -pi a pi
        if (orientation > np.pi):
            orientation = -np.pi + (orientation - np.pi)

        return orientation

    #Refatorar e documentar
    def findInterestPoint(self, robotPosition, tag1, tag2):
        #Queremos achar a bola verde mais à esquerda, pra jogar na mesma função que calcula a orientação do robo de 1 bola

        #Como o Y cresce pra baixo, tem q inverter
        secondary1 = [tag1[0] - robotPosition[0], robotPosition[1] - tag1[1]]
        secondary2 = [tag2[0] - robotPosition[0], robotPosition[1] - tag2[1]]

        if (secondary1[0] >= 0 and secondary1[1] >= 0):
            #Quadrante 1
            if(secondary2[0] < 0 and secondary2[1] >= 0):
                #Quadrante 2
                return tag1
            elif (secondary2[0] >= 0 and secondary2[1] < 0):
                #Quadrante 4
                return tag2
        elif (secondary1[0] < 0 and secondary1[1] >= 0):
            #Quadrante 2
            if(secondary2[0] < 0 and secondary2[1] < 0):
                #Quadrante 3
                return tag1
            elif (secondary2[0] >= 0 and secondary2[1] >= 0):
                #Quadrante 1
                return tag2
        elif (secondary1[0] < 0 and secondary1[1] < 0):
            #Quadrante 3
            if(secondary2[0] >= 0 and secondary2[1] < 0):
                #Quadrante 4
                return tag1
            elif (secondary2[0] < 0 and secondary2[1] >= 0):
                #Quadrante 3
                return tag2
        elif (secondary1[0] >= 0 and secondary1[1] < 0):
            #Quadrante 4
            if(secondary2[0] >= 0 and secondary2[1] >= 0):
                #Quadrante 1
                return tag1
            elif (secondary2[0] < 0 and secondary2[1] < 0): #Arrumar esses menor e menor igual pra condizer com o esperado
                #Quadrante 1
                return tag2

        #Caso de bosta
        return None

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
    def returnData(self, robotList, robotAdvList, ball):
        output = [
            [
                #OurRobots
                {
                    "position": (robotList[0][0], robotList[0][1]),
                    "orientation": robotList[0][2]
                },
                {
                    "position": (robotList[1][0], robotList[1][1]),
                    "orientation": robotList[1][2]
                },
                {
                    "position": (robotList[2][0], robotList[2][1]),
                    "orientation": robotList[2][2]
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
        frame = self.getFrame()
        #frame = cv2.imread("./vision/Tags/newTag.png",cv2.IMREAD_COLOR)

        if frame is None:
            print ("Nao há câmeras ou o dispositivo está ocupado")
            return None

        #Transforma de BRG para HSV
        frameHSV = self.getHSVFrame(frame)

        #Aplica todos os thresholds (pode adicionar threads)
        for i in range(0,4,1):
            self.thresholdedImages[i] = self.applyThreshold(frameHSV, i)

        #Procura os robos
        tempRobotPosition = self.findRobots(self.thresholdedImages[MAIN],TAG_AMIN)

        #Procura as tags Secundarias
        secondaryTagsList = self.findSecondaryTags(self.thresholdedImages[GREEN],TAG_AMIN)

        #Organiza as tags secundarias para corresponderem à ordem das tags primarias
        '''
            Exemplo: Fazer exemplo
        
        '''
        linkedSecondaryTags = self.linkTags(tempRobotPosition, secondaryTagsList,ROBOT_RADIUS)

        for i in range(0,3,1):
            try:
                if (tempRobotPosition[i][0] != -1):
                    if (len(linkedSecondaryTags[i]) == 2):
                       orientation = self.findRobotOrientation(tempRobotPosition[i],linkedSecondaryTags[i])
                       tempRobotPosition[i] = [tempRobotPosition[i][0], tempRobotPosition[i][1], orientation, True]
                    elif (len(linkedSecondaryTags[i]) == 4):
                        tag1 = [linkedSecondaryTags[i][0],linkedSecondaryTags[i][1]]
                        tag2 = [linkedSecondaryTags[i][2],linkedSecondaryTags[i][3]]

                        interestSecondaryTag = self.findInterestPoint(tempRobotPosition[i], tag1, tag2)

                        orientation = self.findRobotOrientation(tempRobotPosition[i],interestSecondaryTag)
                        tempRobotPosition[i] = [tempRobotPosition[i][0], tempRobotPosition[i][1], orientation, True]
                    #elif:
                    else:
                        tag1 = [linkedSecondaryTags[i][0],linkedSecondaryTags[i][1]]
                        tag2 = [linkedSecondaryTags[i][2],linkedSecondaryTags[i][3]]
                        tag3 = [linkedSecondaryTags[i][4],linkedSecondaryTags[i][5]]

                        stepTag1 = self.findInterestPoint(tempRobotPosition[i], tag1, tag2)

                        if (stepTag1 is None):
                            interestSecondaryTag = self.findInterestPoint(tempRobotPosition[i], tag1, tag3)
                        else:
                            stepTag2 = self.findInterestPoint(tempRobotPosition[i], stepTag1, tag3)

                            if (stepTag2 is None):
                                interestSecondaryTag = stepTag1
                            else: interestSecondaryTag = stepTag2


                        orientation = self.findRobotOrientation(tempRobotPosition[i],interestSecondaryTag)
                        tempRobotPosition[i] = [tempRobotPosition[i][0], tempRobotPosition[i][1], orientation, True]
            except:
                pass

        #Procura a bola
        tempBallPosition = self.findBall(self.thresholdedImages[BALL],BALL_AMIN)

        #Procura os adversarios
        self.advRobotPositions = self.robotPositions

        if tempBallPosition is not None:
            self.ballPosition = tempBallPosition

        for i in range(0,3,1):
            if tempRobotPosition[i][3]:
                self.robotPositions[i] = tempRobotPosition[i]

        #Modela os dados para o formato que a Athena recebe e retorna

        self.positions = self.returnData(self.robotPositions,self.advRobotPositions,self.ballPosition)

        print (self.positions)

        if (self.imageId != -1):
            frame = self.thresholdedImages[self.imageId]

        self.callback(self.positions,frame)
