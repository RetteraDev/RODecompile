#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/home_wealth_value_data.o
data = {1: {'maxVal': 100,
     'name': 'Lv1'},
 2: {'maxVal': 400,
     'name': 'Lv2'},
 3: {'maxVal': 900,
     'name': 'Lv3'},
 4: {'maxVal': 1600,
     'name': 'Lv4'},
 5: {'maxVal': 2500,
     'name': 'Lv5'},
 6: {'maxVal': 3600,
     'name': 'Lv6'},
 7: {'maxVal': 4900,
     'name': 'Lv7'},
 8: {'maxVal': 6400,
     'name': 'Lv8'},
 9: {'maxVal': 9999999,
     'name': 'Lv9'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
