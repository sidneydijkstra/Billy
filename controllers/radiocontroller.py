
from factories.messagefactory import MessageFactory
from factories.audiofactory import AudioFactory

from clients.billycontroller import BillyController
from strategy.radiostrategy import RadioStrategy
from strategy.sourcestrategy import SourceStrategy

class RadioController: # TODO: jdl error handle
    def __init__(self):
        self.queue = []

    async def playUrl(self, channel, author, url):
        # get ydl info
        ydlInfo = AudioFactory.getYdlInfoFromUrl(url)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromYdlInfo(ydlInfo)

        # create strategy
        strategy = RadioStrategy(ydlInfo, author, ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy)

    async def playSource(self, channel, author, source):
        # get audio path
        sourcePath = "./audio/%s" % (source)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromSource(sourcePath)

        # create strategy
        strategy = SourceStrategy(source, author, ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy)

    async def playSearch(self, channel, author, search):
        # get ydl info
        ydlInfo = AudioFactory.getYdlInfoFromSearch(search)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromYdlInfo(ydlInfo)

        # create strategy
        strategy = RadioStrategy(ydlInfo, author, ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy)

    async def remove(self, id):
        # get bot voice controller
        voiceClient = BillyController.getVoice()
        # check if voiceClient is active, is playing and queue is not empty
        if voiceClient and voiceClient.is_playing() and len(self.queue) > 0:
            for i in range(0, len(self.queue)):
                if self.queue[i].id == id:
                    await MessageFactory.sendStrategyRemoveMessage(BillyController.getChannel(), self.queue[i])
                    self.queue.pop(i)
                    break

    async def stop(self):
        # get bot voice controller
        voiceClient = BillyController.getVoice()
        # check if voiceClient is active, is playing and queue is not empty
        if voiceClient and voiceClient.is_playing():
            # clear queue
            self.queue.clear()
            # send stop message
            await MessageFactory.sendStrategyStopMessage(BillyController.getChannel())
            # stop voice client
            voiceClient.stop()
        # end if

    async def skip(self):
        # get bot voice controller
        voiceClient = BillyController.getVoice()
        # check if voiceClient is active and playing
        if voiceClient and voiceClient.is_playing():
            # check if queue is empty
            if len(self.queue) <= 0:
                # send noskip message
                await MessageFactory.sendStrategyNoSkipMessage(BillyController.getChannel())
            # end if

            # stop voice client
            voiceClient.stop()
        # end if

        # check if voiceClient is active and not playing
        elif voiceClient and not voiceClient.is_playing():
            # send noskip message
            await MessageFactory.sendStrategyNoSkipMessage(BillyController.getChannel())
        # end elif

    async def list(self):
        # send queue message
        await MessageFactory.sendStrategyQueueMessage(BillyController.getChannel(), self.queue)

    async def _tryPlay(self, strategy):
        # add new strategy to queue
        self.queue.append(strategy)

        # get bot voice controller
        voiceClient = BillyController.getVoice()
        # check if voiceClient is active and not playing
        if voiceClient and not voiceClient.is_playing():
            # send play message
            await MessageFactory.sendStrategyPlayMessage(BillyController.getChannel(), strategy)

            # get strategy
            strategy = self.queue.pop(0)
            # play strategy and set _callbackPlay() as callback function
            strategy.execute(BillyController.getBot(), voiceClient, self._callbackPlay)
        # end if

        # check if voiceClient is active and playing
        elif voiceClient and voiceClient.is_playing():
            # send add message
            await MessageFactory.sendStrategyAddMessage(BillyController.getChannel(), strategy)
        # end elif

        # debug print
        print("_tryPlay()")


    async def _callbackPlay(self): # todo
        # get bot voice controller
        voiceClient = BillyController.getVoice()
        # check if voiceClient is active, not playing and queue not empty
        if voiceClient and not voiceClient.is_playing() and self.queue:
            # get strategy
            strategy = self.queue.pop(0)
            # send play message
            await MessageFactory.sendStrategyPlayMessage(BillyController.getChannel(), strategy)
            # play strategy and set _callbackPlay() as callback function
            strategy.execute(BillyController.getBot(), voiceClient, self._callbackPlay)
        # end if

        # debug print
        print("_callbackPlay()")
