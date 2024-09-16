#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaRankAwardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
import time
import utils
import const
import formula
from uiProxy import UIProxy
from data import arena_season_data as ASD
from data import balance_arena_score_desc_data as BASDD
from data import arena_score_desc_data as ASDD
from data import bonus_data as BD
from data import bonus_set_data as BSD
from data import consumable_item_data as CID
from data import fame_data as FD
from data import item_data as ID
from cdata import font_config_data as FCD
TAB_SEASON = 0
TAB_LIFETIME = 1
AWARD_STATE_NONE = 0
AWARD_STATE_CAN = 1
AWARD_STATE_GET = 2

class ArenaRankAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaRankAwardProxy, self).__init__(uiAdapter)
        self.modelMap = {'getSeasonInfo': self.onGetSeasonInfo,
         'getLifeTimeInfo': self.onGetLifeTimeInfo,
         'confirm': self.onConfirm}
        self.mediator = None
        self.currentTabIndex = -1
        self.arenaMode = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_RANK_AWARD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ARENA_RANK_AWARD:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_RANK_AWARD)

    def reset(self):
        self.currentTabIndex = -1

    def show(self, arenaMode = 0):
        self.arenaMode = arenaMode
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_RANK_AWARD)

    def onGetSeasonInfo(self, *arg):
        self.currentTabIndex = TAB_SEASON
        self.refreshSeasonInfo()

    def refreshSeasonInfo(self):
        if self.currentTabIndex != TAB_SEASON:
            return
        if self.mediator:
            p = BigWorld.player()
            arenaInfo = p.arenaInfo
            if formula.isBalanceArenaMode(self.arenaMode):
                arenaInfo = p.arenaInfoEx
            info = {}
            info['title'] = gameStrings.TEXT_ARENARANKAWARDPROXY_73 % (time.localtime().tm_year, ASD.data.get(arenaInfo.curSeason, {}).get('SessionName', gameStrings.TEXT_ARENARANKAWARDPROXY_73_1))
            tmpASDD = ASDD.data.keys()
            if formula.isBalanceArenaMode(self.arenaMode):
                tmpASDD = BASDD.data.keys()
            tmpASDD.sort()
            scoreList = []
            for minS, maxS in tmpASDD:
                scoreInfo = self.createScoreInfo((minS, maxS))
                scoreList.append(scoreInfo)

            info['scoreList'] = scoreList
            self.mediator.Invoke('refreshSeasonInfo', uiUtils.dict2GfxDict(info, True))

    def onGetLifeTimeInfo(self, *arg):
        self.currentTabIndex = TAB_LIFETIME
        self.refreshLifeTimeInfo()

    def refreshLifeTimeInfo(self):
        if self.currentTabIndex != TAB_LIFETIME:
            return
        if self.mediator:
            p = BigWorld.player()
            arenaInfo = p.arenaInfo
            if formula.isBalanceArenaMode(self.arenaMode):
                arenaInfo = p.arenaInfoEx
            info = {}
            info['title'] = gameStrings.TEXT_ARENARANKAWARDPROXY_73 % (time.localtime().tm_year, ASD.data.get(arenaInfo.curSeason, {}).get('SessionName', gameStrings.TEXT_ARENARANKAWARDPROXY_73_1))
            tmpASDD = ASDD.data.keys()
            if formula.isBalanceArenaMode(self.arenaMode):
                tmpASDD = BASDD.data.keys()
            tmpASDD.sort()
            scoreList = []
            for minS, maxS in tmpASDD:
                scoreInfo = self.createScoreInfo((minS, maxS))
                scoreList.append(scoreInfo)

            info['scoreList'] = scoreList
            self.mediator.Invoke('refreshLifeTimeInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        duanWeiTag = int(arg[3][0].GetNumber())
        if self.currentTabIndex == TAB_SEASON:
            if formula.isBalanceArenaMode(self.arenaMode):
                BigWorld.player().cell.applyArenaDuanWeiAward(duanWeiTag, const.ARENA_MODE_TYPE_BALANCE)
            else:
                BigWorld.player().cell.applyArenaDuanWeiAward(duanWeiTag, const.ARENA_MODE_TYPE_NORMAL)
        elif formula.isBalanceArenaMode(self.arenaMode):
            BigWorld.player().cell.applyArenaDuanWeiNoResetAward(duanWeiTag, const.ARENA_MODE_TYPE_BALANCE)
        else:
            BigWorld.player().cell.applyArenaDuanWeiNoResetAward(duanWeiTag, const.ARENA_MODE_TYPE_NORMAL)

    def createScoreInfo(self, key):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        arenaAwardFlag = p.arenaAwardFlag
        arenaAwardFlagNoReset = p.arenaAwardFlagNoReset
        if formula.isBalanceArenaMode(self.arenaMode):
            arenaInfo = p.arenaInfoEx
            arenaAwardFlag = p.arenaAwardFlagEx
            arenaAwardFlagNoReset = p.arenaAwardFlagNoResetEx
        scoreInfo = {}
        baseData = ASDD.data.get(key, {})
        if formula.isBalanceArenaMode(self.arenaMode):
            baseData = BASDD.data.get(key, {})
        scoreInfo['minS'] = key[0]
        scoreInfo['maxS'] = key[1]
        duanWeiTag = baseData.get('duanWeiTag', 1)
        if self.currentTabIndex == TAB_SEASON:
            keyStr = gameStrings.TEXT_ARENARANKAWARDPROXY_147
            if arenaAwardFlag.has_key(duanWeiTag):
                awardState = AWARD_STATE_GET if arenaAwardFlag[duanWeiTag] else AWARD_STATE_CAN
            else:
                awardState = AWARD_STATE_NONE
            scoreInfo['tipsBonusList'] = self.getAwardContent(baseData.get('duanWeiAward', 0))
        else:
            keyStr = gameStrings.TEXT_ARENARANKAWARDPROXY_154
            if arenaAwardFlagNoReset.has_key(duanWeiTag):
                awardState = AWARD_STATE_GET if arenaAwardFlagNoReset[duanWeiTag] else AWARD_STATE_CAN
            else:
                awardState = AWARD_STATE_NONE
            scoreInfo['tipsBonusList'] = self.getAwardContent(baseData.get('duanWeiNoResetAward', 0))
        if awardState == AWARD_STATE_NONE:
            scoreInfo['btnVisible'] = False
            scoreInfo['awardState'] = gameStrings.TEXT_ARENARANKAWARDPROXY_163
        elif awardState == AWARD_STATE_CAN:
            scoreInfo['btnVisible'] = True
            scoreInfo['awardState'] = ''
        else:
            scoreInfo['btnVisible'] = False
            scoreInfo['awardState'] = gameStrings.TEXT_ARENARANKAWARDPROXY_169 % keyStr
        scoreInfo['duanWeiTag'] = duanWeiTag
        scoreInfo['awardLabel'] = gameStrings.TEXT_ARENARANKAWARDPROXY_172 % keyStr
        scoreInfo['tipsTitle'] = gameStrings.TEXT_ARENARANKAWARDPROXY_173 % keyStr
        nowScore = arenaInfo.arenaScore
        if nowScore >= key[0] and nowScore <= key[1]:
            scoreInfo['curFlag'] = True
            scoreInfo['onceFlag'] = False
            scoreInfo['neverFlag'] = False
        else:
            scoreInfo['curFlag'] = False
            if nowScore > key[1]:
                scoreInfo['onceFlag'] = False
                scoreInfo['neverFlag'] = False
            else:
                scoreInfo['onceFlag'] = True
                scoreInfo['neverFlag'] = True
        scoreInfo['name'] = baseData.get('desc', gameStrings.TEXT_ARENAPROXY_321)
        scoreInfo['curFrame'] = baseData.get('frameName', 'orange1')
        scoreInfo['rankRange'] = gameStrings.TEXT_ARENARANKAWARDPROXY_192 % (key[0], key[1])
        return scoreInfo

    def getAwardContent(self, awardId):
        fixedBonus = BD.data.get(awardId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        bonusItemName = ''
        for i in range(0, len(fixedBonus)):
            bonusType, bonusItemId, bonusNum = fixedBonus[i]
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                name = ID.data.get(bonusItemId, {}).get('name', '')
                quality = ID.data.get(bonusItemId, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('color', '#FFFFE7')
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_206 % (color,
                 name,
                 bonusNum,
                 self.getBonusContent(bonusItemId))
            elif bonusType == gametypes.BONUS_TYPE_FAME:
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_208 % (FD.data.get(bonusItemId, {}).get('name', ''), bonusNum)
            else:
                nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
                 gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
                 gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
                 gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663,
                 gametypes.BONUS_TYPE_BONUS_SET: gameStrings.TEXT_ARENARANKAWARDPROXY_215}
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_208 % (nameMap[bonusType], bonusNum)
            if bonusItemName != '':
                bonusItemName += '<br>'
            bonusItemName += trueName

        return bonusItemName

    def getBonusContent(self, bonusItemId):
        itemSetInfo = CID.data.get(bonusItemId, {}).get('itemSetInfo', ())
        if not itemSetInfo:
            return ''
        itemSetId, _ = itemSetInfo
        itemList = BSD.data.get(itemSetId, [])
        if not itemList:
            return ''
        content = gameStrings.TEXT_ARENARANKAWARDPROXY_231
        for i in xrange(len(itemList)):
            bonusType = itemList[i].get('bonusType', 0)
            bonusId = itemList[i].get('bonusId', 0)
            calcType = itemList[i].get('calcType', 0)
            if bonusType == gametypes.BONUS_TYPE_ITEM and calcType in (0, 1):
                bonusId = utils.filtItemByConfig(bonusId, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            maxBonusNum = itemList[i].get('maxBonusNum', 0)
            if bonusType == 0 or bonusId == 0 or maxBonusNum == 0:
                continue
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                name = ID.data.get(bonusId, {}).get('name', '')
                quality = ID.data.get(bonusId, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('color', '#FFFFE7')
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_247 % (color, name, maxBonusNum)
            elif bonusType == gametypes.BONUS_TYPE_FAME:
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_249 % (FD.data.get(bonusId, {}).get('name', ''), maxBonusNum)
            else:
                nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
                 gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
                 gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
                 gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663,
                 gametypes.BONUS_TYPE_BONUS_SET: gameStrings.TEXT_ARENARANKAWARDPROXY_215}
                trueName = gameStrings.TEXT_ARENARANKAWARDPROXY_249 % (nameMap[bonusType], maxBonusNum)
            content += trueName

        return content
