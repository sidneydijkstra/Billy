import discord

class UniqueIdFactory:
    uniqueIntId = 0

    def getIntId():
        id = UniqueIdFactory.uniqueIntId
        UniqueIdFactory.uniqueIntId = UniqueIdFactory.uniqueIntId + 1
        return id
