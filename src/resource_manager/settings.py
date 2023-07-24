import os

class settings:
    def __init__(self):
        self.settings_dic = {}

    def loadConfig(self):
        try:
            with open("config.txt") as file:
                temp = file.read().splitlines()
                for line in temp:
                    name, var = line.partition(":")[::2]
                    self.settings_dic[name.strip()] = var
        except:
            return -1
        return 0

    def printSettings(self):
        print(self.settings_dic)
        return 0

    def getSettings(self):
        return self.settings_dic

    def getDicValue(self, key):
        return self.settings_dic[key]
