import cv2
import numpy as np

WIDTH = 640
HEIGHT = 480

class Apolo:
	def apllyThreshold(self, imagem, threshMin, threshMax):
		img = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
	
		for x in range(200,231,1):
			for y in range(300,321,1):
				img[x][y] = 255
				
		return img
	
	
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