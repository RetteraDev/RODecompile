#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/arena_playoffs_schedule_desc_data.o
data = {1: {'endCrontab': '0 14 8 10 *',
     'name': 'Этап регистрации',
     'playoffsPlayDesc': 'Регистрация отряда начинается: 10/1 18: 00\n Регистрация отряда заканчивается в: 10/8 14:00',
     'playoffsTeamDesc': 'Арена Дан самый высокий уровень иерархии и трех игроков, чтобы представить свой уровень клана, клан ранжирования по крайней мере убедиться, что каждый сервер имеет команда квалификацию, каждая экстракция сегмент класса самый высокий рейтинг команды команда квалифицироваться, общее количество квалификационных групп каждого сегмента высокого уровня 64.',
     'startCrontab': '0 8 29 9 *',
     'title': 'Облако висит Budokai'},
 2: {'endCrontab': '0 23 15 10 *',
     'name': 'Групповой этап',
     'playoffsPlayDesc': 'Состязания проводятся в 19.00 по понедельникам, средам, пятницам и воскресеньям. Подробности см. в «Текущей сводке».',
     'playoffsTeamDesc': '1. Состязания проводятся по модели «3 победы из 5», после входа на поле боя менять участников нельзя. Выход с поля боя расценивается как отказ от борьбы.\n2. По завершении состязаний каждой малой группе на основании числа побед и счета начисляются очки.\n3. 2 лучших игрока в каждой группе получают денежное вознаграждение.',
     'startCrontab': '0 14 8 10 *',
     'title': 'Облако висит Budokai',
     'type': 1},
 3: {'endCrontab': '0 0 30 10 *',
     'name': 'Плей-офф',
     'playoffsPlayDesc': 'Состязания проводятся в 19.00 по понедельникам, средам, пятницам и воскресеньям. Подробности см. в «Текущей сводке».',
     'playoffsTeamDesc': '1. В каждый день состязаний проводится 3 боя, нужно одержать как минимум 2 победы.\n2. Команда, сумевшая победить 2 раза из 3, проходит дальше, проигравшая команда выбывает.\n3. После входа на поле боя менять участников нельзя. Выход с поля боя расценивается как отказ от борьбы.',
     'startCrontab': '0 23 15 10 *',
     'title': 'Облако висит Budokai',
     'type': 2}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')