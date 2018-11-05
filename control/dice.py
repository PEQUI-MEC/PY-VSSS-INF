from math import atan2, pi, sin, cos
from helpers import geometry
import numpy as np


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
        acc = 1 - \
              geometry.gaussian(np.linalg.norm(np.array(self.warrior.position) - np.array(self.warrior.target)), 8)

        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0, 0.0]

        theta = atan2(sin(self.warrior.transAngle), -cos(self.warrior.transAngle))
        target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]

        targetTheta = atan2((target[1] - self.warrior.position[1]) * 1.3 / 480,
                            -(target[0] - self.warrior.position[0]) * 1.5 / 640)
        currentTheta = atan2(sin(self.warrior.orientation), cos(self.warrior.orientation))

        if atan2(sin(targetTheta - currentTheta + pi / 2), -cos(targetTheta - currentTheta + pi / 2)) < 0:
            self.warrior.backward = True
            self.warrior.front = 1
        else:
            self.warrior.backward = False
            self.warrior.front = -1

        if self.warrior.backward:
            currentTheta = currentTheta + pi
            currentTheta = atan2(sin(currentTheta), -cos(currentTheta))

        thetaError = atan2(sin(targetTheta - currentTheta), -cos(targetTheta - currentTheta))

        left = self.warrior.front + sin(thetaError)
        right = self.warrior.front - sin(thetaError)

        left = geometry.saturate(left)
        right = geometry.saturate(right)

        left = self.warrior.vMax * left
        right = self.warrior.vMax * right

        return [left, right, self.warrior.transAngle]

    def positionControl(self):
        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0, 0.0]

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

        left = geometry.saturate(left)
        right = geometry.saturate(right)

        left = self.warrior.vMax * left
        right = self.warrior.vMax * right

        return [left, right, targetTheta]

    def orientationControl(self):
        targetTheta = self.warrior.targetOrientation
        theta = self.warrior.orientation

        # É necessário girar se estiver com a 'traseira' de frente pro alvo? (Se sim, não usar o if abaixo)
        if geometry.roundAngle(targetTheta - self.warrior.orientation + pi/2) < 0:
            theta = geometry.roundAngle(self.warrior.orientation + pi)

        thetaError = geometry.roundAngle(targetTheta - theta)

        if abs(thetaError) < 2*pi/180:
            return [0.0, 0.0, 0.0]

        self.warrior.vLeft = geometry.saturate(self.warrior.vMax * thetaError)
        self.warrior.vRight = geometry.saturate(-self.warrior.vMax * thetaError)
        return [self.warrior.vLeft * self.warrior.vMax, self.warrior.vRight * self.warrior.vMax, targetTheta]

    def speedControl(self):
        return [self.warrior.vLeft, self.warrior.vRight, 0]
