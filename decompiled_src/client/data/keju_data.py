#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/keju_data.o
data = {1: {'duration': 'Воскресенье, 9:00 - 18:00',
     'intervalTime': 1,
     'npcList': (34271, 34272, 34273, 34274, 34275, 34276, 34277, 34278, 34279, 34280),
     'puzzleRate': (6, 6, 6, 6, 6, 6, 6, 6, 6, 6),
     'text': 'Ответьте на вопросы десяти академиков клуба, чтобы получить приглашение на финал игры.',
     'tips': 'У вас есть две попытки. Засчитывается лучшая.',
     'title': 'Клуб знатоков: большая игра'},
 2: {'duration': 'Воскресенье, 18:10 - 18:30',
     'intervalTime': 1,
     'npcList': (34281,),
     'puzzleRate': (20,),
     'text': 'Ответьте на вопросы финальной игры. Три лучших знатока получат почетные титулы!',
     'tips': 'Финальная игра состоит из одного раунда вопросов.',
     'title': 'Клуб знатоков: финал'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
