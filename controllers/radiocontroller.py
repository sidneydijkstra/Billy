import random

from factories.messagefactory import MessageFactory
from factories.audiofactory import AudioFactory
from factories.filefactory import FileFactory

from clients.billycontroller import BillyController
from strategy.radiostrategy import RadioStrategy
from strategy.sourcestrategy import SourceStrategy

class RadioController: # TODO: jdl error handle
    def __init__(self):
        self.queue = []
        self.JINGLE_PLAY_CHANGE = 0.8

    async def playUrl(self, author, url):
        # get ydl info
        ydlInfo = AudioFactory.getYdlInfoFromUrl(url)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromYdlInfo(ydlInfo)

        # create strategy
        strategy = RadioStrategy(ydlInfo, author, ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy)

    async def playSource(self, author, source):
        # get audio path
        sourcePath = FileFactory.getFilePath(source)

        # check if file exists
        if not sourcePath:
            await MessageFactory.sendStrategyNoSourceMessage(BillyController.getChannel())
        # end if
        else:
            # get ffmpeg audio
            ffmpegAudio = AudioFactory.getAudioFromSource(sourcePath)

            # create strategy
            strategy = SourceStrategy(source, author, ffmpegAudio)
            # do tryPlay
            await self._tryPlay(strategy)
        # end else

    async def playSearch(self, author, search):
        # get ydl info
        ydlInfo = AudioFactory.getYdlInfoFromSearch(search)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromYdlInfo(ydlInfo)

        # create strategy
        strategy = RadioStrategy(ydlInfo, author, ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy)

    def playJingle(self):
        # get random jingle path
        jingle = FileFactory.getRandomJingle()

        # check if file exists
        if jingle == None:
            return

        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromSource(jingle['path'])
        # create strategy
        strategy = SourceStrategy(jingle['name'], "Billy Radio", ffmpegAudio, True)
        self.queue.append(strategy)

    async def say(self, author, value):
        tts = FileFactory.generateTTSFile(value)
        print(tts)
        # get ffmpeg audio
        ffmpegAudio = AudioFactory.getAudioFromSource(tts['path'])

        # create strategy
        strategy = SourceStrategy(tts['name'], "Billy Radio", ffmpegAudio)
        # do tryPlay
        await self._tryPlay(strategy, True)

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

    async def _tryPlay(self, strategy, skipJingle = False):
        # check if random lower than jingle change
        if not skipJingle and random.random() < self.JINGLE_PLAY_CHANGE:
            # play jingle
            self.playJingle()
            print("added jingle")
        # end if

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

        # clear temp folder
        FileFactory.clearTempFolder()

        # debug print
        print("_callbackPlay()")