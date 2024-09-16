#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/mini_game_data.o
data = {1: {'consumeItemId': 369954,
     'consumeItemNum': 0,
     'desc': 'Вы и еще 7 человек можете сесть за этот стол и поделиться своими героическими историями вместе в гармонии.',
     'descTitle': 'Групповая таблица',
     'miniGamePublic': 0,
     'miniGameType': 1,
     'name': 'Групповая таблица'},
 2: {'consumeItemId': 369954,
     'consumeItemNum': 0,
     'desc': 'Вы и еще 7 человек можете сесть за этот стол и поделиться своими героическими историями вместе в гармонии.',
     'descTitle': 'Угадай рисунок',
     'miniGamePublic': 1,
     'miniGameType': 1,
     'name': 'Угадай рисунок'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
