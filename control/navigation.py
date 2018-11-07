from math import pi, atan2, sin, cos, sqrt
from helpers import geometry
import numpy

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
        self.target = target

    def hyperbolic(self, position, r=None, clockwise=True):
        if r is None:
            radius = self.radius
        else:
            radius = r

        ro = numpy.linalg.norm(position - self.target)
        if ro > radius:
            spiral = (pi / 2.0) * (2.0 - (radius + self.kr) / (ro + self.kr))
        else:
            spiral = (pi / 2.0) * sqrt(ro / radius)

        theta = atan2(position[1], position[0])
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

        position = numpy.asarray(p, dtype=float) - self.origin
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
        self.toUnivector = None
        self.toGame = None

        self.hyperSpiral = HyperbolicSpiral()

    def updateParams(self, kr, radius):
        self.kr = kr
        self.radius = radius
        self.hyperSpiral.updateParams(self.kr, self.radius)

    def updateTarget(self, target, orientation):
        self.target = numpy.asarray(target, dtype=float)
        self.orientation = numpy.asarray(orientation, dtype=float)
        self.hyperSpiral.updateTarget(self.target)

        self.buildAxis(self.target, self.orientation)

    def buildAxis(self, orientation, target):
        if type(self.orientation) is int:
            self.x = numpy.asarray([1.0, 0.0], dtype=float)
        else:
            self.x = numpy.asarray(numpy.asarray(orientation, dtype=float)
                                   - numpy.asarray(target, dtype=float), dtype=float)
            if self.x.all() == 0.0:
                self.x = numpy.asarray([1.0, 0.0], dtype=float)

        # self.x = self.x / (-numpy.linalg.norm(self.x))
        self.x = self.x / (-numpy.sqrt(self.x.dot(self.x)))
        theta = atan2(self.x[1], self.x[0])
        self.y = [sin(theta), cos(theta)]

        self.toGame = numpy.asarray([self.x, self.y], dtype=float).T
        self.toUnivector = numpy.linalg.inv(self.toGame)

    def fi_tuf(self, p):
        position = numpy.asarray(p, dtype=float) - self.target
        position = numpy.dot(self.toUnivector, position).reshape(2, )
        x, y = position
        yl = y + self.radius
        yr = y - self.radius
        pl = numpy.asarray([x, yr], dtype=float)
        pr = numpy.asarray([x, yl], dtype=float)

        if -self.radius <= y < self.radius:
            nhCounterClockwise = self.hyperSpiral.hyperbolic(pl, clockwise=True)
            nhCounterClockwise = numpy.asarray([cos(nhCounterClockwise), sin(nhCounterClockwise)], dtype=float)

            nhClockwise = self.hyperSpiral.hyperbolic(pr, clockwise=False)
            nhClockwise = numpy.asarray([cos(nhClockwise), sin(nhClockwise)], dtype=float)

            movement = (abs(yl) * nhCounterClockwise + abs(yr) * nhClockwise) / (2.0 * self.radius)
            movement = numpy.dot(self.toGame, movement).reshape(2, )

        else:
            if y < -self.radius:
                theta = self.hyperSpiral.hyperbolic(pl, clockwise=False)
            else:
                theta = self.hyperSpiral.hyperbolic(pr, clockwise=True)

            # No artigo aqui ele só usa o theta
            movement = numpy.asarray([cos(theta), sin(theta)], dtype=float)
            movement = numpy.dot(self.toGame, movement).reshape(2, )

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
        self.robotPos = numpy.asarray(robotPos, dtype=float)
        self.robotSpeed = numpy.asarray(robotSpeed, dtype=float)

    def updateObstacle(self, obstaclePos, obstacleSpeed):
        self.obstaclePos = numpy.asarray(obstaclePos, dtype=float)
        self.obstacleSpeed = numpy.asarray(obstacleSpeed, dtype=float)

    def getVirtualPos(self):
        s = numpy.linalg.norm(self.k0 * (self.obstacleSpeed - self.robotSpeed))
        distanceBetween = numpy.linalg.norm(self.obstaclePos - self.robotPos)
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
        self.radius = float(radius)
        self.kr = float(kr)
        self.k0 = float(k0)
        self.dMin = float(dMin)
        self.lDelta = float(lDelta)

        self.avoidField.updateParam(self.k0)
        self.moveField.updateParams(self.kr, self.radius)

    def updateRobot(self, robotPos, robotSpeed):
        self.robotPos = numpy.asarray(robotPos, dtype=float)
        self.avoidField.updateRobot(robotPos, robotSpeed)

    def updateTarget(self, targetPos, orientation):
        self.moveField.updateTarget(targetPos, orientation)

    def updateObstacles(self, obstacles, obstacleSpeeds):
        self.obstacles = numpy.asarray(obstacles, dtype=float)
        self.obstaclesSpeed = numpy.asarray(obstacleSpeeds, dtype=float)

    def univector(self, robotPos, robotSpeed, target, obstacles, ostaclesSpeed=None, orientation=None):
        self.updateRobot(robotPos, robotSpeed)
        if orientation is None:
            orientation = [650.0, 250.0]
        self.updateTarget(target, orientation)
        if ostaclesSpeed is None:
            ostaclesSpeed = [0.0, 0.0]
        self.updateObstacles(obstacles, ostaclesSpeed)

        centers = []
        fi_auf = 0.0
        minDistance = self.dMin + 1
        self.obstacles = None  # Para desativar o desvio de obstáculos
        if self.obstacles is not None:
            for i in range(0, len(self.obstacles)):
                self.avoidField.updateObstacle(self.obstacles[i], self.obstaclesSpeed[i])
                center = self.avoidField.getVirtualPos()
                centers.append(center)

            centers = numpy.asarray(centers)
            distVect = numpy.linalg.norm(numpy.subtract(centers, self.robotPos), axis=1)
            index = numpy.argmin(distVect)
            closestCenter = centers[index]
            minDistance = distVect[index]

            fi_auf = self.avoidField.avoid(self.robotPos, vPos=closestCenter, theta=True)

        if minDistance <= self.dMin:
            return fi_auf
        else:
            fi_tuf = self.moveField.fi_tuf(self.robotPos)

            if self.obstacles is not None:
                guass = geometry.gaussian(minDistance - self.dMin, self.lDelta)
                diff = geometry.wrap2pi(fi_auf - fi_tuf)
                return geometry.wrap2pi(guass*diff + fi_tuf)

            else:
                return fi_tuf
