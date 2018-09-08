# import numpy as np
import sys, time
import cv2
from observer import Publisher, Subscriber
from vision import Apolo
from control import Zeus
from strategy.athena import Athena
from communication.hermes import Hermes

from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QMenuBar,QDockWidget,QCheckBox,QStackedWidget,QFileDialog
sys.path.append("interface/")
from afrodite import Afrodite

# This decorator returns time elapsed on execution of a method
##### HOW TO USE #####
# Before the method, place @timeToFinish
# In the terminal will be printed the time elapsed on method execution

def timeToFinish(method):
    def timed(*args, **kwargs):
        tStart = time.time()
        result = method(*args, **kwargs)
        tEnd = time.time()

        print("{:.3f} sec".format(tEnd-tStart))
        return result
    return timed

class Hades:
    def __init__(self, srcCam=None, srcBee=None):

        self.srcCamera = srcCam
        self.srcXbee = srcBee

        self.apolo = Apolo(self.apoloReady)
        self.athena = Athena(self.athenaReady)
        self.zeus = Zeus(self.zeusReady)
        # self.hermes = Hermes("port")
        # invocar fly do hermes como finalização
        # persephane  deusa do submundo

        self.apolo.run()

        # setting things up

    def apoloReady(self, positions):
        print("\t\tchamar estratégia")
        self.athena.run(positions)

    def athenaReady(self, positions):
        print("\t\tchamar controle")
        self.zeus.run(positions)
        print("chamar interface")
        
    def zeusReady(self, rainhos):
        print("\t\tchoque do trovão")

    def hermesReady(self, botinhasQueVoam):
        pass

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
        # inicia o fluxo de eventos
        # verifica se nenhum erro aconteceu
        
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