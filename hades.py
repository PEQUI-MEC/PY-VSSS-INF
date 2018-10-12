# import numpy as np
import time
# from observer import Publisher, Subscriber
import threading

from vision import Apolo
from control import Zeus
from strategy import Athena


# This decorator returns time elapsed on execution of a method
# HOW TO USE
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

        # setting things up

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
        # aguardando luiz ter retorno do método run
        # deve settar o callback

        # setting up apolo
        self.apolo = Apolo.Apolo(self.apoloReady)

        # setting up athena
        self.athena = Athena(self.athenaReady)
        self.athena.setup(3, 300, 300, 1.0)

        # setting up zeus
        self.zeus = Zeus(self.zeusReady)
        self.zeus.setup(3)

        # setting up hermes
        # self.hermes = Hermes(self.srcXbee)
        # invocar fly do hermes como finalização
        # persephane deusa do submundo

    def apoloReady(self, positions):
        print("\t\tApolo ready")
        print(positions)
        self.athena.getTargets(positions)
        # atuaiza as posições na interface
        # recebe o frame e repassa para a interface
        # print(positions)
        

    def athenaReady(self, strategyInfo):
        print("\t\tAthena ready")
        print(strategyInfo)
        self.zeus.getVelocities(strategyInfo)
        
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
        print("choque do trovão")
        # self.hermes.fly(robots)

    def hermesReady(self, allDoneFlag):
        # faltando retorno do hermes de finalização
        # atualiza o FPS da interface
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
        # apolo inicia após start na captura da imagem
        # apolo inicia e nunca mais para de capturar
        self.apolo.run()

    def updatePositions(self):
        return True

    def updateFormation(self):
        return True

    def createFormation(self):
        return True

    def recordGame(self):
        return True

    ##### Callbacks from afrodite #####

    ## MenuBar
    #MenuBarArquivo
    def afLoadConfig(self):
        print("carregando configurações")

    def afSaveConfig(self):
        print("salvando configurações")

    ## Todo
    def startWarp(self):
        print("Hades started warping")

    def afStartButton(self):
        self.startButton = True
        self.puppetLoop()
        print("COMECOU!")

    def afStartCaptureButton(self, deviceLocation=None):
        print(deviceLocation)
        print("captura inicializada")

    def afStartSerialButton(self, deviceLocation=None):
        print(deviceLocation)
        print("serial inicializada")
    

    ##### \Callbacks from afrodite #####

def main():

    hades = Hades()

    hades.setup()
    hades.puppetLoop()
    
    hades.summonAfrodite()

    ##### Afrodite's event configuration #####
    # window.setActionLoadConfigsCallback(hades.afLoadConfig)
    # window.setActionSaveConfigsCallback(hades.afSaveConfig)

    # window.setPushButtonStartCallback(hades.afStartButton)
    # window.setPushButtonCaptureDeviceInformartionCallback(hades.afStartCaptureButton)
    # window.setPushButtonControlSerialDeviceCallback(hades.afStartSerialButton)

    # window.setLabelVideoViewFPS(123)

    # window.setStartWarpCallback(hades.startWarp)

    # ##### \Afrodite's event configuration #####

if __name__ == '__main__':
    # main()
    t = threading.Thread(name='daemon', target=main)
    t.setDaemon(True)
    t.start()
    t.join()
    