# coding=utf-8
import math
import time
from helpers import geometry
from scipy.spatial import distance
from helpers.endless import Endless
from strategy.warrior import Warrior
from strategy.oracle import Oracle


class Athena:
    sAdvance = 0
    sRecover = 1
    sReturn = 2
    sPush = 3
    sPass = 4
    sDanger = 5

    tCatch = "catch"
    tCatchSideways = "catchsideways"
    tBlock = "block"
    tBlockOpening = "blockopening"
    tPush = "push"
    tSpin = "spin"
    tWaitPass = "wait"
    tKick = "kick"
    tUnlock = "unlock"

    def __init__(self):
        self.warriors = []
        self.theirWarriors = []
        self.theirWarriorsLastPos = []

        self.atk = None
        self.mid = None
        self.gk = None

        self.ball = {
            "position": (0, 0),
            "oracle": None
        }

        self.transitionTimer = 0
        self.estimationTimer = 1
        # angulo da bola com o gol
        self.ballGoal = 0

        self.globalState = "push"
        self.transitionsEnabled = True
        self.roles = ["gk", "mid", "atk"]
        self.unlockDirection = 1
        self.deltaTime = time.time()
        self.lastTime = time.time()

        print("Athena summoned")

    def setup(self, numRobots, width, height, defaultVel):
        Endless.setup(width, height)
        for i in range(0, numRobots):
            self.warriors.append(Warrior(defaultVel))

        self.ball = {
            "position": (0, 0),
            "oracle": Oracle(100, Endless.pixelMeterRatio)
        }

        print("Athena is set up.")
        return self

    def reset(self):
        self.transitionTimer = 0

    def getTargets(self, positions):
        """
            Recebe um objeto do tipo
            [
                [ # robôs aliados
                    {
                        "position": (x, y)
                        "orientation": orientação
                        "robotLetter": letra do robô
                    },
                    {
                        "position": (x, y)
                        "orientation": orientação
                        "robotLetter": letra do robô
                    },
                    {
                        "position": (x, y)
                        "orientation": orientação
                        "robotLetter": letra do robô
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
        """
        self.deltaTime = time.time() - self.lastTime
        self.lastTime = time.time()
        self.__parsePositions(positions)
        self.__analyzeAndSetRoles()
        self.__selectTactics()
        self.__selectActions()

        commands = self.__generateResponse(self.warriors)
        return commands

    def __parsePositions(self, positions):
        if type(positions) is not list or type(positions[0]) is not list or type(positions[1]) is not list \
                or type(positions[2]) is not dict:
            raise ValueError("Invalid positions object received.")

        if len(positions) is not 3:  # allies, enemies and ball
            raise ValueError("Invalid positions length")

        if len(positions[0]) is not len(self.warriors):
            raise ValueError("Invalid allies size length (" + str(len(positions[0])) +
                             "). Expected " + str(len(self.warriors)))

        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.warriors[i].setup(positions[0][i]["robotLetter"],
                                   positions[0][i]["position"],
                                   positions[0][i]["orientation"])
            self.warriors[i].velEstimated = \
                distance.euclidean(self.warriors[i].position, self.warriors[i].lastPosition) / self.deltaTime
            self.warriors[i].velEstimated /= Endless.pixelMeterRatio
            # print(self.warriors[i].defaultVel)

        self.theirWarriorsLastPos = []
        for i in range(0, len(self.theirWarriors)):
            self.theirWarriorsLastPos.append(self.theirWarriors[i].position)

        self.theirWarriors = []
        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.theirWarriors.append(Warrior())
            self.theirWarriors[i].setup('z', positions[1][i]["position"])

        for i in range(0, len(self.theirWarriors)):
            dist = []
            for x in range(0, len(self.theirWarriorsLastPos)):
                dist.append(distance.euclidean(self.theirWarriors[i].position, self.theirWarriorsLastPos[x]))

            if len(dist) > 0:
                self.theirWarriors[i].velEstimated = min(dist) / self.deltaTime
                self.theirWarriors[i].velEstimated /= Endless.pixelMeterRatio

        self.ball["position"] = positions[2]["position"]
        # oracle é acessado sem verificação pois deve quebrar o programa se a Athena não tiver sido configurada
        self.ball["oracle"].pushState(self.ball["position"])

        return positions

    def __generateResponse(self, warriors):
        """Retorna um vetor de comandos para os robôs
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
                        "orientation": θ radianos | (x, y),  # opcional - pode ser uma orientação final ou
                                                                          uma posição de lookAt
                    }
                    "velocity": X m/s,  # opcional - se passado, sem before, é a velocidade constante /
                                                                 com before é velocidade padrão
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
                    "velocity": X m/s
                }
            }
            - {
                "command": stop,
                "data": {before: 0}
            }
        """
        response = []
        for warrior in warriors:
            command = {
                "robotLetter": warrior.robotID,
                "tactics": warrior.tactics,
                "futureBall": self.__ballInterceptLocation(warrior)  # self.ball["oracle"].predict(1)
            }

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
                else:
                    command["data"]["target"]["orientation"] = Endless.pastGoal

                if "targetVelocity" in warrior.command:
                    command["data"]["velocity"] = warrior.command["targetVelocity"]

                if "before" in warrior.command:
                    command["data"]["before"] = warrior.command["before"]

                if "avoidObstacles" in warrior.command:
                    command["data"]["obstacles"] = []
                    command["data"]["obstaclesSpeed"] = []
                    for obstacle in self.warriors:
                        if obstacle != warrior:
                            command["data"]["obstacles"].append(obstacle.position)
                            # print("Warriors: ", obstacle.velEstimated)
                            command["data"]["obstaclesSpeed"].append([obstacle.velEstimated, obstacle.velEstimated])
                    for obstacle in self.theirWarriors:
                        command["data"]["obstacles"].append(obstacle.position)
                        # print("Enemies: ", obstacle.velEstimated)
                        command["data"]["obstaclesSpeed"].append([obstacle.velEstimated, obstacle.velEstimated])

                    if warrior.position[0] > self.ball["position"][0] in warrior.command:
                        command["data"]["obstacles"].append(self.ball["position"])

            elif warrior.command["type"] == "lookAt":
                command["command"] = "lookAt"
                command["data"] = {}
                command["data"]["pose"] = {
                    "position": warrior.position,
                    "orientation": warrior.orientation
                }

                if "targetVelocity" in warrior.command:
                    command["data"]["velocity"] = warrior.command["targetVelocity"]

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

            else:  # stop
                command["command"] = "stop"
                command["data"] = {}
                if "before" in warrior.command:
                    command["data"]["before"] = warrior.command["before"]
                else:
                    command["data"]["before"] = 0

            response.append(command)

        return response

    def __analyzeAndSetRoles(self):
        """
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
        """

        # verifica os ângulos dos robôs, bola e gols
        # TODO calcular o kickangle com a projeção da bola
        ballX = self.ball["position"][0]
        ballY = self.ball["position"][1]
        # angulo da bola com o gol
        self.ballGoal = math.atan2(Endless.goal[1] - ballY, (Endless.pastGoal[0] - ballX))

        for i in range(len(self.warriors)):
            # angulo do robô com a bola
            self.warriors[i].robotBall = math.atan2(ballY - self.warriors[i].position[1],
                                                    (ballX - self.warriors[i].position[0]))
            # angulo entre as retas robo->bola e bola->gol
            self.warriors[i].robotBallGoal = math.atan2(math.sin(self.warriors[i].robotBall - self.ballGoal),
                                                        math.cos(self.warriors[i].robotBall - self.ballGoal))
            # orientação do robô em relação ao gol
            self.warriors[i].robotGoal = abs(
                geometry.roundAngle(
                    math.atan2(Endless.pastGoal[1] - self.warriors[i].position[1],
                               -(Endless.pastGoal[0] - self.warriors[i].position[0]))
                )
            )

            self.warriors[i].hasKickAngle = abs(self.warriors[i].robotBallGoal) < math.pi / 4 and \
                                               (self.warriors[i].robotGoal < math.pi / 4 or
                                                self.warriors[i].robotGoal > 3 * math.pi / 4)

        availableWarriors = self.warriors.copy()

        if self.transitionsEnabled:
            if self.transitionTimer > 0:
                self.transitionTimer -= self.deltaTime
            else:
                self.atk = self.gk = self.mid = None

                for warrior in availableWarriors:
                    if warrior.hasKickAngle:
                        dist = self.__distanceToBall(warrior)
                        if dist < Endless.width / 4 and (self.atk is None or dist < self.__distanceToBall(self.atk)):
                            self.atk = warrior

                if self.atk is None:
                    self.atk = sorted(availableWarriors, key=self.__distanceToBall)[0]

                self.atk.role = "atk"  # usado ao selecionar ação pra tática

                availableWarriors.remove(self.atk)

                # escolhe os melhores pra cada posição crítica
                # o defensor vai ser escolhido de acordo com a situação do jogo
                self.gk = sorted(availableWarriors, key=self.__distanceToGoal)[0]
                self.gk.role = "gk"  # usado ao selecionar ação pra tática
                availableWarriors.remove(self.gk)
                self.mid = availableWarriors[0]
                self.mid.role = "mid"  # usado ao selecionar ação pra tática

                # espera um segundo para permitir outra troca de posições
                self.transitionTimer = 1

        else:
            for i in range(len(self.roles)):
                if self.roles[i] == "gk":
                    self.gk = availableWarriors[i]
                    self.gk.role = "gk"
                elif self.roles[i] == "mid":
                    self.mid = availableWarriors[i]
                    self.mid.role = "mid"
                else:
                    self.atk = availableWarriors[i]
                    self.atk.role = "Attack"

        ballX = self.ball["position"][0]
        # analisa o estado global do jogo
        if ballX > self.atk.position[0] - Endless.robotSize and ballX > self.mid.position[0]:
            if ballX > Endless.midField[0]:
                self.globalState = Athena.sAdvance
            else:
                self.globalState = Athena.sPush

        elif ballX > self.mid.position[0]:
            if ballX > Endless.midField[0]:
                self.globalState = Athena.sRecover
            else:
                self.globalState = Athena.sPass

        elif ballX > self.gk.position[0]:
            if ballX > Endless.midField[0]:
                self.globalState = Athena.sReturn
            else:
                self.globalState = Athena.sDanger

        # estado Holy Shit não existe mais, é considerado o ourCorner

    def __selectTactics(self):
        """
            Analisa o estado de cada Warrior em mais baixo nível e seleciona uma tática
            Táticas possíveis:
                - catch: pega a bola com uvf jogando ela pro gol
                - catchSideways: pega a bola com uvf jogando ela pras laterais
                - block: bloqueia passagem bola em relação ao gol (observar limitações de role)
                - blockOpening: fica em posição de bloqueio da área em que o goleiro não está
                - push: dá um empurrão pra frente na bola
                - spin: gira para empurrar a bola pra frente
                - waitPass: para em posição de sobra e fica olhando pra bola,
                            recuando se a bola voltar muito em posse do atacante
                - kick: velocidade máxima com uvf pro gol
        """

        ballX = self.ball["position"][0]
        ballY = self.ball["position"][1]

        # táticas temporárias - um robô pode estar executando uma tática que depende de tempo e consistência
        tAtk = tMid = tGk = None

        # usa o estado global pra agir

        if self.globalState == Athena.sAdvance:
            # se o ângulo do robô com a bola e da bola com o gol é bom, se o atk tá atrás da bola e se tá perto dela
            if distance.euclidean(self.ball["position"], self.atk.position) < Endless.spinSize:
                if self.atk.hasKickAngle:
                    tAtk = Athena.tKick
                else:
                    tAtk = Athena.tSpin
            else:
                # atacante pega a bola com uvf
                tAtk = Athena.tCatch

            # mid fica em posição de sobra
            tMid = Athena.tWaitPass
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            tGk = Athena.tBlock

        elif self.globalState == Athena.sPush:
            # atacante pega a bola com uvf e leva pra área de ataque
            tAtk = Athena.tCatch
            # mid cobre área não coberta por goleiro
            tMid = Athena.tBlockOpening
            # goleiro fica em posição real da bola
            tGk = Athena.tBlock

        elif self.globalState == Athena.sRecover:
            # atacante volta rápido pra tentar retomar a posse de bola
            tAtk = Athena.tCatch
            # mid fica em área de sobra, caso a bola escape do atacante
            if ballX > Endless.midField[0]:
                tMid = Athena.tPush
            else:
                tMid = Athena.tBlock
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            tGk = Athena.tBlock

        elif self.globalState == Athena.sPass:
            # acatante volta rápido pra posição de sobra
            tAtk = Athena.tBlockOpening
            # mid vai rápido em direção à bola com uvf (ele não era o que tava mais perto da bola)
            tMid = Athena.tCatch
            # goleiro fica em posição real da bola
            tGk = Athena.tBlock

        elif self.globalState == Athena.sReturn:
            # atacante volta rápido pra recuperar a bola
            tAtk = Athena.tCatchSideways
            # mid volta rápido em posição Athena.tB sobra
            tMid = Athena.tBlockOpening
            # goleiro fica em posição híbrida entre projeção da bola e posiçãoAthena.tBtua
            tGk = Athena.tBlock

        elif self.globalState == Athena.sDanger:
            # atacante volta rápido pra posição de saída de bola
            tAtk = Athena.tCatchSideways
            # mid volta rápido pra recuperar a bola
            tMid = Athena.tBlockOpening
            # goleiro fica em posição real da bola
            """ NÃO DEIXA GOLEIRO SAIR DO GOL
            if ballX < Endless.width / 4 and \
                    distance.euclidean(self.atk.position, self.ball["position"]) > 3 * Endless.robotSize and \
                    distance.euclidean(self.mid.position, self.ball["position"]) > 3 * Endless.robotSize:
                tGk = Athena.tCatchSideways
            else:"""
            tGk = Athena.tBlock

        # situações especiais

        # se a bola tá muito próxima ao nosso gol em x
        if ballX < Endless.areaLine:
            # mid marca a saída de bola
            tMid = Athena.tBlockOpening

            # se a bola tá fora da área
            if ballY > Endless.areaTop or ballY < Endless.areaBottom:
                # responsabilidade do atk buscar
                tAtk = Athena.tCatchSideways
                # goleiro espera
                tGk = Athena.tBlock

            # se a bola tá dentro da área, mas sem tanto risco
            elif Endless.goalTop > ballY > Endless.goalBottom:
                # responsabilidade do goleiro dar um "chega pra lá"
                tGk = Athena.tPush
                # atk marca a área vulnerável enquanto goleiro avança (pode até trocar)
                tAtk = Athena.tCatchSideways

            # se a bola tá dentro da área de risco e tá perto do goleiro
            elif distance.euclidean(self.gk.position, self.ball["position"]) < Endless.robotSize:
                # goleiro gira
                tGk = Athena.tSpin
                # atk marca canto da área onde a bola vai
                tAtk = Athena.tBlockOpening

            # se a bola tá dentro da área de risco e goleiro não tá perto
            else:
                # goleiro vai por dentro do gol marcar a posição da bola (uvf)
                tGk = Athena.tCatch
                # defensor tenta tirar a bola, se possível
                tAtk = Athena.tCatchSideways

        # se a bola tá muito próxima do gol deles em x
        elif ballX > Endless.corner:
            # goleiro marca a projeção da bola em y
            tGk = Athena.tBlock

            # se a bola tá fora da área
            if ballY > Endless.areaTop or ballY < Endless.areaTop:
                # mid fica em posição de cruzamento
                tMid = Athena.tWaitPass

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < Endless.spinSize:
                    # atacante gira
                    tAtk = Athena.tSpin
                else:
                    # atacante busca a bola com uvf
                    tAtk = Athena.tCatch

            # se a bola tá dentro da área mas fora do gol
            elif ballY > Endless.goalTop or ballY < Endless.goalBottom:
                # mid fica em posição de cruzamento
                tMid = Athena.tWaitPass

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < Endless.robotSize:
                    # atacante gira
                    tAtk = Athena.tSpin
                else:
                    # atacante busca a bola com uvf
                    tAtk = Athena.tCatch

            # se a bola tá dentro da área de risco e atacante tá perto
            elif distance.euclidean(self.atk.position, self.ball["position"]) < Endless.robotSize:
                # atk gira pra dentro do gol
                tAtk = Athena.tSpin
                # mid fica em posição de sobra
                tMid = Athena.tWaitPass

            # se a bola tá dentro da área de risco e atacante não tá perto
            else:
                # mid pega a sobra com uvf, chutando
                tMid = Athena.tKick  # !TODO pensar em outras situações pra forçar o chute
                # atacante vai pra posição de sobra
                tAtk = Athena.tWaitPass

        # ações específicas de cada papel
        if distance.euclidean(self.gk.position, self.ball["position"]) < Endless.spinSize:
            tGk = Athena.tSpin

        if tMid != Athena.tPush and tMid != Athena.tKick:
            if distance.euclidean(self.mid.position, self.ball["position"]) < Endless.spinSize:
                tMid = Athena.tSpin

        if tAtk != Athena.tPush and tAtk != Athena.tKick:
            if distance.euclidean(self.atk.position, self.ball["position"]) < Endless.spinSize:
                tAtk = Athena.tSpin

        # verifica se algum robô está travado
        for warrior in self.warriors:
            # se ele não _deve_ estar parado
            if not warrior.positionLocked:
                # se ele não se moveu de um ciclo pra cá
                if warrior.actionTimer <= 0 and \
                        distance.euclidean(warrior.position, warrior.lastPosition) < 10 * self.deltaTime:
                    # se atingiu o máximo de tempo bloqueado, executa ação de sair
                    if warrior.lockedTime > 0.2:
                        # print("locked " + str(time.time()))
                        if distance.euclidean(warrior.position, self.ball["position"]) < Endless.robotSize:
                            warrior.tactics = Athena.tSpin  # sobrebrescreve a tática direto
                            warrior.actionTimer = 0.5
                        else:
                            warrior.tactics = Athena.tUnlock  # sobrebrescreve a tática direto
                            warrior.lockedTime = 0
                            warrior.actionTimer = 0.8  # tempo que deverá andar numa direção pra destravar
                            self.unlockDirection *= -1  # direção que deverá tentar dessa vez
                    else:
                        warrior.lockedTime += self.deltaTime

                # se ele começou a se mover, mas para sair do bloqueio, continua a mesma ação
                elif warrior.actionTimer > 0:
                    # print("unlocking " + str(time.time()))
                    warrior.actionTimer -= self.deltaTime

                # se ele deve estar parado ou está andando, o reseta o lockedTime
                else:
                    warrior.lockedTime = 0
            else:
                warrior.lockedTime = 0

        if self.atk.actionTimer > 0:
            self.atk.actionTimer -= self.deltaTime
        else:
            self.atk.tactics = tAtk
            
        if self.mid.actionTimer > 0:
            self.mid.actionTimer -= self.deltaTime
        else:
            self.mid.tactics = tMid

        if self.gk.actionTimer > 0:
            self.gk.actionTimer -= self.deltaTime
        else:
            self.gk.tactics = tGk

    def __selectActions(self):
        """
            Seleciona ações de baixo nível baseado na tática
            Campos do warrior.command:
                type: "goTo" ou "lookAt" ou "spin"
                target: tupla
                targetOrientation: float ou tupla
                targetVelocity: float
                before: float (segundos)
                spinDirection: "clockwise" ou "counter"
                avoidObstacles: qualquer coisa
        """
        ballY = self.ball["position"][1]
        ballX = self.ball["position"][0]

        for warrior in self.warriors:
            # reseta o lock, se necessário vai ser ativado de novo
            warrior.positionLocked = False

            if warrior.tactics == Athena.tKick:
                # vai pra cima com tudo, sem desviar de obstáculos
                warrior.command["type"] = "goTo"
                warrior.command["target"] = Endless.goal
                warrior.command["targetOrientation"] = Endless.pastGoal
                warrior.command["targetVelocity"] = warrior.maxVel

            elif warrior.tactics == Athena.tPush:
                # vai pra cima cuidadosamente
                warrior.command["type"] = "goTo"
                warrior.command["targetOrientation"] = Endless.pastGoal
                warrior.command["avoidObstacles"] = "por favor"
                warrior.command["targetVelocity"] = warrior.defaultVel

                if distance.euclidean(warrior.position, self.ball["position"]) < Endless.robotSize:
                    warrior.command["target"] = Endless.goal
                else:
                    warrior.command["target"] = self.ball["position"]

            elif warrior.tactics == Athena.tCatch:
                # se é pra pegar a bola, o alvo é ela com orientação pro gol
                warrior.command["type"] = "goTo"
                warrior.command["targetOrientation"] = Endless.pastGoal
                warrior.command["targetVelocity"] = warrior.defaultVel
                warrior.command["avoidObstacles"] = "por favor"

                if ballX < warrior.position[0] - Endless.robotSize:
                    if ballY > Endless.midField[1]:
                        warrior.command["target"] = (
                            self.ball["position"][0] - 2 * Endless.robotSize,
                            self.ball["position"][1] - 1.2 * Endless.robotRadius)
                    else:
                        warrior.command["target"] = (
                            self.ball["position"][0] - 2 * Endless.robotSize,
                            self.ball["position"][1] + 1.2 * Endless.robotRadius)
                else:
                    warrior.command["target"] = self.ball["position"]

            elif warrior.tactics == Athena.tCatchSideways:
                # faz o melhor pra desviar a bola do rumo do nosso gol com alvo nela com orientação pros lados
                warrior.command["type"] = "goTo"
                warrior.command["targetVelocity"] = warrior.defaultVel
                warrior.command["avoidObstacles"] = "vai que é tua meu amigo"

                # escolhe o lado que vai pressionar a bola, dependendo de qual parede ela tá mais perto
                if ballY > Endless.midField[1]:
                    warrior.command["targetOrientation"] = math.pi / 2
                else:
                    warrior.command["targetOrientation"] = -math.pi / 2

                if ballX < warrior.position[0] - Endless.robotSize:
                    if ballY > Endless.midField[1]:
                        warrior.command["target"] = (
                            self.ball["position"][0] - 2 * Endless.robotSize,
                            self.ball["position"][1] - 1.2 * Endless.robotRadius)
                    else:
                        warrior.command["target"] = (
                            self.ball["position"][0] - 2 * Endless.robotSize,
                            self.ball["position"][1] + 1.2 * Endless.robotRadius)
                else:
                    warrior.command["target"] = self.ball["position"]

            elif warrior.tactics == Athena.tBlock:
                warrior.command["targetVelocity"] = warrior.defaultVel
                # !TODO pegar Y composto com a velocidade da bola
                targetX = Endless.goalieLine

                projection = self.ball["oracle"].getY(targetX)
                trustabillity = geometry.saturate(ballY / Endless.midField[0], 1, 0)
                targetY = geometry.saturate(projection * trustabillity + ballY * (1 - trustabillity), Endless.goalBottom, Endless.goalTop)

                target = (targetX, targetY)

                if distance.euclidean(warrior.position, target) > Endless.robotSize:
                    # se está longe do alvo, vai até ele
                    warrior.command["type"] = "goTo"
                    warrior.command["target"] = target
                    warrior.command["avoidObstacles"] = "se não for pedir demais..."

                    # se posiciona com uvf para maior precisão
                    if warrior.position[1] > Endless.midField[1]:
                        warrior.command["targetOrientation"] = (Endless.goalieLine, Endless.height)
                    else:
                        warrior.command["targetOrientation"] = (Endless.goalieLine, 0)

                else:
                    # se já chegou, só conserta a orientação
                    warrior.positionLocked = True
                    warrior.command["type"] = "lookAt"
                    warrior.command["targetOrientation"] = (Endless.goalieLine, 0)

            elif warrior.tactics == Athena.tBlockOpening:
                warrior.command["targetVelocity"] = warrior.defaultVel
                targetX = Endless.areaLine
                targetY = ballY

                if ballY > Endless.height - Endless.robotSize:
                    targetY = Endless.height - Endless.robotSize
                elif ballY < Endless.robotSize:
                    targetY = Endless.robotSize

                # TODO o que fazer se a bola está dentro da área?
                if ballX < Endless.areaLine:
                    if targetY > Endless.areaTop:
                        targetY = Endless.areaTop
                    elif targetY < Endless.areaBottom:
                        targetY = Endless.areaBottom

                target = (targetX, targetY)

                if distance.euclidean(warrior.position, target) > Endless.robotSize:
                    warrior.command["type"] = "goTo"
                    warrior.command["target"] = target
                    warrior.command["avoidObstacles"] = "por favor, nunca te pedi nada irmão"

                    # !TODO verificar se ele está chegando pelo lado certo
                    if warrior.position[1] > Endless.midField[1]:
                        warrior.command["targetOrientation"] = (Endless.goalieLine, Endless.height)
                    else:
                        warrior.command["targetOrientation"] = (Endless.goalieLine, 0)

                else:
                    warrior.positionLocked = True
                    warrior.command["type"] = "lookAt"
                    warrior.command["targetOrientation"] = self.ball["position"]

            elif warrior.tactics == Athena.tWaitPass:
                # TODO verificar se é bom dividir o mid e atk verticalmente no campo
                # dessa forma faz com que o mid sempre acompanhe do meio do campo em Y
                targetX = self.ball["position"][0] - Endless.width / 4

                if targetX < Endless.areaSize[0]:
                    targetX = Endless.areaSize[0]

                target = (targetX, Endless.midField[1])

                if distance.euclidean(warrior.position, target) > Endless.robotSize:
                    warrior.command["type"] = "goTo"
                    warrior.command["target"] = target
                    warrior.command["targetVelocity"] = warrior.defaultVel
                    warrior.command["avoidObstacles"] = "mas é claro, chefia"
                    if target == self.ball["position"]:
                        warrior.command["targetOrientation"] = (self.ball["position"][0] + 10,
                                                                self.ball["position"][1] + 10)
                    else:
                        warrior.command["targetOrientation"] = self.ball["position"]
                else:
                    warrior.positionLocked = True
                    warrior.command["type"] = "lookAt"
                    warrior.command["targetOrientation"] = self.ball["position"]

            elif warrior.tactics == Athena.tSpin:
                warrior.positionLocked = True
                warrior.command["type"] = "spin"
                warrior.command["targetVelocity"] = warrior.maxVel  # TODO verificar se é melhor defaultVel

                if warrior.position[1] - Endless.robotSize > ballY:
                    warrior.command["spinDirection"] = "counter"
                elif warrior.position[1] + Endless.robotSize < ballY:
                    warrior.command["spinDirection"] = "clockwise"
                elif warrior.position[0] > ballX:
                    if warrior.position[1] > Endless.midField[1]:
                        warrior.command["spinDirection"] = "clockwise"
                    else:
                        warrior.command["spinDirection"] = "counter"
                else:
                    if warrior.position[1] > Endless.midField[1]:
                        warrior.command["spinDirection"] = "clockwise"
                    else:
                        warrior.command["spinDirection"] = "counter"

                # sobrescreve giro pra dar aquele toque pra fazer a bola entrar
                if ballX > Endless.midField[0] and Endless.goalBottom < ballY < Endless.goalTop:
                    if warrior.position[1] < ballY:
                        warrior.command["spinDirection"] = "clockwise"
                    else:
                        warrior.command["spinDirection"] = "counter"

            elif warrior.tactics == Athena.tUnlock:
                warrior.command["type"] = "goTo"
                warrior.command["targetVelocity"] = warrior.defaultVel
                warrior.command["target"] = (warrior.position[0] + self.unlockDirection * 100 *
                                             math.cos(warrior.orientation),
                                             warrior.position[1] + self.unlockDirection * 100 *
                                             math.sin(warrior.orientation))

        return self.warriors

    def __distanceToBall(self, item):
        """
            Calcula as "distâncias" entre um robô e a bola/nosso gol
            Leva em consideração a angulação entre o objeto e o alvo
        """
        return distance.euclidean(item.position, self.ball["position"])

    def __distanceToGoal(self, item):
        # !TODO levar em consideração a angulação
        return distance.euclidean(item.position, Endless.ourGoal)

    def __timeToArrive(self, fromPos, toPos, vel):
        dist = distance.euclidean(fromPos, toPos)
        return dist / (vel * Endless.pixelMeterRatio)

    def __ballInterceptLocation(self, robot):
        # tempo de chegada em linha reta, na maior velocidade possível
        tta = self.__timeToArrive(robot.position, self.ball["position"], robot.defaultVel)
        # onde a bola vai estar nesse meio tempo
        projection = self.ball["oracle"].predict(tta)

        # verifica se é impossível alcançar o alvo
        if self.ball["oracle"].velocity > robot.defaultVel:
            return projection

        # enquanto o tempo de chegada for maior do que o tempo para a bola chegar na posição
        while tta > self.__timeToArrive(robot.position, projection, robot.defaultVel):
            tta = self.__timeToArrive(robot.position, projection, robot.defaultVel)
            projection = self.ball["oracle"].predict(tta)

        return projection

    # GETTERS AND SETTERS

    def setTransitionsState(self, state):
        self.transitionsEnabled = state

    def setRoles(self, roles):
        """
        Sets the robot's roles
        :param roles: The robot's roles. Can be "Attack", "Defense" or "Goalkeeper"
        :return: True if the roles are correct, False otherwise
        """
        print("\n[Athena] New roles:")
        for i in range(len(roles)):
            if roles[i] != "Goalkeeper" and roles[i] != "Defense" and roles[i] != "Attack":
                print("Invalid role: " + roles[i])
                return False

            print("\t" + str(i + 1) + ": " + roles[i])

        self.roles = roles
        return True

    def setVelocities(self, atkSpeed, midSpeed, gkSpeed):
        """
        Sets robots' velocities
        :param atkSpeed: velocity of the Attacker
        :param midSpeed: velocity of the Defensor
        :param gkSpeed: velocity of the Goalkeeper
        """
        print("\n[Athena] New velocities:")
        for warrior in self.warriors:
            if warrior.role == "atk":
                warrior.setDefaultVel(atkSpeed)
                print("\tAttacker: " + atkSpeed)
            elif warrior.role == "mid":
                warrior.setDefaultVel(midSpeed)
                print("\tDefensor (Mid): " + midSpeed)
            elif warrior.role == "gk":
                warrior.setDefaultVel(gkSpeed)
                print("\tGoalkeeper: " + gkSpeed)
