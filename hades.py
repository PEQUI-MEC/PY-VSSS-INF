import time
from PyQt5.QtCore import QThread, pyqtSignal

from vision import Apolo
from control import Zeus
from strategy import Athena
from communication import Hermes


class Hades(QThread):
    sigfps = pyqtSignal(str)

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
            positions = self.runApolo()

            if self.play:
                commands = self.runAthena(positions)
                velocities = self.runZeus(commands)
                self.hermesRules(velocities)

            self.getFPS()

    def stop(self):
        self.wait()

    # MAIN METHODS

    def runApolo(self):
        """
        Roda a visão, atualiza a interface e retorna as posições

        Returns:
            lista com as posições dos objetos
        """
        if self.apolo is None:
            return

        positions, frame = self.apolo.run()

        # atualiza o vídeo na interface
        self.prepareDraw(positions)
        self.afrodite.updateFrameVideoView(frame)

        # atualiza as posições dos robôs na interface
        self.afrodite.updateLabelVideoViewPositionsRobot1(positions[0][0]["position"], positions[0][0]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsRobot2(positions[0][1]["position"], positions[0][1]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsRobot3(positions[0][2]["position"], positions[0][2]["orientation"])
        self.afrodite.updateLabelVideoViewPositionsBall(positions[2]["position"])

        if self.isCalibrating:
            index = self.afrodite.getHSVIndex()
            self.apolo.setHSVThresh(self.afrodite.getHSVCalibration(index), index)

        return positions

    def runAthena(self, positions):
        commands = self.athena.getTargets(positions)

        return commands

    def zeusRules(self, commands):
        velocities = self.zeus.getVelocities(commands)
        return velocities

    def hermesRules(self, velocities):
        self.hermes.fly(velocities)

    # HELPERS
    def getFPS(self):
        # calcula o fps e manda pra interface
        self.cascadeTime += time.time() - self.cascadeLastTime
        self.cascadeLoops += 1
        self.cascadeLastTime = time.time()
        if self.cascadeTime > 1:
            fps = self.cascadeLoops / self.cascadeTime
            self.sigfps.emit("{:.2f}".format(fps))
            self.cascadeTime = self.cascadeLoops = 0

    def prepareDraw(self, positions):
        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.afrodite.objectsToDraw["robot" + str(i + 1)] = {
                "shape": "robot",
                "position": positions[0][i]["position"],
                "color": (255, 255, 0),
                "label": str(i + 1),
                "orientation": positions[0][i]["orientation"]
            }

        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.afrodite.objectsToDraw["advRobot" + str(i + 1)] = {
                "shape": "robot",
                "position": positions[1][i]["position"],
                "color": (0, 0, 255),
                "label": str(i + 1),
            }

        self.afrodite.objectsToDraw["ball"] = {
            "shape": "circle",
            "position": positions[2]["position"],
            "color": (255, 255, 255),
            "label": "Bola",
            "radius": 4
        }

    # EVENTOS
    # Hades
    def eventStartGame(self):
        self.play = not self.play
        print("Hades started") if self.play else print("Hades stopped")

    # Camera e Visão
    def calibrationEvent(self):
        if self.isCalibrating:
            self.isCalibrating = False
            self.apolo.resetImageId()
        else:
            self.isCalibrating = True

    def eventStartVision(self, cameraId):
        self.apolo = Apolo(cameraId)

    def changeCamera(self, cameraId):
        self.apolo.changeCamera(cameraId)

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
