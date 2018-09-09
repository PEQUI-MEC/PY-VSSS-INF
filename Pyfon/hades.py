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

class Hades():
    def __init__(self, srcCam=None, srcBee=None):

        ### setting things up

        # sources
        self.srcCamera = srcCam
        self.srcXbee = srcBee

        # gods
        self.afrodite = None
        self.apolo = None
        self.athena = None
        self.zeus = None
        self.hermes = None

        # variables
        self.startButton = False

    def setup(self):
        # self.afrodite = Afrodite(self)
        # aguardando luiz ter retorno do método run
        # deve settar o callback
        # self.apolo = Apolo(self.apoloReady)
        self.athena = Athena(self.athenaReady)
        self.zeus = Zeus(self.zeusReady)
        self.hermes = Hermes(self.srcXbee)
        # invocar fly do hermes como finalização
        # persephane deusa do submundo

    def printTest(self):
        print("test")

    def apoloReady(self, positions):
        print("\t\tApolo ready")
        self.athena.getTargets(positions)

    def athenaReady(self, strategyInfo):
        print("\t\tAthena ready")
        self.zeus.run(strategyInfo)
        
    def zeusReady(self, velocities):
        robots = [
            #robot 1
			[
				0,
				velocities[0]['vLeft'],
				velocities[0]['vRight']
	    	],
	    	#robot 2
			[
				1,
				velocities[1]['vLeft'],
				velocities[1]['vRight']
			],
			#robot 3
			[
				2,
				velocities[2]['vLeft'],
				velocities[2]['vRight']
			],
        ]
        self.hermes.fly(robots)

    def hermesReady(self, allDoneFlag):
        # faltando retorno do hermes de finalização
        pass

    # Set link between camera and software
    def summonCapture(self):
        # try:
        #     cap = cv2.VideoCapture(self.srcCamera)
        # except cv2.error:
        #     return None
        # else:
        #     return cap
        
        pass
    
    # Unlink camera and software
    def killCapture(self):
        # try:
        #     self.cap.release()
        #     cv2.destroyAllWindows()
        # except cv2.error:
        #     print("Sorry =( I cannot stop your capture connection.\n")
        #     return self.cap
        # else:
        #     return None
        pass
    
    # Cleanup capture flags and set again
    def refreshCapture(self):
        # self.killCapture()
        # self.summonCapture()
        # return True
        pass

    def summonCommunication(self):
        return True

    def puppetLoop(self):
        # inicia o fluxo de eventos
        # verifica se nenhum erro aconteceu
        '''
        Interface (start button)
                |
                V
              apolo
                |
                V
              athena
                |
                V
               zeus
                |
                V
              hermes
        '''
        
        # loops while startButton flag is True
        while self.startButton is True:
            self.apolo.run()

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

    app=QApplication(sys.argv)
    window=Afrodite()
    window.show()
    sys.exit(app.exec_())

    self.setup()

if __name__ == '__main__':
    main()