from . import constants
import math


class Translate:

    robot = []

    @staticmethod
    def setup(robot):
        translate = Translate()
        translate.robot = robot

        if robot[constants._cmdType] is None:
            return None

        if robot[constants._cmdType] == 'UVF':
            translate.uvfControl()
        elif robot[constants._cmdType] == 'VECTOR':
            translate.vectorControl()
        elif robot[constants._cmdType] == 'POSITION':
            translate.positionControl()
        elif robot[constants._cmdType] == 'ORIENTATION':
            translate.orientationControl()

        return [robot[constants._vRight], robot[constants._vLeft]]

    def uvfControl(self):
        pass

    def vectorControl(self):
        pass

    def positionControl(self):
        positionError = math.sqrt(math.pow(self.robot[constants._position][0] - self.robot[constants._target][0], 2) +
                                  math.pow(self.robot[constants._position][1] - self.robot[constants._target][1], 2))

        if self.robot[constants._vMax] == 0 or positionError < 1:
            self.robot[constants._vRight] = 0
            self.robot[constants._vLeft] = 0

        # To be continue...



    def orientationControl(self):
        T = Translate()
        theta = self.robot[constants._orientation]

        # !TODO É necessário girar se o robô estiver com a "traseira de frente pro alvo? (Se não, usar o if abaixo)
        '''
        if T.roundAngle(targetOrientation - orientation + math.pi/2) < 0:
           theta = T.roundAngle(orientation + math.pi)
        '''

        thetaError = T.roundAngle(self.robot[constants._targetOrientation] - theta)

        if math.fabs(thetaError) < 2*math.pi/180:
            self.robot[constants._vRight] = 0
            self.robot[constants._vLeft] = 0
            self.robot[constants._vMax] = 0

        self.robot[constants._vRight] = T.saturate(0.8 * thetaError)
        self.robot[constants._vLeft] = T.saturate(-0.8 * thetaError)

    @staticmethod
    def roundAngle(angle):
        theta = math.fmod(angle,  2 * math.pi)

        if theta > math.pi:
            theta = theta - (2 * math.pi)
        elif theta < -math.pi:
            theta = theta + (2 * math.pi)

        return theta

    @staticmethod
    def saturate(value):
        if value > 1:
            value = 1
        elif value < -1:
            value = -1;

        return value
