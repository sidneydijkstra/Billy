import discord
import uuid

class UniqueIdFactory:
    uniqueIntId = 0

    def getIntId():
        id = UniqueIdFactory.uniqueIntId
        UniqueIdFactory.uniqueIntId = UniqueIdFactory.uniqueIntId + 1
        return id

    def getUuid():
        return str(uuid.uuid4())
