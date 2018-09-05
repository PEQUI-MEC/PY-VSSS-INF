class Robot:
    def __init__(self):
        self.position = None
        self.target = None
        self.orientation = None
        self.targetOrientation = None
        self.transAngle = None
        self.cmdType = None
        self.vMax = None
        self.vLeft = None
        self.vRight = None
        self.action = None

    def set(self, entry, value):
        if entry == 'position':
            self.position = value
        elif entry == 'target':
            self.target = value
        elif entry == 'orientation':
            self.orientation = value
        elif entry == 'targetOrientation':
            self.targetOrientation = value
        elif entry == 'transAngle':
            self.transAngle = value
        elif entry == 'cmdType':
            self.cmdType = value
        elif entry == 'vMax':
            self.vMax = value
        elif entry == 'vLeft':
            self.vLeft = value
        elif entry == 'vRight':
            self.vRight = value
        elif entry == 'action':
            self.action = value


