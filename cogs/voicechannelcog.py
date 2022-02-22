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

        jingleFiles = os.listdir("./audio/radio")
        self.jingles = []
        for jingle in jingleFiles:
            self.jingles.append("./audio/radio/" + jingle)

        self.shuffleJingles()

    @commands.command(name="join", help = "- Let the bot join youre current channel")
    async def join(self, ctx):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

    @commands.command(name="leave", help = "- Remove the bot from the channel.")
    async def leave(self, ctx):
        await AudioFactory.leaveChannel(ctx.bot, ctx.author)

    @commands.command(name="splay", help = "- Play a sound from source location")
    async def splay(self, ctx, *args):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and not voice_client.is_playing():
            if len(args) > 0:
                source = "./audio/%s" % (args[0])
                voice_client.play(AudioFactory.getVideoFromSource(source), after=lambda ex: ptint(ex) if ex else print("done splay! -> %s" % (source)))

    @commands.command(name="fplay", help = "- Play a random jingle.")
    async def fplay(self, ctx):
        await AudioFactory.joinChannel(ctx.bot, ctx.author)

        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and not voice_client.is_playing():
            jingle = self.getJingle()
            voice_client.play(AudioFactory.getVideoFromSource(jingle), after=lambda ex: ptint(ex) if ex else print("done fplay! -> %d" % (len(self.shuffledJingles))))


    @commands.command(name="play", aliases=["p"], help = "- Add a new song to the queue by a search or a link.")
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

    @commands.command(name="skip", help = "- Skip a song from the queue.")
    async def skip(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing() and self.queue:
            voice_client.stop()

    @commands.command(name="remove", aliases=["rm"], help = "- Remove a song from the queue by it's id.")
    async def remove(self, ctx, *args):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if len(args) > 0 and args[0].isdigit() and voice_client and self.queue:
            for i in range(0, len(self.queue)):
                if self.queue[i].id == int(args[0]):
                    await ctx.message.channel.send("", embed=EmbeddedFactory.generateAudioRemoveMessage(self.queue[i]))
                    self.queue.pop(i)
                    break;

    @commands.command(name="list", help = "- List all the song's inside the queue.")
    async def list(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and self.queue:
            await ctx.message.channel.send(embed=EmbeddedFactory.generateAudioQueueMessage(self.queue))
        else:
            await ctx.message.channel.send(embed=EmbeddedFactory.generateAudioQueueEmptyMessage())

    @commands.command(name="stop", help = "- Stop the current song from playing.")
    async def stop(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            self.queue.clear()
            voice_client.stop()

    @commands.command(name="pause", help = "- Pause the current song from playing.")
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
            jingle = self.getJingle()
            voice_client.play(AudioFactory.getVideoFromSource(jingle), after=lambda ex: asyncio.run_coroutine_threadsafe(self._play(ctx), self.bot.loop))

    def getJingle(self):
        if len(self.shuffledJingles) > 0:
            return self.shuffledJingles.pop(0)
        else:
            self.shuffleJingles()
            return self.shuffledJingles.pop(0)

    def shuffleJingles(self):
        self.shuffledJingles = random.sample(self.jingles, len(self.jingles))

def setup(bot):
    bot.add_cog(VoiceChannelCog(bot))
