class Warrior:
    def __init__(self):
        self.position = {
            "x": 0,
            "y": 0
        }
        self.orientation = 0
        self.command = ""

    def setup(self, position, orientation = 0):
        self.position = position
        self.orientation = orientation