#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/migrate_server_data.o
valueAttrs = (('id', 'I'),
 ('serverName', 'S'),
 ('migrateOut', 'I'),
 ('migrateIn', 'I'),
 ('invterval', 'S'),
 ('migrateNum', 'I'),
 ('freeMigrate', 'I'),
 ('maxCash', 'I'),
 ('minLv', 'I'),
 ('group', 'I'),
 ('mutex', 'E'),
 ('recommandServer', 'E'),
 ('mailTemplateId', 'I'),
 ('exEailTemplateId', 'I'),
 ('noviceServer', 'I'),
 ('globalFriendGroup', 'I'))
attrs = [ pair[0] for pair in valueAttrs ]
keyType = 1
import sys
import utils
if hasattr(utils, 'MDB_MODULES'):
    utils.MDB_MODULES.add(sys.modules.get(__name__))
data = {99: {'exEailTemplateId': 803,
      'freeMigrate': 1,
      'globalFriendGroup': 2,
      'group': 2,
      'invterval': '3 14 * * 3',
      'mailTemplateId': 538,
      'maxCash': 1000000,
      'migrateIn': 1,
      'migrateNum': 100,
      'migrateOut': 1,
      'minLv': 40,
      'mutex': [29013],
      'noviceServer': 1,
      'serverName': 'Для межсерверных событий'},
 10001: {'globalFriendGroup': 7,
         'group': 1,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10009],
         'serverName': 'Сенатор'},
 10009: {'globalFriendGroup': 7,
         'group': 1,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10001],
         'serverName': 'Не сегодня'},
 10013: {'globalFriendGroup': 7,
         'group': 1,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10001, 10009],
         'serverName': 'Вечная встреча'},
 10015: {'globalFriendGroup': 7,
         'group': 5,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10017,
                             10018,
                             10020,
                             10021],
         'serverName': 'Лучший в своем деле'},
 10017: {'globalFriendGroup': 7,
         'group': 5,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10015,
                             10018,
                             10020,
                             10021],
         'serverName': 'Древняя вечная пропасть'},
 10018: {'globalFriendGroup': 7,
         'group': 5,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10015,
                             10017,
                             10020,
                             10021],
         'serverName': 'Море светлячков'},
 10020: {'globalFriendGroup': 7,
         'group': 5,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10015,
                             10017,
                             10018,
                             10021],
         'serverName': 'Плавающие Воспоминания'},
 10021: {'globalFriendGroup': 7,
         'group': 5,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10015,
                             10017,
                             10018,
                             10020],
         'serverName': 'Милые клены'},
 10022: {'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 0,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Ворота в Звезды'},
 10023: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10059,
                             10064,
                             10024],
         'serverName': 'Moonchaser'},
 10024: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10059],
         'serverName': 'Цветок жизни'},
 10026: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Высшее Возрождение'},
 10028: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Запретный Пик'},
 10031: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Жизнь как сон'},
 10036: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Возвышенная красота'},
 10037: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Карнавал цветов'},
 10038: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Встреча по счастливой случайности'},
 10041: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Луна в отражении'},
 10042: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Цветущий ликорис'},
 10044: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Весенний феникс'},
 10045: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Паническое бегство дракона'},
 10050: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Дворец двух лун'},
 10051: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Обитель страданий'},
 10052: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Сияние'},
 10055: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10059,
                             10023,
                             10064,
                             10024],
         'serverName': 'Крылатый хранитель'},
 10056: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Шаг мерцания'},
 10057: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Танец мечей'},
 10058: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Стремиться к небесам'},
 10059: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Тайны Темного Падения'},
 10060: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10059,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Пелена дождя'},
 10064: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10059,
                             10024],
         'serverName': 'Падение Карима'},
 10065: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Цепляющиеся Приливы'},
 10067: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Пакт Утреннего Снега'},
 10069: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10059,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Отступление Дракона'},
 10071: {'globalFriendGroup': 7,
         'group': 6,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 59,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10023,
                             10064,
                             10024],
         'serverName': 'Живописный пейзаж'},
 10072: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Солнце и Луна'},
 10073: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 7,
         'group': 4,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 50000,
         'migrateIn': 0,
         'migrateNum': 999999,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'recommandServer': [10060,
                             10069,
                             10055,
                             10020,
                             10021,
                             10001,
                             10111,
                             10112],
         'serverName': 'Суланская академия'},
 10074: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Единение сердец'},
 10075: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Сон в летнюю ночь'},
 10076: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Небесный страж'},
 10077: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Облачная пастораль'},
 10078: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Озерный бриз'},
 10079: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Головокружительный взлет'},
 10080: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Серебряные звезды'},
 10081: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Негаснущая любовь'},
 10082: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Весна'},
 10083: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Улыбнитесь, вас снимают'},
 10084: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Чудесная панорама'},
 10085: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Лотри'},
 10086: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Гора Байюнь'},
 10087: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Несравненная красота'},
 10094: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Богатство и процветание'},
 10095: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Я люблю жизнь'},
 10096: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Детские игры'},
 10097: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Подарок \"С Днем всех влюбленных!\"'},
 10098: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Счастливые супруги'},
 10099: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Бесценный дар'},
 10100: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Осенняя песня'},
 10101: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Первый дождь на Горе отшельников'},
 10102: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Инистый веер'},
 10103: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Кинжалы молний'},
 10104: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Звездная тень'},
 10105: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Звездная мечта'},
 10106: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Весна повсюду'},
 10107: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Морской призрак'},
 10108: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Пышный Сулан'},
 10109: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Сказочный день'},
 10110: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Вечное лето'},
 10111: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Сердце океана'},
 10112: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Сто Птиц к Фениксу'},
 10113: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Знай осень с одного листа.'},
 10114: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Город в небесах'},
 10115: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Долина Ветров'},
 10116: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Новое предназначение'},
 10117: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Амор Бэй'},
 10118: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Крылья рассвета'},
 10119: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Море цветов'},
 10120: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Заголовок золотого списка'},
 10121: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Тот берег неба'},
 10122: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Ветер гонит облака'},
 10124: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Хмельные песни'},
 10125: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Завоевание Аусгита'},
 10126: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Осгит Судьба'},
 10127: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Весенняя песня войны'},
 10128: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Воитель Крылатых'},
 10129: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Мечта об Осгите'},
 10130: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Рука об руку'},
 10131: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Улица демонов'},
 10132: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Царство Богов'},
 10133: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Происхождение иллюзий'},
 10134: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Фейерверк \"Ледяная вьюга\"'},
 10135: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Жить в соответствии с Шаохуа'},
 10136: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Цветы распускаются на Мо'},
 10137: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Цинлин Именг'},
 10138: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Облака падают, как обычно'},
 10139: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Оседлать ветер и волны'},
 10140: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Обновление Вьентьяна'},
 10141: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Душа Дракона Чжаоши'},
 10142: {'globalFriendGroup': 7,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 59,
         'serverName': 'Юаньин Дэнхуй'},
 29004: {'globalFriendGroup': 2,
         'group': 8,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 0,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 69,
         'recommandServer': [29027],
         'serverName': 'Пимпин'},
 29006: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Ларч'},
 29007: {'globalFriendGroup': 2,
         'group': 8,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 0,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 69,
         'recommandServer': [29027],
         'serverName': 'Минга'},
 29009: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Сэсил'},
 29010: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'serverName': 'Брюн'},
 29011: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'common'},
 29012: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Борч'},
 29013: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Гейб'},
 29014: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Джоуи'},
 29019: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Эмилио'},
 29021: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'serverName': 'Студент Куминь'},
 29027: {'globalFriendGroup': 2,
         'group': 8,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 0,
         'minLv': 69,
         'serverName': 'Он Лунчен'},
 29028: {'globalFriendGroup': 2,
         'group': 8,
         'invterval': '3 14 * * 3',
         'maxCash': 1000000,
         'migrateIn': 0,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 69,
         'recommandServer': [29027],
         'serverName': 'План 1'},
 30000: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'noviceServer': 1,
         'serverName': 'Плановая версия'},
 30001: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'mutex': [29013],
         'noviceServer': 1,
         'serverName': 'Предварительное уведомление'},
 30303: {'exEailTemplateId': 803,
         'freeMigrate': 1,
         'globalFriendGroup': 2,
         'group': 2,
         'invterval': '3 14 * * 3',
         'mailTemplateId': 538,
         'maxCash': 1000000,
         'migrateIn': 1,
         'migrateNum': 100,
         'migrateOut': 1,
         'minLv': 40,
         'mutex': [29013],
         'noviceServer': 1,
         'serverName': 'Межсерверная плановая версия'}}
from MDBUtils import convertToMDB
data = convertToMDB(data, '_'.join(__name__.split('.')), sys.modules.get(__name__))
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')