#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/delegation_exp_ratio_data.o
data = {1: {'rate': 0.5,
     'num': 20},
 2: {'rate': 0.25,
     'num': 40},
 3: {'rate': 0.1,
     'num': 80},
 4: {'rate': 0.0,
     'num': 120},
 5: {'rate': 0.0,
     'num': 1000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
