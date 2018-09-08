from .actions import Actions
from .translate import Translate


class Zeus:
    robots = []

    def __init__(self, callback):
        print("Zeus summoned")
        self.callback = callback

    def run(self, commands):
        print("\tZeus working on " + commands)
        messages = "mensagens"
        self.callback(messages)

    def setup(self):
        return True

    def getRobots(self, robots):
        print("Zeus working.")
        print("\t" + robots)

    def generateJson(self):
        pass

    def controlRoutine(self):
        pass