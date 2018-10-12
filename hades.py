import time

from vision import Apolo
from control import Zeus
from strategy import Athena
from communication import Hermes


class Hades:
    def __init__(self, afrodite):
        # gods
        self.afrodite = afrodite
        self.apolo = Apolo(self.apoloReady)
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
        print("choque do trovão")
        self.hermes.fly(velocities)

    def hermesReady(self, messages):
        # faltando retorno do hermes de finalização
        # atualiza o FPS da interface
        if self.play:
            self.apolo.run()

    # EVENTOS

    def eventStart(self):
        self.play = not self.play

        if self.play:
            print("Started.")
            self.apolo.run()

    def eventStartXbee(self, port):
        self.hermes.setup(port)

    def eventSendMessage(self, robotId, leftWheel, rightWheel):
        message = self.hermes.createMessage(robotId, leftWheel, rightWheel)
        self.hermes.sendMessage(robotId, message)
        self.hermes.clearMessages()

    # Captura
    # TODO implementar callbacks de eventos das funções da captura

    # Vision
    # TODO implementar callbacks de eventos das funções da visão

    # Robots
    # TODO implementar callbacks de eventos das funções de configuração dos robôs

    # Control
    # TODO implementar callbacks de eventos das funções do controle

    # Communication
    # TODO implementar callbacks de eventos das funções da comunicação

    # Strategy
    # TODO implementar callbacks de eventos das funções da stratégia


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