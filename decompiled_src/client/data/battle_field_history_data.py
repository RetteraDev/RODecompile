#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/battle_field_history_data.o
data = {1: {'key': 'joinCnt',
     'name': 'Битвы',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 2: {'key': 'winCnt',
     'name': 'Победы',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 3: {'key': 'loseCnt',
     'name': 'Поражения',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 4: {'divide': ('winCnt', 'joinCnt'),
     'isAverage': 1,
     'isPercentForm': 1,
     'key': 'averWinCnt',
     'name': 'Доля побед',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 5: {'key': 'jibaiCnt',
     'name': 'У/П',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 6: {'key': 'damage',
     'name': 'Нанесенный урон',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 7: {'key': 'cureTotal',
     'name': 'Лечение',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 8: {'key': 'beDamageTotal',
     'name': 'Полученный урон',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 9: {'key': 'donateScore',
     'name': 'Вклад',
     'type': [0,
              1,
              2,
              3,
              8,
              9]},
 10: {'key': 'dieCnt',
      'name': 'Смерти',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 11: {'divide': ('jibaiCnt', 'joinCnt'),
      'isAverage': 1,
      'key': 'averJibai',
      'name': 'У/П (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 12: {'divide': ('damage', 'joinCnt'),
      'isAverage': 1,
      'key': 'averDamage',
      'name': 'Нанесенный урон (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 13: {'divide': ('cureTotal', 'joinCnt'),
      'isAverage': 1,
      'key': 'averCure',
      'name': 'Лечение (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 14: {'divide': ('beDamageTotal', 'joinCnt'),
      'isAverage': 1,
      'key': 'averBeDamage',
      'name': 'Полученный урон (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 15: {'divide': ('dieCnt', 'joinCnt'),
      'isAverage': 1,
      'key': 'averDieCnt',
      'name': 'Смерти (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 16: {'divide': ('donateScore', 'joinCnt'),
      'isAverage': 1,
      'key': 'averDonateScore',
      'name': 'Вклад (в среднем)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 17: {'key': 'maxBFTime',
      'name': 'Самый длинный бой (сек.)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 18: {'key': 'minBFTime',
      'name': 'Самый короткий бой (сек.)',
      'type': [0,
               1,
               2,
               3,
               8,
               9]},
 19: {'gloryFrameIdx': 0,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'firstBloodCnt',
      'name': 'Первая кровь × %s'},
 20: {'gloryFrameIdx': 1,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'legendaryCnt',
      'name': 'Больше всего убийств × %s'},
 21: {'gloryFrameIdx': 2,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'maxjibaiCnt',
      'name': 'Лучшая серия убийств × %s'},
 22: {'gloryFrameIdx': 3,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'firstCnt',
      'name': 'Медали дракона x %s'},
 23: {'gloryFrameIdx': 4,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'secondCnt',
      'name': 'Медали тигра × %s'},
 24: {'gloryFrameIdx': 5,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'thirdCnt',
      'name': 'Медали леопарда × %s'},
 25: {'gloryFrameIdx': 6,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'mvp',
      'name': 'MVP×%s'},
 26: {'gloryFrameIdx': 7,
      'isGloryData': [0,
                      1,
                      2,
                      3,
                      8,
                      9],
      'key': 'maxDonateScore',
      'name': 'Самый высокий вклад'},
 27: {'key': 'monsterDamage',
      'name': 'Урон монстрам',
      'type': [1]},
 28: {'key': 'specialBossJibaiCnt',
      'name': 'Вклад (сильные монстры)',
      'type': [1]},
 29: {'key': 'mouseJibaiCnt',
      'name': 'Убийства (крыса-обжора)',
      'type': [1]},
 30: {'key': 'specialZaijuDamage',
      'name': 'Урон (древодемон)',
      'type': [1]},
 31: {'divide': ('monsterDamage', 'joinCnt'),
      'isAverage': 1,
      'key': 'averMonsterDamage',
      'name': 'Урон монстрам (в среднем)',
      'type': [1]},
 32: {'key': 'holdFlagCnt',
      'name': 'Вклад (башни)',
      'type': [2]},
 33: {'key': 'fightInFlagTime',
      'name': 'Вклад (бой)',
      'type': [2]},
 34: {'key': 'enterFly',
      'name': 'Управление орнитоптером',
      'type': [3]},
 35: {'key': 'killFlyCnt',
      'name': 'Орнитоптеров уничтожено',
      'type': [3]},
 36: {'key': 'withFlyDamageTotal',
      'name': 'Урон (орнитоптер)',
      'type': [3]},
 37: {'key': 'fightInFlagTime',
      'name': 'Вклад (бой)',
      'type': [3]},
 38: {'divide': ('killFlyCnt', 'joinCnt'),
      'isAverage': 1,
      'key': 'averJibaiFlyCnt',
      'name': 'Орнитоптеров уничтожено (в среднем)',
      'type': [3]},
 39: {'divide': ('withFlyDamageTotal', 'joinCnt'),
      'isAverage': 1,
      'key': 'averFlyDamage',
      'name': 'Средний урон (орнитоптер)',
      'type': [3]},
 40: {'gloryFrameIdx': 0,
      'isGloryData': [12],
      'key': 'pubg150',
      'name': 'Совокупные выигрыши×%s'},
 41: {'gloryFrameIdx': 1,
      'isGloryData': [12],
      'key': 'pubg151',
      'name': 'Совокупное участие×%s'},
 42: {'gloryFrameIdx': 2,
      'isGloryData': [12],
      'key': 'pubg152',
      'name': 'Совокупные убийства×%s'},
 43: {'gloryFrameIdx': 3,
      'isGloryData': [12],
      'key': 'pubg153',
      'name': 'Совокупные передачи×%s'},
 44: {'gloryFrameIdx': 4,
      'isGloryData': [12],
      'key': 'pubg120',
      'name': 'Участие в сезоне×%s'},
 45: {'gloryFrameIdx': 5,
      'isGloryData': [12],
      'key': 'pubg122',
      'name': 'Сезон проигран×%s'},
 46: {'gloryFrameIdx': 6,
      'isGloryData': [12],
      'key': 'pubg124',
      'name': 'Результативные передачи в сезоне×%s'},
 47: {'gloryFrameIdx': 7,
      'isGloryData': [12],
      'key': 'pubg125',
      'name': 'Совокупный ущерб в течение сезона'},
 48: {'key': 'pubg131',
      'name': 'Участвовал в сессии на прошлой неделе',
      'type': [12]},
 49: {'key': 'pubg133',
      'name': 'Первые 8 сеансов на прошлой неделе',
      'type': [12]},
 50: {'key': 'pubg132',
      'name': 'Совокупное поражение на прошлой неделе',
      'type': [12]},
 51: {'key': 'pubg134',
      'name': 'Накопленные голевые передачи на прошлой неделе',
      'type': [12]},
 52: {'key': 'pubg135',
      'name': 'Совокупный ущерб на прошлой неделе',
      'type': [12]},
 53: {'key': 'pubg137',
      'name': 'Средняя продолжительность времени на прошлой неделе',
      'type': [12]}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')