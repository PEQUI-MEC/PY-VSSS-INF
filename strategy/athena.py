# coding=utf-8
from scipy.spatial import distance
from strategy.endless import Endless
from strategy.warrior import Warrior

# só pra testes
import pprint


class Athena:
    sAdvance = 0
    sRecover = 1
    sReturn = 2
    sPush = 3
    sPass = 4
    sDanger = 5
    sHoly = 6

    tCatch = 0
    tCatchSideways = 1
    tBlock = 2
    tBlockOpening = 3
    tPush = 4
    tSpin = 5
    tWaitPass = 6
    tKick = 7

    def __init__(self, callback):
        self.endless = None
        self.warriors = []
        self.theirWarriors = []
        self.ball = {
            "position": (0, 0),
            "velocity": 0
        }

        self.atk = None
        self.mid = None
        self.gk = None

        self.globalState = "push"

        print("Athena summoned")

    def setup(self, numRobots, width, height, defaultVel):
        self.endless = Endless(width, height)
        warriorNames = ["aquiles", "teseu", "perseu"]
        for i in range(0, numRobots):
            self.warriors.append(Warrior(defaultVel, warriorNames[i]))

        print("Athena is set up.")
        return self

    '''
    Recebe um objeto do tipo
    [
        [ # robôs aliados
            {
                "position": (x, y)
                "orientation": orientação
            },
            {
                "position": (x, y)
                "orientation": orientação
            },
            {
                "position": (x, y)
                "orientation": orientação
            }
        ],
        [ # robôs adversários
            {
                "position": (x, y)
            },
            {
                "position": (x, y)
            },
            {
                "position": (x, y)
            }
        ],
        { # bola
            "position": (x, y)
        }
    ]
    
    ... e retorna um vetor de comandos de tamanho 'numrobots'
    
    LEMBRE-SE QUE O Y CRESCE PRA CIMA
    '''
    def getTargets(self, positions):
        self.parsePositions(positions)
        self.analyzeAndSetRoles()
        self.selectTactics()
        self.selectActions()
        return self.generateResponse(self.warriors)

    # TODO fazer mais verificações
    def parsePositions(self, positions):
        if type(positions) is not list or type(positions[0]) is not list or type(positions[1]) is not list or type(positions[2]) is not dict:
            raise ValueError("Invalid positions object received.")

        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.warriors[i].setup(positions[0][i]["position"], positions[0][i]["orientation"])

        self.theirWarriors = []
        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.theirWarriors.append(Warrior())
            self.theirWarriors[i].setup(positions[1][i]["position"])

        self.ball = {
            "position": positions[2]["position"],
            "velocity": 0  # !TODO calcular velocidade da bola
        }

        return positions

    '''
    Formato dos comandos:
    - {
        "command": "stop"
    }
    - {
        "command": "goTo",
        "data": {
            "pose": {
                "position": (x, y),
                "orientation": θ radianos
            },
            "target": {
                "position": (x, y),
                "orientation": θ radianos | (x, y),  # opcional - pode ser uma orientação final ou uma posição de lookAt
            }
            "velocity": X m/s,  # opcional - se passado, sem before, é a velocidade constante / com before é velocidade padrão
            "before": X s  # se passado sem o velocity, usa a velocidade máxima do robô como teto
            "obstacles": [
                (x, y),
                (x, y),
                ...
            ]
        }
    }
    - {
        "command": "spin",
        "data": {
            "velocity": X m/s,
            "direction": "clockwise" | "counter"
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
    '''
    def generateResponse(self, warriors):
        response = []
        for warrior in warriors:
            command = {}
            if warrior.command["type"] == "goTo":
                command["command"] = "goTo"
                command["data"] = {}
                command["data"]["pose"] = {
                    "position": warrior.position,
                    "orientation": warrior.orientation
                }
                command["data"]["target"] = {}
                command["data"]["target"]["position"] = warrior.command["target"]

                if "targetOrientation" in warrior.command:
                    command["data"]["target"]["orientation"] = warrior.command["targetOrientation"]

                if "targetVelocity" in warrior.command:
                    command["data"]["velocity"] = warrior.command["targetVelocity"]

                if "before" in warrior.command:
                    command["data"]["before"] = warrior.command["before"]

                if "avoidObstacles" in warrior.command:
                    command["data"]["obstacles"] = []
                    for obstacle in self.warriors:
                        command["data"]["obstacles"].append(obstacle.position)
                    for obstacle in self.theirWarriors:
                        command["data"]["obstacles"].append(obstacle.position)
                    if "avoidBall" in warrior.command:
                        command["data"]["obstacles"].append(self.ball["position"])

            elif warrior.command["type"] == "lookAt":
                command["command"] = "lookAt"
                command["data"] = {}

                if "targetOrientation" in warrior.command:
                    command["data"]["target"] = warrior.command["targetOrientation"]

                elif "target" in warrior.command:
                    command["data"]["pose"] = {
                        "position": warrior.position,
                        "orientation": warrior.orientation
                    }
                    command["data"]["target"] = warrior.command["target"]

            elif warrior.command["type"] == "spin":
                command["command"] = "spin"
                command["data"] = {}
                command["data"]["velocity"] = warrior.command["targetVelocity"]
                command["data"]["direction"] = warrior.command["spinDirection"]

            else: # stop
                command["command"] = "stop"
                command["data"] = {}
                if "before" in warrior.command:
                    command["data"]["before"] = warrior.command["before"]
                else:
                    command["data"]["before"] = 0

            response.append(command)

        return response

    '''
    Verifica a distância dos alidados para os pontos de interesse (nosso gol, bola, gol adversário)
    Verifica o posicionamento dos robôs e da bola e classifica entre situação de ataque, defesa, etc
    Analisa o estado geral do jogo
    Estados globais possíveis:
        - advance: bola está na frente de todos os aliados e no campo adversário
        - recover: bola está atrás do atk, na frente do mid e no campo adversário
        - return: bola está atrás do atk e do mid, no campo adversário
        - wtf: bola está atrás de todos os aliados e no campo adversário (???)

        - push: bola está na frente de todos os aliados e no campo aliado
        - pass: bola está atrás do atk, na frente do mid e no campo aliado
        - danger: bola está atrás do atk e do mid e no campo aliado
        - holyshit: bola está atrás de todos os aliados e no campo aliado
    '''
    def analyzeAndSetRoles(self):
        # escolhe os melhores pra cada posição crítica - o defensor vai ser escolhido de acordo com a situação do jogo
        avaliableWarriors = self.warriors.copy()
        self.gk = sorted(avaliableWarriors, key = self.__distanceToGoal)[0]
        self.gk.role = "gk"  # usado ao selecionar ação pra tática
        avaliableWarriors.remove(self.gk)
        self.atk = sorted(avaliableWarriors, key=self.__distanceToBall)[0]
        self.atk.role = "atk"  # usado ao selecionar ação pra tática
        avaliableWarriors.remove(self.atk)
        self.mid = avaliableWarriors[0]
        self.mid.role = "mid"  # usado ao selecionar ação pra tática

        ballX = self.ball["position"][0]
        # analisa o estado global do jogo
        if ballX > self.atk.position[0] and ballX > self.mid.position[0]:
            if ballX > self.endless.midField[0]:
                self.globalState = Athena.sAdvance
            else:
                self.globalState = Athena.sPush

        elif ballX > self.mid.position[0]:
            if ballX > self.endless.midField[0]:
                self.globalState = Athena.sRecover
            else:
                self.globalState = Athena.sPass

        elif ballX > self.gk.position[0]:
            if ballX > self.endless.midField[0]:
                self.globalState = Athena.sReturn
            else:
                self.globalState = Athena.sDanger

        else:
            self.globalState = Athena.sHoly

    '''
    Analisa o estado de cada Warrior em mais baixo nível e seleciona uma tática
    Táticas possíveis:
        - catch: pega a bola com uvf jogando ela pro gol
        - catchSideways: pega a bola com uvf jogando ela pras laterais
        - block: bloqueia passagem bola em relação ao gol (observar limitações de role)
        - blockOpening: fica em posição de bloqueio da área em que o goleiro não está
        - push: dá um empurrão pra frente na bola
        - spin: gira para empurrar a bola pra frente
        - waitPass: para em posição de sobra e fica olhando pra bola, recuando se a bola voltar muito em posse do atacante
        - kick: velocidade máxima com uvf pro gol
    '''
    def selectTactics(self):
        ballX = self.ball["position"][0]
        ballY = self.ball["position"][1]

        # TODO o que acontece no penalti?

        # se a bola tá muito próxima ao nosso gol em x
        if ballX < self.endless.ourCorner:
            # mid marca a saída de bola
            self.mid.tactics = Athena.tBlockOpening

            # se a bola tá fora da área
            if ballY > self.endless.areaTop or ballY < self.endless.areaTop:
                # responsabilidade do atk buscar
                self.atk.tactics = Athena.tCatchSideways
                # goleiro espera
                self.gk.tactics = Athena.tBlock

            # se a bola tá dentro da área, mas sem tanto risco
            elif ballY > self.endless.goalTop or ballY < self.endless.goalBottom or (ballX > self.gk.position[0] + self.endless.robotSize / 2):
                # responsabilidade do goleiro dar um "chega pra lá"
                self.gk.tactics = Athena.tPush
                # atk marca a área vulnerável enquanto goleiro avança (pode até trocar)
                self.atk.tactics = Athena.tCatchSideways

            # se a bola tá dentro da área de risco e tá perto do goleiro
            elif distance.euclidean(self.gk.position, self.ball["position"]) < self.endless.robotSize:
                # goleiro gira
                self.gk.tactics = Athena.tSpin
                # atk marca canto da área onde a bola vai
                self.atk.tactics = Athena.tBlockOpening

            # se a bola tá dentro da área de risco e goleiro não tá perto
            else:
                # goleiro vai por dentro do gol marcar a posição da bola (uvf)
                self.gk.tactics = Athena.tCatch
                # defensor tenta tirar a bola, se possível
                self.atk.tactics = Athena.tCatchSideways

        # se a bola tá muito próxima do gol deles em x
        elif ballX > self.endless.corner:
            # goleiro marca a projeção da bola em y
            self.gk.tactics = Athena.tBlock

            # se a bola tá fora da área
            if ballY > self.endless.areaTop or ballY < self.endless.areaTop:
                # mid fica em posição de cruzamento
                self.mid.tactics = Athena.tWaitPass

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < self.endless.robotSize:
                    # atacante gira !TODO analisar se compensa ele levar a bola pro mid
                    self.atk.tactics = Athena.tSpin
                else:
                    # atacante busca a bola com uvf
                    self.atk.tactics = Athena.tCatch

            # se a bola tá dentro da área mas fora do gol
            elif ballY > self.endless.goalTop or ballY < self.endless.goalBottom:
                # mid fica em posição de cruzamento
                self.mid.tactics = Athena.tWaitPass

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < self.endless.robotSize:
                    # atacante gira
                    self.atk.tactics = Athena.tSpin
                else:
                    # atacante busca a bola com uvf
                    self.atk.tactics = Athena.tCatch

            # se a bola tá dentro da área de risco e atacante tá perto
            elif distance.euclidean(self.atk.position, self.ball["position"]) < self.endless.robotSize:
                # atk gira pra dentro do gol
                self.atk.tactics = Athena.tSpin
                # mid fica em posição de sobra
                self.mid.tactics = Athena.tWaitPass

            # se a bola tá dentro da área de risco e atacante não tá perto
            else:
                # mid pega a sobra com uvf, chutando
                self.mid.tactics = Athena.tKick  # !TODO pensar em outras situações pra forçar o chute
                # atacante vai pra posição de sobra
                self.atk.tactics = Athena.tWaitPass

        # se a bola não tá em situações especiais, usa o estado global pra agir

        elif self.globalState == Athena.sAdvance:
            # atacante pega a bola com uvf e chuta
            self.atk.tactics = Athena.tCatch  # !TODO verficar se angulo é bom e chutar
            # mid fica em posição de sobra
            self.mid.tactics = Athena.tWaitPass
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            self.gk.tactics = Athena.tBlock

        elif self.globalState == Athena.sRecover:
            # atacante volta rápido pra tentar retomar a posse de bola
            self.atk.tactics = Athena.tCatch
            # mid fica em área de sobra, caso a bola escape do atacante
            self.mid.tactics = Athena.tBlockOpening  # !TODO fazer com que funcione bem para o mid também
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            self.gk.tactics = Athena.tBlock

        elif self.globalState == Athena.sReturn:
            # atacante volta rápido pra recuperar a bola
            self.atk.tactics = Athena.tCatchSideways
            # mid volta rápido em posição Athena.tB sobra
            self.mid.tactics = Athena.tBlockOpening
            # goleiro fica em posição híbrida entre projeção da bola e posiçãoAthena.tBtua
            self.gk.tactics = Athena.tBlock

        elif self.globalState == Athena.sPush:
            # atacante pega a bola com uvf e leva ra área de ataque
            self.atk.tactics = Athena.tCatch
            # mid cobre área não coberta por goleir
            self.mid.tactics = Athena.tBlockOpening
            # goleiro fica em posição real da bola
            self.gk.tactics = Athena.tBlock

        elif self.globalState == Athena.sPass:
            # acatante volta rápido pra posição de sobra
            self.atk.tactics = Athena.tBlockOpening
            # mid vai rápido em direção à bola com uvf (ele não era o que tava mais perto da bola)
            self.mid.tactics = Athena.tCatch
            # goleiro fica em posição real da bola
            self.gk.tactics = Athena.tBlock

        elif self.globalState == Athena.sDanger:
            # atacante volta rápido pra posição de saída de bola
            self.atk.tactics = Athena.tCatchSideways
            # mid volta rápido pra recuperar a bola
            self.mid.tactics = Athena.tBlockOpening
            # goleiro fica em posição real da bola
            self.gk.tactics = Athena.tBlock # !TODO fazer goleiro sair na bola quando possível

        elif self.globalState == Athena.sHoly:
            # atacante volta rápido pra posição de saída de bola
            self.atk.tactics = Athena.tCatchSideways
            # mid bloqueia outros jogadores
            self.mid.tactics = Athena.tCatchSideways
            # goleiro tenta dar a volta na bola o mais rápido possível, passando por dentro do gol
            self.gk.tactics = Athena.tCatch

    '''
    Seleciona ações de baixo nível baseado na tática
    Campos do warrior.command:
        type: "goTo" ou "lookAt" ou "spin"
        target: tupla
        targetOrientation: float ou tupla
        targetVelocity: float
        before: float (segundos)
        spinDirection: "clockwise" ou "counter"
        avoidObstacles: qualquer coisa
    '''
    def selectActions(self):
        for warrior in self.warriors:
            if warrior.tactics == Athena.tCatch:
                warrior.command["type"] = "goTo"
                warrior.command["target"] = self.ball["position"]
                warrior.command["targetOrientation"] = self.endless.goal
                warrior.command["targetVelocity"] = warrior.defaultVel
                warrior.command["avoidObstacles"] = "por favor"

            elif warrior.tactics == Athena.tCatchSideways:
                warrior.command["type"] = "goTo"
                warrior.command["target"] = self.ball["position"]
                warrior.command["targetVelocity"] = warrior.defaultVel
                warrior.command["avoidObstacles"] = "por favor"

                # escolhe o lado que vai pressionar a bola, dependendo de qual parede ela tá mais perto
                if self.ball["position"][1] > self.endless.midField[1]:
                    warrior.command["targetOrientation"] = (self.endless.midField[0], self.endless.height)
                else:
                    warrior.command["targetOrientation"] = (self.endless.midField[0], 0)

            elif warrior.tactics == Athena.tBlock:
                ballY = self.ball["position"][1]  # !TODO pegar Y composto com a velocidade da bola
                targetX = self.endless.goalieLine if warrior.role == "gk" else self.endless.areaLine

                if warrior.role == "gk":
                    if ballY > self.endless.goalTop:
                        target = (targetX, self.endless.goalTop)
                    elif ballY < self.endless.goalBottom:
                        target = (targetX, self.endless.goalBottom)
                    else:
                        target = (targetX, ballY)
                else:
                    if ballY > self.endless.goalTop:
                        target = (targetX, self.endless.goalTop)
                    elif ballY < self.endless.goalBottom:
                        target = (targetX, self.endless.goalBottom)
                    else:
                        target = (targetX, ballY)

                if distance.euclidean(warrior.position, target) > self.endless.robotSize:
                    warrior.command["type"] = "goTo"
                    warrior.command["target"] = self.ball["position"]

                    if warrior.position[1] > self.endless.midField[1]:
                        warrior.command["targetOrientation"] = (self.endless.goalieLine, 0)
                    else:
                        warrior.command["targetOrientation"] = (self.endless.goalieLine, self.endless.height)

                else:
                    warrior.command["type"] = "lookAt"
                    warrior.command["targetOrientation"] = (self.endless.goalieLine, 0)

                warrior.command["targetVelocity"] = warrior.defaultVel

            elif warrior.tactics == Athena.tBlockOpening:
                # !TODO bloquear em volta de toda a área
                targetX = self.endless.areaLine

                if self.gk.position[1] > self.endless.midField[1]: # !TODO usar uma equação decente
                    targetY = self.gk.position[1] - self.endless.robotSize
                else:
                    targetY = self.gk.position[1] + self.endless.robotSize

                if targetY > self.endless.areaTop:
                    target = (targetX, self.endless.areaTop)
                elif targetY < self.endless.areaBottom:
                    target = (targetX, self.endless.areaBottom)
                else:
                    target = (targetX, targetY)

                if distance.euclidean(warrior.position, target) > self.endless.robotSize:
                    warrior.command["type"] = "goTo"
                    warrior.command["target"] = self.ball["position"]

                    # !TODO verificar se ele está chegando pelo lado certo
                    if warrior.position[1] > self.endless.midField[1]:
                        warrior.command["targetOrientation"] = (self.endless.goalieLine, 0)
                    else:
                        warrior.command["targetOrientation"] = (self.endless.goalieLine, self.endless.height)

                else:
                    warrior.command["type"] = "lookAt"
                    warrior.command["targetOrientation"] = (self.endless.goalieLine, 0)

                warrior.command["targetVelocity"] = warrior.defaultVel

            elif warrior.tactics == Athena.tPush:
                warrior.command["type"] = "stop"

            elif warrior.tactics == Athena.tSpin:
                warrior.command["type"] = "stop"

            elif warrior.tactics == Athena.tWaitPass:
                warrior.command["type"] = "stop"

            elif warrior.tactics == Athena.tKick:
                warrior.command["type"] = "stop"

        return self.warriors

    '''
    Calcula as "distâncias" entre um robô e a bola/nosso gol
    Leva em consideração a angulação entre o objeto e o alvo
    '''
    def __distanceToBall(self, item):
        # !TODO levar em consideração a angulação
        return distance.euclidean(item.position, self.ball["position"])

    def __distanceToGoal(self, item):
        # !TODO levar em consideração a angulação
        return distance.euclidean(item.position, self.endless.ourGoal)


def main():
    fictionalPositions = [
        [
            {
                "position": (0, 200),
                "orientation": 0.5
            },
            {
                "position": (0, 200),
                "orientation": 0.5
            },
            {
                "position": (0, 200),
                "orientation": 0.5
            }
        ],
        [
            {
                "position": (0, 200)
            },
            {
                "position": (0, 200)
            },
            {
                "position": (0, 200)
            }
        ],
        {
            "position": (0, 200)
        }
    ]
    athena = Athena()
    athena.setup(3, 100, 100, 0.8)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(athena.getTargets(fictionalPositions))


if __name__ == "__main__":
    main()
