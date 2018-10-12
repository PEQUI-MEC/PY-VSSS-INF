class Robot(object):

    def __init__(self):
        self.position = None
        self.orientation = None
        self.transAngle = None

        self.vMax = None
        self.vLeft = None
        self.vRight = None

        self.target = None
        self.targetOrientation = None

        self.action = []

        self.cmdType = None


