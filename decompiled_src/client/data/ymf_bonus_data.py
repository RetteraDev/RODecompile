#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/ymf_bonus_data.o
data = {101: {'bonusId': 11454,
       'desc': '50 очков являются минимумом для получения награды. Вам достанутся очки опыта и немного боеприпасов.',
       'score': 50,
       'title': '50 оч.'},
 102: {'bonusId': 11453,
       'desc': '100 очков позволяют претендовать на улучшенную награду. Есть шанс получить ценные боеприпасы и Главы книг ярости.',
       'score': 100,
       'title': '100 оч.'},
 103: {'bonusId': 11452,
       'desc': 'Тому, кто заработает 200 очков, обещаны лучшие сокровища Вершины вечных снегов.',
       'score': 200,
       'title': '200 оч.'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
