class Velocity:
    def __init__(self):
        self.id = -1
        self.left_wheel = 0
        self.right_wheel= 0
        

    def setup(self, id, left_wheel, right_wheel):
        self.id = id
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel