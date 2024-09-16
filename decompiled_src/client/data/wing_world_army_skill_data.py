#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wing_world_army_skill_data.o
data = {(9446, 1): {'desc': 'Кипящая ярость'},
 (9447, 1): {'desc': 'Каменный щит'},
 (9448, 1): {'desc': 'Дыхание жизни',
             'notOnZaiju': (6017, 6018, 6019, 6020, 6007, 6008, 6009, 6010, 6011)},
 (9449, 1): {'desc': 'Крыло феникса'},
 (9450, 1): {'desc': 'Голос Империи'},
 (9451, 1): {'desc': 'Голос Калахара'},
 (9452, 1): {'desc': 'Голос Сулана'},
 (9453, 1): {'desc': 'Решающий штурм',
             'limit': (2,)},
 (9454, 1): {'desc': 'Сигнал к атаке',
             'limit': (2,)},
 (9455, 1): {'desc': 'Боевая броня'},
 (9456, 1): {'desc': 'Ритуал спасения',
             'tgtTeam': 1},
 (9458, 1): {'desc': 'Ритуал призыва',
             'limit': (2,),
             'notOnZaiju': 1}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')
