#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/fishing_top_reward_data.o
data = {10004: {'desc1': 'Вы заняли %d-е место и заслужили награду.',
         'desc2': 'В ходе турнира вы набрали %d оч. и заслужили награду.',
         'gameFishIds': (350700, 350701, 350702, 350703, 350704),
         'noticeTime': 900,
         'prizeChat': 'Выберите награду турнира.',
         'questId': 36210,
         'rankBonus': [10113,
                       10114,
                       10115,
                       10116],
         'ranks': [(1, 3),
                   (4, 10),
                   (11, 30),
                   (31, 100)],
         'scoreBonus': [12961, 10119],
         'scores': [(80, 1000), (30, 1000)],
         'title': 'Рыбомания'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
