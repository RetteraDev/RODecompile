#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/monsterClanWarActivityProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import formula
import gameglobal
import utils
import clientUtils
import gametypes
from guis import uiConst
from guis import uiUtils
from data import activity_basic_data as ABD
from data import monster_clan_war_config_data as MCWCD
from data import bonus_data as BD
MONSTER_CLAN_WAR_START = 1
MONSTER_CLAN_WAR_END = 2
MONSTER_CLAN_WAR_PREPARE = 3

class MonsterClanWarActivityProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MonsterClanWarActivityProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetMonsterAttackData,
         'getPlayerSchool': self.onGetPlayerSchool,
         'getReward': self.onGetMonsterClanReward,
         'openRank': self.onOpenClanRank,
         'openMap': self.openClanMap,
         'getTipsData': self.onGetTipsData,
         'getRuleTip': self.onGetRuleTip,
         'getPlayerLvStr': self.onGetPlayerLvStr}
        self.mediator = None
        self.pushMed = None
        self.mySchoolIdx = 0
        self.cacheData = {}
        self.schoolId = 0
        self.activityState = 0
        self.myRank = 0
        self.clanStartTime = 0
        self.prepareTime = 0
        self.lvKey = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_RANK:
            self.mediator = mediator
        if widgetId == uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_PUSH:
            self.pushMed = mediator
            return uiUtils.dict2GfxDict(self._getActivityData(), True)

    def show(self):
        if not gameglobal.rds.configData.get('enableMonsterClanWar', False):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_RANK)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.lvKey = ''
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_RANK)

    def clearData(self):
        self.mediator = None
        self.pushMed = None
        self.mySchoolIdx = 0
        self.cacheData = {}
        self.schoolId = 0
        self.activityState = 0
        self.myRank = 0
        self.clanStartTime = 0
        self.prepareTime = 0
        self.lvKey = ''

    def onGetMonsterAttackData(self, *arg):
        self.schoolId = int(arg[3][0].GetNumber())
        self.lvKey = arg[3][1].GetString()
        if self.lvKey == '':
            self.lvKey = self._genPlayerLvStr()
        ret = self._getData()
        key = '%s_%d' % (self.lvKey, self.schoolId)
        BigWorld.player().base.getTopMonsterClanWar(self.cacheData.get(key, {}).get('ver', 0), key)
        return uiUtils.dict2GfxDict(ret, True)

    def _genPlayerLvStr(self):
        p = BigWorld.player()
        if 40 <= p.lv <= 69:
            return '40_69'
        if 70 <= p.lv <= 79:
            return '70_79'
        return '40_69'

    def updateMonsterAttackData(self, data):
        ver = data[0]
        key = data[1]
        self.myRank = data[2]
        rankData = data[3]
        if not self.cacheData.has_key(key):
            self.cacheData[key] = {}
        self.cacheData[key] = {'ver': ver,
         'data': rankData}
        if key == '%s_%d' % (self.lvKey, self.schoolId):
            self.updateView()

    def onGetPlayerLvStr(self, *arg):
        return GfxValue(self._genPlayerLvStr())

    def updateView(self):
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self._getData(), True))

    def _getData(self):
        ret = {}
        p = BigWorld.player()
        myfame = p.monsterClanWarFame
        myMonsterKill = p.monsterClanWarKillCnt
        myBossDmg = p.monsterClanWarBossDmg
        ret['myScore'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_127 % formula.getMonsterClanWarContribute(myfame, myMonsterKill, myBossDmg)
        ret['monsterKill'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_128 % myMonsterKill
        ret['combat'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_129 % myBossDmg
        key = '%s_%d' % (self.lvKey, self.schoolId)
        ret['list'] = self._genMonsterClanRankData(self.cacheData.get(key, {}).get('data', []))
        rank = self.myRank
        if rank > 0:
            ret['desc'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_134 % rank
        else:
            ret['desc'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_136
        contributionBonusId = MCWCD.data.get('contributionBonusId', 0)
        fixedBonus = BD.data.get(contributionBonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        ret['reward'] = uiUtils.getGfxItemById(itemId)
        needScore = MCWCD.data.get('rewardThreshold', 0)
        currentScore = formula.getMonsterClanWarContribute(myfame, myMonsterKill, myBossDmg)
        ret['enableReward'] = currentScore >= needScore
        ret['isRewarded'] = p.monsterClanWarRewardTime > 0
        ret['needScore'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_151 % needScore
        if self.lvKey == '':
            self.lvKey = self._genPlayerLvStr()
        awardShowList = []
        rankBonus = MCWCD.data.get('rankBonus', {}).get(self.lvKey, None)
        if rankBonus:
            for low, high, bonusId in rankBonus:
                bonus = clientUtils.genItemBonus(bonusId)
                itemId = bonus[0][0]
                bonusInfo = uiUtils.getGfxItemById(itemId)
                bonusInfo['slotName'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_162 % (low, high)
                awardShowList.append(bonusInfo)

        ret['awardShowList'] = awardShowList
        return ret

    def _genMonsterClanRankData(self, data):
        ret = []
        temp = []
        for i in xrange(len(data)):
            playerData = data[i]
            obj = {}
            obj['rank'] = i + 1
            obj['playerName'] = playerData[0]
            obj['attack'] = playerData[2]
            obj['combat'] = playerData[3]
            obj['score'] = formula.getMonsterClanWarContribute(playerData[1], playerData[2], playerData[3])
            obj['timeStamp'] = playerData[5]
            temp.append(obj)

        temp.sort(key=lambda k: k['timeStamp'], reverse=True)
        temp.sort(key=lambda k: k['score'], reverse=True)
        for i in xrange(len(temp)):
            obj = temp[i]
            obj['rank'] = i + 1
            ret.append(obj)

        return ret

    def onGetPlayerSchool(self, *arg):
        self.mySchoolIdx = BigWorld.player().realSchool
        return GfxValue(self.mySchoolIdx)

    def updateClanIcon(self):
        if not gameglobal.rds.configData.get('enableMonsterClanWar', False):
            return
        if self.pushMed:
            self.pushMed.Invoke('updateView', uiUtils.dict2GfxDict(self._getActivityData(), True))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_PUSH)

    def prepareMonsterClanActivty(self):
        if not gameglobal.rds.configData.get('enableMonsterClanWar', False):
            return
        if self.checkInMonsterClan():
            self.startMonsterClanActivity()
        else:
            self.activityState = MONSTER_CLAN_WAR_PREPARE
            self.updateClanIcon()

    def startMonsterClanActivity(self):
        if not gameglobal.rds.configData.get('enableMonsterClanWar', False):
            return
        if self.checkInMonsterClan():
            self.activityState = MONSTER_CLAN_WAR_START
            self.updateClanIcon()
        else:
            self.checkRewardState()

    def checkRewardState(self):
        p = BigWorld.player()
        if not self.checkInMonsterClan() and getattr(p, 'monsterClanWarRewardTime', 0) == 0:
            myfame = getattr(p, 'monsterClanWarFame', 0)
            myMonsterKill = getattr(p, 'monsterClanWarKillCnt', 0)
            myBossDmg = getattr(p, 'monsterClanWarBossDmg', 0)
            needScore = MCWCD.data.get('rewardThreshold', 0)
            currentScore = formula.getMonsterClanWarContribute(myfame, myMonsterKill, myBossDmg)
            if needScore <= currentScore:
                self.activityState = MONSTER_CLAN_WAR_END
                self.updateClanIcon()

    def endMonsterClanActivity(self):
        if not gameglobal.rds.configData.get('enableMonsterClanWar', False):
            return
        self.activityState = MONSTER_CLAN_WAR_END
        self.updateClanIcon()

    def onGetMonsterClanReward(self, *arg):
        BigWorld.player().cell.getMonsterClanWarAward()

    def onOpenClanRank(self, *arg):
        self.show()
        p = BigWorld.player()
        myfame = p.monsterClanWarFame
        myMonsterKill = p.monsterClanWarKillCnt
        myBossDmg = p.monsterClanWarBossDmg
        needScore = MCWCD.data.get('rewardThreshold', 0)
        currentScore = formula.getMonsterClanWarContribute(myfame, myMonsterKill, myBossDmg)
        if p.monsterClanWarRewardTime > 0 or needScore > currentScore:
            self.pushMed = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_PUSH)

    def openClanMap(self, *arg):
        gameglobal.rds.ui.zhanJu.show()

    def _getActivityData(self, *arg):
        ret = {}
        ret['activityState'] = self.activityState
        ret['tPass'] = -1
        if self.activityState == MONSTER_CLAN_WAR_PREPARE and self.prepareTime > 0:
            ret['tPass'] = self.getClanStartTime() - utils.getNow()
        elif self.activityState == MONSTER_CLAN_WAR_START and self.clanStartTime > 0:
            ret['tPass'] = utils.getNow() - self.clanStartTime
        ret['isReward'] = BigWorld.player().monsterClanWarRewardTime
        return ret

    def getClanStartTime(self):
        data = ABD.data.get(uiConst.MONSTER_CLAN_ACTIVITY_ID, {})
        startTimes = data.get('startTimes', None)
        if startTimes:
            return utils.getNextCrontabTime(startTimes[0])
        else:
            return 0

    def checkInMonsterClan(self):
        if utils.getNow() < 0:
            return False
        else:
            minLv = MCWCD.data.get('minLv', 40)
            p = BigWorld.player()
            if p.lv < minLv:
                return False
            data = ABD.data.get(uiConst.MONSTER_CLAN_ACTIVITY_ID, {})
            startTimes = data.get('startTimes', None)
            endTimes = data.get('endTimes', None)
            weekSet = data.get('weekSet', 0)
            if endTimes and startTimes:
                if utils.inCrontabRange(startTimes[0], endTimes[0], weekSet=weekSet):
                    return True
            return False

    def _getMonsterClanCountDown(self):
        if self.checkInMonsterClan():
            data = ABD.data.get(uiConst.MONSTER_CLAN_ACTIVITY_ID, {})
            now = utils.getNow()
            endTimes = data.get('endTimes', None)
            if len(endTimes) > 0:
                return utils.getNextCrontabTime(endTimes[0]) - now
        return 0

    def _getTipsData(self):
        ret = {}
        p = BigWorld.player()
        myfame = p.monsterClanWarFame
        myMonsterKill = p.monsterClanWarKillCnt
        myBossDmg = p.monsterClanWarBossDmg
        ret['score'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_127 % formula.getMonsterClanWarContribute(myfame, myMonsterKill, myBossDmg)
        ret['attack'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_128 % myMonsterKill
        ret['combat'] = gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_129 % myBossDmg
        return ret

    def onGetTipsData(self, *arg):
        ret = self._getTipsData()
        return uiUtils.dict2GfxDict(ret, True)

    def updateMonsterClanWarPushTips(self):
        if self.pushMed:
            ret = self._getTipsData()
            self.pushMed.Invoke('updateTips', uiUtils.dict2GfxDict(ret, True))

    def closeMonsterClanWarPushTips(self):
        if not self.checkInMonsterClan() and self.pushMed:
            self.pushMed = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MONSTER_CLAN_WAR_ACTIVITY_PUSH)

    def updateStartTime(self, time):
        self.clanStartTime = time
        self.updateClanIcon()

    def updatePrepareTime(self, time):
        self.prepareTime = time
        self.prepareMonsterClanActivty()

    def forceOpenMonsterClanWarPushTips(self):
        if self.pushMed:
            ret = self._getTipsData()
            self.pushMed.Invoke('forceOpenTips', uiUtils.dict2GfxDict(ret, True))

    def onGetRuleTip(self, *arg):
        ret = {}
        monsterKillTip = MCWCD.data.get('monsterKillTip', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
        bossKillTip = MCWCD.data.get('bossKillTip', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
        ret['monsterKillTip'] = monsterKillTip
        ret['bossKillTip'] = bossKillTip
        return uiUtils.dict2GfxDict(ret, True)
