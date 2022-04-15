import io, sys, traceback
import discord
from discord.ext import commands

from clients.billycontroller import BillyController
from controllers.radiocontroller import RadioController

class RadioCog(commands.Cog):
    def __init__(self, bot):
        self.radio = RadioController()

    @commands.command(name="join")
    async def join(self, ctx):
        await BillyController.joinUser(ctx.author)

    @commands.command(name="leave")
    async def leave(self, ctx):
        await BillyController.leaveChannel()

    @commands.command(name="play")
    async def play(self, ctx, *args):
        if len(args) > 0 and "https://" in args[0]:
            await self.radio.playUrl(ctx.message.channel, ctx.author, args[0])
        elif len(args) > 1 and args[0] == "-s":
            await self.radio.playSource(ctx.message.channel, ctx.author, args[1])
        elif len(args) > 0 and args[0] != "-s":
            await self.radio.playSearch(ctx.message.channel, ctx.author, ' '.join(args))

    @commands.command(name="stop")
    async def stop(self, ctx):
        await self.radio.stop()

    @commands.command(name="remove")
    async def remove(self, ctx, *args):
        if len(args) > 0 and args[0].isdigit():
            await self.radio.remove(int(args[0]))

    @commands.command(name="list")
    async def list(self, ctx):
        await self.radio.list()

    @commands.command(name="skip")
    async def skip(self, ctx):
        await self.radio.skip()

    @commands.command(name="_p")
    async def _p(self, ctx):
        pass


def setup(bot):
    bot.add_cog(RadioCog(bot))
