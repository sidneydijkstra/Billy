import discord
from discord.ext import commands

from factories.embeddedfactory import EmbeddedFactory

class Billy(commands.Bot):

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def on_message(self, message): # on tag
        if message.author == self.user:
            return



        if self.user in message.mentions:
            if message.author == message.guild.owner:
                await message.channel.send("Dag papa! Ik heb je gemist!")
                return

            embeddedBlock = EmbeddedFactory.generateMentionMessage()
            await message.channel.send("Hey Hoi, " + message.author.name + "! Ik zie dat je me een bericht stuurt, dus ik denk dat je me aandacht wil!", embed=embeddedBlock)
        else:

            if message.content[0] == "$":
                print("Processing command from %s, %s" % (message.author.name, message.content))

            await self.process_commands(message)
