#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/quest_item_group_data.o
data = {1: {'itemList': (361001, 361002, 361003, 361004, 361005, 361011, 361012, 361013, 361014, 361015, 361021, 361022, 361023, 361024, 361025),
     'itemMsg': 'Представленные материалы о жизни: %d / %d',
     'itemTk': 110155892},
 2: {'itemList': (100121, 100221, 100321, 100421, 100521, 100621, 101150, 101250, 101350, 101450, 101550, 101650, 101750),
     'itemMsg': 'Представлено оборудование для испытаний арены: %d / %d',
     'itemTk': 110155892},
 3: {'itemList': (242001, 242002, 242003, 242004),
     'itemMsg': 'Звезды Даоса представили: %d / %d',
     'itemTk': 110155892}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
