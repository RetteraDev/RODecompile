#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/intimacy_numeric_data.o
data = {1: {'maxVal': 34999,
     'minVal': 30000,
     'name': 'Взаимное чувство',
     'titleId': 20920},
 2: {'maxVal': 41999,
     'minVal': 35000,
     'name': 'Слияние небес',
     'titleId': 20921},
 3: {'maxVal': 51999,
     'minVal': 42000,
     'name': 'Крылом к крылу',
     'titleId': 20922},
 4: {'maxVal': 69999,
     'minVal': 52000,
     'name': 'Клятва согласия',
     'titleId': 20923},
 5: {'maxVal': 99998,
     'minVal': 70000,
     'name': 'Нерушимый союз',
     'titleId': 20924},
 6: {'maxVal': 131399,
     'minVal': 99999,
     'name': 'Легендарная пара',
     'titleId': 20925},
 7: {'maxVal': 188887,
     'minVal': 131400,
     'name': 'Взаимопомощь',
     'titleId': 20926},
 8: {'maxVal': 288887,
     'minVal': 188888,
     'name': 'Луговой сбор',
     'titleId': 20927},
 9: {'effectTitleId': 31,
     'maxVal': 99999999,
     'minVal': 288888,
     'name': 'Неизменность'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')