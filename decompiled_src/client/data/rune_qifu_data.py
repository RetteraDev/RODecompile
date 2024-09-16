#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/rune_qifu_data.o
data = {(1, 1): {'desc': 'Требуются пять кварцевых точильных камней.',
          'lv': 1,
          'opType': 1,
          'qiFuData': [((240000, 5),)]},
 (1, 2): {'desc': 'Требуются пять кварцевых точильных камней и один алмазный.',
          'lv': 1,
          'opType': 2,
          'qiFuData': [((240001, 1), (240000, 5))]},
 (2, 1): {'lv': 2,
          'opType': 1,
          'qiFuData': [((240002, 1),)]},
 (2, 2): {'lv': 2,
          'opType': 2,
          'qiFuData': [((240002, 1),)]}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')
