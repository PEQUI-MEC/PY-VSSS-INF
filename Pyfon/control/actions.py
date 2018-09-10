import math


class Actions:

    def run(self, robot):
        if robot.action[0] == "stop":
            return self.stop(robot)
        elif robot.action[0] == "lookAt":
            return self.lookAt(robot)
        elif robot.action[0] == "spin":
            return self.spin(robot)
        elif robot.action[0] == "goTo":
            return self.goTo(robot)

    def stop(self, robot):
        robot.cmdType = 'SPEED'
        robot.vMax = 0
        robot.vLeft = 0
        robot.vRight = 0
        robot.target = [-1, -1]

        return robot

    def lookAt(self, robot):
        robot.cmdType = "ORIENTATION"

        if robot.action[1] == "target":
            x = robot.target[0] - robot.position[0]
            y = robot.target[1] - robot.position[1]
            robot.cmdType = "ORIENTATION"
            robot.targetOrientation = math.atan2(y, -x)

        return robot

    def spin(self, robot):
        robot.cmdType = "SPEED"
        if robot.action[1] == "clockwise":
            robot.vLeft = robot.vMax
            robot.vRight = -robot.vMax
        else:
            robot.vLeft = -robot.vMax
            robot.vRight = robot.vMax

        return robot

    def goTo(self, robot):
        pass
