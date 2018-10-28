class Warrior:

    def __init__(self, defaultVel=0.8):
        self.defaultVel = defaultVel

        self.robotID = "A"
        self.position = (0, 0)
        self.orientation = 0

        self.tactics = "wait"

        self.command = {}

    def setup(self, robotID, position, orientation=0):
        self.robotID = robotID
        self.position = position
        self.orientation = orientation

    def setDefaultVel(self, defaultVel):
        self.defaultVel = defaultVel
