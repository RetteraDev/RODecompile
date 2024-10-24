#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/ns_guild_prestige_act_data.o
data = {1: {'enableTime1': ('week', 1, 5),
     'enableTime2': ('week', 6, 4),
     'enableTime3': ('week', 10, 4),
     'fromMergeTime': 0,
     'prestigeMultiple2': {126: 1.5},
     'prestigeMultiple3': {128: 1.5},
     'rankBonus1': {(1, 1): 1000,
                    (2, 2): 1001,
                    (3, 3): 1002,
                    (4, 10): 1003},
     'rankBonus2': {(1, 1): 1004,
                    (2, 2): 1005,
                    (3, 3): 1006,
                    (4, 10): 1007},
     'rankBonus3': {(1, 1): 1008,
                    (2, 2): 1009,
                    (3, 3): 1010,
                    (4, 10): 1011},
     'rankTitle1': 'Ten Guilds · Megatron',
     'rankTitle2': 'Десять лучших гильдий: сигнальные костры',
     'rankTitle3': 'Десять лучших гильдий: горные дуэли'},
 2: {'enableTime1': ('week', 2, 6),
     'fromMergeTime': 1,
     'rankBonus1': {(1, 1): 1012,
                    (2, 2): 1013,
                    (3, 3): 1014,
                    (4, 10): 1015},
     'rankTitle1': 'Ten Guilds · Megatron'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
