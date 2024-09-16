#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/monster_clan_war_config_data.o
data = {'ZHANJU_ACTION_TIPS': 'Наведите курсор на значок монстра, чтобы увидеть подсказку. Щелкните по нему, чтобы отправиться к месту битвы.',
 'bossKillTip': 'За каждые 3000 ед. урона боссу начисляется 1 оч. отваги.',
 'contributionBonusId': 12922,
 'dmgDivisor': 3000,
 'minLv': 40,
 'monsterKillTip': 'За уничтожение обычного монстра начисляется 1 оч. отваги.<BR>За уничтожение сильного – 5 оч. За редкого – 10 оч. отваги.',
 'rankBonus': {'40_69': ((1, 2, 13040), (3, 5, 13041), (6, 10, 13042)),
               '70_79': ((1, 2, 13040), (3, 5, 13041), (6, 10, 13042))},
 'rewardThreshold': 100}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
