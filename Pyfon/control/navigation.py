import math
import numpy as np
from scipy.spatial import distance


def gaussian(m, v):
    return math.exp(-(m**2) / (2 * (v**2)))


def angleWithX(p):
    i = np.array([1.0, 0.0])
    theta = math.atan2(np.cross(i, p), np.dot(i, p))
    return theta


def wrap2pi(theta):
    if theta > math.pi:
        return theta - 2 * math.pi
    if theta < -math.pi:
        return 2 * math.pi + theta
    else:
        return theta


def angle(target, position):
    x = target[0] - position[0]
    y = target[1] - position[1]
    return math.atan2(y, -x)


class HyperbolicSpiral:
    def __init__(self, Kr, radius):
        self.Kr = Kr
        self.radius = radius
        self.origin = None
        self.orientation = None

    def updateParams(self, KR, RADIUS):
        self.Kr = KR
        self.radius = RADIUS

    def updateOrigin(self, newOrigin):
        self.origin = np.array(newOrigin)

    def updateOrientation(self, orientation):
        self.orientation = np.array(orientation)

    def fi_h(self, p, radius=None, cw=True):
        if radius is None:
            r = self.radius
        else:
            r = radius

        # theta = angle(p, self.origin) - (self.orientation - angle(p, self.origin))
        theta = math.atan2(p[1], p[0])  # TODO(Luana) Verificar mudanças
        print("61: Theta: " + str(theta))

        # p = distance.euclidean(_p, self.origin)
        ro = np.linalg.norm(p)  # TODO(Luana) Verificar mudanças
        if ro > r:
            a = (math.pi / 2.0) * (2.0 - (r + self.Kr)/(ro + self.Kr))
        else:
            a = (math.pi / 2.0) * math.sqrt(ro / r)

        if cw:
            _theta = wrap2pi(theta+a)
            return math.atan2(math.sin(_theta), math.cos(_theta))
        else:
            _theta = wrap2pi(theta - a)
            return math.atan2(math.sin(_theta), math.cos(_theta))

    def n_h(self, p, radius=None, cw=True):
        if radius is None:
            radius = self.radius
        else:
            radius = radius

        fi = self.fi_h(p, radius, cw)

        return np.array([math.cos(fi), math.cos(fi)])


class Repulsive:
    def __init__(self):
        self.origin = None

    def updateOrigin(self, newOrigin):
        self.origin = np.copy(newOrigin)

    def fi_r(self, p, origin=None, theta=True):
        if origin is not None:
            self.updateOrigin(origin)

        p = np.array(p) - self.origin

        if theta is True:
            # theta = angleWithX(p)
            # return wrap2pi(theta)
            return math.atan2(p[1], p[0])
        else:
            return p


LEFT = 0
RIGHT = 1


class Move2Goal:

    def __init__(self, Kr, radius, attackGoal=RIGHT, rotationSupport=False):
        self.Kr = Kr
        self.radius = radius
        self.hyperSpiral = HyperbolicSpiral(self.Kr, self.radius)
        self.orientation = None
        self.origin = None
        self.attack_goal = attackGoal
        self.rotation_support = rotationSupport
        self.u = np.array([None, None])
        self.v = np.array([None, None])
        self.toUnivectorMatrix = None
        self.toCanonicalMatrix = None

    def updateParams(self, KR, RADIUS):
        self.Kr = KR
        self.radius = RADIUS
        self.hyperSpiral.updateParams(self.Kr, self.radius)

    def updateOrigin(self, newOrigin):
        self.origin = np.array(newOrigin)
        self.hyperSpiral.updateOrigin(newOrigin)
        self.buildAxis()

    def updateOrientation(self, orientation):
        self.orientation = np.array(orientation)
        self.hyperSpiral.updateOrientation(orientation)

    # TODO to targetOrientation
    def buildAxis(self):
        if type(self.attack_goal) != type(int) and self.rotation_support is True:
            self.u = np.array(self.attack_goal - self.origin, dtype=np.float32)
        else:  # is int
            if self.attack_goal == RIGHT:
                self.u = np.array([-1.0, 0.0])
            else:
                self.u = np.array([1.0, 0.0])

        self.u /= -np.linalg.norm(self.u)
        theta = math.atan2(self.u[1], self.u[0])
        self.v = np.array([-math.sin(theta), math.cos(theta)])

        self.toCanonicalMatrix = np.array([self.u, self.v]).T
        self.toUnivectorMatrix = np.linalg.inv(self.toCanonicalMatrix)

    def fi_tuf(self, p):
        p = np.array(p) - self.origin

        # TODO verificar de onde deabos deve ser esse x e y
        p = np.dot(self.toUnivectorMatrix, p).reshape(2, )
        x, y = p
        yl = y + self.radius
        yr = y - self.radius

        pl = np.array([x, yr])
        pr = np.array([x, yl])

        if -self.radius <= y < self.radius:
            nhCCW = self.hyperSpiral.n_h(pl, cw=False)
            nhCW = self.hyperSpiral.n_h(pr, cw=True)

            vec = (abs(yl) * nhCCW + abs(yr) * nhCW) / (2.0 * self.radius)
            vec = np.dot(self.toCanonicalMatrix, vec).reshape(2, )
            # return wrap2pi(angleWithX(vec))
        else:
            if y < -self.radius:
                theta = self.hyperSpiral.fi_h(pl, cw=True)
            else:  # y >= r
                theta = self.hyperSpiral.fi_h(pr, cw=False)

            vec = np.array([math.cos(theta), math.sin(theta)])
            vec = np.dot(self.toCanonicalMatrix, vec).reshape(2, )

        return math.atan2(vec[1], vec[0])


class AvoidObstacle:
    def __init__(self, pObs, vObs, pRobot, vRobot, K0):
        self.pObs = np.array(pObs)
        self.vObs = np.array(vObs)
        self.pRobot = np.array(pRobot)
        self.vRobot = np.array(vRobot)
        self.K0 = K0
        self.repField = Repulsive()

    def updateParam(self, K0):
        self.K0 = K0

    def updateRobot(self, pRobot, vRobot):
        self.pRobot = np.array(pRobot)
        self.vRobot = np.array(vRobot)

    def updateObstacle(self, pObs, vObs):
        self.pObs = np.copy(np.array(pObs))
        self.vObs = np.copy(np.array(vObs))

    def getS(self):
        return self.K0 * (self.vObs - self.vRobot)

    def getVirtualPos(self):
        sNorm = np.linalg.norm(self.getS())
        d = np.linalg.norm(self.pObs - self.pRobot)
        if d >= sNorm:
            vPos = self.pObs + self.getS()
        else:
            vPos = self.pObs + (d/sNorm)*self.getS()
        return vPos

    def fi_auf(self, robotPos, vPos=None, theta=True):
        if vPos is None:
            vPos = self.getVirtualPos()
        else:
            vPos = vPos
        vec = self.repField.fi_r(robotPos, origin=vPos, theta=theta)
        return vec


class UnivectorField:
    def __init__(self, attackGoal=RIGHT, rotation=True):
        # Field constants
        self.RADIUS = None
        self.KR = None
        self.K0 = None
        self.DMIN = None
        self.LDELTA = None

        # Subfields
        self.avdObsField = AvoidObstacle([None, None], [None, None], [None, None], [None, None], self.K0)
        self.mv2GoalField = Move2Goal(self.KR, self.RADIUS, attackGoal=attackGoal, rotationSupport=rotation)

        self.obstacles = None
        self.obstaclesSpeed = None
        self.targetPos = None
        self.robotPos = None
        self.vRobot = None
        self.orientation = None

    def updateConstants(self, RADIUS, KR, K0, DMIN, LDELTA):
        self.RADIUS = RADIUS
        self.KR = KR
        self.K0 = K0
        self.DMIN = DMIN
        self.LDELTA = LDELTA
        self.avdObsField.updateParam(self.K0)
        self.mv2GoalField.updateParams(self.KR, self.RADIUS)

    def updateRobot(self, robotPos, vRobot):
        self.robotPos = np.array(robotPos)
        self.vRobot = np.array(vRobot)
        self.avdObsField.updateRobot(self.robotPos, self.vRobot)

    def updateTarget(self, targetPos):
        self.targetPos = np.array(targetPos)
        self.mv2GoalField.updateOrigin(targetPos)

    def updateObstacles(self, obstacles, obsSpeeds):
        self.obstacles = np.array(obstacles)
        self.obstaclesSpeed = np.array(obsSpeeds)

    def updateOrientation(self, orientation):
        self.orientation = np.array(orientation)
        self.mv2GoalField.updateOrientation(orientation)

    def getVec(self, robotPos=None, vRobot=None, target=None, orientation=None):
        robotPos = np.array(robotPos)
        vRobot = np.array(vRobot)
        target = np.array(target)
        orientation = np.array(orientation)

        # Atualizar valores recebidos
        if robotPos is not None and vRobot is not None:
            self.updateRobot(robotPos, vRobot)
        if target is not None:
            self.updateTarget(target)
        if orientation is not None:
            self.updateOrientation(orientation)

        closestCenter = np.array([None, None])
        centers = []
        minDistance = self.DMIN + 1
        fi_auf = 0.0

        if self.obstacles is not None:
            for i in range(self.obstacles.shape[0]):
                self.avdObsField.updateObstacle(self.obstacles[i], self.obstaclesSpeed[i])
                center = self.avdObsField.getVirtualPos()
                centers.append(center)

            centers = np.asarray(centers)
            distVect = np.linalg.norm(np.subtract(centers, self.robotPos), axis=1)
            index = np.argmin(distVect)
            closestCenter = centers[index]
            minDistance = distVect[index]

            fi_auf = self.avdObsField.fi_auf(self.robotPos, vPos=closestCenter, theta=True)

        if minDistance <= self.DMIN:
            return fi_auf
        else:
            fi_tuf = self.mv2GoalField.fi_tuf(self.robotPos)
            print("320:  FiAuf " + str(fi_tuf))

            if self.obstacles is not None:
                print("325:  Existe? ")
                g = gaussian(minDistance - self.DMIN, self.LDELTA)
                diff = wrap2pi(fi_auf - fi_tuf)
                return wrap2pi(g*diff + fi_tuf)

            else:
                return fi_tuf
