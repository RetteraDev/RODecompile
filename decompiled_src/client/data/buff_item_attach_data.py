#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/buff_item_attach_data.o
data = {1: {'subId': (10563,),
     'attachHp': 'HP_back',
     'defaultAction': '1101',
     'modelId': 90566,
     'part': 'back',
     'type': 1},
 2: {'subId': (10563,),
     'attachHp': 'HP_back',
     'defaultAction': '1101',
     'modelId': 90567,
     'part': 'back',
     'type': 1},
 3: {'subId': (10562,),
     'attachHp': 'HP_hand_right_item1',
     'isActionWear': 1,
     'modelId': 90692,
     'equipType': 27,
     'part': 'back',
     'scale': 1.0,
     'type': 1},
 4: {'subId': (10563,),
     'attachHp': 'HP_backplus',
     'modelId': 90503,
     'part': 'back',
     'scale': 2.0,
     'type': 1}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')