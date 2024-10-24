#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/map_filter_config.o
data = {1: {'desc': 'Осадные орудия',
     'level1': '0',
     'level2': '0',
     'level3': '1',
     'level4': '1',
     'list': [['Бастионы', 'Map_ZuLong'], ["Башни \'Око\'", 'Map_AirTower'], ['Ловцы душ', 'Map_GuildTransDis']],
     'name': 'clanwar'},
 2: {'desc': 'Ключевые NPC',
     'level1': '0',
     'level2': '0',
     'level3': '1',
     'level4': '1',
     'list': [['Хозяйки склада', 'mapStorage'],
              ['Аукционисты', 'mapConsign'],
              ['Проводники', 'maptrans'],
              ['Почта', 'mapMail'],
              ['Искатели приключений', 'mapAdventure'],
              ['Орден убийц', 'mapdeadOrAlive'],
              ['Работа', 'mapWorkBoard'],
              ['Подарки', 'mapbonus'],
              ['Оружейницы', 'mapenhance'],
              ['Местные жители', 'mapcommon'],
              ['Летописцы', 'mapyunchuiji'],
              ['Поставщики', 'mapSpecialtyBussiness'],
              ['Дружба и свадьбы', 'mapintimacy'],
              ['Смена класса', 'mapzhuanzhi']],
     'name': 'functionNpc'},
 3: {'desc': 'Торговцы',
     'level1': '0',
     'level2': '0',
     'level3': '0',
     'level4': '1',
     'list': [['Торговцы', 'mapshop'], ['Особые товары', 'mapAdvanceShop']],
     'name': 'functionNpc'},
 4: {'desc': 'Участники группы',
     'level1': '0',
     'level2': '0',
     'level3': '1',
     'level4': '1',
     'list': [],
     'name': 'member'},
 5: {'desc': 'Побочные задания',
     'isHideHoverDetail': 1,
     'level1': '0',
     'level2': '1',
     'level3': '1',
     'level4': '1',
     'list': [['Практические', 'mapavailable3'], ['Сюжетные', 'mapunfinished3'], ['Обучающие', 'mapcomplete3']],
     'name': 'mapcomplete'},
 6: {'desc': 'Обучающие',
     'isHideHoverDetail': 1,
     'level1': '0',
     'level2': '0',
     'level3': '1',
     'level4': '1',
     'list': [['Обучающие', 'mapavailable4'], ['Обучающие', 'mapunfinished4'], ['Обучающие', 'mapcomplete4']],
     'name': 'mapcomplete'},
 7: {'desc': 'Задания оплота',
     'level1': '1',
     'level2': '1',
     'level3': '1',
     'level4': '1',
     'list': [['Испытание', 'mapavailable17'],
              ['- выполняется', 'mapunfinished17'],
              ['- выполнено', 'mapcomplete17'],
              ['Задание оплота', 'mapavailable18'],
              ['- выполняется', 'mapunfinished18'],
              ['- выполнено', 'mapcomplete18']],
     'name': 'mapDiGongPort'},
 8: {'desc': 'Охотничьи угодья',
     'icon': 'mapDiGongPort',
     'level1': '1',
     'level2': '1',
     'level3': '1',
     'level4': '1',
     'list': [['Охотничьи угодья', 'mapDiGongPort']],
     'name': 'mapDiGongPort'},
 9: {'desc': 'Инстансы',
     'icon': 'mapFubenPort',
     'level1': '1',
     'level2': '1',
     'level3': '1',
     'level4': '1',
     'list': [['Инстансы', 'mapFubenPort']],
     'name': 'mapFubenPort'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
