from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    '''
    Seleciona ações de baixo nível baseado na tática
    Ações que podem ser escolhidas:
    - "goTo": {
            "pose": {
                "position": (x, y),
                "orientation": θ radianos
            },
            "target": {
                "position": (x, y),
                "orientation": θ radianos | (x, y),  # opcional - pode ser uma orientação final ou uma posição de lookAt
            }
            "velocity": X m/s,  # opcional, não será usado com o 'before'
            "before": X s,
        }
    - "spin": {
            "velocity": X m/s,
            "direction": "clockwise" | "counter"
        }
    - "lookAt": {
            "pose": {
                "position": (x, y),
                "orientation": θ radianos
            }, # opcional - é passado se o target for um ponto
            "target": θ radianos | (x, y)
        }
    '''

    def __init__(self, callback=None):
        self.demigod = []
        self.actions = None
        self.translate = None
        print("Zeus summoned")

        self.callback = callback

    def setup(self):
        self.actions = Actions()
        self.translate = Translate()

        for i in range(0, 3):
            self.demigod.append(Robot())

        print("Zeus is set up")
        return self

    def run(self, strategia):
        self.getRobots(strategia)
        velocities = self.controlRoutine()
        output = self.generateOutput(velocities)

        for robot in self.demigod:
            robot.targetOrientation = None

        if self.callback is not None:
            self.callback(output)
        else:
            return output

    def getRobots(self, strategia):

        for x in range(0, len(strategia)):
            info = strategia[x]["data"]
            self.demigod[x].action.append(strategia[x]["command"])

            if strategia[x]["command"] == "goTo":
                self.demigod[x].position = info["pose"]["position"]
                self.demigod[x].orientation = info["pose"]["orientation"]

                self.demigod[x].target = info["target"]["position"]
                self.demigod[x].targetOrientation = info["target"]["orientation"]

                self.demigod[x].vMax = info["velocity"]

                if "before" in info:
                    self.demigod[x].action.append(int(info["before"]))

            elif strategia[x]["command"] == "spin":
                self.demigod[x].vMax = info["velocity"]
                self.demigod[x].action.append(info["direction"])

            elif strategia[x]["command"] == "lookAt":
                self.demigod[x].orientation = info["pose"]["orientation"]
                if type(info["target"]) == type(float):
                    self.demigod[x].targetOrientation = info["target"]
                    self.demigod[x].action.append(info["orientation"])
                else:
                    self.demigod[x].position = info["pose"]["position"]
                    self.demigod[x].target = info["target"]
                    self.demigod[x].action.append(info["orientation"])

        return self.demigod

    def generateOutput(self, velocities):
        output = [
            {
                "vLeft": velocities[0][0],
                "vRight": velocities[0][1]
            },
            {
                "vLeft": velocities[1][0],
                "vRight": velocities[1][1]
            },
            {
                "vLeft": velocities[2][0],
                "vRight": velocities[2][1]
            }
        ]

        return output

    def controlRoutine(self):
        velocities = []

        for robot in self.demigod:
            if robot.action is not None:
                robotAction = self.actions.run(robot)
                velocities.append(self.translate.run(robotAction))

        return velocities
