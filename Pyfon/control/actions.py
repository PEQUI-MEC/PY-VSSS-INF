from . import constants
import math


class Actions:

    def setup(self, robot):
        self.robot = robot

        if self.robot[constants._actionsCommand] == 'stop':
            Actions().stop(self.robot)
            return True
        elif self.robot[constants._actionsCommand] == 'kick':
            Actions().kick(self.robot)
            return True
        elif self.robot[constants._actionsCommand] == 'lookAt':
            Actions().lookAt(self.robot)
            return True
        elif self.robot[constants._actionsCommand] == 'spinClockwise':
            Actions().spinClockwise(self.robot)
            return True
        elif self.robot[constants._actionsCommand] == 'spinCounterClockWise':
            Actions().spinCounterClockWise(self.robot)
            return True
        else:
            return False

    def stop(self, robot):
        self.robot = robot
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vMax] = 0
        self.robot[constants._vLeft] = 0
        self.robot[constants._vRight] = 0
        self.robot[constants._target] = [-1, -1]

    def lookAt(self, robot):
        self.robot = robot
        x = self.robot[constants._target][0] - self.robot[constants._position][0]
        y = self.robot[constants._target][1] - self.robot[constants._position][1]
        self.robot[constants._cmdType] = 'ORIENTATION'
        self.robot[constants._targetOrientation] = math.atan2(x, -y)

    def kick(self, robot):
        self.robot = robot
        x = self.robot[constants._target][0] - self.robot[constants._position][0]
        y = self.robot[constants._target][1] - self.robot[constants._position][1]
        self.robot[constants._cmdType] = 'VECTOR'
        self.robot[constants._transAngle] = -math.atan2(x, y)

    def spinClockwise(self, robot):
        self.robot = robot
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vLeft] = self.robot[constants._vMax]
        self.robot[constants._vRight] = -(self.robot[constants._vMax])

    def spinCounterClockWise(self, robot):
        self.robot = robot
        self.robot[constants._cmdType] = 'SPEED'
        self.robot[constants._vLeft] = -(self.robot[constants._vMax])
        self.robot[constants._vRight] = self.robot[constants._vMax]

