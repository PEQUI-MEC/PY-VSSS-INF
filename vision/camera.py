import cv2

class Ciclope:
    def __init__(self, cameraId):
        self.camera = cv2.VideoCapture(cameraId)

    #Testar o changeCamera
    def changeCamera(self, cameraId):
        self.killYourself()
        self.camera = cv2.VideoCapture(cameraId)
    def getFrame(self):
        return self.camera.read()

    def killYourself(self):
        print ("SUICIDE!")
        self.camera.release()

    def isCameraOpened(self):
        return self.camera.isOpened()