import os
import discord

from clients.billy import Billy

COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')

class BillyController:
    bot = None
    currentMessageChannel = None

    @staticmethod
    def setup():
        BillyController.bot = Billy(
            command_prefix = COMMAND_PREFIX,
            description = 'Robot Billy'
        )
        BillyController.bot.addInitCallback(BillyController.init)
        BillyController.bot.load_extension("cogs.debugcog")
        BillyController.bot.load_extension("cogs.radiocog")
        BillyController.bot.load_extension("cogs.admincog")
        #bot.load_extension("cogs.voicechannelcog")
        #bot.load_extension("cogs.minecraftcog")
        BillyController.bot.run(os.getenv('DISCORD_TOKEN'), bot = True)

    @staticmethod
    def init():
        for guild in BillyController.bot.guilds:
            for channel in guild.channels:
                if str(channel.type) == 'text' and channel.name == DISCORD_CHANNEL:
                    BillyController.currentMessageChannel = channel
                    print(channel)

    @staticmethod
    def getBot():
        return BillyController.bot

    def getChannel():
        return BillyController.currentMessageChannel

    def hasChannel():
        return BillyController.currentMessageChannel != None

    @staticmethod
    def getVoice():
        # return voice channel of bot
        if BillyController.bot.voice_clients and BillyController.bot.voice_clients[0]:
            return BillyController.bot.voice_clients[0]
        return None

    @staticmethod
    async def joinChannel(channel):
        # on no channel exit function
        if channel == None:
            return
        ## get voice client of bot
        voiceClient = BillyController.bot.voice_clients
        # check if bot already in voice channel
        if voiceClient:
            # if bot already in channel exit function
            if voiceClient[0].channel == channel:
                return
            # leave that channel
            await voiceClient[0].disconnect()
        # join new channel
        await channel.connect()

    @staticmethod
    async def joinUser(user):
        # on no user, voice or channel exit function
        if user == None or user.voice == None or user.voice.channel == None:
            return
        ## get voice client of bot
        voiceClient = BillyController.bot.voice_clients
        # check if bot already in voice channel
        if voiceClient:
            # if bot already in channel exit function
            if voiceClient[0].channel == user.voice.channel:
                return
            # leave that channel
            await voiceClient[0].disconnect()
        # join new channel
        await user.voice.channel.connect()


    @staticmethod
    async def leaveChannel():
        ## get voice client of bot
        voiceClient = BillyController.bot.voice_clients
        # check if bot in voice channel
        if voiceClient:
            # leave that channel
            await voiceClient[0].disconnect()
