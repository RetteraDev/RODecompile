#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/guild_run_man_data.o
data = {1: {'lv': 50,
     'maxRewardPassNum': 20,
     'name': 'Гильдейский забег'},
 2: {'lv': 50,
     'maxRewardPassNum': 20,
     'name': 'Еженедельный гильдейский забег'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
