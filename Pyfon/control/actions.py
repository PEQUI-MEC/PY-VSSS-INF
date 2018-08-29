from . import constants
import math


class Actions:
    robot = []

    def setup(self, robot):
        __class__.robot = robot

        if __class__.robot[constants._actionsCommand] == 'stop':
            return Actions().stop()
        elif __class__.robot[constants._actionsCommand] == 'kick':
            return Actions().kick()
        elif __class__.robot[constants._actionsCommand] == 'lookAt':
            return Actions().lookAt()
        elif __class__.robot[constants._actionsCommand] == 'spinClockwise':
            return Actions().spinClockwise()
        elif __class__.robot[constants._actionsCommand] == 'spinCounterClockWise':
            return Actions().spinCounterClockWise()
        else:
            return False

    def stop(self):
        __class__.robot[constants._cmdType] = 'SPEED'
        __class__.robot[constants._vMax] = 0
        __class__.robot[constants._vLeft] = 0
        __class__.robot[constants._vRight] = 0
        __class__.robot[constants._target] = [-1, -1]

    def lookAt(self):
        x = __class__.robot[constants._target][0] - __class__.robot[constants._position][0]
        y = __class__.robot[constants._target][1] - __class__.robot[constants._position][1]
        __class__.robot[constants._cmdType] = 'ORIENTATION'
        __class__.robot[constants._targetOrientation] = math.atan2(x, -y)

    def kick(self):
        x = __class__.robot[constants._target][0] - __class__.robot[constants._position][0]
        y = __class__.robot[constants._target][1] - __class__.robot[constants._position][1]
        __class__.robot[constants._cmdType] = 'VECTOR'
        __class__.robot[constants._transAngle] = -math.atan2(x, y)

    def spinClockwise(self):
        __class__.robot[constants._cmdType] = 'SPEED'
        __class__.robot[constants._vLeft] = __class__.robot[constants._vMax]
        __class__.robot[constants._vRight] = -(__class__.robot[constants._vMax])

    def spinCounterClockWise(self):
        __class__.robot[constants._cmdType] = 'SPEED'
        __class__.robot[constants._vLeft] = -(__class__.robot[constants._vMax])
        __class__.robot[constants._vRight] = __class__.robot[constants._vMax]