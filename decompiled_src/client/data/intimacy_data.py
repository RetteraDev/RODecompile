#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/intimacy_data.o
data = {1: {'maxVal': 200,
     'name': 'Случайный знакомый'},
 2: {'maxVal': 1000,
     'name': 'Близкий знакомый'},
 3: {'maxVal': 3000,
     'name': 'Приятель'},
 4: {'maxVal': 6000,
     'name': 'Товарищ'},
 5: {'maxVal': 10000,
     'name': 'Соратник'},
 6: {'maxVal': 15000,
     'name': 'Единомышленник'},
 7: {'maxVal': 21000,
     'name': 'Близкий друг'},
 8: {'maxVal': 28000,
     'name': 'Лучший друг'},
 9: {'maxVal': 99999999,
     'name': 'Родственная душа'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
