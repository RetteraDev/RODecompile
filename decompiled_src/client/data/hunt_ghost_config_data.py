#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/hunt_ghost_config_data.o
data = {'BigBoxExistTime': 120,
 'HUNT_GHOST_LEFT_DESC': 'Компас',
 'HUNT_GHOST_LEFT_TIPS': 'Исследуя дух, вы можете обнаружить тысячу лепестков духовных сердец.\n %s',
 'bigGhostMaxNum': 3,
 'bigTreasureBoxIds': (1490, 1491, 1492),
 'boxTypeMaxCount': {1: 3,
                     2: 5},
 'boxTypeRate': {1: (0, 25),
                 2: (26, 1000)},
 'delayDelAnonymityTime': 180,
 'distanceGrading': (500.0, 75.0, 15.0),
 'ghostNameInMap': 'По окончанию таймера Аленький цветочек будет готов к сбору',
 'huntGhostAreaNumber': 500,
 'huntGhostEndTime': '30 19 * * 5',
 'huntGhostFindRewardBoxMinNum': 1,
 'huntGhostFlagBoxId': 1493,
 'huntGhostLastBigBoxBornTime': '15 19 * * 5',
 'huntGhostLevel': 40,
 'huntGhostMaskConsumeCash': 10000,
 'huntGhostMateDistance': 30,
 'huntGhostMateRewardDistance': 300,
 'huntGhostMaxNumber': 50,
 'huntGhostPushId': 11670,
 'huntGhostReleaseCD': 60,
 'huntGhostRewardBoxRate': 75,
 'huntGhostStartTime': '00 19 * * 5',
 'huntGhostTreasureBoxOwnGroupsMaxNum': 2,
 'openBoxMinValidTime': 2,
 'openBoxRemainMinTime': 5,
 'ownerProtectRate': 0,
 'protectBuff': (55152, 6),
 'resistBuff': (55153, 60),
 'smallGhostMaxNum': 50,
 'smallTreasureBoxIds': (1485, 1486, 1487, 1488, 1489),
 'totalRewardTimes': 5}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')