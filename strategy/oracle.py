import time
import math
from scipy.spatial import distance


class Oracle:
    """
    Ser que possui o poder de prever o futuro de instâncias
    """

    def __init__(self, maxReads):
        self.history = []
        self.maxReads = maxReads
        self.velocity = 0  # deve ser utilizado após um predict

    def pushState(self, position, readTime=-1):
        """Adiciona um novo estado ao histórico apagando, se necessário, o mais antigo
        Args:
            position: Novo estado
            readTime: Quando o estado foi lido
        Returns:
            tuple: Estado mais novo da lista e quando foi lido
        """

        registry = (position, time.time() if readTime < 0 else readTime)
        self.history.append(registry)
        if len(self.history) > 10:
            self.history.pop(0)

        return self.history[-1]

    def predict(self, timeAhead):
        """
        Calcula a projeção de um objeto em um determinado tempo

        Args:
            timeAhead: tempo no futuro de projeção

        Returns:
            Posição projetada em _time_ segundos
        """
        deltaPos = (self.history[-1][0][0] - self.history[0][0][0], self.history[-1][0][1] - self.history[0][0][1])
        dist = distance.euclidean(self.history[-1][0], self.history[0][0])
        deltaTime = self.history[-1][1] - self.history[0][1]

        if deltaTime == 0:
            return self.history[-1][0]

        self.velocity = dist / deltaTime

        theta = math.atan2(deltaPos[1], deltaPos[0])

        nextPos = (self.history[-1][0][0] + timeAhead * self.velocity * math.cos(theta),
                   self.history[-1][0][1] + timeAhead * self.velocity * math.sin(theta))

        return nextPos

    def getY(self, x):
        """
        Calcula o Y da projeção do vetor do objeto em um determinado X

        Args:
            x: posição no eixo X em que a reta passará

        Returns:
            float y: posição no eixo Y em que a reta passa
        """

        if self.history[-1][0][0] - self.history[0][0][0] == 0:
            return self.history[-1][0][1]

        m = (self.history[-1][0][1] - self.history[0][0][1]) / (self.history[-1][0][0] - self.history[0][0][0])
        pred_y = self.history[-1][0][1] - m * (self.history[-1][0][0] - x)
        return pred_y
