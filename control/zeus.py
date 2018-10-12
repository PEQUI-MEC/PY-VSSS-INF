from control.eunomia import Eunomia
from control.dice import Dice
from control.warrior import Warrior


class Zeus:

    def __init__(self, callback):
        self.callback = callback

        self.warriors = []
        self.nWarriors = 0
        self.maxVelocity = 1.0
        self.attackSpeed = None
        self.defenseSpeed = None
        self.goalkeeperSpeed = None
        self.actions = Eunomia()
        self.translate = Dice()
        print("Zeus summoned")

    def updateSpeeds(self, attackSpeed, defenseSpeed, goalkeeperSpeed):
        self.attackSpeed = attackSpeed
        self.defenseSpeed = defenseSpeed
        self.goalkeeperSpeed = goalkeeperSpeed

    def setup(self, nWarriors, width=100):
        """Zeus first movements

        Esse método deverá ser chamado antes de usar Zeus apropriadamente.
        Aqui é instânciado o Actions e o Translate bem como a quantidade nWarriors de Warriors a serem usados.

        Args:
            nWarriors (int): Num of warriors in game
            width (int):

        Returns:

        """

        self.actions.setup(width)
        self.nWarriors = nWarriors

        for i in range(0, nWarriors):
            self.warriors.append(Warrior())

        print("Zeus is set up")
        return self

    def getVelocities(self, strategia):
        """Zeus main method

        Recebe dados retornados pela estratégia e gera uma lista de Warrior() em getWarriors.
        Essa lista é encaminhada para o controlRoutine onde serão feitos as chamadas de action.run
        e translate.run para cada warrior in game e, ao final dessa rotina, é obtido uma lista com
        as velocidades de cada roda dos warrios que serão enviadas para generateOutput afim de se obter
        uma lista de dicionários com esses valores.

        Args:
            strategia (list): Lista de dicionários com as informações geradas pelo Strategy

        Returns:
            list: Informações a serem passadas para Comunicação(Hermes)

        """

        self.warriors = self.getWarriors(strategia)
        velocities = self.generateOutput(self.controlRoutine())
        self.callback(velocities)
        return velocities

    def getWarriors(self, strategia):
        """Transforma uma lista de dicionários em uma lista de Warrior()

        Seta os atributos do object Warrior() baseado nas informações passadas pela estratégia. Ações que podem ser escolhidas:
        - {
            "command": "goTo",
            "data": {
                "obstacles": [(x, y)] # opcional - se passado, desviar de tais obstaclos
                "pose": { "position": (x, y), "orientation": θ radianos },
                "target": {
                    "position": (x, y),
                    "orientation": θ radianos | (x, y)  # opcional - pode ser uma orientação final ou uma posição de lookAt
                    },
                "velocity": X m/s,  # opcional - se passado, sem before, é a velocidade constante / com before é velocidade padrão
                "before": X s  # se passado sem o velocity, usa a velocidade máxima do robô como teto
            }
        }
        - {
            "command": "spin",
            "data": { "velocity": X m/s, "direction": "clockwise" | "counter" }
        }
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
        - {
            "command": stop,
            "data": {before: 0}
        }

        Args:
            strategia (list): Lista de dicionários com as informações geradas pelo Strategy

        Returns:
            list: Lista de object Warrior()

        """

        # TODO(Luana) Testar paralelização com um(1) processo para cada robô.
        warriors = []
        if type(strategia) is not list or \
                len(strategia) != self.nWarriors:
            raise ValueError("Invalid data object received.")

        for i in range(0, self.nWarriors):
            if type(strategia[i]) is not dict:
                raise ValueError("Invalid data object received.")

            if ("command" in strategia[i]) is False or \
                    ("data" in strategia[i]) is False:
                raise ValueError("Invalid data object received.")

            warriors.append(Warrior())

        for x in range(0, len(strategia)):
            if strategia[x]["command"] is not "goTo" and \
                    strategia[x]["command"] is not "spin" and \
                    strategia[x]["command"] is not "lookAt" and \
                    strategia[x]["command"] is not "stop":
                raise ValueError("Invalid command.")

            warriors[x].action.append(strategia[x]["command"])
            info = strategia[x]["data"]

            if strategia[x]["command"] == "goTo":
                warriors[x].position = info["pose"]["position"]
                warriors[x].orientation = info["pose"]["orientation"]

                warriors[x].target = info["target"]["position"]
                warriors[x].targetOrientation = info["target"]["orientation"]

                if "velocity" in info:
                    warriors[x].vMax = info["velocity"]
                else:
                    warriors[x].vMax = self.maxVelocity

                if "before" in info:
                    warriors[x].before = float(info["before"])

                if "obstacles" in info:
                    warriors[x].obstacles = info["obstacles"]

            elif strategia[x]["command"] == "spin":
                warriors[x].vMax = info["velocity"]
                warriors[x].action.append(info["direction"])

            elif strategia[x]["command"] == "lookAt":
                warriors[x].orientation = info["pose"]["orientation"]
                if type(info["target"]) is float:
                    warriors[x].targetOrientation = info["target"]
                    warriors[x].action.append("orientation")
                else:
                    warriors[x].position = info["pose"]["position"]
                    warriors[x].target = info["target"]
                    warriors[x].action.append("target")

            elif strategia[x]["command"] == "stop":
                warriors[x].before = float(info["before"])

        return warriors

    def controlRoutine(self):
        """Action and Translate call

        Fluxo de cálculos para gerar os pwm's que serão passados para a comunicação
        Actions() realiza os cálculos baseados nos comandos setados pela estratégia
        Translate() pega os dados gerados pelo Actions() e calcula a velocidade final de cada roda

        Returns:
            list: Lista com as velicidades de cada roda dos robôs retornadas pelo Translate.

        """

        # TODO(Luana) Testar paralelização com um(1) processo para cada robô.
        velocities = []
        for warrior in self.warriors:
            if len(warrior.action) > 0:
                velocities.append(self.translate.run(self.actions.run(warrior)))

        return velocities

    def generateOutput(self, velocities):
        """Padronização dos dados de saída

        Gera lista de dicionários com as velocidades de cada robô.

        Args:
            velocities (list): Lista com as velicidades de cada roda dos robôs.

        Returns:
            list: Lista de dicionário pronto para ser enviado para a Comunicação(Hermes).

        """

        output = [
            {
                "vLeft": velocities[0][0],
                "vRight": velocities[0][1]
            },
            {
                "vLeft": velocities[1][0],
                "vRight": velocities[1][1]
            },
            {
                "vLeft": velocities[2][0],
                "vRight": velocities[2][1]
            }
        ]

        return output
