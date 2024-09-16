#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/interactive_emote_data.o
data = {1: {'name': 'Хихиканье',
     'res': '1005'},
 2: {'name': 'Удивление',
     'res': '1006'},
 3: {'name': 'Cердце разбито',
     'res': '1007'},
 4: {'name': 'Головокружение',
     'res': '1001'},
 5: {'name': 'Звездочки',
     'res': '1001'},
 6: {'name': 'Злюсь',
     'res': '1002'},
 7: {'name': 'Волнение',
     'res': '1003'},
 8: {'name': 'Нет слов',
     'res': '1004'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
