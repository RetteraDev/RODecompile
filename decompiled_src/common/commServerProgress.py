#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commServerProgress.o
import const
import utils
from data import server_progress_data as SPD

def getMaxDuration(msId, serverProgresses):
    data = SPD.data.get(msId, {})
    maxDurationPrevId, maxDuration = data.get('maxDurationPrevId'), data.get('maxDuration', 0)
    if maxDurationPrevId and serverProgresses.has_key(maxDurationPrevId):
        maxDurationPrev = SPD.data.get(maxDurationPrevId, {}).get('maxDuration', 0)
        if maxDurationPrev and maxDurationPrev < maxDuration:
            tWhen = serverProgresses.get(maxDurationPrevId)
            return (utils.getDaySecond(sec=tWhen) - utils.getDaySecond(sec=utils.getServerOpenTime())) / const.TIME_INTERVAL_DAY + (maxDuration - maxDurationPrev)
    else:
        return maxDuration
