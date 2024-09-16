#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/digong_clanwar_config_data.o
data = {'gsxyActivityCreateTime': '0 0 9 3 *',
 'gsxyCreateTime': '0 20 9 3 *',
 'gsxyEndTime': '0 21 30 3 *',
 'gsxyLvLimit': 69,
 'gsxyMLCreateTime': '50 19 30 3 *',
 'gsxyMLPrepareInterval': 600,
 'gsxyMaxMemberNum': 60,
 'gsxyRankScore': (20, 18, 15, 12, 9, 6, 5, 4, 3, 2),
 'gsxyTopEndTime': '58 20 23 3 *',
 'qualifyPostList': [1,
                     2,
                     10,
                     11],
 'qualifyPostTip': 'Это могут выполнить только Глава гильдии, Наместник, Командир и Маршал.'}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
