# coding=utf-8
from control.eunomia import Eunomia
from control.dice import Dice
from control.warrior import Warrior
import numpy

# TODO é possível fazer os cálculos em paralelo para cada robô?


class Zeus:
    """Classe Control

    Essa classe está responsável pelos cáculos necessários afim de se encontrar a devida velocidade dos robôs dado
    um comando enviado pela estratégia. Essa etapa do programa precede o envio de mensagens aos robôs.

    Attributes:
        warriors: Lista de Warrior() com as informações dos robôs.
        nWarriors: Quantidade de robôs em jogo.
        robotsSpeed: Velocidades dos robôs que são setadas na interface
        actions: Instãncia da classe Eunomia() que calcula o necessário para encontrar as velocidades dos robos.
        translate: Instância da classe Dice() que calcula as velocidades dos robôs.
    """

    def __init__(self):
        self.warriors = None
        self.nWarriors = None
        self.robotsSpeed = None
        self.actions = None
        self.translate = None

        print("Zeus summoned")

    def setup(self, nWarriors):
        """Primeiros passos de Zeus

        Esse método deve ser chamado antes de se usar Zeus apropriadamente.
        Aqui é instânciado Eunomia() e Dice() bem como são setados a quantidade nWarriors de warriors.

        Args:
            nWarriors: Número de warriors em jogo.
        """

        self.actions = Eunomia().setup()
        self.translate = Dice().setup()

        self.nWarriors = nWarriors

        self.warriors = []
        self.robotsSpeed = []
        for i in range(0, nWarriors):
            self.warriors.append(Warrior())
            self.robotsSpeed.append(0.0)

        print("Zeus is set up")

        return self

    def updateSpeeds(self, robots):
        """Atualização de velocidades

        Esse método recebe uma lista de velocidades que são setadas na interface.
        O mesmo é chamado toda vez que há uma mudança na interface.

        Args:
            robots: Lista de velocidades em double
        """

        print("[Zeus] New speeds:")
        for i in range(0, len(robots)):
            self.robotsSpeed[i] = robots[i]
            print(self.robotsSpeed[i])

    def reset(self):
        """Método para resetar uma varivável de tempo de transição

        Esse método reseta a variável de tempo de transição utilizado em Dice() no controle de transição
        do backwards em vectorControl e positionControl
        """

        self.translate.reset()

    def getVelocities(self, strategia):
        """Método principal de Zeus

        Recebe dados retornados pela estratégia e gera uma lista de Warrior() em getWarriors.
        Essa lista é encaminhada para o controlRoutine onde serão feitos as chamadas de action.run
        e translate.run para cada warrior in game e, ao final dessa rotina, é obtido uma lista com
        as velocidades de cada roda dos warrios que serão enviadas para generateOutput afim de se obter
        uma lista de dicionários com esses valores.

        Args:
            strategia: Lista de dicionários com as informações geradas pelo Strategy

        Returns:
            list: Informações a serem passadas para Comunicação(Hermes)

        """

        self.warriors = self.getWarriors(strategia)
        velocities = self.generateOutput(self.controlRoutine(), strategia)
        return velocities

    def getWarriors(self, strategia):
        """Transforma uma lista de dicionário em uma lista de Warrior().

        Seta os atributos do object Warrior() baseado nas informações passadas pela estratégia.
        Ações que podem ser escolhidas estão listadas abaixo:
            - {
                "command": "goTo",
                "data": {
                    "obstacles": [(x, y)] # opcional - se passado, desviar de tais obstaclos
                    "pose": { "position": (x, y), "orientation": θ radianos },
                    "target": {
                        "position": (x, y),
                        "orientation": θ rad|(x, y)  # opcional: pode ser uma orientação final ou uma posição de lookAt
                        },
                    "velocity": X m/s
                        # opcional: se passado, sem before, é a velocidade constante/com before é velocidade padrão
                    "before": X s
                        # se passado sem o velocity, usa a velocidade máxima do robô como teto
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
                        "position": (x, y),  # opcional: é passado se o target for um ponto
                        "orientation": θ rad
                    },
                    "target": θ rad | (x, y)
                }
            }

            - {
                "command": stop,
                "data": {before: 0}
            }

        Args:
            strategia: Lista de dicionário com informações geradas pelo módulo de estratégia.

        Returns:
            list: Lista de Warrior().

        Raises:
            ValueError:
                Se tamanho da lista informado pela estratégia não for equivalente ao número de robos;
                Se os elementos da lista 'estretegia' não for dicionários;
                Se nos dicionários não conterem as key's "command" e "data";
                Se os comandos em "command" forem diferentes de: goTo, spin, lookAt ou stop.

        """

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
                warriors[x].position = numpy.asarray(info["pose"]["position"], dtype=float)
                warriors[x].orientation = float(info["pose"]["orientation"])

                warriors[x].target = numpy.asarray(info["target"]["position"], dtype=float)
                if type(info["target"]["orientation"]) is tuple:
                    warriors[x].targetOrientation = numpy.asarray(info["target"]["orientation"], dtype=float)
                else:
                    warriors[x].targetOrientation = float(info["target"]["orientation"])

                if "velocity" in info:
                    warriors[x].vMax = numpy.asarray(info["velocity"], dtype=float)
                else:
                    warriors[x].vMax = self.robotsSpeed[x]

                if "before" in info:
                    warriors[x].before = float(info["before"])

                if "obstacles" in info:
                    warriors[x].obstacles = numpy.asarray(info["obstacles"], dtype=float)

            elif strategia[x]["command"] == "spin":
                warriors[x].action.append(info["direction"])

                if "velocity" in info:
                    warriors[x].vMax = numpy.asarray(info["velocity"], dtype=float)
                else:
                    warriors[x].vMax = self.robotsSpeed[x]

            elif strategia[x]["command"] == "lookAt":
                warriors[x].orientation = float(info["pose"]["orientation"])

                if "velocity" in info:
                    warriors[x].vMax = numpy.asarray(info["velocity"], dtype=float)
                else:
                    warriors[x].vMax = self.robotsSpeed[x]

                if type(info["target"]) is not tuple:
                    warriors[x].targetOrientation = float(info["target"])
                    warriors[x].action.append("orientation")
                else:
                    warriors[x].position = numpy.asarray(info["pose"]["position"], dtype=float)
                    warriors[x].target = numpy.asarray(info["target"], dtype=float)
                    warriors[x].action.append("target")

            elif strategia[x]["command"] == "stop":
                warriors[x].vMax = 0.0
                warriors[x].before = float(info["before"])

            warriors[x].backward = self.warriors[x].backward
            warriors[x].front = self.warriors[x].front
            warriors[x].velAcc = self.warriors[x].velAcc

        return warriors

    def controlRoutine(self):
        """Chamadas de action e translate

        Fluxo de cálculos para a geração de PWM's que serão passados para comunicação.
        Actions faz os cálculos baseados nas informações passadas para estratégia.
        Translate pega os dados gerados pelo Actions e calcula a velocidade final de cada roda.

        Returns:
            list: Lista com velocidades de cada roda dos robos.

        """

        velocities = []
        for warrior in self.warriors:
            if len(warrior.action) > 0:
                velocities.append(self.translate.run(self.actions.run(warrior)))

        return velocities

    def generateOutput(self, velocities, strategia):
        """Gera os dados de saida

        Esse método gera uma lista de dicionários com as velocidades de cada robo.

        Args:
            velocities: Lista com as velocidades de cada roda de cada robo.
            strategia: Informações da estratégia. Usado para inserir os Id's dos respectivos robos.

        Returns:
            list: Lista de dicionário pronto para ser enviado para Communication(Hermes).

        """
        output = []
        for x in range(0, self.nWarriors):
            output.append(
                {
                    "robotLetter": strategia[x]["robotLetter"],
                    "vLeft": velocities[x][0],
                    "vRight": velocities[x][1],
                    "vector": velocities[x][2]
                }
            )

        return output
