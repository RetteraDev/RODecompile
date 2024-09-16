#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wing_world_data.o
data = {1: {'campMaxmp': 10000,
     'desc': 'Первая лига',
     'maxmp': 5000,
     'name': 'Первая лига',
     'rebalaceMsgId': 51366,
     'rebalanceMode': 10,
     'skillSchemeModeId': 6},
 2: {'campMaxmp': 10000,
     'desc': 'Вторая лига',
     'maxmp': 5000,
     'name': 'Вторая лига',
     'rebalaceMsgId': 51367,
     'rebalanceMode': 7,
     'skillSchemeModeId': 3},
 3: {'campMaxmp': 10000,
     'desc': 'Третья лига',
     'maxmp': 5000,
     'name': 'Третья лига',
     'rebalaceMsgId': 51368,
     'rebalanceMode': 6,
     'skillSchemeModeId': 2}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
