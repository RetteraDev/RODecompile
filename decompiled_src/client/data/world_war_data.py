#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/world_war_data.o
data = {1: {'desc': 'Третья лига',
     'maxmp': 5000,
     'name': 'Третья лига'},
 2: {'desc': 'Вторая лига',
     'maxmp': 5000,
     'name': 'Вторая лига'},
 3: {'desc': 'Первая лига',
     'maxmp': 5000,
     'name': 'Первая лига'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
