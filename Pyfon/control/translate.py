import math


class Translate:

    velAcc = 0
    previouslyBackwards = False

    def run(self, robot):
        if robot.cmdType is None:
            raise ValueError("CmdType isn't set.")

        if robot.cmdType == "VECTOR":
            return self.vectorControl(robot)
        elif robot.cmdType == "POSITION":
            return self.positionControl(robot)
        elif robot.cmdType == "ORIENTATION":
            return self.orientationControl(robot)
        elif robot.cmdType == "SPEED":
            return self.speedControl(robot)

    def vectorControl(self, robot):
        return [0.0, 0.0]

    def positionControl(self, robot):
        # Stops after arriving at destination
        positionError = math.sqrt(math.pow(robot.position[0] - robot.target[0], 2) +
                                  math.pow(robot.position[1] - robot.target[1], 2))
        if positionError < 1:
            robot.vLeft = 0
            robot.vRight = 0
            return [robot.vLeft, robot.Right]

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        # targetTheta in direction of [target.x, target.y]
        targetTheta = math.atan2(robot.target[1] - robot.position[1],
                                 robot.target[0] - robot.position[0])
        theta = robot.orientation

        # Activates backward movement if thetaError > PI/2
        moveBackwards = bool(self.roundAngle(targetTheta - robot.orientation + math.pi/2) < 0)
        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = self.roundAngle(robot.orientation + math.pi)

        thetaError = self.roundAngle(targetTheta - theta)

        # To be continue...
        return [0.0, 0.0]

    def orientationControl(self, robot):
        theta = robot.orientation

        # !TODO É necessário girar se o robô estiver com a "traseira de frente pro alvo? (Se sim, não usar o if abaixo)
        if self.roundAngle(robot.targetOrientation - robot.orientation + math.pi/2) < 0:
           theta = self.roundAngle(robot.orientation + math.pi)

        thetaError = self.roundAngle(robot.targetOrientation - theta)

        if math.fabs(thetaError) < 2*math.pi/180:
            robot.vRight = 0
            robot.vLeft = 0
            robot.vMax = 0

        robot.vLeft = self.saturate(-robot.vMax * thetaError)
        robot.vRight = self.saturate(robot.vMax * thetaError)

        return [float(robot.vLeft), float(robot.vRight)]

    def speedControl(self, robot):
        return [float(robot.vLeft), float(robot.vRight)]

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
            value = -1

        return value
