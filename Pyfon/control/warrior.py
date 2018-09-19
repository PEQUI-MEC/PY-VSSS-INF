from ctypes import Structure


class Warrior(Structure):

    def __init__(self):
        self.position = None
        self.orientation = None
        self.transAngle = None

        self.vMax = None
        self.vLeft = None
        self.vRight = None

        self.target = None
        self.targetOrientation = None

        self.obstacles = None

        self.action = []

        self.cmdType = None


