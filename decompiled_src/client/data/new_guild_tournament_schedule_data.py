#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/new_guild_tournament_schedule_data.o
data = {1: {'crontab': '0 0 * * 0',
     'endTime': 'Понедельник, 0:00',
     'readyTime': 'Понедельник, 0:00',
     'round': 0,
     'startTime': 'Понедельник, 0:00'},
 2: {'crontab': '55 19 * * 4',
     'endTime': 'Пятница, 19:55',
     'readyTime': 'Пятница, 19:55',
     'round': 0,
     'startTime': 'Пятница, 19:55'},
 4: {'crontab': '05 20 * * 4',
     'endTime': '20:30',
     'readyTime': '20:05',
     'round': 1,
     'startTime': '20:10'},
 5: {'crontab': '30 20 * * 4',
     'endTime': '20:55',
     'readyTime': '20:30',
     'round': 2,
     'startTime': '20:35'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
