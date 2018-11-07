from ctypes import Structure


class Warrior(Structure):

    def __init__(self):
        self.name = None

        self.front = -1
        self.backward = False

        self.position = None
        self.orientation = None
        self.transAngle = None

        self.vMax = None
        self.vLeft = None
        self.vRight = None
        self.velAcc = 0.5

        self.target = None
        self.targetOrientation = None

        self.obstacles = None
        self.obstaclesSpeed = None

        self.action = []

        self.cmdType = None

        self.before = None
