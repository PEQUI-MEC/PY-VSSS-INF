from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    def setup(self, strategyInfo):
        robots = Zeus().getRobots(strategyInfo)
        robotsVelocity = Zeus().controlRoutine(robots)
        output = Zeus().generateOutput(robotsVelocity)
        print(robotsVelocity)

    def getRobots(self, strategyInfo):
        robots = []

        for r in range(0, len(strategyInfo)):
            robots.append(Robot())
            for key, value in strategyInfo[r].items():
                robots[r].set(key, value)

        return robots

    def generateOutput(self, velocitys):
        output = [
            {
                "vLeft": velocitys[0][0],
                "vRight": velocitys[0][1]
            },
            {
                "vLeft": velocitys[1][0],
                "vRight": velocitys[1][1]
            },
            {
                "vLeft": velocitys[2][0],
                "vRight": velocitys[2][1]
            }
        ]

        return output

    def controlRoutine(self, robots):
        actions = Actions()
        robotVelocity = []

        for robot in robots:
            if robot.action is not None:
                robotAction = actions.setup(robot)
            robotVelocity.append(Translate().setup(robotAction))

        return robotVelocity