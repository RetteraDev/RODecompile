#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/team_endless_config_data.o
data = {'affix': {1: (1211, 1212, 1213, 1214, 1215),
           5: (1221, 1222, 1223, 1224),
           10: (1231, 1232, 1233),
           15: (1241,)},
 'fbNos': {(69, 69): (1161, 1162, 1163),
           (70, 79): (1171, 1172, 1173)},
 'fbTypes': {1: (1161, 1171),
             2: (1162, 1172),
             3: (1163, 1173)},
 'levelRewardMail': 2910,
 'reduceLevelWeekly': (2, 4),
 'rewardTimes': {69: 116001,
                 79: 117001},
 'teamEndlessDefaultFloorLimit': 20,
 'teamEndlessFameRewardFormula': 90303,
 'teamEndlessProgressBar': 1000,
 'teamEndlessRewardRemainTip': 'Пространственные ключи используются для получения (не открытия) сундуков Круга жизни. Осталось на этой неделе: %d',
 'teamEndlessWeekFameRewardFormula': 90304,
 'waitingTimeout': 60}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
