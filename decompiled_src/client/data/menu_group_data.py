#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/menu_group_data.o
data = {10: {'blockId': 40,
      'groupName': 'Обучение',
      'sortId': 360},
 20: {'blockId': 60,
      'groupName': 'Другое',
      'sortId': 450}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
