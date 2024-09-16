#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/guild_scale_data.o
data = {1: {'name': 'Эра Основания',
     'prosperity': 0},
 2: {'costItems': ((430031, 150), (430033, 25)),
     'name': 'Эра Стабильности',
     'prosperity': 5500},
 3: {'costItems': ((430031, 1400), (430033, 350)),
     'name': 'Эра Прогресса',
     'prosperity': 27000},
 4: {'costItems': ((430031, 10000), (430033, 4000), (430035, 700)),
     'name': 'Эра Изобилия',
     'prosperity': 67000},
 5: {'costItems': ((430031, 45000),
                   (430033, 15000),
                   (430035, 4500),
                   (430037, 1000)),
     'name': 'Эра Величия',
     'prosperity': 135000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
