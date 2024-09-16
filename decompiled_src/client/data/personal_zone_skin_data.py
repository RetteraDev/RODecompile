#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/personal_zone_skin_data.o
data = {1: {'desc': 'Используйте, чтобы применить дизайн «Мой угол по умолчанию».',
     'itemId': 442316,
     'name': 'Рамка по умолчанию',
     'validTime': 0},
 2: {'desc': 'Используйте, чтобы применить дизайн Dragonscale Moonlight My Corner.',
     'itemId': 441042,
     'name': 'Рамка \"Звездная ночь\"',
     'validTime': 15552000},
 3: {'desc': 'After use, you can successfully unlock the magic space · Hongyan',
     'itemId': 441041,
     'name': 'Рамка \"Цветение сакуры\"',
     'validTime': 15552000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
