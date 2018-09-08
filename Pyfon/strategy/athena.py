# coding=utf-8
from .endless import Endless
from .warrior import Warrior

class Athena:
    def __init__(self, callback):
        self.endless = None
        self.warriors = []
        self.theirWarriors = []
        print("Athena summoned.")

        self.callback = callback
    
    def run(self, positions):
        print("\tAthena working on " + positions)
        commands = "commands"
        self.callback(commands)

    def setup(self, numRobots, width, height):
        self.endless = Endless(width, height)
        for i in range(0, numRobots):
            self.warriors.append(Warrior())

        print("Athena is set up.")
        return self

    '''
    Recebe um objeto do tipo
    [
        [ # robôs aliados
            {
                "x": posição_x
                "y": posição_y
                "orientation": orientação
            },
            {
                "x": posição_x
                "y": posição_y
                "orientation": orientação
            },
            {
                "x": posição_x
                "y": posição_y
                "orientation": orientação
            }
        ],
        [ # robôs adversários
            {
                "x": posição_x
                "y": posição_y
            },
            {
                "x": posição_x
                "y": posição_y
            },
            {
                "x": posição_x
                "y": posição_y
            }
        ],
        { # bola
            "x": posição_x
            "y": posição_y
        }
    ]
    '''
    def getTargets(self, positions):
        self.parsePositions(positions)
        self.analyzeState()
        self.setRoles()
        self.selectTactics()
        self.selectActions()
        return self.generateResponse(self.warriors)

    # TODO fazer mais verificações
    def parsePositions(self, positions):
        if type(positions) is not list or type(positions[0]) is not list or type(positions[1]) is not list or type(positions[2]) is not dict:
            raise ValueError("Invalid positions object received.")

        for i in range(0, len(positions[0])):
            if type(positions[0][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.warriors[i].setup({positions[0][i]["x"], positions[0][i]["y"]}, positions[0][i]["orientation"])

        self.theirWarriors = []
        for i in range(0, len(positions[1])):
            if type(positions[1][i]) is not dict:
                raise ValueError("Invalid value for our warriors received.")

            self.theirWarriors.append(Warrior())
            self.theirWarriors[i].setup({positions[1][i]["x"], positions[1][i]["y"]})

        return positions

    def generateResponse(self, warriors):
        response = []
        for warrior in warriors:
            response.append({
                "command": warrior.command
            })

        return response

    def analyzeState(self):
        pass

    def setRoles(self):
        pass

    def selectTactics(self):
        pass

    def selectActions(self):
        for warrior in self.warriors:
            warrior.command = "atack"

        return self.warriors


def main():
    fictionalPositions = [
        [
            {
                "x": 100,
                "y": 200,
                "orientation": 0.5
            },
            {
                "x": 100,
                "y": 200,
                "orientation": 0.5
            },
            {
                "x": 100,
                "y": 200,
                "orientation": 0.5
            }
        ],
        [
            {
                "x": 100,
                "y": 200
            },
            {
                "x": 100,
                "y": 200
            },
            {
                "x": 100,
                "y": 200
            }
        ],
        {
            "x": 100,
            "y": 200
        }
    ]
    athena = Athena()
    athena.setup(3, 100, 100)
    print(athena.getTargets(fictionalPositions))


if __name__ == "__main__":
    main()
