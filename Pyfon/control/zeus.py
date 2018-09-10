from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    def __init__(self):
        self.robots = []
        self.actions = None
        self.translate = None
        print("Zeus summoned")

    def setup(self):
        self.actions = Actions()
        self.translate = Translate()

        for i in range(0, 3):
            self.robots.append(Robot())

        print("Zeus is set up")
        return self

    # Athena -> getVelocities -> Hermes
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
            info = strategia[x]["data"]
            self.robots[x].action.append(strategia[x]["command"])

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

    def controlRoutine(self):
        velocities = []
        for robot in self.robots:
            if robot.action is not None:
                velocities.append(self.translate.run(self.actions.run(robot)))

        return velocities

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


