# coding=utf-8
from math import atan2, cos, sin
from .navigation import UnivectorField
from helpers.endless import Endless
from helpers.decorators import timeToFinish
import numpy


class Eunomia:
    """Módulo de ações

    Essa classe é responsável por fazer os pré-cálculos necessários para encontrar as velocidades das rodas.

    Attributes:
        uvf: Instância da classe UnivectorField()
        warrior: Objeto Warrior()
        radius: Constante raio da espiral hiperbólica
        kr: Constante de suavização da espiral hiperbólica
        k0: Constante multiplicativa do vetor de deslocamento do cálculo da posição virtual
        dMin: Distância mínima entre o robô e um obstáculo
        lDelta: Constante Gaussiana
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
        """Primeiros passos de Eunomia
        Esse método deve ser chamado antes de usar Eunomia apropriadamente. Aqui é inicializado todas as constantes
        usadas no univector field.
        """
        self.uvf = UnivectorField()
        self.radius = 50.0
        self.kr = 5.9  # 0.9
        self.k0 = 0.12
        self.dMin = 20.0
        self.lDelta = 4.5

        return self

    # @timeToFinish
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
        """Comando stop

        Esse método é utilizado quando deseja-se que o robô pare de se locomover. Seu cmdtype é 'SPEED'.
        """
        # TODO Fazer controle de desesceleração?
        self.warrior.vLeft = 0.0
        self.warrior.vRight = 0.0

    def spin(self):
        """Comando spin

        Esse método é utilizado quando deseja-se que o robô gire para alguma direção (horário ou anti-horário). Seu
        cmdtype é 'SPEED'.
        """

        if self.warrior.action[1] == "clockwise":
            self.warrior.vLeft = self.warrior.vMax
            self.warrior.vRight = -self.warrior.vMax
        else:
            self.warrior.vLeft = -self.warrior.vMax
            self.warrior.vRight = self.warrior.vMax

    def lookAt(self):
        """Comando lookAt

        Esse método é utilizado quando deseja-se que o robô fique com uma das suas frentes voltada para uma orientação
        desejada. Se a segunda opção de ação for 'target' será calculado em qual direção o ponto passado está. Seu
        cmdtype é 'ORIENTATION'.

        Raises:
            ValueError: Se a segunda opção de ação não for 'target' nem 'orientation'.
        """
        if self.warrior.action[1] is "target":
            x = self.warrior.target[0] - self.warrior.position[0]
            y = self.warrior.target[1] - self.warrior.position[1]
            self.warrior.targetOrientation = atan2(y, -x)

        elif self.warrior.action[1] is not "orientation":
            raise ValueError("Invalid data.")

    def goTo(self):
        """Comando goTo

        Esse método é utilizado quando deseja-se ir para algum ponto, ou andar em direção à aguma orientação desejada. O
        método recebe a posição e orientação atual do robô bem como uma posição alvo. Para que o robô chegue no alvo com
        uma orientação final desejada (targetOrientation) é passado um ponto ou um valor de orientação. Se para
        orientação final for passado um valor de orientação é então calculado um ponto situado na direção desejada para
        que no univectorField o campo seja gerado levando esse ponto como referencial. O método também permite que possa
        ser passado pontos de obstáculos que deverão ser desviados.

        Atualmente, o raio da espiral hiberbólica do univectorField varia de acordo com a distância do robô para com o
        alvo, e de acordo com a distância do robô com as bordas do campo, com o objetivo de suavizar as curvas e evitar
        com que os robôs fiquem presos nas paredes do campo.
        """

        # TODO testar colocar obstáculos nas bordas do campo para evitar que o robô bata de cara nelas.

        # Se o targetOrientation passado não for um ponto
        if not isinstance(self.warrior.targetOrientation, numpy.ndarray):
            theta = atan2(sin(self.warrior.targetOrientation), -cos(self.warrior.targetOrientation))
            target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]
            del self.warrior.targetOrientation
            self.warrior.targetOrientation = target

        # TODO otimizar variação da espiral
        if self.warrior.position[1] >= Endless.areaTop:
            spiral = 0.06
        elif self.warrior.position[1] < Endless.areaBottom:
            spiral = 0.06
        elif numpy.linalg.norm(self.warrior.position[0] - self.warrior.target[0]) > 250.0:
            spiral = 1.0
        else:
            spiral = 0.1

        self.warrior.vRight = self.warrior.vMax
        self.warrior.vLeft = self.warrior.vMax
        self.uvf.updateConstants(self.radius*spiral, self.kr, self.k0, self.dMin, self.lDelta)
        self.warrior.transAngle = self.uvf.univector(robotPos=self.warrior.position,
                                                     robotSpeed=[self.warrior.vLeft, self.warrior.vRight],
                                                     target=self.warrior.target,
                                                     obstacles=self.warrior.obstacles,
                                                     orientation=self.warrior.targetOrientation)
