from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    def __init__(self, callback=None):
        print("Zeus summoned")
        self.callback = callback

    def setup(self, strategyInfo):
        robots = Zeus().getRobots(strategyInfo)
        robotsVelocity = Zeus().controlRoutine(robots)
        output = Zeus().generateOutput(robotsVelocity)
        print(robotsVelocity)

        # self.callback(output)

    def getRobots(self, strategyInfo):
        robots = []

        for r in range(0, len(strategyInfo)):
            robots.append(Robot())
            for key, value in strategyInfo[r].items():
                robots[r].set(key, value)

        return robots

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

    def controlRoutine(self, robots):
        actions = Actions()
        robotVelocity = []

        for robot in robots:
            if robot.action is not None:
                robotAction = actions.setup(robot)
            robotVelocity.append(Translate().setup(robotAction))

        return robotVelocity
