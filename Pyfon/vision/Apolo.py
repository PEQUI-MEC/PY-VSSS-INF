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
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				break
		
		return cx,cy
		
	def labelImage(self, imagem):
	
		for x in range(100,106,1):
			for y in range(100,106,1):
				imagem[x][y] = 1
				
				
		for x in range(200,206,1):
			for y in range(210,216,1):
				imagem[x][y] = 2
				
		for x in range(250,256,1):
			for y in range(300,306,1):
				imagem[x][y] = 3
				
		return imagem
		
	def findRobots(self, labelledImage, areaMin):
		robotLists = list()
		
		_, contours, hierarchy = cv2.findContours(labelledImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for i in contours:
			M = cv2.moments(i)
			
			if (M['m00'] > areaMin):
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				print ("X: ",cx," Y: ",cy)
				robotLists.extend([cx,cy])
				
		
		print (robotLists)
		
		return (103,103),(203,213),(253,303)
		
	def findAdvRobots(self, labelledImage):
		return ("ADV1:",103,103),("ADV2:",203,213),("ADV3:",253,303)
		
	def setRobots(self, labelledImage):
		return ("R1:",103,103),("R2:",203,213),("R3:",253,303)
		
	def findRobotOrientation(self,secondaryTagsImage):
		pass
		
	def findAdvOrientation(self,previousAdvPosition, currentAdvPosition):
		pass
		
	def findBallOrientation(self,previousBallPosition, currentBallPosition):
		pass