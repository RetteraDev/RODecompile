#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/hand_in_item_crystal_data.o
data = {1: {'bonus': 20043,
     'name': '1 день',
     'round': 6,
     'startTime': '2020.1.30.8.0.0'},
 2: {'bonus': 20044,
     'name': 'День 2',
     'round': 8,
     'startTime': '2020.1.31.8.0.0'},
 3: {'bonus': 20045,
     'name': '3 день',
     'round': 16,
     'startTime': '2020.2.1.8.0.0'},
 4: {'bonus': 20046,
     'name': '5 день',
     'round': 16,
     'startTime': '2020.2.3.8.0.0'},
 5: {'bonus': 20047,
     'name': '7 день',
     'round': 8,
     'startTime': '2020.2.5.8.0.0'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
