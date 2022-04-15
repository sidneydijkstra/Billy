from factories.uniqueidfactory import UniqueIdFactory

class BaseStrategy:
    def __init__(self):
        self.id = UniqueIdFactory.getIntId()

    def execute(self, bot, voiceClient, callback):
        pass

    def getTitle(self):
        return "#title"

    def getDescription(self):
        return "*"

    def toString(self):
        return "#title, *"
