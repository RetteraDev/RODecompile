#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/couple_emote_basic_data.o
data = {1: {'name': 'взять на руки',
     'showFKey': 1},
 2: {'friendnessLimit': 4,
     'name': 'поднять на руки',
     'needFlag': 1},
 10004: {'lockDC': 1,
         'name': 'погладить по голове',
         'needFlag': 1,
         'noAttachModel': 1},
 10005: {'lockDC': 1,
         'name': 'обнять',
         'needFlag': 1,
         'noAttachModel': 1},
 10006: {'lockDC': 1,
         'name': 'обнять',
         'needFlag': 1,
         'noAttachModel': 1},
 10007: {'lockDC': 1,
         'name': 'удивить',
         'needFlag': 1,
         'noAttachModel': 1}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
