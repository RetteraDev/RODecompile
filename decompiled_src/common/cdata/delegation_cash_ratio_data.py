#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/delegation_cash_ratio_data.o
data = {1: {'rate': 0.4,
     'num': 10},
 2: {'rate': 0.1,
     'num': 30},
 3: {'rate': 0.0,
     'num': 100},
 4: {'rate': 0.0,
     'num': 250},
 5: {'rate': 0.0,
     'num': 1000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
