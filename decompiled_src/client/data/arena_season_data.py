#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/arena_season_data.o
data = {1: {'SessionName': 'Сезон 1',
     'SessionTimeText': '(1.1--3.31)'},
 2: {'SessionName': 'Сезон 2',
     'SessionTimeText': '(4.1--6.30)'},
 3: {'SessionName': 'Сезон 3',
     'SessionTimeText': '(7.1--9.30)'},
 4: {'SessionName': 'Сезон 4',
     'SessionTimeText': '(10.1--12.31)'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
