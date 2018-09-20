import numpy as np
import math
from scipy.spatial import distance


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


class HyperbolicSpiral:
    def __init__(self, _Kr, _radius):
        self.Kr = _Kr
        self.radius = _radius
        self.origin = np.array([None, None])

    def updateParams(self, _KR, _RADIUS):
        self.Kr = _KR
        self.radius = _RADIUS

    def updateOrigin(self, newOrigin):
        self.origin = np.array(newOrigin)

    def fi_h(self, _p, radius=None, cw=True):
        Kr = self.Kr

        if radius is None:
            r = self.radius
        else:
            r = radius

        p = np.array(_p)
        # p = distance.euclidean(p, self.origin)

        # TODO(Luana) ver cálculo do theta. Theta = eixo das abcissas à posição p
        theta = wrap2pi(angleWithX(p))
        # print("Theta: " + str(theta))
        ro = np.linalg.norm(p)

        # TODO(Luana) Trocar ro por p. p = distância do robo para seu target
        if ro > r:
            a = (math.pi / 2.0) * (2.0 - (r + Kr)/(ro + Kr))
        else:
            a = (math.pi / 2.0) * math.sqrt(ro / r)

        if cw:
            return wrap2pi(theta + a)
        else:
            return wrap2pi(theta - a)

    def n_h(self, _p, _radius=None, cw=True):
        p = np.array(_p)
        if _radius is None:
            radius = self.radius
        else:
            radius = _radius

        fi = self.fi_h(p, radius, cw)
        cos = math.cos(fi)
        sin = math.sin(fi)
        return np.array([cos, sin])


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
            theta = angleWithX(p)
            return wrap2pi(theta)
        else:
            return p


class Move2Goal:

    def __init__(self, _Kr, _radius):
        self.Kr = _Kr
        self.radius = _radius
        self.hyperSpiral = HyperbolicSpiral(self.Kr, self.radius)
        # self.origin = np.array([None, None])

    def updateParams(self, _KR, _RADIUS):
        self.Kr = _KR
        self.radius = _RADIUS
        self.hyperSpiral.updateParams(self.Kr, self.radius)

    def updateOrigin(self, newOrigin):
        self.hyperSpiral.updateOrigin(newOrigin)
        # self.origin = np.array(newOrigin)

    def fi_tuf(self, _p):
        hyperSpiral = self.hyperSpiral
        n_h = self.hyperSpiral.n_h

        r = self.radius

        # TODO(Luana) Encontrar x e y dado uma orientação final desejada?
        p = np.array(_p)
        x,y = p
        yl = y+r
        yr = y-r


        pl = np.array([x, yl])
        pr = np.array([x, yr])

        if -r <= y < r:
            nhCCW = n_h(pl, cw=False)
            nhCW = n_h(pr, cw=True)

            vec = ( abs(yl)*nhCCW + abs(yr)*nhCW ) / (2.0 * r)
            return wrap2pi(angleWithX(vec))
        elif y < -r:
            return hyperSpiral.fi_h(pl, cw=True)
        else: #y >= r
            return hyperSpiral.fi_h(pr, cw=False)


class AvoidObstacle:
    def __init__(self, _pObs, _vObs, _pRobot, _vRobot, _K0):
        self.pObs = np.array(_pObs)
        self.vObs = np.array(_vObs)
        self.pRobot = np.array(_pRobot)
        self.vRobot = np.array(_vRobot)
        self.K0 = _K0
        self.repField = Repulsive()

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

    def fi_auf(self, _robotPos, _vPos=[None, None], _theta=True):
        if _vPos is None:
            vPos = self.getVirtualPos()
        else:
            vPos = _vPos
        vec = self.repField.fi_r(_robotPos, _origin=vPos, _theta=_theta)
        return vec

    def updateParam(self, _K0):
        self.K0 = _K0

    def updateObstacle(self, _pObs, _vObs):
        self.pObs = np.copy(np.array(_pObs))
        self.vObs = np.copy(np.array(_vObs))

    def updateRobot(self, _pRobot, _vRobot):
        self.pRobot = np.array(_pRobot)
        self.vRobot = np.array(_vRobot)


class UnivectorField:
    def __init__(self):
        self.obstacles = np.array([[None, None]])
        self.obstaclesSpeed = np.array([[None, None]])
        self.ballPos = np.array([None, None])
        self.robotPos = np.array([None, None])
        self.vRobot = np.array([None, None])

        # Field constants
        self.RADIUS = None
        self.KR = None
        self.K0 = None
        self.DMIN = None
        self.LDELTA = None

        # Subfields
        self.avdObsField = AvoidObstacle([None, None], [None, None], [None, None], [None, None], self.K0)
        self.mv2GoalField = Move2Goal(self.KR, self.RADIUS)

    def updateObstacles(self, _obstacles, _obsSpeeds):
        self.obstacles = np.array(_obstacles)
        self.obstaclesSpeed = np.array(_obsSpeeds)

    def updateBall(self, _ballPos):
        self.ballPos = np.array(_ballPos)
        self.mv2GoalField.updateOrigin(_ballPos)

    def updateRobot(self, _robotPos, _vRobot):
        self.robotPos = np.array(_robotPos)
        self.vRobot = np.array(_vRobot)
        self.avdObsField.updateRobot(self.robotPos, self.vRobot)

    def updateConstants(self, _RADIUS, _KR, _K0, _DMIN, _LDELTA):
        self.RADIUS = _RADIUS
        self.KR = _KR
        self.K0 = _K0
        self.DMIN = _DMIN
        self.LDELTA = _LDELTA

        self.avdObsField.updateParam(self.K0)
        self.mv2GoalField.updateParams(self.KR, self.RADIUS)

    def getVec(self, _robotPos=[None, None], _vRobot=[None, None], _ball=[None, None]):
        robotPos = np.array(_robotPos)
        vRobot = np.array(_vRobot)
        ball = np.array(_ball)

        if robotPos is not None and vRobot is not None:
            self.updateRobot(robotPos, vRobot)
        if ball is not None:
            self.updateBall(ball)

        closestCenter = np.array([None, None]) # array to store the closest center
        centers = []
        minDistance = self.DMIN + 1

        if len(self.obstacles) > 0 and self.obstacles[0][0] is not None and self.obstacles[0][1] is not None:
            # get the repulsive field centers
            for i in range(self.obstacles.shape[0]):
                self.avdObsField.updateObstacle(self.obstacles[i], self.obstaclesSpeed[i])
                center = self.avdObsField.getVirtualPos()
                centers.append(center)

            centers = np.asarray(centers)
            distVect = np.linalg.norm(np.subtract(centers, self.robotPos), axis=1)
            index = np.argmin(distVect) # index of closest center
            closestCenter = centers[index]
            minDistance = distVect[index]

            fi_auf = self.avdObsField.fi_auf(self.robotPos, _vPos=closestCenter, _theta=True)

        # the first case when the robot is to close from an obstacle
        if minDistance <= self.DMIN:
            return fi_auf
        else:
            fi_tuf = self.mv2GoalField.fi_tuf(self.robotPos)
            # print("FiAuf " + str(fi_tuf))
            # Checks if at least one obstacle exist
            if len(self.obstacles) > 0 and self.obstacles[0][0] is not None and self.obstacles[0][1] is not None:
                # print("Existe? ")
                g = gaussian(minDistance - self.DMIN, self.LDELTA)
                diff = wrap2pi(fi_auf - fi_tuf)
                # print(g*diff + fi_tuf)
                return g*diff + fi_tuf

            # if there is no obstacles
            else:
                return fi_tuf
