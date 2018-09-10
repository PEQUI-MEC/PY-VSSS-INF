from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    def __init__(self):
        self.robots = []
        self.actions = None
        self.translate = None
        print("Zeus summoned")

    # Setup Zeus: nRobots is the num of robots in game
    def setup(self, nRobots):
        self.actions = Actions()
        self.translate = Translate()

        for i in range(0, nRobots):
            self.robots.append(Robot())

        print("Zeus is set up")
        return self

    # Athena -> getVelocities -> Hermes
    # Hermes(Zeus.getVelocities(Athena))
    def getVelocities(self, strategia):
        self.getRobots(strategia)
        return self.generateOutput(self.controlRoutine())

    def getRobots(self, strategia):
        if type(strategia) is not list or \
                type(strategia[0]) is not dict or\
                type(strategia[1]) is not dict or \
                type(strategia[2]) is not dict:
            raise ValueError("Invalid data object received.")

        for x in range(0, len(strategia)):
            self.robots[x].action.append(strategia[x]["command"])
            info = strategia[x]["data"]

            if strategia[x]["command"] == "goTo":
                self.robots[x].position = info["pose"]["position"]
                self.robots[x].orientation = info["pose"]["orientation"]

                self.robots[x].target = info["target"]["position"]
                self.robots[x].targetOrientation = info["target"]["orientation"]

                self.robots[x].vMax = info["velocity"]

                if "before" in info:
                    self.robots[x].action.append(int(info["before"]))

            elif strategia[x]["command"] == "spin":
                self.robots[x].vMax = info["velocity"]
                self.robots[x].action.append(info["direction"])

            elif strategia[x]["command"] == "lookAt":
                self.robots[x].orientation = info["pose"]["orientation"]
                if type(info["target"]) is float:
                    self.robots[x].targetOrientation = info["target"]
                    self.robots[x].action.append("orientation")
                else:
                    self.robots[x].position = info["pose"]["position"]
                    self.robots[x].target = info["target"]
                    self.robots[x].action.append("target")

        return self.robots

    # Cálculos necessarios para gerar os pwm's
    def controlRoutine(self):
        velocities = []
        for robot in self.robots:
            if len(robot.action) > 0:
                velocities.append(self.translate.run(self.actions.run(robot)))
            else:
                # !TODO estudar comando raise ValueError. Usar ele aqui ou apenas passar velocidades Nnone?
                print("No action command was set.")
                velocities.append([None, None])

        return velocities

    # Gera lista de dicionários com as velocidades de cada robô
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


