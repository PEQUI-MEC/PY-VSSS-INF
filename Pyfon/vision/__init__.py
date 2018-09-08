import cv2
import numpy as np

WIDTH = 640
HEIGHT = 480

class Apolo:
	def __init__(self, callback):
		print("Apolo summoned")
		self.callback = callback

	def run(self):
		print("\tApolo working")
		positions = "posicoes"
		self.callback(positions)

	def apllyThreshold(self, imagem, threshMin, threshMax):
		img = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
	
		for x in range(200,230,1):
			for y in range(300,320,1):
				img[x][y] = 255
				
		return img
	
	
	def findBall(self, imagem):
		return 310,215
		
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
		
	def findRobots(self, labelledImage):
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