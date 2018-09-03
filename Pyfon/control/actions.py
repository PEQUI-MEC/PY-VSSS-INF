import math
from .robot import Robot


class Actions:

    def setup(self, robot):
        actions = Actions()

        if robot.get('actions') == 'stop':
            return actions.stop(robot)
        elif robot.get('actions') == 'kick':
            return actions.kick(robot)
        elif robot.get('actions') == 'lookAt':
            return actions.lookAt(robot)
        elif robot.get('actions') == 'spinClockwise':
            return actions.spinClockwise(robot)
        elif robot.get('actions') == 'spinCounterClockWise':
            return actions.spinCounterClockWise(robot)
        else:
            return False


    def stop(self, robot):
        robot.set('cmdType', 'SPEED')
        robot.set('vMax', 0)
        robot.set('vLeft', 0)
        robot.set('vRight', 0)
        robot.set('target', [-1, -1])

        return robot

    def lookAt(self, robot):
        if robot.get('orientation') is not None:
            robot.set('cmdType', 'ORIENTATION')
            robot.set('targetOrientation', robot.get('orientation'))

        if robot.get('orientation') is None and robot.get('targetOrientation') is not None:
            x = robot.get('target')[0] - robot.get('position')[0]
            y = robot.get('target')[1] - robot.get('position')[1]
            robot.set('cmdType', 'ORIENTATION')
            robot.set('targetOrientation', math.atan2(y, -x))

        else:
            pass

        return robot

    def kick(self, robot):
        x = robot.get('target')[0] - robot.get('position')[0]
        y = robot.get('target')[1] - robot.get('position')[1]
        robot.set('cmdType', 'VECTOR')
        robot.set('transAngle', -math.atan2(-y, x))

        return robot

    def spinClockwise(self, robot):
        robot.set('cmdType', 'SPEED')
        robot.set('vLeft', robot.get('vMax'))
        robot.set('vRight', -robot.get('vMax'))

        return robot

    def spinCounterClockWise(self, robot):
        robot.set('cmdType', 'SPEED')
        robot.set('vLeft', -robot.get('vMax'))
        robot.set('vRight', robot.get('vMax'))

        return robot
