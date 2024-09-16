#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/qiren_pandect_data.o
data = {1: {'groupIdList': (1,),
     'idList': (6, 250),
     'name': 'Герои'},
 2: {'idList': (800, 850, 451, 401),
     'name': 'Чудовища'},
 3: {'idList': (450, 400, 500, 501),
     'name': 'Тайны'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
