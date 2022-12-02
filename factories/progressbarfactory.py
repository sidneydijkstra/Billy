from datetime import datetime, timedelta

class ProgressBarFactory:

    # generate time string with display bar
    def generateProgressFromTime(fromTime, toTime, barSize = 18, frontChar='█', backChar='░'):
        formatFromTime = datetime.now() - fromTime
        played = str(formatFromTime).split(".")[0]
        total = toTime

        # calculation to get values between 0 and barSize
        fillAmount = round(((toTime.total_seconds() - formatFromTime.total_seconds()) / toTime.total_seconds()) * barSize)
        barAmount = barSize - fillAmount

        return "%s %s%s %s" % (played, ('█'*barAmount), ('░'*fillAmount), total)
