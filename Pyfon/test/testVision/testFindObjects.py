import unittest
import random
import numpy as np
import sys
import cv2
from vision import Apolo as Vision

apolo = Vision.Apolo()

WIDTH = 640 #X-axys
HEIGHT = 480 #Y-axys

#Simula o Labelling (retorna uma imagem como se tivesse feito o Labelling)
def getLabelledImage():
	imgLab = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
	imgThresh = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
	
	for x in range(100,106,1):
		for y in range(100,106,1):
			imgLab[x][y] = 1
			imgThresh[x][y] = 255
				
	for x in range(200,206,1):
		for y in range(210,216,1):
			imgLab[x][y] = 2
			imgThresh[x][y] = 255
			
	for x in range(250,256,1):
		for y in range(300,306,1):
			imgLab[x][y] = 3
			imgThresh[x][y] = 255

	return imgLab, imgThresh
	
#Simula o threshold(retorna uma imagem como se houvesse ocorrido um threshold nela)
def getThresholdedImage():
	img = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
	
	for x in range(200,231,1):
		for y in range(300,321,1):
			img[x][y] = 255
			
	return img



class TestSearchMethods(unittest.TestCase):
	#Testa a função de aplicar o threshold
	def testApplyThreshold(self):
		img = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
		
		thresholdedImage = getThresholdedImage()
		
		for x in range(0,200,1):
			for y in range(0,300,1):
				img[x][y] = random.randrange(100)
		
		for x in range(200,231,1):
			for y in range(300,321,1):
				img[x][y] = 150
		
		for x in range(231,640,1):
			for y in range(321,480,1):
				img[x][y] = random.randrange(201,256,1)
				
		self.assertTrue((thresholdedImage == apolo.apllyThreshold(img,100,200)).all())
		
	#Testa a função de encontrar a bola dado uma imagem com apenas um elemento
	def testFindBall(self):
		imagem = getThresholdedImage()
					

		#Ta invertido X com Y --- TODO: ARRUMAR
		self.assertEqual((310,215),apolo.findBall(imagem,50))
	
	#Testa a função de Label, dada uma imagem com três objetos
	def testLabelImage(self):
		thresholdedImage = np.zeros((WIDTH, HEIGHT), dtype = "uint8")
		
		labelledImage,_ = getLabelledImage()
		
		for x in range(100,106,1):
			for y in range(100,106,1):
				thresholdedImage[x][y] = 255
					
		for x in range(200,206,1):
			for y in range(210,216,1):
				thresholdedImage[x][y] = 255
				
		for x in range(250,256,1):
			for y in range(300,306,1):
				thresholdedImage[x][y] = 255
			
		self.assertTrue((labelledImage == apolo.labelImage(thresholdedImage)).all())
		
	#Testa a função de encontrar os robos, dada uma imagem onde o Label já ocorreu
	def testFindRobots(self):		
		labelledImage, threshImage = getLabelledImage()
				
		#self.assertEqual(((103,103),(203,213),(253,303)),apolo.findRobots(labelledImage))
		self.assertEqual(((103,103),(203,213),(253,303)),apolo.findRobots(threshImage,20))
	
	#Testa a função de encontrar os adversarios, dada uma imagem onde o Label ja ocorreu
	def testFindAdvRobots(self):
		labelledImage,_ = getLabelledImage()
				
		self.assertEqual((("ADV1:",103,103),("ADV2:",203,213),("ADV3:",253,303)),apolo.findAdvRobots(labelledImage))

	#Testa a função de identificar qual robo está em que posição, dada uma imagem com o threshold das tags secundarias feito
	def testSetRobots(self):
		labelledImage = getLabelledImage() #Para simular as tags secundarias, utilizei uma imagem com o Label feito
				
		self.assertEqual((("R1:",103,103),("R2:",203,213),("R3:",253,303)),apolo.setRobots(labelledImage))
	
if __name__ == '__main__':
    unittest.main()