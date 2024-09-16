#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/skill_macro_type_data.o
data = {'Предмет': {'type': 1},
 'Умения': {'type': 0},
 'Умения духов': {'type': 4},
 'Чат': {'type': 3},
 'действие': {'type': 2}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='dict')
