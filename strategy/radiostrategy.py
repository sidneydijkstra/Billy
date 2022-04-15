import asyncio

from strategy.basestrategy import BaseStrategy

class RadioStrategy(BaseStrategy):
    def __init__(self, ydlInfo, author, ffmpegAudio):
        super().__init__()
        self.title = ydlInfo['title']
        self.uploader = ydlInfo['uploader']
        self.duration = self.getDuration(ydlInfo['duration'])
        self.views = int(ydlInfo['view_count'])
        self.url = ydlInfo['formats'][0]['url']
        self.author = author
        self.ffmpegAudio = ffmpegAudio

    def execute(self, bot, voiceClient, callback):
        voiceClient.play(self.ffmpegAudio, after=lambda ex: asyncio.run_coroutine_threadsafe(callback(), bot.loop))

    def getTitle(self):
        return "%s [%s]" % (self.title, self.duration)

    def getDescription(self):
        return "%d Views - By %s - id: %d" % (self.views, self.uploader, self.id)

    def getDuration(self, duration):
        m = round(duration / 60)
        s = round(duration % 60)
        return "%s:%s" % (str(m), str(s) if s > 9 else "0" + str(s))

    def toString(self):
        return ("[%d] request from: %s -> %s by %s : [%s] - %d views" % (self.id, self.author, self.title, self.uploader, self.duration, self.views))
