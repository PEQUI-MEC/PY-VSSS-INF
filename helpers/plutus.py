import json


class Plutus:
    """
    Deus grego da riqueza, o que *guarda* coisas valiosas
    Responsável por fazer o save/load das configurações do programa
    """
    def __init__(self, file="helpers/quicksave.json"):
        self.saveFile = None
        self.data = {}

        try:
            self.saveFile = open(file, 'w')
        except EnvironmentError:
            print("Failed to open '" + file + "'")

        try:
            self.data = json.load(self.saveFile)
            print("Plutus summoned")

        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)

    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set(self, key, value):
        if self.saveFile is None:
            return False

        self.data[key] = value
        try:
            json.dump(self.data, self.saveFile)
            return True
        except TypeError:
            print("Error saving to file.")
            return False
