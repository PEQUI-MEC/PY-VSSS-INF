from . import constants
import math


class Actions:

    robot = []

    @staticmethod
    def setup(robot):
        actions = Actions()
        actions.robot = robot

        if robot[constants._actionsCommand] == 'stop':
            actions.stop()
        elif robot[constants._actionsCommand] == 'kick':
            actions.kick()
        elif robot[constants._actionsCommand] == 'lookAt':
            actions.lookAt()
        elif robot[constants._actionsCommand] == 'spinClockwise':
            actions.spinClockwise()
        elif robot[constants._actionsCommand] == 'spinCounterClockWise':
            actions.spinCounterClockWise()
        else:
            return False

        return robot

    def stop(self):
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vMax] = 0
        self.robot[constants._vLeft] = 0
        self.robot[constants._vRight] = 0
        self.robot[constants._target] = [-1, -1]

    def lookAt(self):

        if self.robot[constants._orientation] is None and self.robot[constants._targetOrientation] is not None:
            x = self.robot[constants._target][0] - self.robot[constants._position][0]
            y = self.robot[constants._target][1] - self.robot[constants._position][1]
            self.robot[constants._cmdType] = 'ORIENTATION'
            self.robot[constants._targetOrientation] = math.atan2(-y, -x)

        elif self.robot[constants._targetOrientation] is None and self.robot[constants._orientation] is not None:
            self.robot[constants._cmdType] = 'ORIENTATION'
            self.robot[constants._targetOrientation] = self.robot[constants._orientation]

        else:
            pass

    def kick(self):
        x = self.robot[constants._target][0] - self.robot[constants._position][0]
        y = self.robot[constants._target][1] - self.robot[constants._position][1]
        self.robot[constants._cmdType] = 'VECTOR'
        self.robot[constants._transAngle] = -math.atan2(-y, x)

    def spinClockwise(self):
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vLeft] = self.robot[constants._vMax]
        self.robot[constants._vRight] = -(self.robot[constants._vMax])

    def spinCounterClockWise(self):
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vLeft] = -(self.robot[constants._vMax])
        self.robot[constants._vRight] = self.robot[constants._vMax]

