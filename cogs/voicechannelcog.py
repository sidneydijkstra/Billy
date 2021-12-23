import os
import random
import asyncio
import queue
import discord
from discord.ext import commands

from factories.embeddedfactory import EmbeddedFactory
from factories.audiofactory import AudioFactory

class VoiceChannelCog(commands.Cog):
    def __init__(self, bot):
        self.JINGLE_PLAY_CHANCE = 0.4
        self.bot = bot
        self.queue = []
        print(os.listdir("./audio/radio/"))

    @commands.command(name="load")
    async def load(self, ctx, arg1):
        await AudioFactory.loadVideo(arg1)

    @commands.command(name="join")
    async def join(self, ctx):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

    @commands.command(name="leave")
    async def leave(self, ctx):
        await AudioFactory.leaveChannel(ctx.bot, ctx.author)

    @commands.command(name="fplay")
    async def fplay(self, ctx):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and not voice_client.is_playing():
            jingles = os.listdir("./audio/radio")
            jingle = jingles[random.randint(0, len(jingles) - 1)]
            voice_client.play(AudioFactory.getVideoFromSource("./audio/radio/" + jingle), after=lambda ex: ptint(ex) if ex else print("done fplay!"))


    @commands.command(name="play")
    async def play(self, ctx, *args):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

        audioInfo = None
        if len(args) > 0 and "https://" in args[0]:
                audioInfo = AudioFactory.getVideoFromUrl(args[0], ctx.author)
        elif len(args) > 1:
            search = ""
            for i in args:
                search += str(i) + " "
            audioInfo = AudioFactory.getVideoFromSearch(search, ctx.author)
        elif len(args) > 0:
            audioInfo = AudioFactory.getVideoFromSearch(args[0], ctx.author)

        if not audioInfo:
            return

        self.queue.append(audioInfo)

        if ctx.message:
            await ctx.message.delete()

        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client.is_playing():
            await self._play(ctx)
        else:
            await ctx.message.channel.send("Ik heb het verzoekje van %s toegevoegd, B-B-Billy radio!!" % (audioInfo.auther), embed=EmbeddedFactory.generateAudioInfoMessage(audioInfo))

    @commands.command(name="skip")
    async def skip(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing() and self.queue:
            voice_client.stop()

    @commands.command(name="list")
    async def list(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and self.queue:
            await ctx.message.channel.send(embed=EmbeddedFactory.generateAudioQueueMessage(self.queue))

    @commands.command(name="stop")
    async def stop(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            self.queue.clear()
            voice_client.stop()

    @commands.command(name="pause")
    async def pause(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        elif voice_client and voice_client.is_paused():
            voice_client.resume()

    async def _play(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and not voice_client.is_playing() and self.queue:
            audioInfo = self.queue.pop(0)
            await ctx.message.channel.send("B-B-B-Billy Radio met een verzoekje van %s!" % (audioInfo.auther), embed=EmbeddedFactory.generateAudioInfoMessage(audioInfo))
            voice_client.play(audioInfo.ffmpegAudio, after=lambda ex: asyncio.run_coroutine_threadsafe(self._jingle(ctx), self.bot.loop) if random.random() < self.JINGLE_PLAY_CHANCE else asyncio.run_coroutine_threadsafe(self._play(ctx), self.bot.loop))

    async def _jingle(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and not voice_client.is_playing() and self.queue:
            jingles = os.listdir("./audio/radio")
            jingle = jingles[random.randint(0, len(jingles) - 1)]
            voice_client.play(AudioFactory.getVideoFromSource("./audio/radio/" + jingle), after=lambda ex: asyncio.run_coroutine_threadsafe(self._play(ctx), self.bot.loop))



def setup(bot):
    bot.add_cog(VoiceChannelCog(bot))
