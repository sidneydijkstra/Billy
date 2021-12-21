
class AudioInfo():

    def __init__(self, ydlInfo, auther, ffmpegAudio):
        if ydlInfo:
            self.title = ydlInfo['title']
            self.uploader = ydlInfo['uploader']
            self.duration = self.getDuration(ydlInfo['duration'])
            self.views = int(ydlInfo['view_count'])
            self.url = ydlInfo['formats'][0]['url']
            self.auther = auther
            self.ffmpegAudio = ffmpegAudio

    def getDuration(self, duration):
        m = round(duration / 60)
        s = round(duration % 60)
        return "%s:%s" % (str(m), str(s) if s > 9 else "0" + str(s))

    def toString(self):
        return ("requerst from: %s -> %s by %s : [%s] - %d views" % (self.auther, self.title, self.uploader, self.duration, self.views))
