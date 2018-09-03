class Robot:
    def __init__(self, position=[0,0], target=[0,0], orientation=0, targetOrientation=0, transAngle=0, cmdType="", vMax=0, vLeft=0, vRight=0, actions=""):
        self.position = position
        self.target = target
        self.orientation = orientation
        self.targetOrientation = targetOrientation
        self.transAngle = transAngle
        self.cmdType = cmdType
        self.vMax = vMax
        self.vLeft = vLeft
        self.vRight = vRight
        self.actions = actions

    def get(self, entry):
        if entry == 'position':
            return self.position
        elif entry == 'target':
            return self.target
        elif entry == 'orientation':
            return self.orientation
        elif entry == 'targetOrientation':
            return self.targetOrientation
        elif entry == 'transAngle':
            return self.transAngle
        elif entry == 'cmdType':
            return self.cmdType
        elif entry == 'vMax':
            return self.vMax
        elif entry == 'vLeft':
            return self.vLeft
        elif entry == 'vRight':
            return self.vRight
        elif entry == 'actions':
            return self.actions

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
        elif entry == 'actions':
            self.actions = value


