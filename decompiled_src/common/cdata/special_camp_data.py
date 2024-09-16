#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/special_camp_data.o
data = {2001: {'campName': 'Лагерь игрока 1',
        'enemy': (2002,),
        'friendly': (1000, 2000)},
 2002: {'campName': 'Лагерь игрока 2',
        'enemy': (2001,),
        'friendly': (1000, 2000)}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
