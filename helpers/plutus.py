import json
import os.path


class Plutus:
    """
    Deus grego da riqueza, o que *guarda* coisas valiosas
    Responsável por fazer o save/load das configurações do programa
    """
    def __init__(self):
        self.file = None
        print("Plutus summoned")

    def setFile(self, file):
        self.file = "helpers/" + file + ".json"

    def get(self, key=None):
        if key is None:
            try:
                loadFile = open(self.file, "r")
            except EnvironmentError:
                print("File is empty")
                return False

            return True

        data = {}
        loadFile = open(self.file, "r")

        try:
            if loadFile:
                data = json.load(loadFile)
        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)
            return

        if loadFile is not None:
            loadFile.close()

        if key in data:
            return data[key]
        else:
            return None

    def set(self, key, value):
        data = {}
        loadFile = None
        try:
            loadFile = open(self.file, "r")
        except EnvironmentError:
            print("File is empty")

        try:
            if loadFile:
                data = json.load(loadFile)
        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)
            return

        if loadFile is not None:
            loadFile.close()

        data[key] = value

        try:
            saveFile = open(self.file, 'w+')
            json.dump(data, saveFile)
            saveFile.close()
            return True
        except TypeError:
            print("Error saving to file.")
            return False
