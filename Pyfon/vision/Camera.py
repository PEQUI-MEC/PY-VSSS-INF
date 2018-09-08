import cv2

class Ciclope:
	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		
	def getFrame(self):
		return self.camera.read()
		
	def killYourself(self):
		print ("SUICIDE!")
		self.camera.release()
		
	def isOpened(self):
		return self.camera.isOpened()