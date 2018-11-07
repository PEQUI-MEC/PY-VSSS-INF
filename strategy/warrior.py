class Warrior:

    def __init__(self, defaultVel=0.8):
        self.robotID = "A"

        self.defaultVel = defaultVel
        self.maxVel = 1
        self.velEstimated = 0

        self.robotID = "A"
        self.lastPosition = (0, 0)
        self.position = (0, 0)
        self.orientation = 0

        self.positionLocked = False
        self.actionTimer = 0
        self.lockedTime = 0

        self.tactics = "wait"

        self.spiral = 1

        # ângulo do robô com a bola
        self.robotBall = 0
        # angulo entre as retas robo->bola e bola->gol
        self.robotBallGoal = 0
        # orientação do robô em relação ao gol
        self.robotGoal = 0
        # o robô tem ângulo bom pra chutar?
        self.hasKickAngle = False

        self.command = {}

    def setup(self, robotID, position, orientation=0):
        self.robotID = robotID
        self.lastPosition = self.position
        self.position = position
        self.orientation = orientation

    def setDefaultVel(self, defaultVel):
        self.defaultVel = defaultVel
