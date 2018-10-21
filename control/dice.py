from math import sqrt, pow, atan2, pi, fmod, sin, tan, cos


def roundAngle(angle):
    """

    Args:
        angle:

    Returns:

    """

    theta = fmod(angle,  2 * pi)

    if theta > pi:
        theta = theta - (2 * pi)
    elif theta < -pi:
        theta = theta + (2 * pi)

    return theta


def saturate(value):
    """

    Args:
        value:

    Returns:

    """

    if value > 1:
        value = 1
    elif value < -1:
        value = -1

    return value


class Dice:
    """
    Attributes:
        velAcc (float):
        previouslyBackwards (boolean):
        maxThetaError (float):
    """

    def __init__(self):
        self.warrior = None
        self.velAcc = 0
        self.previouslyBackwards = False
        self.maxThetaError = roundAngle(20.0*pi/180)

    def run(self, warrior):
        """

        Args:
            warrior:

        Returns:

        """

        self.warrior = warrior
        self.warrior.vMax = round(self.warrior.vMax * 100) / 100

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
        """

        Args:
            warrior:

        Returns:

        """

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        if self.warrior.vMax == 0:
            return [0.0, 0.0]

        theta = float(atan2(sin(self.warrior.orientation - (-self.warrior.transAngle)),
                            cos(self.warrior.orientation - (-self.warrior.transAngle))) * 180 / pi)
        theta = round(theta * 100) / 100

        target = [50 * cos(theta * pi/180), 50 * sin(theta * pi/180)]
        targetTheta = atan2(target[1] - self.warrior.position[1], target[0] - self.warrior.position[0])

        theta = self.warrior.orientation
        moveBackwards = bool(abs(targetTheta - self.warrior.orientation) > pi/2)
        if moveBackwards:
            theta = roundAngle(self.warrior.orientation + pi)
        if moveBackwards != self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        thetaError = roundAngle(targetTheta - theta)

        if abs(thetaError) > self.maxThetaError:
            # !TODO arrumar o decremento de velocidade
            self.velAcc = self.velAcc - 0.2
        else:
            if self.velAcc < self.warrior.vMax:
                # !TODO arrumar o incremento de velocidade
                self.velAcc = self.velAcc + 0.1
            else:
                self.velAcc = self.warrior.vMax

        if moveBackwards:
            self.warrior.vLeft = -1 - sin(thetaError) + (-1 * tan(thetaError/2))
            self.warrior.vLeft = saturate(self.warrior.vLeft)

            self.warrior.vRight = -1 + sin(thetaError) + (-1 * tan(-1 * thetaError / 2))
            self.warrior.vRight = saturate(self.warrior.vRight)
        else:
            self.warrior.vLeft = 1 - sin(thetaError) + tan(-1 * thetaError / 2)
            self.warrior.vLeft = saturate(self.warrior.vLeft)

            self.warrior.vRight = 1 + sin(thetaError) + tan(thetaError / 2)
            self.warrior.vRight = saturate(self.warrior.vRight)

        return [self.warrior.vLeft*self.velAcc, self.warrior.vRight*self.velAcc]

    def positionControl(self):
        """

        Args:
            warrior:

        Returns:

        """

        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0]

        temp = [self.warrior.target[0] - self.warrior.position[0], self.warrior.target[1] - self.warrior.position[1]]
        transTarget = [round(cos(self.warrior.orientation) * (temp[0]) + sin(self.warrior.orientation) * temp[1]),
                       round(-(sin(self.warrior.orientation) * (temp[0]) + cos(self.warrior.orientation) * temp[1]))]
        target = [round(transTarget[0] * ((150.0/640.0)*100)/100), round(transTarget[1] * ((130.0/480.0)*100)/100)]

        # Stops after arriving at destination
        positionError = sqrt(pow(self.warrior.position[0] - target[0], 2) + pow(self.warrior.position[1] - target[1], 2))
        if positionError < 1:
            return [0.0, 0.0]

        if self.velAcc < 0.3:
            self.velAcc = 0.3

        targetTheta = atan2(target[1] - self.warrior.position[1], target[0] - self.warrior.position[0])
        theta = self.warrior.orientation

        # Activates backward movement if thetaError > PI/2
        moveBackwards = bool(roundAngle(targetTheta - self.warrior.orientation + pi/2) < 0)
        if moveBackwards is not self.previouslyBackwards:
            self.velAcc = 0.3

        self.previouslyBackwards = moveBackwards

        if moveBackwards:
            theta = roundAngle(self.warrior.orientation + pi)

        thetaError = roundAngle(targetTheta - theta)

        if abs(thetaError) > self.maxThetaError:
            if self.velAcc > self.warrior.vMax:
                self.velAcc = self.warrior.vMax
            elif self.velAcc > 0.3:
                self.velAcc = self.velAcc - 0.2
        else:
            difference = self.warrior.vMax - self.velAcc
            if difference > 0.2:
                # !TODO arrumar incremento de velocidade
                self.velAcc = self.velAcc + 0.2
            elif difference < 0:
                self.velAcc = self.warrior.vMax

        limiar = atan2(1.0, positionError)
        limiar = 30 if limiar > 30 else limiar

        if abs(thetaError < limiar):
            thetaError = 0

        if moveBackwards:
            self.warrior.vLeft = -1 - sin(thetaError) + (-1 * tan(thetaError/2))
            self.warrior.vLeft = saturate(self.warrior.vLeft)

            self.warrior.vRight = -1 + sin(thetaError) + (-1 * tan(-1 * thetaError / 2))
            self.warrior.vRight = saturate(self.warrior.vRight)
        else:
            self.warrior.vLeft = 1 - sin(thetaError) + tan(-1 * thetaError / 2)
            self.warrior.vLeft = saturate(self.warrior.vLeft)

            self.warrior.vRight = 1 + sin(thetaError) + tan(thetaError / 2)
            self.warrior.vRight = saturate(self.warrior.vRight)

        return [self.warrior.vLeft*self.velAcc, self.warrior.vRight*self.velAcc]

    def orientationControl(self):
        """

        Args:
            warrior:

        Returns:

        """

        targetTheta = self.warrior.orientation - (- self.warrior.targetOrientation)
        targetTheta = round((targetTheta * 180 / pi) * 100) / 100
        targetTheta = roundAngle(targetTheta * pi/180)

        theta = self.warrior.orientation

        # É necessário girar se estiver com a 'traseira' de frente pro alvo? (Se sim, não usar o if abaixo)
        if roundAngle(targetTheta - self.warrior.orientation + pi/2) < 0:
           theta = roundAngle(self.warrior.orientation + pi)

        thetaError = roundAngle(targetTheta - theta)

        if abs(thetaError) < 2*pi/180:
            return [0.0, 0.0]

        self.warrior.vLeft = saturate(0.8 * thetaError)
        self.warrior.vRight = saturate(-0.8 * thetaError)

        return [float(self.warrior.vLeft * self.warrior.vMax),
                float(self.warrior.vRight * self.warrior.vMax)]

    def speedControl(self):
        """

        Args:
            warrior:

        Returns:

        """

        return [float(round(self.warrior.vLeft * 100) / 100),
                float(round(self.warrior.vRight * 100) / 100)]
