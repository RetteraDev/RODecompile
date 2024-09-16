#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/npc_yabiao_data.o
data = {48066: {'desc': 'Дротик',
         'type': 0},
 48067: {'desc': 'Доклад 1',
         'type': 1},
 48068: {'desc': 'Доклад 2',
         'type': 1},
 48069: {'desc': 'Доклад 3',
         'type': 1},
 48070: {'desc': 'Выполнить',
         'type': 2},
 48094: {'desc': 'Обновить',
         'type': 3}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
