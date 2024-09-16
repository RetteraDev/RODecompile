#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/world_war_army_skill_data.o
data = {(9390, 1): {'desc': 'Кипящая ярость'},
 (9391, 1): {'desc': 'Каменный щит'},
 (9392, 1): {'desc': 'Дыхание жизни',
             'notOnZaiju': (6017, 6018, 6019, 6020, 6007, 6008, 6009, 6010, 6011)},
 (9393, 1): {'desc': 'Крыло феникса'},
 (9394, 1): {'desc': 'Голос Империи'},
 (9395, 1): {'desc': 'Голос Калахара'},
 (9396, 1): {'desc': 'Голос Сулана'},
 (9397, 1): {'desc': 'Решающий штурм',
             'spaceNo': (11, 19)},
 (9398, 1): {'desc': 'Сигнал к атаке',
             'spaceNo': (11, 19)},
 (9426, 1): {'desc': 'Боевая броня'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')
