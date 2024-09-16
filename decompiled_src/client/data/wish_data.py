#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wish_data.o
data = {1: {'consumeItemCnt': 1,
     'consumeItemId': 442103},
 2: {'consumeItemCnt': 1,
     'consumeItemId': 442103},
 4: {'LUCKY_WISH_TIME': 'Мечты начнут сбываться в 21:00! Успейте загадать желание с 00:00 до 20:30.',
     'consumeItemCnt': 1,
     'consumeItemId': 442104,
     'desc': 'Древо желаний порой претворяет в жизнь самые сокровенные мечты. Быть может, и вам повезёт?'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
