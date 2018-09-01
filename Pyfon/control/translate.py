from . import constants as r
import math


class Translate:

    robot = []
    velAcc = 0
    previouslyBackwards = False

    @staticmethod
    def setup(robot):
        translate = Translate()
        translate.robot = robot

        if robot[r._cmdType] is None:
            return None

        if robot[r._cmdType] == 'UVF':
            translate.uvfControl()
        elif robot[r._cmdType] == 'VECTOR':
            translate.vectorControl()
        elif robot[r._cmdType] == 'POSITION':
            translate.positionControl()
        elif robot[r._cmdType] == 'ORIENTATION':
            translate.orientationControl()

        return [robot[r._vRight], robot[r._vLeft]]

    def uvfControl(self):
        pass

    def vectorControl(self):
        pass

    def positionControl(self):
        T = Translate()
        positionError = math.sqrt(math.pow(self.robot[r._position][0] - self.robot[r._target][0], 2) +
                                  math.pow(self.robot[r._position][1] - self.robot[r._target][1], 2))

        if self.robot[r._vMax] == 0 or positionError < 1:
            self.robot[r._vRight] = 0
            self.robot[r._vLeft] = 0

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        targetTheta = math.atan2(self.robot[r._target][1] - self.robot[r._position][1],
                                 self.robot[r._target][0] - self.robot[r._position][0])
        theta = self.robot[r._orientation]
        moveBackwards = bool(T.roundAngle(targetTheta - self.robot[r._orientation]) < 0)

        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = T.roundAngle(self.robot[r._orientation] + math.pi)

        thetaError = T.roundAngle(targetTheta - theta)

        # To be continue...

    def orientationControl(self):
        T = Translate()
        theta = self.robot[r._orientation]

        # !TODO É necessário girar se o robô estiver com a "traseira de frente pro alvo? (Se não, usar o if abaixo)
        '''
        if T.roundAngle(targetOrientation - orientation + math.pi/2) < 0:
           theta = T.roundAngle(orientation + math.pi)
        '''

        thetaError = T.roundAngle(self.robot[r._targetOrientation] - theta)

        if math.fabs(thetaError) < 2*math.pi/180:
            self.robot[r._vRight] = 0
            self.robot[r._vLeft] = 0
            self.robot[r._vMax] = 0

        self.robot[r._vRight] = T.saturate(0.8 * thetaError)
        self.robot[r._vLeft] = T.saturate(-0.8 * thetaError)

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
