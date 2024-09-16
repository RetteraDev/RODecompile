#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/vp_stage_data.o
data = {0: {'expParam': 1.0,
     'transformRatio': 0.0,
     'vpStageName': 'Нулевая концентрация'},
 1: {'expParam': 2.0,
     'transformRatio': 1.0,
     'vpStageName': 'Обычная концентрация'},
 2: {'expParam': 3.0,
     'transformRatio': 1.0,
     'vpStageName': 'Повышенная концентрация'},
 3: {'expParam': 5.0,
     'transformRatio': 1.0,
     'vpStageName': 'Сильная концентрация'},
 4: {'expParam': 5.0,
     'transformRatio': 1.0,
     'vpStageName': 'Ясно с первого взгляда'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
