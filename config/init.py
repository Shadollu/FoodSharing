import configparser


class init:
    def __init__(self, configName):
      self.config = configparser.ConfigParser()
      self.config.read(configName)

    def getVal(self, key, value):
        return self.config.get(key, value)
