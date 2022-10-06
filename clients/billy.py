import discord
from discord.ext import commands

from factories.messagefactory import MessageFactory
from factories.embeddedfactory import EmbeddedFactory

class Billy(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initCallbacks = []

    def addInitCallback(self, callback):
        self.initCallbacks.append(callback)

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

        for callback in self.initCallbacks:
            callback()

    async def on_command_error(self, context, exception):
        await MessageFactory.sendErrorMessage(context, context.message.content, exception)

    async def on_message(self, message): # on tag
        if message.author == self.user:
            return

        if self.user in message.mentions:
            if message.author.id == message.guild.owner_id:
                await message.channel.send("Dag papa! Ik heb je gemist!")
                return

            embeddedBlock = EmbeddedFactory.generateMentionMessage()
            await message.channel.send("Hey Hoi, " + message.author.name + "! Ik zie dat je me een bericht stuurt, dus ik denk dat je me aandacht wil!", embed=embeddedBlock)
        else:

            if message.content[0] == "$":
                print("Processing command from %s, %s" % (message.author.name, message.content))

            await self.process_commands(message)
