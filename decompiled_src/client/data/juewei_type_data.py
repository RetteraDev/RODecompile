#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/juewei_type_data.o
data = {1: {'consumeItem': 440828,
     'name': 'Рядовой',
     'needJunJieLv': 4,
     'needLv': 3},
 2: {'consumeItem': 440829,
     'name': 'Сержант',
     'needJunJieLv': 7,
     'needLv': 6},
 3: {'consumeItem': 440830,
     'name': 'Лейтенант',
     'needJunJieLv': 10,
     'needLv': 9},
 4: {'consumeItem': 440831,
     'name': 'Капитан',
     'needJunJieLv': 10,
     'needLv': 12},
 5: {'name': 'Полковник'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
