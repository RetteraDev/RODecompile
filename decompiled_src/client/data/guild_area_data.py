#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/guild_area_data.o
data = {1: {'ext': 0,
     'level': 1,
     'name': 'Акрополь',
     'open': 1},
 2: {'ext': 2000,
     'fog': (49, 50, 51, 52),
     'fogPos': (1184, 602),
     'level': 2,
     'name': 'Зеленая заводь',
     'open': 1,
     'picId': 1},
 3: {'ext': 0,
     'level': 1,
     'name': 'Дикие земли',
     'open': 1},
 4: {'ext': 2000,
     'fog': (56, 57, 58),
     'fogPos': (1200, 213),
     'level': 1,
     'name': 'Туманные скалы',
     'open': 1,
     'picId': 3},
 5: {'ext': 4000,
     'fog': (59, 60),
     'fogPos': (428, 52),
     'level': 2,
     'name': 'Побережье',
     'open': 1,
     'picId': 4}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')