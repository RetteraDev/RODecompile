#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/summon_sprite_ability_display_data.o
data = {(1, 1): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Здоровье: [1.p1]</font>\n\nРасходуется при получении урона.\nБазовый запас здоровья: <font color=\'#66CD00\'>[1.p2]</font>\nДополнительный запас здоровья: <font color=\'#66CD00\'>[1.p3]</font>",
          'displayOrder': 1,
          'formual1Params': (10053,),
          'formual2Params': (30004,),
          'formual3Params': (10053, 30004),
          'formula1': 'p1',
          'formula2': 'p1',
          'formula3': 'p1-p2',
          'idParam': [((10053,), 'p1')],
          'name': 'Здоровье',
          'showType': '[1.p1]',
          'type': 1},
 (1, 2): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Сила атаки: [1.p1]</font>\n\nУвеличивает физический урон от умений и обычных атак.\nБазовая сила атаки: <font color=\'#66CD00\'>[1.p2]</font>\nДополнительная сила атаки: <font color=\'#66CD00\'>[1.p3]</font>",
          'displayOrder': 2,
          'formual1Params': (12010, 12020),
          'formual2Params': (30001,),
          'formual3Params': (12010, 12020, 30001),
          'formula1': 'p1+p2',
          'formula2': 'p1',
          'formula3': 'p1+p2-p3',
          'idParam': [((12010, 12020), 'p1+p2')],
          'name': 'Сила атаки',
          'showType': '[1.p1]',
          'type': 1},
 (1, 3): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Защита: [1.p1]</font>\n\nКогда духа атакует противник того же уровня, получаемый физический урон снижается на <font color=\'#66CD00\'>[2.p2]</font> (вплоть до <font color=\'#66CD00\'>90%</font>).\nБазовая защита: <font color=\'#66CD00\'>[1.p3]</font>\nДополнительная защита: <font color=\'#66CD00\'>[1.p4]</font>",
          'displayOrder': 3,
          'formual1Params': (12100,),
          'formual2Params': (12100, 10000),
          'formual3Params': (30002,),
          'formual4Params': (12100, 30002),
          'formula1': 'p1',
          'formula2': 'min(1.0*p1/(p1+40*(p2+5)),0.9)',
          'formula3': 'p1',
          'formula4': 'p1-p2',
          'idParam': [((12100, 12116), 'p1+p2')],
          'name': 'Защита',
          'showType': '[1.p1]',
          'type': 1},
 (1, 4): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Сила заклинаний: [1.p1]</font>\n\nУвеличивает магический урон от умений и обычных атак.\nБазовая сила заклинаний: <font color=\'#66CD00\'>[1.p2]</font>\nДополнительная сила заклинаний: <font color=\'#66CD00\'>[1.p3]</font>",
          'displayOrder': 4,
          'formual1Params': (12012, 12021),
          'formual2Params': (30005,),
          'formual3Params': (12012, 12021, 30005),
          'formula1': 'p1+p2',
          'formula2': 'p1',
          'formula3': 'p1+p2-p3',
          'idParam': [((12012, 12021), 'p1+p2')],
          'name': 'Сила заклинаний',
          'showType': '[1.p1]',
          'type': 1},
 (1, 5): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Сопротивление: [1.p1]</font>\n\nКогда духа атакует противник того же уровня, получаемый магический урон снижается на <font color=\'#66CD00\'>[2.p2]</font> (вплоть до <font color=\'#66CD00\'>90%</font>).\nБазовое сопротивление: <font color=\'#66CD00\'>[1.p3]</font>\nДополнительное сопротивление: <font color=\'#66CD00\'>[1.p4]</font>",
          'displayOrder': 5,
          'formual1Params': (12101,),
          'formual2Params': (12101, 10000),
          'formual3Params': (30003,),
          'formual4Params': (12101, 30003),
          'formula1': 'p1',
          'formula2': 'min(1.0*p1/(p1+40*(p2+5)),0.9)',
          'formula3': 'p1',
          'formula4': 'p1-p2',
          'idParam': [((12101, 12117), 'p1+p2')],
          'name': 'Сопротивление',
          'showType': '[1.p1]',
          'type': 1},
 (2, 1): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Критический удар: [2.p1]</font>\n\nШанс нанести критический урон при использовании обычной атаки или умения: <font color=\'#66CD00\'>[2.p1]</font>.\nБазовый критический удар: <font color=\'#66CD00\'>1%</font>\nДополнительный критический удар: <font color=\'#66CD00\'>[2.p2]</font>",
          'displayOrder': 1,
          'formual1Params': (12138,),
          'formual2Params': (12138,),
          'formula1': '1.0*p1',
          'formula2': '1.0*p1-0.01',
          'idParam': [((12138,), '1.0*p1')],
          'name': 'Критический удар',
          'showType': '[2.p1]',
          'type': 2},
 (2, 10): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Скорость восстановления умений ярости духов: [2.p1]</font>\n\nУмения ярости духов восстанавливаются на <font color=\'#66CD00\'>[2.p1]</font> быстрее.\nНе может превышать <font color=\'#66CD00\'>60%</font>.",
           'displayOrder': 10,
           'formual1Params': (12136,),
           'formula1': '1.0*p1',
           'idParam': [((12136,), '1.0*p1')],
           'name': 'Восстановление ярости духов',
           'showType': '[2.p1]',
           'type': 2},
 (2, 11): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Вероятность блокирования: [2.p1]</font>\n\nКогда духа атакуют, с вероятностью <font color=\'#66CD00\'>[2.p1]</font> он может блокировать атаку.\nБазовая вероятность блокирования: <font color=\'#66CD00\'>1%</font>\nДополнительная вероятность блокирования: <font color=\'#66CD00\'>[2.p2]</font>",
           'displayOrder': 11,
           'formual1Params': (12113,),
           'formual2Params': (12113,),
           'formula1': '1.0*p1',
           'formula2': '1.0*p1-0.01',
           'idParam': [((12113,), '1.0*p1')],
           'name': 'Вероятность блокирования',
           'showType': '[2.p1]',
           'type': 2},
 (2, 12): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Блокирование: [2.p1]</font>\n\nПри успешном блокировании урон от атаки снижается на <font color=\'#66CD00\'>[2.p1]</font>.\nБазовое блокирование: <font color=\'#66CD00\'>30%</font>\nДополнительное блокирование: <font color=\'#66CD00\'>[2.p2]</font>\nНе может превышать <font color=\'#66CD00\'>70%</font>.",
           'displayOrder': 12,
           'formual1Params': (12104,),
           'formual2Params': (12104,),
           'formula1': '1.0*p1',
           'formula2': '1.0*p1-0.3',
           'idParam': [((12104,), '1.0*p1')],
           'name': 'Блокирование',
           'showType': '[2.p1]',
           'type': 2},
 (2, 13): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Вероятность уклонения: [2.p1]</font>\n\nКогда духа атакуют, с вероятностью <font color=\'#66CD00\'>[2.p1]</font> он может уклониться от атаки.\nБазовая вероятность уклонения: <font color=\'#66CD00\'>1%</font>\nДополнительная вероятность уклонения: <font color=\'#66CD00\'>[2.p2]</font>",
           'displayOrder': 13,
           'formual1Params': (12106,),
           'formual2Params': (12106,),
           'formula1': '1.0*p1',
           'formula2': '1.0*p1-0.01',
           'idParam': [((12106,), '1.0*p1')],
           'name': 'Вероятность уклонения',
           'showType': '[2.p1]',
           'type': 2},
 (2, 14): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Уклонение: [2.p1]</font>\n\nПри успешном уклонении урон от атаки снижается на <font color=\'#66CD00\'>[2.p1]</font>.\nБазовое уклонение: <font color=\'#66CD00\'>70%</font>\nДополнительное уклонение: <font color=\'#66CD00\'>[2.p2]</font>\nНе может превышать <font color=\'#66CD00\'>100%</font>.",
           'displayOrder': 14,
           'formual1Params': (12120,),
           'formual2Params': (12120,),
           'formula1': '1.0*p1',
           'formula2': '1.0*p1-0.7',
           'idParam': [((12120,), '1.0*p1')],
           'name': 'Уклонение',
           'showType': '[2.p1]',
           'type': 2},
 (2, 15): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Устойчивость к критическому удару: [2.p1]</font>\n\nШанс получить критический урон снижается на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 15,
           'formual1Params': (12140,),
           'formula1': '1.0*p1',
           'idParam': [((12140,), '1.0*p1')],
           'name': 'Устойчивость к критическому удару',
           'showType': '[2.p1]',
           'type': 2},
 (2, 16): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Устойчивость к комбо-ударам: [2.p1]</font>\n\nСнижает шанс противника нанести комбо-удар при обычной атаке на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 16,
           'formual1Params': (12141,),
           'formula1': '1.0*p1',
           'idParam': [((12141,), '1.0*p1')],
           'name': 'Устойчивость к комбо-ударам',
           'showType': '[2.p1]',
           'type': 2},
 (2, 17): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Усиление физического урона: [2.p1]</font>\n\nУвеличивает физический урон на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 17,
           'formual1Params': (12025,),
           'formula1': '1.0*p1',
           'idParam': [((12025,), '1.0*p1')],
           'name': 'Усиление физ. урона',
           'showType': '[2.p1]',
           'type': 2},
 (2, 18): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Усиление магического урона: [2.p1]</font>\n\nУсиливает эффекты, наносящие магический урон, на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 18,
           'formual1Params': (12026,),
           'formula1': '1.0*p1',
           'idParam': [((12026,), '1.0*p1')],
           'name': 'Усиление маг. урона',
           'showType': '[2.p1]',
           'type': 2},
 (2, 19): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Устойчивость к физическому урону: [2.p1]</font>\n\nСнижает получаемый физический урон на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 19,
           'formual1Params': (12108,),
           'formula1': '1.0*p1',
           'idParam': [((12108,), '1.0*p1')],
           'name': 'Устойчивость к физ. урону',
           'showType': '[2.p1]',
           'type': 2},
 (2, 2): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Критический урон: [2.p1]</font>\n\nДополнительный урон при нанесении критического удара: <font color=\'#66CD00\'>[2.p1]</font>.\nБазовый критический урон: <font color=\'#66CD00\'>100%</font>\nДополнительный критический урон: <font color=\'#66CD00\'>[2.p2]</font>\nМаксимальный бонус не более<font color=\'#66CD00\'>250%</font>",
          'displayOrder': 2,
          'formual1Params': (12139,),
          'formual2Params': (12139,),
          'formula1': '1.0*p1',
          'formula2': '1.0*p1-1.0',
          'idParam': [((12139,), '1.0*p1')],
          'name': 'Критический урон',
          'showType': '[2.p1]',
          'type': 2},
 (2, 20): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Устойчивость к магическому урону: [2.p1]</font>\n\nСнижает получаемый магический урон на <font color=\'#66CD00\'>[2.p1]</font>.",
           'displayOrder': 20,
           'formual1Params': (12109,),
           'formula1': '1.0*p1',
           'idParam': [((12109,), '1.0*p1')],
           'name': 'Устойчивость к маг. урону',
           'showType': '[2.p1]',
           'type': 2},
 (2, 3): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Скорость атаки: [2.p1]</font>\n\nСкорость обычных атак: <font color=\'#66CD00\'>[2.p1]</font>.\nНе может превышать <font color=\'#66CD00\'>250%</font>.",
          'displayOrder': 3,
          'formual1Params': (12143,),
          'formula1': '1.0*p1+1.0',
          'idParam': [((12143,), '1.0*p1+1.0')],
          'name': 'Скорость атаки',
          'showType': '[2.p1]',
          'type': 2},
 (2, 4): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Скорость применения умений: [2.p1]</font>\n\nУмения применяются на <font color=\'#66CD00\'>[2.p1]</font> быстрее.\nНе может превышать <font color=\'#66CD00\'>400%</font>.",
          'displayOrder': 4,
          'formual1Params': (12142,),
          'formula1': '1.0*p1+1.0',
          'idParam': [((12142,), '1.0*p1+1.0')],
          'name': 'Скорость применения умений',
          'showType': '[2.p1]',
          'type': 2},
 (2, 5): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Комбо-удар: [2.p1]</font>\n\nШанс нанести двойной урон при обычной атаке: <font color=\'#66CD00\'>[2.p1]</font>\nБазовый комбо-удар: <font color=\'#66CD00\'>1%</font>\nДополнительный комбо-удар: <font color=\'#66CD00\'>[2.p2]</font>",
          'displayOrder': 5,
          'formual1Params': (12134,),
          'formual2Params': (12134,),
          'formula1': '1.0*p1',
          'formula2': '1.0*p1-0.01',
          'idParam': [((12134,), '1.0*p1')],
          'name': 'Вероятность комбо-удара',
          'showType': '[2.p1]',
          'type': 2},
 (2, 6): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Серия комбо-ударов: [2.p1]</font>\n\nШанс нанести несколько комбо-ударов при обычной атаке: <font color=\'#66CD00\'>[2.p1]</font>",
          'displayOrder': 6,
          'formual1Params': (12135,),
          'formula1': '1.0*p1',
          'idParam': [((12135,), '1.0*p1')],
          'name': 'Серия комбо-ударов',
          'showType': '[2.p1]',
          'type': 2},
 (2, 7): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Энергия: [1.p1]</font>\n\nРасходуется при применении умений.\nБазовый запас энергии: <font color=\'#66CD00\'>100</font>\nДополнительный запас энергии: <font color=\'#66CD00\'>[1.p2]</font>",
          'displayOrder': 7,
          'formual1Params': (10054,),
          'formual2Params': (10054,),
          'formula1': 'p1',
          'formula2': 'p1-100',
          'idParam': [((10054,), 'p1')],
          'name': 'Энергия',
          'showType': '[1.p1]',
          'type': 2},
 (2, 8): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Восстановление энергии: [1.p1]</font>\n\nСкорость восстановления энергии в бою: <font color=\'#66CD00\'>[1.p1]</font> ед. в секунду.\nБазовое восстановление энергии: <font color=\'#66CD00\'>[2.p2]</font>, что соответствует <font color=\'#66CD00\'>[1.p4]</font> ед.\nДополнительное восстановление энергии: <font color=\'#66CD00\'>[1.p3]</font> ед.",
          'displayOrder': 8,
          'formual1Params': (10065, 10054, 10064),
          'formual2Params': (10065,),
          'formual3Params': (10064,),
          'formual4Params': (10065, 10054),
          'formula1': 'p1*p2+p3',
          'formula2': 'p1',
          'formula3': 'p1',
          'formula4': 'p1*p2',
          'idParam': [((10065, 10054, 10064), 'p1*p2+p3')],
          'name': 'Восстановление энергии',
          'showType': '[1.p1]',
          'type': 2},
 (2, 9): {'detail1': "<font size = \'14\' color =\'#E5BE67\'>Скорость восстановления умений: [2.p1]</font>\n\nОбычные умения восстанавливаются на <font color=\'#66CD00\'>[2.p1]</font> быстрее.\nНе может превышать <font color=\'#66CD00\'>60%</font>.",
          'displayOrder': 9,
          'formual1Params': (12133,),
          'formula1': '1.0*p1',
          'idParam': [((12133,), '1.0*p1')],
          'name': 'Скорость восстановления умений',
          'showType': '[2.p1]',
          'type': 2}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')