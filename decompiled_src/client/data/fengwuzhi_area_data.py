#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/fengwuzhi_area_data.o
data = {1: {'mapType': 0,
     'name': 'Зачарованный край'},
 2: {'mapType': 0,
     'name': 'Калахарские земли'},
 3: {'mapType': 0,
     'name': 'Пепельная пустыня'},
 4: {'mapType': 0,
     'name': 'Окрестности Астериона',
     'overviewIdList': (18, 19, 20, 21, 22, 23, 24, 27, 25, 26),
     'pos': (463, 133)},
 5: {'mapType': 0,
     'name': 'Зеленая жемчужина'},
 6: {'mapType': 0,
     'name': 'Курган мечей'},
 7: {'mapType': 0,
     'name': 'Вековые леса',
     'overviewIdList': (13, 14, 15, 16, 17),
     'pos': (623, 13)},
 8: {'mapType': 0,
     'name': 'Озёрный дол',
     'overviewIdList': (7, 8, 9, 10, 11, 12),
     'pos': (723, 181)},
 9: {'mapType': 0,
     'name': 'Суланские земли'},
 10: {'mapType': 0,
      'name': 'Окрестности Сулана',
      'overviewIdList': (1, 2, 3, 4),
      'pos': (750, 352)}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')