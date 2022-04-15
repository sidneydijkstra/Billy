import os
import discord
import youtube_dl

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

    def getYdlInfoFromUrl(url):
        ydlInfo = ydl.extract_info(url, download=False)
        return ydlInfo

    def getYdlInfoFromSearch(search):
        ydlInfo = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        return ydlInfo

    def getAudioFromUrl(url):
        ffmpeg = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=url, **ffmpeg_option)
        return ffmpeg

    def getAudioFromYdlInfo(ydlInfo):
        ffmpeg = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=ydlInfo['formats'][0]['url'], **ffmpeg_option)
        return ffmpeg

    def getAudioFromSource(source):
        ffmpeg = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=source)
        return ffmpeg
