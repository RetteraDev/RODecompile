#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/collect_item_pos2item_data.o
data = {1: {'name': 'Алчность',
     'originItem': 331469,
     'pathNpc': (110155853, 110159651),
     'replaceItems': [331477]},
 2: {'name': 'Сказка о тролле',
     'originItem': 331471,
     'pathNpc': (110155853, 110159651),
     'replaceItems': [331477]},
 3: {'name': 'Инту и Айна',
     'originItem': 331472,
     'pathNpc': (110155853, 110159651),
     'replaceItems': [331477]},
 4: {'name': 'Кольца Власти',
     'originItem': 331473,
     'pathNpc': (110155844, 110159652),
     'replaceItems': [331477]},
 5: {'name': 'Сказки для гурмана',
     'originItem': 331475,
     'pathNpc': (110155844, 110159652),
     'replaceItems': [331477]},
 6: {'name': 'Король Суходрев',
     'originItem': 331476,
     'pathNpc': (110155844, 110159652),
     'replaceItems': [331477]}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')