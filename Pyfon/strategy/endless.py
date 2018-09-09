class Endless:

    def __setup(self):
        pixelMeterRatio = self.width / 1.70 # o campo tem 1m 70cm

        # tamanhos
        self.robotSize = round(0.08 * pixelMeterRatio)
        self.goalSize = (round(0.1 * pixelMeterRatio), round(0.4 * pixelMeterRatio))
        self.areaSize = (round(0.15 * pixelMeterRatio), round(0.7 * pixelMeterRatio))

        # coordenadas
        self.midField = (self.width / 2, self.height / 2)
        self.goal = (self.width - self.goalSize[0], self.height / 2)
        self.ourGoal = (self.goalSize[0], self.height / 2)

        # limites
        self.corner = self.width - self.goalSize[0] - self.areaSize[0]
        self.ourCorner = self.goalSize[0] + self.areaSize[0]
        self.goalTop = self.height / 2 - self.goalSize[1] / 2
        self.goalBottom = self.height / 2 + self.goalSize[1] / 2
        self.areaTop = self.height / 2 - self.areaSize[1] / 2
        self.areaBottom = self.height / 2 + self.areaSize[1] / 2

        print("Endless is set up.")

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__setup()

