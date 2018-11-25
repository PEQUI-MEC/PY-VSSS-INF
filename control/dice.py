# coding=utf-8
from math import atan2, pi, sin, cos
from helpers import geometry
from helpers.endless import Endless
from helpers.decorators import timeToFinish
import numpy
import time


class Dice:
    """Módulo de tradução

    Essa classe é responsável por encontrar as velocidades de cada roda dos robôs.

    Attributes:
        warrior: Objeto Warrior()
        deltaTime:
        lastTime:
        transitionTime:
    """

    acc = 0.5

    def __init__(self):
        self.warrior = None
        self.deltaTime = None
        self.lastTime = None
        self.transitionTime = None

    def setup(self):
        """Primeiros passos de Dice

        Esse método deve ser chamado antes de usar Dice apropriadamente.
        Aqui é inicializado as variáveis deltaTime e lastTime com o tempo atual do clock.
        """

        self.deltaTime = time.time()
        self.lastTime = time.time()
        self.transitionTime = 0

        return self

    # @timeToFinish
    def run(self, warrior):
        """ Metódo principal de Dice()

        Esse método recebe uma instância de Warrior() e encaminha os dados para seu respectivo método
        de acordo com o cmdType.

        Args:
            warrior: Instância de Warrior()

        Returns:
            list: lista com velocidade da roda esquerda, velocidade da roda direita e orientação alvo respectivamente

        """

        self.warrior = warrior

        if warrior.cmdType == "VECTOR":
            return self.vectorControl()
        elif warrior.cmdType == "POSITION":
            return self.positionControl()
        elif warrior.cmdType == "ORIENTATION":
            return self.orientationControl()
        elif warrior.cmdType == "SPEED":
            return self.speedControl()
        else:
            raise ValueError("Invalid cmdType")

    def reset(self):
        """Método para resetar uma varivável de tempo de transição

        Esse método reseta a variável de tempo de transição utilizado no backwards em vectorControl e positionControl
        """

        self.transitionTime = 0

    def vectorControl(self):
        """Controle por vetor
        No controle por vetor temos uma orientação alvo que é calculada no navigation.py, ao chegar nesse método
        é gerado um ponto na direção da orientação alvo, então é feito o mesmo processo do controle de posição.

        Returns:
            list: lista com velocidade da roda esquerda, velocidade da roda direita e orientação alvo respectivamente

        """

        if self.warrior.velAcc < Dice.acc:
            self.warrior.velAcc = Dice.acc

        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0, 0.0]

        theta = atan2(sin(self.warrior.transAngle), -cos(self.warrior.transAngle))
        target = [self.warrior.position[0] + cos(theta), self.warrior.position[1] + sin(theta)]

        targetTheta = atan2((target[1] - self.warrior.position[1]) * 1.3 / Endless.height,
                            -(target[0] - self.warrior.position[0]) * 1.5 / Endless.width)
        currentTheta = atan2(sin(self.warrior.orientation), cos(self.warrior.orientation))

        self.lastTime = time.time()
        self.deltaTime -= time.time() - self.lastTime

        if self.transitionTime > 0:
            self.transitionTime -= self.deltaTime

        else:
            if atan2(sin(targetTheta - currentTheta + pi / 2.0), -cos(targetTheta - currentTheta + pi / 2.0)) < 0.0:
                if not self.warrior.backward:
                    self.transitionTime = 1
                self.warrior.backward = True
                self.warrior.front = 1

            else:
                if self.warrior.backward:
                    self.transitionTime = 1
                self.warrior.backward = False
                self.warrior.front = -1

        if self.warrior.backward:
            currentTheta = currentTheta + pi
            currentTheta = atan2(sin(currentTheta), -cos(currentTheta))

        thetaError = atan2(sin(targetTheta - currentTheta), -cos(targetTheta - currentTheta))

        if self.warrior.velAcc < 1.0:
            self.warrior.velAcc = self.warrior.velAcc + 0.25
        else:
            self.warrior.velAcc = 1.0

        left = self.warrior.front + sin(thetaError)
        right = self.warrior.front - sin(thetaError)

        left = geometry.saturate(left)
        right = geometry.saturate(right)

        accDistance = 1 - geometry.gaussian(numpy.linalg.norm(numpy.asarray(self.warrior.position)
                                                              - numpy.asarray(self.warrior.target)), 15)

        accError = geometry.gaussian(thetaError, 15)

        left = self.warrior.vMax * left * accDistance * accError * self.warrior.velAcc
        right = self.warrior.vMax * right * accDistance * accError * self.warrior.velAcc

        return [left, right, self.warrior.transAngle]

    def positionControl(self):
        """Controle de posição

        No controle de posição temos um cálculo direto para encontrar as velocidades das rodas para sair da posição
        atual do robo e ir até uma posição target desejada. Sem controle de curvas ou preocupação com obstáculos.

        Returns:
            list: lista com velocidade da roda esquerda, velocidade da roda direita e orientação alvo respectivamente

        """

        if self.warrior.velAcc < Dice.acc:
            self.warrior.velAcc = Dice.acc

        if self.warrior.target[0] == -1 and self.warrior.target[1] == -1:
            return [0.0, 0.0, 0.0]

        targetTheta = atan2((self.warrior.target[1] - self.warrior.position[1]) * 1.3 / Endless.height,
                            -(self.warrior.target[0] - self.warrior.position[0]) * 1.5 / Endless.width)
        currentTheta = atan2(sin(self.warrior.orientation), cos(self.warrior.orientation))

        self.lastTime = time.time()
        self.deltaTime -= time.time() - self.lastTime

        if self.transitionTime > 0:
            self.transitionTime -= self.deltaTime

        else:
            if atan2(sin(targetTheta - currentTheta + pi / 2.0), -cos(targetTheta - currentTheta + pi / 2.0)) < 0.0:
                if not self.warrior.backward:
                    self.transitionTime = 1
                self.warrior.backward = True
                self.warrior.front = 1

            else:
                if self.warrior.backward:
                    self.transitionTime = 1
                self.warrior.backward = False
                self.warrior.front = -1

        if self.warrior.backward:
            currentTheta = currentTheta + pi
            currentTheta = atan2(sin(currentTheta), -cos(currentTheta))

        thetaError = atan2(sin(targetTheta - currentTheta), cos(targetTheta - currentTheta))

        if self.warrior.velAcc < 1.0:
            self.warrior.velAcc = self.warrior.velAcc + 0.25
        else:
            self.warrior.velAcc = 1.0

        left = self.warrior.front + sin(thetaError)
        right = self.warrior.front - sin(thetaError)

        left = geometry.saturate(left)
        right = geometry.saturate(right)

        accDistance = 1 - geometry.gaussian(numpy.linalg.norm(numpy.asarray(self.warrior.position)
                                                              - numpy.asarray(self.warrior.target)), 15)
        accError = geometry.gaussian(thetaError, 15)

        left = self.warrior.vMax * left * accDistance * accError * self.warrior.velAcc
        right = self.warrior.vMax * right * accDistance * accError * self.warrior.velAcc

        return [left, right, targetTheta]

    def orientationControl(self):
        """Controle de orientação

        No controle de aceleração temos a orientação atual do robô e uma orientação final desejada,
        onde então será calculado as velocidades necessárias para um giro onde ao final do giro o robô esteja com
        a orientação desejada.

        Returns:
            list: lista com velocidade da roda esquerda, velocidade da roda direita e orientação alvo respectivamente

        """

        # Se a frente do robô estiver na direção contrária ao alvo, robô nao gira
        # As duas partes do robôs são consideradas como frente mediante situação
        if geometry.roundAngle(self.warrior.targetOrientation - self.warrior.orientation + pi/2.0) < 0.0:
            self.warrior.orientation = geometry.roundAngle(self.warrior.orientation + pi)

        thetaError = geometry.roundAngle(self.warrior.targetOrientation - self.warrior.orientation)

        if abs(thetaError) < 2 * pi / 180.0:
            return [0.0, 0.0, 0.0]

        self.warrior.vLeft = geometry.saturate(self.warrior.vMax * thetaError)
        self.warrior.vRight = geometry.saturate(-self.warrior.vMax * thetaError)
        # TODO test self.warrior.vLeft*self.warrior.vMax

        return [self.warrior.vLeft * self.warrior.vMax,
                self.warrior.vRight * self.warrior.vMax,
                self.warrior.targetOrientation]

    def speedControl(self):
        """Controle de velocidade

        No controle de velocidade não há cálculo de tragetória, apenas é enviado as velocidades diretamente.

        Returns:
            list: lista com velocidade da roda esquerda, velocidade da roda direita e orientação alvo respectivamente

        """

        # TODO Precisa fazer controle de deseceleração?

        if self.warrior.velAcc < Dice.acc:
            self.warrior.velAcc = Dice.acc

        if self.warrior.velAcc < 1.0:
            self.warrior.velAcc = self.warrior.velAcc + 0.25
        else:
            self.warrior.velAcc = 1.0

        self.warrior.vLeft *= self.warrior.velAcc
        self.warrior.vRight *= self.warrior.velAcc

        return [self.warrior.vLeft, self.warrior.vRight, 0.0]
