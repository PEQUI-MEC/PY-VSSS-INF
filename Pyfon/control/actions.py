import math
from .unfield import UnivectorField


class Actions:
    def __init__(self):
        self.uvf = UnivectorField()
        self.uvf.updateConstants(0.06, 0.7, 0.1, 0.04, 0.15)

    def run(self, robot):
        if robot.action[0] == "stop":
            robot.cmdType = "SPEED"
            return self.stop(robot)

        elif robot.action[0] == "spin":
            robot.cmdType = "SPEED"
            return self.spin(robot)

        elif robot.action[0] == "lookAt":
            robot.cmdType = "ORIENTATION"
            robot.targetOrientation = self.lookAt(robot.action[1], robot.target,  robot.position, robot.targetOrientation)
            return robot

        elif robot.action[0] == "goTo":
            robot.cmdType = "SPEED"
            return self.goTo(robot)

    '''
    - {
        "command": stop,
        "data": {}
    }
    '''
    def stop(self, robot):
        # !TODO verficar a necessidade de ter um estado de parada com deseceleração
        robot.vMax = 0
        robot.vLeft = 0
        robot.vRight = 0

        return robot

    '''
    - {
        "command": "spin",
        "data": { "velocity": X m/s, "direction": "clockwise" | "counter"
        }
    }
    '''
    def spin(self, robot):
        if robot.action[1] == "clockwise":
            robot.vLeft = robot.vMax
            robot.vRight = -robot.vMax
        else:
            robot.vLeft = -robot.vMax
            robot.vRight = robot.vMax

        return robot

    '''
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
    '''
    def lookAt(self, where, target, position, orientation=None):
        if where is "orientation":
            return orientation

        elif where is "target":
            x = target[0] - position[0]
            y = target[1] - position[1]
            return math.atan2(y, -x)

        else:
            raise ValueError("Invalid data.")

    '''
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
    '''
    def goTo(self, robot):
        '''
        # Se o targetOrientation passado for um ponto, calcular o targetOrientation usando o lookAt
        if type(robot.targetOrientation) is tuple:
            target = robot.targetOrientation
            del robot.targetOrientation
            robot.targetOrientation = self.lookAt("target", target, robot.position)

        if robot.obstacles is not None:
            self.uvf.updateObstacles(robot.obstacles, [[0, 0], [0, 0]])

        #  Verificar se existe um 'before' na chamada desse método
        time = None
        if len(robot.action) > 1:
            time = robot.action[1]

        if time is None:
            # !TODO sem aceleração ou eu quem controlo como será feito a aceleração?
            print("VMax = " + str(robot.vMax))
            robot.vRight = robot.vMax
            robot.vLeft = robot.vMax
            print(self.uvf.getVec(list(robot.position), [robot.vLeft, robot.vRight]), list(robot.target))
        else:
            # !TODO Fazer verificação se é possível realizar o trajeto com o tempo requisitado
            pass
        '''

        return robot
