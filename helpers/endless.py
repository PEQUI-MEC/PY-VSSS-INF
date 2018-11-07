class Endless:
    height = 0
    width = 0
    pixelMeterRatio = 0
    robotSize = 0
    spinSize = 0
    robotRadius = 0
    goalSize = 0
    areaSize = 0
    midField = 0
    goal = 0
    pastGoal = 0
    ourGoal = 0
    topSide = 0
    bottomSide = 0
    corner = 0
    ourCorner = 0
    goalTop = 0
    goalBottom = 0
    areaTop = 0
    areaBottom = 0
    goalieLine = 0
    areaLine = 0
    areaBorderOffset = 0
    goalieOffset = 0
    areaOffset = 0

    @staticmethod
    def setup(width, height):
        Endless.width = width
        Endless.height = height
        Endless.pixelMeterRatio = width / 1.70  # o campo tem 1m 70cm

        # tamanhos
        Endless.robotSize = round(0.08 * Endless.pixelMeterRatio)
        Endless.spinSize = Endless.robotSize * 1.2
        Endless.robotRadius = Endless.robotSize / 2
        Endless.goalSize = (round(0.1 * Endless.pixelMeterRatio), round(0.4 * Endless.pixelMeterRatio))
        Endless.areaSize = (round(0.15 * Endless.pixelMeterRatio), round(0.8 * Endless.pixelMeterRatio))

        # coordenadas
        Endless.midField = (Endless.width / 2, Endless.height / 2)
        Endless.goal = (Endless.width, Endless.height / 2)
        Endless.pastGoal = (Endless.width + Endless.areaSize[0], Endless.height / 2)
        Endless.ourGoal = (Endless.goalSize[0], Endless.height / 2)

        # offsets
        Endless.areaBorderOffset = 0
        Endless.goalieOffset = 0
        Endless.areaOffset = 0

        # limites
        Endless.topSide = Endless.height - Endless.robotSize
        Endless.bottomSide = Endless.robotSize
        Endless.corner = Endless.width - Endless.goalSize[0] - Endless.areaSize[0]  # em X
        Endless.ourCorner = Endless.areaSize[0]  # em X
        Endless.goalTop = Endless.height / 2 + Endless.goalSize[1] / 2  # em Y
        Endless.goalBottom = Endless.height / 2 - Endless.goalSize[1] / 2  # em Y
        Endless.areaTop = Endless.height / 2 + Endless.areaSize[1] / 2 + Endless.areaBorderOffset  # em Y
        Endless.areaBottom = Endless.height / 2 - Endless.areaSize[1] / 2 - Endless.areaBorderOffset  # em Y
        Endless.goalieLine = Endless.goalSize[0] + Endless.robotSize + Endless.goalieOffset  # em X
        Endless.areaLine = Endless.goalSize[0] + Endless.areaSize[0] + Endless.robotSize + Endless.areaOffset  # em X

        print("Endless is set up.")
