from . import constants
import math


class Translate:

    robot = []

    @staticmethod
    def setup(robot):
        translate = Translate()
        translate.robot = robot

        if robot[constants._cmdType] == 'UVF':
            translate.uvfControl()
        elif robot[constants._cmdType] == 'VECTOR':
            translate.vectorControl()
        elif robot[constants._cmdType] == 'POSITION':
            translate.positionControl()
        elif robot[constants._cmdType] == 'ORIENTATION':
            translate.orientationControl()

        elif robot[constants._cmdType] is None:
            return None

        return [robot[constants._vRight], robot[constants._vLeft]]

    def uvfControl(self):
        pass

    def vectorControl(self):
        pass

    def positionControl(self):
        pass

    def orientationControl(self):
        pass

    def speedControl(self):
        pass
