class Warrior:

    def __init__(self, defaultVel=0.8):
        self.defaultVel = defaultVel
        self.maxVel = 1.4

        self.robotID = "A"
        self.lastPosition = (0, 0)
        self.position = (0, 0)
        self.orientation = 0

        self.positionLocked = False
        self.actionTimer = 0
        self.lockedTime = 0

        self.tactics = "wait"

        self.command = {}

    def setup(self, robotID, position, orientation=0):
        self.robotID = robotID
        self.lastPosition = self.position
        self.position = position
        self.orientation = orientation

    def setDefaultVel(self, defaultVel):
        self.defaultVel = defaultVel
