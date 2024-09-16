#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/sheng_si_chang_data.o
data = {5000: {'lv': ((40, 49), (50, 59), (60, 60)),
        'readyTime': 30,
        'enterTime': 45,
        'applyStartTimes': ('0 0 * * 5',),
        'roundNum': 4,
        'sideNum': 10,
        'sscLv': 80,
        'quitTime': 15,
        'applyEndTimes': ('55 14 * * 5',),
        'activityStartTimes': ('00 15 * * 5',)},
 5005: {'lv': ((40, 49), (50, 59), (60, 60)),
        'readyTime': 30,
        'enterTime': 45,
        'applyStartTimes': ('0 0 * * 5',),
        'roundNum': 4,
        'sideNum': 6,
        'sscLv': 80,
        'quitTime': 15,
        'nextRoundPrepareTime': 30,
        'applyEndTimes': ('55 14 * * 5',),
        'activityStartTimes': ('00 15 * * 5',)}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
