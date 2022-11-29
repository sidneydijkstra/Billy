from factories.uniqueidfactory import UniqueIdFactory
from datetime import datetime

class BaseStrategy:
    def __init__(self, hidden = False):
        self.id = UniqueIdFactory.getIntId()
        self.hidden = hidden
        self.currentTimePlayed = datetime.now()

    def execute(self, bot, voiceClient, callback):
        self.currentTimePlayed = datetime.now()
        pass

    def getTitle(self):
        return "#title"

    def getDescription(self):
        return "*"

    def getCurrentTimePlayed(self):
        return self.currentTimePlayed

    def toString(self):
        return "#title, *"
