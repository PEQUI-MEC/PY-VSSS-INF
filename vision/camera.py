import cv2

class Ciclope:
    def __init__(self, id):
        self.camera = cv2.VideoCapture(id)
        print("Ciclope summoned")

    def getFrame(self):
        return self.camera.read()

    def changeCamera(self,id):
        self.killYourself()
        self.camera = cv2.VideoCapture(id)

    def killYourself(self):
        print ("SUICIDE!")
        self.camera.release()

    def isCameraOpened(self):
        return self.camera.isOpened()