#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/equip_enhance_probability_data.o
data = {240000: {'prob4': 0.17,
          'prob3': 0.25,
          'prob2': 0.34,
          'prob1': 0.5,
          'type': 1},
 240001: {'type': 1,
          'prob8': 0.17,
          'prob7': 0.25,
          'prob6': 0.34,
          'prob5': 0.5},
 240002: {'prob9': 0.5,
          'type': 1,
          'prob11': 0.25,
          'prob10': 0.34,
          'prob12': 0.17},
 240003: {'prob17': 0.02,
          'prob18': 0.02,
          'type': 2},
 240004: {'prob17': 0.02,
          'prob19': 0.02,
          'prob18': 0.02,
          'prob20': 0.02,
          'type': 2},
 240005: {'prob17': 0.05,
          'prob19': 0.05,
          'prob18': 0.05,
          'prob20': 0.05,
          'type': 2},
 240006: {'prob15': 0.25,
          'prob14': 0.34,
          'prob16': 0.17,
          'type': 1,
          'prob13': 0.5},
 240007: {'prob17': 0.5,
          'prob19': 0.25,
          'prob18': 0.34,
          'prob20': 0.17,
          'type': 1}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')