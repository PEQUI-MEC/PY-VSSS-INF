from math import pi, atan2, sin, cos, exp, sqrt
from scipy.spatial import distance
import numpy as np


def gaussian(m, v):
    return exp(-(m**2) / (2 * (v**2)))


def angleWithX(p):
    i = np.array([1.0, 0.0])
    theta = atan2(np.cross(i, p), np.dot(i, p))
    return theta


def wrap2pi(theta):
    if theta > pi:
        return theta - 2 * pi
    if theta < -pi:
        return 2 * pi + theta
    else:
        return theta


def angle(target, position):
    x = target[0] - position[0]
    y = target[1] - position[1]
    return atan2(y, -x)


class HyperbolicSpiral:
    def __init__(self, kr, radius):
        self.kr = kr
        self.radius = radius
        self.origin = None

    def updateParams(self, kr, radius):
        self.kr = kr
        self.radius = radius

    def updateOrigin(self, newOrigin):
        self.origin = np.array(newOrigin)

    def hyperbolic(self, position, r=None, clockwise=True):
        if r is None:
            radius = self.radius
        else:
            radius = r

        # theta = angle(p, self.origin) - (self.orientation - angle(p, self.origin))
        theta = atan2(position[1], position[0])  # TODO(Luana) Verificar mudanças
        print(": Theta: " + str(theta))

        ro = distance.euclidean(position, self.origin)
        if ro > radius:
            spiral = (pi / 2.0) * (2.0 - (radius + self.kr) / (ro + self.kr))
        else:
            spiral = (pi / 2.0) * sqrt(ro / radius)

        if clockwise:
            spiral = wrap2pi(theta + spiral)
            return atan2(sin(spiral), cos(spiral))
        else:
            spiral = wrap2pi(theta - spiral)
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
            return atan2(position[1], position[0])
        else:
            return position


class Move2Goal:

    def __init__(self, kr, radius, attackGoal=1, rotationSupport=False):
        self.kr = kr
        self.radius = radius
        self.hyperSpiral = HyperbolicSpiral(self.kr, self.radius)
        self.origin = None
        self.attackGoal = attackGoal
        self.rotation_support = rotationSupport
        self.u = np.array([None, None])
        self.v = np.array([None, None])
        self.toUnivectorMatrix = None
        self.toCanonicalMatrix = None

    def updateParams(self, kr, radius):
        self.kr = kr
        self.radius = radius
        self.hyperSpiral.updateParams(self.kr, self.radius)

    def updateOrigin(self, newOrigin):
        self.origin = np.array(newOrigin)
        self.hyperSpiral.updateOrigin(newOrigin)
        self.buildAxis()

    def updateOrientation(self, orientation):
        self.attackGoal = np.array(orientation)

    # TODO to targetOrientation
    def buildAxis(self):
        if type(self.attackGoal) != type(int) and self.rotation_support is True:
            self.u = np.array(self.attackGoal - self.origin, dtype=np.float32)
        else:
            if self.attackGoal == 1:
                self.u = np.array([1.0, 0.0])
            else:
                self.u = np.array([-1.0, 0.0])

        self.u /= -np.linalg.norm(self.u)
        theta = atan2(self.u[1], self.u[0])
        self.v = np.array([-sin(theta), cos(theta)])

        self.toCanonicalMatrix = np.array([self.u, self.v]).T
        self.toUnivectorMatrix = np.linalg.inv(self.toCanonicalMatrix)

    def fi_tuf(self, p):
        position = np.array(p) - self.origin

        # TODO verificar de onde deabos deve ser esse x e y
        position = np.dot(self.toUnivectorMatrix, position).reshape(2, )
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
            movement = np.dot(self.toCanonicalMatrix, movement).reshape(2, )

        else:
            if y < -self.radius:
                theta = self.hyperSpiral.hyperbolic(pl, clockwise=True)
            else:
                theta = self.hyperSpiral.hyperbolic(pr, clockwise=False)

            # TODO(Luana) no artigo aqui ele só usa o theta
            movement = np.array([cos(theta), sin(theta)])
            movement = np.dot(self.toCanonicalMatrix, movement).reshape(2, )

        return atan2(movement[1], movement[0])


class AvoidObstacle:
    def __init__(self, obstaclePos, obstacleSpeed, robotPos, robotSpeed, k0):
        self.obstaclePos = np.array(obstaclePos)
        self.obstacleSpeed = np.array(obstacleSpeed)
        self.robotPos = np.array(robotPos)
        self.robotSpeed = np.array(robotSpeed)
        self.k0 = k0
        self.repulsive = Repulsive()

    def updateParam(self, k0):
        self.k0 = k0

    def updateRobot(self, robotPos, robotSpeed):
        self.robotPos = np.array(robotPos)
        self.robotSpeed = np.array(robotSpeed)

    def updateObstacle(self, obstaclePos, obstacleSpeed):
        self.obstaclePos = np.array(obstaclePos)
        self.obstacleSpeed = np.array(obstacleSpeed)

    def getVirtualPos(self):
        sNorm = np.linalg.norm(self.k0 * (self.obstacleSpeed - self.robotSpeed))
        distanceBetween = distance.euclidean(self.obstaclePos, self.robotPos)
        if distanceBetween >= sNorm:
            virtualPos = self.obstaclePos + (self.k0 * (self.obstacleSpeed - self.robotSpeed))
        else:
            virtualPos = self.obstaclePos + (distanceBetween/sNorm)*(self.k0 * (self.obstacleSpeed - self.robotSpeed))
        return virtualPos

    def avoid(self, robotPos, vPos=None, theta=True):
        if vPos is None:
            virtualPos = self.getVirtualPos()
        else:
            virtualPos = vPos

        return self.repulsive.repulsive(robotPos, origin=virtualPos, theta=theta)


class UnivectorField:
    def __init__(self, attackGoal=1, rotation=True):
        # Constants
        self.radius = None
        self.kr = None
        self.k0 = None
        self.dMin = None
        self.lDelta = None

        # Subfields
        self.avoidField = AvoidObstacle([None, None], [None, None], [None, None], [None, None], self.k0)
        self.moveField = Move2Goal(self.kr, self.radius, attackGoal=attackGoal, rotationSupport=rotation)

        #
        self.obstacles = None
        self.obstaclesSpeed = None
        self.targetPos = None
        self.robotPos = None
        self.robotSpeed = None

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

    def updateTarget(self, targetPos):
        self.targetPos = np.array(targetPos)
        self.moveField.updateOrigin(targetPos)

    def updateObstacles(self, obstacles, obstacleSpeeds):
        self.obstacles = np.array(obstacles)
        self.obstaclesSpeed = np.array(obstacleSpeeds)

    def updateOrientation(self, orientation):
        self.moveField.updateOrientation(orientation)

    def getVec(self, robotPos=None, robotSpeed=None, target=None, orientation=None):
        robotPos = np.array(robotPos)
        robotSpeed = np.array(robotSpeed)
        target = np.array(target)
        orientation = np.array(orientation)

        # Atualizar valores recebidos
        if robotPos is not None and robotSpeed is not None:
            self.updateRobot(robotPos, robotSpeed)
        if target is not None:
            self.updateTarget(target)
        if orientation is not None:
            self.updateOrientation(orientation)

        closestCenter = np.array([None, None])
        centers = []
        minDistance = self.dMin + 1
        fi_auf = 0.0

        if self.obstacles is not None:
            for i in range(self.obstacles.shape[0]):
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
            return fi_auf
        else:
            fi_tuf = self.moveField.fi_tuf(self.robotPos)
            print(":  FiAuf " + str(fi_tuf))

            if self.obstacles is not None:
                print(":  Existe? ")
                guass = gaussian(minDistance - self.dMin, self.lDelta)
                diff = wrap2pi(fi_auf - fi_tuf)
                return wrap2pi(guass*diff + fi_tuf)

            else:
                return fi_tuf
