#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/intimacy_config_data.o
data = {'ALLOW_PULL_INTIMACY_DIGONG': (100, 110, 170, 300, 310, 320),
 'INTIMACY_BIRTH_DESC': 'Сегодня я и %s празднуем день зарождения нашей прекрасной дружбы. Ура!',
 'INTIMACY_QUEST_DESC': 'Сегодня я и %s достигли в наших отношениях нового уровня. И это только начало!',
 'INTIMACY_RESET_LV_LIMIT_BY_REMOVE': 5,
 'INTIMACY_YEARLY_REWARD_NPC_ID': 41544,
 'MAX_INTIMACY_LV': 9,
 'UNBIND_FRIENDSHIP_CASH_WITH_COOP': 10000,
 'fullScreenFirework': 10,
 'scoIconTip': ['Веха',
                'Уровень мастерства',
                'Имперский ранг',
                'Орден Хранителей',
                'PvP-рейтинг',
                'Премиум',
                'Топ-200 рейтинга боевой мощи',
                'Ценность коллекции'],
 'scoIcons': (10002, 10006, 10004, 10005, 10003, 10001, 10008, 10010)}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
