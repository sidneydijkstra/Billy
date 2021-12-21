import os
import discord
import youtube_dl

from models.audioinfo import AudioInfo

# get ffmpeg location and set options
ffmpeg_location = os.getenv("FFMPEG_LOCATION")
ffmpeg_option = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# load youtube dl
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'prefer_ffmpeg': True
}
ydl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

class AudioFactory:

    async def joinChannel(bot, user):
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=user.guild)
        if user.voice and not voice_client or user.voice and not voice_client.channel == user.voice.channel:
            if voice_client:
                await voice_client.disconnect()

            await user.voice.channel.connect()

    async def leaveChannel(client, user):
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=user.guild)
        if voice_client:
            await voice_client.disconnect()


    def getVideoFromUrl(url, auther):
        ydlInfo = ydl.extract_info(url, download=False)
        url = ydlInfo['formats'][0]['url']
        ffmpegAudio = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=url, **ffmpeg_option)


        audioInfo = AudioInfo(ydlInfo, auther, ffmpegAudio)
        return audioInfo

    def getVideoFromSearch(search, auther):
        ydlInfo = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        url = ydlInfo['formats'][0]['url']
        ffmpegAudio = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=url, **ffmpeg_option)

        audioInfo = AudioInfo(ydlInfo, auther, ffmpegAudio)
        return audioInfo

    def getVideoFromSource(source):
        return discord.FFmpegPCMAudio(executable=ffmpeg_location, source=source)
