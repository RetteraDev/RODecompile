#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/hunt_ghost_area_data.o
data = {1: {'name': 'Кноттль',
     'posLeftUp': (-500, 0, 2000),
     'posRightDown': (-100, 0, 1400)},
 2: {'name': 'Туманные топи',
     'posLeftUp': (5600, 0, 900),
     'posRightDown': (6000, 0, 500)},
 3: {'name': 'Западные степи',
     'posLeftUp': (300, 0, -100),
     'posRightDown': (700, 0, -500)},
 4: {'name': 'Гиблый каньон',
     'posLeftUp': (-2200, 0, -200),
     'posRightDown': (-1800, 0, -600)}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
