from math import atan2
from .navigation import UnivectorField


class Eunomia:
    """Action Controller

    Attributes:
        uvf : Instance of Univector Field class. This class manager all robot navigation.
    """

    def __init__(self):
        self.uvf = UnivectorField()

    def setup(self, width=100):
        """

        Args:
            width:

        Returns:

        """

        # radius = 0.2*width/1.70
        # Espiral radius, moveToGoal kr, avoidObstacles k0, distance dmin, gaussian delta
        self.uvf.updateConstants(radius=6.0, kr=5.9, k0=0.12, dMinex=5.0, lDelta=4.5)

    def run(self, warrior):
        """Main method of action controller

        Recebe um objeto do tipo Warrior(). De acordo com o tipo de ação de warrior, chama-se o respectivo método que
        irá tratar e calcular corretamente todos os dados necessários para a geração de velocidades.

        Args:
            warrior:

        Returns:
            Warrior(): objeto com as variáveis calculadas e prontas para geração de velocidades

        """
        if warrior.action[0] == "stop":
            warrior.cmdType = "SPEED"
            return self.stop(warrior)

        elif warrior.action[0] == "spin":
            warrior.cmdType = "SPEED"
            return self.spin(warrior)

        elif warrior.action[0] == "lookAt":
            warrior.cmdType = "ORIENTATION"
            return self.lookAt(warrior)

        elif warrior.action[0] == "goTo":
            warrior.cmdType = "VECTOR"
            return self.goTo(warrior)

    def stop(self, warrior):
        """Command Stop

        - {
            "command": stop,
            "data": {}
        }

        Args:
            warrior:

        Returns:

        """

        if warrior.before == 0:
            warrior.vMax = 0
            warrior.vLeft = 0
            warrior.vRight = 0

        else:
            # TODO Fazer controle de desesceleração
            warrior.vMax = 0
            warrior.vLeft = 0
            warrior.vRight = 0

        return warrior

    def spin(self, warrior):
        """Command Spin

          - {
                "command": "spin",
                "data": { "velocity": X m/s, "direction": "clockwise" | "counter"}
            }

        Args:
            warrior:

        Returns:

        """

        if warrior.action[1] == "clockwise":
            warrior.vLeft = warrior.vMax
            warrior.vRight = -warrior.vMax
        else:
            warrior.vLeft = -warrior.vMax
            warrior.vRight = warrior.vMax

        return warrior

    def lookAt(self, warrior):
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

        if warrior.action[1] is "orientation":
            warrior.orientation = warrior.targetOrientation

        elif warrior.action[1] is "target":
            x = warrior.target[0] - warrior.position[0]
            y = warrior.target[1] - warrior.position[1]
            warrior.targetOrientation = atan2(y, -x)

        else:
            raise ValueError("Invalid data.")

        return warrior

    def goTo(self, warrior):
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
        if type(warrior.targetOrientation) is not tuple:
            target = warrior.targetOrientation
            del warrior.targetOrientation

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        # if warrior.before is not None:
        #   time = warrior.before

        if time is None:
            warrior.vRight = warrior.vMax
            warrior.vLeft = warrior.vMax

            # print("\nwarrior ", list(warrior.position))
            # print("Target ", list(warrior.target))

            warrior.transAngle = self.uvf.univector(robotPos=list(warrior.position),
                                                    robotSpeed=[warrior.vLeft, warrior.vRight],
                                                    target=list(warrior.target),
                                                    obstacles=warrior.obstacles,
                                                    orientation=warrior.targetOrientation)
            # print("UVF " + str(warrior.transAngle))
        else:
            # TODO Fazer verificação se é possível realizar o trajeto com o tempo requisitado
            pass

        return warrior
