#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/clan_war_tip_data.o
data = {1: {'musicId': (814, 546),
     'name': 'Осада началась!'},
 2: {'musicId': (815, 547),
     'name': 'Осада закончилась!'},
 3: {'musicId': (548,),
     'name': '%s переходит под контроль гильдии \"%s\"!'},
 4: {'musicId': (816,),
     'name': 'Ворота разрушены!'},
 5: {'musicId': (817,),
     'name': 'Строительство ворот завершено!'},
 8: {'musicId': (818,),
     'name': 'Территория освобождена!'},
 9: {'musicId': (819,),
     'name': 'Территория захвачена!'},
 10: {'musicId': (820,),
      'name': 'Строительство ловца душ завершено!'},
 11: {'musicId': (821,),
      'name': 'Строительство зенитной башни завершено!'},
 12: {'musicId': (548,),
      'name': '%s: активирован знак власти!'},
 14: {'musicId': (3441,),
      'name': 'Вы обороняетесь!'},
 15: {'musicId': (3440,),
      'name': 'Вы атакуете!'},
 16: {'musicId': (3439,),
      'name': 'Расстановка сил скоро изменится.'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')