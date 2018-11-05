import math


def roundAngle(angle):
    theta = math.fmod(angle, 2 * math.pi)

    if theta > math.pi:
        theta = theta - (2 * math.pi)
    elif theta < -math.pi:
        theta = theta + (2 * math.pi)

    return theta


def gaussian(m, v):
    return math.exp(-(m**2) / (2 * (v**2)))


def wrap2pi(theta):
    if theta > math.pi:
        return theta - 2 * math.pi
    if theta < -math.pi:
        return 2 * math.pi + theta
    else:
        return theta


def saturate(value, bottomLimit=-1, topLimit=1):
    if value > topLimit:
        value = topLimit
    elif value < bottomLimit:
        value = bottomLimit

    return value


def projection(lastPos, pos, time, deltaTime):
    """Calcula a projeção de um objeto em um determinado tempo
    Args:
        lastPos: última posição do objeto, há _deltaTime_ segundos atrás
        pos: posição atual do objeto
        time: tempo no futuro da projeção
        deltaTime: tempo entre o _pos_ e o _lastPos_

    Returns:
        Posição projetada em _time_ segundos
    """
    deltaPos = (pos[0] - lastPos[0], pos[1] - lastPos[1])
    theta = math.atan2(deltaPos[1], deltaPos[0])

    nextPos = (pos[0] + time * deltaTime * (math.cos(theta)),
               pos[1] + time * deltaTime * (math.sin(theta)))

    return nextPos
