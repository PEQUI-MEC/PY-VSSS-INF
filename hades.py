import time

from vision import Apolo
from control import Zeus
from strategy import Athena
from communication import Hermes
from vision import Ciclope


class Hades:
    def __init__(self, afrodite):
        # gods
        self.afrodite = afrodite
        self.ciclope = Ciclope(0)
        self.apolo = Apolo(self.apoloReady, self.ciclope)
        self.athena = Athena(self.athenaReady)
        self.zeus = Zeus(self.zeusReady)
        self.hermes = Hermes(self.hermesReady)

        self.play = False

        print("Hades summoned")

    def setup(self):
        # set up apolo

        # set up athena
        self.athena.setup(3, 300, 300, 1.0)

        # set up zeus
        self.zeus.setup(3)

        # setting up hermes
        # self.hermes = Hermes(self.srcXbee)
        # invocar fly do hermes como finalização
        # persephane deusa do submundo

    # CALLBACKS

    def apoloReady(self, positions, imagem):
        print("\t\tApolo ready")
        print(positions)
        self.afrodite.updateFrameVideoView(imagem)

        if (self.play):
            self.athena.getTargets(positions)
        # atuaiza as posições na interface
        # recebe o frame e repassa para a interface
        # print(positions)

    def athenaReady(self, strategyInfo):
        print("\t\tAthena ready")
        print(strategyInfo)
        self.zeus.getVelocities(strategyInfo)

    def zeusReady(self, velocities):
        print("choque do trovão")
        self.hermes.fly(velocities)

    def hermesReady(self, messages):
        # faltando retorno do hermes de finalização
        # atualiza o FPS da interface
        if self.play:
            self.apolo.run()

    # EVENTOS

    def eventStartVision(self):
            self.apolo.run()

    def eventStartGame(self):
        self.play = not self.play

        if self.play:
            print("Started.")
            self.apolo.run()

    def eventStartXbee(self, port):
        self.hermes.setup(port)

    def eventCreateAndSendMessage(self, robotId, leftWheel, rightWheel):
        message = self.hermes.createMessage(robotId, leftWheel, rightWheel)
        self.hermes.sendMessage(robotId, message)
        self.hermes.clearMessages()

    def eventSendMessage(self, message):
        self.hermes.sendMessage(message)

    # Captura
    # TODO implementar callbacks de eventos das funções da captura
    def changeCamera(self,id):
        self.ciclope.changeCamera(id)

    # Vision
    # TODO implementar callbacks de eventos das funções da visão

    # Robots
    # TODO implementar callbacks de eventos das funções de configuração dos robôs

    # Control
    # TODO implementar callbacks de eventos das funções do controle
    def eventUpdateSpeeds(self, attackSpeed, defenseSpeed, goalkeeperSpeed):
        self.zeus.updateSpeeds(attackSpeed, defenseSpeed, goalkeeperSpeed)

    def enablePIDTest(self):
        print("PID test enabled")

    def disablePIDTest(self):
        print("PID test disabled")

    # Communication
    # TODO implementar callbacks de eventos das funções da comunicação

    # Strategy
    # TODO implementar callbacks de eventos das funções da stratégia
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