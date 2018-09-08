import cv2
import numpy as np
import sys
import Camera

WIDTH = 640
HEIGHT = 480

class Apolo:
	def __init__(self):
		self.camera = Camera.Ciclope()
	
	def run(self):
		if self.camera.isOpened():
			while True: #Colocar condição de parada
				ret, frame = self.camera.getFrame()
				
				frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
					
				'''
				Assinatura -> applyThreshold(frameHSV, HMin, HMax, SMin, SMax, VMin, VMax)
				Retorno -> imagem binarizada de acordo com os valores de HSV passados
				Pegar os valores de HSV da interface
				'''
				
				threshFrame = self.applyThreshold(frameHSV,120,250,0,250,0,250)
				
				'''
				Assinatura -> applyThreshold(thresholdedFrame, areaMinimaDaTag)
				Retorno -> lista com as posições em x e y dos nossos robos  
				Pegar areaMinima da interface
				'''
				
				robotList = self.findRobots(threshFrame,30)
				
				self.seeThroughMyEyes("Original",frame)
				self.seeThroughMyEyes("Thresh",threshFrame)
				
			self.camera.killYourself()
			
			return True
		else: 
			print ("Nao há câmeras ou o dispositivo está ocupado")
			return False	
		
	def applyThreshold(self, src, HMin, HMax, SMin, SMax, VMin, VMax):		
		maskHSV = cv2.inRange(src,(HMin,SMin,VMin),(HMax,SMax,VMax))
				
		return maskHSV
	
	
	def findBall(self, imagem, areaMin):
		_, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for i in contours:
			M = cv2.moments(i)
			if (M['m00'] > areaMin):
				cx = int(M['m01']/M['m00'])
				cy = int(M['m10']/M['m00'])
				break
		
		return cx,cy
		
	'''
	Econtra os robos em uma imagem onde o threshold foi aplicado
	'''
	
	#Bota outro nome nessa função por favor
	def seeThroughMyEyes(self, nome, imagem):
		cv2.namedWindow(nome, cv2.WINDOW_AUTOSIZE)
		cv2.imshow(nome,imagem)
		cv2.waitKey(1)
	
	def findRobots(self, thresholdedImage, areaMin):
		robotPositionList = list()
		
		_, contours, hierarchy = cv2.findContours(thresholdedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		j = 0
		
		for i in contours:
			j += 1
			M = cv2.moments(i)
			
			if (M['m00'] > areaMin):
				cx = int(M['m01']/M['m00'])
				cy = int(M['m10']/M['m00'])
				robotPositionList.extend([(cx,cy)])
		
			if (len(robotPositionList) == 3): break
		
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