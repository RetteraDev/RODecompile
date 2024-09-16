#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommStrongerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameconfigCommon
import gameglobal
import uiConst
import events
import commQuest
import formula
import utils
import itemToolTipUtils
import const
import gamelog
import gametypes
import clientUtils
from data import summon_sprite_skill_data as SSSD
from cdata import combatscore_reward_data as CRD
from data import enhance_suit_data as ESD
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
MAX_TAB_BTN_NUM = 6
MAX_PROGRESS_NUM = 6
TAB_ID_OVERVIEW = 1
TAB_ID_EQUIP = 2
TAB_ID_SKILL = 3
TAB_ID_RUNE = 4
TAB_ID_JINGJIE = 5
TAB_ID_PROPERTY = 6
TAB_ID_SUMMON_SPRITE = 7
TAB_ID_GET = 201
TAB_ID_JINGLIAN = 202
TAB_ID_JUEXING = 203
TAB_ID_PREFIX = 204
TAB_ID_STAR = 205
TAB_ID_SLOT = 206
TAB_ID_EQUIP_SLOT_23 = 207
TAB_ID_EQUIP_SLOT_5 = 208
TAB_ID_COMM_SKILL = 301
TAB_ID_WS_SKILL = 302
TAB_ID_AIR_SKILL = 303
TAB_ID_RUNEINFO = 401
TAB_ID_GUILD_GROWTH = 601
TAB_ID_EQUIP_SOUL = 602
TAB_ID_PVP_ENHANCE = 603
TAB_ID_CARD = 604
TAB_ID_SUMMON_SPRITE_GET = 701
TAB_ID_SUMMON_SPRITE_FAMI = 702
TAB_ID_SUMMON_SPRITE_SKILL = 703
TAB_ID_SUMMON_SPRITE_APTITUDE = 704
TAB_ID_SUMMON_SPRITE_GUIDE = 705
TAB_ID_SUMMON_SPRITE_GROWTH = 706
ZHANLI_TYPE_LOW = 1
ZHANLI_TYPE_NORMAL = 2
ZHANLI_TYPE_HIGH = 3
RUNE_SLOT_STATE_FILLED = 1
RUNE_SLOT_STATE_EMPTY = 2
RUNE_SLOT_STATE_NONE = 3
from data import equip_enhance_refining_data as EERD
from data import play_recomm_config_data as PRCD
from data import equip_data as ED
from data import play_recomm_equip_get_data as PREGD
from data import item_data as ID
from data import play_recomm_equip_category_data as PRECD
from data import play_recomm_strongger_data as PRSD
from data import sys_config_data as SCD
from data import prop_ref_data as EPRD
from data import equip_prefix_prop_data as EPPD
from data import school_data as SD
from cdata import equip_special_props_data as ESPD
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_order_factor_data as EOFD
from cdata import equip_enhance_prop_data as EEPD
from data import play_recomm_score_data as PRSCD
from data import formula_client_data as FCD
from cdata import equip_gem_score_data as EGSD
from cdata import game_msg_def_data as GMDD
from data import equip_gem_data as EGD
MULTIPLE_BATTLE_ID = 1
SUMMON_SPRITE_GET_FORMULA_ID = 90168
SUMMON_SPRITE_FAMI_FORMULA_ID = 90169
SUMMON_SPRITE_GET_SKILL_FORMULA_ID = 90170
SUMMON_SPRITE_APTITTUDE_FORMULA_ID = 90171
SCORE_REWARD_NOT_COMPLETED = 0
SCORE_REWARD_COMPLETED = 1
SCORE_REWARD_GET_REWARD = 2
TAB_ID_TO_PID_MAP = {TAB_ID_OVERVIEW: const.COMBAT_SCORE,
 TAB_ID_EQUIP: const.EQUIP_SCORE,
 TAB_ID_SKILL: const.WS_SKILL_LV_SCORE,
 TAB_ID_RUNE: const.RUNE_SCORE,
 TAB_ID_PROPERTY: const.COMBAT_SCORE_BASIC,
 TAB_ID_SUMMON_SPRITE: const.SPRITE_SCORE}

class PlayRecommStrongerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommStrongerProxy, self).__init__(uiAdapter)
        self.tabIdx = TAB_ID_OVERVIEW
        self.widget = None
        self.reset()

    def reset(self):
        self.maxEnhancePerfect = {}
        self.lastSelTab = None
        self.gridAlign = 'center'

    def initPanel(self, widget):
        BigWorld.player().cell.getCombatScoreRewardInfo()
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        if self.lastSelTab:
            self.lastSelTab.selected = False
        self.widget = None
        self.reset()

    def initUI(self):
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 3)

    def initMaxEnhPerfectData(self):
        eerdd = EERD.data
        for enhLv, enhData in eerdd.iteritems():
            maxLv = 0
            enhEffects = enhData.get('enhEffects', [])
            for e in enhEffects:
                maxLv = max(maxLv, e[0])

            self.maxEnhancePerfect[enhLv] = round(self.maxEnhancePerfect.get(enhLv - 1, 0) + maxLv, 4)

    def getStrongerTabInfo(self):
        self.initMaxEnhPerfectData()
        ret = {}
        tabList = []
        tabOrder = PRCD.data.get('strongerTabOrder', (1, 2, 3))
        tabNames = PRCD.data.get('strongerTabName', {1: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_158,
         2: gameStrings.TEXT_ACTIVITYFACTORY_93,
         3: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_158_2})
        showLimit = PRCD.data.get('strongerTabShowLimit', {})
        strongerTabShowConfig = PRCD.data.get('strongerTabShowConfig', {})
        for tabId in tabOrder:
            tabInfo = {}
            tabInfo['tabId'] = tabId
            tabInfo['tabName'] = tabNames.get(tabId, '')
            enableConfig = strongerTabShowConfig.get(tabId, '')
            if not tabInfo['tabName']:
                continue
            if enableConfig and not gameglobal.rds.configData.get(enableConfig, False):
                continue
            if not self.tabShowCheck(showLimit.get(tabId, {})):
                continue
            tabList.append(tabInfo)

        ret['tabList'] = tabList
        ret['defSelectTabId'] = PRCD.data.get('strongerDefSelectTabId', 1)
        return ret

    def tabShowCheck(self, limitData):
        if not limitData:
            return True
        p = BigWorld.player()
        minLv = limitData.get('minLv', -1)
        if minLv > 0 and p.lv < minLv:
            return False
        serverEvent = limitData.get('serverEvent', 0)
        if serverEvent and not p.checkServerProgress(serverEvent, False):
            return False
        if not getattr(p, 'newAvatarStraightLvUpFlag', False):
            comQuestId = limitData.get('questComp', 0)
            if comQuestId > 0:
                if p.getQuestFlag(comQuestId):
                    return True
                elif comQuestId in p.quests:
                    return commQuest.completeQuestCheck(p, comQuestId)
                else:
                    return False
        return True

    def getPlayRecommValByFormula(self, formula):
        myLv = BigWorld.player().lv
        formatedFormula = '1'
        for k, v in formula.iteritems():
            if k[0] <= myLv <= k[1]:
                formatedFormula = v.replace('lv', str(myLv))

        try:
            val = eval(formatedFormula)
        except:
            val = 1

        return int(val)

    def getScoreType(self, subId, score):
        p = BigWorld.player()
        lowScore = PRSCD.data.get((p.lv, subId), {}).get('lowScore', 10000)
        highScore = PRSCD.data.get((p.lv, subId), {}).get('highScore', 10000)
        if score < lowScore:
            return ZHANLI_TYPE_LOW
        elif score < highScore:
            return ZHANLI_TYPE_NORMAL
        else:
            return ZHANLI_TYPE_HIGH

    def getPlayRecommValByLv(self, subId):
        return PRSCD.data.get((BigWorld.player().lv, subId), {}).get('highScore', 10000)

    def calcEquipStarScoreClient(self, equip, enh, juexing, gemScore):
        if not equip:
            return 0
        starScore = 0
        effectScore = 0
        starFactor = ESFCD.data.get(equip.starLv, {}).get('factor', 1.0)
        if equip.starExp > 0 and equip.starExp >= equip._getEquipStarUpExp():
            isManual = equip.isManualEquip()
            isExtended = equip.isExtendedEquip()
            if isManual or isExtended:
                data = equip._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
                effectScore = starPropFixScore + ESPD.data.get(data.get('starSEffect', 0), {}).get('equipScore', 0)
            else:
                ed = ED.data.get(equip.id, {})
                starPropFixScore = ed.get('starPropFixScore', 0)
                effectScore = starPropFixScore + ESPD.data.get(ed.get('starSEffect', 0), {}).get('equipScore', 0)
        starScore = effectScore + (equip.score - enh - juexing - effectScore) * (starFactor - 1) / starFactor
        return starScore

    def calcEquipEnhanceScoreClient(self, equip):
        enhanceScore = 0
        juexingScore = 0
        if not equip:
            return (enhanceScore, juexingScore)
        orderFactor = EOFD.data.get(equip.order, {}).get('factor', 1.0)
        refiningFactor = 0
        for eLv, v in getattr(equip, 'enhanceRefining', {}).iteritems():
            if eLv <= min(getattr(equip, 'enhLv', 0), equip.getMaxEnhLv(BigWorld.player())):
                refiningFactor += v

        enhanceData = EEPD.data.get((equip.equipType, equip.equipSType, equip.enhanceType), {})
        if enhanceData.has_key('enhScore'):
            fVars = {'enhanceRefining': refiningFactor,
             'orderFactor': orderFactor,
             'enhanceLv': min(getattr(equip, 'enhLv', 0), equip.getMaxEnhLv(BigWorld.player()))}
            enhScore = enhanceData['enhScore']
            fId = enhScore[0]
            params = enhScore[1:]
            for i in range(len(params)):
                param = params[i]
                fVars['p%d' % (i + 1,)] = param

            enhanceScore = formula.calcFormulaById(fId, fVars)
        try:
            for eLv, juexingPropList in getattr(equip, 'enhJuexingData', {}).iteritems():
                if eLv > min(getattr(equip, 'enhLv', 0), equip.maxEnhlv):
                    continue
                juexingDataList = utils.getEquipEnhJuexingPropData(equip.equipType, equip.equipSType, eLv, equip.enhanceType)
                for pid, ptp, value in juexingPropList:
                    if pid not in juexingDataList:
                        continue
                    data = EPRD.data.get(pid)
                    if not data:
                        continue
                    juexingScoreFormula = data.get('juexingScore')
                    if not juexingScoreFormula:
                        continue
                    formulaId, formulaParams = juexingScoreFormula[0], juexingScoreFormula[1:]
                    juexingPropScore = equip.evalValue(formulaId, formulaParams, {'val': value,
                     'enhLv': eLv})
                    juexingScore += int(juexingPropScore)

        except Exception as e:
            gamelog.error('calc juexing score error!', equip.id, e.message)

        if not enhanceScore:
            enhanceScore = 0
        if not juexingScore:
            juexingScore = 0
        return (enhanceScore, juexingScore)

    def calcEquipGemScoreClient(self, equip):
        gemScore = 0
        maxSlotCount = gameglobal.rds.ui.equipGem.slotMaxCount
        if not equip:
            return 0
        else:
            egsdd = EGSD.data
            for i in range(maxSlotCount):
                yinSlotData = equip.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
                if yinSlotData != None and yinSlotData.gem:
                    gemData = utils.getEquipGemData(yinSlotData.gem.id)
                    if gemData:
                        if equip.addedOrder >= gemData.get('orderLimit', 0):
                            gemScore += egsdd.get((gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)), {}).get('gPoint', 0)
                        elif gameconfigCommon.enableLessLvWenYin():
                            lessGemId = utils.getLessLvWenYinGemId(equip.addedOrder, gemData)
                            lessGemData = EGD.data.get(lessGemId, {})
                            if lessGemData:
                                gemLv = lessGemData.get('lv', 0)
                                gemType = lessGemData.get('type', 0)
                                gemSubType = lessGemData.get('subType', 0)
                                gemScore += EGSD.data.get((gemLv, gemType, gemSubType), {}).get('gPoint', 0)
                yangSlotData = equip.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
                if yangSlotData != None and yangSlotData.gem:
                    gemData = utils.getEquipGemData(yangSlotData.gem.id)
                    if gemData:
                        if equip.addedOrder >= gemData.get('orderLimit', 0):
                            gemScore += egsdd.get((gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)), {}).get('gPoint', 0)
                        elif gameconfigCommon.enableLessLvWenYin():
                            lessGemId = utils.getLessLvWenYinGemId(equip.addedOrder, gemData)
                            lessGemData = EGD.data.get(lessGemId, {})
                            if lessGemData:
                                gemLv = lessGemData.get('lv', 0)
                                gemType = lessGemData.get('type', 0)
                                gemSubType = lessGemData.get('subType', 0)
                                gemScore += EGSD.data.get((gemLv, gemType, gemSubType), {}).get('gPoint', 0)

            return gemScore

    def calcAllEquipmentSubScore(self):
        enhScore = 0
        juexingScore = 0
        gemScore = 0
        starScore = 0
        equipment = BigWorld.player().equipment
        for it in equipment:
            if not it:
                continue
            enh, juexing = self.calcEquipEnhanceScoreClient(it)
            gem = self.calcEquipGemScoreClient(it)
            star = self.calcEquipStarScoreClient(it, enh, juexing, gem)
            enhScore += enh
            juexingScore += juexing
            gemScore += gem
            starScore += star

        return (int(enhScore),
         int(juexingScore),
         int(gemScore),
         int(starScore))

    def getZhanLiValueById(self, pId):
        combatScoreList = BigWorld.player().combatScoreList
        enhScore, juexingScore, slotScore, starScore = self.calcAllEquipmentSubScore()
        slotScore = combatScoreList[const.WEN_YIN_SCORE]
        item = BigWorld.player().equipment[23]
        hufuScore = int(item.score if item else 0)
        item = BigWorld.player().equipment[5]
        huiZhangScore = int(item.score if item else 0)
        if pId == TAB_ID_OVERVIEW:
            return combatScoreList[const.COMBAT_SCORE]
        elif pId == TAB_ID_EQUIP:
            value = combatScoreList[const.EQUIP_SCORE]
            if gameconfigCommon.enableSplitWenYinFromEquip():
                value += combatScoreList[const.WEN_YIN_SCORE]
            if gameconfigCommon.enableEquipEnhanceSuit():
                addScore = self.uiAdapter.equipRefineSuitsProp.getAddScore()
                value += addScore
            return value
        elif pId == TAB_ID_SKILL:
            return combatScoreList[const.SKILL_ENHANCE_SCORE] + combatScoreList[const.WS_SKILL_LV_SCORE] + combatScoreList[const.WS_SKILL_ENH_SCORE]
        elif pId == TAB_ID_RUNE:
            return combatScoreList[const.RUNE_SCORE]
        elif pId == TAB_ID_RUNEINFO:
            return combatScoreList[const.RUNE_SCORE]
        elif pId == TAB_ID_PROPERTY:
            value = combatScoreList[const.COMBAT_SCORE] - combatScoreList[const.EQUIP_SCORE] - combatScoreList[const.SKILL_ENHANCE_SCORE] - combatScoreList[const.RUNE_SCORE] - combatScoreList[const.WS_SKILL_LV_SCORE] - combatScoreList[const.WS_SKILL_ENH_SCORE] - self.getSummonSpriteScore()[4]
            if gameconfigCommon.enableSplitWenYinFromEquip():
                value -= combatScoreList[const.WEN_YIN_SCORE]
            if gameconfigCommon.enableEquipEnhanceSuit():
                value -= self.uiAdapter.equipRefineSuitsProp.getAddScore()
            return value
        elif pId == TAB_ID_GET:
            return combatScoreList[const.EQUIP_SCORE] + combatScoreList[const.WEN_YIN_SCORE] - enhScore - juexingScore - slotScore - starScore - hufuScore - huiZhangScore
        elif pId == TAB_ID_JINGLIAN:
            return enhScore
        elif pId == TAB_ID_JUEXING:
            return juexingScore
        elif pId == TAB_ID_PREFIX:
            return 0
        elif pId == TAB_ID_STAR:
            return starScore
        elif pId == TAB_ID_SLOT:
            return slotScore
        elif pId == TAB_ID_COMM_SKILL:
            return combatScoreList[const.SKILL_ENHANCE_SCORE]
        elif pId == TAB_ID_WS_SKILL:
            return combatScoreList[const.WS_SKILL_LV_SCORE] + combatScoreList[const.WS_SKILL_ENH_SCORE]
        elif pId == TAB_ID_AIR_SKILL:
            return 0
        elif pId == TAB_ID_SUMMON_SPRITE:
            return self.getSummonSpriteScore()[4]
        elif pId == TAB_ID_SUMMON_SPRITE_GET:
            return self.getSummonSpriteScore()[0]
        elif pId == TAB_ID_SUMMON_SPRITE_FAMI:
            return self.getSummonSpriteScore()[1]
        elif pId == TAB_ID_SUMMON_SPRITE_SKILL:
            return self.getSummonSpriteScore()[2]
        elif pId == TAB_ID_SUMMON_SPRITE_APTITUDE:
            return self.getSummonSpriteScore()[3]
        elif pId == TAB_ID_SUMMON_SPRITE_GUIDE:
            return combatScoreList[const.SPRITE_ACC_SCORE]
        elif pId == TAB_ID_SUMMON_SPRITE_GROWTH:
            return combatScoreList[const.SPRITE_GROWTH_SCORE]
        elif pId == TAB_ID_GUILD_GROWTH:
            return combatScoreList[const.GUILD_GROWTH_SCORE]
        elif pId == TAB_ID_EQUIP_SOUL:
            return combatScoreList[const.EQUIP_SOUL_SCORE]
        elif pId == TAB_ID_PVP_ENHANCE:
            return combatScoreList[const.PVP_ENH_SCORE]
        elif pId == TAB_ID_CARD:
            return combatScoreList[const.CARD_SCORE]
        elif pId == TAB_ID_EQUIP_SLOT_23:
            return hufuScore
        elif pId == TAB_ID_EQUIP_SLOT_5:
            return huiZhangScore
        else:
            return 0

    def getStrongerProgressInfo(self):
        ret = []
        progressOrder = PRCD.data.get('progressOrder', (1, 2, 3, 4, 5, 6))
        progressConfig = PRCD.data.get('progressConfig', {})
        scoreColor = PRCD.data.get('scoreLevelColor', ('blue', 'purple', 'yellow', 'orange'))
        overviewTips = PRCD.data.get('overviewTips', {})
        strongerTabShowConfig = PRCD.data.get('strongerTabShowConfig', {})
        progressPartMaxSum = 0
        progressPartMaxMap = {}
        progressPartSum = PRCD.data.get('progressPartSum', (2, 3, 4, 6))
        overviewConfig = PRCD.data.get('overviewConfig', {})
        p = BigWorld.player()
        for pId in progressPartSum:
            total = 0
            subIds = overviewConfig.get(pId, ())
            for subId in subIds:
                total += self.getPlayRecommValByLv(subId)

            if pId == TAB_ID_PROPERTY:
                total += p.combatScoreList[const.SCHOOL_SCORE]
            progressPartMaxMap[pId] = total
            progressPartMaxSum += total

        progressPartMaxMap[MULTIPLE_BATTLE_ID] = progressPartMaxSum
        isAllSatified = True
        isLastIndex = False
        for pId in progressOrder:
            info = {}
            configData = progressConfig.get(pId, {})
            enableConfig = strongerTabShowConfig.get(pId, '')
            if enableConfig and not gameglobal.rds.configData.get(enableConfig, False):
                continue
            info['open'] = self.tabShowCheck(configData.get('openLimit', {}))
            frameName = configData.get('frameName', 'zonghe')
            info['propName'] = gameStrings.PLAY_RECOMM_V2_STRONGER_FRAME_NAME_MAP.get(frameName, '')
            if progressPartMaxMap[pId]:
                info['max'] = progressPartMaxMap[pId]
            else:
                info['max'] = self.getPlayRecommValByLv(pId)
            info['val'] = self.getZhanLiValueById(pId)
            rewardMaxScore, itemInfo = self.getRewardNeedScoreAndReward(pId)
            margins = CRD.data.get(TAB_ID_TO_PID_MAP[pId], {}).get('rewardMargins', ())
            if margins.index(rewardMaxScore) == len(margins) - 1:
                isLastIndex = True
            lastMargin = BigWorld.player().combatScoreRewardInfo.get(TAB_ID_TO_PID_MAP[pId], 0)
            if info['val'] < rewardMaxScore:
                info['rewardStage'] = SCORE_REWARD_NOT_COMPLETED
            elif lastMargin < rewardMaxScore:
                info['rewardStage'] = SCORE_REWARD_COMPLETED
            else:
                info['rewardStage'] = SCORE_REWARD_GET_REWARD
            info['rewardMaxScore'] = rewardMaxScore
            info['rewardData'] = uiUtils.getGfxItemById(itemInfo[0], itemInfo[1])
            isAllSatified = isAllSatified and info['val'] >= info['rewardMaxScore']
            info['isSatisfied'] = info['val'] >= info['rewardMaxScore']
            info['scoreLv'] = self.getScoreLv(info['val'], info['max'], configData.get('scoreRange', ()))
            info['scoreColor'] = scoreColor[info['scoreLv']]
            info['tips'] = overviewTips.get(pId, '')
            info['tabId'] = pId
            ret.append(info)

        for info in ret:
            info['isAllSatisfied'] = isAllSatified
            info['isLastIndex'] = isLastIndex

        return ret

    def getRewardNeedScoreAndReward(self, tabId):
        pid = TAB_ID_TO_PID_MAP[tabId]
        indexDic = {}
        combatScoreInfo = BigWorld.player().combatScoreRewardInfo
        for key, data in CRD.data.iteritems():
            currentScore = combatScoreInfo.get(key, 0)
            rewardMargins = data.get('rewardMargins', ())
            if currentScore not in rewardMargins:
                indexDic[key] = -1
            else:
                indexDic[key] = rewardMargins.index(currentScore)

        indexList = indexDic.values()
        indexList.sort()
        nextIndex = indexList[0] + 1
        print 'jbx:tabId, pid', tabId, pid
        rewardMargins = CRD.data.get(pid, {}).get('rewardMargins', ())
        nextIndex = min(nextIndex, len(rewardMargins) - 1)
        print 'jbx:nextIndex', nextIndex, rewardMargins
        score = rewardMargins[nextIndex]
        bonusId = CRD.data.get(pid, {}).get('bonusIds', ())[nextIndex]
        items = clientUtils.genItemBonusEx(bonusId)
        return (score, items[0])

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            strongerData = self.getStrongerTabInfo()
            i = 0
            tabMc = None
            tabList = strongerData['tabList']
            defSelectTabId = strongerData['defSelectTabId']
            if self.lastSelTab:
                self.lastSelTab.selected = False
            self.lastSelTab = None
            strongerPanel = self.widget.strongerPanel
            for i in xrange(MAX_TAB_BTN_NUM):
                tabMc = getattr(strongerPanel, 'tabBtn%d' % i)
                tabMc.selected = False
                if i >= len(tabList):
                    tabMc.visible = False
                    continue
                tabInfo = tabList[i]
                tabMc.visible = True
                tabMc.label = tabInfo['tabName']
                tabMc.data = tabInfo['tabId']
                tabMc.addEventListener(events.EVENT_SELECT, self.tabBtnSelectListener, False, 0, True)
                tabMc.addEventListener(events.BUTTON_CLICK, self.btnClickListener, False, 0, True)
                tabMc.selected = tabInfo['tabId'] == defSelectTabId
                if tabMc.selected:
                    self.lastSelTab = tabMc

            if self.lastSelTab == None:
                tabMc = getattr(strongerPanel, 'tabBtn0')
                tabMc.selected = True
                self.lastSelTab = tabMc
            progressInfo = self.getStrongerProgressInfo()
            for i in xrange(MAX_PROGRESS_NUM):
                progressMc = getattr(strongerPanel, 'progress%d' % i)
                if i >= len(progressInfo):
                    progressMc.visible = False
                    continue
                info = progressInfo[i]
                progressMc.visible = True
                if not info['open']:
                    progressMc.gotoAndStop('off')
                    continue
                else:
                    progressMc.gotoAndStop('on')
                progressMc.nameMc.htmlText = info['propName']
                if gameconfigCommon.enableCombatScoreListReward():
                    progressMc.targetLabel.visible = True
                    progressMc.reward.visible = True
                    stage = info['rewardStage']
                    if stage <= SCORE_REWARD_NOT_COMPLETED:
                        progressMc.targetLabel.text = gameStrings.PLAY_RECOMM_V2_STRONGER_TARGET % (info['val'], info['rewardMaxScore'])
                    elif info['isLastIndex']:
                        progressMc.targetLabel.text = PRCD.data.get('targetScoreAllCompleted', 'AllCompleted')
                    else:
                        progressMc.targetLabel.text = PRCD.data.get('tartScoreCompleted', 'Completed')
                    ASUtils.autoSizeWithFont(progressMc.targetLabel, 12, progressMc.targetLabel.width, 9)
                    progressMc.reward.gotoAndStop(('notComplete', 'completed', 'getReward')[stage])
                    progressMc.reward.slot.dragable = False
                    progressMc.reward.slot.setItemSlotData(info['rewardData'])
                    progressMc.reward.isAllSatisfied = info['isAllSatisfied']
                    progressMc.reward.isSatisfied = info['isSatisfied']
                    progressMc.reward.isGetReward = stage == SCORE_REWARD_GET_REWARD
                    progressMc.reward.tabId = info['tabId']
                    if progressMc.reward.effect:
                        ASUtils.setHitTestDisable(progressMc.reward.effect, True)
                    if progressMc.reward.check:
                        ASUtils.setHitTestDisable(progressMc.reward.check, True)
                    progressMc.reward.slot.addEventListener(events.MOUSE_CLICK, self.handleScoreRewardClick, False, 0, True)
                else:
                    progressMc.targetLabel.visible = False
                    progressMc.reward.visible = False
                progressMc.progressLabel.htmlText = str(info['val']) + '/' + str(info['max'])
                TipManager.addTip(progressMc, info['tips'])

            return

    def handleScoreRewardClick(self, *args):
        currentTarget = ASObject(args[3][0]).currentTarget
        tabId = int(currentTarget.parent.tabId)
        if tabId == TAB_ID_OVERVIEW and not currentTarget.parent.isAllSatisfied:
            BigWorld.player().showGameMsg(GMDD.data.PALY_RECOMM_STRONGER_NOT_ALL_SATISFIED)
        elif not currentTarget.parent.isSatisfied:
            BigWorld.player().showGameMsg(GMDD.data.PALY_RECOMM_STRONGER_NOT_SATISFIED)
        else:
            if currentTarget.parent.isGetReward:
                return
            tabId = int(currentTarget.parent.tabId)
            pid = TAB_ID_TO_PID_MAP[tabId]
            gamelog.info('jbx:getCombatScoreReward', pid)
            BigWorld.player().cell.getCombatScoreReward(pid)

    def tabBtnSelectListener(self, *args):
        e = ASObject(args[3][0])
        gamelog.info('@jbx:tabBtnSelectListener', e.target.selected, e.target.data)
        if not e.target.selected:
            return
        tabId = int(e.target.data)
        self.tabIdx = tabId
        if tabId == TAB_ID_OVERVIEW:
            self.refreshPanelOverview()
        elif tabId == TAB_ID_EQUIP:
            self.refreshPanelEquip()
        elif tabId == TAB_ID_SKILL:
            self.refreshPanelSkill()
        elif tabId == TAB_ID_RUNE:
            self.refreshPanelRune()
        elif tabId == TAB_ID_JINGJIE:
            self.refreshPanelJingjie()
        elif tabId == TAB_ID_PROPERTY:
            self.refreshPanelProperty()
        elif tabId == TAB_ID_SUMMON_SPRITE:
            self.refreshSummonSprite()

    def getScoreLv(self, val, maxVal, scoreRange):
        if not scoreRange:
            return 0
        percent = float(val) / max(maxVal, 1)
        for lv in xrange(len(scoreRange)):
            sRange = scoreRange[lv]
            if percent >= sRange[0] and percent < sRange[1]:
                return min(lv, 3)

        return 3

    def getOverViewInfo(self, *arg):
        overviewOrder = PRCD.data.get('overviewOrder', (2, 4, 3))
        overviewConfig = PRCD.data.get('overviewConfig', {})
        strongerTabName = PRCD.data.get('strongerTabName', {})
        showLimit = PRCD.data.get('strongerTabShowLimit', {})
        tabNames = PRCD.data.get('equipTabName', {201: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_688,
         2: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_688_1,
         3: gameStrings.TEXT_EQUIPMIXNEWPROXY_295})
        equipTabShowLimit = PRCD.data.get('equipTabShowLimit', {})
        overviewTips = PRCD.data.get('overviewTips', {})
        strongerOverviewItems = PRCD.data.get('strongerOverviewItems', {})
        strongerOverviewItemLinkText = PRCD.data.get('strongerOverviewItemLinkText', {})
        strongerOvervieItemBtnNames = PRCD.data.get('strongerOvervieItemBtnNames', {})
        itemList = []
        for oId in overviewOrder:
            cateInfo = {}
            if not self.tabShowCheck(showLimit.get(oId)):
                continue
            subList = []
            cateInfo['overviewList'] = subList
            for subId in overviewConfig.get(oId, ()):
                if not self.tabShowCheck(equipTabShowLimit.get(subId, {})):
                    continue
                maxValue = self.getPlayRecommValByLv(subId)
                value = self.getZhanLiValueById(subId)
                subInfo = {}
                subInfo['scoreType'] = self.getScoreType(subId, value)
                subInfo['name'] = tabNames.get(subId, gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_688)
                subInfo['value'] = value
                subInfo['maxValue'] = maxValue
                subInfo['oId'] = oId
                subInfo['subId'] = subId
                subInfo['itemId'] = strongerOverviewItems.get(subId, subId)
                subInfo['tips'] = overviewTips.get(subId, '')
                subInfo['linkText'] = strongerOverviewItemLinkText.get(subId, '')
                subInfo['btnName'] = strongerOvervieItemBtnNames.get(subId, '')
                subInfo['isBtnEnable'] = True
                if subId == 706:
                    subInfo['isBtnEnable'] = gameglobal.rds.ui.summonedWarSprite.checkXiuLianLvAndJinejie()
                itemList.append(subInfo)

            if len(subList) <= 0:
                continue
            cateInfo['cateName'] = strongerTabName.get(oId, gameStrings.TEXT_ACTIVITYFACTORY_93) + gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_731

        return itemList

    def fillOverViewSubList(self, canvas, subList, startX, startY, width):
        height = 0
        offset = 0
        for j in xrange(len(subList)):
            gridMc = self.widget.getInstByClsName('PlayRecommV2Stronger_PlayRecommStronge_OverviewGrid')
            gridInfo = subList[j]
            if self.gridAlign == 'center':
                offset = startX + (width - gridMc.width * subList.length) / 2
            else:
                offset = startX
            gridMc.name = 'grid'
            gridMc.overviewId = gridInfo['oId']
            gridMc.subId = gridInfo['subId']
            gridMc.title.htmlText = gridInfo['name']
            gridMc.scoreLogoMc.gotoAndStop('lv' + str(gridInfo['lv']))
            gridMc.scoreMc.gotoAndStop(gridInfo['score'])
            gridMc.x = offset + j * gridMc.width
            gridMc.y = startY
            gridMc.progressBar.maxValue = int(gridInfo['maxValue'])
            gridMc.progressBar.currentValue = int(gridInfo['value'])
            gridMc.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
            canvas.addChild(gridMc)
            height = gridMc.height
            TipManager.addTip(gridMc, gridInfo['tips'])

        return height

    def fillOverviewLine(self, viewLine, canvas, offset, lineNum):
        CAVAS_WIDTH = 720
        GRID_WIDTH = 140
        titleHeight = 0
        gridHeight = 0
        allGridNum = 0
        for i in xrange(len(viewLine)):
            info = viewLine[i]
            subList = info['overviewList']
            allGridNum += len(subList)

        for i in xrange(len(viewLine)):
            info = viewLine[i]
            subList = info['overviewList']
            cateTitle = self.widget.getInstByClsName('PlayRecommV2Stronger_PlayRecommStronger_OverviewTitle')
            cateTitle.titleMc.titleText.htmlText = info['cateName']
            cateTitle.titleMc.scoreMc.gotoAndStop(info['cateScore'])
            if self.gridAlign == 'center':
                width = len(subList) * CAVAS_WIDTH / allGridNum
                cateTitle.titleMc.x = (width - cateTitle.titleMc.width) / 2
            else:
                width = len(subList) * GRID_WIDTH
                cateTitle.titleMc.x = 0
            cateTitle.y = offset
            cateTitle.name = 'cateTitle.%d.%d' % (lineNum, i)
            canvas.addChild(cateTitle)
            if i:
                lastTitle = canvas.getChildByName('cateTitle.' + str(lineNum) + '.' + str(i - 1))
                cateTitle.x = lastTitle.x + 150
            titleHeight = cateTitle.height
            gridHeight = self.fillOverViewSubList(canvas, subList, cateTitle.x, offset + titleHeight, width)

        return titleHeight + gridHeight

    def onGetEquipTabInfo(self, *arg):
        ret = {}
        tabList = []
        tabOrder = PRCD.data.get('equipTabOrder', (201, 202, 203))
        tabNames = PRCD.data.get('equipTabName', {201: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_688,
         2: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_688_1,
         3: gameStrings.TEXT_EQUIPMIXNEWPROXY_295})
        showLimit = PRCD.data.get('equipTabShowLimit', {})
        for tabId in tabOrder:
            tabInfo = {}
            tabInfo['tabId'] = tabId
            tabInfo['tabName'] = tabNames.get(tabId, '')
            if not tabInfo['tabName']:
                continue
            if not self.tabShowCheck(showLimit.get(tabId, {})):
                continue
            tabList.append(tabInfo)

        ret['tabList'] = tabList
        ret['defSelectTabId'] = PRCD.data.get('equipDefSelectTabId', 201)
        return uiUtils.dict2GfxDict(ret, True)

    def refreshPanelOverview(self):
        self.tabIdx = TAB_ID_OVERVIEW
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = True
        strongerPanel.detailPanel.visible = False
        strongerPanel.runeWnd.visible = False
        strongerPanel.overviewPanel.overviewScrollWnd.itemRenderer = 'PlayRecommV2Stronger_OverviewItemRender'
        strongerPanel.overviewPanel.overviewScrollWnd.column = 2
        strongerPanel.overviewPanel.overviewScrollWnd.itemWidth = 384
        strongerPanel.overviewPanel.overviewScrollWnd.itemHeight = 75
        overviewInfo = self.getOverViewInfo()
        strongerPanel.overviewPanel.overviewScrollWnd.labelFunction = self.overViewItemLabelFunction
        strongerPanel.overviewPanel.overviewScrollWnd.dataArray = overviewInfo
        strongerPanel.overviewPanel.overviewScrollWnd.validateNow()

    def overViewItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.scoreType == ZHANLI_TYPE_LOW:
            itemMc.gotoAndStop('down')
            itemMc.lowScore.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverViewItemMouseOver, False, 0, True)
            itemMc.lowScore.addEventListener(events.MOUSE_ROLL_OUT, self.handleOverViewItemMouseOut, False, 0, True)
            TipManager.addTip(itemMc.lowScore, PRCD.data.get('stronggerTips', ('', ''))[0])
        elif itemData.scoreType == ZHANLI_TYPE_NORMAL:
            itemMc.gotoAndStop('normal')
        else:
            itemMc.gotoAndStop('up')
            itemMc.highScore.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverViewItemMouseOver, False, 0, True)
            itemMc.highScore.addEventListener(events.MOUSE_ROLL_OUT, self.handleOverViewItemMouseOut, False, 0, True)
            TipManager.addTip(itemMc.highScore, PRCD.data.get('stronggerTips', ('', ''))[1])
        itemMc.itemSlot.setItemSlotData(uiUtils.getGfxItemById(int(itemData.itemId)))
        itemMc.txtName.htmlText = itemData.name
        itemMc.txtNowValue.text = gameStrings.PLAY_RECOMM_V2_STRONGER_OVERVIEW_ITEM_NOW_SCORE % int(itemData.value)
        itemMc.txtMaxValue.text = gameStrings.PLAY_RECOMM_V2_STRONGER_OVERVIEW_ITEM_MAX_SCORE % int(itemData.maxValue)
        itemMc.strongerBtn.linkText = itemData.linkText
        itemMc.strongerBtn.enabled = itemData.isBtnEnable
        ASUtils.setHitTestDisable(itemMc.selectedMc, True)
        itemMc.selectedMc.visible = False
        itemMc.itemSlot.addEventListener(events.MOUSE_OVER, self.handleOverViewItemMouseOver, False, 0, True)
        itemMc.itemSlot.addEventListener(events.MOUSE_OUT, self.handleOverViewItemMouseOut, False, 0, True)
        itemMc.addEventListener(events.MOUSE_OVER, self.handleOverViewItemMouseOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_OUT, self.handleOverViewItemMouseOut, False, 0, True)
        itemMc.strongerBtn.label = itemData.btnName

    def refreshPanelEquip(self):
        self.tabIdx = TAB_ID_EQUIP
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.detailPanel.visible = True
        strongerPanel.runeWnd.visible = False
        strongerPanel.detailPanel.skillPanel.visible = False
        strongerPanel.detailPanel.equipPanel.visible = True
        strongerPanel.detailPanel.equipPanel.refreshEquipPanel(self.uiAdapter.playRecomm.getPrMediator())

    def refreshPanelSkill(self):
        self.tabIdx = TAB_ID_SKILL
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.runeWnd.visible = False
        strongerPanel.detailPanel.visible = True
        strongerPanel.detailPanel.skillPanel.visible = True
        strongerPanel.detailPanel.equipPanel.visible = False
        strongerPanel.detailPanel.skillPanel.refreshSkillPanel(self.uiAdapter.playRecomm.getPrMediator())

    def refreshPanelRune(self):
        self.tabIdx = TAB_ID_RUNE
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.detailPanel.visible = False
        strongerPanel.runeWnd.visible = True
        strongerPanel.runeWnd.canvas.runePanel.refreshRunePanel(self.uiAdapter.playRecomm.getPrMediator())
        strongerPanel.runeWnd.refreshHeight()

    def refreshPanelJingjie(self):
        self.tabIdx = TAB_ID_JINGJIE
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.detailPanel.visible = False
        strongerPanel.runeWnd.visible = False

    def refreshPanelProperty(self):
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.detailPanel.visible = False
        strongerPanel.runeWnd.visible = False

    def refreshSummonSprite(self):
        self.tabIdx = TAB_ID_SUMMON_SPRITE
        strongerPanel = self.widget.strongerPanel
        strongerPanel.overviewPanel.visible = False
        strongerPanel.runeWnd.visible = False
        strongerPanel.detailPanel.visible = True
        strongerPanel.detailPanel.skillPanel.visible = True
        strongerPanel.detailPanel.equipPanel.visible = False
        strongerPanel.detailPanel.skillPanel.refreshSkillPanel({'playRecommModel': {'getSkillTabInfo': self.onGetSkillTabInfo}})

    def mouseClickListener(self, *args):
        e = ASObject(args[3][0])
        gamelog.info('@jbx:mouseClickListener', e.buttonIdx)
        if e.buttonIdx != uiConst.LEFT_BUTTON:
            return
        targetMc = e.currentTarget
        name = targetMc.name
        strongerPanel = self.widget.strongerPanel
        if name.index('grid') == 0:
            for i in xrange(MAX_TAB_BTN_NUM):
                tabMc = getattr(strongerPanel, 'tabBtn%d' % i)
                if tabMc.data == targetMc.overviewId:
                    if tabMc.data == TAB_ID_EQUIP:
                        strongerPanel.detailPanel.equipPanel.preOpenTabId = targetMc.subId
                    elif tabMc.data == TAB_ID_SKILL:
                        strongerPanel.detailPanel.skillPanel.preOpenTabId = targetMc.subId
                    ASUtils.DispatchButtonEvent(tabMc)
                    break

    def gotoOverViewTab(self, tabId, subId):
        strongerPanel = self.widget.strongerPanel
        for i in xrange(MAX_TAB_BTN_NUM):
            tabMc = getattr(strongerPanel, 'tabBtn%d' % i)
            if tabMc.data == tabId:
                if tabMc.data == TAB_ID_EQUIP:
                    strongerPanel.detailPanel.equipPanel.preOpenTabId = subId
                elif tabMc.data == TAB_ID_SKILL:
                    strongerPanel.detailPanel.skillPanel.preOpenTabId = subId
                ASUtils.DispatchButtonEvent(tabMc)
                break

    def difficultLvFix(self, itemId):
        myLv = BigWorld.player().lv
        needLv = ID.data.get(itemId, {}).get('lvReq', myLv)
        if myLv - needLv >= 10:
            return -int((myLv - needLv) * 0.1)
        return 0

    def recommLvFix(self, itemId):
        myLv = BigWorld.player().lv
        needLv = ID.data.get(itemId, {}).get('lvReq', myLv)
        if myLv - needLv >= 1:
            return -(myLv - needLv - 1) * 0.1
        return 0

    def genTrackListInfo(self, detailData):
        ret = []
        trackTypeName = PRCD.data.get('trackTypeName', {})
        trackKeys = ('trackBuy', 'trackDrop', 'trackMake')
        nameKeys = ('buy', 'drop', 'make')
        for i in xrange(len(trackKeys)):
            key = trackKeys[i]
            nameKey = nameKeys[i]
            trackKey = detailData.get(key, ())
            if not trackKey:
                continue
            keyInfo = {}
            keyInfo['typeName'] = trackTypeName.get(nameKey, gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_990)
            keyInfo['typeList'] = trackKey
            ret.append(keyInfo)

        return ret

    def equipGetComp(self, a, b):
        recommLvA = a.get('recommLv', 1)
        recommLvB = b.get('recommLv', 1)
        if recommLvA > recommLvB:
            return -1
        if recommLvA < recommLvB:
            return 1
        minLvA = a.get('minLv', 1)
        minLvB = b.get('minLv', 1)
        if minLvA > minLvB:
            return -1
        if minLvA < minLvB:
            return 1
        return 1

    def getEquipGetDetailInfo(self, part, equipedId):
        precdd = PRECD.data
        school = BigWorld.player().school
        detailIds = precdd.get((school, part), {}).get('itemId', ())
        if type(detailIds) != tuple:
            return []
        detailInfos = []
        pregdd = PREGD.data
        myLv = BigWorld.player().lv
        for detailId in detailIds:
            info = {}
            detailData = pregdd.get(detailId, {})
            if myLv < detailData.get('minLv', 1):
                continue
            if detailData.has_key('recommItemId'):
                recommItemId = detailData['recommItemId']
                info.update(uiUtils.getGfxItemById(recommItemId))
                info['itemName'] = ID.data.get(recommItemId, {}).get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
            else:
                info['itemName'] = ''
            desc = gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1041
            diffLv = detailData.get('difficultyLv', 1)
            if type(diffLv) == str:
                desc = diffLv
            else:
                difficultLv = max(diffLv + self.difficultLvFix(detailData.get('recommItemId', 0)), 0)
                difficultDesc = PRCD.data.get('equipGetDifficultDesc', {})
                for diffLvRange in difficultDesc:
                    if type(diffLvRange) != tuple:
                        continue
                    if len(diffLvRange) != 2:
                        continue
                    if difficultLv >= diffLvRange[0] and difficultLv <= diffLvRange[1]:
                        desc = difficultDesc[diffLvRange]
                        break

            info['title'] = detailData.get('title', '')
            info['difficultyLv'] = desc
            info['recommLv'] = max(detailData.get('recommLv', 1) + self.recommLvFix(detailData.get('recommItemId', 0)), 0)
            info['trackList'] = self.genTrackListInfo(detailData)
            if detailData.get('recommItemId', 0) == equipedId:
                info['title'] += gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1066
            detailInfos.append(info)

        detailInfos.sort(self.equipGetComp)
        count = min(len(detailInfos), 6)
        return detailInfos[:count]

    def getCommDetailInfo(self, detailData):
        commDetailInfo = []
        myLv = BigWorld.player().lv
        for i in range(3):
            index = i + 1
            blockInfo = {}
            blockInfo['extraDesc'] = ''
            blockInfo['title'] = detailData.get('block%dName' % index, gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1083)
            blockInfo['desc1'] = detailData.get('block%dDesc1' % index, '')
            blockInfo['desc2'] = detailData.get('block%dDesc2' % index, '')
            blockInfo['desc3'] = detailData.get('block%dDesc3' % index, '')
            blockInfo['desc4'] = detailData.get('block%dDesc4' % index, '')
            blockInfo['trackList'] = detailData.get('block%dSeek' % index, ())
            if i != 2:
                commDetailInfo.append(blockInfo)
                continue
            blockInfo['extraDesc'] = detailData.get('block%dCtrlText' % index, '')
            blockInfo['trackList'] = []
            blockInfo['block2trackList'] = self.genTrackListInfo(detailData)
            for j in range(3):
                lvIndex = j + 1
                lvRange = detailData.get('block3lv' + str(lvIndex), (1, 1))
                if type(lvRange) != tuple or len(lvRange) != 2:
                    continue
                if myLv < lvRange[0] or myLv > lvRange[1]:
                    continue
                items = detailData.get('block3Item' + str(lvIndex), ())
                materialsInfo = [ uiUtils.getGfxItemById(itemId) for itemId in items ]
                blockInfo['materials'] = materialsInfo
                blockInfo['desc2'] = detailData.get('block3OutputName', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1111)
                blockInfo['desc3'] = detailData.get('block3Output' + str(lvIndex), '')
                break

            commDetailInfo.append(blockInfo)

        return commDetailInfo

    def getEquipJingLianInfo(self, part):
        equip = BigWorld.player().equipment[part]
        if equip:
            enhLv = getattr(equip, 'enhLv', 0)
            maxEnhLv = getattr(equip, 'maxEnhlv', 0)
            if maxEnhLv <= 0:
                return ''
            else:
                return str(int(enhLv * 100 / maxEnhLv)) + '%'
        else:
            return ''

    def getJingLianStar(self, equip):
        enhLv = getattr(equip, 'enhLv', 0)
        if enhLv <= 0:
            return (0, 0)
        if not hasattr(equip, 'enhanceRefining'):
            return (0, 0)
        sumRef = sum(equip.enhanceRefining.values())
        star = uiUtils.getEquipStar(equip)
        fakeStar = star
        if not self.maxEnhancePerfect.has_key(enhLv):
            self.initMaxEnhPerfectData()
        if fakeStar == 10 and sumRef < self.maxEnhancePerfect.get(enhLv, 0):
            fakeStar -= 1
        return (star, fakeStar)

    def getEquipJingLianDetailInfo(self, part):
        detailData = PRSD.data.get((TAB_ID_EQUIP, TAB_ID_JINGLIAN), {})
        commDetailInfo = self.getCommDetailInfo(detailData)
        equip = BigWorld.player().equipment[part]
        if equip:
            enhLv = getattr(equip, 'enhLv', 0)
            maxEnhLv = getattr(equip, 'maxEnhlv', 0)
            equipJingLianExtraDesc = PRCD.data.get('equipJingLianExtraDesc', {})
            commDetailInfo[0]['enhLv'] = enhLv
            if enhLv > 0:
                commDetailInfo[0]['desc1'] += str(enhLv)
            elif maxEnhLv <= 0:
                commDetailInfo[0]['desc1'] += PRCD.data.get('cannotEnhanceTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1167)
            else:
                commDetailInfo[0]['desc1'] += PRCD.data.get('noEnhanceTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1169)
            if maxEnhLv > 0 and enhLv >= maxEnhLv:
                enhLv = 99
            for lvRange in equipJingLianExtraDesc:
                if type(lvRange) != tuple or len(lvRange) != 2:
                    continue
                if enhLv < lvRange[0] or enhLv > lvRange[1]:
                    continue
                commDetailInfo[0]['extraDesc'] = equipJingLianExtraDesc[lvRange]
                break

        else:
            commDetailInfo[0]['desc1'] = PRCD.data.get('noEquipTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1184)
            commDetailInfo[0]['enhLv'] = 0
        if equip:
            star, fakeStar = self.getJingLianStar(equip)
            commDetailInfo[1]['perfectLv'] = star
            equipJingLianPerfectExtraDesc = PRCD.data.get('equipJingLianPerfectExtraDesc', {})
            if maxEnhLv <= 0:
                commDetailInfo[1]['desc1'] += PRCD.data.get('cannotEnhanceTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1167)
            elif enhLv <= 0:
                commDetailInfo[1]['desc1'] += PRCD.data.get('noEnhanceTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1169)
            for lvRange in equipJingLianPerfectExtraDesc:
                if type(lvRange) != tuple or len(lvRange) != 2:
                    continue
                if fakeStar < lvRange[0] or fakeStar > lvRange[1]:
                    continue
                commDetailInfo[1]['extraDesc'] = equipJingLianPerfectExtraDesc[lvRange]
                break

        else:
            commDetailInfo[1]['desc1'] = PRCD.data.get('noEquipTips', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1184)
            commDetailInfo[1]['perfectLv'] = 0
        return commDetailInfo

    def getEquipJuexingInfo(self, part):
        p = BigWorld.player()
        equip = p.equipment[part]
        if not equip:
            return []
        if not hasattr(equip, 'enhJuexingData'):
            return []
        jueXingPos = 0
        enhJueXing = ''
        enhJueXingFinalList = []
        enhJueXingList = [ [key, val] for key, val in equip.enhJuexingData.items() ]
        enhJueXingList.sort(key=lambda k: k[0])
        enhJueXingTitle = SCD.data.get('enhJueXingTitle', (gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227,
         gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_1,
         gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_2,
         gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_3))
        for key in enhJueXingList:
            if not key[1]:
                continue
            needGray = False
            hasNotIn = False
            juexingDataList = key[1]
            title = enhJueXingTitle[jueXingPos]
            dataForEj = utils.getEquipEnhJuexingPropData(equip.equipType, equip.equipSType, key[0], equip.enhanceType)
            juexingStep = utils.getJuexingDataStep(equip, key[0], juexingDataList[0], utils.getEquipEnhJuexingPyData())
            for j in juexingDataList:
                if j[0] not in dataForEj:
                    hasNotIn = True
                    break

            enhMaxLv = ED.data.get(equip.id, {}).get('maxEnhlv', 0)
            if key[0] > getattr(equip, 'enhLv', 0) or hasNotIn or key[0] > enhMaxLv:
                needGray = True
            if needGray:
                enhJueXing += "<font color =\'#808080\'>" + title + ' '
            else:
                enhJueXing += title + ' '
            for juexingData in juexingDataList:
                pType = juexingData[1]
                info = EPRD.data.get(juexingData[0], {})
                jueXingNum = juexingData[2]
                if juexingData[0] in itemToolTipUtils.PROPS_SHOW_SHRINK:
                    jueXingNum = round(jueXingNum / 100.0, 1)
                enhJueXing += info['name'] + '  +'
                enhJueXing += itemToolTipUtils.formatProp(jueXingNum, pType, info.get('showType', 0))

            if needGray:
                enhJueXing += gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1266
            else:
                enhJueXing += '</font>'
            enhJueXingFinalList.append([enhJueXing, juexingStep])
            enhJueXing = ''
            jueXingPos += 1

        return enhJueXingFinalList

    def getEquipJuexingDetailInfo(self, part):
        detailData = PRSD.data.get((TAB_ID_EQUIP, TAB_ID_JUEXING), {})
        commDetailInfo = self.getCommDetailInfo(detailData)
        return commDetailInfo

    def getEquipPrefixInfo(self, part):
        p = BigWorld.player()
        equip = p.equipment[part]
        if not equip:
            return ''
        if not hasattr(equip, 'prefixInfo'):
            return ''
        eppdd = EPPD.data.get(equip.prefixInfo[0], [])
        for prefixItem in eppdd:
            if prefixItem['id'] == equip.prefixInfo[1]:
                return prefixItem['name'][:-2]

    def getEquipStarInfo(self, part):
        starInfo = {'starExp': 0,
         'starLv': 0,
         'maxStarLv': 0,
         'activeStarLv': 0,
         'inactiveStarLv': 0,
         'needExp': 0}
        p = BigWorld.player()
        equip = p.equipment[part]
        if not equip:
            return starInfo
        for starKey in starInfo:
            starInfo[starKey] = getattr(equip, starKey, 0)

        starInfo['needExp'] = equip._getEquipStarUpExp()
        return starInfo

    def getEquipSlotDetailInfo(self, part):
        detailData = PRSD.data.get((TAB_ID_EQUIP, TAB_ID_SLOT), {})
        commDetailInfo = self.getCommDetailInfo(detailData)
        return commDetailInfo

    def getEquipSlotInfo(self, part):
        slotsInfo = {}
        yinSlotList = slotsInfo.setdefault('yinSlot', [])
        yangSlotList = slotsInfo.setdefault('yangSlot', [])
        maxSlotCount = gameglobal.rds.ui.equipGem.slotMaxCount
        p = BigWorld.player()
        equip = p.equipment[part]
        if not equip:
            return slotsInfo
        else:
            for i in range(maxSlotCount):
                yinSlotData = equip.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
                if yinSlotData != None:
                    yinSlot = {}
                    yinSlot['gem'] = uiUtils.getGfxItemById(yinSlotData.gem.id) if yinSlotData.gem else {}
                    yinSlot['state'] = yinSlotData.state
                    yinSlot['tips'] = itemToolTipUtils.getBaoShiDesc(yinSlotData)
                    yinSlotList.append(yinSlot)
                yangSlotData = equip.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
                if yangSlotData != None:
                    yangSlot = {}
                    yangSlot['gem'] = uiUtils.getGfxItemById(yangSlotData.gem.id) if yangSlotData.gem else {}
                    yangSlot['state'] = yangSlotData.state
                    yangSlot['tips'] = itemToolTipUtils.getBaoShiDesc(yangSlotData)
                    yangSlotList.append(yangSlot)

            return slotsInfo

    def getEquipStarDetailInfo(self, part):
        detailData = PRSD.data.get((TAB_ID_EQUIP, TAB_ID_STAR), {})
        commDetailInfo = self.getCommDetailInfo(detailData)
        return commDetailInfo

    def getEquipPrefixDetailInfo(self, part):
        detailData = PRSD.data.get((TAB_ID_EQUIP, TAB_ID_PREFIX), {})
        commDetailInfo = self.getCommDetailInfo(detailData)
        return commDetailInfo

    def onGetEquipPartInfo(self, *arg):
        ret = {}
        equipTabId = int(arg[3][0].GetNumber())
        equipment = BigWorld.player().equipment
        equipPartOrder = PRCD.data.get('equipPartOrder', (9, 10, 0, 1, 4, 3, 2, 6, 21, 22, 7, 8))
        equipPartName = PRCD.data.get('equipPartName', {})
        equipPartInfo = []
        if equipTabId == TAB_ID_SLOT:
            equipPartOrder = PRCD.data.get('wenyinEquipPartOrder', (9, 10, 0, 1, 4, 3, 2))
        for part in equipPartOrder:
            partInfo = {}
            equipedId = 0
            partItem = equipment[part]
            if not partItem:
                partInfo['empty'] = True
            else:
                partInfo['empty'] = False
                equipedId = partItem.id
                partInfo.update(uiUtils.getGfxItem(partItem, location=const.ITEM_IN_EQUIPMENT))
            partInfo['partId'] = part
            partInfo['partName'] = equipPartName.get(part, '')
            if equipTabId == TAB_ID_GET:
                partInfo['detailInfo'] = self.getEquipGetDetailInfo(part, equipedId)
            elif equipTabId == TAB_ID_JINGLIAN:
                partInfo['detailInfo'] = self.getEquipJingLianDetailInfo(part)
                partInfo['extraInfo'] = self.getEquipJingLianInfo(part)
            elif equipTabId == TAB_ID_JUEXING:
                partInfo['detailInfo'] = self.getEquipJuexingDetailInfo(part)
                partInfo['extraInfo'] = self.getEquipJuexingInfo(part)
            elif equipTabId == TAB_ID_PREFIX:
                partInfo['detailInfo'] = self.getEquipPrefixDetailInfo(part)
                partInfo['extraInfo'] = self.getEquipPrefixInfo(part)
            elif equipTabId == TAB_ID_STAR:
                partInfo['detailInfo'] = self.getEquipStarDetailInfo(part)
                partInfo['extraInfo'] = self.getEquipStarInfo(part)
            elif equipTabId == TAB_ID_SLOT:
                partInfo['detailInfo'] = self.getEquipSlotDetailInfo(part)
                partInfo['extraInfo'] = self.getEquipSlotInfo(part)
            else:
                partInfo['detailInfo'] = []
            equipPartInfo.append(partInfo)

        ret['equipPartList'] = equipPartInfo
        ret['defSelectPartId'] = PRCD.data.get('equipDefPart', 9)
        return uiUtils.dict2GfxDict(ret, True)

    def onSearchItemInSprite(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        itemName = ID.data.get(itemId, {}).get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
        self.searchInSprite(itemName)

    def searchInSprite(self, keyWord):
        gameglobal.rds.ui.help.show(keyWord)

    def getSkillDetailInfo(self, skillTabId):
        detailData = PRSD.data.get((TAB_ID_SKILL, skillTabId), {})
        return self.getCommDetailInfo(detailData)

    def getSummonSpriteDetailInfo(self, skillTabId):
        detailData = PRSD.data.get((TAB_ID_SUMMON_SPRITE, skillTabId), {})
        return self.getCommDetailInfo(detailData)

    def onGetSkillTabInfo(self, *arg):
        if self.tabIdx == TAB_ID_SUMMON_SPRITE:
            return self.onGetSummonSpriteTabInfo()
        ret = {}
        tabList = []
        tabOrder = PRCD.data.get('skillTabOrder', (301, 302, 303))
        tabNames = PRCD.data.get('equipTabName', {})
        showLimit = PRCD.data.get('equipTabShowLimit', {})
        for tabId in tabOrder:
            tabInfo = {}
            tabInfo['tabId'] = tabId
            tabInfo['tabName'] = tabNames.get(tabId, '')
            if not tabInfo['tabName']:
                continue
            if not self.tabShowCheck(showLimit.get(tabId, {})):
                continue
            tabInfo['detailInfo'] = self.getSkillDetailInfo(tabId)
            tabList.append(tabInfo)

        ret['tabList'] = tabList
        ret['defSelectTabId'] = PRCD.data.get('skillDefSelectTabId', 301)
        return uiUtils.dict2GfxDict(ret, True)

    def onGetSummonSpriteTabInfo(self, *arg):
        ret = {}
        tabList = []
        tabOrder = PRCD.data.get('summonSpriteOrder', (701, 702, 703))
        tabNames = PRCD.data.get('equipTabName', {})
        showLimit = PRCD.data.get('equipTabShowLimit', {})
        for tabId in tabOrder:
            tabInfo = {}
            tabInfo['tabId'] = tabId
            tabInfo['tabName'] = tabNames.get(tabId, '')
            if not tabInfo['tabName']:
                continue
            if not self.tabShowCheck(showLimit.get(tabId, {})):
                continue
            tabInfo['detailInfo'] = self.getSummonSpriteDetailInfo(tabId)
            tabList.append(tabInfo)

        ret['tabList'] = tabList
        ret['defSelectTabId'] = PRCD.data.get('skillDefSelectTabId', 301)
        return uiUtils.dict2GfxDict(ret, True)

    def onGetRuneInfo(self, *arg):
        if gameglobal.rds.configData.get('enableHierogram', False):
            return self._getHieroInfo()
        else:
            return self._getRuneInfo()

    def _getHieroInfo(self):
        p = BigWorld.player()
        ret = {}
        runePartName = PRCD.data.get('runePartName', {0: gameStrings.TEXT_ITEMTOOLTIPUTILS_1624,
         1: gameStrings.TEXT_UICONST_2539,
         2: gameStrings.TEXT_UICONST_2539_1,
         3: gameStrings.TEXT_UICONST_2539_2})
        ret['detailInfo'] = self.getCommDetailInfo(PRSD.data.get((TAB_ID_RUNE, TAB_ID_RUNEINFO), {}))
        ret['runeDisk'] = {'state': RUNE_SLOT_STATE_EMPTY,
         'partName': runePartName.get(0, '')}
        ret['hundun'] = {'state': RUNE_SLOT_STATE_NONE,
         'partName': runePartName.get(const.RUNE_TYPE_BENYUAN, '')}
        yonghengList = ret.setdefault('yongheng', [])
        for i in range(8):
            info = {'state': RUNE_SLOT_STATE_NONE,
             'partName': runePartName.get(const.RUNE_TYPE_TIANLUN, '')}
            yonghengList.append(info)

        lunhuiList = ret.setdefault('lunhui', [])
        for i in range(4):
            info = {'state': RUNE_SLOT_STATE_NONE,
             'partName': runePartName.get(const.RUNE_TYPE_DILUN, '')}
            lunhuiList.append(info)

        if p.hierogramDict:
            hieroEquipItem = p.hierogramDict.get('hieroEquip', None)
            if hieroEquipItem:
                ret['runeDisk']['state'] = RUNE_SLOT_STATE_FILLED
                ret['runeDisk']['itemInfo'] = uiUtils.getGfxItem(hieroEquipItem, location=const.ITEM_IN_HIEROGRAM)
        hundunNum = 1
        if hundunNum > 0:
            ret['hundun']['state'] = RUNE_SLOT_STATE_EMPTY
        yonghengNum = uiConst.HIERO_TIANLUN_NUM
        for i in range(yonghengNum):
            ret['yongheng'][i]['state'] = RUNE_SLOT_STATE_EMPTY

        lunhuiNum = uiConst.HIERO_DILUN_NUM
        for i in range(lunhuiNum):
            ret['lunhui'][i]['state'] = RUNE_SLOT_STATE_EMPTY

        hieroCrystals = p.hierogramDict.get('hieroCrystals', {})
        for hType, hPart in hieroCrystals:
            if hType == uiConst.HIERO_TYPE_TIANLUN:
                ret['yongheng'][hPart]['itemInfo'] = uiUtils.getGfxItem(hieroCrystals[hType, hPart], location=const.ITEM_IN_HIEROGRAM)
                ret['yongheng'][hPart]['state'] = RUNE_SLOT_STATE_FILLED
            elif hType == uiConst.HIERO_TYPE_DILUN:
                ret['lunhui'][hPart]['itemInfo'] = uiUtils.getGfxItem(hieroCrystals[hType, hPart], location=const.ITEM_IN_HIEROGRAM)
                ret['lunhui'][hPart]['state'] = RUNE_SLOT_STATE_FILLED
            elif hType == uiConst.HIERO_TYPE_BENYUAN:
                ret['hundun']['itemInfo'] = uiUtils.getGfxItem(hieroCrystals[hType, hPart], location=const.ITEM_IN_HIEROGRAM)
                ret['hundun']['state'] = RUNE_SLOT_STATE_FILLED

        return uiUtils.dict2GfxDict(ret, True)

    def _getRuneInfo(self):
        ret = {}
        runePartName = PRCD.data.get('runePartName', {0: gameStrings.TEXT_ITEMTOOLTIPUTILS_1624,
         1: gameStrings.TEXT_UICONST_2539,
         2: gameStrings.TEXT_UICONST_2539_1,
         3: gameStrings.TEXT_UICONST_2539_2})
        ret['detailInfo'] = self.getCommDetailInfo(PRSD.data.get((TAB_ID_RUNE, TAB_ID_RUNEINFO), {}))
        ret['runeDisk'] = {'state': RUNE_SLOT_STATE_EMPTY,
         'partName': runePartName.get(0, '')}
        ret['hundun'] = {'state': RUNE_SLOT_STATE_NONE,
         'partName': runePartName.get(const.RUNE_TYPE_BENYUAN, '')}
        yonghengList = ret.setdefault('yongheng', [])
        for i in range(8):
            info = {'state': RUNE_SLOT_STATE_NONE,
             'partName': runePartName.get(const.RUNE_TYPE_TIANLUN, '')}
            yonghengList.append(info)

        lunhuiList = ret.setdefault('lunhui', [])
        for i in range(4):
            info = {'state': RUNE_SLOT_STATE_NONE,
             'partName': runePartName.get(const.RUNE_TYPE_DILUN, '')}
            lunhuiList.append(info)

        runeEquip = BigWorld.player().runeBoard.runeEquip
        if not runeEquip:
            return uiUtils.dict2GfxDict(ret, True)
        ret['runeDisk']['state'] = RUNE_SLOT_STATE_FILLED
        ret['runeDisk']['itemInfo'] = uiUtils.getGfxItem(runeEquip, location=const.ITEM_IN_RUNEBOARD)
        hundunNum = runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_BENYUAN)
        if hundunNum > 0:
            ret['hundun']['state'] = RUNE_SLOT_STATE_EMPTY
        yonghengNum = runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_TIANLUN)
        for i in range(yonghengNum):
            ret['yongheng'][i]['state'] = RUNE_SLOT_STATE_EMPTY

        lunhuiNum = runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_DILUN)
        for i in range(lunhuiNum):
            ret['lunhui'][i]['state'] = RUNE_SLOT_STATE_EMPTY

        for runeDataVal in runeEquip.runeData:
            if not runeDataVal.item:
                continue
            appendInfo = {'lvName': ''}
            if runeDataVal.runeSlotsType == const.RUNE_TYPE_BENYUAN:
                ret['hundun']['itemInfo'] = uiUtils.getGfxItem(runeDataVal.item, location=const.ITEM_IN_RUNEBOARD, appendInfo=appendInfo)
                ret['hundun']['state'] = RUNE_SLOT_STATE_FILLED
            elif runeDataVal.runeSlotsType == const.RUNE_TYPE_TIANLUN:
                ret['yongheng'][runeDataVal.part]['itemInfo'] = uiUtils.getGfxItem(runeDataVal.item, location=const.ITEM_IN_RUNEBOARD, appendInfo=appendInfo)
                ret['yongheng'][runeDataVal.part]['state'] = RUNE_SLOT_STATE_FILLED
            elif runeDataVal.runeSlotsType == const.RUNE_TYPE_DILUN:
                ret['lunhui'][runeDataVal.part]['itemInfo'] = uiUtils.getGfxItem(runeDataVal.item, location=const.ITEM_IN_RUNEBOARD, appendInfo=appendInfo)
                ret['lunhui'][runeDataVal.part]['state'] = RUNE_SLOT_STATE_FILLED

        return uiUtils.dict2GfxDict(ret, True)

    def onOpenRuneHelp(self, *arg):
        school = BigWorld.player().school
        schoolName = SD.data.get(school, {}).get('name', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1597)
        keyWord = schoolName + gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1598
        self.searchInSprite(keyWord)

    def btnClickListener(self, *args):
        e = ASObject(args[3][0])
        name = e.target.name
        if name.index('tabBtn') == 0:
            if self.lastSelTab:
                self.lastSelTab.selected = False
            e.target.selected = True
            self.lastSelTab = e.target

    def handleOverViewItemMouseOver(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.name in ('itemSlot', 'lowScore', 'highScore'):
            e.currentTarget.parent.selectedMc.visible = True
        else:
            e.currentTarget.selectedMc.visible = True

    def handleOverViewItemMouseOut(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.name in ('itemSlot', 'lowScore', 'highScore'):
            e.currentTarget.parent.selectedMc.visible = False
        else:
            e.currentTarget.selectedMc.visible = False

    def getSpriteAptitudeMargin(self, spriteInfo, aptitudeName):
        spriteId = spriteInfo.get('spriteId', 0)
        props = spriteInfo.get('props', {})
        aptitude = props.get(aptitudeName, 0)
        aptitudeOrigin = utils.getAptitudeMin(spriteId, aptitudeName)
        return (aptitude, aptitudeOrigin)

    def getLearnedSkillNumWithHigh(self, skillInfo):
        lowSkillNum, highSkillNum, ultimateSkillNum = (0, 0, 0)
        for it in skillInfo.get('learns', []):
            if it.get('slot', None) in (const.SSPRITE_SKILL_SLOT_NO_PROTECT, const.SSPRITE_SKILL_SLOT_PROTECT):
                learnSkillHigh = SSSD.data.get(it.get('id', 0), {}).get('learnSkillHigh', gametypes.SPRITE_LEARN_SKILL_LOW)
                if learnSkillHigh == gametypes.SPRITE_LEARN_SKILL_ULTIMATE:
                    ultimateSkillNum += 1
                elif learnSkillHigh == gametypes.SPRITE_LEARN_SKILL_HIGH:
                    highSkillNum += 1
                elif gametypes.SPRITE_LEARN_SKILL_LOW:
                    lowSkillNum += 1

        return (lowSkillNum, highSkillNum, ultimateSkillNum)

    def getSummonSpriteAptitudeDic(self, spriteInfo):
        attrDic = {}
        aptitudePw, aptitudePwLow = self.getSpriteAptitudeMargin(spriteInfo, 'aptitudePw')
        aptitudeAgi, aptitudeAgiLow = self.getSpriteAptitudeMargin(spriteInfo, 'aptitudeAgi')
        aptitudeSpr, aptitudeSprLow = self.getSpriteAptitudeMargin(spriteInfo, 'aptitudeSpr')
        aptitudePhy, aptitudePhyLow = self.getSpriteAptitudeMargin(spriteInfo, 'aptitudePhy')
        aptitudeInt, aptitudeIntLow = self.getSpriteAptitudeMargin(spriteInfo, 'aptitudeInt')
        skillInfo = spriteInfo.get('skills', {})
        props = spriteInfo.get('props', {})
        famiEffLv = props.get('famiEffLv', 0)
        attrDic['aptitudePwLow'] = aptitudePwLow
        attrDic['aptitudeAgiLow'] = aptitudeAgiLow
        attrDic['aptitudeSprLow'] = aptitudeSprLow
        attrDic['aptitudePhyLow'] = aptitudePhyLow
        attrDic['aptitudeIntLow'] = aptitudeIntLow
        attrDic['lv'] = props.get('lv', 1)
        attrDic['bonusNum'] = len(skillInfo.get('bonus', []))
        attrDic['naturalLv'] = utils.getEffLvBySpriteFamiEffLv(famiEffLv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
        attrDic['naturalNum'] = len(skillInfo.get('naturals', []))
        attrDic['fami'] = props.get('familiar', 0)
        attrDic['famiEffAdd'] = props.get('famiEffAdd', 0)
        attrDic['traitLv'] = utils.getEffLvBySpriteFamiEffLv(famiEffLv, 'trait', const.DEFAULT_SKILL_LV_SPRITE)
        attrDic['juexing'] = props.get('juexing', 0)
        attrDic['awakeLv'] = utils.getEffLvBySpriteFamiEffLv(famiEffLv, 'awake', const.DEFAULT_SKILL_LV_SPRITE)
        learnsLow, learnsHigh, learnsUltimate = self.getLearnedSkillNumWithHigh(spriteInfo.get('skills', {}))
        attrDic['learnsUltimate'] = learnsUltimate
        attrDic['learnsHigh'] = learnsHigh
        attrDic['learnsLow'] = learnsLow
        attrDic['aptPw'] = aptitudePw
        attrDic['aptAgi'] = aptitudeAgi
        attrDic['aptSpr'] = aptitudeSpr
        attrDic['aptPhy'] = aptitudePhy
        attrDic['aptInt'] = aptitudeInt
        attrDic['growth'] = props.get('baseGrowthRatio', 0)
        attrDic['boneLv'] = props.get('boneLv', 0)
        attrDic['famiExp'] = props.get('famiExp', 0)
        attrDic['famiMaxExp'] = props.get('famiMaxExp', 0)
        attrDic['famiEffLv'] = famiEffLv
        return attrDic

    def getSummonSpriteScoreByFormula(self, spriteInfo, formulaId):
        func = FCD.data.get(formulaId, {}).get('formula', None)
        if func:
            return func(self.getSummonSpriteAptitudeDic(spriteInfo))
        else:
            return 0

    def getSummonSpriteScore(self):
        scoreList = []
        p = BigWorld.player()
        for index, spriteInfo in p.summonSpriteList.iteritems():
            score = [self.getSummonSpriteScoreByFormula(spriteInfo, SUMMON_SPRITE_GET_FORMULA_ID),
             self.getSummonSpriteScoreByFormula(spriteInfo, SUMMON_SPRITE_FAMI_FORMULA_ID),
             self.getSummonSpriteScoreByFormula(spriteInfo, SUMMON_SPRITE_GET_SKILL_FORMULA_ID),
             self.getSummonSpriteScoreByFormula(spriteInfo, SUMMON_SPRITE_APTITTUDE_FORMULA_ID)]
            score.append(sum(score))
            scoreList.append(score)

        scoreList and scoreList.sort(cmp=lambda x, y: cmp(x[4], y[4]), reverse=True)
        score = [0,
         0,
         0,
         0,
         0]
        if scoreList:
            score = scoreList[0]
        if len(scoreList) > 1:
            score[0] += 0.5 * scoreList[1][0]
            score[1] += 0.5 * scoreList[1][1]
            score[2] += 0.5 * scoreList[1][2]
            score[3] += 0.5 * scoreList[1][3]
        score[0] = int(score[0])
        score[1] = int(score[1])
        score[2] = int(score[2])
        score[3] = p.combatScoreList[const.SPRITE_SCORE] - sum(score[:3])
        score[4] = p.combatScoreList[const.SPRITE_SCORE] + p.combatScoreList[const.SPRITE_ACC_SCORE] + p.combatScoreList[const.SPRITE_GROWTH_SCORE]
        return score
