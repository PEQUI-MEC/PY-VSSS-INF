class Endless:

    def __setup(self):
        self.pixelMeterRatio = self.width / 1.70  # o campo tem 1m 70cm

        # tamanhos
        self.robotSize = round(0.08 * self.pixelMeterRatio)
        self.goalSize = (round(0.1 * self.pixelMeterRatio), round(0.4 * self.pixelMeterRatio))
        self.areaSize = (round(0.15 * self.pixelMeterRatio), round(0.7 * self.pixelMeterRatio))

        # coordenadas
        self.midField = (self.width / 2, self.height / 2)
        self.goal = (self.width, self.height / 2)
        self.pastGoal = (self.width + self.areaSize[0], self.height / 2)
        self.ourGoal = (self.goalSize[0], self.height / 2)

        # limites
        self.corner = self.width - self.goalSize[0] - self.areaSize[0]  # em X
        self.ourCorner = self.goalSize[0] - self.areaSize[0]  # em X
        self.goalTop = self.height / 2 + self.goalSize[1] / 2  # em Y
        self.goalBottom = self.height / 2 - self.goalSize[1] / 2  # em Y
        self.areaTop = self.height / 2 + self.areaSize[1] / 2  # em Y
        self.areaBottom = self.height / 2 - self.areaSize[1] / 2  # em Y
        self.goalieLine = self.goalSize[0] + self.robotSize  # em X
        self.areaLine = self.goalSize[0] + self.areaSize[0] + self.robotSize  # em X

        print("Endless is set up.")

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__setup()

