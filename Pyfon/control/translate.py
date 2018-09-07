import math
from .robot import Robot


class Translate:

    velAcc = 0
    previouslyBackwards = False

    def setup(self, robot):
        translate = Translate()

        if robot.cmdType is None:
            return None

        if robot.cmdType == 'UVF':
            return translate.uvfControl(robot)
        elif robot.cmdType == 'VECTOR':
            return translate.vectorControl(robot)
        elif robot.cmdType == 'POSITION':
            return translate.positionControl(robot)
        elif robot.cmdType == 'ORIENTATION':
            return translate.orientationControl(robot)
        elif robot.cmdType == "SPEED":
            return translate.speedControl(robot)

    def uvfControl(self, robot):
        pass

    def vectorControl(self, robot):
        pass

    def positionControl(self, robot):
        T = Translate()
        positionError = math.sqrt(math.pow(robot.position[0] - robot.target[0], 2) +
                                  math.pow(robot.position[1] - robot.target[1], 2))

        if robot.vMax == 0 or positionError < 1:
            robot.vRight = 0
            robot.vLeft = 0

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        targetTheta = math.atan2(robot.target[1] - robot.position[1],
                                 robot.target[0] - robot.position[0])
        theta = robot.orientation
        moveBackwards = bool(T.roundAngle(targetTheta - robot.orientation) < 0)

        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = T.roundAngle(robot.orientation + math.pi)

        thetaError = T.roundAngle(targetTheta - theta)

        # To be continue...
        pass

    def orientationControl(self, robot):
        T = Translate()
        theta = robot.orientation

        # !TODO É necessário girar se o robô estiver com a "traseira de frente pro alvo? (Se não, usar o if abaixo)
        '''
        if T.roundAngle(targetOrientation - orientation + math.pi/2) < 0:
           theta = T.roundAngle(orientation + math.pi)
        '''

        thetaError = T.roundAngle(robot.targetOrientation - theta)

        if math.fabs(thetaError) < 2*math.pi/180:
            robot.vRight = 0
            robot.vLeft = 0
            robot.vMax = 0

        robot.vLeft = T.saturate(-0.8 * thetaError)
        robot.vRight = T.saturate(0.8 * thetaError)

        return [float(robot.vLeft), float(robot.vRight)]

    def speedControl(self, robot):

        return [float(robot.vMax), float(robot.vMax)]


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
