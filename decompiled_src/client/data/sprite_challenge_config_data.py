#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/sprite_challenge_config_data.o
data = {'FbRewardsNotInTop': ((1, 50), (((0, 0.3), (0, 0.3)), ((0.3, 0.65), (0.3, 0.5)), ((0.65, 0.9), (0.5, 0.7)))),
 'SpriteChallengeRewardRemainTip': 'Оставшееся количество доступных сундуков с сокровищами для прохождения Башни Испытаний на сегодняшний день: %d',
 'maxLvConvert': (79, 89),
 'spriteChallengeAvailableLv': {1: (60, 69),
                                2: (70, 79)},
 'spriteChallengeHate': (4, 3, 2, 1),
 'spriteChallengePos': [(-2410, 0, 2985),
                        (-2400, 0, 2982),
                        (-2390, 0, 2985),
                        (-2385, 0, 2992)],
 'spriteChallengeRankInfo': {'60_69': {'bonusCheckId': 209801,
                                       'fbNo': 1363,
                                       'maxLv': 200},
                             '70_79': {'bonusCheckId': 209801,
                                       'fbNo': 1361,
                                       'maxLv': 200}},
 'spriteSpecialSkillInitCD': {12: 14,
                              13: 13,
                              15: 13,
                              17: 13},
 'weekRewardCrontab': '1 0 * * 0'}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
