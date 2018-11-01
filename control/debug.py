import navigation
import numpy as np
import random
import cv2
import math
import time


w, h = 150, 130
teamColor = (255, 0, 0)
enemyColor = (0, 255, 255)
ballColor = (31, 136, 246)
pathColor = (255, 0, 255)


def getObstacle():
    return np.array([random.randint(0, w-1), -random.randint(0, h-1)])


def getBall():
    return np.array([random.randint(0, w-1), -random.randint(0, h-1)])


def getRobot():
    return np.array([random.randint(0, w-1), -random.randint(0, h-1)])


def printObstacles(_obstacle, plt):
    for i in range(_obstacle.shape[0]):
        plt.plot(_obstacle[i][0], _obstacle[i][1], 'go')


def cm2pixel(pos):
    posArray = np.array(pos)
    return 4*posArray


def drawRobot(img, robotPos, enemy=False):
    if enemy:
        color = enemyColor
    else:
        color = teamColor

    pos = cm2pixel([robotPos[0], -robotPos[1]])
    topLeft = (pos[0]-15, pos[1]-15)
    bottomRight = (pos[0]+15, pos[1]+15)
    cv2.rectangle(img, topLeft, bottomRight, color, -1)


def drawObstacles(img, obstacles):
    if obstacles.size:
        for i in range(obstacles.shape[0]):
            drawRobot(img, obstacles[i], enemy=True)


def drawBall(img, ballPos):
    cv2.circle(img, (ballPos[0], -ballPos[1]), 9, ballColor, -1)


def drawField(img, univetField):
    for l in range(0, h, 2):
        for c in range(0, w, 2):
            pos = [c, -l]
            theta = univetField.univector(robotPos=pos, robotSpeed=[0, 0], orientation=np.array([160, 130]))

            v = np.array([np.cos(theta), np.sin(theta)])

            s = cm2pixel(np.array([c, l]))
            new = cm2pixel(np.array(pos)) + 8*v

            new[1] = -new[1]
            cv2.arrowedLine(img, tuple(np.int0(s)), tuple(np.int0(new)), (0,255,255), 1)


def drawPath(img, start, end, univetField):
    currentPos = start
    _currentPos = cm2pixel(currentPos)

    newPos = None
    alpha = 0.8
    beta = 1

    t0 = time.time()

    while np.linalg.norm(currentPos - end) >= beta:
        theta = univetField.univector(robotPos=currentPos, robotSpeed=[0,0], orientation=np.array([160, 130]))
        v = np.array([math.cos(theta), math.sin(theta)])
        newPos = currentPos + (alpha*v)
        _newPos = cm2pixel(newPos).astype(int)

        cv2.line(img, (_currentPos[0], -_currentPos[1]), (_newPos[0], -_newPos[1]), pathColor, 3)

        cv2.imshow('field', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if time.time() - t0 > 5:
            return False, newPos

        currentPos = newPos
        _currentPos = _newPos
    return True, None


def main(radius=6.0, kr=0.9, k0=0.12, dmin=20.0, lDelta=4.5):
    imgField = cv2.imread('vss-field.jpg')
    imgField2 = np.copy(imgField)

    robot = getRobot()
    ball = getBall()

    drawRobot(imgField2, robot)
    drawBall(imgField2, cm2pixel(ball))

    univetField = navigation.UnivectorField()
    univetField.updateConstants(radius, kr, k0, dmin, lDelta)

    univetField.updateTarget(ball, [160, 130])

    drawField(imgField2, univetField)
    ret, pos = drawPath(imgField2, robot, ball, univetField)

    cv2.imshow('field', imgField2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    del univetField


if __name__ == "__main__":
    main()
