from control.eunomia import Eunomia
from control.dice import Dice
from control.warrior import Warrior
from multiprocessing import Pool


class Zeus:
    """Class of robot Control

    Attributes:
        callback: function that should be call after all Control routines.
        warriors: Warrior() list with the information of the robots.
        nWarriors: Robots in play.
        robotsSpeeds: interface speed list.
        actions: Instance of class Eunomia() that calculates what is needed to find de robots velocities.
        translate: Instance of class Dice() that calculates the robots velocities.
    """

    def __init__(self, callback=None):
        """

        Args:
            callback:
        """

        self.callback = callback
        self.warriors = []
        self.nWarriors = 0
        self.robotsSpeed = [0, 0, 0]
        self.actions = Eunomia()
        self.translate = Dice()
        print("Zeus summoned")

    def updateSpeeds(self, robotA, robotB, robotC):
        """Get

        Args:
            robotA:
            robotB:
            robotC:

        Returns:

        """
        print("[Zeus] New speeds:")
        self.robotsSpeed[0] = robotA
        self.robotsSpeed[1] = robotB
        self.robotsSpeed[2] = robotC

        for robot in self.robotsSpeed:
            print(robot)

    def setup(self, nWarriors, width=100):
        """Zeus first movements

        This method must be called before using Zeus properly.
        Here is instantiated the Eunomia() and Dice() as well as the amount nWarriors of Warriors to be used.

        Args:
            nWarriors: Num of warriors in game
            width:

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
        """Transforms a list of dictionaries into a Warrior() list.

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
            strategia (list): List of dictionaries with information generated by Strategy0

        Returns:
            list: Object Warrior() list

        Raises:
            ValueError:

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
                    warriors[x].vMax = self.robotsSpeed[x]

                if "before" in info:
                    warriors[x].before = float(info["before"])

                if "obstacles" in info:
                    warriors[x].obstacles = info["obstacles"]

            elif strategia[x]["command"] == "spin":
                warriors[x].action.append(info["direction"])
                if "velocity" in info:
                    warriors[x].vMax = info["velocity"]
                else:
                    warriors[x].vMax = self.robotsSpeed[x]

            elif strategia[x]["command"] == "lookAt":
                warriors[x].orientation = info["pose"]["orientation"]
                warriors[x].vMax = 0.8
                if type(info["target"]) is float:
                    warriors[x].targetOrientation = info["target"]
                    warriors[x].action.append("orientation")
                else:
                    warriors[x].position = info["pose"]["position"]
                    warriors[x].target = info["target"]
                    warriors[x].action.append("target")

            elif strategia[x]["command"] == "stop":
                warriors[x].vMax = 0
                warriors[x].before = float(info["before"])

        return warriors

    def controlRoutine(self):
        """Action and Translate call

        Flow of calculations to generate the PWM's that will be passed to the communication.
        Actions performs the calculations based on the commands set by the Strategy.
        Translate takes the data generated by Actions and calculates the final speed of each wheel.

        Returns:
            list: Velocities list of each wheel of the robots returned by Translate.

        """

        # TODO(Luana) Testar paralelização com um(1) processo para cada robô.
        velocities = []
        for warrior in self.warriors:
            if len(warrior.action) > 0:
                velocities.append(self.translate.run(self.actions.run(warrior)))

        # with Pool(processes=3) as pool:
        #    warriors = pool.map(self.actions.run, self.warriors)
        #    velocities = pool.map(self.translate.run, warriors)

        return velocities

    def generateOutput(self, velocities):
        """Generation of output data

        This method generates list of dictionaries with the speeds of each robot.

        Args:
            velocities (list): List with the speeds of each wheels of each robot.

        Returns:
            list: List of dictionary ready to be sent to the Communication(Hermes).

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
