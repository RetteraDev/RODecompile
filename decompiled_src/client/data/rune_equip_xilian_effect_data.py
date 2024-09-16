#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/rune_equip_xilian_effect_data.o
data = {1: {'activateCondition': [(0, 3)],
     'effects': [[1, 1001, 9], [2, 1, 1]],
     'icon': 'blue',
     'name': 'Небесные светила'},
 2: {'activateCondition': [(4, 3)],
     'effects': [[1, 1002, 9], [2, 4, 1]],
     'icon': 'gold',
     'name': 'Грозовые ливни'},
 3: {'activateCondition': [(3, 3)],
     'effects': [[1, 1003, 9], [2, 3, 1]],
     'icon': 'red',
     'name': 'Небесный огонь'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
