from math import atan2
from .navigation import UnivectorField


class Eunomia:
    """Action Controller

    Attributes:
        uvf : Instance of Univector Field class. This class manager all robot navigation.
    """

    def __init__(self):
        self.uvf = UnivectorField()
        self.warrior = None

    def setup(self, width=100):
        """

        Args:
            width:

        Returns:

        """

        # radius = 0.2*width/1.70
        # Espiral radius, moveToGoal kr, avoidObstacles k0, distance dmin, gaussian delta
        self.uvf.updateConstants(radius=6.0, kr=5.9, k0=0.12, dMin=5.0, lDelta=4.5)

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

    def stop(self, ):
        """Command Stop

        - {
            "command": stop,
            "data": {}
        }

        Args:
            warrior:

        Returns:

        """

        if self.warrior.before == 0:
            self.warrior.vLeft = 0
            self.warrior.vRight = 0

        else:
            # TODO Fazer controle de desesceleração
            self.warrior.vLeft = 0
            self.warrior.vRight = 0

    def spin(self):
        """Command Spin

          - {
                "command": "spin",
                "data": { "velocity": X m/s, "direction": "clockwise" | "counter"}
            }

        Args:
            warrior:

        Returns:

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

        Args:
            warrior:

        Returns:

        """

        if self.warrior.action[1] is "orientation":
            self.warrior.orientation = self.warrior.targetOrientation

        elif self.warrior.action[1] is "target":
            x = self.warrior.target[0] - self.warrior.position[0]
            y = self.warrior.target[1] - self.warrior.position[1]
            self.warrior.targetOrientation = atan2(y, -x)

        else:
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

        Args:
            warrior:

        Returns:

        """

        # Se o targetOrientation passado não for um ponto, gerar um ponto no infinito
        if type(self.warrior.targetOrientation) is not tuple:
            target = self.warrior.targetOrientation
            del self.warrior.targetOrientation

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        # if warrior.before is not None:
        #   time = warrior.before

        if time is None:
            self.warrior.vRight = self.warrior.vMax
            self.warrior.vLeft = self.warrior.vMax

            # print("\nwarrior ", list(warrior.position))
            # print("Target ", list(warrior.target))

            self.warrior.transAngle = self.uvf.univector(robotPos=list(self.warrior.position),
                                                         robotSpeed=[self.warrior.vLeft, self.warrior.vRight],
                                                         target=list(self.warrior.target),
                                                         obstacles=self.warrior.obstacles,
                                                         orientation=self.warrior.targetOrientation)
            # print("UVF " + str(warrior.transAngle))
        else:
            # TODO Fazer verificação se é possível realizar o trajeto com o tempo requisitado
            pass
