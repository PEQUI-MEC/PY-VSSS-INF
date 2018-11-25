from math import pi, atan2, sin, cos, sqrt
from helpers import geometry
from helpers.decorators import timeToFinish
import numpy


class Move2Goal:

    def __init__(self):
        self.kr = None
        self.radius = None

        self.toUnivector = None
        self.toGame = None

    def updateParams(self, kr, radius):
        if kr is not None:
            self.kr = float(kr)
        if radius is not None:
            self.radius = float(radius)

    # @timeToFinish
    # TODO refazer método
    def buildAxis(self, orientation, target):
        if type(orientation) is int:
            x = numpy.asarray([1.0, 0.0], dtype=float)
        else:
            x = numpy.asarray(numpy.asarray(orientation, dtype=float)
                              - numpy.asarray(target, dtype=float), dtype=float)
            if x.all() == 0.0:
                x = numpy.asarray([1.0, 0.0], dtype=float)

        # self.x = self.x / (-numpy.linalg.norm(self.x))
        x = x / (-numpy.sqrt(x.dot(x)))
        theta = atan2(x[1], x[0])
        y = [sin(theta), cos(theta)]

        self.toGame = numpy.asarray([x, y], dtype=float).T
        self.toUnivector = numpy.linalg.inv(self.toGame)

    def hyperbolic(self, position, target, clockwise=True):
        ro = numpy.linalg.norm(position - target)
        if ro > self.radius:
            spiral = (pi / 2.0) * (2.0 - (self.radius + self.kr) / (ro + self.kr))
        else:
            spiral = (pi / 2.0) * sqrt(ro / self.radius)

        theta = atan2(position[1], position[0])
        if clockwise:
            spiral = geometry.wrap2pi(theta + spiral)
            return atan2(sin(spiral), cos(spiral))
        else:
            spiral = geometry.wrap2pi(theta - spiral)
            return atan2(sin(spiral), cos(spiral))

    def fi_tuf(self, pos, target, orientation):
        self.buildAxis(target, orientation)

        position = numpy.asarray(pos, dtype=float) - target
        position = numpy.dot(self.toUnivector, position).reshape(2, )
        x, y = position
        yl = y + self.radius
        yr = y - self.radius
        pl = numpy.asarray([x, yr], dtype=float)
        pr = numpy.asarray([x, yl], dtype=float)

        if -self.radius <= y < self.radius:
            nhCounterClockwise = self.hyperbolic(pl, target, clockwise=True)
            nhCounterClockwise = numpy.asarray([cos(nhCounterClockwise), sin(nhCounterClockwise)], dtype=float)

            nhClockwise = self.hyperbolic(pr, target, clockwise=False)
            nhClockwise = numpy.asarray([cos(nhClockwise), sin(nhClockwise)], dtype=float)

            movement = (abs(yl) * nhCounterClockwise + abs(yr) * nhClockwise) / (2.0 * self.radius)
            movement = numpy.dot(self.toGame, movement).reshape(2, )

        else:
            if y < -self.radius:
                theta = self.hyperbolic(pl, target, clockwise=False)
            else:
                theta = self.hyperbolic(pr, target, clockwise=True)

            # No artigo aqui ele só usa o theta
            movement = numpy.asarray([cos(theta), sin(theta)], dtype=float)
            movement = numpy.dot(self.toGame, movement).reshape(2, )

        return atan2(movement[1], -movement[0])


class AvoidObstacle:
    # TODO calculo do vetor velocidade para geração de posição virtual.

    def __init__(self):
        self.k0 = None

    def updateParam(self, k0):
        self.k0 = k0

    # @timeToFinish
    def getVirtualPos(self, robotPos, robotSpeed, obstaclePos, obstacleSpeed):
        s = numpy.linalg.norm(self.k0 * (obstacleSpeed - robotSpeed))
        distanceBetween = numpy.linalg.norm(obstaclePos - robotPos)
        if distanceBetween >= s:
            virtualPos = (self.k0 * (obstacleSpeed - robotSpeed)) + obstaclePos
        else:
            virtualPos = ((distanceBetween / s) * (self.k0 * (obstacleSpeed - robotSpeed))) + obstaclePos

        return virtualPos

    # @timeToFinish
    @staticmethod
    def avoid(robotPos, virtualPos):
        position = numpy.asarray(robotPos, dtype=float) - virtualPos
        return atan2(position[1], -position[0])


class UnivectorField:
    def __init__(self):
        self.dmin = None
        self.delta = None

        self.moveField = Move2Goal()
        self.avoidField = AvoidObstacle()

    def updateConstants(self, radius=None, kr=None, k0=None, dmin=None, delta=None):
        if dmin is not None:
            self.dmin = float(dmin)
        if delta is not None:
            self.delta = float(delta)
        if k0 is not None:
            self.avoidField.updateParam(float(k0))
        if kr is not None or radius is not None:
            self.moveField.updateParams(kr, radius)

    def univector(self, robotPos, robotSpeed, target, obstacles=None,
                  ostaclesSpeed=numpy.asarray([0.0, 0.0], dtype=float),
                  orientation=numpy.asarray([650.0, 250.0], dtype=float)):

        centers = []
        fi_auf = 0.0
        minDistance = self.dmin + 1

        if obstacles is not None:
            for i in range(0, len(obstacles)):
                center = self.avoidField.getVirtualPos(robotPos, robotSpeed, obstacles[i], ostaclesSpeed)
                centers.append(center)

            centers = numpy.asarray(centers)
            distance = numpy.linalg.norm(numpy.subtract(centers, robotPos), axis=1)
            index = numpy.argmin(distance)
            closestCenter = centers[index]
            minDistance = distance[index]

            fi_auf = self.avoidField.avoid(robotPos, virtualPos=closestCenter)

        if minDistance <= self.dmin:
            return fi_auf
        else:
            fi_tuf = self.moveField.fi_tuf(robotPos, target, orientation)

            if obstacles is not None:
                guass = geometry.gaussian(minDistance - self.dmin, self.delta)
                diff = geometry.wrap2pi(fi_auf - fi_tuf)

                return geometry.wrap2pi(guass * diff + fi_tuf)

            else:
                return fi_tuf
