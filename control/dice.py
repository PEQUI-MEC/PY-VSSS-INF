from math import atan2, pi, fmod, sin, cos


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


class Dice:
    def __init__(self):
        self.warrior = None

    def run(self, warrior):
        self.warrior = warrior

        if warrior.cmdType == "VECTOR":
            return self.vectorControl()
        elif warrior.cmdType == "POSITION":
            return self.positionControl()
        elif warrior.cmdType == "ORIENTATION":
            return self.orientationControl()
        elif warrior.cmdType == "SPEED":
            return self.speedControl()
        else:
            raise ValueError("Invalid cmdType")

    def vectorControl(self):
        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0]

        theta = atan2(sin(self.warrior.transAngle), -cos(self.warrior.transAngle))
        target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]

        targetTheta = atan2(target[1] - self.warrior.position[1], -(target[0] - self.warrior.position[0]))
        currentTheta = atan2(sin(self.warrior.orientation), cos(self.warrior.orientation))

        '''
        if atan2(sin(targetTheta - currentTheta + pi / 2), cos(targetTheta - currentTheta + pi / 2)) < 0:
            self.warrior.backward = True
            self.warrior.front = 1
            # currentTheta = currentTheta + pi
            # currentTheta = atan2(sin(currentTheta), cos(currentTheta))

        else:
            self.warrior.backward = False
            self.warrior.front = -1
        '''

        thetaError = atan2(sin(targetTheta - currentTheta), cos(targetTheta - currentTheta))

        left = self.warrior.front + sin(thetaError)
        right = self.warrior.front - sin(thetaError)

        left = saturate(left)
        right = saturate(right)

        left = self.warrior.vMax * left
        right = self.warrior.vMax * right

        if self.warrior.name == "huguinho":
            # print(self.warrior.position)
            print("Orientation: ", self.warrior.orientation, "Current: ", currentTheta, " Target: ", targetTheta)

        return [left, right]

    def positionControl(self):
        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0]

        targetTheta = atan2((self.warrior.target[1] - self.warrior.position[1])*1.3 / 480,
                            -(self.warrior.target[0] - self.warrior.position[0])*1.5 / 640)
        currentTheta = atan2(sin(self.warrior.orientation), cos(self.warrior.orientation))

        if atan2(sin(targetTheta - currentTheta + pi/2), cos(targetTheta - currentTheta + pi/2)) < 0:
            self.warrior.backward = True
            self.warrior.front = 1
        else:
            self.warrior.backward = False
            self.warrior.front = -1

        if self.warrior.backward:
            currentTheta = currentTheta + pi
            currentTheta = atan2(sin(currentTheta), cos(currentTheta))

        thetaError = atan2(sin(targetTheta - currentTheta), cos(targetTheta - currentTheta))

        left = self.warrior.front + sin(thetaError)
        right = self.warrior.front - sin(thetaError)

        left = saturate(left)
        right = saturate(right)

        left = self.warrior.vMax * left
        right = self.warrior.vMax * right

        return [left, right]

    def orientationControl(self):
        targetTheta = self.warrior.targetOrientation
        theta = self.warrior.orientation

        # É necessário girar se estiver com a 'traseira' de frente pro alvo? (Se sim, não usar o if abaixo)
        if roundAngle(targetTheta - self.warrior.orientation + pi/2) < 0:
            theta = roundAngle(self.warrior.orientation + pi)

        thetaError = roundAngle(targetTheta - theta)

        if abs(thetaError) < 2*pi/180:
            return [0.0, 0.0]

        self.warrior.vLeft = saturate(0.8 * thetaError)
        self.warrior.vRight = saturate(-0.8 * thetaError)

        return [self.warrior.vLeft * self.warrior.vMax, self.warrior.vRight * self.warrior.vMax]

    def speedControl(self):
        return [self.warrior.vLeft, self.warrior.vRight]
