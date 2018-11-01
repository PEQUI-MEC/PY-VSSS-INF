import math


def roundAngle(angle):
    theta = math.fmod(angle, 2 * math.pi)

    if theta > math.pi:
        theta = theta - (2 * math.pi)
    elif theta < -math.pi:
        theta = theta + (2 * math.pi)

    return theta
