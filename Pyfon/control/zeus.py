from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:

    def __init__(self, callback=None):
        self.robots = []
        self.actions = None
        self.translate = None
        print("Zeus summoned")

        self.callback = callback

    def setup(self):
        self.actions = Actions()
        self.translate = Translate()

        for i in range(0, 3):
            self.robots.append(Robot())

        print("Zeus is set up")
        return self

    def run(self, strategyInfo):
        self.getRobots(strategyInfo)
        velocities = self.controlRoutine()
        output = self.generateOutput(velocities)

        for robot in self.robots:
            robot.targetOrientation = None

        if self.callback is not None:
            self.callback(output)
        else:
            return output

    def getRobots(self, strategyInfo):
        for r in range(0, len(strategyInfo)):
            for key, value in strategyInfo[r].items():
                self.robots[r].set(key, value)
        return self.robots

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

        for robot in self.robots:
            if robot.action is not None:
                robotAction = self.actions.run(robot)
                velocities.append(self.translate.run(robotAction))

        return velocities
