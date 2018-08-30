from .actions import Actions
from .translate import Translate
from . import constants
import json

_robot_location = "database/robots.json"


class Zeus:
    robots = []

    def setup(self):
        zeus = Zeus()
        zeus.robots = zeus.getRobots()

        return zeus.controlRoutine()

    @staticmethod
    def getRobots():
        robots = []

        with open(_robot_location, 'r') as file:
            robots = json.loads(file.read())
            file.close()
        if len(robots) == 0:
            return FileNotFoundError
        else:
            return robots

    def generateJson(self):
        pass

    def controlRoutine(self):
        robotActions = Actions()
        counter = 0

        for robot in self.robots:
            if robot[constants._actionsCommand] is not None:
                robot = robotActions.setup(robot)

                if robot:
                    counter = counter + 1
            # robot = Translate().mainTranslate(robot)

        if counter == 3:
            return True
        else:
            return False
