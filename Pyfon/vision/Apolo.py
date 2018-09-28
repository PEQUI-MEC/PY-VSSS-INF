# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
import math
sys.path.append("../")
from vision import Camera

#Constantes
WIDTH = 640
HEIGHT = 480
MAIN = 0
BALL = 1
ADV = 2
GREEN = 3

#O threshold quando for setado deve estar no formato ((Hmin,HMax),(Smin,SMax),(Vmin,VMax))
class Apolo:
	def __init__(self):
		self.ciclope = Camera.Ciclope()
		
		self.threshList = [None] * 4
		self.thresholdedImages = [None] * 4
		#Por default seta esses valores, deve ser modificado quando der o quickSave
		self.setHSVThresh(((28,30),(0,255),(0,255)), MAIN)
		self.setHSVThresh(((120,250),(0,250),(0,250)), BALL)
		self.setHSVThresh(((120,250),(0,250),(0,250)), ADV)
		self.setHSVThresh(((69,70),(0,255),(0,255)), GREEN)
		
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
				line = cv2.fitLine(i,2,0,0.01,0.01)
				orientation = self.findRobotOrientation(line)
				print ("ROBOT ORIENTATION: ",orientation)
				
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				robotPositionList.extend([(cx,cy,orientation)])
		
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
		
			if (len(secondaryTags) == 4): break
		
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
		
		
	#TODO: Implementar essa função para definir qual robo é qual
	def setRobots(self, robotList, secondaryTagsList, robotRadius):
		robots = list()
		
		for i in robotList:
			#Reseta a lista de tags secundarias
			tagsSecundarias = list()
			for j in secondaryTagsList:
				#Verifica se uma tag 'j' pertence ao robo 'i'
				if (abs(i[0] - j[0]) + abs(i[1] - j[1]) <= robotRadius):
					#Se pertencer, adiciona ela na lista de tags secundarias
					tagsSecundarias.extend(j)
			
			#Linka o robo com suas tags secundarias
			robots.extend(tagsSecundarias)
		
		return robots
		
		
	#TODO: Encontrar orientação dos robos
	def findRobotOrientation(self, line):
		if (line[1] < 0.0001): radAngle = np.arccos(abs(line[0]))
		else: radAngle = np.arcsin(abs(line[1]))
		
		print (radAngle)
		
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
		frame = cv2.imread("Tags/30Graus.png")
		
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
		robotList = self.findRobots(self.thresholdedImages[MAIN],30)
		
		secondaryTagsList = self.findSecondaryTags(self.thresholdedImages[GREEN],30)
		
		print (robotList)
		print (secondaryTagsList)
		
		self.setRobots(robotList,secondaryTagsList,300)
		
		#Procura a bola
		ball = self.findBall(self.thresholdedImages[BALL],30)
		
		#Procura os adversarios
		robotAdvList = robotList
		
		cv2.imshow("frame",frame)
		cv2.waitKey(0)
		#Modela os dados para o formato que a Athena recebe e retorna
		#return self.returnData(robotList,robotAdvList,(300,300))