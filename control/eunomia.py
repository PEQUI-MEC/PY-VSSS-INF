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
        self.uvf.updateConstants(6.0, 5.9, 0.12, 5.0, 4.5)

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
            warrior.targetOrientation = self.lookAt(warrior.action[1], warrior.target,  warrior.position,
                                                    warrior.targetOrientation)
            return warrior

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
            # TODO(Luana) Fazer controle de desesceleração
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

    def lookAt(self, where, target, position, orientation=None):
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
            where:
            target:
            position:
            orientation:

        Returns:

        """
        if where is "orientation":
            return orientation

        elif where is "target":
            x = target[0] - position[0]
            y = target[1] - position[1]
            return atan2(y, -x)

        else:
            raise ValueError("Invalid data.")

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

        # Se o targetOrientation passado for um ponto, calcular o targetOrientation usando o lookAt
        if type(warrior.targetOrientation) is tuple:
            self.uvf.updateOrientation(list(warrior.targetOrientation))
            target = warrior.targetOrientation
            del warrior.targetOrientation
            warrior.targetOrientation = self.lookAt("target", target, warrior.position)
        # else:
            # TODO(Luana) Tratar se passado apenas uma orientação.
            # O uvf utiliza um ponto x,y para construir o plano de orientação final da espiral hiberbólica.

        # Verificar se existe obstáculos para se desviar
        if warrior.obstacles is not None:
            self.uvf.updateObstacles(warrior.obstacles, [[0, 0], [0, 0]])

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        # if warrior.before is not None:
        #   time = warrior.before

        if time is None:
            warrior.vRight = warrior.vMax
            warrior.vLeft = warrior.vMax

            print("\nwarrior ", list(warrior.position))
            print("Target ", list(warrior.target))

            warrior.transAngle = self.uvf.getVec(list(warrior.position), [warrior.vLeft, warrior.vRight],
                                                 list(warrior.target), warrior.targetOrientation)
            print("UVF " + str(warrior.transAngle))
        else:
            # TODO(Luana) Fazer verificação se é possível realizar o trajeto com o tempo requisitado
            pass

        return warrior
