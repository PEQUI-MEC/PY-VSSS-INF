from math import atan2, cos, sin
from .navigation import UnivectorField
from helpers.endless import Endless
import numpy


class Eunomia:
    """
        Attributes:
            uvf:
            warrior:
            radius:
            kr:
            k0:
            dMin:
            lDelta:
    """
    def __init__(self):
        self.uvf = None
        self.warrior = None
        self.radius = None
        self.kr = None
        self.k0 = None
        self.dMin = None
        self.lDelta = None

    def setup(self):
        """
        Espiral radius, moveToGoal kr, avoidObstacles k0, distance dmin, gaussian delta
        """
        self.uvf = UnivectorField()
        self.radius = 50.0
        self.kr = 5.9  # 0.9
        self.k0 = 0.12
        self.dMin = 20.0
        self.lDelta = 4.5

        return self

    def run(self, warrior):
        """Método principal do controle de Ações

        Recebe um objeto do tipo Warrior(). De acordo com o tipo de ação de warrior, chama-se o respectivo método que
        irá tratar e calcular corretamente todos os dados necessários para a geração de velocidades.

        Args:
            warrior: Objeto Warrior().

        Returns:
            Warrior(): Objeto com as variáveis calculadas e prontas para geração de velocidades.

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
        if self.warrior.action[1] == "clockwise":
            self.warrior.vLeft = self.warrior.vMax
            self.warrior.vRight = -self.warrior.vMax
        else:
            self.warrior.vLeft = -self.warrior.vMax
            self.warrior.vRight = self.warrior.vMax

    def lookAt(self):
        if self.warrior.action[1] is "target":
            x = self.warrior.target[0] - self.warrior.position[0]
            y = self.warrior.target[1] - self.warrior.position[1]
            self.warrior.targetOrientation = atan2(y, -x)

        elif self.warrior.action[1] is not "orientation":
            raise ValueError("Invalid data.")

    def goTo(self):
        # Se o targetOrientation passado não for um ponto
        if not isinstance(self.warrior.targetOrientation, numpy.ndarray):
            theta = atan2(sin(self.warrior.targetOrientation), -cos(self.warrior.targetOrientation))
            target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]
            del self.warrior.targetOrientation
            self.warrior.targetOrientation = target

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        # if warrior.before is not None:
        #   time = warrior.before

        if self.warrior.position[1] >= Endless.areaTop:
            spiral = 0.06
        elif self.warrior.position[1] < Endless.areaBottom:
            spiral = 0.06
        elif numpy.linalg.norm(self.warrior.position[0] - self.warrior.target[0]) > 250.0:
            spiral = 1.0
        else:
            spiral = 0.1

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
