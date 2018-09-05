from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    def setup(self, strategyInfo):
        robots = Zeus().getRobots(strategyInfo)
        robotsVelocity = Zeus().controlRoutine(robots)
        output = Zeus().generateOutput(robotsVelocity)

        return output

    def getRobots(self, strategyInfo):
        robots = []

        for r in range(0, len(strategyInfo)):
            robots.append(Robot())
            for key, value in strategyInfo[r].items():
                robots[r].set(key, value)

        return robots

    def generateOutput(self, velocitys):
        pass

    def controlRoutine(self, robots):
        actions = Actions()
        robotVelocity = []

        for robot in robots:
            if robot.action is not None:
                robotAction = actions.setup(robot)
            robotVelocity.append(Translate().setup(robotAction))

        return robotVelocity