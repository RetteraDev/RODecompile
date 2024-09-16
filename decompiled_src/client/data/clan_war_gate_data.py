#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/clan_war_gate_data.o
data = {502000: {'charType': 15210,
          'name': 'Декоративные ворота'},
 502001: {'charType': 15211,
          'name': 'Обычные ворота'},
 502002: {'charType': 15212,
          'name': 'Прочные ворота'},
 502003: {'charType': 15213,
          'name': 'Укрепленные ворота'},
 502004: {'charType': 15214,
          'name': 'Надежные ворота'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
