from .actions import Actions
from .translate import Translate
from .warrior import Warrior


class Zeus:
    def __init__(self):
        self.warriors = []
        self.actions = None
        self.translate = None
        self.nWarriors = 0
        self.maxVelocity = 1.0
        print("Zeus summoned")

    '''
    Setup Zeus: nWarriors is the num of warriors in game
    '''
    def setup(self, nWarriors):
        self.actions = Actions()
        self.translate = Translate()
        self.nWarriors = nWarriors

        for i in range(0, nWarriors):
            self.warriors.append(Warrior())

        print("Zeus is set up")
        return self

    '''    
    getVelocities recebe dados da estratégia e retorna uma lista de dicionários comm as
    velocidades de cada roda
    '''
    def getVelocities(self, strategia):
        self.warriors = self.getwarriors(strategia)
        return self.generateOutput(self.controlRoutine())

    '''
    Seta os atributos do object Robot() baseado nas informações passadas pela estratégia
    Ações que podem ser escolhidas:
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
    - {
        "command": "spin",
        "data": { "velocity": X m/s, "direction": "clockwise" | "counter"
        }
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
    '''
    def getWarriors(self, strategia):
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
                    warriors[x].action.append(int(info["before"]))

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
                warriors[x].action.append(int(info["before"]))

        return warriors

    '''
    Fluxo de cálculos para gerar os pwm's que serão passados para a comunicação
    Actions() realiza os cálculos baseados nos comandos setados pela estratégia
    Translate() pega os dados gerados pelo Actions() e calcula a velocidade final de cada roda
    '''
    def controlRoutine(self):
        velocities = []
        for warrior in self.warriors:
            if len(warrior.action) > 0:
                velocities.append(self.translate.run(self.actions.run(warrior)))

        return velocities

    '''
    Gera lista de dicionários com as velocidades de cada robô
    '''
    def generateOutput(self, velocities):
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


