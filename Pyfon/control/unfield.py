import math
import numpy as np
from scipy.spatial import distance

LEFT = 0
RIGHT = 1


def gaussian(m, v):
    return math.exp(-(m**2) / (2 * (v**2)))


def angleWithX(p):
    i = np.array([1.0,0.0])
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
    def __init__(self, _Kr, _radius):
        self.Kr = _Kr
        self.radius = _radius
        self.origin = None
        self.orientation = None

    def updateParams(self, _KR, _RADIUS):
        self.Kr = _KR
        self.radius = _RADIUS

    def updateOrigin(self, _newOrigin):
        self.origin = np.array(_newOrigin)

    def updateOrientation(self, _orientation):
        self.orientation = np.array(_orientation)

    def fi_h(self, _p, radius=None, cw=True):
        Kr = self.Kr

        if radius is None:
            r = self.radius
        else:
            r = radius

        p = np.array(_p)
        # theta = angle(p, self.origin) - (self.orientation - angle(p, self.origin))
        theta = math.atan2(p[1], p[0])  # TODO(Luana) Verificar mudanças
        print("61: Theta: " + str(theta))

        # p = distance.euclidean(_p, self.origin)
        ro = np.linalg.norm(p)  # TODO(Luana) Verificar mudanças
        if ro > r:
            a = (math.pi / 2.0) * (2.0 - (r + Kr)/(ro + Kr))
        else:
            a = (math.pi / 2.0) * math.sqrt(ro / r)

        # TODO(Luana) Verificar mudanças
        if cw:
            _theta = wrap2pi(theta+a)
            return math.atan2(math.sin(_theta), math.cos(_theta))
        else:
            _theta = wrap2pi(theta - a)
            return math.atan2(math.sin(_theta), math.cos(_theta))

    def n_h(self, _p, _radius=None, cw=True):
        p = np.array(_p)

        if _radius is None:
            radius = self.radius
        else:
            radius = _radius

        fi = self.fi_h(p, radius, cw)

        return np.array([math.cos(fi), math.cos(fi)])


class Repulsive:
    def __init__(self):
        self.origin = np.array([None, None])

    def updateOrigin(self, newOrigin):
        self.origin = np.copy(newOrigin)

    def fi_r(self, _p, _origin=None, _theta=True):
        if _origin is not None:
            self.updateOrigin(_origin)

        p = np.array(_p) - self.origin

        if _theta is True:
            # theta = angleWithX(p)
            # return wrap2pi(theta)
            # TODO(Luana) Verificar mudanças
            return math.atan2(p[1], p[0])
        else:
            return p


class Move2Goal:

    def __init__(self, _Kr, _radius, _attackGoal=RIGHT, _rotationSupport=False):
        self.Kr = _Kr
        self.radius = _radius
        self.hyperSpiral = HyperbolicSpiral(self.Kr, self.radius)
        self.orientation = None
        self.origin = None
        self.attack_goal = _attackGoal
        self.rotation_support = _rotationSupport
        self.u = np.array([None, None])
        self.v = np.array([None, None])
        self.toUnivectorMatrix = None
        self.toCanonicalMatrix = None

    def updateParams(self, _KR, _RADIUS):
        self.Kr = _KR
        self.radius = _RADIUS
        self.hyperSpiral.updateParams(self.Kr, self.radius)

    def updateOrigin(self, _newOrigin):
        self.origin = np.array(_newOrigin)
        self.hyperSpiral.updateOrigin(_newOrigin)
        self.buildAxis()

    def updateOrientation(self, _orientation):
        self.orientation = np.array(_orientation)
        self.hyperSpiral.updateOrientation(_orientation)

    # TODO(Luana) Verificar mudanças
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

    def fi_tuf(self, _p):
        hyperSpiral = self.hyperSpiral
        n_h = self.hyperSpiral.n_h
        r = self.radius
        p = np.array(_p) - self.origin

        # TODO(Luana) verificar de onde deabos deve ser esse x e y
        p = np.dot(self.toUnivectorMatrix, p).reshape(2, )
        x, y = p
        yl = y + r
        yr = y - r

        pl = np.array([x, yr])
        pr = np.array([x, yl])

        if -r <= y < r:
            nhCCW = n_h(pl, cw=False)
            nhCW = n_h(pr, cw=True)

            vec = (abs(yl) * nhCCW + abs(yr) * nhCW) / (2.0 * r)
            vec = np.dot(self.toCanonicalMatrix, vec).reshape(2, )
            # return wrap2pi(angleWithX(vec))
        else:
            if y < -r:
                theta = hyperSpiral.fi_h(pl, cw=True)
            else:  # y >= r
                theta = hyperSpiral.fi_h(pr, cw=False)

            vec = np.array([math.cos(theta), math.sin(theta)])
            vec = np.dot(self.toCanonicalMatrix, vec).reshape(2, )

        return math.atan2(vec[1], vec[0])


class AvoidObstacle:
    def __init__(self, _pObs, _vObs, _pRobot, _vRobot, _K0):
        self.pObs = np.array(_pObs)
        self.vObs = np.array(_vObs)
        self.pRobot = np.array(_pRobot)
        self.vRobot = np.array(_vRobot)
        self.K0 = _K0
        self.repField = Repulsive()

    def updateParam(self, _K0):
        self.K0 = _K0

    def updateRobot(self, _pRobot, _vRobot):
        self.pRobot = np.array(_pRobot)
        self.vRobot = np.array(_vRobot)

    def updateObstacle(self, _pObs, _vObs):
        self.pObs = np.copy(np.array(_pObs))
        self.vObs = np.copy(np.array(_vObs))

    def getS(self):
        return self.K0 * (self.vObs - self.vRobot)

    def getVirtualPos(self):
        s = self.getS()
        sNorm = np.linalg.norm(s)
        d = np.linalg.norm(self.pObs - self.pRobot)
        if d >= sNorm:
            vPos = self.pObs + s
        else:
            vPos = self.pObs + (d/sNorm)*s
        return vPos

    def fi_auf(self, _robotPos, _vPos=None, _theta=True):
        if _vPos is None:
            vPos = self.getVirtualPos()
        else:
            vPos = _vPos
        vec = self.repField.fi_r(_robotPos, _origin=vPos, _theta=_theta)
        return vec


class UnivectorField:
    def __init__(self, _attackGoal=RIGHT, _rotation=True):
        self.obstacles = None
        self.obstaclesSpeed = None
        self.targetPos = None
        self.robotPos = None
        self.vRobot = None
        self.orientation = None

        # Field constants
        self.RADIUS = None
        self.KR = None
        self.K0 = None
        self.DMIN = None
        self.LDELTA = None

        # Subfields
        self.avdObsField = AvoidObstacle([None, None], [None, None], [None, None], [None, None], self.K0)
        self.mv2GoalField = Move2Goal(self.KR, self.RADIUS, _attackGoal=_attackGoal, _rotationSupport=_rotation)

    def updateConstants(self, _RADIUS, _KR, _K0, _DMIN, _LDELTA):
        self.RADIUS = _RADIUS
        self.KR = _KR
        self.K0 = _K0
        self.DMIN = _DMIN
        self.LDELTA = _LDELTA
        self.avdObsField.updateParam(self.K0)
        self.mv2GoalField.updateParams(self.KR, self.RADIUS)

    def updateRobot(self, _robotPos, _vRobot):
        self.robotPos = np.array(_robotPos)
        self.vRobot = np.array(_vRobot)
        self.avdObsField.updateRobot(self.robotPos, self.vRobot)

    def updateTarget(self, _targetPos):
        self.targetPos = np.array(_targetPos)
        self.mv2GoalField.updateOrigin(_targetPos)

    def updateObstacles(self, _obstacles, _obsSpeeds):
        self.obstacles = np.array(_obstacles)
        self.obstaclesSpeed = np.array(_obsSpeeds)

    def updateOrientation(self, _orientation):
        self.orientation = np.array(_orientation)
        self.mv2GoalField.updateOrientation(_orientation)

    def getVec(self, _robotPos=None, _vRobot=None, _target=None, _orientation=None):
        robotPos = np.array(_robotPos)
        vRobot = np.array(_vRobot)
        target = np.array(_target)
        orientation = np.array(_orientation)

        # Atualizar valores recebidos
        if robotPos is not None and vRobot is not None:
            self.updateRobot(robotPos, vRobot)
        if target is not None:
            self.updateTarget(target)
        if orientation is not None:
            self.updateOrientation(orientation)

        closestCenter = np.array([None, None])  # array to store the closest center
        centers = []
        minDistance = self.DMIN + 1
        fi_auf = 0.0

        if self.obstacles is not None:
            # get the repulsive field centers
            for i in range(self.obstacles.shape[0]):
                self.avdObsField.updateObstacle(self.obstacles[i], self.obstaclesSpeed[i])
                center = self.avdObsField.getVirtualPos()
                centers.append(center)

            centers = np.asarray(centers)
            distVect = np.linalg.norm(np.subtract(centers, self.robotPos), axis=1)
            index = np.argmin(distVect)  # index of closest center
            closestCenter = centers[index]
            minDistance = distVect[index]

            fi_auf = self.avdObsField.fi_auf(self.robotPos, _vPos=closestCenter, _theta=True)

        # the first case when the robot is to close from an obstacle
        if minDistance <= self.DMIN:
            return fi_auf
        else:
            fi_tuf = self.mv2GoalField.fi_tuf(self.robotPos)
            print("320:  FiAuf " + str(fi_tuf))

            # Checks if at least one obstacle exist
            if self.obstacles is not None:
                print("325:  Existe? ")
                g = gaussian(minDistance - self.DMIN, self.LDELTA)
                diff = wrap2pi(fi_auf - fi_tuf)
                return wrap2pi(g*diff + fi_tuf)

            # if there is no obstacles
            else:
                return fi_tuf
