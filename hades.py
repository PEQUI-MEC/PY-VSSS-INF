from PyQt5.QtCore import QThread, pyqtSignal
import time
import numpy

from helpers.plutus import Plutus

from vision import Apolo
from control import Zeus
from strategy import Athena
from communication import Hermes


class Hades(QThread):
    sigFps = pyqtSignal(str)
    sigDraw = pyqtSignal(dict)
    sigDisplay = pyqtSignal(numpy.ndarray)
    sigPositions = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        # gods
        self.apolo = None
        self.athena = Athena()
        self.zeus = Zeus()
        self.hermes = Hermes()

        self.play = False
        self.isCalibrating = False

        self.cascadeTime = 0
        self.cascadeLoops = 0
        self.cascadeLastTime = 0

        print("Hades summoned")

    def __del__(self):
        self.wait()

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

    # LOOP PRINCIPAL
    def run(self):
        while True:
            # visão
            positions = self.apoloRules()

            if self.play:
                commands = self.athenaRules(positions)
                velocities = self.zeusRules(commands)
                self.hermesRules(velocities)

            time.sleep(0.0001)
    # MAIN METHODS

    def apoloRules(self):
        """
        Roda a visão, atualiza a interface e retorna as posições

        Returns:
            lista com as posições dos objetos
        """
        if self.apolo is None:
            return None

        positions, frame = self.apolo.run()

        # atualiza o vídeo na interface
        self.prepareDraw(positions)
        self.sigDisplay.emit(frame)

        # atualiza as posições dos robôs na interface
        formattedPositions = [
            [
                positions[0][0]["position"],
                positions[0][0]["orientation"],
            ],
            [
                positions[0][1]["position"],
                positions[0][1]["orientation"],
            ],
            [
                positions[0][2]["position"],
                positions[0][2]["orientation"],
            ],
            positions[2]["position"]
        ]
        self.sigPositions.emit(formattedPositions)

        self.getFPS()

        return positions

    def athenaRules(self, positions):
        if positions is None:
            return None

        commands = self.athena.getTargets(positions)
        return commands

    def zeusRules(self, commands):
        if commands is None:
            return None

        velocities = self.zeus.getVelocities(commands)
        return velocities

    def hermesRules(self, velocities):
        if velocities is None:
            return None

        self.hermes.fly(velocities)

    # HELPERS
    def getFPS(self):
        # calcula o fps e manda pra interface
        self.cascadeTime += time.time() - self.cascadeLastTime
        self.cascadeLoops += 1
        self.cascadeLastTime = time.time()
        if self.cascadeTime > 1:
            fps = self.cascadeLoops / self.cascadeTime
            self.sigFps.emit("{:.2f}".format(fps))
            self.cascadeTime = self.cascadeLoops = 0

    def prepareDraw(self, positions):
        objectsToDraw = {}

        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            objectsToDraw["robot" + str(i + 1)] = {
                "shape": "robot",
                "position": positions[0][i]["position"],
                "color": (255, 255, 0),
                "label": str(i + 1),
                "orientation": positions[0][i]["orientation"]
            }

        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            objectsToDraw["advRobot" + str(i + 1)] = {
                "shape": "robot",
                "position": positions[1][i]["position"],
                "color": (0, 0, 255),
                "label": str(i + 1),
            }

        objectsToDraw["ball"] = {
            "shape": "circle",
            "position": positions[2]["position"],
            "color": (255, 255, 255),
            "label": "Bola",
            "radius": 4
        }

        self.sigDraw.emit(objectsToDraw)

    # EVENTOS
    # Hades
    def eventStartGame(self):
        self.play = not self.play
        print("Hades started") if self.play else print("Hades stopped")

    # Camera e Visão
    def getCamCongigs(self):
        return self.apolo.getCamConfigs()

    def eventCamConfigs(self, newBrightness, newSaturation, newGain, newContrast, newHue,
                        newExposure, newWhiteBalanceU, newWhiteBalanceV, newIsoSpeed):
        if self.apolo is not None:
            self.apolo.updateCamConfigs(newBrightness, newSaturation, newGain, newContrast, newHue, newExposure,
                                        newWhiteBalanceU, newWhiteBalanceV, newIsoSpeed)

    def calibrationEvent(self, imageId, calibration=None):
        if self.apolo is not None:
            self.apolo.setHSVThresh(calibration, imageId)

    def eventStartVision(self, cameraId):
        self.apolo = Apolo(int(cameraId))

    def eventStopVision(self):
        self.apolo.closeCamera()
        self.apolo = None
        # self.changeCamera(cameraId)
        # pass

    def changeRobotLetters(self, robotLetters):
        self.apolo.changeLetters(robotLetters)

    def changeCamera(self, cameraId):
        if self.apolo is not None:
            self.apolo.changeCamera(cameraId)

    def setHSVVision(self, thresholdId):
        if self.apolo is not None:
            self.apolo.setImg(thresholdId)

    # Strategy
    def eventToggleTransitions(self, state):
        self.athena.setTransitionsState(state)

    def eventSelectRoles(self, roles):
        self.athena.setRoles(roles)

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

    def eventsendMessage(self, robotId, message):
        self.hermes.sendMessage(robotId, message)


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
