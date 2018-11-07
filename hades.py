from PyQt5.QtCore import QThread, pyqtSignal
import time
import numpy
from scipy.spatial import distance
from helpers.endless import Endless
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
    sigMessages = pyqtSignal(list)
    sigRemoveDraw = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        # gods
        self.apolo = None
        self.athena = Athena()
        self.zeus = Zeus()
        self.hermes = Hermes()

        self.plutus = Plutus()

        self.play = False
        self.isCalibrating = False

        self.height = 480  # TODO pegar isso da afrodite e passar pro apolo
        self.width = 640

        self.skippedFrames = 0
        self.framesToSkip = 5  # valor padrão

        self.cascadeTime = 0
        self.cascadeLoops = 0
        self.cascadeLastTime = 0

        # formations
        self.formationToExecute = -1
        self.formations = []
        self.formating = False

        self.pidTesting = False
        self.pidRobot = -1
        self.pidTarget = None
        self.pidSpeed = 0.4

        self.drawStrategyConstants = False

        print("Hades summoned")

    def __del__(self):
        self.wait()

    def setup(self):
        # set up apolo

        # set up athena
        # TODO passar as dimensões corretamente
        self.athena.setup(3, self.width, self.height, 0.6)

        # set up zeus
        # TODO passar as dimensões corretamente
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

            elif self.pidTesting:
                commands = self.getPIDTarget(positions)
                velocities = self.zeusRules(commands)
                self.hermesRules(velocities)

            elif self.formating:
                commands = self.executeFormation(positions)
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
        if frame is not None:
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
        if self.skippedFrames < self.framesToSkip:
            self.skippedFrames += 1
            return None

        if velocities is None:
            return None

        hermesMessages = self.hermes.fly(velocities)
        self.sigMessages.emit(hermesMessages)

        self.skippedFrames = 0

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
                "position": (int(positions[0][i]["position"][0] - Endless.robotSize / 2),
                             int(self.height - positions[0][i]["position"][1] - Endless.robotSize / 2)),
                "color": (255, 255, 0),
                "label": str(i + 1),
                "orientation": positions[0][i]["orientation"]
            }

        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            objectsToDraw["advRobot" + str(i + 1)] = {
                "shape": "robot",
                "position": (int(positions[1][i]["position"][0] - Endless.robotSize / 2),
                             int(self.height - positions[1][i]["position"][1] - Endless.robotSize / 2)),
                "color": (0, 0, 255),
                "label": str(i + 1),
            }

        objectsToDraw["ball"] = {
            "shape": "circle",
            "position": (positions[2]["position"][0], self.height - positions[2]["position"][1]),
            "color": (255, 255, 255),
            "label": "Bola",
            "radius": 4
        }

        if self.drawStrategyConstants:
            objectsToDraw["strategyGoalieLine"] = {
                "shape": "line",
                "position": (Endless.goalieLine, int(Endless.goalTop)),
                "target": (Endless.goalieLine, int(Endless.goalBottom)),
                "label": "Goalie Line",
                "color": (0, 255, 0)
            }
            objectsToDraw["strategyAreaLine"] = {
                "shape": "line",
                "position": (Endless.areaLine, int(Endless.areaTop)),
                "target": (Endless.areaLine, int(Endless.areaBottom)),
                "label": "Area Line",
                "color": (0, 255, 0)
            }
            objectsToDraw["strategyGoalBorder1"] = {
                "shape": "line",
                "position": (int(Endless.goalSize[0]), int(Endless.areaTop)),
                "target": (Endless.areaLine, int(Endless.areaTop)),
                "label": "Goal Border",
                "color": (0, 255, 0)
            }
            objectsToDraw["strategyGoalBorder2"] = {
                "shape": "line",
                "position": (int(Endless.goalSize[0]), int(Endless.areaBottom)),
                "target": (Endless.areaLine, int(Endless.areaBottom)),
                "label": "Goal Border",
                "color": (0, 255, 0)
            }

        if self.pidRobot != -1:
            objectsToDraw["pidRobot"] = {
                "shape": "rect",
                "position": (int(positions[0][self.pidRobot]["position"][0] - Endless.robotSize / 2 - 5),
                             int(self.height - positions[0][self.pidRobot]["position"][1] - Endless.robotSize / 2 - 5)),
                "limit": Endless.robotSize + 10,
                "color": (255, 255, 255),
                "label": "Selecionado",
            }

        if self.pidTarget:
            objectsToDraw["pidTarget"] = {
                "shape": "circle",
                "position": (self.pidTarget[0], self.height - self.pidTarget[1]),
                "color": (255, 255, 255),
                "label": "Alvo",
                "radius": 6
            }

        self.sigDraw.emit(objectsToDraw)

    def getPIDTarget(self, positions):
        if not self.pidTarget or self.pidRobot == -1:
            return None

        commands = []

        for i in range(len(positions)):
            if i == self.pidRobot:
                if distance.euclidean(positions[0][i]["position"], self.pidTarget) < Endless.robotSize:
                    self.pidTarget = None
                else:
                    commands.append(
                        {
                            "command": "goTo",
                            "robotLetter": positions[0][i]["robotLetter"],
                            "data": {
                                "pose": {
                                    "position": positions[0][i]["position"],
                                    "orientation": positions[0][i]["orientation"]
                                },
                                "target": {
                                    "position": self.pidTarget,
                                    "orientation": Endless.pastGoal
                                },
                                "velocity": self.pidSpeed
                            }
                        }
                    )
                    continue

            commands.append(
                {
                    "command": "stop",
                    "robotLetter": positions[0][i]["robotLetter"],
                    "data": {
                        "before": 0
                    }
                }
            )

        return commands

    def executeFormation(self, positions):
        if self.formationToExecute == -1:
            return None

        commands = []

        for i in range(positions[0]):
            if distance.euclidean(positions[0][i]["position"],
                                  self.formations[self.formationToExecute]["positions"][i]) < Endless.robotSize:
                commands.append(
                    {
                        "command": "lookAt",
                        "robotLetter": positions[0][i]["robotLetter"],
                        "data": {
                            "pose": {
                                "position": positions[0][i]["position"],
                                "orientation": positions[0][i]["orientation"]
                            },
                            "target": self.formations[self.formationToExecute]["orientations"][i],
                            "velocity": 0.4
                        }
                    }
                )
            else:
                commands.append(
                    {
                        "command": "goTo",
                        "robotLetter": positions[0][i]["robotLetter"],
                        "data": {
                            "pose": {
                                "position": positions[0][i]["position"],
                                "orientation": positions[0][i]["orientation"]
                            },
                            "target": {
                                "position": self.formations[self.formationToExecute]["positions"][i],
                                "orientation": self.formations[self.formationToExecute]["orientations"][i]
                            },
                            "velocity": 0.4
                        }
                    }
                )

        return commands

    # EVENTOS
    # Hades
    def eventStartGame(self):
        self.play = not self.play

        if self.play:
            self.athena.reset()
            self.zeus.reset()
            print("Hades started")
        else:
            print("Hades stopped")

        return self.play

    def setRobotRadiusEvent(self, robotRadius):
        self.apolo.setRobotRadius(robotRadius)

    def SetFileSave(self, file):
        self.plutus.setFile(file)

    def eventSaveConfigs(self, value):
        for key in value:
            self.plutus.set(key, value[key])
        print("Save configs")

    def eventLoadConfigs(self, key=None):
        if key is None:
            return self.plutus.get()

        value = self.plutus.get(key)
        if value is not None:
            return value
        else:
            return 0

    def saveFormation(self, positions, orientations):
        newFormation = {
            "positions": positions,
            "orientations": orientations
        }
        self.formations.append(newFormation)
        self.plutus.set("formations", self.formations)

    def loadFormations(self):
        self.formations = self.plutus.get("formations")
        return self.formations

    def loadFormation(self, formationIndex):
        if self.play:
            return

        self.formationToExecute = formationIndex
        self.formating = True

    def stopFormation(self):
        self.formationToExecute = -1
        self.formating = False
    
    # Camera e Visão
    def eventInvertImage(self, state):
        if self.apolo is not None:
            return self.apolo.setInvertImage(state)
        return False

    def getCameraConfigs(self):
        return self.apolo.getCamConfigs()

    def eventCamConfigs(self, newBrightness, newSaturation, newGain, newContrast,
                        newExposure, newWhiteBalance):
        if self.apolo is not None:
            self.apolo.updateCamConfigs(newBrightness, newSaturation, newGain, newContrast, newExposure,
                                        newWhiteBalance)

    def eventCalibration(self, imageId, calibration=None):
        if self.apolo is not None:
            self.apolo.setHSVThresh(calibration, imageId)

    def eventStartVision(self, cameraId):
        try:
            self.apolo = Apolo(int(cameraId))
            # self.apolo = Apolo(0)
            return True
        except:
            return False

    # refresh não funciona; programa fechando
    # def eventStopVision(self):
    #     if self.apolo is not None:
    #         self.apolo.closeCamera()
    #         self.apolo = None

    def changeRobotLetters(self, robotLetters):
        if self.apolo is not None:
            return self.apolo.changeLetters(robotLetters)
        return ["A", "B", "C"]

    def closeCamera(self):
        if self.apolo is not None:
            self.apolo.closeCamera()

    def changeCamera(self, cameraId):
        if self.apolo is not None:
            self.apolo.changeCamera(cameraId)

    def setHSVVision(self, thresholdId):
        if self.apolo is not None:
            self.apolo.setImg(thresholdId)

    # Warp
    def eventWarp(self, warpMatriz):
        self.apolo.setWarpPoints(warpMatriz[0], warpMatriz[1], warpMatriz[2], warpMatriz[3])
        
    # WarpGoal
    def eventWarpGoalMatriz(self, warpMatriz):
        return self.apolo.setWarpGoalMatriz(warpMatriz)

    def eventWarpReset(self):
        self.apolo.resetWarp()

    # Offset

    def eventWarpOffsetChanged(self, offsetLeft, offsetRight):
        self.apolo.setWarpOffset(offsetLeft, offsetRight)
        
    # Strategy
    def eventToggleTransitions(self, state):
        self.athena.setTransitionsState(state)

    def setDrawConstantsState(self, state):
        self.drawStrategyConstants = state

    def eventSelectRoles(self, roles):
        self.athena.setRoles(roles)

    @staticmethod
    def updateStrategyConstants(goalieLine, goalieOffset, areaLine):
        Endless.goalieOffset = goalieLine
        Endless.areaBorderOffset = goalieOffset
        Endless.areaOffset = areaLine

        Endless.areaTop = Endless.height / 2 + Endless.areaSize[1] / 2 + Endless.areaBorderOffset  # em Y
        Endless.areaBottom = Endless.height / 2 - Endless.areaSize[1] / 2 - Endless.areaBorderOffset  # em Y
        Endless.goalieLine = Endless.goalSize[0] + Endless.robotSize + Endless.goalieOffset  # em X
        Endless.areaLine = Endless.goalSize[0] + Endless.areaSize[0] + Endless.robotSize + Endless.areaOffset  # em X

    # Control
    def eventUpdateSpeeds(self, speeds):
        self.zeus.updateSpeeds(speeds)
        # self.athena.setVelocities(speeds[0], speeds[1], speeds[2])

    # PID TEST
    def enablePIDTest(self, state):
        self.pidTarget = None
        self.pidRobot = -1
        self.pidTesting = state

    def setRobotPID(self, robotID):
        self.pidRobot = robotID
        if robotID == -1:
            self.pidTarget = None

            self.sigRemoveDraw.emit("pidTarget")
            self.sigRemoveDraw.emit("pidRobot")

    def setPointPID(self, point):
        if self.pidRobot != -1:
            self.pidTarget = (point[0], Endless.height - point[1])

    def setPIDSpeed(self, speed):
        try:
            speed = float(speed)
            self.pidSpeed = speed
        except ValueError:
            print("Invalid speed value")

    # Communication
    def eventStartXbee(self, port):
        return self.hermes.setup(port=port)

    def eventSendMessage(self, robotId, message):
        message = self.hermes.sendMessage(robotId, message)
        message[0] = (list(self.changeRobotLetters(None)).index(robotId), message[0][1])
        self.sigMessages.emit(message)

    def eventSetSkippedFrames(self, framesToSkip):
        self.framesToSkip = framesToSkip

    @staticmethod
    def ordenaWarp(points):
        WIDTH = 640
        HEIGHT = 480
        largura = WIDTH/2
        altura = HEIGHT/2
        pt1 = pt2 = pt3 = pt4 = None

        for i in range(0, 4, 1):
            if points[i][0] - largura < 0:
                if points[i][1] - altura < 0:
                    # Quadrante 1
                    pt1 = points[i]
                else:
                    # Quadrante 4
                    pt4 = points[i]
            else:
                if points[i][1] - altura < 0:
                    # Quadrante 2
                    pt2 = points[i]
                else:
                    # Quadrante 3
                    pt3 = points[i]

        return pt1, pt2, pt3, pt4
