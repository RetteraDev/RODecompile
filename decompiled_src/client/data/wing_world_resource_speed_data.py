#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wing_world_resource_speed_data.o
data = {0: {'collectCoef': {(1, 5000): 1,
                     (10001, 999999999): 0,
                     (5001, 10000): 0.5},
     'collectMax': 100000,
     'name': 'Обсидиановая руда',
     'speedFormulaId': 90181},
 1: {'collectCoef': {(1, 5000): 1,
                     (10001, 999999999): 0,
                     (5001, 10000): 0.5},
     'collectMax': 100000,
     'name': 'Топленая древесина',
     'speedFormulaId': 90182},
 2: {'collectCoef': {(1, 5000): 1,
                     (10001, 999999999): 0,
                     (5001, 10000): 0.5},
     'collectMax': 100000,
     'name': 'Небесная вода',
     'speedFormulaId': 90183}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
