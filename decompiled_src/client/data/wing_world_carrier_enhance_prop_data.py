#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wing_world_carrier_enhance_prop_data.o
data = {1: {'name': 'Прочность',
     'tipDesc': 'Здоровье боевого транспорта'},
 2: {'name': 'Маневренность',
     'tipDesc': 'Скорость боевого транспорта'},
 3: {'name': 'Наносимый урон ',
     'tipDesc': 'Сила нанесения урона зданиям от боевого транспорта'},
 4: {'name': 'Смертоносность',
     'tipDesc': 'Сила нанесения урона игрокам от боевого транспорта'},
 5: {'name': 'Разрушительность',
     'tipDesc': 'Сила нанесения боевым транспортом урона другому транспорту'},
 6: {'name': 'Перезарядки',
     'tipDesc': 'Частота атак боевого транспорта'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
