import asyncio

from strategy.basestrategy import BaseStrategy

class SourceStrategy(BaseStrategy):
    def __init__(self, title, author, ffmpegAudio):
        super().__init__()
        self.title = title
        self.author = author
        self.ffmpegAudio = ffmpegAudio

    def execute(self, bot, voiceClient, callback):
        voiceClient.play(self.ffmpegAudio, after=lambda ex: asyncio.run_coroutine_threadsafe(callback(), bot.loop))

    def getTitle(self):
        return "%s [00:00]" % (self.title)

    def getDescription(self):
        return "Een local nummertje op Billy Radio!"
