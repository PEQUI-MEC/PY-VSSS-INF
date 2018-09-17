from .actions import Actions
from .translate import Translate
from .robot import Robot

class Zeus:
    def __init__(self, callback):
        self.robots = []
        self.actions = None
        self.translate = None
        self.nRobots = 0
        self.maxVelocity = 1.0

        self.callback = callback
        print("Zeus summoned")

    '''
    Setup Zeus: nRobots is the num of robots in game
    '''
    def setup(self, nRobots):
        self.actions = Actions()
        self.translate = Translate()
        self.nRobots = nRobots

        for i in range(0, nRobots):
            self.robots.append(Robot())

        print("Zeus is set up")
        return self

    '''    
    getVelocities recebe dados da estratégia e retorna uma lista de dicionários comm as
    velocidades de cada roda
    '''
    def getVelocities(self, strategia):
        self.robots = self.getRobots(strategia)
        # return self.generateOutput(self.controlRoutine())
        self.callback(self.generateOutput(self.controlRoutine()))

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
        "data": {}
    }
    '''
    def getRobots(self, strategia):
        robots = []
        if type(strategia) is not list or \
                len(strategia) != self.nRobots:
            raise ValueError("Invalid data object received.")

        for i in range(0, self.nRobots):
            if type(strategia[i]) is not dict:
                raise ValueError("Invalid data object received.")

            if ("command" in strategia[i]) is False or \
                    ("data" in strategia[i]) is False:
                raise ValueError("Invalid data object received.")

            robots.append(Robot())

        for x in range(0, len(strategia)):
            if strategia[x]["command"] is not "goTo" and \
                    strategia[x]["command"] is not "spin" and \
                    strategia[x]["command"] is not "lookAt" and \
                    strategia[x]["command"] is not "stop":
                raise ValueError("Invalid command.")

            robots[x].action.append(strategia[x]["command"])
            info = strategia[x]["data"]

            if strategia[x]["command"] == "goTo":
                robots[x].position = info["pose"]["position"]
                robots[x].orientation = info["pose"]["orientation"]

                robots[x].target = info["target"]["position"]
                robots[x].targetOrientation = info["target"]["orientation"]

                if "velocity" in info:
                    robots[x].vMax = info["velocity"]
                else:
                    robots[x].vMax = self.maxVelocity

                if "before" in info:
                    robots[x].action.append(int(info["before"]))

                if "obstacles" in info:
                    robots[x].obstacles = info["obstacles"]

            elif strategia[x]["command"] == "spin":
                robots[x].vMax = info["velocity"]
                robots[x].action.append(info["direction"])

            elif strategia[x]["command"] == "lookAt":
                robots[x].orientation = info["pose"]["orientation"]
                if type(info["target"]) is float:
                    robots[x].targetOrientation = info["target"]
                    robots[x].action.append("orientation")
                else:
                    robots[x].position = info["pose"]["position"]
                    robots[x].target = info["target"]
                    robots[x].action.append("target")

            # elif strategia[x]["command"] == "stop":
                # !TODO definir estrutura final do comando stop

        return robots

    '''
    Fluxo de cálculos para gerar os pwm's que serão passados para a comunicação
    Actions() realiza os cálculos baseados nos comandos setados pela estratégia
    Translate() pega os dados gerados pelo Actions() e calcula a velocidade final de cada roda
    '''
    def controlRoutine(self):
        velocities = []
        for robot in self.robots:
            if len(robot.action) > 0:
                velocities.append(self.translate.run(self.actions.run(robot)))

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


