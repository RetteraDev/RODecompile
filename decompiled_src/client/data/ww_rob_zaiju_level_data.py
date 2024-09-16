#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/ww_rob_zaiju_level_data.o
data = {1: {'levelBuff': 42358,
     'playerDieNum': 500},
 2: {'levelBuff': 42359,
     'playerDieNum': 1500},
 3: {'levelBuff': 42360,
     'playerDieNum': 3000},
 4: {'levelBuff': 42361,
     'playerDieNum': 5000},
 5: {'levelBuff': 42362,
     'playerDieNum': 1000000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
