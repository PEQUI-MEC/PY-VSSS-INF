class Warrior:


    def __init__(self, defaultVel = 0.8, name = "pericles"):
        self.name = name
        self.defaultVel = defaultVel

        self.position = (0, 0)
        self.orientation = 0

        self.tactics = "wait"

        self.command = {}

    def setup(self, position, orientation = 0):
        self.position = position
        self.orientation = orientation