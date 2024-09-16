#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/arena_level_data.o
data = {1: {'maxLv': 59,
     'minLv': 1,
     'weeklyAwardName': 'weeklyAward1_59'},
 2: {'maxLv': 69,
     'minLv': 60,
     'weeklyAwardName': 'weeklyAward60_69'},
 3: {'maxLv': 89,
     'minLv': 70,
     'weeklyAwardName': 'weeklyAward70_89'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
