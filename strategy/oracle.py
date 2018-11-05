import time
import math
from scipy.spatial import distance


class Oracle:
    """
    Ser que possui o poder de prever o futuro de instâncias
    """

    def __init__(self, maxReads, meterPixelRatio):
        self.history = []
        self.meterPixelRatio = meterPixelRatio
        self.maxReads = maxReads

    def pushState(self, position):
        registry = (position, time.time())
        self.history.append(registry)
        if len(self.history) > 10:
            self.history.pop(0)

    def predict(self, timeAhead):
        """Calcula a projeção de um objeto em um determinado tempo
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

        velocity = 100 * dist / (deltaTime * self.meterPixelRatio)

        theta = math.atan2(deltaPos[1], deltaPos[0])

        nextPos = (self.history[-1][0][0] + timeAhead * velocity * math.cos(theta),
                   self.history[-1][0][1] + timeAhead * velocity * math.sin(theta))

        return nextPos
