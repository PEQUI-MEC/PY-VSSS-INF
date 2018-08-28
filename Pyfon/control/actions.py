from . import constants


class Actions:
    robot = []

    def setup(robot):
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
        pass

    def kick(self):
        pass

    def lookAt(self):
        return True

    def spinClockwise(self):
        pass

    def spinCounterClockWise(self):
        pass