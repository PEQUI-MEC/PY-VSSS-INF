# import numpy as np
import cv2
import sys
from observer import Publisher, Subscriber
from interface.afrodite import Afrodite
from control import Zeus
# importar estratégia
from communication.hermes import Hermes

from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget,QFileDialog

class Hades:
    def __init__(self, srcCam=None, srcBee=None):

        self.channels = ['vision', 'strategy', 'control', 'communication']
        self.srcCamera = srcCam
        self.srcXbee = srcBee
        
        # initializing all publishers
        self.hadesPub = Publisher(self.channels)
        self.apoloPub = Publisher(self.channels[0:1])
        self.athenaPub = Publisher(self.channels[1:2])
        self.zeusPub = Publisher(self.channels[2:3])
        self.hermesPub = Publisher(self.channels[3:4])

        # initializing all subscribers
        self.hadesSub = Subscriber('hades')   # manager
        self.apoloSub = Subscriber('apolo')   # visão
        self.athenaSub = Subscriber('athena') # strategy
        self.zeusSub = Subscriber('zeus')     # control
        self.hermesSub = Subscriber('hermes') # communication

        # registering subscribers
        self.apoloPub.register(self.channels[0], self.hadesSub)
        self.apoloPub.register(self.channels[0], self.athenaSub)
        self.athenaPub.register(self.channels[1], self.hadesSub)
        self.athenaPub.register(self.channels[1], self.zeusSub)
        self.zeusPub.register(self.channels[2], self.hadesSub)
        self.zeusPub.register(self.channels[2], self.hermesSub)
        self.hermesPub.register(self.channels[3], self.hadesSub)
        
        self.apoloPub.dispatch("vision", "STARRRRRT")

        # setting things up

    def setup(self):
        pass

    # Set link between camera and software
    # def summonCapture(self):
    #     try:
    #         cap = cv2.VideoCapture(self.srcCamera)
    #     except cv2.error:
    #         return None
    #     else:
    #         return cap
    #
    # # Unlink camera and software
    # def killCapture(self):
    #     try:
    #         self.cap.release()
    #         cv2.destroyAllWindows()
    #     except cv2.error:
    #         print("Sorry =( I cannot stop your capture connection.\n")
    #         return self.cap
    #     else:
    #         return None
    #
    # # Cleanup capture flags and set again
    # def refreshCapture(self):
    #     self.killCapture()
    #     self.summonCapture()
    #     return True

    def summonCommunication(self):
        return True

    def puppetLoop(self):
        return True

    def updatePositions(self):
        return True

    def updateFormation(self):
        return True

    def createFormation(self):
        return True

    def recordGame(self):
        return True

def main():
    hades = Hades()

    # app=QApplication(sys.argv)
    # window=Afrodite()
    # window.show()
    # sys.exit(app.exec_())

if __name__ == '__main__':
    main()