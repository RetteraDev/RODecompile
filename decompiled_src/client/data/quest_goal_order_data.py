#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/quest_goal_order_data.o
data = {1: {'tk': 'markerNpcsTk',
     'name': 'markerNpcs'},
 2: {'tk': 'debateNpcTk',
     'name': 'debateNpc'},
 3: {'tk': 'needDialogTk',
     'name': 'needDialog'},
 4: {'tk': 'comCltItemTk',
     'name': 'compItemCollect'},
 5: {'name': 'questEquip'},
 6: {'tk': 'needMonsterTk',
     'name': 'needMonsters'},
 7: {'tk': 'beatMonsterTk',
     'name': 'beatMonsterNo'},
 8: {'name': 'needConvoy'},
 9: {'name': 'comBuff'},
 10: {'name': 'questVars'},
 11: {'name': 'puzzleId'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
