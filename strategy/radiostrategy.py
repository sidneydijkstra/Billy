import asyncio

from strategy.basestrategy import BaseStrategy
from managers.csvmanager import CSVManager

class RadioStrategy(BaseStrategy):
    def __init__(self, ydlInfo, author, ffmpegAudio, hidden = False, url = None):
        super().__init__(hidden)
        self.title = ydlInfo['title']
        self.uploader = ydlInfo['uploader']
        self.duration = self.getDuration(ydlInfo['duration'])
        self.views = int(ydlInfo['view_count'])
        self.url = ydlInfo['formats'][0]['url']
        self.author = author
        self.ffmpegAudio = ffmpegAudio

        # add entrie in song history
        CSVManager.addSongHistory(ydlInfo['id'], ydlInfo['title'], "https://www.youtube.com/watch?v={0}".format(ydlInfo['id']) if not url else url)



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
