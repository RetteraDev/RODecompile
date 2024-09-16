#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/chat_reg_rule_data.o
data = {0: {'blackList': (40,),
     'linkText': "<font color=\'#55BDFF\'>[<a href = \'event:baishi%s\'><u>Пригласить наставника</u></a>]</font>",
     'regStr': '.*Принять ученика|Ученик.*'},
 1: {'blackList': (40,),
     'linkText': "<font color=\'#55BDFF\'>[<a href = \'event:shoutu%s\'><u>Взять в ученики</u></a>]</font>",
     'regStr': '.*Пригласить наставника|Наставник.*'},
 2: {'blackList': (22, 23, 30, 40),
     'linkText': "<font color=\'#55BDFF\'>[<a href = \'event:applyTeam%s\'><u>Вступить в группу</u></a>]</font>",
     'regStr': '.*Пригласить в команду|\\+\\+|Любой|Танк|Помощник|Атакер|DPS|Страж|Друид|Рыцарь|Стрелок|Маг|Жнец|Ассасин|Листья|4\\=1|3\\=2|2\\=3.*'},
 3: {'blackList': (22, 23, 30, 40),
     'linkText': "<font color=\'#55BDFF\'>[<a href = \'event:inviteTeam%s\'><u>Пригласить в команду</u></a>]</font>",
     'regStr': '.*Пригласить в команду|\\+\\+|Любой|Танк|Помощник|Атакер|DPS|Страж|Друид|Рыцарь|Стрелок|Маг|Жнец|Ассасин|Листья|4\\=1|3\\=2|2\\=3.*'},
 4: {'blackList': (0, 4, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 114),
     'linkText': "<font color=\'#55BDFF\'>[<a href = \'event:inviteTeam%s\'><u>Пригласить в команду</u></a>]</font>",
     'regStr': '.* Нужна команда для поиска духов. Все, пожалуйста, присоединяйтесь \\ + \\ + \\ +. X'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
