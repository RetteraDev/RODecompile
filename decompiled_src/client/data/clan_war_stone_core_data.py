#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/clan_war_stone_core_data.o
data = {501000: {'name': 'Малый знак воителя'},
 501001: {'name': 'Малый знак защитника'},
 501002: {'name': 'Малый знак чародея'},
 501003: {'name': 'Малый знак экзорциста'},
 501004: {'name': 'Малый знак палача'},
 501005: {'name': 'Знак тюремщика'},
 501100: {'name': 'Средний знак чародея'},
 501101: {'name': 'Средний знак экзорциста'},
 501102: {'name': 'Средний знак воителя'},
 501103: {'name': 'Средний знак защитника'},
 501104: {'name': 'Средний знак палача'},
 501200: {'excludeFortId': (13, 32),
          'name': 'Знак ловчего'},
 501201: {'name': 'Средний знак гвардейца'},
 501202: {'name': 'Средний знак убийцы'},
 501203: {'name': 'Малый знак гвардейца'},
 501204: {'name': 'Малый знак убийцы'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
