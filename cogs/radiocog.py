import io, sys, traceback
import discord
from discord.ext import commands

from clients.billycontroller import BillyController
from controllers.radiocontroller import RadioController

class RadioCog(commands.Cog):
    def __init__(self, bot):
        self.radio = RadioController()

    #@commands.command(name="shutdown", aliases=["q", "quit"], help = "- Shutdown the bot.") 
    @commands.command(name="join")
    async def join(self, ctx):
        await BillyController.joinUser(ctx.author)

    @commands.command(name="leave")
    async def leave(self, ctx):
        await BillyController.leaveChannel()

    @commands.command(name="play")
    async def play(self, ctx, *args):
        print(args)
        if len(args) > 0 and "https://" in args[0]: # url
            await self.radio.playUrl(ctx.author, args[0])
        elif len(args) > 1 and args[0] == "-s": # soundcloud
            await self.radio.playSource(ctx.author, args[1])
        elif len(args) > 0 and args[0] == "-top": # top songs
            await self.radio.playTop(ctx.author, 10 if len(args) == 1 else int(args[1]))
        elif len(args) > 0 and args[0] != "-s": # search
            await self.radio.playSearch(ctx.author, ' '.join(args))

    @commands.command(name="say")
    async def say(self, ctx, *args):
        if len(args) > 0:
            await self.radio.say(ctx.author, ' '.join(args))
            
    @commands.command(name="pause")
    async def pause(self, ctx):
        await self.radio.pause()

    @commands.command(name="stop")
    async def stop(self, ctx):
        await self.radio.stop()

    @commands.command(name="remove")
    async def remove(self, ctx, *args):
        if len(args) > 0 and args[0].isdigit():
            await self.radio.remove(int(args[0]))

    @commands.command(name="list")
    async def list(self, ctx, *args):
        if len(args) > 0 and isinstance(int(args[0]), int):
            await self.radio.list(int(args[0]))
        else:
            await self.radio.list()

    @commands.command(name="skip")
    async def skip(self, ctx):
        await self.radio.skip()


def setup(bot):
    bot.add_cog(RadioCog(bot))
