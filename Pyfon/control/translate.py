from math import sqrt, pow, atan2, pi, fmod, fabs


def roundAngle(angle):
    theta = fmod(angle,  2 * pi)

    if theta > pi:
        theta = theta - (2 * pi)
    elif theta < -pi:
        theta = theta + (2 * pi)

    return theta


def saturate(value):
    if value > 1:
        value = 1
    elif value < -1:
        value = -1

    return value


class Translate:
    # TODO(Luana) Defirnir um nome final para Translate e documentá-lo

    def __init__(self):
        self.velAcc = 0
        self.previouslyBackwards = False

    def run(self, warrior):

        if warrior.cmdType == "VECTOR":
            return self.vectorControl(warrior)
        elif warrior.cmdType == "POSITION":
            return self.positionControl(warrior)
        elif warrior.cmdType == "ORIENTATION":
            return self.orientationControl(warrior)
        elif warrior.cmdType == "SPEED":
            return self.speedControl(warrior)
        else:
            raise ValueError("Invalid cmdType")

    def vectorControl(self, warrior):

        return [0.0, 0.0]

    def positionControl(self, warrior):
        # Stops after arriving at destination
        positionError = sqrt(pow(warrior.position[0] - warrior.target[0], 2) +
                                  pow(warrior.position[1] - warrior.target[1], 2))
        if positionError < 1:
            warrior.vLeft = 0
            warrior.vRight = 0
            return [warrior.vLeft, warrior.Right]

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        # targetTheta in direction of [target.x, target.y]
        targetTheta = atan2(warrior.target[1] - warrior.position[1],
                                 warrior.target[0] - warrior.position[0])
        theta = warrior.orientation

        # Activates backward movement if thetaError > PI/2
        moveBackwards = bool(roundAngle(targetTheta - warrior.orientation + pi/2) < 0)
        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = roundAngle(warrior.orientation + pi)

        thetaError = roundAngle(targetTheta - theta)

        # To be continue...
        # TODO(Luana) Terminar calculos. Levar em consideração theta_error?

        return [0.0, 0.0]

    def orientationControl(self, warrior):
        theta = warrior.orientation

        # TODO(Luana) É necessário girar se estiver com a 'traseira' de frente pro alvo? (Se sim, não usar o if abaixo)
        if roundAngle(warrior.targetOrientation - warrior.orientation + pi/2) < 0:
           theta = roundAngle(warrior.orientation + pi)

        thetaError = roundAngle(warrior.targetOrientation - theta)

        if fabs(thetaError) < 2*pi/180:
            warrior.vRight = 0
            warrior.vLeft = 0
            warrior.vMax = 0

        warrior.vLeft = saturate(-warrior.vMax * thetaError)
        warrior.vRight = saturate(warrior.vMax * thetaError)

        return [float(warrior.vLeft), float(warrior.vRight)]

    def speedControl(self, warrior):
        if warrior.vLeft is None or warrior.vRight is None:
            return [float(warrior.vMax), float(warrior.vMax)]

        return [float(warrior.vLeft), float(warrior.vRight)]
