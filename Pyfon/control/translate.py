import math
from .robot import Robot


class Translate:

    velAcc = 0
    previouslyBackwards = False

    def setup(self, robot):
        translate = Translate()

        if robot.get('cmdType') is None:
            return None

        if robot.get('cmdType') == 'UVF':
            return translate.uvfControl(robot)
        elif robot.get('cmdType') == 'VECTOR':
            return translate.vectorControl(robot)
        elif robot.get('cmdType') == 'POSITION':
            return translate.positionControl(robot)
        elif robot.get('cmdType') == 'ORIENTATION':
            return translate.orientationControl(robot)



    def uvfControl(self, robot):
        pass

    def vectorControl(self, robot):
        pass

    def positionControl(self, robot):
        T = Translate()
        positionError = math.sqrt(math.pow(self.robot[0].position - self.robot[0].target, 2) +
                                  math.pow(self.robot[1].position - self.robot[1].target, 2))

        if self.robot.vMax == 0 or positionError < 1:
            self.robot.vRight = 0
            self.robot.vLeft = 0

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        targetTheta = math.atan2(self.robot[1].target - self.robot[1].position,
                                 self.robot[0].target - self.robot[0].position)
        theta = self.robot.orientation
        moveBackwards = bool(T.roundAngle(targetTheta - self.robot.orientation) < 0)

        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = T.roundAngle(self.robot.orientation + math.pi)

        thetaError = T.roundAngle(targetTheta - theta)

        # To be continue...

    def orientationControl(self, robot):
        T = Translate()
        theta = robot.get('orientation')

        # !TODO É necessário girar se o robô estiver com a "traseira de frente pro alvo? (Se não, usar o if abaixo)
        '''
        if T.roundAngle(targetOrientation - orientation + math.pi/2) < 0:
           theta = T.roundAngle(orientation + math.pi)
        '''

        thetaError = T.roundAngle(robot.get('targetOrientation') - theta)

        if math.fabs(thetaError) < 2*math.pi/180:
            robot.set('vRight', 0)
            robot.set('vLeft', 0)
            robot.set('vMax', 0)

        robot.set('vRight', T.saturate(0.8 * thetaError))
        robot.set('vLeft', T.saturate(-0.8 * thetaError))

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
