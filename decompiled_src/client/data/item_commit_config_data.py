#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/item_commit_config_data.o
data = {'canExtraRewordMsg': 'Доступно дополнительных наград: %s',
 'commitAllMsg': 'За этот взнос вы получите дополнительную награду! (Осталось наград: %s). Продолжить?',
 'commitCntTxt': 'За первые %s взноса в день можно получить дополнительную награду!<br>Наград в неделю: %s. Получено: %s.',
 'commitDaily': 'Получено дополнительных наград: %s',
 'commitWeekMax': 'Получено дополнительных наград: %s',
 'itemCommitRateMsg': {1: 'Сейчас вы не получаете дополнительные очки снабжения.',
                       1.2: 'Сейчас вы получаете на 20% больше очков снабжения за взнос.',
                       1.5: 'Сейчас вы получаете на 50% больше очков снабжения за взнос.',
                       2: 'Сейчас вы получаете на 100% больше очков снабжения за взнос!'},
 'rewardRates': ((0, 0.6667, 2),
                 (0.6667, 0.8333, 1.5),
                 (0.8333, 1, 1.2),
                 (1, 999, 1))}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
