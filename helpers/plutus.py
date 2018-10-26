import json
import os.path


class Plutus:
    """
    Deus grego da riqueza, o que *guarda* coisas valiosas
    Responsável por fazer o save/load das configurações do programa
    """
    def __init__(self, file="helpers/quicksave.json"):
        self.data = {}
        self.file = file
        loadFile = None

        try:
            loadFile = open(file, "r")
        except EnvironmentError:
            print("File is empty")

        try:
            if loadFile:
                self.data = json.load(loadFile)
        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)
            return

        if loadFile is not None:
            loadFile.close()

        print("Plutus summoned")

    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set(self, key, value):
        self.data[key] = value

        try:
            saveFile = open(self.file, 'w+')
            json.dump(self.data, saveFile)
            saveFile.close()
            return True
        except TypeError:
            print("Error saving to file.")
            return False
