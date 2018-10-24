import time
import threading

from vision import Apolo
from vision import Ciclope
from control import Zeus
from strategy import Athena
from communication import Hermes


class Hades:
    def __init__(self, afrodite):
        # gods
        self.afrodite = afrodite
        #self.apolo = Apolo(self.apoloReady, self.ciclope)
        self.athena = Athena(self.athenaReady)
        self.zeus = Zeus(self.zeusReady)
        self.hermes = Hermes(self.hermesReady)

        self.play = False
        self.isCalibrating = False

        self.timeCascadeStarted = 0

        print("Hades summoned")

    def setup(self):
        # set up apolo

        # set up athena
        # TODO passar as dimensões corretamente
        self.athena.setup(3, 300, 300, 1.0)

        # set up zeus
        self.zeus.setup(3)

        # setting up hermes
        # self.hermes = Hermes(self.srcXbee)
        # invocar fly do hermes como finalização
        # persephane deusa do submundo

    # CALLBACKS

    def apoloReady(self, positions, imagem):
        # calcula o fps e manda pra interface
        lastCascadeTime = time.time() - self.timeCascadeStarted
        fps = 1 / lastCascadeTime
        self.afrodite.setLabelVideoViewFPS("{:.2f}".format(fps))
        self.timeCascadeStarted = time.time()

        # atualiza o vídeo na interface
        self.afrodite.updateFrameVideoView(imagem)

        # atualiza as posições dos robôs na interface
        self.afrodite.updateLabelVideoViewPositionsRobot1(positions[0][0]["position"], positions[0][0]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsRobot2(positions[0][1]["position"], positions[0][1]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsRobot3(positions[0][2]["position"], positions[0][2]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsBall(positions[2]["position"])

        if self.isCalibrating:
            index = self.afrodite.getHSVIndex()
            self.apolo.setHSVThresh(self.afrodite.getHSVCalibration(index), index)
        
        # decide qual é o próximo módulo na cascata
        if self.play:
            nextOnCascade = threading.Thread(target=self.athena.getTargets, args=[positions])
        else:
            nextOnCascade = threading.Thread(target=self.apolo.run)

        nextOnCascade.start()  # inicia o processamento no próximo módulo (deve ser a última coisa a ser feita)

    def athenaReady(self, strategyInfo):
        # print("\t\tAthena ready")

        # decide qual é o próximo módulo na cascata
        if self.play:
            nextOnCascade = threading.Thread(target=self.zeus.getVelocities, args=[strategyInfo])
        else:
            nextOnCascade = threading.Thread(target=self.apolo.run)
            
        nextOnCascade.start()

    # EVENTOS
    def calibrationEvent(self):
        if self.isCalibrating:
            self.isCalibrating = False
            self.apolo.resetImageId()
        else:
            self.isCalibrating = True

    def zeusReady(self, velocities):
        # print("\t\tZeus ready")

        # decide qual é o próximo módulo na cascata
        if self.play:
            nextOnCascade = threading.Thread(target=self.hermes.fly, args=[velocities])
        else:
            nextOnCascade = threading.Thread(target=self.apolo.run)

        nextOnCascade.start()  # inicia o processamento no próximo módulo

    def hermesReady(self, messages):
        # TODO está faltando retorno do hermes de finalização
        # TODO atualizar o FPS da interface
        nextOnCascade = threading.Thread(target=self.apolo.run)
        nextOnCascade.start()  # inicia o processamento no próximo módulo

    # EVENTOS
    # Hades
    def eventStartGame(self):
        self.play = not self.play
        print("Hades started") if self.play else print("Hades stopped")

    # Camera e Visão
    def eventStartVision(self, cameraId):
        self.ciclope = Ciclope(int(cameraId))
        self.apolo = Apolo(self.apoloReady, self.ciclope)
        apoloThread = threading.Thread(target=self.apolo.run)
        apoloThread.start()

    def changeCamera(self, cameraId):
        self.ciclope.changeCamera(cameraId)

    def setHSVVision(self, thresholdId):
        self.apolo.setImg(thresholdId)

    # Control
    def eventUpdateSpeeds(self, attackSpeed, defenseSpeed, goalkeeperSpeed):
        self.zeus.updateSpeeds(attackSpeed, defenseSpeed, goalkeeperSpeed)

    def enablePIDTest(self):
        print("PID test enabled")

    def disablePIDTest(self):
        print("PID test disabled")

    # Communication
    def eventStartXbee(self, port):
        self.hermes.setup(port=port)

    def eventCreateAndSendMessage(self, robotId, leftWheel, rightWheel):
        message = self.hermes.createMessage(robotId, leftWheel, rightWheel)
        self.hermes.sendMessage(robotId, message)
        self.hermes.clearMessages()

    def eventSendMessage(self, message):
        self.hermes.sendMessage(message)

    # Strategy
    def eventToggleTransitions(self, state):
        self.athena.setTransitionsState(state)

    def eventSelectRoles(self, roles):
        self.athena.setRoles(roles)


def timeToFinish(method):
    # This decorator returns time elapsed on execution of a method
    # HOW TO USE
    # Before the method, place @timeToFinish
    # In the terminal will be printed the time elapsed on method execution

    def timed(*args, **kwargs):
        tStart = time.time()
        result = method(*args, **kwargs)
        tEnd = time.time()

        print("{:.3f} sec".format(tEnd-tStart))
        return result
    return timed
