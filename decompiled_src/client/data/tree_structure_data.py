#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/tree_structure_data.o
data = {1: {'value': {'云垂声望': [453],
               '功绩点': [420],
               '四帝炼境': [401, 415],
               'PVP': [11, 12],
               '剧情点': [514]}},
 2: {'value': {'sulan': [421,
                         424,
                         425,
                         426],
               'yingchuan': [422],
               'yumu': [432, 427, 428],
               'dishi': [423, 429],
               'yunchuidiguo': [431]}},
 3: {'value': {'yunchuidiguo': [433],
               'sulan': [430]}}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
