import io, sys, traceback
import discord
from discord.ext import commands

from clients.billycontroller import BillyController
from controllers.configcontroller import ConfigController

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.config = ConfigController()

    @commands.command(name="config")
    async def config(self, ctx, *args):
        # check if edit command
        if len(args) > 2 and "-e" in args[0]:
            path = args[1].split('/')
            content = str(args[2])
            await self.config.edit(ctx.author, path, content)
        # end if

        # check if show command
        elif len(args) > 0 and "-e" not in args[0]:
            path = args[0].split('/')
            await self.config.show(ctx.author, path)
        # end elif

        # else list config
        else:
            await self.config.list(ctx.author)
        # end else

def setup(bot):
    bot.add_cog(ConfigCog(bot))
