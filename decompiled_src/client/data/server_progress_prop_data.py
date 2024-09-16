#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/server_progress_prop_data.o
data = {10001: {'def': 'AVATAR_MAX_LV',
         'name': 'Доступный уровень'},
 10002: {'def': 'NPC_FUNC',
         'name': 'Функция NPC'},
 10003: {'def': 'SHOP_ITEM',
         'name': 'Доступен магазин'},
 10004: {'def': 'EXP_TO_YUANSHEN',
         'name': 'Свиток Цан Цин и передача силы богам'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
