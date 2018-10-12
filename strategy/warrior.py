class Warrior:

    def __init__(self, defaultVel=0.8):
        self.defaultVel = defaultVel

        self.position = (0, 0)
        self.orientation = 0

        self.tactics = "wait"

        self.command = {}

    def setup(self, position, orientation=0):
        self.position = position
        self.orientation = orientation

    def setDefaultVel(self, defaultVel):
        self.defaultVel = defaultVel
