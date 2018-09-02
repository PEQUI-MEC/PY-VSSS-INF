class Endless:

    def __setup(self):
        self.midField = {
            "x": self.width / 2,
            "y": self.height / 2
        }
        self.ourGoal = {
            "x": 0,
            "y": self.height / 2
        }
        self.goal = {
            "x": self.width,
            "y": self.height / 2
        }
        print("Endless is set up.")

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__setup()

