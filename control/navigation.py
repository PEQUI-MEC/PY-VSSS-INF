from math import pi, atan2, sin, cos, sqrt
from helpers import geometry
import numpy as np

# TODO Documentar tudo


class HyperbolicSpiral:
    def __init__(self):
        self.kr = None
        self.radius = None
        self.target = None

    def updateParams(self, kr, radius):
        self.kr = kr
        self.radius = radius

    def updateTarget(self, target):
        self.target = np.array(target)

    def hyperbolic(self, position, r=None, clockwise=True):
        if r is None:
            radius = self.radius
        else:
            radius = r

        # theta = angle(p, self.origin) - (self.orientation - angle(p, self.origin))
        theta = atan2(position[1], position[0])
        # print(": Theta: " + str(theta))

        ro = np.linalg.norm(position - self.target)
        if ro > radius:
            spiral = (pi / 2.0) * (2.0 - (radius + self.kr) / (ro + self.kr))
        else:
            spiral = (pi / 2.0) * sqrt(ro / radius)

        if clockwise:
            spiral = geometry.wrap2pi(theta + spiral)
            return atan2(sin(spiral), cos(spiral))
        else:
            spiral = geometry.wrap2pi(theta - spiral)
            return atan2(sin(spiral), cos(spiral))


class Repulsive:
    def __init__(self):
        self.origin = None

    def updateOrigin(self, newOrigin):
        self.origin = newOrigin

    def repulsive(self, p, origin=None, theta=True):
        if origin is not None:
            self.updateOrigin(origin)

        position = np.array(p) - self.origin
        if theta is True:
            return atan2(position[1], -position[0])
        else:
            return position


class Move2Goal:

    def __init__(self):
        self.kr = None
        self.radius = None

        self.target = None

        self.x = None
        self.y = None
        self.orientation = 1
        self.rotation = True
        self.toUnivector = None
        self.toGame = None

        self.hyperSpiral = HyperbolicSpiral()

    def updateParams(self, kr, radius):
        self.kr = kr
        self.radius = radius
        self.hyperSpiral.updateParams(self.kr, self.radius)

    def updateTarget(self, target, orientation):
        self.target = np.array(target)
        self.orientation = np.array(orientation)
        self.hyperSpiral.updateTarget(target)

        self.buildAxis(target, orientation)

    def updateOrientation(self, orientation):
        self.orientation = np.array(orientation)

    def buildAxis(self, orientation, target):
        print(orientation, target)
        if type(orientation) != int and self.rotation is True:
            # print("Orientation ", self.orientation, " Origin ", self.target)
            self.x = np.array(np.array(orientation) - np.array(target), dtype=np.float32)
        else:
            if orientation == 1:
                self.x = [1.0, 0.0]
            else:
                self.x = [-1.0, 0.0]

        print(self.x)
        self.x /= -np.linalg.norm(self.x)

        theta = atan2(self.x[1], self.x[0])
        self.y = [sin(theta), cos(theta)]

        # print("X: ", self.x, " theta: ", theta, " y: ", self.y)
        self.toGame = np.array([self.x, self.y]).T
        self.toUnivector = np.linalg.inv(self.toGame)

    def fi_tuf(self, p):
        position = np.array(p) - self.target
        position = np.dot(self.toUnivector, position).reshape(2, )
        x, y = position
        yl = y + self.radius
        yr = y - self.radius

        pl = np.array([x, yr])
        pr = np.array([x, yl])

        if -self.radius <= y < self.radius:
            nhCounterClockwise = self.hyperSpiral.hyperbolic(pl, clockwise=False)
            nhCounterClockwise = np.array([cos(nhCounterClockwise), sin(nhCounterClockwise)])

            nhClockwise = self.hyperSpiral.hyperbolic(pr, clockwise=True)
            nhClockwise = np.array([cos(nhClockwise), sin(nhClockwise)])

            movement = (abs(yl) * nhCounterClockwise + abs(yr) * nhClockwise) / (2.0 * self.radius)
            movement = np.dot(self.toGame, movement).reshape(2, )

        else:
            if y < -self.radius:
                theta = self.hyperSpiral.hyperbolic(pl, clockwise=True)
            else:
                theta = self.hyperSpiral.hyperbolic(pr, clockwise=False)

            # No artigo aqui ele só usa o theta
            movement = np.array([cos(theta), sin(theta)])
            movement = np.dot(self.toGame, movement).reshape(2, )

        return atan2(movement[1], -movement[0])


class AvoidObstacle:
    def __init__(self):
        self.repulsive = Repulsive()
        self.obstaclePos = None
        self.obstacleSpeed = None
        self.robotPos = None
        self.robotSpeed = None
        self.k0 = None

    def updateParam(self, k0):
        self.k0 = k0

    def updateRobot(self, robotPos, robotSpeed):
        self.robotPos = np.array(robotPos)
        self.robotSpeed = np.array(robotSpeed)

    def updateObstacle(self, obstaclePos, obstacleSpeed):
        self.obstaclePos = np.array(obstaclePos)
        self.obstacleSpeed = np.array(obstacleSpeed)

    def getVirtualPos(self):
        s = np.linalg.norm(self.k0 * (self.obstacleSpeed - self.robotSpeed))
        distanceBetween = np.linalg.norm(self.obstaclePos - self.robotPos)
        if distanceBetween >= s:
            virtualPos = (self.k0 * (self.obstacleSpeed - self.robotSpeed)) + self.obstaclePos
        else:
            virtualPos = ((distanceBetween / s) * (self.k0 * (self.obstacleSpeed - self.robotSpeed))) + self.obstaclePos

        return virtualPos

    def avoid(self, robotPos, vPos=None, theta=True):
        if vPos is None:
            virtualPos = self.getVirtualPos()
        else:
            virtualPos = vPos
        return self.repulsive.repulsive(robotPos, origin=virtualPos, theta=theta)


class UnivectorField:
    def __init__(self):
        self.radius = None
        self.kr = None
        self.k0 = None
        self.dMin = None
        self.lDelta = None

        self.obstacles = None
        self.obstaclesSpeed = None
        self.robotPos = None
        self.robotSpeed = None

        self.moveField = Move2Goal()
        self.avoidField = AvoidObstacle()

    def updateConstants(self, radius, kr, k0, dMin, lDelta):
        self.radius = radius
        self.kr = kr
        self.k0 = k0
        self.dMin = dMin
        self.lDelta = lDelta

        self.avoidField.updateParam(self.k0)
        self.moveField.updateParams(self.kr, self.radius)

    def updateRobot(self, robotPos, robotSpeed):
        self.robotPos = np.array(robotPos)
        self.robotSpeed = np.array(robotSpeed)

        self.avoidField.updateRobot(self.robotPos, self.robotSpeed)

    def updateTarget(self, targetPos, orientation):
        self.moveField.updateTarget(targetPos, orientation)

    def updateObstacles(self, obstacles, obstacleSpeeds):
        self.obstacles = np.array(obstacles)
        self.obstaclesSpeed = np.array(obstacleSpeeds)

    def univector(self, robotPos=None, robotSpeed=None, target=None, obstacles=None, ostaclesSpeed=None, orientation=None):
        if robotPos is not None and robotSpeed is not None:
            self.updateRobot(robotPos, robotSpeed)
        if target is not None:
            if orientation is None:
                orientation = [650, 250]
            self.updateTarget(target, orientation)
        if obstacles is not None:
            if ostaclesSpeed is None:
                ostaclesSpeed = [0.0, 0.0]
            self.updateObstacles(obstacles, ostaclesSpeed)

        centers = []
        fi_auf = 0.0
        minDistance = self.dMin + 1
        self.obstacles = None
        if self.obstacles is not None:
            for i in range(0, len(self.obstacles)):
                self.avoidField.updateObstacle(self.obstacles[i], self.obstaclesSpeed[i])
                center = self.avoidField.getVirtualPos()
                centers.append(center)

            centers = np.asarray(centers)
            distVect = np.linalg.norm(np.subtract(centers, self.robotPos), axis=1)
            index = np.argmin(distVect)
            closestCenter = centers[index]
            minDistance = distVect[index]

            fi_auf = self.avoidField.avoid(self.robotPos, vPos=closestCenter, theta=True)

        if minDistance <= self.dMin:
            # print("Obstaculo!!!")
            return fi_auf
        else:
            fi_tuf = self.moveField.fi_tuf(self.robotPos)

            if self.obstacles is not None:
                guass = geometry.gaussian(minDistance - self.dMin, self.lDelta)
                diff = geometry.wrap2pi(fi_auf - fi_tuf)
                return geometry.wrap2pi(guass*diff + fi_tuf)

            else:
                return fi_tuf
