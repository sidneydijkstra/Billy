import os
import discord

from clients.billy import Billy
from managers.configmanager import ConfigManager
systemConfig = ConfigManager.get('system')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class BillyController:
    bot = None
    currentMessageChannel = None

    @staticmethod
    def setup():
        BillyController.bot = Billy(
            command_prefix = systemConfig['commandPrefix'],
            description = systemConfig['name']
        )
        BillyController.bot.addInitCallback(BillyController.init)
        BillyController.bot.load_extension("cogs.debugcog")
        BillyController.bot.load_extension("cogs.radiocog")
        BillyController.bot.load_extension("cogs.admincog")
        BillyController.bot.load_extension("cogs.configcog")
        BillyController.bot.load_extension("cogs.statscog")
        BillyController.bot.run(DISCORD_TOKEN, bot = True)

    @staticmethod
    def init():
        for guild in BillyController.bot.guilds:
            for channel in guild.channels:
                if str(channel.type) == 'text' and channel.name == systemConfig['textChannel']:
                    BillyController.currentMessageChannel = channel
                    print(channel)

    @staticmethod
    async def setIdle():
        # set activity status
        await BillyController.getBot().change_presence(activity=None)

    @staticmethod
    async def setStatus(status):
        # set activity status
        await BillyController.getBot().change_presence(activity=discord.Game(status))

    @staticmethod
    def getBot():
        return BillyController.bot

    @staticmethod
    def getChannel():
        return BillyController.currentMessageChannel

    @staticmethod
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
