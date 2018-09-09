# coding=utf-8
from scipy.spatial import distance

from endless import Endless
from warrior import Warrior

#só pra testes
import pprint


class Athena:

    '''
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
    sAdvance = 0
    sRecover = 1
    sReturn = 2
    sPush = 3
    sPass = 4
    sDanger = 5
    sHoly = 6

    def __init__(self):
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

        print("Athena summoned.")

    def setup(self, numRobots, width, height):
        self.endless = Endless(width, height)
        for i in range(0, numRobots):
            self.warriors.append(Warrior())

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
        warriorNames = ["aquiles", "teseu", "perseu"]

        if type(positions) is not list or type(positions[0]) is not list or type(positions[1]) is not list or type(positions[2]) is not dict:
            raise ValueError("Invalid positions object received.")

        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.warriors[i].setup(positions[0][i]["position"], positions[0][i]["orientation"], warriorNames[i])

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

                if warrior.command["targetOrientation"] is not None:
                    command["data"]["target"]["orientation"] = warrior.command["target"]

                if warrior.command["targetVelocity"] is not None:
                    command["data"]["velocity"] = warrior.command["targetVelocity"]

                if warrior.command["before"] is not None:
                    command["data"]["before"] = warrior.command["before"]

            elif warrior.command["type"] == "lookAt":
                command["command"] = "lookAt"
                command["data"] = {}

                if warrior.command["targetOrientation"] is not None:
                    command["data"]["target"] = warrior.command["targetOrientation"]

                elif warrior.command["target"] is not None:
                    command["data"]["pose"] = {
                        "position": warrior.position,
                        "orientation": warrior.orientation
                    }
                    command["data"]["target"] = warrior.command["target"]

            else:  # spin
                command["command"] = "spin"
                command["data"] = {}
                command["data"]["velocity"] = warrior.command["targetVelocity"]
                command["data"]["direction"] = warrior.command["spinDirection"]

            response.append(command)

        return response

    '''
    Verifica a distância dos alidados para os pontos de interesse (nosso gol, bola, gol adversário)
    Verifica o posicionamento dos robôs e da bola e classifica entre situação de ataque, defesa, etc
    Analisa o estado geral do jogo
    '''
    def analyzeAndSetRoles(self):
        # escolhe os melhores pra cada posição crítica - o defensor vai ser escolhido de acordo com a situação do jogo
        avaliableWarriors = self.warriors.copy()
        self.gk = sorted(avaliableWarriors, key = self.__distanceToGoal)[0]
        avaliableWarriors.remove(self.gk)
        self.atk = sorted(avaliableWarriors, key=self.__distanceToBall)[0]
        avaliableWarriors.remove(self.atk)
        self.mid = avaliableWarriors[0]

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
    Analisa o estado de cada Warrior em mais baixo nível
    '''
    def selectTactics(self):
        ballX = self.ball["position"][0]
        ballY = self.ball["position"][1]

        # se a bola tá muito próxima ao nosso gol em x
        if ballX < self.endless.ourCorner:
            # atacante marca a saída de bola

            # se a bola tá fora da área
            if ballY > self.endless.areaTop or ballY < self.endless.areaTop:
                # responsabilidade do mid buscar
                # goleiro espera
                pass

            # se a bola tá dentro da área, mas sem tanto risco
            elif ballY > self.endless.goalTop or ballY < self.endless.goalBottom or (ballX > self.gk.position[0] + self.endless.robotSize / 2):
                # responsabilidade do goleiro dar um "chega pra lá"
                # mid marca a área vulnerável enquanto goleiro avança (pode até trocar)
                pass

            # se a bola tá dentro da área de risco e tá perto do goleiro
            elif distance.euclidean(self.gk.position, self.ball["position"]) < self.endless.robotSize:
                # goleiro gira
                # mid marca canto da área onde a bola vai
                pass

            # se a bola tá dentro da área de risco e goleiro não tá perto
            else:
                # goleiro vai por dentro do gol marcar a posição da bola (uvf)
                # defensor tenta tirar a bola, se possível
                pass

        # se a bola tá muito próxima do gol deles em x
        elif ballX > self.endless.corner:
            # goleiro marca a projeção da bola em y !TODO analisar se é seguro deixar ele adiantado

            # se a bola tá fora da área
            if ballY > self.endless.areaTop or ballY < self.endless.areaTop:
                # mid fica em posição de cruzamento

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < self.endless.robotSize:
                    # atacante gira !TODO analisar se compensa ele levar a bola pro mid
                    pass
                else:
                    # atacante busca a bola com uvf
                    pass

            # se a bola tá dentro da área mas fora do gol
            elif ballY > self.endless.goalTop or ballY < self.endless.goalBottom:
                # mid fica em posição de cruzamento

                # se a bola tá perto do atacante
                if distance.euclidean(self.ball["position"], self.atk.position) < self.endless.robotSize:
                    # atacante gira !TODO analisar se compensa ele levar a bola pro mid
                    pass
                else:
                    # atacante busca a bola com uvf
                    pass

            # se a bola tá dentro da área de risco e atacante tá perto
            elif distance.euclidean(self.atk.position, self.ball["position"]) < self.endless.robotSize:
                # mid gira pra dentro do gol
                # defensor fica em posição de sobra
                pass

            # se a bola tá dentro da área de risco e atacante não tá perto
            else:
                # mid pega a sobra com uvf, chutando
                # atacante vai pra posição de sobra
                pass

        # se a bola não tá em situações especiais, usa o estado global pra agir

        elif self.globalState == Athena.sAdvance:
            # atacante pega a bola com uvf e chuta
            # mid fica em posição de sobra
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            pass

        elif self.globalState == Athena.sRecover:
            # atacante volta rápido pra tentar retomar a posse de bola
            # mid fica em área de sobra, caso a bola escape do atacante
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            pass

        elif self.globalState == Athena.sReturn:
            # atacante volta rápido pra recuperar a bola
            # mid volta rápido em posição de sobra
            # goleiro fica em posição híbrida entre projeção da bola e posição atual
            pass

        elif self.globalState == Athena.sPush:
            # atacante pega a bola com uvf e leva pra área de ataque
            # mid cobre área não coberta por goleiro
            # goleiro fica em posição real da bola
            pass

        elif self.globalState == Athena.sPass:
            # acatante volta rápido pra posição de sobra
            # mid vai rápido em direção à bola com uvf (ele não era o que tava mais perto da bola)
            # goleiro fica em posição real da bola
            pass

        elif self.globalState == Athena.sDanger:
            # atacante volta rápido pra posição de saída de bola
            # mid volta rápido pra recuperar a bola
            # goleiro fica em posição real da bola
            pass

        elif self.globalState == Athena.sHoly:
            # atacante volta rápido pra posição de saída de bola
            # mid bloqueia outros jogadores
            # goleiro tenta dar a volta na bola o mais rápido possível, passando por dentro do gol
            pass

    '''
    Seleciona ações de baixo nível baseado na tática
    Ações que podem ser escolhidas:
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
    def selectActions(self):
        for warrior in self.warriors:
            warrior.command["type"] = "goTo"
            warrior.command["target"] = (100, 200)
            warrior.command["targetOrientation"] = self.endless.goal
            warrior.command["targetVelocity"] = 0.8
            warrior.command["before"] = 2

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
    athena.setup(3, 100, 100)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(athena.getTargets(fictionalPositions))


if __name__ == "__main__":
    main()
