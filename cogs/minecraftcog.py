import io, sys, traceback
import discord
from discord.ext import commands

import subprocess

bashCommand = "screen -list | grep -q minecraft"

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mstatus", aliases=["ms", "minecraftstatus"])
    async def mStatus(self, ctx):
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
        print("----------------------------------------")
        print(error)

def setup(bot):
    bot.add_cog(MinecraftCog(bot))
