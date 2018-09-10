# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
sys.path.append("../")
from vision import Camera

WIDTH = 640
HEIGHT = 480

class Apolo:
	def __init__(self):
		self.camera = Camera.Ciclope()
		
		#Por default seta esses valores, deve ser modificado quando der o quickSave
		self.setHueThresh(120,250)
		self.setSaturationThresh(0,250)
		self.setValueThresh(0,250)
		
	def setHueThresh(self,hMin,hMax):
		self.hThresh = (hMin,hMax)
		
	def setSaturationThresh(self,sMin,sMax):
		self.sThresh = (sMin,sMax)	
		
	def setValueThresh(self,vMin,vMax):
		self.vThresh = (vMin,vMax)
		
	def getThreshValues(self):
		return (self.hThresh,self.sThresh,self.vThresh)
		
		
	#Funçao principal da visao
	def run(self):
		if self.camera.isOpened():
			#Colocar condição de parada
			ret, frame = self.camera.getFrame()
			
			frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
				
			'''
			Assinatura -> applyThreshold(frameHSV, HMin, HMax, SMin, SMax, VMin, VMax)
			Retorno -> imagem binarizada de acordo com os valores de HSV passados
			Pegar os valores de HSV da interface
			'''
			#Adicionar threads para fazerem o threshold da bola, tags principais e tags secundarias
			threshFrame = self.applyThreshold(frameHSV)
			
			'''
			Assinatura -> applyThreshold(thresholdedFrame, areaMinimaDaTag)
			Retorno -> lista com as posições em x e y dos nossos robos  
			Pegar areaMinima da interface
			'''
			
			self.seeThroughMyEyes("Original",frame)
			self.seeThroughMyEyes("Thresh",threshFrame)
			
			#Seta os dados dos robos e da bola
			
			robotList = self.findRobots(threshFrame,30)
			#ball = self.findBall(ballThreshFrame,30)
			robotAdvList = robotList
			
			#Modela os dados para o formato que a Athena recebe e retorna
			return self.returnData(robotList,robotAdvList,(300,300))

		else: 
			print ("Nao há câmeras ou o dispositivo está ocupado")
			return None	
		
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
	
	
	def applyThreshold(self, src):
		threshMin = (self.hThresh[0], self.sThresh[0], self.vThresh[0])
		threshMax = (self.hThresh[1],self.sThresh[1],self.vThresh[1])
		
		maskHSV = cv2.inRange(src,threshMin, threshMax)
				
		return maskHSV
	
	
	def findBall(self, imagem, areaMin):
		_, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		cx = -1
		cy = -1
		
		for i in contours:
			M = cv2.moments(i)
			if (M['m00'] > areaMin):
				cx = int(M['m01']/M['m00'])
				cy = int(M['m10']/M['m00'])
				break
		
		return (cx,cy)
		
	'''
	Econtra os robos em uma imagem onde o threshold foi aplicado
	'''
	
	#Bota outro nome nessa função por favor
	def seeThroughMyEyes(self, nome, imagem):
		cv2.namedWindow(nome, cv2.WINDOW_AUTOSIZE)
		cv2.imshow(nome,imagem)
		cv2.waitKey(1)
	
	#Se a posiçao for -1, nao encontrou o robo
	def findRobots(self, thresholdedImage, areaMin):
		robotPositionList = list()
		
		_, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for i in contours:
			M = cv2.moments(i)
			
			if (M['m00'] > areaMin):
				cx = int(M['m01']/M['m00'])
				cy = int(M['m10']/M['m00'])
				robotPositionList.extend([(cx,cy)])
		
			if (len(robotPositionList) == 3): break
		
		while (len(robotPositionList) < 3):
			robotPositionList.extend([(-1,-1)])
		
		return robotPositionList
		
	def findAdvRobots(self, labelledImage):
		return ("ADV1:",103,103),("ADV2:",203,213),("ADV3:",253,303)
		
	def setRobots(self, secondaryTagsImage):
	
		return ("R1:",103,103),("R2:",203,213),("R3:",253,303)
		
	def findRobotOrientation(self, lastPosition, newPosition):
	
		x = newPosition[0] - lastPosition[0]
		y = (newPosition[1] - lastPosition[1]) * -1
				
		return np.arctan2(x,y) * 180 / np.pi
		
	def findAdvOrientation(self,previousAdvPosition, currentAdvPosition):
		pass
		
	def findBallOrientation(self,previousBallPosition, currentBallPosition):
		pass