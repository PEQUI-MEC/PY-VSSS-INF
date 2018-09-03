from .actions import Actions
from .translate import Translate
from .robot import Robot


class Zeus:
    # robots = []

    def setup(self, robots):
        # self.robots = robots
        # print(len(self.robots))
        return Zeus().controlRoutine(robots)

    def generateOutput(self):
        pass

    def controlRoutine(self, robots):
        actions = Actions()
        counter = 0

        for id in range(0, 3):
            robot = robots[id]
            if robot.get('actions') is not None:
                r = actions.setup(robots[id])
                if r:
                    counter = counter + 1
            # robot = Translate().mainTranslate(robot)

        if counter == 3:
            return True
        else:
            return False
