class Warrior:


    def __init__(self):
        self.name = ""
        self.position = (0, 0)
        self.orientation = 0
        self.command = ""

    def setup(self, position, orientation = 0, name = "pericles"):
        self.name = name
        self.position = position
        self.orientation = orientation