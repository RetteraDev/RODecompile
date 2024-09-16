#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/upgrade_manual_equip.o
data = {(120706, 0): {'needLv': 79,
               'needCash': (90402, 19500, 20000),
               'needItemB': (240024, (90401, 195, 120)),
               'id': 1,
               'needItemA': (240046, (90400, 15, 25)),
               'extraNeedEquip': (120706, 2, 1),
               'targetEquip': 120707},
 (120706, 1): {'needLv': 79,
               'needCash': (90402, 19500, 20000),
               'needItemB': (240024, (90401, 195, 120)),
               'id': 2,
               'needItemA': (240046, (90400, 15, 25)),
               'extraNeedEquip': (120706, 1, 2),
               'targetEquip': 120707}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')
