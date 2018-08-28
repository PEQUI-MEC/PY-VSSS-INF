from .actions import Actions
from .translate import Translate
from . import constants
import json

_robot_location = "database/robots.json"


class Zeus:
    robots = []

    def setup(self):
        if Zeus().getRobots():

            if Zeus().controlRoutine():
                return True
            else:
                return False

        else:
            return False

    def getRobots(self):
        __class__.robots = []
        with open(_robot_location, 'r') as file:
            __class__.robots = json.loads(file.read())
            file.close()
        if len(__class__.robots) == 0:
            return False
        else:
            return True

    def generateJson(self):
        pass

    def controlRoutine(self):
        counter = 0
        for robot in __class__.robots:
            if robot[constants._actionsCommand] is not None:
                robot = Actions().setup(robot)
                if robot:
                    counter = counter + 1
            # robot = Translate().mainTranslate(robot)

        if counter == 3:
            return True
        else:
            return False