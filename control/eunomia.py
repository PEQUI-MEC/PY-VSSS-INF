from math import atan2, cos, sin
from scipy.spatial import distance
from .navigation import UnivectorField
from helpers.endless import Endless
import numpy


class Eunomia:
    def __init__(self):
        self.uvf = UnivectorField()
        self.warrior = None
        self.radius = None
        self.kr = None
        self.k0 = None
        self.dMin = None
        self.lDelta = None

    def setup(self):
        # radius = 0.2*width/1.70
        # Espiral radius, moveToGoal kr, avoidObstacles k0, distance dmin, gaussian delta
        # self.uvf.updateConstants(radius=6.0, kr=0.9, k0=0.12, dMin=20.0, lDelta=4.5)
        self.radius = 50.0
        self.kr = 5.9  # 0.9
        self.k0 = 0.12
        self.dMin = 20.0
        self.lDelta = 4.5

        # print("Corner ", Endless.corner)
        # print("OurConer ", Endless.ourCorner)
        # print("Golie ", Endless.goalieLine)
        # print("area ", Endless.areaLine)

    def run(self, warrior):
        """Main method of action controller

        Recebe um objeto do tipo Warrior(). De acordo com o tipo de ação de warrior, chama-se o respectivo método que
        irá tratar e calcular corretamente todos os dados necessários para a geração de velocidades.

        Args:
            warrior:

        Returns:
            Warrior(): objeto com as variáveis calculadas e prontas para geração de velocidades

        """

        self.warrior = warrior

        if warrior.action[0] == "stop":
            warrior.cmdType = "SPEED"
            self.stop()

        elif warrior.action[0] == "spin":
            warrior.cmdType = "SPEED"
            self.spin()

        elif warrior.action[0] == "lookAt":
            warrior.cmdType = "ORIENTATION"
            self.lookAt()

        elif warrior.action[0] == "goTo":
            warrior.cmdType = "VECTOR"
            self.goTo()

        return self.warrior

    def stop(self):
        if self.warrior.before == 0:
            self.warrior.vLeft = 0.0
            self.warrior.vRight = 0.0

        else:
            # TODO Fazer controle de desesceleração
            self.warrior.vLeft = 0.0
            self.warrior.vRight = 0.0

    def spin(self):
        """Command Spin

          - {
                "command": "spin",
                "data": { "velocity": X m/s, "direction": "clockwise" | "counter"}
            }
        """

        if self.warrior.action[1] == "clockwise":
            self.warrior.vLeft = self.warrior.vMax
            self.warrior.vRight = -self.warrior.vMax
        else:
            self.warrior.vLeft = -self.warrior.vMax
            self.warrior.vRight = self.warrior.vMax

    def lookAt(self):
        """Command lookAt

        - {
            "command": "lookAt",
            "data": {
                "pose": {
                    "position": (x, y),  # opcional - é passado se o target for um ponto
                    "orientation": θ radianos
                },
                "target": θ radianos | (x, y)
            }
        }
        """

        if self.warrior.action[1] is "target":
            x = self.warrior.target[0] - self.warrior.position[0]
            y = self.warrior.target[1] - self.warrior.position[1]
            self.warrior.targetOrientation = atan2(y, -x)

        elif self.warrior.action[1] is not "orientation":
            raise ValueError("Invalid data.")

    def goTo(self):
        """Command goTo

        - {
            "command": "goTo",
            "data": {
                "obstacles": [(x, y)] # opcional - se passado, desviar de tais obstaclos
                "pose": {"position": (x, y), "orientation": θ radianos},
                "target": {"position": (x, y), "orientation": θ radianos | (x, y)},  # opcional - pode ser uma orientação final ou uma posição de lookAt
                "velocity": X m/s,  # opcional - se passado, sem before, é a velocidade constante / com before é velocidade padrão
                "before": X s  # se passado sem o velocity, usa a velocidade máxima do robô como teto
            }
        }
        """

        # Se o targetOrientation passado não for um ponto+
        if not isinstance(self.warrior.targetOrientation, numpy.ndarray):
            theta = atan2(sin(self.warrior.targetOrientation), -cos(self.warrior.targetOrientation))
            target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]
            del self.warrior.targetOrientation
            self.warrior.targetOrientation = target

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        # if warrior.before is not None:
        #   time = warrior.before

        spiral = 0.1
        if self.warrior.position[1] >= Endless.areaTop:
            spiral = 0.06
        elif self.warrior.position[1] < Endless.areaBottom:
            spiral = 0.06

        elif distance.euclidean(self.warrior.position[0], self.warrior.target[0]) > 250.0:
            spiral = 1.0

        if time is None:
            self.warrior.vRight = self.warrior.vMax
            self.warrior.vLeft = self.warrior.vMax
            self.uvf.updateConstants(self.radius*spiral, self.kr, self.k0, self.dMin, self.lDelta)
            self.warrior.transAngle = self.uvf.univector(robotPos=self.warrior.position,
                                                         robotSpeed=[self.warrior.vLeft, self.warrior.vRight],
                                                         target=self.warrior.target,
                                                         obstacles=self.warrior.obstacles,
                                                         ostaclesSpeed=self.warrior.obstaclesSpeed,
                                                         orientation=self.warrior.targetOrientation)
        else:
            # TODO Fazer verificação se é possível realizar o trajeto com o tempo requisitado
            pass
