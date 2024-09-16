#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/life_csm_state_data.o
data = {1: {'name': 'процветающий'},
 2: {'name': 'Обычный'},
 3: {'name': 'Бедные'},
 4: {'name': 'Обновить один'},
 5: {'name': 'Обновить 3'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
