import io, sys, traceback
import discord
from discord.ext import commands

from clients.billycontroller import BillyController

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get")
    @commands.is_owner()
    async def get(self, ctx):
        print(BillyController.getChannel())


def setup(bot):
    bot.add_cog(DebugCog(bot))
