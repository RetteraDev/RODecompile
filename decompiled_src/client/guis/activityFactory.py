#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityFactory.o
from gamestrings import gameStrings
import random
import types
import BigWorld
import formula
import gameglobal
import gametypes
import uiConst
import const
import gamelog
import utils
import uiUtils
import clientUtils
from gameclass import Singleton
from Scaleform import GfxValue
from ui import gbk2unicode
from gamestrings import gameStrings
from callbackHelper import Functor
from data import activity_basic_data as ABD
from data import special_award_data as SAD
from data import stats_target_data as STD
from data import seeker_data as SD
from data import fb_data as FD
from data import wmd_config_data as WCD
from cdata import game_msg_def_data as GMDD
EXP = 1
BIND_CASH = 2
CASH = 3
BANG_GONG = 4
FAME = 5
ACTIVE = 6
LINGSHI = 7
ICON_SHOW_LIMIT = 3
ACTIVITY = 1
DAILY = 2
WEEKLY = 3
AWARD = 4
BUTTON_FLAG_NOT_FINISHED = 1
BUTTON_FLAG_FINISHED = 2
BUTTON_FLAG_AWARDED = 3
BUTTON_FLAG_NOT_VISIBLE = 4
AWARD_ITEM_TYPE_CASH_ONLY = 1
AWARD_ITEM_TYPE_ITEM_ONLY = 2
AWARD_ITEM_TYPE_CASH_ITEM = 3
BONUS_NUM_MAP = {1: gameStrings.TEXT_ACTIVITYFACTORY_66,
 2: gameStrings.TEXT_ACTIVITYFACTORY_67,
 3: gameStrings.TEXT_ACTIVITYFACTORY_68,
 4: gameStrings.TEXT_ACTIVITYFACTORY_69,
 5: gameStrings.TEXT_ACTIVITYFACTORY_70}
ACT_SHENG_SI_CHANG_ID = 10043

class IActivityInfo(object):

    def __init__(self, id):
        self.id = id
        self.itemIndex = 0
        self.isNeedUpdate = True

    def setItemIndex(self, index):
        self.itemIndex = index

    def getItemIndex(self):
        return self.itemIndex

    def getClassName(self):
        cls = ABD.data.get(self.id, {}).get('class', (uiConst.SCHE_CLASS_LEVEL_UP,))
        if cls[0] == uiConst.SCHE_CLASS_LEVEL_UP:
            return gameStrings.TEXT_ACTIVITYFACTORY_91
        elif cls[0] == uiConst.SCHE_CLASS_EQUIP:
            return gameStrings.TEXT_ACTIVITYFACTORY_93
        elif cls[0] == uiConst.SCHE_CLASS_DUEL:
            return gameStrings.TEXT_ACTIVITYFACTORY_95
        elif cls[0] == uiConst.SCHE_CLASS_MONEY:
            return gameStrings.TEXT_ACTIVITYFACTORY_97
        elif cls[0] == uiConst.SCHE_CLASS_CHALLENGE:
            return gameStrings.TEXT_CHALLENGEPROXY_152
        elif cls[0] == uiConst.SCHE_CLASS_WEEKLY:
            return gameStrings.TEXT_ACTIVITYFACTORY_101
        elif cls[0] == uiConst.SCHE_CLASS_VP:
            return gameStrings.TEXT_GM_COMMAND_GUILD_1453
        elif cls[0] == uiConst.SCHE_CLASS_WORLD_WAR:
            return gameStrings.TEXT_CONST_5120
        else:
            return gameStrings.TEXT_ACTIVITYFACTORY_107

    def getClass(self):
        return ABD.data.get(self.id, {}).get('class', (1,))

    def getIncludeServer(self):
        return ABD.data.get(self.id, {}).get('includeServer', ())

    def getExcludeServer(self):
        return ABD.data.get(self.id, {}).get('excludeServer', ())

    def getIsHideInNoviceServer(self):
        return ABD.data.get(self.id, {}).get('isHideInNoviceServer', 0)

    def getServerConfigId(self):
        return ABD.data.get(self.id, {}).get('serverConfigId', 0)

    def getFubenAwardTimesLink(self):
        return ABD.data.get(self.id, {}).get('fubenAwardTimesLink', '')

    def getName(self):
        return ABD.data.get(self.id, {}).get('name', '')

    def getSortedId(self):
        return ABD.data.get(self.id, {}).get('sortedId', 0)

    def _queryShengSiChangStatusDesc(self):
        p = BigWorld.player()
        desc = ''
        if p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_DEFAULT:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_137
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_APPLYING:
            desc = gameStrings.TEXT_GUILDPROXY_2244
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_CONFIRMING:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_141
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_CONFIRMED:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_143
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_IN_SSC:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_145
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_WIN_STANDBY:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_147
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_WIN_FINAL:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_149
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_DISCARD:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_151
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_START:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_147
        elif p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_TIMEOUT:
            desc = gameStrings.TEXT_ACTIVITYFACTORY_155
        else:
            desc = gameStrings.TEXT_GAME_1747
        return desc

    def getDesc(self):
        desc = ABD.data.get(self.id, {}).get('desc', '')
        if self.id == ACT_SHENG_SI_CHANG_ID:
            desc += gameStrings.TEXT_ACTIVITYFACTORY_165 + "<font color = \'#FF0000\'>" + self._queryShengSiChangStatusDesc() + '</font><br>'
        return desc

    def getAEval(self, curClsType):
        starDict = ABD.data.get(self.id, {}).get('aEval', {}).get(curClsType, {})
        if isinstance(starDict, dict):
            star = 1
            for lvs, val in starDict.items():
                lv = BigWorld.player().lv
                if len(lvs) == 2 and lvs[0] <= lv and lv <= lvs[1]:
                    star = val

            return star
        else:
            return starDict

    def getTeamType(self):
        return ABD.data.get(self.id, {}).get('teamType', 1)

    def getFilterType(self):
        return ABD.data.get(self.id, {}).get('filterType', (0,))

    def getErefType(self):
        return ABD.data.get(self.id, {}).get('erefType', 5)

    def getErefId(self):
        return ABD.data.get(self.id, {}).get('erefId', ())

    def getATime(self):
        return ABD.data.get(self.id, {}).get('aTime', '')

    def getAvailableTime(self):
        startTimes = ABD.data.get(self.id, {}).get('startTimes', (utils.CRON_ANY,))
        endTimes = ABD.data.get(self.id, {}).get('endTimes', (utils.CRON_ANY,))
        return (startTimes, endTimes)

    def getDuration(self):
        duration = ABD.data.get(self.id, {}).get('duration', (utils.CRON_ANY, utils.CRON_ANY))
        return duration

    def getDayActiveTime(self):
        dayActiveTime = ABD.data.get(self.id, {}).get('dayActiveTime', (utils.CRON_ANY, utils.CRON_ANY))
        return dayActiveTime

    def getJoinActTime(self):
        return ABD.data.get(self.id, {}).get('joinActTime', (utils.CRON_ANY, utils.CRON_ANY))

    def getMinLv(self):
        return ABD.data.get(self.id, {}).get('minLv', 0)

    def getMaxLv(self):
        return ABD.data.get(self.id, {}).get('maxLv', 100)

    def getShowFlag(self):
        return ABD.data.get(self.id, {}).get('needShow', True)

    def isInvalidWeek(self):
        weekSet = ABD.data.get(self.id, {}).get('weekSet', 0)
        return utils.isInvalidWeek(weekSet)

    def getShowActSingleWithTime(self):
        return ABD.data.get(self.id, {}).get('showActSingleWithTime', 0)

    def getACPeriodCnt(self):
        return self.getPeriodCnt()

    def getPeriodCnt(self):
        return ABD.data.get(self.id, {}).get('periodCnt', 1)

    def getPeriodType(self):
        return ABD.data.get(self.id, {}).get('periodType', 1)

    def getAPlace(self):
        return ABD.data.get(self.id, {}).get('aPlace', ())

    def getIsEnableNpcFly(self):
        return ABD.data.get(self.id, {}).get('isEnableNpcFly', (0,))

    def getIsEnablePlaceFly(self):
        return ABD.data.get(self.id, {}).get('isEnablePlaceFly', (0,))

    def getRandomFlag(self):
        return ABD.data.get(self.id, {}).get('randomPlace', 0) or ABD.data.get(self.id, {}).get('randomNpc', 0)

    def getPlaceId(self):
        return ABD.data.get(self.id, {}).get('aPlaceTk', ())

    def getNPCName(self):
        npcId = ABD.data.get(self.id, {}).get('aNPC', ())
        if len(npcId) == 0:
            return ()
        else:
            npcName = []
            for nId in npcId:
                npcName.append(uiUtils.getNpcName(nId, gameStrings.TEXT_ACTIVITYFACTORY_262))

            return npcName

    def getNPCId(self):
        return ABD.data.get(self.id, {}).get('aNPCTk', ())

    def getNPCPos(self):
        aNPCTk = ABD.data.get(self.id, {}).get('aNPCTk', ())
        if type(aNPCTk) == types.IntType:
            aNPCTk = (aNPCTk,)
        npcPos = []
        for nTrack in aNPCTk:
            xpos = str(int(SD.data.get(nTrack, {}).get('xpos', 0)))
            ypos = str(int(SD.data.get(nTrack, {}).get('ypos', 0)))
            zpos = str(int(SD.data.get(nTrack, {}).get('zpos', 0)))
            posStr = ''
            posStr += '(' + xpos + gameStrings.TEXT_ACTIVITYFACTORY_280 + zpos + gameStrings.TEXT_ACTIVITYFACTORY_280 + ypos + ')'
            npcPos.append(posStr)

        return npcPos

    def getPlacePos(self):
        aPlaceTk = ABD.data.get(self.id, {}).get('aPlaceTk', ())
        if type(aPlaceTk) == types.IntType:
            aPlaceTk = (aPlaceTk,)
        placePos = []
        for pTrack in aPlaceTk:
            xpos = str(int(SD.data.get(pTrack, {}).get('xpos', 0)))
            ypos = str(int(SD.data.get(pTrack, {}).get('ypos', 0)))
            zpos = str(int(SD.data.get(pTrack, {}).get('zpos', 0)))
            posStr = ''
            posStr += '(' + xpos + gameStrings.TEXT_ACTIVITYFACTORY_280 + zpos + gameStrings.TEXT_ACTIVITYFACTORY_280 + ypos + ')'
            placePos.append(posStr)

        return placePos

    def getAwdDetail(self):
        return ABD.data.get(self.id, {}).get('aAwdDetail', ())

    def getAwdItem(self):
        return ABD.data.get(self.id, {}).get('aAwdItem', ())

    def getAwdItemType(self):
        if len(self.getAwdDetail()) > 0 and len(self.getAwdItem()) > 0:
            return AWARD_ITEM_TYPE_CASH_ITEM
        elif len(self.getAwdDetail()) > 0:
            return AWARD_ITEM_TYPE_CASH_ONLY
        else:
            return AWARD_ITEM_TYPE_ITEM_ONLY

    def getExtraCnt(self):
        return ABD.data.get(self.id, {}).get('extraCnt', -1)

    def getExtraDesc(self):
        msg = '#'
        if self.getExtraCnt() != -1:
            msg = gameStrings.TEXT_ACTIVITYFACTORY_323 % (self.getExtraCnt(), self.getExtraPoint())
        return msg

    def getBtnActionType(self):
        return ABD.data.get(self.id, {}).get('btnActionType', 0)

    def getBtnActionName(self):
        btnActionType = self.getBtnActionType()
        itemInfo = ABD.data.get(self.id, {})
        if btnActionType == gametypes.ACTIVIIY_ENTER_TYPE_DIGONG_DYD:
            cronList = ABD.data.get(self.id, {}).get('joinActTime', ())
            weekSet = ABD.data.get(self.id, {}).get('weekSet', 0)
            for crons in cronList:
                if utils.inCrontabRange(crons[0], crons[1], weekSet=weekSet):
                    if BigWorld.player().fishingActivityData.get(self.id):
                        return itemInfo.get('btnActionName2', gameStrings.TEXT_ACTIVITYFACTORY_338)
                    else:
                        return itemInfo.get('btnActionName', gameStrings.TEXT_ARENAPROXY_1034)

            return itemInfo.get('btnActionName', gameStrings.TEXT_ARENAPROXY_1034)
        if btnActionType == gametypes.ACTIVITY_ENTER_TYPE_WMD:
            if WCD.data.get('wmdRankSwitcher', 0):
                return itemInfo.get('btnActionName', gameStrings.TEXT_ACTIVITYFACTORY_345)
            else:
                return ''
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_WORLD_WAR_BATTLE:
            if not gameglobal.rds.ui.worldWar.enableWorldWarBattle:
                return ''
            elif BigWorld.player().worldWar.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                return itemInfo.get('btnActionName2', '')
            else:
                return itemInfo.get('btnActionName', '')
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_XINMO:
            if not gameglobal.rds.ui.xinmoRecord._checkCollectItemSignUp() and gameglobal.rds.ui.xinmoRecord._checkActivityTime():
                return itemInfo.get('btnActionName', gameStrings.TEXT_ACTIVITYFACTORY_359)
            else:
                return itemInfo.get('btnActionName2', gameStrings.TEXT_ACTIVITYFACTORY_361)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_CRYSTAL_DEFENCE:
            isSignUp = False
            if hasattr(BigWorld.player(), 'handInItemActSignUpData'):
                isSignUp = BigWorld.player().handInItemActSignUpData.get(self.id, False)
            if isSignUp and gameglobal.rds.ui.crystalDefenceMain.checkActivityTime(self.id):
                return itemInfo.get('btnActionName2', gameStrings.ACT_BTN_NAME_2)
            else:
                return itemInfo.get('btnActionName', gameStrings.ACT_BTN_NAME_1)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_MONSTER_CLAN_WAR:
            if gameglobal.rds.ui.monsterClanWarActivity.checkInMonsterClan():
                return itemInfo.get('btnActionName', gameStrings.TEXT_ACTIVITYFACTORY_375)
            else:
                return itemInfo.get('btnActionName2', gameStrings.TEXT_ACTIVITYFACTORY_377)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_TEAM_SSC:
            if BigWorld.player().teamShengSiChangStatus == 0:
                return itemInfo.get('btnActionName', gameStrings.TEXT_ACTIVITYFACTORY_381)
            else:
                return itemInfo.get('btnActionName2', gameStrings.TEXT_GUILDPROXY_2244)
        else:
            return itemInfo.get('btnActionName', '')

    def getBtnActionArg(self):
        return ABD.data.get(self.id, {}).get('btnActionArg', 0)

    def getTabDesc(self):
        pass

    def getExtraPoint(self):
        return ABD.data.get(self.id, {}).get('extraPoint', 0)

    def getAccuAct(self):
        return ABD.data.get(self.id, {}).get('accuAct', ())

    def getSumAccuAct(self):
        accuAct = 0
        for value in self.getAccuAct():
            accuAct += value

        return accuAct

    def getBgId(self):
        return ABD.data.get(self.id, {}).get('bgId', '10001')

    def getCnt(self):
        return 0

    def getACCnt(self):
        return self.getCnt()

    def getIsEnableGroupMatch(self):
        return ABD.data.get(self.id, {}).get('isEnableGroupMatch', 0)

    def getVisibleCamp(self):
        return ABD.data.get(self.id, {}).get('visibleCamp', 0)

    def checkCanGroupMatch(self):
        p = BigWorld.player()
        if p.lv < self.getMinLv() or p.lv > self.getMaxLv():
            return False
        return uiUtils.checkIsCanGroupMatch(self.getIsEnableGroupMatch())

    def _setItemDetail(self, item):
        ar = gameglobal.rds.ui.movie.CreateArray()
        ar.SetElement(0, GfxValue(item[0]))
        ar.SetElement(1, GfxValue(item[1]))
        ar.SetElement(2, GfxValue(gbk2unicode(item[2])))
        return ar

    def getRealAccuAct(self, i):
        if len(self.getAccuAct()) == 0:
            return ''
        return self.getAccuAct()[i]

    def getTabData(self):
        ret = gameglobal.rds.ui.movie.CreateArray()
        obj = gameglobal.rds.ui.movie.CreateObject()
        for item in self.getAwdDetail():
            bonusType = item[0]
            bonusNum = BONUS_NUM_MAP[item[1]]
            if bonusType == EXP:
                obj.SetMember('exp', GfxValue(gbk2unicode(bonusNum)))
                obj.SetMember('expDesc', GfxValue(gbk2unicode(item[2])))
            elif bonusType == BIND_CASH:
                obj.SetMember('bindCash', GfxValue(gbk2unicode(bonusNum)))
                obj.SetMember('bindCashDesc', GfxValue(gbk2unicode(item[2])))
            elif bonusType == CASH:
                obj.SetMember('cash', GfxValue(gbk2unicode(bonusNum)))
                obj.SetMember('cashDesc', GfxValue(gbk2unicode(item[2])))
            elif bonusType == BANG_GONG:
                obj.SetMember('bangGong', GfxValue(gbk2unicode(bonusNum)))
            elif bonusType == FAME:
                obj.SetMember('fame', GfxValue(gbk2unicode(item[1])))

        icons = gameglobal.rds.ui.movie.CreateArray()
        for index, icon in enumerate(self.getAwdItem()):
            icons.SetElement(index, uiUtils.genIconsAr(icon))

        obj.SetMember('icons', icons)
        obj.SetMember('awardType', GfxValue(self.getAwdItemType()))
        obj.SetMember('desc', GfxValue(''))
        obj.SetMember('accuAct', GfxValue(self.getRealAccuAct(0)))
        obj.SetMember('btnFlag', GfxValue(BUTTON_FLAG_NOT_VISIBLE))
        ret.SetElement(0, obj)
        return ret

    def randomIndexList(self):
        length = len(self.getNPCName()) if len(self.getNPCName()) > 0 else len(self.getAPlace())
        if len == 0:
            return []
        seqList = [ i for i in xrange(length) ]
        if self.getRandomFlag():
            random.shuffle(seqList)
        self.indexList = seqList

    def getShowInJunzi(self):
        return ABD.data.get(self.id, {}).get('showInJunzi', 0)

    def getShowInZhanxun(self):
        return ABD.data.get(self.id, {}).get('showInZhanxun', 0)

    def getShowInQumo(self):
        erefId = self.getErefId()
        if not len(erefId):
            return 0
        nowErefId = erefId[0]
        item = STD.data.get(nowErefId, {})
        return item.get('rewardQumo', 0)

    def getIndexList(self):
        if hasattr(self, 'indexList'):
            return self.indexList
        else:
            return []

    def getItemDetail(self, weekReq):
        obj = gameglobal.rds.ui.movie.CreateObject()
        obj.SetMember('erefType', GfxValue(self.getErefType()))
        obj.SetMember('sTitle', GfxValue(gbk2unicode(self.getName())))
        obj.SetMember('sLevel', GfxValue(str(self.getMinLv()) + '-' + str(self.getMaxLv())))
        cntStr = ''
        if self.getPeriodCnt() == 0:
            obj.SetMember('periodCnt', GfxValue('#'))
        elif weekReq < uiUtils.getWeekDay():
            obj.SetMember('periodCnt', GfxValue(cntStr + '-/-'))
        elif weekReq == uiUtils.getWeekDay():
            obj.SetMember('periodCnt', GfxValue(cntStr + str(self.getCnt()) + '/' + str(self.getPeriodCnt())))
        else:
            obj.SetMember('periodCnt', GfxValue(cntStr + '0' + '/' + str(self.getPeriodCnt())))
        obj.SetMember('sDesc', GfxValue(gbk2unicode(self.getDesc())))
        self.randomIndexList()
        indexList = self.getIndexList()
        if len(self.getNPCName()) == 0:
            obj.SetMember('sNPC', GfxValue(gbk2unicode('#')))
        else:
            npcArray = []
            for i in xrange(len(self.getNPCName())):
                index = indexList[i]
                seekId = self.getNPCId()[index]
                npcArray.append({'chunkName': uiUtils.getChunkNameBySeekId(seekId),
                 'sNPCName': self.getNPCName()[index],
                 'sNPCPos': self.getNPCPos()[index],
                 'isEnableNpcFly': self.getIsEnableNpcFly()[index]})

            obj.SetMember('sNPC', uiUtils.array2GfxAarry(npcArray, True))
        if len(self.getAPlace()) == 0:
            obj.SetMember('sPlace', GfxValue(gbk2unicode('#')))
        else:
            placeArray = []
            for i in xrange(len(self.getAPlace())):
                index = indexList[i]
                seekId = self.getPlaceId()[index]
                placeArray.append({'chunkName': uiUtils.getChunkNameBySeekId(seekId),
                 'sPlaceName': self.getAPlace()[index],
                 'sPlacePos': self.getPlacePos()[index],
                 'isEnablePlaceFly': self.getIsEnablePlaceFly()[index]})

            obj.SetMember('sPlace', uiUtils.array2GfxAarry(placeArray, True))
        obj.SetMember('sExtra', GfxValue(gbk2unicode(self.getExtraDesc())))
        obj.SetMember('fubenAwardTimesLink', GfxValue(gbk2unicode(self.getFubenAwardTimesLink())))
        obj.SetMember('sTab', self.getTabData())
        obj.SetMember('activePoints', GfxValue(self.getRealAccuAct(0)))
        obj.SetMember('bgPath', GfxValue('scheduleBg/' + self.getBgId() + '.dds'))
        obj.SetMember('id', GfxValue(self.id))
        obj.SetMember('canGroupMatch', GfxValue(self.checkCanGroupMatch()))
        obj.SetMember('btnActionType', GfxValue(self.getBtnActionType()))
        actionName = self.getBtnActionName()
        if actionName:
            obj.SetMember('btnActionLabelName', GfxValue(gbk2unicode(self.getBtnActionName())))
        startCrons, endCrons = self.getAvailableTime()
        startCrons = startCrons or (utils.CRON_ANY,)
        endCrons = endCrons or (utils.CRON_ANY,)
        activityStart = False
        cronList = ABD.data.get(self.id, {}).get('joinActTime')
        weekSet = ABD.data.get(self.id, {}).get('weekSet', 0)
        if not cronList:
            for i in xrange(len(startCrons)):
                if utils.inCrontabRange(startCrons[i], endCrons[i], weekSet=weekSet):
                    activityStart = True
                    break

        else:
            for crons in cronList:
                if utils.inCrontabRange(crons[0], crons[1], weekSet=weekSet):
                    activityStart = True

        obj.SetMember('activityStart', GfxValue(activityStart))
        obj.SetMember('wmdRankSwitcher', GfxValue(WCD.data.get('wmdRankSwitcher', 0)))
        return obj

    def canBeTrack(self):
        return True

    def canGetReward(self):
        return False

    def isFinish(self):
        gamelog.debug('hjx debug schedule#isFinish:', self.getPeriodCnt(), self.getCnt())
        if self.getCnt() >= self.getPeriodCnt():
            return True
        else:
            return False

    def getItemIcons(self):
        ret = gameglobal.rds.ui.movie.CreateObject()
        for item in self.getAwdDetail():
            bonusType = item[0]
            bonusNum = item[1]
            isShow = bonusNum > ICON_SHOW_LIMIT
            if bonusType == EXP:
                ret.SetMember('exp', GfxValue(isShow))
            elif bonusType == BIND_CASH:
                ret.SetMember('bindCash', GfxValue(isShow))
            elif bonusType == CASH:
                ret.SetMember('cash', GfxValue(isShow))
            elif bonusType == BANG_GONG:
                ret.SetMember('bangGong', GfxValue(isShow))
            elif bonusType == FAME:
                ret.SetMember('fame', GfxValue(isShow))
            elif bonusType == ACTIVE:
                ret.SetMember('active', GfxValue(isShow))

        return ret

    def onGroupMatchClick(self):
        p = BigWorld.player()
        if not uiUtils.groupMatchApplyCheck():
            return
        if p.isInGroup():
            p.showGameMsg(GMDD.data.GROUP_MATCH_FAILED_NOT_TEAM, ())
            return
        if p.isInTeam():
            p.cell.applyGroupMatchOfTeam(gametypes.GROUP_MATCH_CLASS_ACT, gametypes.GROUP_MATCH_TYPE_RANDOM, (uiUtils.calcGroupMatchId(self.id),))
        else:
            p.cell.applyGroupMatchOfPerson(gametypes.GROUP_MATCH_CLASS_ACT, gametypes.GROUP_MATCH_TYPE_RANDOM, (uiUtils.calcGroupMatchId(self.id),))

    def onActionBtnClick(self):
        btnActionType = self.getBtnActionType()
        p = BigWorld.player()
        if btnActionType == gametypes.ACTIVITY_ENTER_TYPE_DIGONG_SXY:
            if formula.spaceInMultiLine(p.spaceNo):
                p.showGameMsg(GMDD.data.SWITCH_LINE_FAILED_FROM_ACTIVITY_PANEL, ())
                return
            commonMlgNo, _ = self.getBtnActionArg()
            gameglobal.rds.ui.diGong.showFromActivity(self.id, commonMlgNo)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_DIGONG_YMF:
            if formula.spaceInMultiLine(p.spaceNo):
                p.showGameMsg(GMDD.data.SWITCH_LINE_FAILED_FROM_ACTIVITY_PANEL, ())
                return
            if p.pvpTempCamp == const.CAMP_PVP_TEMP_CAMP_NONE:
                p.showGameMsg(GMDD.data.DIGONG_BATTLE_FIELD_ENTER_FAILED_NO_CAMP, ())
                return
            commonMlgNo, _ = self.getBtnActionArg()
            gameglobal.rds.ui.diGong.showFromActivity(self.id, commonMlgNo)
        elif btnActionType == gametypes.ACTIVIIY_ENTER_TYPE_DIGONG_DYD:
            cronList = ABD.data.get(self.id, {}).get('joinActTime', ())
            weekSet = ABD.data.get(self.id, {}).get('weekSet', 0)
            for crons in cronList:
                if utils.inCrontabRange(crons[0], crons[1], weekSet=weekSet):
                    if not BigWorld.player().fishingActivityData.get(self.id):
                        BigWorld.player().cell.joinFishingActivity(self.id)
                        return

            if formula.spaceInMultiLine(p.spaceNo):
                p.showGameMsg(GMDD.data.SWITCH_LINE_FAILED_FROM_ACTIVITY_PANEL, ())
                return
            commonMlgNo, _ = self.getBtnActionArg()
            gameglobal.rds.ui.diGong.showFromActivity(self.id, commonMlgNo)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_DUEL_SSC:
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
                self.applyShengSiChang()
            else:
                p.cell.onApplyShengSiChang()
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_WMD:
            gameglobal.rds.ui.wmdRankList.openShangjinRank()
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_WORLD_WAR_BATTLE:
            if p.wbApplyHireHostId:
                p.cell.cancelWorldWarBattleHireApply()
            elif p._getWBHireHostId():
                p.showGameMsg(GMDD.data.WB_HIRE_APPLY_ALREADY_HIRED, ())
                return
            p.cell.enterWorldWarEvent(gametypes.WORLD_WAR_TYPE_BATTLE)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_XINMO:
            if not gameglobal.rds.ui.xinmoRecord._checkCollectItemSignUp() and gameglobal.rds.ui.xinmoRecord._checkActivityTime():
                BigWorld.player().base.signupCollectItem(10234)
            gameglobal.rds.ui.xinmoRecord.show()
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_CRYSTAL_DEFENCE:
            actID = self.id
            HIID_ID, _ = self.getBtnActionArg()
            gameglobal.rds.ui.crystalDefenceMain.signUpOrShowCrystalMain(actID, HIID_ID)
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_MONSTER_CLAN_WAR:
            gameglobal.rds.ui.monsterClanWarActivity.show()
        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_TEAM_SSC:
            if p.teamShengSiChangStatus != 0:
                p.showGameMsg(GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_ALREADY_IN, ())
            elif gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
                self.applyTeamShengSiChang()
            else:
                self.confirmApplyTeamShengSiChang()

    def applyShengSiChang(self):
        p = BigWorld.player()
        msg = gameStrings.SSC_APPLY_CONFIRM_TEXT
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.onApplyShengSiChang, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_GIVEUP)

    def applyTeamShengSiChang(self):
        msg = gameStrings.SSC_TEAM_APPLY_CONFIRM_TEXT
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmApplyTeamShengSiChang, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_GIVEUP)

    def confirmApplyTeamShengSiChang(self):
        p = BigWorld.player()
        if p.isInTeamOrGroup():
            memberCnt = len(p.members)
            if memberCnt > const.TEAM_SHENG_SI_CHANG_MAX_NUM:
                p.showGameMsg(GMDD.data.TEAM_SSC_TOOMANY_PEOPLE, ())
            elif memberCnt == const.TEAM_SHENG_SI_CHANG_MAX_NUM:
                msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_WILL_INVITE_NOTIFY, 'invite team member?')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=p.cell.applyTeamShengSiChangTeam)
            else:
                p.showGameMsg(GMDD.data.TEAM_SSC_ONLYONE_PEOPLE_INTEAM, ())
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_ONLYONE_PEOPLE, 'only one')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=p.cell.applyTeamShengSiChangSingle)


class ActLoopQeustInfo(IActivityInfo):

    def __init__(self, id):
        super(ActLoopQeustInfo, self).__init__(id)
        self.erefId = self.getErefId()

    def getCnt(self):
        p = BigWorld.player()
        cnt = 0
        for value in self.erefId:
            if p.questLoopInfo.has_key(value):
                cnt += p.questLoopInfo[value].loopCnt

        return cnt


class ActFubenInfo(IActivityInfo):

    def __init__(self, id):
        super(ActFubenInfo, self).__init__(id)
        self.erefId = self.getErefId()
        self.fbInfo = {}
        for fbNo in self.erefId:
            self.fbInfo[fbNo] = FD.data.get(fbNo, {})

    def getCurEnterTimes(self, fbNo):
        p = BigWorld.player()
        fbs = []
        fbs.extend(FD.data.get(fbNo, {}).get('shareCDFbs', ()))
        if fbNo not in fbs:
            fbs.append(fbNo)
        cnt = 0
        for fb in set(fbs):
            key = '_fbEnterTimes%d' % fb
            if hasattr(p, 'statsInfo') and p.statsInfo.has_key(key):
                cnt += p.statsInfo[key]

        return cnt

    def getCanEnterTimes(self, fbNo):
        p = BigWorld.player()
        shareCDFbs = self.fbInfo[fbNo].get('shareCDFbs', ())
        sCnt = self.getCurEnterTimes(fbNo)
        for sFbNo in shareCDFbs:
            key = '_fbEnterTimes%d' % sFbNo
            if hasattr(p, 'statsInfo') and p.statsInfo.has_key(key):
                sCnt += p.statsInfo[key]

        return sCnt

    def getPeriodCnt(self):
        return 0

    def getACPeriodCnt(self):
        cnt = 0
        for fbNo in self.erefId:
            cnt += self.getAllEnterTimes(fbNo)

        return cnt

    def getCnt(self):
        return 0

    def getACCnt(self):
        cnt = 0
        for fbNo in self.erefId:
            cnt += self.getFinishCnt(fbNo)

        return cnt

    def getSumAccuAct(self):
        accuAct = 0
        for index, value in enumerate(self.getAccuAct()):
            cnt = self.getAllEnterTimes(self.erefId[index])
            accuAct += value * cnt

        return accuAct

    def getAllEnterTimes(self, fbNo):
        timesLimit = self.fbInfo[fbNo].get('timesLimit', 0)
        return timesLimit

    def getFinishCnt(self, fbNo):
        p = BigWorld.player()
        key = '_fbConquerTimes%d' % fbNo
        if hasattr(p, 'statsInfo') and p.statsInfo.has_key(key):
            return p.statsInfo[key]
        return 0

    def getAwdDetails(self, fbNo):
        aAwdDetail = self.fbInfo[fbNo].get('aAwdDetail', ())
        return aAwdDetail

    def getAwdItemType(self, fbNo):
        dropItems = self.fbInfo[fbNo].get('dropItems', ())
        aAwdDetail = self.fbInfo[fbNo].get('aAwdDetail', ())
        if len(dropItems) > 0 and (len(aAwdDetail) > 0 or len(self.getAccuAct()) > 0):
            return AWARD_ITEM_TYPE_CASH_ITEM
        elif len(aAwdDetail) > 0:
            return AWARD_ITEM_TYPE_CASH_ONLY
        else:
            return AWARD_ITEM_TYPE_ITEM_ONLY

    def getTabData(self):
        p = BigWorld.player()
        ret = gameglobal.rds.ui.movie.CreateArray()
        for i, value in enumerate(self.erefId):
            gamelog.debug('hjx debug schedule#ActStatInfo#getTabData:', self.id, value, p.isStatsFinish(self.id, value))
            obj = gameglobal.rds.ui.movie.CreateObject()
            item = self.fbInfo[value]
            icons = gameglobal.rds.ui.movie.CreateArray()
            dropItems = item.get('dropItems', ())
            for j, itemId in enumerate(dropItems):
                icons.SetElement(j, uiUtils.genIconsAr((itemId, 1)))

            obj.SetMember('icons', icons)
            obj.SetMember('awardType', GfxValue(self.getAwdItemType(value)))
            allEnterTimes = self.getAllEnterTimes(value)
            if allEnterTimes == 0:
                allEnterTimes = '-'
            obj.SetMember('fbName', GfxValue(gbk2unicode(formula.getFbDetailName(value))))
            obj.SetMember('enterCnt', GfxValue(str(self.getCurEnterTimes(value)) + '/' + str(allEnterTimes)))
            obj.SetMember('finishCnt', GfxValue(self.getFinishCnt(value)))
            obj.SetMember('accuAct', GfxValue(self.getRealAccuAct(i)))
            for item in self.getAwdDetails(value):
                bonusType = item[0]
                bonusNum = BONUS_NUM_MAP[item[1]]
                if bonusType == EXP:
                    obj.SetMember('exp', GfxValue(gbk2unicode(bonusNum)))
                    obj.SetMember('expDesc', GfxValue(gbk2unicode(item[2])))
                elif bonusType == BIND_CASH:
                    obj.SetMember('bindCash', GfxValue(gbk2unicode(bonusNum)))
                    obj.SetMember('bindCashDesc', GfxValue(gbk2unicode(item[2])))
                elif bonusType == CASH:
                    obj.SetMember('cash', GfxValue(gbk2unicode(bonusNum)))
                    obj.SetMember('cashDesc', GfxValue(gbk2unicode(item[2])))
                elif bonusType == BANG_GONG:
                    obj.SetMember('bangGong', GfxValue(gbk2unicode(bonusNum)))
                elif bonusType == FAME:
                    obj.SetMember('fame', GfxValue(gbk2unicode(item[1])))
                elif bonusType == LINGSHI:
                    obj.SetMember('lingshi', GfxValue(gbk2unicode(bonusNum)))

            ret.SetElement(i, obj)

        return ret

    def onGroupMatchClick(self):
        gameglobal.rds.ui.fubenLogin.selectedFb = self.getErefId()[0]
        gameglobal.rds.ui.fubenLogin.showFbGroupMatch()

    def checkCanGroupMatch(self):
        return uiUtils.checkFbGroupMatchCondition(self.getErefId()[0]) and uiUtils.checkIsCanGroupMatch(self.getIsEnableGroupMatch())


class ActStatInfo(IActivityInfo):

    def __init__(self, id):
        super(ActStatInfo, self).__init__(id)
        self.erefId = self.getErefId()

    def getStatsInfoValue(self, key):
        p = BigWorld.player()
        if hasattr(p, 'statsInfo') and p.statsInfo.has_key(key):
            return p.statsInfo[key]
        return 0

    def getCnt(self):
        cnt = 0
        p = BigWorld.player()
        for value in self.erefId:
            if hasattr(p, 'statsTargets') and p.statsTargets.has_key(value) and p.statsTargets[value].done:
                cnt += 1

        return cnt

    def getTabData(self):
        p = BigWorld.player()
        ret = gameglobal.rds.ui.movie.CreateArray()
        for i, value in enumerate(self.erefId):
            gamelog.debug('hjx debug schedule#ActStatInfo#getTabData:', self.id, value, p.isStatsFinish(self.id, value))
            obj = gameglobal.rds.ui.movie.CreateObject()
            item = STD.data.get(value, {})
            if item['type'] != gametypes.STATS_SUBTYPE_ACTIVITY:
                continue
            icons = gameglobal.rds.ui.movie.CreateArray()
            bonusId = item.get('bonusId', 0)
            itemBonus = clientUtils.genItemBonus(bonusId)
            for j, icon in enumerate(itemBonus):
                icons.SetElement(j, uiUtils.genIconsAr(icon))

            obj.SetMember('icons', icons)
            obj.SetMember('awardType', GfxValue(self.getAwdItemType(item)))
            if item.get('needFormat', 1):
                actProperty = item.get('property', '')
                actDesc = item.get('desc', '%d/0') % self.getStatsInfoValue(actProperty)
            else:
                actDesc = item.get('desc', '')
            obj.SetMember('desc', GfxValue(gbk2unicode(actDesc)))
            obj.SetMember('accuAct', GfxValue(self.getRealAccuAct(i)))
            obj.SetMember('cash', GfxValue(item.get('cashBonus', 0)))
            obj.SetMember('exp', GfxValue(item.get('expBonus', 0)))
            obj.SetMember('bindCash', GfxValue(0))
            obj.SetMember('bangGong', GfxValue(0))
            obj.SetMember('btnFlag', GfxValue(self.getBtnFlag(value)))
            ret.SetElement(i, obj)

        return ret

    def getAwdItemType(self, statsValue):
        if (statsValue.has_key('cashBonus') or statsValue.has_key('expBonus') or len(self.getAccuAct()) > 0) and statsValue.has_key('itemBonus'):
            return AWARD_ITEM_TYPE_CASH_ITEM
        elif statsValue.has_key('cashBonus') or statsValue.has_key('expBonus') or len(self.getAccuAct()) > 0:
            return AWARD_ITEM_TYPE_CASH_ONLY
        else:
            return AWARD_ITEM_TYPE_ITEM_ONLY

    def getBtnFlag(self, erefId):
        p = BigWorld.player()
        if p.isStatsAwarded(erefId):
            return BUTTON_FLAG_AWARDED
        elif p.isStatsFinish(self.id, erefId):
            return BUTTON_FLAG_FINISHED
        else:
            return BUTTON_FLAG_NOT_FINISHED

    def canGetReward(self):
        p = BigWorld.player()
        isGetReward = False
        for value in self.erefId:
            if p.isStatsFinish(self.id, value) and not p.isStatsAwarded(value):
                isGetReward = True
                break

        return isGetReward


class ActSpecialAwdInfo(IActivityInfo):

    def __init__(self, id):
        super(ActSpecialAwdInfo, self).__init__(id)
        self.erefId = self.getErefId()

    def getCnt(self):
        p = BigWorld.player()
        for value in self.erefId:
            awardType = 0
            itemInfo = SAD.data.get(value, None)
            if itemInfo:
                awardType = itemInfo.get('type', 0)
                break

        if not p.specialRewardInfo.has_key(awardType):
            return 0
        else:
            return len(p.specialRewardInfo[awardType])

    def getExtraDesc(self):
        return ''

    def _getItemData(self, tValue):
        ret = gameglobal.rds.ui.movie.CreateArray()
        for i, value in enumerate(self.erefId):
            gamelog.debug('hjx debug schedule#ActSpecialAwdInfo#_getItemData', value)
            obj = gameglobal.rds.ui.movie.CreateObject()
            item = SAD.data.get(value, {})
            icons = gameglobal.rds.ui.movie.CreateArray()
            for j, icon in enumerate(item.get('itemBonus', ())):
                icons.SetElement(j, uiUtils.genIconsAr(icon))

            obj.SetMember('icons', icons)
            obj.SetMember('desc', GfxValue(gbk2unicode(item.get('desc', ''))))
            obj.SetMember('id', GfxValue(value))
            obj.SetMember('activity', GfxValue(item.get('value', 0)))
            obj.SetMember('btnFlag', GfxValue(self.getBtnFlag(value)))
            ret.SetElement(i, obj)

        return ret

    def getBtnFlag(self, erefId):
        p = BigWorld.player()
        if p.isSpAwdRewarded(erefId):
            return BUTTON_FLAG_AWARDED
        elif p.isSpAwdFinish(erefId):
            return BUTTON_FLAG_FINISHED
        else:
            return BUTTON_FLAG_NOT_FINISHED

    def _getSpecialAwardType(self):
        if len(self.erefId) == 0:
            return 1
        item = SAD.data.get(self.erefId[0], {})
        return item.get('type', 1)

    def getItemDetail(self, weekReq):
        p = BigWorld.player()
        saType = self._getSpecialAwardType()
        obj = gameglobal.rds.ui.movie.CreateObject()
        obj.SetMember('erefType', GfxValue(self.getErefType()))
        if saType == gametypes.SPECIAL_AWARD_DAILYTIME:
            obj.SetMember('nowTime', GfxValue(p.getLoginSecondOfToday()))
            obj.SetMember('typeDesc', GfxValue(gbk2unicode(gameStrings.TEXT_ACTIVITYFACTORY_1096)))
            tValue = p.getLoginHourOfToday()
        elif saType == gametypes.SPECIAL_AWARD_SEQLOGIN:
            obj.SetMember('nowTime', GfxValue(p.getDeltaTime()))
            obj.SetMember('typeDesc', GfxValue(gbk2unicode(gameStrings.TEXT_ACTIVITYFACTORY_1100)))
            tValue = p.getDeltaTime()
        obj.SetMember('item', self._getItemData(tValue))
        obj.SetMember('activePoints', GfxValue(self.getRealAccuAct(0)))
        obj.SetMember('type', GfxValue(saType))
        obj.SetMember('bgPath', GfxValue('scheduleBg/' + self.getBgId() + '.dds'))
        obj.SetMember('canGroupMatch', GfxValue(self.checkCanGroupMatch()))
        return obj

    def canBeTrack(self):
        return False

    def canGetReward(self):
        p = BigWorld.player()
        isGetReward = False
        for value in self.erefId:
            if p.isSpAwdFinish(value) and not p.isSpAwdRewarded(value):
                isGetReward = True
                break

        return isGetReward


class YaBiaoInfo(IActivityInfo):

    def __init__(self, id):
        super(YaBiaoInfo, self).__init__(id)

    def getCnt(self):
        return BigWorld.player().yabiaoCnt


class ActFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.resetActIns()
        self.createActIns()

    def __createIns(self, id, erefType):
        if erefType == uiConst.ACT_LOOP_QUEST:
            return ActLoopQeustInfo(id)
        elif erefType == uiConst.ACT_STAT:
            return ActStatInfo(id)
        elif erefType == uiConst.ACT_SPECIAL_AWD:
            return ActSpecialAwdInfo(id)
        elif erefType == uiConst.ACT_FUBEN:
            return ActFubenInfo(id)
        elif erefType == uiConst.ACT_YABIAO:
            return YaBiaoInfo(id)
        else:
            return IActivityInfo(id)

    def createActIns(self):
        for key, value in ABD.data.items():
            try:
                self.actIns[key] = self.__createIns(key, value['erefType'])
            except:
                gamelog.error('hjx ActFactory error:', key, value)
                self.actIns[key] = None

    def resetActIns(self):
        self.actIns = {}

    def resetUpdateAttr(self):
        for ins in self.actIns.values():
            ins.isNeedUpdate = True


def getInstance():
    return ActFactory.getInstance()
