#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankCommonUtils.o
from gamestrings import gameStrings
import time
import BigWorld
import gametypes
import clientUtils
import utils
import const
import copy
import gameglobal
import uiConst
from gameStrings import gameStrings
from cdata import top_reward_data as TRD
from data import school_data as SD
from data import title_data as TD
from data import rank_common_format_data as RCFD
from data import region_server_config_data as RSCD
from data import mail_template_data as MTD
import gamelog
import spriteChallengeHelper
from callbackHelper import Functor
from helpers import tournament
RANKCOMMON_KEYINDEX_LEVEL = 0
RANKCOMMON_KEYINDEX_SCHOOL = 1
RANKCOMMON_KEYINDEX_ROPDOWNKEY = 2

def getRankDataByConfig(config, datalist, myInfo, sortRule, serverKey):
    p = BigWorld.player()
    keyDict = {}
    if serverKey:
        keys = serverKey.split('_')
        if config.get('lvint', ()) and keys and len(keys) >= 2:
            keyDict['level'] = keys.pop(0) + '_' + keys.pop(0)
        if config.get('schoolFiter', 0) and keys:
            try:
                keyDict['school'] = int(keys.pop(0))
            except:
                keyDict['school'] = 0

        if config.get('customDropdown', 0) and keys:
            keyDict['customDropdown'] = int(keys.pop(0))
        if config.get('customKey', 0) and keys:
            keyDict['customKey'] = int(keys.pop(0))
    else:
        gamelog.debug('ypc@ getRankDataByConfig error! serverKey is None!')
    if config.get('isSeason', 0):
        datalist = _getSortedCommonRankDataSeason(datalist)
        ret = _generateCommonDataSeason(config, datalist, myInfo)
    else:
        if sortRule:
            datalist = _getSortedCommonRankData(datalist, sortRule)
        ret = _generateCommonData(config, datalist, myInfo, keyDict, sortRule, serverKey=serverKey)
    ret['playerGbId'] = p.gbId
    return ret


def getRankCommonCacheKey(topId, serverKey):
    if serverKey:
        return str(int(topId)) + '_' + serverKey
    return str(int(topId))


def getCommonAwardInfo(awardKey, useDescRank = False):
    rewards = {}
    rewards['list'] = []
    p = BigWorld.player()
    awardData = TRD.data.get(awardKey, {})
    rewards['title'] = awardData[0].get('titleName', '')
    rewards['rule'] = awardData[0].get('rule', '')
    for award in awardData:
        awardtmp = {}
        titleId = award['schoolTitles'][p.school] if 'schoolTitles' in award else award.get('title', -1)
        awardtmp['title'] = TD.data.get(titleId, {})['name'] if titleId != -1 else ''
        low, high = award.get('rankRange', (1, 1))
        awardtmp['rank'] = gameStrings.COMMON_RANK_DESC % (str(low) if low == high else '%d-%d' % (low, high))
        if useDescRank:
            awardtmp['rank'] = award.get('desc', awardtmp['rank'])
        index = 0
        if 'schoolBonusIds' in award:
            bonusId = award['schoolBonusIds'].get(p.school, -1)
            if bonusId != -1:
                items = clientUtils.genItemBonus(bonusId)
                for itemId, count in items:
                    awardtmp['item%d' % index] = itemId
                    awardtmp['itemNum%d' % index] = count
                    index += 1
                    if index == 3:
                        break

        if index < 3:
            bonusId = award.get('bonusId', -1)
            if bonusId != -1:
                items = clientUtils.genItemBonus(bonusId)
                for itemId, count in items:
                    awardtmp['item%d' % index] = itemId
                    awardtmp['itemNum%d' % index] = count
                    index += 1
                    if index == 3:
                        break

        if index < 3:
            if 'mailTemplateId' in award:
                bonusId = MTD.data.get(award['mailTemplateId'], {}).get('bonusId', -1)
                if bonusId != -1:
                    items = clientUtils.genItemBonus(bonusId)
                    for itemId, count in items:
                        awardtmp['item%d' % index] = itemId
                        awardtmp['itemNum%d' % index] = count
                        index += 1
                        if index == 3:
                            break

        if index < 3:
            for i in xrange(0, 3 - index):
                awardtmp['item%d' % (i + index)] = -1

        rewards['list'].append(awardtmp)

    return rewards


def genCacheKeyAndServerKey(config, lvKey, schoolId, dropdownKey = -1, customKey = -1):
    p = BigWorld.player()
    topId = config['TopId']
    schoolFiter = config.get('schoolFiter', 0)
    lvFilter = config.get('LvFiter', '')
    customDropdown = config.get('customDropdown', ())
    customKeys = config.get('customKey', ())
    key = ''
    serverKey = ''
    if topId == gametypes.TOP_TYPE_CARD_COMBAT_SCORE:
        schoolId = 0
    if schoolFiter or lvFilter:
        if schoolFiter and lvFilter:
            key = str(int(topId)) + '_' + lvKey + '_' + str(schoolId)
        elif schoolFiter:
            key = str(int(topId)) + '_' + str(schoolId)
        elif lvFilter:
            key = str(int(topId)) + '_' + str(lvKey) + '_' + '0'
        serverKey = key[key.index('_') + 1:]
    else:
        key = str(int(topId))
    if topId == gametypes.TOP_TYPE_WING_WORLD_SEASON_CONTRI:
        serverKey = str(p.getWingWorldGroupId()) + '_' + str(p.wingWorldCamp) + '_' + str(schoolId)
        key = str(int(topId)) + '_' + serverKey
    elif topId == gametypes.TOP_TYPE_WING_WORLD_GUILD_SEASON_CONTRI:
        serverKey = str(p.getWingWorldGroupId()) + '_' + str(p.wingWorldCamp)
        key = str(int(topId)) + '_' + serverKey
    if dropdownKey != -1 and customDropdown:
        key = key + '_' + str(dropdownKey)
        serverKey = serverKey + '_' + str(dropdownKey) if serverKey else str(dropdownKey)
    if customKey != -1 and customKeys:
        key = key + '_' + str(customKey)
        serverKey = serverKey + '_' + str(customKey) if serverKey else str(customKey)
    if topId == gametypes.TOP_TYPE_CARD_COMBAT_SCORE and lvKey == '1_79':
        serverKey = 'allLv'
    if topId == gametypes.TOP_TYPE_CROSS_CLAN_WAR_SERVER_CONTRIB:
        serverKey = '0'
    elif topId == gametypes.TOP_TYPE_CLAN_WAR_EVENT:
        serverKey = '0'
    elif topId in (gametypes.TOP_TYPE_GSXY_GUILD_RANK, gametypes.TOP_TYPE_GSXY_SERVER_CONTRIB):
        serverKey = '0'
    elif topId == gametypes.TOP_TYPE_SPRITE_CHALLENGE_FRIEND:
        serverKey = serverKey[:-2]
    elif topId == gametypes.TOP_TYPE_NGT_RANK:
        serverKey = key + '_' + serverKey
    return (key, serverKey)


def _getSortedCommonRankData(dataList, sortRule):
    sortList = []
    if not sortRule or type(sortRule) is not tuple:
        sortList = []
    else:
        sortList = copy.copy(sortRule)
    return sorted(dataList, cmp=Functor(_commonRankDataCmp, sortList))


def _commonRankDataCmp(sortRule, value_a, value_b):
    for order, dataIndex in sortRule:
        if dataIndex not in value_a or dataIndex not in value_b:
            return 0
        if value_a[dataIndex] == value_b[dataIndex]:
            continue
        if value_a[dataIndex] > value_b[dataIndex]:
            if order == gametypes.TOP_UNIVERSAL_SORT_ASC:
                return 1
            return -1
        if order == gametypes.TOP_UNIVERSAL_SORT_DESC:
            return 1
        return -1

    return 0


def _getSortedCommonRankDataSeason(seasonList):
    ret = copy.deepcopy(seasonList)
    for season in ret:
        season.get(gametypes.TOP_UNIVERSAL_SEASON_TOP_DATA, []).sort(key=lambda x: x[gametypes.TOP_UNIVERSAL_SEASON_INDEX])

    ret.sort(key=lambda x: x[gametypes.TOP_UNIVERSAL_SEASON])
    return ret


def _generateCommonData(config, datalist, myInfo, keyDict = None, sortRule = None, serverKey = ''):
    ret = {}
    ret['list'] = []
    ret['topId'] = config['TopId']
    ret['myRank'] = -1
    ret['myRankIdx'] = -1
    ret['isSeason'] = 0
    if config.get('endTime', -1) == 1:
        ret['time'] = _getDeadlineTime(config['endTimeType'])
    else:
        ret['time'] = ''
    ret['lastRank'] = myInfo.get(gametypes.TOP_UNIVERSAL_LAST_WEEK_RANK, -1)
    additionData = _genAdditionDataFromServerData(config, myInfo, serverKey)
    if additionData:
        ret['addition'] = additionData
    tipText = config.get('tipText', '')
    ret['tipText'] = tipText
    rankIndex = 0
    multiDataIndex = -1
    if 'customDropdown' in config and keyDict and 'customDropdown' in keyDict:
        dropdownSelect = keyDict['customDropdown']
        ddData = config['customDropdown']
        keys = [ k for n, k in ddData ]
        multiDataIndex = keys.index(dropdownSelect) if dropdownSelect in keys else -1
    elif 'customKey' in keyDict:
        ret['customKey'] = keyDict['customKey']
        keys = [ k for n, k in config['customKey'] ]
        multiDataIndex = keys.index(keyDict['customKey']) if keyDict['customKey'] in keys else -1
        if multiDataIndex >= 0:
            ret['multiDataIndex'] = multiDataIndex
    gamelog.debug('ypc@ keyDict = ', keyDict)
    if not datalist:
        return ret
    else:
        topServerData = datalist[0]
        lastData = None
        listIdx = 0
        for serverData in datalist:
            newData = {}
            if config.get('enableParallelRank', 0):
                if not sortRule or type(sortRule) is not tuple:
                    sortRule = []
                if sortRule and lastData and _commonRankDataCmp(sortRule, lastData, serverData) == 0:
                    pass
                else:
                    rankIndex += 1
            else:
                rankIndex += 1
            newData['index'] = rankIndex
            isSelf = _isSelf(config, serverData)
            if isSelf:
                ret['myRank'] = rankIndex
                ret['myRankIdx'] = listIdx
                if not additionData:
                    ret['addition'] = _genAdditionDataFromServerData(config, serverData, serverKey)
            newData['isSelf'] = isSelf
            topSD = topServerData if rankIndex > 0 else None
            newData.update(_generateColData(config, serverData, multiDataIndex, topSD, serverKey=serverKey, rankIdx=rankIndex))
            ret['list'].append(newData)
            listIdx += 1
            lastData = serverData

        if 'addition' in config and 'addition' not in ret:
            additionConfig = config.get('addition', {})
            label = additionConfig[0]
            val = additionConfig[1]
            if type(val) is float:
                val = int(val)
            labelValue = str(myInfo.get(val, ''))
            ret['addition'] = (label, labelValue)
        return ret


def _generateCommonDataSeason(config, datalist, myInfo):
    p = BigWorld.player()
    ret = {}
    ret['topId'] = config['TopId']
    ret['list'] = []
    ret['myRank'] = -1
    if config.get('endTime', -1) == 1:
        ret['time'] = _getDeadlineTime(config['endTimeType'])
    else:
        ret['time'] = ''
    ret['addition'] = _genAdditionDataFromServerData(config, myInfo)
    tipText = config.get('tipText', '')
    ret['tipText'] = tipText
    ret['lastRank'] = myInfo.get(gametypes.TOP_UNIVERSAL_LAST_WEEK_RANK, -1)
    ret['isSeason'] = config['isSeason']
    realPlayerName = utils.getRealRoleName(p.roleName)
    for seasonData in datalist:
        season = {}
        seasonIdx = seasonData.get(gametypes.TOP_UNIVERSAL_SEASON, '')
        season['desc'] = seasonData.get(gametypes.TOP_UNIVERSAL_SEASON_DESC, '')
        seasonRank = seasonData.get(gametypes.TOP_UNIVERSAL_SEASON_TOP_DATA, [])
        rankIndex = 0
        for rankData in seasonRank:
            newData = {}
            newData['index'] = rankData.get(gametypes.TOP_UNIVERSAL_SEASON_INDEX, 0)
            rankPlayerName = rankData.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, '')
            newData['isSelf'] = utils.getRealRoleName(rankPlayerName) == realPlayerName
            newData.update(_generateColData(config, rankData, seasonKey=seasonIdx))
            season['rank%d' % rankIndex] = newData
            rankIndex += 1

        ret['list'].append(season)

    return ret


def _getDeadlineTime(format = 1):
    if format == 1:
        t = time.localtime(BigWorld.player().getServerTime())
        timeTxt = gameStrings.TEXT_FORMULA_1568 % (t.tm_year, t.tm_mon, t.tm_mday)
        return timeTxt
    else:
        t = time.localtime(BigWorld.player().getServerTime())
        timeTxt = '%d/%d/%d %02d:%02d' % (t.tm_year,
         t.tm_mon,
         t.tm_mday,
         t.tm_hour,
         t.tm_min)
        return timeTxt


def _generateColData(config, serverData, multiDataIndex = -1, topServerData = None, serverKey = '', seasonKey = '', rankIdx = 0):
    newData = {}
    index = 1
    topId = config.get('TopId', 0)
    if gametypes.TOP_UNIVERSAL_GBID in serverData:
        newData['roleGbid'] = serverData.get(gametypes.TOP_UNIVERSAL_GBID, 0)
    if gametypes.TOP_UNIVERSAL_TIP_CONTENT in serverData:
        tipContent = serverData.get(gametypes.TOP_UNIVERSAL_TIP_CONTENT, '')
        if topId not in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
            if type(tipContent) is tuple or type(tipContent) is list:
                tipContent = '\n'.join([ str(t) for t in tipContent ])
            else:
                tipContent = str(tipContent)
        if topId in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
            spriteInfo = tipContent.get('sprite', {})
            spriteDps = tipContent.get('spriteDPS', 0)
            spriteInfo['spriteDps'] = spriteDps
            gameglobal.rds.ui.rankCommon.addZmjSpriteInfo(newData.get('roleGbid'), spriteInfo)
            tipContent = {}
        newData['tipContent'] = tipContent
    if gametypes.TOP_UNIVERSAL_SPRITE_UUID in serverData:
        newData['spriteUUID'] = serverData[gametypes.TOP_UNIVERSAL_SPRITE_UUID]
    if gametypes.TOP_UNIVERSAL_SCHOOL in serverData:
        newData['roleSchool'] = serverData.get(gametypes.TOP_UNIVERSAL_SCHOOL, 0)
    generalConfigs = config.get('GeneralColConfigs', [])
    for dataIndex in generalConfigs:
        if type(dataIndex) is tuple and multiDataIndex >= 0:
            curIndex = dataIndex[multiDataIndex]
        else:
            curIndex = dataIndex
        sevIndex = RCFD.data.get(curIndex, {}).get('ServerIndex', 0)
        if sevIndex not in serverData and sevIndex not in gametypes.TOP_UNIVERSAL_CLIENT_COLS:
            continue
        val = serverData.get(sevIndex, '')
        if type(val) is float:
            val = int(val)
        if sevIndex == gametypes.TOP_UNIVERSAL_FINISH_TIME:
            if config.get('TimeType', 1) == 1:
                timeFormat = 'h:m:s'
                if topId in (gametypes.TOP_TYPE_SPRITE_CHALLENGE_HERO, gametypes.TOP_TYPE_SPRITE_CHALLENGE):
                    val = min(val, 180)
                timeStr = utils.formatTimeStr(val, timeFormat, True, 2, 2, 2)
            else:
                timeStr = val
            newData['data%d' % index] = timeStr
        elif sevIndex == gametypes.TOP_UNIVERSAL_SCHOOL:
            newData['data%d' % index] = SD.data.get(val, {}).get('name', '')
        elif sevIndex == gametypes.TOP_UNIVERSAL_SPRITE_COMBAT:
            newData['data%d' % index] = str(val)
        elif sevIndex == gametypes.TOP_UNIVERSAL_TEAM_NAME:
            newData['data%d' % index] = str(val)
        elif sevIndex == gametypes.TOP_UNIVERSAL_GUILD_ATTEND_COUNT_EX and topServerData and type(val) is int:
            topGuildNum = topServerData.get(gametypes.TOP_UNIVERSAL_GUILD_ATTEND_COUNT_EX, 0)
            if topGuildNum == 0 or val == 0:
                newData['data%d' % index] = 'f1'
            else:
                numRatio = max(min(int(float(val) / topGuildNum * 100), 100), 0)
                if numRatio in range(80, 101):
                    newData['data%d' % index] = 'f5'
                elif numRatio in range(60, 80):
                    newData['data%d' % index] = 'f4'
                elif numRatio in range(40, 60):
                    newData['data%d' % index] = 'f3'
                elif numRatio in range(20, 40):
                    newData['data%d' % index] = 'f2'
                elif numRatio in range(0, 20):
                    newData['data%d' % index] = 'f1'
                else:
                    newData['data%d' % index] = 'f1'
        elif sevIndex == gametypes.TOP_UNIVERSAL_CARD_SUIT_NAME:
            newData['data%d' % index] = str(val) if val else gameStrings.CARD_SUIT_TIP_NONE_SUIT
            newData['isCard'] = True
        elif sevIndex == gametypes.TOP_UNIVERSAL_ZMJ_DMG:
            dataStr = ''
            if val > uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD:
                dataStr = gameStrings.ZMJ_DMG_SIMPLIFY_TXT % (val / uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD,)
                newData['dmgTip%d' % index] = str(val)
            else:
                dataStr = str(val)
            newData['data%d' % index] = dataStr
        elif sevIndex == gametypes.TOP_UNIVERSAL_HOST_ID:
            if type(val) == str:
                newData['data%d' % index] = str(val)
            else:
                hostName = utils.getServerName(val)
                newData['data%d' % index] = str(hostName)
        elif sevIndex == gametypes.TOP_UNIVERSAL_SPRITE_LIST:
            roleGBId = newData.get('roleGbid', 0)
            spriteListKeyOrder = val.get('spriteListKeyOrder', [])
            if not spriteListKeyOrder:
                spriteListKeyOrder = [ key for key in val.keys() if type(key) == int ]
            spriteInfoText = ''
            for spIdx in spriteListKeyOrder:
                spriteInfo = val.get(spIdx, {})
                if spriteInfo:
                    spriteGbId = str(topId) + str(serverKey) + str(seasonKey) + str(roleGBId) + str(spIdx)
                    spriteId = spriteInfo.get(const.SPRITE_DICT_INDEX_spriteId, 0)
                    gameglobal.rds.ui.ranking.updateSpriteDetailInfo(spriteGbId, spriteInfo)
                    spriteInfoText += '[sprite.2#%s#%s@32]' % (spriteId, spriteGbId)

            newData['data%d' % index] = spriteInfoText
        elif sevIndex == gametypes.TOP_UNIVERSAL_CLIENT_TIP:
            clientVal = ''
            if topId == gametypes.TOP_TYPE_NGT_RANK:
                clientVal = getNTGGroupName(rankIdx)
            newData['data%d' % index] = str(clientVal)
        elif sevIndex == gametypes.TOP_UNIVERSAL_NGT_SCORE:
            groupId = int(serverKey[-1])
            rankText = tournament.getRankStarText(groupId, int(val))
            newData['data%d' % index] = rankText
        else:
            newData['data%d' % index] = str(val)
        index += 1

    return newData


def getNTGGroupName(rank):
    from data import guild_config_data as GCD
    NGTNRankGroupNames = GCD.data.get('NGTNRankGroupNames', ())
    for i in xrange(len(NGTNRankGroupNames)):
        start, groupName = NGTNRankGroupNames[-(i + 1)]
        if rank >= start:
            return groupName % (rank - start + 1)

    return gameStrings.WING_WORLD_NO_OWNER


def _isSelf(config, serverData):
    p = BigWorld.player()
    topId = config['TopId']
    if topId == gametypes.TOP_TYPE_DOUBLE_ARENA_SCORE:
        dArenaTeamName = getattr(p.doubleArenaTeamInfo, 'teamName', '')
        return dArenaTeamName and dArenaTeamName == serverData.get(gametypes.TOP_UNIVERSAL_TEAM_NAME, '')
    elif topId == gametypes.TOP_TYPE_CROSS_CLAN_WAR_SERVER_CONTRIB:
        hostId = serverData.get(gametypes.TOP_UNIVERSAL_HOST_ID, 0)
        return hostId and hostId == utils.getHostId()
    elif topId == gametypes.TOP_TYPE_PLAYOFFS_TEAM_COMBATSCORE:
        arenaTeamName = p.arenaPlayoffsTeam.get('teamName', '')
        return arenaTeamName and arenaTeamName == serverData.get(gametypes.TOP_UNIVERSAL_TEAM_NAME, '')
    elif topId == gametypes.TOP_TYPE_CROSS_ARENA_SCORE_PLAYOFFS:
        teamNUID = getattr(p, 'arenaScorePlayoffsTeamNUID', 0)
        return teamNUID and teamNUID == serverData.get(gametypes.TOP_UNIVERSAL_GBID, '')
    elif gametypes.TOP_UNIVERSAL_ROLE_NAME in serverData:
        realPlayerName = utils.getRealRoleName(p.roleName)
        return serverData.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, '') == realPlayerName
    elif gametypes.TOP_UNIVERSAL_COUNTRY_NAME in serverData:
        countryName = RSCD.data.get(p.getOriginHostId(), {}).get('serverName', '')
        if countryName:
            return countryName == serverData.get(gametypes.TOP_UNIVERSAL_COUNTRY_NAME, '')
        return False
    elif gametypes.TOP_UNIVERSAL_GUILD_NAME in serverData:
        return p.guildName == serverData.get(gametypes.TOP_UNIVERSAL_GUILD_NAME, '')
    else:
        return False


def _genAdditionDataFromServerData(config, serverData, serverKey = ''):
    ret = []
    additionConfig = config.get('addition', ())
    if len(additionConfig) > 0:
        if len(additionConfig) % 2 == 0:
            for i in xrange(len(additionConfig) / 2):
                label = additionConfig[i * 2]
                valIdx = int(additionConfig[i * 2 + 1])
                if valIdx in serverData:
                    val = serverData.get(valIdx, 0)
                    if type(val) is float:
                        val = int(val)
                    if serverKey and valIdx == gametypes.TOP_UNIVERSAL_NGT_SCORE:
                        groupId = int(serverKey[-1])
                        val = tournament.getRankStarText(groupId, int(val))
                    ret.extend((label, val))

        else:
            gamelog.debug('ypc@ _generateCommonData config error! topId:', config.get('topId', 0))
    return ret


def getCustomKeyByTopId(topId):
    p = BigWorld.player()
    if topId == gametypes.TOP_TYPE_WING_WAR_GUILD_CONTRIBUTE:
        return p.getWingCityId()
    if topId == gametypes.TOP_TYPE_WING_WAR_TEMP_GUILD_CONTRIBUTE:
        return p.getWingCityId()
    return -1


def getCustomDropdownKeyByTopId(topId):
    if topId in (gametypes.TOP_TYPE_WING_WORLD_SEASON_CONTRI, gametypes.TOP_TYPE_WING_WORLD_GUILD_SEASON_CONTRI):
        if gameglobal.rds.ui.wingWorldCampTrend.tempRankKey:
            return gameglobal.rds.ui.wingWorldCampTrend.tempRankKey
    return -1


def getAdditionValueLocal(topId):
    p = BigWorld.player()
    if topId == gametypes.TOP_TYPE_WING_WAR_PERSONAL_CONTRIBUTE_TOTAL:
        return getattr(p, 'wingWorldTotalContributeCache', None)
    elif topId == gametypes.TOP_TYPE_DOUBLE_ARENA_SCORE:
        doubleArenaTeamInfo = getattr(p, 'doubleArenaTeamInfo', None)
        if doubleArenaTeamInfo:
            return doubleArenaTeamInfo.statistics.score
        return 0
    elif topId == gametypes.TOP_TYPE_CROSS_ARENA_SCORE_PLAYOFFS:
        return getattr(p, 'arenaScorePlayoffsTeam', {}).get('score', {}).get('score', 0)
    else:
        return


def setRankCommonExtraInfo(config, topId, serverKey):
    if topId == gametypes.TOP_TYPE_SPRITE_CHALLENGE:
        if serverKey[-1] != '2':
            config['tipText'] = ''
        if serverKey[-1] == '3':
            config['isSeason'] = 1
            config['Newranking'] = 0
            config['Newrankingicon'] = 0
