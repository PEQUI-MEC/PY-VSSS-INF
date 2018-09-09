import math
from .robot import Robot


class Actions:

    def run(self, robot):

        if robot.action == 'stop':
            return self.stop(robot)
        elif robot.action == 'kick':
            return self.kick(robot)
        elif robot.action == 'lookAt':
            return self.lookAt(robot)
        elif robot.action == 'spinClockwise':
            return self.spinClockwise(robot)
        elif robot.action == 'spinCounterClockwise':
            return self.spinCounterClockWise(robot)
        else:
            pass

    def stop(self, robot):
        robot.cmdType = 'SPEED'
        robot.vMax = 0
        robot.vLeft = 0
        robot.vRight = 0
        robot.target = [-1, -1]

        return robot

    def lookAt(self, robot):
        if robot.targetOrientation is not None:
            robot.cmdType = 'ORIENTATION'

        elif robot.targetOrientation is None:
            x = robot.target[0] - robot.position[0]
            y = robot.target[1] - robot.position[1]
            robot.cmdType = 'ORIENTATION'
            robot.targetOrientation = math.atan2(y, -x)

        else:
            pass

        return robot

    def kick(self, robot):
        x = robot.target[0] - robot.position[0]
        y = robot.target[1] - robot.position[1]
        robot.cmdType = 'VECTOR'
        robot.transAngle = -math.atan2(-y, x)

        return robot

    def spinClockwise(self, robot):
        robot.cmdType = 'SPEED'
        robot.vLeft = robot.vMax
        robot.vRight = -robot.vMax

        return robot

    def spinCounterClockWise(self, robot):
        robot.cmdType = 'SPEED'
        robot.vLeft = -robot.vMax
        robot.vRight = robot.vMax

        return robot
