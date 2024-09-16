#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/business_lv_config_data.o
data = {1: {'bindCashRewardRate': 0.1,
     'baseFame': 4000,
     'maxFame': 15000},
 2: {'bindCashRewardRate': 0.1,
     'baseFame': 5000,
     'maxFame': 18000},
 3: {'bindCashRewardRate': 0.1,
     'baseFame': 6000,
     'maxFame': 21000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
