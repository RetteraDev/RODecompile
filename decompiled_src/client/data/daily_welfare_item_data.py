#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/daily_welfare_item_data.o
data = {1: {'bonusProb': 10,
     'itemCount': 1,
     'itemId': 334067,
     'itemIdList': (336731, 336732, 336733, 336734),
     'name': 'Малый мешочек с подарками',
     'nowPrice': 19,
     'sourcePrice': 60},
 2: {'bonusProb': 20,
     'itemCount': 1,
     'itemId': 335074,
     'itemIdList': (336735, 336736, 336737, 336738, 336739),
     'name': 'Средний мешок с подарками',
     'nowPrice': 39,
     'sourcePrice': 100},
 3: {'bonusProb': 30,
     'itemCount': 1,
     'itemId': 335332,
     'itemIdList': (336740, 336741, 336742, 336743),
     'name': 'Большой мешок с подарками',
     'nowPrice': 89,
     'sourcePrice': 220}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
