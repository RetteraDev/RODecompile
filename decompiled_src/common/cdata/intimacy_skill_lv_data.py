#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/intimacy_skill_lv_data.o
data = {1: {'intimacyTgtLv': 4,
     'name': 'Товарищ'},
 2: {'intimacyTgtLv': 5,
     'name': 'Соратник'},
 3: {'intimacyTgtLv': 6,
     'name': 'Единомышленник'},
 4: {'intimacyTgtLv': 7,
     'name': 'Близкий друг'},
 5: {'intimacyTgtLv': 8,
     'name': 'Лучший друг'},
 6: {'intimacyTgtLv': 9,
     'name': 'Родственная душа'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
