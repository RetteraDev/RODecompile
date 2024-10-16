#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/reward_catch_up_data.o
data = {1001: {'ItemTitle': 'Дух в поисках ★★★(%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 1.635 * int(6 / 3.0) * 200 * 1.2 + int(int((d['lv'] + 2.2) ** 1.45 / 2.0) * d['lv'] * 0.1 + 5) * 5 * 5 * 15 * 0.75 + 16 * int(min(max(64, int((d['lv'] + 2.2) ** 1.45 / 2.0)), 273) * (0.5 * d['lv'] + max(12, min(0.5 * d['lv'], 35))) * 0.1 * 69.387) + 100 * (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5),
        'bonusIds': {(1, 99): 16395},
        'consumeCoins': lambda d: round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.34, 0) + round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.12, 0) + round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.48, 0) + round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.06, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Зов духов ★★★',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 0},
 1002: {'ItemTitle': 'Порядок удаления пыли (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30,
        'bonusIds': {(1, 39): 21801,
                     (40, 49): 21802,
                     (50, 59): 21803,
                     (60, 69): 21804,
                     (70, 99): 21805},
        'consumeCoins': lambda d: 5,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (30, 89),
        'name': 'Битва с демонами',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 1},
 1003: {'ItemTitle': 'Ежедневные задания гильдии (%d раз)',
        'addExp': lambda d: (int(min((d['lv'] + 2.2) ** 1.45, 260) * 35 * 0.05) + 5) * 5 * 100,
        'bonusIds': {(1, 99): 21786},
        'consumeCoins': lambda d: 9,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Гильдейские задания',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 2},
 1004: {'ItemTitle': 'Святая Церковь*Кооперативное возрождение (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((532, 600),),
        'bonusIds': {(1, 99): 21787},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот стражей',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 3,
        'sortOrder': 3},
 1005: {'ItemTitle': 'Юйсу*Сотрудничайте, чтобы возродиться (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((533, 600),),
        'bonusIds': {(1, 99): 21788},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот магов',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 4,
        'sortOrder': 3},
 1006: {'ItemTitle': 'Клинок Света*Совместное возрождение (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((534, 600),),
        'bonusIds': {(1, 99): 21789},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот рыцарей',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 5,
        'sortOrder': 3},
 1007: {'ItemTitle': 'Линглонг*Возрождение кооператива (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((536, 600),),
        'bonusIds': {(1, 99): 21790},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот друидов',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 7,
        'sortOrder': 3},
 1008: {'ItemTitle': 'Яньтянь* Сотрудничайте, чтобы возродиться (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((535, 600),),
        'bonusIds': {(1, 99): 21791},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот стрелков',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 6,
        'sortOrder': 3},
 1009: {'ItemTitle': 'Стример*Возрождение кооператива (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((537, 600),),
        'bonusIds': {(1, 99): 21792},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот жнецов',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 8,
        'sortOrder': 3},
 1010: {'ItemTitle': 'Отраслевой тормоз*Сотрудничайте, чтобы возродиться (%d раз)',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((538, 600),),
        'bonusIds': {(1, 99): 21793},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Оплот ассасинов',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 9,
        'sortOrder': 3},
 1011: {'ItemTitle': 'Тяньчжао*Возрождение кооператива (%d раз)',
        'activityCanCatchUpStartTime': '0 10 17 12 * 2020',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 10,
        'addFame': ((538, 600),),
        'bonusIds': {(1, 99): 21794},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 4 + 21.5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (20, 89),
        'name': 'Тяньчжао* Сотрудничайте, чтобы возродить',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'school': 10,
        'sortOrder': 3},
 1012: {'ItemTitle': 'Теневой демон (%d раз)',
        'addExp': lambda d: int(min((d['lv'] + 2.2) ** 1.45 / 2, 250) * (0.5 * d['lv'] + min(0.5 * d['lv'], 38)) * 0.05 * 5 * 8) * 2 / 1 * 5,
        'bonusIds': {(1, 99): 16370},
        'consumeCoins': lambda d: 27,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.4',
        'lv': (45, 89),
        'name': 'Демон Мира теней',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 4},
 1013: {'ItemTitle': 'Пиратский груз (%d раз)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30,
        'bonusIds': {(1, 99): 21779},
        'consumeCoins': lambda d: 3,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (50, 89),
        'name': 'Пиратские товары',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 5},
 1014: {'ItemTitle': 'Душа сирены (%d раз)',
        'bonusIds': {(1, 99): 21780},
        'consumeCoins': lambda d: 4,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (50, 89),
        'name': 'Души Темноводных',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 5},
 1015: {'ItemTitle': 'Пик конкуренции (%d раз)',
        'activityCanCatchUpStartTime': '0 10 18 10 * 2018',
        'addExp': lambda d: int((d['lv'] + 2.2) ** 1.45 / 2 * d['lv'] * 0.1 + 5) * 5 * 15 * 1,
        'bonusIds': {(1, 99): 21781},
        'consumeCoins': lambda d: 2,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Арена сильнейших',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 6},
 1016: {'ItemTitle': 'Лингсу*Убивающий Бога (%d раз)',
        'bonusIds': {(1, 99): 21812},
        'consumeCoins': lambda d: 23,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (55, 64),
        'name': 'Лингсу*Убивающий Бога',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 7},
 1017: {'ItemTitle': 'Подземная Великая стена*Убийство Бога (%d раз)',
        'bonusIds': {(1, 99): 21813},
        'consumeCoins': lambda d: 41,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (65, 74),
        'name': 'Подземная Великая стена* Убивающий Бога',
        'periodCnt': 2,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 8},
 1018: {'ItemTitle': 'Курган мечей*Убивающий Бога (%d раз)',
        'bonusIds': {(1, 99): 21814},
        'consumeCoins': lambda d: 49,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (75, 89),
        'name': 'Джианзука*Убивающий Бога',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 9},
 1019: {'ItemTitle': 'Заброшенное святилище*Вызов (%d раз)',
        'activityCanCatchUpStartTime': '0 10 15 6 * 2017',
        'bonusIds': {(1, 99): 21815},
        'consumeCoins': lambda d: 23,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (59, 68),
        'name': 'Храм проклятых',
        'periodCnt': 2,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 10},
 1020: {'ItemTitle': 'Меха Сити*Вызов (%d раз)',
        'activityCanCatchUpStartTime': '0 10 15 6 * 2017',
        'bonusIds': {(1, 99): 21816},
        'consumeCoins': lambda d: 39,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (69, 78),
        'name': 'Машинариум',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 11},
 1021: {'ItemTitle': 'Длинный Юань*Вызов (%d раз)',
        'activityCanCatchUpStartTime': '0 10 25 5 * 2016',
        'bonusIds': {(1, 99): 21817},
        'consumeCoins': lambda d: 57,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (89, 88),
        'name': 'Вызов Лонгюаня',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 12},
 1022: {'ItemTitle': 'Имперский город Демонов* Разбитая армия· Базовый (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 16 8 * 2018',
        'bonusIds': {(1, 69): 21818,
                     (70, 99): 21819},
        'consumeCoins': lambda d: (d['lv'] > 69) * 180 + (d['lv'] <= 69) * 90,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (69, 89),
        'name': 'Имперский город Демонов* Разбитая Армия· Основание',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 13},
 1023: {'ItemTitle': 'Имперский город демонов*Падение Бога·Базовый (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 12 9 *2019',
        'bonusIds': {(1, 69): 21820,
                     (70, 99): 21821},
        'consumeCoins': lambda d: (d['lv'] > 69) * 210 + (d['lv'] <= 69) * 105,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (69, 89),
        'name': 'Имперский город Демонов*Падение Бога·Основание',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 14},
 1024: {'ItemTitle': 'Двенадцать храмов·Парадный зал (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 14 12 * 2017',
        'bonusIds': {(1, 99): 21833},
        'consumeCoins': lambda d: (d['lv'] > 59) * 7 + (d['lv'] <= 59) * 4,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (59, 89),
        'name': 'Первый сектор Храма Двенадцати',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 15},
 1025: {'ItemTitle': 'Двенадцать храмов·Неф (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 14 12 * 2017',
        'bonusIds': {(1, 99): 21834},
        'consumeCoins': lambda d: (d['lv'] > 59) * 25 + (d['lv'] <= 59) * 14,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (59, 89),
        'name': 'Второй сектор Храма Двенадцати',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 16},
 1026: {'ItemTitle': 'Двенадцать храмов*Апсида (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 14 12 * 2017',
        'bonusIds': {(1, 99): 21835},
        'consumeCoins': lambda d: 120 * min(max(d['lv'] - 69, 0), 1) + 112 * min(max(70 - d['lv'], 0) * max(d['lv'] - 59, 0), 1) + 64 * min(max(60 - d['lv'], 0), 1),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (59, 89),
        'name': 'Третий сектор Храма Двенадцати',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 17},
 1027: {'ItemTitle': 'Прогулки по Сулану (Пропущено: %d)',
        'addExp': lambda d: min(300, max((d['lv'] + 2.2) ** 1.45 * 0.5, 69)) * max(min(74, d['lv']), 6 + 0.8 * d['lv']) * 2.1 * 2 * 34,
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 28, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (30, 89),
        'name': 'Прогулки по Сулану',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 18},
 1028: {'ItemTitle': 'Во имя Хранителей (Пропущено: %d)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'addExp': lambda d: (int((int(d['lv'] / 5) * 5 + 2.2) ** 1.45 * int(d['lv'] / 5) * 5 * 0.05) + 5) * 5 * 4 * 15 * 1.5,
        'bonusIds': {(1, 99): 21806},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 9 + 5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (30, 89),
        'name': 'Во имя Хранителей',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 19},
 1029: {'ItemTitle': 'Петля времени (Пропущено: %d)',
        'activityCanCatchUpStartTime': '0 10 29 6 * 2017',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 75 * (3 + (d['lv'] >= 60) * 2),
        'bonusIds': {(1, 59): 21807,
                     (60, 69): 21808,
                     (70, 99): 21809},
        'consumeCoins': lambda d: round((int((d['lv'] - 5) / 10 + 10) * 0.0625 * 18 + 4.5) * 5 / 3, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.4',
        'lv': (50, 89),
        'name': 'Петля времени',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 20},
 1030: {'ItemTitle': 'Поле боя (Пропущено: %d)',
        'activityCanCatchUpStartTime': '0 10 6 8 * 2020',
        'addExp': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 4 * 15 * 1.5,
        'bonusIds': {(1, 99): 21810},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 9 + (11 + 9 * min(max(d['lv'] - 60, 0), 1) + 18 * min(max(d['lv'] - 70, 0), 1)), 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Поле боя',
        'periodCnt': 5,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 21},
 1031: {'ItemTitle': 'Теософский экзамен (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'bonusIds': {(1, 99): 21784},
        'consumeCoins': lambda d: 30,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (35, 89),
        'name': 'Теософский экзамен',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 22},
 1032: {'ItemTitle': 'Башня затмения (Пропущено: %d)',
        'addFame': ((446, 240),),
        'bonusIds': {(1, 99): 16392},
        'consumeCoins': lambda d: 51,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (59, 89),
        'name': 'Башня затмения',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 23},
 1033: {'ItemTitle': 'Испытания Крылатых (%d р.)',
        'activityCanCatchUpStartTime': '0 10 26 4 * 2018',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'bonusIds': {(1, 99): 21798},
        'consumeCoins': lambda d: 17,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (55, 89),
        'name': 'Испытания Крылатых',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 24},
 1034: {'ItemTitle': 'Остров Разбитой Звезды (%d раз)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'bonusIds': {(1, 99): 21782},
        'consumeCoins': lambda d: 15,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Остров расколотых звезд',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 25},
 1035: {'ItemTitle': 'Темный легион (Пропущено: %d)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'bonusIds': {(1, 99): 21797},
        'consumeCoins': lambda d: 13,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Темный легион',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 26},
 1036: {'ItemTitle': 'Небесная битва (%d раз)',
        'activityCanCatchUpStartTime': '0 10 5 12 * 2019',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 3,
        'bonusIds': {(1, 99): 21795},
        'consumeCoins': lambda d: 30,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Небесная битва',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 27},
 1037: {'ItemTitle': 'Игра на выживание (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30,
        'bonusIds': {(1, 99): 22129},
        'consumeCoins': lambda d: 13,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Игра на выживание',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 28},
 1038: {'ItemTitle': 'Сюнь Цинь Цзи*Ручное оборудование (%d раз)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'activityCanCatchUpStartTime': '0 10 21 4 * 2016',
        'addExp': lambda d: (min(200, max(int((d['lv'] + 2.2) ** 1.45 / 2.0), 154)) * max(0.3 * d['lv'] + min(40, 0.7 * d['lv']), 44) * 0.1 + 5) * 5 * 1.3 * 2 * 120,
        'bonusIds': {(1, 49): 21688,
                     (50, 59): 21689,
                     (60, 69): 21690,
                     (70, 99): 21691},
        'consumeCoins': lambda d: 200,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0',
        'lv': (40, 89),
        'name': 'Торговые поручения',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 29},
 1039: {'ItemTitle': 'Парк развлечений (Пропущено: %d)',
        'activityCanCatchUpEndTime': '0 8 17 12 * 2020',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'addFame': ((438, 300),),
        'bonusIds': {(1, 99): 21811},
        'consumeCoins': lambda d: round(int(max(5, (d['lv'] - 5) / 10) + 10) * 0.0625 * 35 + 43.9, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (35, 89),
        'name': 'Парк развлечений',
        'periodCnt': 2,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 30},
 1040: {'ItemTitle': 'Рыбомания (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'bonusIds': {(1, 99): 21796},
        'consumeCoins': lambda d: 13,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Рыбомания',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 31},
 1041: {'ItemTitle': 'Беглые истории (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 4,
        'bonusIds': {(1, 99): 21800},
        'consumeCoins': lambda d: 55,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (40, 89),
        'name': 'Беглые истории',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 3,
        'sortOrder': 32},
 1042: {'ItemTitle': 'Клуб знатоков (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 4,
        'bonusIds': {(1, 99): 21799},
        'consumeCoins': lambda d: 52,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (49, 89),
        'name': 'Ходячая энциклопедия',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 3,
        'sortOrder': 33},
 1043: {'ItemTitle': 'Игры лунного затмения (Пропущено: %d)',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 4,
        'addFame': ((446, 240),),
        'bonusIds': {(1, 99): 21783},
        'consumeCoins': lambda d: 46,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (59, 89),
        'name': 'Игры лунного затмения',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 3,
        'sortOrder': 34},
 1044: {'ItemTitle': 'Экзорцист Чжоу Фэн (%d раз)',
        'activityType': 26,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (30, 89),
        'name': 'Орден Хранителей',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 35},
 1045: {'ItemTitle': 'Еженедельный оклад воинского звания (%d раз)',
        'activityType': 27,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (30, 89),
        'name': 'Империя',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 36},
 1046: {'ItemTitle': 'Парк развлечений (Пропущено: %d)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30 * 2,
        'addFame': ((438, 300),),
        'bonusIds': {(1, 99): 22457},
        'consumeCoins': lambda d: round(int(max(5, (d['lv'] - 5) / 10) + 10) * 0.0625 * 35 + 43.9, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (35, 89),
        'name': 'Парк развлечений',
        'periodCnt': 2,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 30},
 1047: {'ItemTitle': 'Сюнь Цинь Цзи*Ручное оборудование (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'addExp': lambda d: (min(200, max(int((d['lv'] + 2.2) ** 1.45 / 2.0), 154)) * max(0.3 * d['lv'] + min(40, 0.7 * d['lv']), 44) * 0.1 + 5) * 5 * 1.3 * 2 * 120,
        'bonusIds': {(1, 49): 21688,
                     (50, 59): 21689,
                     (60, 69): 21690,
                     (70, 79): 21691,
                     (80, 89): 22459},
        'consumeCoins': lambda d: 200,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0',
        'lv': (40, 89),
        'name': 'Торговые поручения',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 29},
 1048: {'ItemTitle': 'Во имя Хранителей (Пропущено: %d)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'addExp': lambda d: (int((int(d['lv'] / 5) * 5 + 2.2) ** 1.45 * int(d['lv'] / 5) * 5 * 0.05) + 5) * 5 * 4 * 15 * 1.5,
        'bonusIds': {(1, 79): 21806,
                     (80, 89): 22460},
        'consumeCoins': lambda d: round(int((d['lv'] - 5) / 10 + 10) * 0.0625 * 9 + 5, 0),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (30, 89),
        'name': 'Во имя Хранителей',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 19},
 1049: {'ItemTitle': 'Имперский город Демонов* Разбитая армия· Базовый (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'bonusIds': {(1, 69): 21818,
                     (70, 79): 21819,
                     (80, 89): 22461},
        'consumeCoins': lambda d: (d['lv'] > 69) * 180 + (d['lv'] <= 69) * 90 + (d['lv'] > 79) * 36,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (69, 89),
        'name': 'Имперский город Демонов* Разбитая Армия· Основание',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 13},
 1050: {'ItemTitle': 'Имперский город демонов*Падение Бога·Базовый (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'bonusIds': {(1, 69): 21820,
                     (70, 79): 21821,
                     (80, 89): 22462},
        'consumeCoins': lambda d: (d['lv'] > 69) * 210 + (d['lv'] <= 69) * 105 + (d['lv'] > 79) * 42,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (69, 89),
        'name': 'Имперский город Демонов*Падение Бога·Основание',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 14},
 1051: {'ItemTitle': 'Двенадцать храмов·Парадный зал (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'bonusIds': {(1, 79): 21833,
                     (80, 89): 22463},
        'consumeCoins': lambda d: (d['lv'] > 59) * 7 + (d['lv'] <= 59) * 4 + (d['lv'] > 79) * 1.4,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (59, 89),
        'name': 'Первый сектор Храма Двенадцати',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 15},
 1052: {'ItemTitle': 'Двенадцать храмов·Неф (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'bonusIds': {(1, 79): 21834,
                     (80, 89): 22464},
        'consumeCoins': lambda d: (d['lv'] > 59) * 25 + (d['lv'] <= 59) * 14 + (d['lv'] > 79) * 5,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.5',
        'lv': (59, 89),
        'name': 'Второй сектор Храма Двенадцати',
        'periodCnt': 3,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 16},
 1053: {'ItemTitle': 'Двенадцать храмов*Апсида (%d раз)',
        'activityCanCatchUpStartTime': '0 0 21 12 * 2020',
        'bonusIds': {(1, 79): 21835,
                     (80, 89): 22465},
        'consumeCoins': lambda d: 144 * min(max(d['lv'] - 79, 0), 1) + 120 * min(max(d['lv'] - 69, 0), 1) + 112 * min(max(70 - d['lv'], 0) * max(d['lv'] - 59, 0), 1) + 64 * min(max(60 - d['lv'], 0), 1),
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.3',
        'lv': (59, 89),
        'name': 'Третий сектор Храма Двенадцати',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 17},
 1054: {'ItemTitle': 'Порядок удаления пыли (%d раз)',
        'activityCanCatchUpStartTime': '0 0 18 12 * 2020',
        'addExp': lambda d: int(min(int((d['lv'] + 2.2) ** 1.45 / 2), 300) * d['lv'] * 0.1 + 5) * 5 * 30,
        'bonusIds': {(1, 39): 21801,
                     (40, 49): 21802,
                     (50, 59): 21803,
                     (60, 69): 21804,
                     (70, 79): 21805,
                     (80, 89): 22458},
        'consumeCoins': lambda d: 5,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0.6',
        'lv': (30, 89),
        'name': 'Битва с демонами',
        'periodCnt': 1,
        'periodType': 1,
        'periodTypeNum': 1,
        'sortOrder': 1},
 1055: {'ItemTitle': 'Бездна пустоши (%d раз)',
        'activityCanCatchUpStartTime': '0 0 18 12 * 2020',
        'bonusIds': {(80, 99): 22468},
        'consumeCoins': lambda d: 140,
        'disCount': lambda d: max(1 - (max((int((d['days'] - 30) / 30), 1)) - 1) * 0.05, 0.6),
        'freePercent': '0',
        'lv': (80, 89),
        'name': 'Бездна пустоши',
        'periodCnt': 1,
        'periodType': 2,
        'periodTypeNum': 1,
        'sortOrder': 17}}
