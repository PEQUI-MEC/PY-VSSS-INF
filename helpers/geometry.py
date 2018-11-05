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
