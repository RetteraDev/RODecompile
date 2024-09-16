#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommActivationProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import clientUtils
import const
import gamelog
import sMath
from guis import ui
from item import Item
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import play_recomm_activity_data as PRAD
from data import quest_data as QD
from data import play_recomm_item_data as PRID
from data import quest_loop_data as QLD
from data import sys_config_data as SCD
from data import play_recomm_config_data as PRCD
from data import play_recomm_circle_data as PRCCD
from data import consumable_reverse_data as CRD
from data import challenge_reward_data as CRD1
from data import mall_config_data as MCFD
from data import mall_item_data as MID
from data import bonus_history_check_data as BHCD
from data import world_quest_refresh_data as WQRD
from data import play_recomm_operation_activity_data as PROAD
from data import activation_reward_data as ARD
from data import guild_config_data as GCD
from data import avoid_doing_activity_data as ADAD
from data import wing_world_config_data as WWCD
from data import wing_world_resource_speed_data as WWRSD
from data import wing_world_resource_sprite_slot_data as WWRSSD
from cdata import week_activation_reward_data as WARD
from cdata import evaluate_set_play_recomm_data_export as ESPRD
from cdata import school_entrust_reverse_data as SERD
from cdata import game_msg_def_data as GMDD
from cdata import play_recomm_item_reverse_data as PRIRD
import gametypes
import utils
import pubgUtils
from data import fb_data as FD
from data import fame_data as FAD
SORT_TYPE_PRIVILEGE_BUY = 1
SORT_TYPE_NOT_REVEIVE_REWARD = 2
SORT_TYPE_OPENING = 3
SORT_TYPE_SHOW_ONLY = 4
SORT_TYPE_COMMING_SOON = 5
SORT_TYPE_COMPLETED = 6
BONUS_HISTORY_BONUSID_SET = [gametypes.RECOMMEND_TYPE_SHA_XING,
 gametypes.RECOMMEND_TYPE_BONUS,
 gametypes.RECOMMEND_TYPE_DIGONG_PUZZLE,
 gametypes.RECOMMEND_TYPE_BFY]
DAILY_ITEM_TYPE_DAILY = 1
DAILY_ITEM_TYPE_WEEK = 2
COMPLETE_HINT_FLAG_PASS = 0
COMPLETE_HINT_FLAG_GOING = 1
COMPLETE_HINT_FLAG_FINISH = 2
PLAY_RECOMM_DAILY_LOCATE_ABD = 0
PLAY_RECOMM_DAILY_LOCATE_PRID = 1
BTNINFO_LABEL_INDEX = 0
BTNINFO_SHOW_INDEX = 1
PLAY_RECOMM_GUILD_SIGN_IN_ID = 40009
PLAY_RECOMM_GUILD_BONFIRE_ID = 40010
BAI_DI_SHI_LIAN_PROP_KEY = 'tianyuyanwu'

class PlayRecommActivationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommActivationProxy, self).__init__(uiAdapter)
        self.widget = None
        self.playRecommendedFinishedActivities = []
        self.hofFinishActivities = []
        self.bonusHistory = {}
        self.needGetBonusHistory = True
        self.useFly = False
        self.worldQuestRefreshFilterDict = {}
        self.hadCheckTimer = False
        self.callbackTimer = 0
        self.reset()

    def reset(self):
        self.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.isGotoTab = False
        self.isClickCompleteHint = False
        self.selectedDailyItem = None
        self.selectedDailyId = 0
        self.selectedWeeklyItem = None
        self.selectedWeeklyId = 0
        self.useFly = False
        self.showWeekAdvanceLvItem = True
        self.showDayAdvanceLvItem = True
        self.tipsMc = None
        self.treeCanvas = None
        self.blackCoverItemId = 0

    def initPanel(self, widget):
        self.getDailyRecommConfigInfo()
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.hideActivityTips()
        if self.treeCanvas:
            self.widget.removeChild(self.treeCanvas)
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.mainMC.dailyAndWeekly.getWeeklyRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleGetWeeklyReward, False, 0, True)
        self.widget.mainMC.operationBtn.addEventListener(events.BUTTON_CLICK, self.handleOperationBtnClick, False, 0, True)
        self.widget.mainMC.dailyBtn.addEventListener(events.BUTTON_CLICK, self.handleDailyBtnClick, False, 0, True)
        self.widget.mainMC.weeklyBtn.addEventListener(events.BUTTON_CLICK, self.handleWeeklyBtnClick, False, 0, True)
        self.widget.mainMC.activationPanel.showWeekLoopBtn.addEventListener(events.BUTTON_CLICK, self.handleShowWeekLoppBtnClick, False, 0, True)
        self.widget.mainMC.activationPanel.weekActivation.hideWeekLoopBtn.addEventListener(events.BUTTON_CLICK, self.handleHideWeekLoopBtnClick, False, 0, True)
        self.widget.mainMC.dailyAndWeekly.getDailyRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleGetDailyRewardBtnClick, False, 0, True)
        dailyList = self.widget.mainMC.activationPanel.dailyList
        dailyList.itemRenderer = 'PlayRecommV2Activity_PlayRecomm_DayItem'
        dailyList.itemWidth = 386
        dailyList.itemHeight = 85
        dailyList.column = 2
        dailyList.lableFunction = self.fillDailyItemData
        self.widget.mainMC.activationPanel.weekList.itemRenderer = 'PlayRecommV2Activity_PlayRecomm_DayItem'
        self.widget.mainMC.activationPanel.weekList.itemWidth = 386
        self.widget.mainMC.activationPanel.weekList.itemHeight = 85
        self.widget.mainMC.activationPanel.weekList.column = 2
        self.widget.mainMC.activationPanel.weekList.dataArray = []
        self.widget.mainMC.activationPanel.weekList.lableFunction = self.fillWeekPanelItemH
        completeHint = self.widget.mainMC.activationPanel.completeHint
        completeHint.hint.btnGroup.backBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBackBtn, False, 0, True)
        completeHint.hint.btnGroup.longBackBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBackBtn, False, 0, True)
        completeHint.hint.btnGroup.gotoWeekBtn.addEventListener(events.BUTTON_CLICK, self.handleClickGotoWeekBtn, False, 0, True)
        completeHint.hint.btnGroup.gotoLvUpBtn.addEventListener(events.BUTTON_CLICK, self.handleClickGotoLvUpBtn, False, 0, True)
        self.widget.mainMC.activationPanel.checkBoxUseFly.addEventListener(events.EVENT_SELECT, self.handleSetUseFly, False, 0, True)
        self.widget.mainMC.activationPanel.continueGameBtn.addEventListener(events.BUTTON_CLICK, self.buttonClickEventListener, False, 0, True)
        self.widget.mainMC.activationPanel.exitGameBtn.addEventListener(events.BUTTON_CLICK, self.buttonClickEventListener, False, 0, True)
        self.widget.mainMC.activationPanel.checkBoxAdvanced.addEventListener(events.EVENT_SELECT, self.handleSetAdvanced, False, 0, True)
        self.widget.mainMC.activationPanel.avoidDoingBtn.addEventListener(events.BUTTON_CLICK, self.clickAvoidDoingBtn, False, 0, True)
        if self.uiAdapter.playRecomm.isQuitGame:
            self.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB
        self.uiAdapter.playRecomm.checkDailyCompleteQuestFinish()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTabBtnList()
        if self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB and (BigWorld.player().lv < SCD.data.get('PlayRecommV2OperationTabShowLv', 60) or not gameglobal.rds.configData.get('enableWeekActivation', False)):
            self.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB
        if not self.isGotoTab and self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB and self.isOperationActivityAllDone():
            self.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB
        self.refreshDailyActivation()
        self.refreshWeekActivation()
        self.refreshRecomm(self.activationTabIdx, True)

    def isOperationActivityAllDone(self):
        p = BigWorld.player()
        for key, value in PROAD.data.iteritems():
            startTime = value.get('startTime', None)
            startShowTime = value.get('startShowTime', None)
            endTime = value.get('endTime', None)
            conditionType = value.get('conditionType', gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY)
            if conditionType != gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                if not startTime or not endTime:
                    continue
                if not startShowTime or not utils.inTimeTuplesRange(startShowTime, endTime):
                    continue
            if value.has_key('serverConfigId') and not utils.checkInCorrectServer(value['serverConfigId']):
                continue
            activityInfo = p.weekOperationActivityInfo.get(key, None)
            complete = activityInfo and activityInfo.status
            if conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                continue
            elif conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_SHOW_ONLY:
                continue
            elif utils.inTimeTuplesRange(startTime, endTime):
                if not complete:
                    return False
            elif conditionType == gametypes.OPERATION_ACTIVITY_REFRESH_TYPE_ONCE:
                continue

        return True

    def getWeekActivationInfo(self):
        info = {}
        p = BigWorld.player()
        ard = {}
        for minLv, maxLv in WARD.data.keys():
            if minLv <= p.activationLv <= maxLv:
                ard = WARD.data.get((minLv, maxLv), {})
                break

        if not ard:
            for minLv, maxLv in WARD.data.keys():
                if minLv <= p.lv <= maxLv:
                    ard = WARD.data.get((minLv, maxLv), {})
                    break

        activationMargins = ard.get('activationMargins')
        bonusIds = ard.get('bonusIds')
        crontabStart = ard.get('extraCrontabStart')
        crontabEnd = ard.get('extraCrontabEnd')
        if crontabStart and crontabEnd:
            if utils.inTimeTuplesRange(crontabStart, crontabEnd):
                bonusIdsEx = ard.get('extraBonusIds', ())
            else:
                bonusIdsEx = ()
        else:
            bonusIdsEx = ard.get('extraBonusIds', ())
        if not activationMargins or not bonusIds:
            return info
        stepInfoList = []
        maxValue = activationMargins[-1]
        btnEnabled = False
        bonusLen = min(len(bonusIds), len(activationMargins))
        satisfyCount = 0
        bonusExLen = len(bonusIdsEx)
        for i in xrange(bonusLen):
            activationMargin = activationMargins[i]
            itemInfo = {}
            bonusId = bonusIds[i]
            itemBonus = clientUtils.genItemBonus(bonusId)
            itemId, itemNum = itemBonus[0]
            itemInfo['slotInfo'] = uiUtils.getGfxItemById(itemId, itemNum)
            if i < bonusExLen and bonusIdsEx[i] != 0:
                bonusIdEx = bonusIdsEx[i]
                itemBonusEx = clientUtils.genItemBonus(bonusIdEx)
                itemIdEx, itemNumEx = itemBonusEx[0]
                itemInfo['slotExInfo'] = uiUtils.getGfxItemById(itemIdEx, itemNumEx)
                itemInfo['showSlotEx'] = True
            else:
                itemInfo['showSlotEx'] = False
            if activationMargin <= p.weekActivation:
                itemInfo['value'] = uiUtils.toHtml(str(activationMargin / 1000), '#66CC66')
                satisfyCount += 1
                if bonusId in p.weekActivationRewards:
                    itemInfo['state'] = 'finish'
                    itemInfo['multipleEffectType'] = 'type1'
                    itemInfo['multipleEffectExType'] = 'type1'
                else:
                    itemInfo['state'] = 'normal'
                    itemInfo['effectVisible'] = True
                    btnEnabled = True
            else:
                itemInfo['value'] = activationMargin / 1000
                itemInfo['state'] = 'normal'
                itemInfo['effectVisible'] = False
            stepInfoList.append(itemInfo)

        info['nowPoint'] = p.weekActivation / 1000
        info['maxPoint'] = maxValue / 1000
        info['stepsInfoList'] = stepInfoList
        info['btnEnable'] = btnEnabled
        info['status'] = '%d/3' % satisfyCount
        return info

    def getDailyActivationInfo(self, playSound = False):
        ard = {}
        p = BigWorld.player()
        for minLv, maxLv in ARD.data.keys():
            if minLv <= p.activationLv <= maxLv:
                ard = ARD.data.get((minLv, maxLv), {})
                break

        if not ard:
            for minLv, maxLv in ARD.data.keys():
                if minLv <= p.lv <= maxLv:
                    ard = ARD.data.get((minLv, maxLv), {})
                    break

        activationMargins = ard.get('activationMargins')
        bonusIds = ard.get('bonusIds')
        crontabStart = ard.get('crontabStart')
        crontabEnd = ard.get('crontabEnd')
        if crontabStart and crontabEnd:
            if utils.inDateRange(crontabStart, crontabEnd):
                bonusIdsEx = ard.get('bonusIds2', ())
            else:
                bonusIdsEx = ()
        else:
            bonusIdsEx = ard.get('bonusIds2', ())
        showFreeJuexingRebuildActivation = ard.get('showFreeJuexingRebuildActivation', 0)
        if not activationMargins or not bonusIds:
            return None
        else:
            maxValue = activationMargins[-1]
            itemList = []
            btnEnabled = False
            isMultiple = False
            bonusLen = min(len(bonusIds), len(activationMargins))
            bonusExLen = len(bonusIdsEx)
            marginsLen = len(activationMargins)
            subValue = 1 if marginsLen == bonusLen else 0
            currentValue = 0.0
            lastStepMargin = 0
            for i in xrange(bonusLen):
                activationMargin = activationMargins[i]
                itemInfo = {}
                itemInfo['offset'] = 1.0 - (bonusLen - subValue - i) * 1.0 / marginsLen
                bonusId = bonusIds[i]
                itemBonus = clientUtils.genItemBonus(bonusId)
                itemId, itemNum = itemBonus[0]
                itemInfo['slotInfo'] = uiUtils.getGfxItemById(itemId, itemNum)
                if i < bonusExLen and bonusIdsEx[i] != 0:
                    bonusIdEx = bonusIdsEx[i]
                    itemBonusEx = clientUtils.genItemBonus(bonusIdEx)
                    itemIdEx, itemNumEx = itemBonusEx[0]
                    itemInfo['slotExInfo'] = uiUtils.getGfxItemById(itemIdEx, itemNumEx)
                    itemInfo['showSlotEx'] = True
                else:
                    bonusIdEx = 0
                    itemInfo['showSlotEx'] = False
                if activationMargin <= p.activation:
                    itemInfo['value'] = uiUtils.toHtml(str(activationMargin / 1000), '#66CC66')
                    currentValue += 1.0 / marginsLen
                    if bonusId in p.activationRewards:
                        itemInfo['state'] = 'finish'
                        multiple = p.activationRewards.get(bonusId, 1)
                        isMultiple = True if multiple > 1 else isMultiple
                        itemInfo['multipleEffectType'] = 'type%d' % multiple
                        if bonusIdEx:
                            multiple = p.activationRewards.get(bonusIdEx, 1)
                            isMultiple = True if multiple > 1 else isMultiple
                            itemInfo['multipleEffectExType'] = 'type%d' % multiple
                    else:
                        itemInfo['state'] = 'normal'
                        itemInfo['effectVisible'] = True
                        btnEnabled = True
                else:
                    itemInfo['value'] = activationMargin / 1000
                    itemInfo['state'] = 'normal'
                    itemInfo['effectVisible'] = False
                    currentValue += max(0.0, p.activation - lastStepMargin) * 1.0 / (activationMargin - lastStepMargin) * (1.0 / marginsLen)
                if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False) and activationMargin == showFreeJuexingRebuildActivation:
                    itemInfo['showFree'] = True
                    itemInfo['freeState'] = 'valid' if activationMargin <= p.activation else 'invalid'
                    itemInfo['freeTips'] = SCD.data.get('equipChangeJuexingRebuildFreeTips', '')
                else:
                    itemInfo['showFree'] = False
                lastStepMargin = activationMargin
                itemList.append(itemInfo)

            currentValue += max(0.0, p.activation - lastStepMargin) * 1.0 / (maxValue - lastStepMargin) * (1.0 / marginsLen)
            currentValue = min(100.0, currentValue * 100.0)
            info = {'itemList': itemList,
             'btnEnabled': btnEnabled,
             'currentValue': currentValue,
             'dayActivation': p.activation / 1000,
             'weekActivation': p.weekActivation / 1000,
             'lastWeekActivation': p.lastWeekActivation / 1000}
            if playSound and isMultiple:
                gameglobal.rds.sound.playSound(5635)
            return info

    def refreshDailyActivation(self, playSound = False):
        if not self.widget:
            return
        else:
            self.widget.removeAllInst(self.widget.mainMC.dailyAndWeekly.dailyItemList)
            info = self.getDailyActivationInfo(playSound)
            if not info:
                return
            itemInfo = None
            itemMc = None
            itemLen = len(info['itemList'])
            dailyItemMcList = self.widget.mainMC.dailyAndWeekly.dailyItemList
            for i in xrange(itemLen):
                itemInfo = info['itemList'][i]
                if itemInfo['showSlotEx']:
                    itemMc = self.widget.getInstByClsName('PlayRecommV2Activity_Activation_Item_Small')
                else:
                    itemMc = self.widget.getInstByClsName('PlayRecommV2Activity_Activation_Item')
                itemMc.gotoAndStop(itemInfo['state'])
                if itemInfo['state'] == 'normal':
                    itemMc.effect.visible = itemInfo['effectVisible']
                    if itemInfo['showSlotEx']:
                        itemMc.effectEx.visible = itemInfo['effectVisible']
                    itemMc.canClick = itemInfo['effectVisible']
                else:
                    itemMc.multipleEffect.gotoAndStop(itemInfo['multipleEffectType'])
                    ASUtils.setHitTestDisable(itemMc.multipleEffect, True)
                    ASUtils.setHitTestDisable(itemMc.effect, True)
                    if itemInfo['showSlotEx']:
                        itemMc.multipleEffectEx.gotoAndStop(itemInfo['multipleEffectExType'])
                        ASUtils.setHitTestDisable(itemMc.multipleEffectEx, True)
                    itemMc.canClick = False
                itemMc.value.htmlText = itemInfo['value']
                ASUtils.setHitTestDisable(itemMc.value, True)
                if itemInfo['showFree']:
                    itemMc.juexingRebuildFree.visible = True
                    itemMc.juexingRebuildFree.gotoAndStop(itemInfo['freeState'])
                    if itemInfo['freeState'] == 'valid':
                        itemMc.juexingRebuildFree.addEventListener(events.MOUSE_CLICK, self.handleClickFree, False, 0, True)
                        TipManager.removeTip(itemMc.juexingRebuildFree)
                    else:
                        itemMc.juexingRebuildFree.removeEventListener(events.MOUSE_CLICK, self.handleClickFree)
                        TipManager.addTip(itemMc.juexingRebuildFree, itemInfo['freeTips'])
                else:
                    itemMc.juexingRebuildFree.visible = False
                itemMc.slot.setItemSlotData(itemInfo['slotInfo'])
                itemMc.slot.dragable = False
                if itemInfo['showSlotEx']:
                    itemMc.slotEx.setItemSlotData(itemInfo['slotExInfo'])
                    itemMc.slotEx.dragable = False
                itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickDailyActivatonItem, False, 0, True)
                dailyItemMcList.addChild(itemMc)
                itemMc.x = -195 + 338.0 * itemInfo['offset']
                itemMc.y = -60 if itemInfo['showSlotEx'] else -47

            self.widget.mainMC.dailyAndWeekly.progressBar.thumb.visible = False
            self.widget.mainMC.dailyAndWeekly.progressBar.currentValue = info['currentValue']
            self.widget.mainMC.dailyAndWeekly.dayActivation.text = info['dayActivation']
            self.widget.mainMC.dailyAndWeekly.getDailyRewardBtn.enabled = info['btnEnabled']
            self.widget.mainMC.dailyAndWeekly.dailyHeart.gotoAndStop('daily')
            return

    def refreshWeekActivation(self):
        if not self.widget:
            return
        self.widget.removeAllInst(self.widget.mainMC.dailyAndWeekly.weeklyItemList)
        info = self.getWeekActivationInfo()
        if not info:
            return
        self.widget.mainMC.dailyAndWeekly.weeklyItemList.visible = True
        for i, itemInfo in enumerate(info['stepsInfoList']):
            isShowExtra = itemInfo['showSlotEx']
            itemMc = self.widget.getInstByClsName('PlayRecommV2Activity_Activation_Item_Small' if isShowExtra else 'PlayRecommV2Activity_Activation_Item')
            itemMc.gotoAndStop(itemInfo['state'])
            if itemInfo['state'] == 'normal':
                itemMc.effect.visible = itemInfo['effectVisible']
                ASUtils.setHitTestDisable(itemMc.effect, True)
                if itemInfo['showSlotEx']:
                    itemMc.effectEx.visible = itemInfo['effectVisible']
                    ASUtils.setHitTestDisable(itemMc.effectEx, True)
                itemMc.canClick = itemInfo['effectVisible']
            else:
                itemMc.multipleEffect.gotoAndStop(itemInfo['multipleEffectType'])
                ASUtils.setHitTestDisable(itemMc.multipleEffect, True)
                ASUtils.setHitTestDisable(itemMc.effect, True)
                if itemInfo['showSlotEx']:
                    itemMc.multipleEffectEx.gotoAndStop(itemInfo['multipleEffectExType'])
                    ASUtils.setHitTestDisable(itemMc.multipleEffectEx, True)
                itemMc.canClick = False
            itemMc.value.htmlText = itemInfo['value']
            ASUtils.setHitTestDisable(itemMc.value, True)
            itemMc.juexingRebuildFree.visible = False
            itemMc.slot.setItemSlotData(itemInfo['slotInfo'])
            itemMc.slot.dragable = False
            if itemInfo['showSlotEx']:
                itemMc.slotEx.setItemSlotData(itemInfo['slotExInfo'])
                itemMc.slotEx.dragable = False
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickOperatonItem, False, 0, True)
            self.widget.mainMC.dailyAndWeekly.weeklyItemList.addChild(itemMc)
            itemMc.y = -50 if not isShowExtra else -63
            itemMc.x = -90 + i * 55

        self.widget.mainMC.dailyAndWeekly.weeklyHeartValue.text = info['nowPoint']
        self.widget.mainMC.dailyAndWeekly.weeklyHeart.gotoAndStop('weekly')
        self.widget.mainMC.dailyAndWeekly.getWeeklyRewardBtn.enabled = info['btnEnable']

    def refreshRecomm(self, tabIdx = None, forceRefresh = False):
        if not self.widget:
            return
        tabIdx = self.activationTabIdx if not tabIdx else tabIdx
        if self.activationTabIdx == tabIdx and not forceRefresh:
            return
        self.activationTabIdx = tabIdx
        self.hideAllSubTabs()
        self.widget.mainMC.dailyBtn.selected = tabIdx == uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB
        self.widget.mainMC.operationBtn.selected = tabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.widget.mainMC.weeklyBtn.selected = tabIdx == uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB
        tabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB and self.refreshOperatonRecommItems()
        tabIdx == uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB and self.refreshDailyRecommItems()
        tabIdx == uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB and self.refreshWeeklyRecommItems()
        if tabIdx == uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB or tabIdx == uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB:
            self.widget.mainMC.activationPanel.checkBoxAdvanced.removeEventListener(events.EVENT_SELECT, self.handleSetAdvanced)
            self.widget.mainMC.activationPanel.checkBoxAdvanced.selected = self.showDayAdvanceLvItem if tabIdx == uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB else self.showWeekAdvanceLvItem
            self.widget.mainMC.activationPanel.checkBoxAdvanced.addEventListener(events.EVENT_SELECT, self.handleSetAdvanced, False, 0, True)

    def hideAllSubTabs(self):
        self.widget.mainMC.tipsCtrlTextField.visible = not self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.widget.mainMC.activationPanel.checkBoxAdvanced.visible = not self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.widget.mainMC.activationPanel.avoidDoingBtn.visible = not self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB and gameglobal.rds.configData.get('enableAvoidDoingActivity', False)
        self.widget.mainMC.activationPanel.checkBoxUseFly.visible = not self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.widget.mainMC.activationPanel.exitGameBtn.visible = False
        self.widget.mainMC.activationPanel.continueGameBtn.visible = False
        self.widget.mainMC.activationPanel.operationActivityList.visible = False
        self.widget.mainMC.activationPanel.completeHint.visible = False
        self.widget.mainMC.activationPanel.weekActivation.visible = False
        self.widget.mainMC.activationPanel.dailyList.visible = False
        self.widget.mainMC.activationPanel.weekList.visible = False
        self.widget.mainMC.tipsCtrlTextField.visible = False
        self.widget.removeChild(self.treeCanvas)
        if self.widget.mainMC.activationPanel.checkBoxAdvanced.visible:
            if self.widget.mainMC.activationPanel.avoidDoingBtn.visible:
                self.widget.mainMC.activationPanel.checkBoxAdvanced.x = 150
                self.widget.mainMC.activationPanel.checkBoxUseFly.x = 280
            else:
                self.widget.mainMC.activationPanel.checkBoxAdvanced.x = 6
                self.widget.mainMC.activationPanel.checkBoxUseFly.x = 156
        self.hideActivityTips()

    def getOperationActivationInfo(self):
        infoList = []
        p = BigWorld.player()
        for key, value in PROAD.data.iteritems():
            startTime = value.get('startTime', None)
            startShowTime = value.get('startShowTime', None)
            endTime = value.get('endTime', None)
            conditionType = value.get('conditionType', gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY)
            if conditionType != gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                if not startTime or not endTime:
                    continue
                if not startShowTime or not utils.inTimeTuplesRange(startShowTime, endTime):
                    continue
            if value.has_key('serverConfigId') and not utils.checkInCorrectServer(value['serverConfigId']):
                continue
            info = {}
            activityInfo = p.weekOperationActivityInfo.get(key, None)
            conditionProgress = value.get('conditionProgress', 0)
            nowProgress = 0 if not activityInfo else activityInfo.progress
            nowProgress = min(nowProgress, conditionProgress)
            info['conditionType'] = conditionType
            info['bg'] = 'playRecomm/weekActivation/%s.dds' % value.get('bg', '10016')
            info['conditionProgerss'] = conditionProgress
            info['nowProgress'] = nowProgress
            info['desc'] = value.get('desc', 'desc None')
            info['rewardPoint'] = value.get('rewardWeekActivation', 0) / 1000
            info['key'] = key
            info['gotoText'] = value.get('gotoText', '')
            info['secondDesc'] = value.get('timeDesc', '')
            info['sortOrder'] = value.get('sortOrder', 1)
            info['linkText'] = value.get('linkText', '')
            info['txtTitle'] = value.get('txtTitle', '')
            complete = activityInfo and activityInfo.status
            canGainReward = False
            if conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                info['sortType'] = SORT_TYPE_PRIVILEGE_BUY
                canGainReward = True
            elif conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_SHOW_ONLY:
                info['sortType'] = SORT_TYPE_SHOW_ONLY
                canGainReward = True
            elif utils.inTimeTuplesRange(startTime, endTime):
                if activityInfo and activityInfo.status:
                    info['sortType'] = SORT_TYPE_COMPLETED
                    canGainReward = False
                elif activityInfo and activityInfo.progress >= conditionProgress or conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_REWARD_ONLY and not complete:
                    info['sortType'] = SORT_TYPE_NOT_REVEIVE_REWARD
                    canGainReward = True
                else:
                    info['sortType'] = SORT_TYPE_OPENING
                    canGainReward = False
            elif conditionType == gametypes.OPERATION_ACTIVITY_REFRESH_TYPE_ONCE:
                continue
            elif complete:
                info['sortType'] = SORT_TYPE_COMPLETED
                canGainReward = False
            else:
                info['sortType'] = SORT_TYPE_COMMING_SOON
                canGainReward = False
            rewardBonusId = value.get('rewardBonusId', 0)
            itemList = []
            idCntList = clientUtils.genItemBonus(rewardBonusId)
            for id, cnt in idCntList:
                itemList.append(uiUtils.getGfxItemById(id, cnt))

            info['canGainReward'] = canGainReward
            info['itemList'] = itemList
            infoList.append(info)

        infoList.sort(cmp=self.compInfo)
        return infoList

    def compInfo(self, infoA, infoB):
        if infoA['sortType'] != infoB['sortType']:
            return infoA['sortType'] - infoB['sortType']
        else:
            return infoA['sortOrder'] - infoB['sortOrder']

    def refreshOperatonRecommItems(self):
        if not self.widget or self.activationTabIdx != uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB:
            return
        infoList = self.getOperationActivationInfo()
        self.widget.mainMC.activationPanel.operationActivityList.visible = True
        scrollWnd = self.widget.mainMC.activationPanel.operationActivityList
        self.widget.removeAllInst(scrollWnd.canvas)
        scrollWnd.validateNow()
        offsetX = offsetY = 0
        if not infoList:
            itemMc = self.widget.getInstByClsName('PlayRecommV2Activity_PlayRecommWeekActivation_Banner_None')
            itemMc.x = offsetX
            itemMc.y = offsetY
            scrollWnd.setContent(itemMc)
            offsetY += itemMc.height
            return
        for info in infoList:
            itemMc = self.widget.getInstByClsName('PlayRecommV2Activity_PlayRecommWeekActivation_Banner_Item')
            itemMc.icon.bonusType = 'weekActivation'
            if info['sortType'] == SORT_TYPE_COMMING_SOON:
                itemMc.txtType.text = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_COMMING_SOON
            elif info['sortType'] in (SORT_TYPE_OPENING, SORT_TYPE_NOT_REVEIVE_REWARD, SORT_TYPE_SHOW_ONLY):
                itemMc.txtType.text = gameStrings.PLAY_RECOMM_WEEK_ACTIVIATION_OPENING
            else:
                itemMc.txtType.text = ''
            itemMc.bg.fitSize = True
            itemMc.bg.loadImage(info['bg'])
            itemMc.txtContent.htmlText = info['desc']
            itemMc.txtTime.htmlText = info.get('secondDesc', '')
            if not int(info['conditionProgerss']):
                itemMc.progressBar.visible = False
            else:
                itemMc.progressBar.currentValue = int(info['nowProgress'])
                itemMc.progressBar.maxValue = int(info['conditionProgerss'])
                itemMc.progressBar.visible = info['sortType'] != SORT_TYPE_PRIVILEGE_BUY
            if not info['rewardPoint']:
                itemMc.icon.visible = False
                itemMc.count.visible = False
            else:
                itemMc.icon.visible = True
                itemMc.count.visible = True
            itemMc.count.text = info['rewardPoint']
            itemList = info['itemList']
            itemMc.gainRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleGainActivityRewardBtnClick, False, 0, True)
            itemMc.gainRewardBtn.canGainReward = info['canGainReward']
            itemsLen = len(itemList)
            if itemsLen == 2:
                itemMc.item0.x = 611
                itemMc.item1.x = 662
            elif itemsLen == 1:
                itemMc.item0.x = 611 + 51 / 2
            for i in xrange(2):
                slot = itemMc.getChildByName('item%d' % i)
                slot.dragable = False
                if i < itemsLen:
                    slot.visible = True
                    slot.setItemSlotData(itemList[i])
                else:
                    slot.visible = False

            itemMc.gainRewardBtn.dataKey = info['key']
            itemMc.gotoText.visible = False
            itemMc.gainRewardBtn.linkText = ''
            itemMc.gainRewardBtn.label = info['gotoText']
            if info['sortType'] == SORT_TYPE_SHOW_ONLY:
                itemMc.gainRewardBtn.visible = True
            itemMc.succText.visible = info['sortType'] == SORT_TYPE_COMPLETED
            if info['sortType'] == SORT_TYPE_PRIVILEGE_BUY:
                itemMc.gainRewardBtn.visible = True
                itemMc.gainRewardBtn.label = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_GOTO
            elif info['sortType'] == SORT_TYPE_NOT_REVEIVE_REWARD:
                itemMc.gainRewardBtn.visible = True
                itemMc.gainRewardBtn.label = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_GAIN_REWARD
            elif info['sortType'] == SORT_TYPE_OPENING:
                itemMc.gainRewardBtn.visible = True
                itemMc.gainRewardBtn.linkText = info['linkText']
            elif info['sortType'] == SORT_TYPE_SHOW_ONLY:
                itemMc.gainRewardBtn.visible = True
                itemMc.gainRewardBtn.linkText = info['linkText']
            else:
                itemMc.gainRewardBtn.visible = False
            itemMc.succText.visible = info['sortType'] == SORT_TYPE_COMPLETED
            itemMc.txtTitle.htmlText = info['txtTitle']
            if info['txtTitle'] and itemMc.txtType.text:
                itemMc.tagBg.visible = True
                itemMc.txtType.visible = True
            else:
                itemMc.tagBg.visible = False
                itemMc.txtType.visible = False
            itemMc.y = offsetY
            itemMc.x = offsetX
            scrollWnd.setContent(itemMc)
            offsetY += 120

        scrollWnd.refreshHeight(offsetY + 20)

    def getDailyItems(self, locate, treeId = None, needRefreshFubenTimes = True):
        iprdd = PRID.data
        result = []
        p = BigWorld.player()
        if needRefreshFubenTimes:
            p.cell.refreshFubenTimesOnCD()
            p.cell.querySchoolTopDpsTimesWeekly()
        for prid, rdata in iprdd.iteritems():
            try:
                rType = rdata.get('locate', 1)
                if rType != locate:
                    continue
                inTree = rdata.get('inTree')
                if not treeId and inTree:
                    continue
                if treeId and not inTree:
                    continue
                if treeId and inTree != treeId:
                    continue
                if rdata.get('worldQuestRefreshFilter', 0):
                    if not gameglobal.rds.configData.get('enableWorldQuestLoopRefresh', False):
                        continue
                    if inTree and prid not in self.worldQuestRefreshFilterDict:
                        continue
                if rdata.has_key('checkGameConfig'):
                    if not gameglobal.rds.configData.get(rdata.get('checkGameConfig', ''), False):
                        continue
                if not self.checkShowDailyItem(prid, rdata):
                    continue
                if rdata.get('checkServerEvent', None):
                    serverEventIds = rdata.get('checkServerEvent', 0)
                    if self.checkServerProgressOutOfTime(serverEventIds):
                        continue
                showTime = rdata.get('showTime')
                hideTime = rdata.get('hideTime')
                weekSet = rdata.get('weekSet', 0)
                if showTime and hideTime:
                    if not utils.inCrontabRange(showTime, hideTime, weekSet=weekSet):
                        continue
                if utils.getEnableCheckServerConfig():
                    serverConfigId = rdata.get('serverConfigId', 0)
                    if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                        continue
                if prid == 10007 and utils.getServerOpenDays() <= 7:
                    continue
                minlv, maxlv = rdata.get('lv')
                if p.lv > maxlv:
                    continue
                if rType == 1:
                    showLv = self.showDayAdvanceLvItem
                else:
                    showLv = self.showWeekAdvanceLvItem
                hideByLv = rdata.get('hideByLv')
                if (not showLv or hideByLv) and rdata.get('lv'):
                    if p.lv < minlv and not inTree:
                        continue
                if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
                    if rdata.get('hideInNovice', 0):
                        continue
                if not self.isDailyActiveShow(rdata):
                    continue
                if not self.checkSchool(rdata):
                    continue
                funcType = rdata.get('funcType')
                if not self.checkDailyItemByFuncType(funcType):
                    continue
                if funcType == gametypes.RECOMMEND_TYPE_QUMO:
                    items = self.getDailyQumoItems(funcType, prid, rdata)
                    for item in items:
                        result.append(item)

                else:
                    result.append(self.getDailyInfoByType(funcType, prid, rdata))
            except Exception as e:
                gamelog.error('getDailyItems Error', prid, e.message)

        result.sort(key=lambda x: x['weight'], reverse=True)
        return result

    def checkShowDailyItem(self, prid, rdata):
        if rdata.get('checkGameConfig', '') == 'enableSpriteChallenge':
            from guis import spriteChallengeHelper
            if not spriteChallengeHelper.getInstance().inSpriteChallengeSeason():
                return False
        return True

    def getDailyQumoItems(self, funcType, prid, rdata):
        p = BigWorld.player()
        items = []
        qldd = QLD.data
        qdd = QD.data
        for questLoopId, info in p.questLoopInfo.iteritems():
            qldata = qldd.get(questLoopId)
            if not qldata:
                continue
            activityType = rdata.get('funcParam', (0,))[0]
            if qldata.get('activityType') == activityType:
                info = p.questLoopInfo.get(questLoopId)
                if not info:
                    qId = qldd.get(questLoopId, {}).get('quests', [0])[0]
                else:
                    qId = info.getCurrentQuest()
                available = questLoopId in p.questInfoCache.get('available_taskLoops', [])
                finishedLoopQuest = False
                if not qId and available:
                    qId = qldd.get(questLoopId, {}).get('quests', [0])[0]
                elif not qId and not available:
                    finishedLoopQuest = True
                itemInfo = self.getDailyInfoByType(funcType, prid, rdata)
                qData = qdd.get(qId, {})
                name = qData.get('name', '')
                shortDesc = qData.get('shortDesc', '')
                seekId = qData.get('playRecommSeekId', '1')
                quickGroup = qData.get('quickGroup')
                if not quickGroup:
                    itemInfo['btn2Label'] = ''
                if name and shortDesc:
                    itemInfo['btn1Tips'] = name + '\n' + shortDesc
                    itemInfo['seekId'] = str(seekId)
                    itemInfo['questId'] = qId
                minlv, maxlv = rdata.get('lv')
                if p.lv < minlv:
                    itemInfo['comFlag'][0] = 0
                elif finishedLoopQuest:
                    itemInfo['comFlag'][0] = 2
                else:
                    itemInfo['comFlag'][0] = 1
                itemInfo['completeHintFlag'] = self.getCompleteHintFlag(rdata, itemInfo['comFlag'])
                items.append(itemInfo)

        return items

    def getDailyInfoByType(self, funcType, prid, rdata):
        p = BigWorld.player()
        ret = {}
        ret['id'] = prid
        ret['name'] = rdata.get('name', '')
        moreInfoId = rdata.get('moreInfoId', 0)
        ret['moreInfoId'] = moreInfoId
        ret['mIdMapRefActId'] = PRAD.data.get(moreInfoId, {}).get('refActivityId', 0)
        ret['funcType'] = rdata.get('funcType')
        ret['isTree'] = len(rdata.get('treeChild', ())) > 0 and p.lv >= rdata.get('lv', 0)[0]
        ret['treeChild'] = rdata.get('treeChild', ()) if ret['isTree'] else ()
        params = self.getDailyMainParam(prid, funcType, rdata)
        ret['mainDesc'] = self.getMainDesc(funcType, prid, rdata, params)
        ret['mainDescTip'] = self.getMainDescTip(rdata)
        ret['timeDesc'] = self.getDailyTimeDesc(rdata)
        ret['timeDescTips'] = self.getTimeDescTip(rdata)
        ret['weekFlag'] = 0
        ret['itemData'] = self.getDailyIcon(rdata, prid)
        ret['comFlag'] = self.getComFlag(funcType, prid, rdata, params)
        ret['activeFlag'] = self.getActiveFlag(rdata, ret['comFlag'])
        ret['completeHintFlag'] = self.getCompleteHintFlag(rdata, ret['comFlag'])
        btn1Info = self.getBtn1Info(funcType, rdata)
        btn2Info = self.getBtn2Info(funcType, rdata)
        ret['btn1Label'] = btn1Info[BTNINFO_LABEL_INDEX]
        ret['btn2Label'] = btn2Info[BTNINFO_LABEL_INDEX]
        ret['btn1Show'] = btn1Info[BTNINFO_SHOW_INDEX]
        ret['btn2Show'] = btn2Info[BTNINFO_SHOW_INDEX]
        ret['btn1Enabled'] = self.dailyBtn1Enabled(rdata)
        ret['btn2Enabled'] = self.dailyBtn2Enabled(rdata)
        ret['keyBanTips1'] = rdata.get('keyBanTips1', '')
        ret['keyBanTips2'] = rdata.get('keyBanTips2', '')
        ret['keyNotBanTips1'] = rdata.get('keyNotBanTips1', '')
        ret['keyNotBanTips2'] = rdata.get('keyNotBanTips2', '')
        ret['vip'] = self.getVipInfo(funcType, params)
        ret['activityBg'] = rdata.get('activityBg', '')
        if funcType == gametypes.RECOMMEND_TYPE_FUBEN and params[0]:
            ret['exp'] = gameStrings.TEXT_PLAYRECOMMACTIVATIONPROXY_924 % str(params[0])
        else:
            ret['exp'] = 0
        ret['weight'] = self.getItemWeight(funcType, rdata, params, ret['comFlag'])
        ret['guild'] = p.guildNUID != 0
        ret['activation'] = self.getActivationInfo(prid, rdata, gametypes.ACTIVATION_TYPE_ITEM)
        ret['firstReward'] = self.getFirstRewardInfo(prid, ret['comFlag'])
        ret['canExpand'] = ret['isTree'] and not (ret['funcType'] == 10 and not ret['guild'])
        if ret['canExpand']:
            ret['mainDesc'] = ''
        ret['activityIcon'] = self.getActivityIconVisible(prid)
        ret['activityIconTips'] = rdata.get('activityIconTips', '')
        return ret

    def getActivityIconVisible(self, prid):
        now = utils.getNow()
        p = BigWorld.player()
        activityTime = getattr(p, 'guildMergeActivityStartTime', 0)
        if not activityTime:
            return False
        if prid == PLAY_RECOMM_GUILD_SIGN_IN_ID and p.guild:
            isBeMerged = getattr(p, 'lastGuildNameFromMerger', '') and p.lastGuildNameFromMerger != p.guild.name
            endTime = activityTime + GCD.data.get('signInGuildMergerDura ', const.TIME_INTERVAL_DAY * 14)
            return activityTime < now < endTime and isBeMerged
        if prid == PLAY_RECOMM_GUILD_BONFIRE_ID:
            endTime = activityTime + const.TIME_INTERVAL_DAY
            return activityTime < now < endTime
        return False

    def getFirstRewardInfo(self, prid, comFlag):
        if not gameglobal.rds.configData.get('enableWorldQuestLoopRefresh', False):
            visible = False
            value = ''
            tips = ''
        elif prid not in self.worldQuestRefreshFilterDict:
            visible = False
            value = ''
            tips = ''
        elif comFlag and comFlag[0] == 0:
            visible = False
            value = ''
            tips = ''
        else:
            rType = WQRD.data.get(self.worldQuestRefreshFilterDict.get(prid), {}).get('type', 0)
            if rType == gametypes.WORLD_QUEST_REFRESH_BONUS:
                visible = True
                if BigWorld.player().worldRefreshQuestRewarded:
                    value = 'invalid'
                    tips = PRCD.data.get('worldRefreshQuestRewardedTips', '')
                else:
                    value = 'valid'
                    tips = PRCD.data.get('worldRefreshQuestUnrewardedTips', '')
            else:
                visible = False
                value = ''
                tips = ''
        return {'visible': visible,
         'value': value,
         'tips': tips}

    def getActivationInfo(self, id, data, activationType):
        if not gameglobal.rds.configData.get('enableActivation', False):
            visible = False
            value = ''
            tips = ''
        else:
            if activationType == gametypes.ACTIVATION_TYPE_ITEM:
                group = data.get('group')
                if group:
                    activeId = group
                    activeData = PRID.data.get(group, {})
                else:
                    activeId = id
                    activeData = data
            else:
                activeId = id
                activeData = data
            dailyLimit = activeData.get('dailyLimit', 0)
            if dailyLimit:
                visible = True
                curVal = self.getActivationCurVal(activeId, activeData, activationType)
                if curVal > dailyLimit:
                    curVal = dailyLimit
                value = '%d/%d' % (curVal / 1000, dailyLimit / 1000)
                tips = self.getActivationTips(activeData)
            else:
                visible = False
                value = ''
                tips = ''
        return {'visible': visible,
         'value': value,
         'tips': tips}

    def getActivationCurVal(self, id, data, activationType):
        activationInfo = BigWorld.player().activationInfo.get(activationType, {})
        if activationType == gametypes.ACTIVATION_TYPE_ITEM:
            treeChild = data.get('treeChild', ())
            if treeChild and len(treeChild) > 0:
                curVal = sum((activationInfo.get(child, 0) for child in treeChild))
            else:
                curVal = activationInfo.get(id, 0)
        else:
            curVal = activationInfo.get(id, 0)
        return curVal

    def getActivationTips(self, rData):
        p = BigWorld.player()
        activationTips = rData.get('activationTips', {})
        ret = ''
        for key, value in activationTips.items():
            if key[0] <= p.lv <= key[1]:
                ret = value
                break

        return ret

    def getItemWeight(self, funcType, rdata, params, comFlag):
        minlv, _ = rdata.get('lv')
        order = rdata.get('order', 0)
        p = BigWorld.player()
        weight = 3000
        if funcType == gametypes.RECOMMEND_TYPE_VIP:
            if params[0] == 3:
                weight = 0
        elif comFlag[0] == 2:
            weight = 2000
        if p.lv < minlv:
            weight = 1000 - minlv + order * 0.001
        elif funcType in (gametypes.RECOMMEND_TYPE_YOULI,
         gametypes.RECOMMEND_TYPE_WEEKLOOP,
         gametypes.RECOMMEND_TYPE_NORMAL_QUEST_LOOP,
         gametypes.RECOMMEND_TYPE_DIGONG_PUZZLE):
            weekSet = rdata.get('weekSet', 0)
            endTime = rdata.get('endTime')
            passTime = '59 23 * * *'
            if endTime and passTime and utils.inCrontabRange(endTime, passTime, weekSet=weekSet) and comFlag[0] != 2:
                weight = 1000 - minlv + order * 0.001
            else:
                weight = weight + order
        else:
            weight = weight + order
        return weight

    def getVipInfo(self, funcType, params):
        if funcType == gametypes.RECOMMEND_TYPE_VIP:
            vipFlag = params[0]
        else:
            vipFlag = 0
        count = gameglobal.rds.ui.tianyuMall.getUnTakeVipBonusCount(BigWorld.player().vipDailyBonus)
        if count > 0:
            rewardBtnEnabled = True
            rewardBtnLabel = gameStrings.TEXT_PLAYRECOMMACTIVATIONPROXY_1085
        else:
            rewardBtnEnabled = False
            rewardBtnLabel = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
        return {'vipFlag': vipFlag,
         'rewardBtnEnabled': rewardBtnEnabled,
         'rewardBtnLabel': rewardBtnLabel}

    def dailyBtn1Enabled(self, rdata):
        startTimes = rdata.get('keyTimeStart1', ())
        endTimes = rdata.get('keyTimeEnd1', ())
        if not startTimes or not endTimes:
            return True
        weekSet = rdata.get('weekSet', 0)
        if startTimes and endTimes and utils.inCrontabRange(startTimes, endTimes, weekSet=weekSet):
            return True
        return False

    def dailyBtn2Enabled(self, rdata):
        startTimes = rdata.get('keyTimeStart2', ())
        endTimes = rdata.get('keyTimeEnd2', ())
        if not startTimes or not endTimes:
            return True
        weekSet = rdata.get('weekSet', 0)
        if startTimes and endTimes and utils.inCrontabRange(startTimes, endTimes, weekSet=weekSet):
            return True
        return False

    def getBtn1Info(self, funcType, rdata):
        info = [None, None]
        if funcType == gametypes.RECOMMEND_TYPE_FIND_BEAST:
            label, bShow = gameglobal.rds.ui.questTrack.getCurrFindBeastSeekState()
            info[BTNINFO_LABEL_INDEX] = label
            info[BTNINFO_SHOW_INDEX] = bShow
            return info
        else:
            info[BTNINFO_LABEL_INDEX] = rdata.get('keyText1', '')
            info[BTNINFO_SHOW_INDEX] = True
            return info

    def getBtn2Info(self, funcType, rdata):
        info = [None, None]
        info[BTNINFO_LABEL_INDEX] = rdata.get('keyText2', '')
        info[BTNINFO_SHOW_INDEX] = True
        btnType2 = rdata.get('keyType2', 0)
        p = BigWorld.player()
        if funcType == gametypes.RECOMMEND_TYPE_FIND_BEAST:
            funcParam = rdata.get('funcParam', ())
            p = BigWorld.player()
            chain = p.questLoopChain.getChain(funcParam[0])
            exp = chain.calcHistoryExp(p) if chain is not None else 0
            info[BTNINFO_LABEL_INDEX] = rdata.get('keyText2', '')
            info[BTNINFO_SHOW_INDEX] = exp
            return info
        elif btnType2 == uiConst.DAILY_BTN_FUNC_1:
            info[BTNINFO_SHOW_INDEX] = not p.isInTeamOrGroup()
            info[BTNINFO_LABEL_INDEX] = gameStrings.CREATE_TEAM_LABEL
            return info
        elif btnType2 == uiConst.DAILY_BTN_FUNC_16:
            info[BTNINFO_SHOW_INDEX] = gameglobal.rds.configData.get('enableYunChuiScoreDikou', False)
            return info
        elif btnType2 == uiConst.DAILY_BTN_FUNC_17:
            info[BTNINFO_SHOW_INDEX] = gameglobal.rds.configData.get('enableSkyWingChallenge', False)
            return info
        elif btnType2 == uiConst.DAILY_BTN_FUNC_18:
            info[BTNINFO_SHOW_INDEX] = gameglobal.rds.ui.wingWorldRemoveSeal.isWingWorldDiGongExist()
            return info
        else:
            return info

    def getActiveFlag(self, rdata, comFlag):
        if comFlag and comFlag[0] == 2:
            return False
        lv = rdata.get('lv', 0)
        if BigWorld.player().lv < lv[0]:
            return False
        noActive = rdata.get('noActive', 0)
        if noActive:
            return False
        if not self.checkByDailyItemActive(rdata):
            return False
        weekSet = rdata.get('weekSet', 0)
        beginTime = rdata.get('beginTime')
        endTime = rdata.get('endTime')
        if beginTime and endTime and utils.inCrontabRange(beginTime, endTime, weekSet=weekSet):
            return True
        return False

    def wingWorldCheck(self, funcType):
        p = BigWorld.player()
        if funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_WAR and p.inWingCity():
            return False
        return True

    def checkServerProgressOutOfTime(self, serverEventsIds):
        p = BigWorld.player()
        if type(serverEventsIds) == int:
            serverEventsIds = (serverEventsIds,)
        for eventInfo in serverEventsIds:
            if type(eventInfo) in (tuple, list):
                serverEventsId = eventInfo[0]
                checkTime = eventInfo[1]
                if p.isServerProgressFinished(serverEventsId):
                    roundCheckTime = self.getRoundProgressCheckTime(p.getServerProgressFinishTime(serverEventsId), checkTime)
                    if utils.getNow() >= roundCheckTime:
                        return True

        return False

    def getRoundProgressCheckTime(self, finishTime, checkTime):
        nextTime = finishTime + checkTime
        nextTimeTuple = utils.localtimeEx(nextTime)
        if nextTimeTuple[3] == 0 and nextTimeTuple[4] == 0:
            return nextTime
        nextTime = utils.getNextDayTimeStamp(nextTime)
        return nextTime

    def checkServerProgressValid(self, serverEventsIds):
        p = BigWorld.player()
        if type(serverEventsIds) == int:
            serverEventsIds = (serverEventsIds,)
        for eventInfo in serverEventsIds:
            if type(eventInfo) in (tuple, list):
                serverEventsId = eventInfo[0]
                checkTime = eventInfo[1]
                if p.isServerProgressFinished(serverEventsId) and utils.getNow() - p.getServerProgressFinishTime(serverEventsId) < checkTime:
                    return True
            else:
                serverEventsId = eventInfo
                if p.isServerProgressFinished(serverEventsId):
                    return True

        return False

    def getComFlag(self, funcType, prid, rData, params):
        p = BigWorld.player()
        ret = [1, 0]
        if rData.get('checkServerEvent', None):
            serverEventIds = rData.get('checkServerEvent', 0)
            if not self.checkServerProgressValid(serverEventIds) and self.wingWorldCheck(funcType):
                return [3, rData.get('serverEventText', '')]
        lv = rData.get('lv', 0)
        if p.lv < lv[0]:
            return [0, lv[0]]
        activeComplete = rData.get('activeComplete', 0)
        if activeComplete != 0:
            if self.isActiveComplete(prid, rData, activeComplete):
                return [2, 0]
            else:
                return [1, 0]
        if funcType == gametypes.RECOMMEND_TYPE_FUBEN or funcType == gametypes.RECOMMEND_TYPE_VIP:
            params = params[1:]
        comNum = rData.get('comNum', {})
        if funcType == gametypes.RECOMMEND_TYPE_QUMO:
            comNum = {0: params[1]}
        elif funcType == gametypes.RECOMMEND_TYPE_DIGONG:
            comNum = {0: params[1]}
        elif funcType == gametypes.RECOMMEND_TYPE_USE_ITEM_LIMIT:
            comNum = {0: params[1]}
        elif funcType == gametypes.RECOMMEND_TYPE_WENQUAN:
            if params[0] <= 0 and params[2] <= 0:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_YOULI:
            questLoopId = rData.get('funcParam', (0,))[0]
            info = p.questLoopInfo.get(questLoopId)
            if info:
                loopCnt, maxLoopCnt = self.getLoopQuestLoopCnt(questLoopId)
                if loopCnt == maxLoopCnt:
                    return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_WEEKLOOP:
            if prid in self.playRecommendedFinishedActivities:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_CELEBRITY_QUIZ:
            if prid in self.hofFinishActivities:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_GUILD_SIGN_IN:
            if params[0]:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_GUILD_BONFIRE:
            if params[0]:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_BAIDI_SHI_LIAN:
            if params[0]:
                return [2, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_WAR:
            activationInfo = BigWorld.player().activationInfo.get(gametypes.ACTIVATION_TYPE_ITEM, {})
            curVal = activationInfo.get(prid, 0)
            if curVal:
                return [2, 0]
            else:
                return [1, 0]
        elif funcType == gametypes.RECOMMEND_TYPE_SCHOOL_TOP_CHALLENGE:
            if params[0] >= FD.data.get(const.FB_NO_SCHOOL_TOP_DPS, {}).get('timesLimit', 15):
                return [2, 0]
        treeChild = rData.get('treeChild', ())
        if treeChild and len(treeChild) > 0:
            childCom = True
            for child in treeChild:
                childRet = self.getComFlagFromId(child)
                if childRet[0] != 2:
                    childCom = False
                    break

            if childCom:
                return [2, 0]
        if not comNum:
            return ret
        com = True
        if len(params) > 0:
            for key, val in comNum.items():
                if params[key] < val:
                    com = False

        if com:
            return [2, 0]
        else:
            return ret

    def isActiveComplete(self, prid, rData, activeComplete):
        group = rData.get('group', {})
        if group:
            activeId = group
            activeData = PRID.data.get(group, {})
        else:
            activeId = prid
            activeData = rData
        curVal = self.getActivationCurVal(activeId, activeData, gametypes.ACTIVATION_TYPE_ITEM)
        return curVal >= activeComplete

    def getComFlagFromId(self, prid):
        rdata = PRID.data.get(prid, {})
        funcType = rdata.get('funcType')
        params = self.getDailyMainParam(prid, funcType, rdata)
        return self.getComFlag(funcType, prid, rdata, params)

    def getDailyIcon(self, rData, prid):
        p = BigWorld.player()
        itemId = rData.get('icon', 0)
        evaId = ESPRD.data.get(prid, {}).get('ID', None)
        canEvaluate = False
        if evaId:
            canEvaluate = p.getCanEvaluatePlay(evaId)
        it = Item(itemId)
        return uiUtils.getGfxItem(it, appendInfo={'itemId': itemId,
         'canEvaluate': canEvaluate})

    def getTimeDescTip(self, rData):
        p = BigWorld.player()
        timeDescTips = rData.get('timeDescTips', {})
        ret = ''
        for key, value in timeDescTips.items():
            if key[0] <= p.lv <= key[1]:
                ret = value
                break

        return ret

    def getDailyTimeDesc(self, rData):
        p = BigWorld.player()
        timeDesc = rData.get('timeDesc', {})
        ret = ''
        for key, value in timeDesc.items():
            if key[0] <= p.lv <= key[1]:
                ret = value
                break

        return ret

    def getMainDesc(self, funcType, prid, rData, params):
        p = BigWorld.player()
        if funcType == gametypes.RECOMMEND_TYPE_FUBEN:
            params = params[1:]
        elif funcType == gametypes.RECOMMEND_TYPE_YOULI:
            questLoopId = rData.get('funcParam', (0,))[0]
            info = p.questLoopInfo.get(questLoopId)
            if info:
                loopCnt, maxLoopCnt = self.getLoopQuestLoopCnt(questLoopId)
                if loopCnt == maxLoopCnt:
                    params[1] = params[2]
        mainDesc = rData.get('mainDesc', {})
        ret = ''
        if funcType == gametypes.RECOMMEND_TYPE_VIP:
            flag = params[0]
            ret = mainDesc[flag] % tuple(params[1:])
        elif funcType == gametypes.RECOMMEND_TYPE_BANGGONG:
            if not p.guildNUID:
                ret = mainDesc[1]
            else:
                ret = mainDesc[2]
        elif funcType == gametypes.RECOMMEND_TYPE_WEEKLOOP:
            for key, value in mainDesc.items():
                if key[0] <= p.lv <= key[1]:
                    if value.find('%d') != -1:
                        ret = value % (1 if prid in self.playRecommendedFinishedActivities else 0)
                    else:
                        ret = value
                    break

        else:
            for key, value in mainDesc.items():
                if key[0] <= p.lv <= key[1]:
                    if len(params) > 0:
                        ret = value % tuple(params)
                    else:
                        ret = value
                    break

        return ret

    def getMainDescTip(self, rData):
        p = BigWorld.player()
        mainDescTips = rData.get('mainDescTips', {})
        ret = ''
        for key, value in mainDescTips.items():
            if key[0] <= p.lv <= key[1]:
                ret = value
                break

        return ret

    def getDailyMainParam(self, prid, funcType, rdata):
        p = BigWorld.player()
        param = []
        funcParam = rdata.get('funcParam', ())
        if funcType == gametypes.RECOMMEND_TYPE_FUBEN:
            param = self._getFubenDailyParam(prid, rdata)
        elif funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_XINMO:
            param = self._getFubenDailyParam(prid, rdata)[1:]
            bid = rdata.get('xinmoBoundId', -1)
            bhcd = BHCD.data.get(bid, {})
            param.extend([self.bonusHistory.get(bid, 0), bhcd.get('times', 0)])
        elif funcType == gametypes.RECOMMEND_TYPE_NORMAL_QUEST_LOOP:
            loopCnt, maxLoopCnt = self.getLoopQuestLoopCnt(funcParam[0])
            param = [loopCnt, maxLoopCnt]
        elif funcType == gametypes.RECOMMEND_TYPE_YOULI:
            p = BigWorld.player()
            info = p.questLoopInfo.get(funcParam[0])
            if info and info.isYesterday():
                flag = gameStrings.TEXT_HOTKEYPROXY_25_1
            else:
                flag = gameStrings.TEXT_PLAYRECOMMACTIVATIONPROXY_1454
            leftLoopCnt = self.getLeftQuestLoopCnt(funcParam[0])
            loopGroupNum, maxGroupNum = self.getLoopQuestGroupNum(funcParam[0])
            param = [flag,
             loopGroupNum,
             maxGroupNum,
             leftLoopCnt]
        elif funcType == gametypes.RECOMMEND_TYPE_QUMO:
            qldd = QLD.data
            loopCnt = 0
            maxLoopCnt = 0
            for questLoopId, info in p.questLoopInfo.iteritems():
                qldata = qldd.get(questLoopId)
                if not qldata:
                    continue
                if qldata.get('activityType') == funcParam[0]:
                    info = p.questLoopInfo.get(questLoopId)
                    maxLoopCnt = qldata.get('maxLoopCnt', 0)
                    if not info:
                        loopCnt = 0
                    else:
                        loopCnt = info.loopCnt

            param = [loopCnt, maxLoopCnt]
        elif funcType == gametypes.RECOMMEND_TYPE_USE_ITEM_LIMIT:
            limitType = funcParam and (isinstance(funcParam, list) or isinstance(funcParam, tuple)) and funcParam[0]
            if not limitType:
                limitType = gametypes.ITEM_USE_LIMIT_TYPE_DAY
            history = p.itemUseHistory.get(funcParam)
            if history:
                t = self._getItemUseLimitTime(limitType)
                data = history.get(limitType, (0, 0))
                if t == data[0]:
                    value = data[1]
                else:
                    value = 0
            else:
                value = 0
            maxValue = 200
            if funcParam and len(funcParam) >= 2 and funcParam[1] == const.USE_LIMIT_LINGSHI_ITEM_GROUP:
                itemList = CRD.data.get(const.USE_LIMIT_LINGSHI_ITEM_GROUP, [])
                if itemList:
                    maxValue = min(utils.getUseLimitByLv(itemList[0], p.lv, limitType, maxValue), maxValue)
            param = [value, maxValue]
        elif funcType == gametypes.RECOMMEND_TYPE_DIGONG:
            curNum, allNum = gameglobal.rds.ui.player.getKillMonsterNum()
            param = [curNum, allNum]
        elif funcType == gametypes.RECOMMEND_TYPE_WENQUAN:
            for i in range(len(gametypes.RECOMMEND_WENQUAN_FAME)):
                fameId = gametypes.RECOMMEND_WENQUAN_FAME[i]
                value = p.getFame(fameId)
                maxValue = FAD.data.get(fameId, {}).get('maxVal', 0)
                param.append(value)
                param.append(maxValue)

        elif funcType == gametypes.RECOMMEND_TYPE_VIP:
            hasBasicPackage = False
            hasAddedPackage = False
            if not p.vipBasicPackage and MCFD.data.get('vipFirstBuyDaysList', {}) and MCFD.data.get('vipFirstBuyBasicPackage', 0):
                hasBasicPackage = False
                mid = MCFD.data.get('vipFirstBuyBasicPackage', 0)
            else:
                basicLeftTime = float(p.vipBasicPackage.get('tExpire', 0) - utils.getNow())
                hasBasicPackage = basicLeftTime > 0
                mid = MCFD.data.get('vipBasicPackage', 0)
            if hasBasicPackage:
                mid = funcParam[0]
                leftBasicDay = int(max(round(basicLeftTime / const.TIME_INTERVAL_DAY), 1))
            addedPackageId = MID.data.get(mid, {}).get('packageID', 0)
            addedLeftTime = float(p.vipAddedPackage.get(addedPackageId, {}).get('tExpire', 0) - utils.getNow())
            hasAddedPackage = addedLeftTime > 0
            if hasAddedPackage:
                leftAddedDay = int(max(round(addedLeftTime / const.TIME_INTERVAL_DAY), 1))
            flag = 0
            if not hasBasicPackage and not hasAddedPackage:
                flag = 1
                param.append(flag)
            elif hasBasicPackage and not hasAddedPackage:
                flag = 2
                param.append(flag)
                param.append(leftBasicDay)
            elif hasBasicPackage and hasAddedPackage:
                flag = 3
                param.append(flag)
                param.append(leftBasicDay)
                param.append(leftAddedDay)
        elif funcType == gametypes.RECOMMEND_TYPE_COLLECT:
            value = 0
            for quest in funcParam:
                loopCnt, maxLoopCnt = self.getLoopQuestLoopCnt(quest)
                if loopCnt == maxLoopCnt:
                    value = value + 1

            param.append(value)
        elif funcType == gametypes.RECOMMEND_TYPE_SHA_XING:
            bid = funcParam[0]
            bhcd = BHCD.data.get(bid, {})
            shaxingAcIdToLv = PRCD.data.get('shaxingAcIdToLv', ())
            nowLv = 1
            if shaxingAcIdToLv:
                for acId, lv in shaxingAcIdToLv:
                    if gameglobal.rds.ui.achvment.checkAchieveFlag(acId):
                        nowLv = lv
                        break

            param = [self.bonusHistory.get(bid, 0), bhcd.get('times', 0), nowLv]
        elif funcType == gametypes.RECOMMEND_TYPE_BONUS:
            bid = funcParam[0]
            bhcd = BHCD.data.get(bid, {})
            param = [self.bonusHistory.get(bid, 0), bhcd.get('times', 0)]
        elif funcType == gametypes.RECOMMEND_TYPE_DIGONG_PUZZLE:
            for bid in funcParam:
                bhcd = BHCD.data.get(bid, {})
                param.append(self.bonusHistory.get(bid, 0))
                param.append(bhcd.get('times', 0))

        elif funcType == gametypes.RECOMMEND_TYPE_BFY:
            bid = funcParam[0]
            bhcd = BHCD.data.get(bid, {})
            moreInfoId = rdata.get('moreInfoId', 0)
            aData = PRAD.data.get(moreInfoId, {})
            refActivityId = aData.get('refActivityId', 0)
            actIns = self.actFactory.actIns.get(refActivityId, None)
            completeCnt = self.getCntInfo(aData, actIns)
            fbId = funcParam[1]
            fd = FD.data.get(fbId, {})
            timesLimit = fd.get('timesLimit', 0)
            param = [self.bonusHistory.get(bid, 0),
             bhcd.get('times', 0),
             completeCnt,
             timesLimit]
        elif funcType == gametypes.RECOMMEND_TYPE_FIND_BEAST:
            loopCnt, maxLoopCnt = self.getLoopQuestLoopCnt(funcParam[0])
            param = [loopCnt, maxLoopCnt]
        elif funcType == gametypes.RECOMMEND_TYPE_SCHOOL_DAILY:
            loopCnt, _ = self.getLoopQuestLoopCnt(funcParam[0])
            loopGroupNum, maxGroupNum = self.getLoopQuestGroupNum(funcParam[0])
            param = [loopGroupNum, maxGroupNum, loopCnt]
        elif funcType == gametypes.RECOMMEND_TYPE_SCHOOL_ENTRUST:
            acceptCount = p.schoolEntrustCountInfo.get('acceptCount', 0)
            completeCount = p.schoolEntrustCountInfo.get('completeCount', 0)
            dailyAccTimes = SERD.data.get(p.school, {}).get('dailyAccTimes', 0)
            dailyComTimes = SERD.data.get(p.school, {}).get('dailyComTimes', 0)
            param = [completeCount, dailyComTimes, dailyAccTimes - acceptCount]
        elif funcType == gametypes.RECOMMEND_TYPE_GUILD_SIGN_IN:
            param = [1 if p.guildSignIn else 0]
        elif funcType == gametypes.RECOMMEND_TYPE_GUILD_BONFIRE:
            param = [1 if p.guildBonfire else 0]
        elif funcType == gametypes.RECOMMEND_TYPE_BAIDI_SHI_LIAN:
            param = [1 if p.statsInfo.get(BAI_DI_SHI_LIAN_PROP_KEY, 0) else 0]
        elif funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_WAR:
            param = [1 if p.wingWorldAttendedWar else 0]
        elif funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_RESOURCE_COLLECT:
            p = BigWorld.player()
            spriteCount = len(p.spriteWingWorldRes.spriteInSlots.keys())
            unlockedSlots = sMath.clamp(len(list(p.spriteWingWorldRes.unlockedSlots)), 0, SCD.data.get('oneKeyApplySpriteNum', 0))
            collectRate = 0
            for resType, resNum in p.spriteWingWorldRes.resDictCurrent.iteritems():
                collectMax = WWRSD.data.get(resType, {}).get('collectMax', const.MAX_UINT32)
                rate = resNum * 100 / float(collectMax)
                if collectRate <= rate:
                    collectRate = rate

            if collectRate >= 100:
                desc = gameStrings.SPRITE_RES_COLLECT_PLAY_RECOMM_DESC0 % (spriteCount, unlockedSlots)
            elif collectRate > 50:
                desc = gameStrings.SPRITE_RES_COLLECT_PLAY_RECOMM_DESC1 % (spriteCount, unlockedSlots, collectRate)
            else:
                desc = gameStrings.SPRITE_RES_COLLECT_PLAY_RECOMM_DESC2 % (spriteCount, unlockedSlots)
            param = [desc]
        elif funcType == gametypes.RECOMMEND_TYPE_SCHOOL_TOP_CHALLENGE:
            schoolTopDpsTimesWeekly = p.schoolTopDpsTimesWeekly
            param = [schoolTopDpsTimesWeekly]
        elif funcType == gametypes.RECOMMEND_TYPE_GUILD_MEMBERS_FB:
            comNum = rdata.get('comNum', {0: 0})
            param = [p.guildFubenRoundNum.get(funcParam[0], 0), comNum[0]]
        elif funcType == gametypes.RECOMMEND_TYPE_BATTLE_FIELD:
            bfMode = funcParam[0]
            if bfMode == const.BATTLE_FIELD_MODE_PUBG:
                param = list(p.pubgStaticWeekly)
        elif funcType == gametypes.RECOMMEND_TYPE_ZHENZHAN:
            comNum = rdata.get('comNum', {0: 0})
            cnt = 0
            activityInfo = p.rewardRecoveryActivity.getActivity(gametypes.REWARD_RECOVER_ACTIVITY_TYPE_ZHENG_ZHAN_LING)
            if activityInfo.daysVal.has_key(utils.getWeekSecond()):
                cnt = activityInfo.daysVal[utils.getWeekSecond()].cnt
            param = [cnt, comNum[0]]
        return param

    def _getFubenDailyParam(self, prid, rdata):
        p = BigWorld.player()
        data = p.importantPlayRecommendInfo.get(prid)
        fbValue = 0
        lastEnterDays = 0
        coef = 1
        fbId = 0
        maxCount = 0
        if data:
            for fbNo, value, maxValue, _lastEnterDays, _coef in data:
                fbId = fbNo
                maxCount = maxValue
                if rdata.get('bonusGroup', 0):
                    i = 0
                    _fbValue = 0
                    fid = (fbNo, i)
                    item = CRD1.data.get(fid, {})
                    while item != {}:
                        bid = item['bonusHistoryCheckId']
                        _fbValue += self.bonusHistory.get(bid, 0)
                        i += 1
                        fid = (fbNo, i)
                        item = CRD1.data.get(fid, {})

                    fbValue = max(fbValue, _fbValue)
                else:
                    fbValue = max(value, fbValue)
                if lastEnterDays != 0:
                    lastEnterDays = min(lastEnterDays, _lastEnterDays)
                else:
                    lastEnterDays = _lastEnterDays
                if coef != 1:
                    coef = min(coef, _coef)
                else:
                    coef = _coef

            lastEnterDays = min(3, lastEnterDays + 1)
            cdType = FD.data.get(fbId, {}).get('cdType', 0)
            if cdType == 3:
                param = [coef, fbValue, lastEnterDays]
            else:
                param = [0, fbValue, maxCount]
        else:
            param = [coef, 0, 0]
        return param

    def _getItemUseLimitTime(self, limitType):
        if limitType == gametypes.ITEM_USE_LIMIT_TYPE_DAY:
            return utils.getDaySecond()
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_WEEK:
            return utils.getWeekSecond()
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_MONTH:
            return utils.getMonthSecond()
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_QUARTER:
            return utils.getQuarterSecond()
        else:
            return None

    def getLoopQuestGroupNum(self, questLoopId):
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId)
        qldata = QLD.data.get(questLoopId)
        maxGroupNum = qldata.get('groupNum', 0)
        if not qldata:
            return [0, 0]
        if info:
            loopGroupNum = len(info.questInfo)
        else:
            loopGroupNum = 0
        return [loopGroupNum, maxGroupNum]

    def getLeftQuestLoopCnt(self, questLoopId):
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId)
        qldata = QLD.data.get(questLoopId)
        maxLoopCnt = qldata.get('maxLoopCnt', 0)
        if not qldata:
            return 0
        if not info:
            leftLoopCnt = 1
        else:
            if info.isYesterday():
                loopCnt = 0
            else:
                loopCnt = 1
            leftLoopCnt = max(maxLoopCnt - loopCnt, 0)
        return leftLoopCnt

    def getLeftQuestLoopCnt(self, questLoopId):
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId)
        qldata = QLD.data.get(questLoopId, {})
        maxLoopCnt = qldata.get('maxLoopCnt', 0)
        if not qldata:
            return 0
        if not info:
            leftLoopCnt = 1
        else:
            if info.isYesterday():
                loopCnt = 0
            else:
                loopCnt = 1
            leftLoopCnt = max(maxLoopCnt - loopCnt, 0)
        return leftLoopCnt

    def getLoopQuestLoopCnt(self, questLoopId):
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId)
        qldata = QLD.data.get(questLoopId)
        maxLoopCnt = qldata.get('maxLoopCnt', 0)
        if not qldata:
            return [0, 0]
        if not info:
            loopCnt = 0
        else:
            loopCnt = info.loopCnt
            if info.isYesterday():
                loopCnt = 0
        return [loopCnt, maxLoopCnt]

    def getCompleteHintFlag(self, rdata, comFlag):
        if not rdata.get('needCompleteHintFlag', 0):
            return COMPLETE_HINT_FLAG_PASS
        if comFlag and comFlag[0] == 2:
            return COMPLETE_HINT_FLAG_FINISH
        return COMPLETE_HINT_FLAG_GOING

    def checkSchool(self, rdata):
        school = rdata.get('school', ())
        if len(school) == 0:
            return True
        return BigWorld.player().school in school

    def isDailyActiveShow(self, rdata):
        whichDay = rdata.get('whichDay', ())
        if not whichDay:
            return True
        beginTime = rdata.get('beginTime')
        endTime = rdata.get('endTime')
        if not beginTime or not endTime:
            return True
        weekSet = rdata.get('weekSet', 0)
        if weekSet:
            if beginTime and endTime and utils.inDateRange(beginTime, endTime, weekSet=weekSet):
                return True
        else:
            return utils.getWeekInt() + 1 in whichDay
        return False

    def getDailyRecommInfo(self, *args):
        info = {}
        dailyIsFinish = True
        dailyList = self.getDailyItems(DAILY_ITEM_TYPE_DAILY)
        for dailyItem in dailyList:
            if dailyItem['completeHintFlag'] == COMPLETE_HINT_FLAG_GOING:
                dailyIsFinish = False
                break

        info['dailyIsFinish'] = dailyIsFinish and self.showDailyPanel()
        weekIsFinish = True
        weekList = self.getDailyItems(DAILY_ITEM_TYPE_WEEK, needRefreshFubenTimes=False)
        for weekItem in weekList:
            if weekItem['completeHintFlag'] == COMPLETE_HINT_FLAG_GOING:
                weekIsFinish = False
                break

        info['weekIsFinish'] = weekIsFinish and self.showWeekPanel()
        info['dailyList'] = dailyList
        info['showLvUp'] = self.showLvUpPanel()
        return info

    def showDailyPanel(self):
        return BigWorld.player().lv >= PRCD.data.get('importantRecommMinLv', 20)

    def showWeekPanel(self):
        return BigWorld.player().lv >= PRCD.data.get('importantRecommMinWeekLv', 20)

    def showLvUpPanel(self):
        return BigWorld.player().lv >= PRCD.data.get('lvupRecommMinLv', 45)

    def showStrongerPanel(self):
        return BigWorld.player().lv >= PRCD.data.get('strongerRecommMinLv', 20)

    @ui.callAfterTime(0.1)
    def refreshDailyRecommItems(self):
        if not self.widget or not self.widget.stage or self.activationTabIdx != uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB:
            return
        self.widget.mainMC.activationPanel.dailyList.visible = True
        self.widget.mainMC.activationPanel.dailyList.mouseWheelEnable = True
        configInfo = self.getDailyRecommConfigInfo()
        self.widget.mainMC.activationPanel.exitGameBtn.visible = configInfo['isQuitGame']
        self.widget.mainMC.activationPanel.continueGameBtn.visible = configInfo['isQuitGame']
        info = self.getDailyRecommInfo()
        recommInfo = info['dailyList']
        firstShowActId = self.uiAdapter.playRecomm.getFirstShowActId()
        locateType = self.uiAdapter.playRecomm.getLocateType()
        dailyList = self.widget.mainMC.activationPanel.dailyList
        completeHint = self.widget.mainMC.activationPanel.completeHint
        firstId = 0
        needSelectFromActId = 0
        for i in range(len(recommInfo)):
            if self.selectedDailyId == recommInfo[i]['id']:
                firstId = self.selectedDailyId
            if firstId == 0:
                firstId = recommInfo[i]['id']
            if firstShowActId:
                if firstShowActId == recommInfo[i]['mIdMapRefActId'] and locateType == PLAY_RECOMM_DAILY_LOCATE_ABD:
                    needSelectFromActId = recommInfo[i]['id']
                elif firstShowActId == recommInfo[i]['id'] and locateType == PLAY_RECOMM_DAILY_LOCATE_PRID:
                    needSelectFromActId = recommInfo[i]['id']

        if needSelectFromActId:
            self.selectedDailyId = needSelectFromActId
        else:
            self.selectedDailyId = firstId
        dailyList.dataArray = recommInfo
        dailyList.validateNow()
        if self.selectedDailyItem and self.selectedDailyItem.id == self.selectedDailyId:
            dailyList.scrollTo(self.selectedDailyItem.y)
            dailyList.validateNow()
            if not self.selectedDailyItem.canExpand:
                self.selectedDailyItem.openExpand()
        if not self.isClickCompleteHint:
            completeHint.visible = info['dailyIsFinish']
            if completeHint.visible:
                btnGroup = completeHint.hint.btnGroup
                btnGroup.gotoWeekBtn.visible = not info['weekIsFinish']
                btnGroup.gotoLvUpBtn.visible = info['showLvUp']
                if btnGroup.gotoWeekBtn.visible and btnGroup.gotoLvUpBtn.visible:
                    btnGroup.backBtn.visible = True
                    btnGroup.longBackBtn.visible = False
                    btnGroup.gotoWeekBtn.x = 200
                    btnGroup.gotoLvUpBtn.x = 304
                elif btnGroup.gotoWeekBtn.visible:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 142
                    btnGroup.gotoWeekBtn.x = 255
                elif btnGroup.gotoLvUpBtn.visible:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 142
                    btnGroup.gotoLvUpBtn.x = 255
                else:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 199
        self.widget.mainMC.activationPanel.checkBoxUseFly.selected = self.useFly
        self.refreshTreeCanvas()

    def refreshTreeCanvas(self):
        if self.treeCanvas and self.treeCanvas.stage and self.treeCanvas.visible:
            dataList = self.getDailyItems(DAILY_ITEM_TYPE_DAILY, self.blackCoverItemId)
            for index, data in enumerate(dataList):
                item = self.treeCanvas.getChildAt(index + 1)
                item.data = data

    def getDailyRecommConfigInfo(self):
        gameglobal.rds.ui.playRecommPushIcon.cancelNotify()
        p = BigWorld.player()
        ret = {}
        ret['isQuitGame'] = self.uiAdapter.playRecomm.isQuitGame
        ret['showPushIcon'] = self.uiAdapter.playRecommPushIcon.getShowPushIconSetting()
        if not utils.isSameDay(self.uiAdapter.playRecomm.tLastOpen):
            p.cell.queryImportantPlayRecommendInfo()
        self.uiAdapter.playRecomm.tLastOpen = utils.getNow()
        p.cell.queryBonusHistory(1220)
        if self.needGetBonusHistory:
            for k, v in PRID.data.items():
                if v.get('funcType', 0) in BONUS_HISTORY_BONUSID_SET:
                    funcParam = v.get('funcParam', ())
                    if type(funcParam) == int:
                        bhcd = BHCD.data.get(funcParam, {})
                        p.cell.queryBonusHistory(bhcd.get('group', 0))
                    elif type(funcParam) == tuple:
                        for bid in funcParam:
                            bhcd = BHCD.data.get(bid, {})
                            p.cell.queryBonusHistory(bhcd.get('group', 0))

                if v.get('bonusGroup', 0):
                    funcParam = v.get('funcParam', ())
                    if type(funcParam) == int:
                        p.cell.queryBonusHistory(funcParam)
                    elif type(funcParam) == tuple:
                        for bid in funcParam:
                            bhcd = BHCD.data.get(bid, {})
                            p.cell.queryBonusHistory(funcParam[0])

            self.needGetBonusHistory = False
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM_V2 * 100 + 4)
        return ret

    def getWeeklyListDataInfo(self):
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 5)
        info = {}
        dailyIsFinish = True
        dailyList = self.getDailyItems(DAILY_ITEM_TYPE_DAILY)
        for dailyItem in dailyList:
            if dailyItem['completeHintFlag'] == COMPLETE_HINT_FLAG_GOING:
                dailyIsFinish = False
                break

        info['dailyIsFinish'] = dailyIsFinish and self.showDailyPanel()
        weekIsFinish = True
        weekList = self.getDailyItems(DAILY_ITEM_TYPE_WEEK, needRefreshFubenTimes=False)
        for weekItem in weekList:
            if weekItem['completeHintFlag'] == COMPLETE_HINT_FLAG_GOING:
                weekIsFinish = False
                break

        info['weekIsFinish'] = weekIsFinish and self.showWeekPanel()
        info['weekList'] = weekList
        info['showLvUp'] = self.showLvUpPanel()
        info['firstShowActId'] = self.uiAdapter.playRecomm.getFirstShowActId()
        return info

    def getWeekLoopTable(self):
        iprdd = PRCCD.data
        result = {1: {},
         2: {},
         3: {},
         4: {},
         5: {},
         6: {},
         7: {}}
        for item in result.values():
            item['activeData'] = []

        p = BigWorld.player()
        for prid, rdata in iprdd.iteritems():
            try:
                if utils.getEnableCheckServerConfig():
                    serverConfigId = rdata.get('serverConfigId', 0)
                    if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                        continue
                if not self.showWeekAdvanceLvItem and rdata.get('lv'):
                    minlv, maxlv = rdata.get('lv')
                    if p.lv < minlv or p.lv > maxlv:
                        continue
                if prid == 10007 and utils.getServerOpenDays() <= 7:
                    continue
                if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
                    if rdata.get('hideInNovice', 0):
                        continue
                weekSet = rdata.get('weekSet', 0)
                if utils.isInvalidWeek(weekSet):
                    continue
                for day in rdata.get('whichDay', ()):
                    result[day]['now'] = utils.getWeekInt() + 1 == day
                    result[day]['activeData'].append(self.getWeekLoopItem(day, prid, rdata))

            except Exception as e:
                gamelog.error('@jbx: getWeekLoopTable error', e.message)

        for value in result.itervalues():
            if value.get('activeData', []):
                value['activeData'].sort(cmp=lambda a, b: cmp(a['order'], b['order']))

        return result

    def getWeekLoopItem(self, day, prid, rdata):
        ret = {}
        ret['id'] = prid
        ret['name'] = rdata.get('name', '')
        ret['activeFlag'] = self.getActiveFlag(rdata, None) and utils.getWeekInt() + 1 == day
        if ret['activeFlag']:
            ret['time'] = rdata.get('openText', '')
        else:
            ret['time'] = self.getDailyTimeDesc(rdata)
        ret['timeTip'] = self.getTimeDescTip(rdata)
        ret['moreInfoId'] = rdata.get('moreInfoId', 0)
        ret['order'] = rdata.get('order', 0)
        return ret

    def refreshWeeklyRecommItems(self):
        if self.selectedWeeklyItem:
            self.selectedWeeklyItem.selected = False
            self.selectedWeeklyItem = None
        info = self.getWeeklyListDataInfo()
        firstShowActId = info['firstShowActId']
        if firstShowActId:
            self.selectedWeeklyId = info['firstShowActId']
        weekList = info['weekList']
        firstId = 0
        listLength = len(weekList)
        for i in xrange(listLength):
            if self.selectedWeeklyId == weekList[i]['id']:
                firstId = self.selectedWeeklyId
                break
            if firstId == 0:
                firstId = weekList[i]['id']

        if not firstShowActId:
            self.selectedWeeklyId = firstId
        activationPanel = self.widget.mainMC.activationPanel
        activationPanel.weekList.visible = True
        activationPanel.weekList.dataArray = weekList
        activationPanel.weekList.validateNow()
        if not self.isClickCompleteHint:
            self.widget.mainMC.activationPanel.completeHint.visible = info['weekIsFinish']
            if activationPanel.completeHint.visible:
                btnGroup = activationPanel.completeHint.hint.btnGroup
                btnGroup.gotoDailyBtn.visible = not info['dailyIsFinish']
                btnGroup.gotoLvUpBtn.visible = info['showLvUp']
                if btnGroup.gotoDailyBtn.visible and btnGroup.gotoLvUpBtn.visible:
                    btnGroup.backBtn.visible = True
                    btnGroup.longBackBtn.visible = False
                    btnGroup.gotoDailyBtn.x = 200
                    btnGroup.gotoLvUpBtn.x = 304
                elif btnGroup.gotoDailyBtn.visible:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 142
                    btnGroup.gotoDailyBtn.x = 255
                elif btnGroup.gotoLvUpBtn.visible:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 142
                    btnGroup.gotoLvUpBtn.x = 255
                else:
                    btnGroup.backBtn.visible = False
                    btnGroup.longBackBtn.visible = True
                    btnGroup.longBackBtn.x = 199
        activationPanel.checkBoxUseFly.selected = self.useFly

    def refreshTabBtnList(self):
        p = BigWorld.player()
        startX = 22
        posX = startX
        offset = 126
        if p.lv >= SCD.data.get('PlayRecommV2OperationTabShowLv', 60) and gameglobal.rds.configData.get('enableWeekActivation', False):
            self.widget.mainMC.operationBtn.x = posX
            self.widget.mainMC.operationBtn.visible = True
            posX += offset
        else:
            self.widget.mainMC.operationBtn.visible = False
        self.widget.mainMC.dailyBtn.x = posX
        posX += offset
        self.widget.mainMC.weeklyBtn.x = posX

    def fillDailyItemData(self, *args):
        itemData = ASObject(args[3][0])
        dailyItem = ASObject(args[3][1])
        drItem = dailyItem
        drItem.prModel = self.uiAdapter.playRecomm.getPrModel()
        drItem.data = itemData
        ASUtils.setHitTestDisable(drItem.blackCover, True)
        drItem.itemName.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.itemName.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.hideTipListener, False, 0, True)
        drItem.itemIcon.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.btn1Area.alpha = 0
        drItem.btn2Area.alpha = 0
        if 'event' not in drItem.mainDesc.htmlText:
            drItem.mainDesc.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        else:
            drItem.mainDesc.removeEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.timeDesc.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.comFlag.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.activation.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.bg.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.newExpandBtn.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
        drItem.addEventListener(events.MOUSE_CLICK, self.handleClickDailyItem, False, 0, True)
        drItem.newExpandBtn.visible = itemData.canExpand == True
        drItem.canExpand = itemData.canExpand
        drItem.addEventListener('blackCoverShow', self.showBlackCover, False, 0, True)
        drItem.addEventListener('blackCoverHide', self.clearBlackCover, False, 0, True)
        if self.blackCoverItemId and self.treeCanvas and self.treeCanvas.stage:
            drItem.blackCover.visible = itemData.id != self.blackCoverItemId
        if self.selectedDailyId == itemData.id:
            drItem.selected = True
            if itemData.moreInfoId:
                data = self.uiAdapter.playRecomm.getPlayTipData(itemData.moreInfoId, itemData.seekId, itemData.id, itemData.funcType)
                self.showActivityTips(drItem, data)
            else:
                self.hideActivityTips()
            self.selectedDailyItem = drItem
        else:
            drItem.selected = False

    def showActivityTips(self, target, tipsData):
        if not self.uiAdapter.playRecomm.widget:
            return
        else:
            gamelog.info('jbx:showActivityTips')
            self.hideActivityTips()
            if self.tipsMc == None:
                if tipsData.get('expendQuestInfo', None):
                    self.tipsMc = self.uiAdapter.playRecomm.widget.getInstByClsName('ActivityQuest_TipMc')
                else:
                    self.tipsMc = self.uiAdapter.playRecomm.widget.getInstByClsName('Activity_Tip_TipMc')
                ASUtils.setHitTestDisable(self.tipsMc, False)
            tipsMc = self.tipsMc
            tipsMc.visible = True
            tipsMc.tipData = tipsData
            tipsMc.model = self.uiAdapter.playRecomm.getPrModel()
            tipsMc.refMc = target
            tipsMc.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.hideTipListener, False, 0, True)
            self.uiAdapter.playRecomm.widget.addChild(tipsMc)
            self.setupActivityTipLocation(target)
            return

    def mouseClickListener(self, *args):
        gameglobal.rds.sound.playSound(2)
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        self.setCurrentSelectedDailyItem(itemMc)
        if itemMc.moreInfoId:
            data = self.uiAdapter.playRecomm.getPlayTipData(itemMc.moreInfoId, itemMc.seekId, itemMc.id, itemMc.funcType)
            if self.tipsMc and self.tipsMc.refMc == itemMc:
                self.hideActivityTips()
            else:
                self.showActivityTips(itemMc, data)
        else:
            self.hideActivityTips()

    def setupActivityTipLocation(self, target):
        padding = -2
        targetRect = self.uiAdapter.playRecomm.widget.hit.getBounds(self.uiAdapter.playRecomm.currentView)
        tipsMc = self.tipsMc
        tipsMc.x = int(targetRect.x + targetRect.width)
        tipsMc.y = int(targetRect.y + padding)

    def hideTipListener(self, *args):
        self.hideActivityTips()

    def hideActivityTips(self, force = False):
        gamelog.info('jbx:hideActivityTips')
        if self.tipsMc:
            self.tipsMc.refMc = None
            self.uiAdapter.playRecomm.widget.removeToCache(self.tipsMc)
            self.tipsMc = None

    def handleGetWeeklyReward(self, *args):
        BigWorld.player().cell.receiveWeekActivationReward()

    def handleClickOperatonItem(self, *args):
        BigWorld.player().cell.receiveWeekActivationReward()

    def handleGainActivityRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        key = int(e.currentTarget.dataKey)
        conditionType = PROAD.data.get(key, {}).get('conditionType', 0)
        if conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_WEEK_ACTIVATION)
        elif e.currentTarget.canGainReward:
            BigWorld.player().base.getOperationActivityReward(key)

    def handleOperationBtnClick(self, *args):
        self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB)

    def handleDailyBtnClick(self, *args):
        self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB)

    def handleWeeklyBtnClick(self, *args):
        self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB)

    def handleClickDailyItem(self, *args):
        e = ASObject(args[3][0])
        curItem = e.currentTarget
        self.setCurrentSelectedDailyItem(curItem)

    def setCurrentSelectedDailyItem(self, curItem):
        if self.selectedDailyId == curItem.id:
            return
        if curItem.blackCover.visible:
            return
        if self.selectedDailyItem:
            self.selectedDailyItem.selected = False
        self.selectedDailyId = curItem.id
        self.selectedDailyItem = curItem
        self.selectedDailyItem.selected = True

    def showBlackCover(self, *args):
        e = ASObject(args[3][0])
        curItem = e.currentTarget
        dailyList = self.widget.mainMC.activationPanel.dailyList
        items = dailyList.items
        if len(items) == 0:
            return
        else:
            item = None
            for item in items:
                if item == curItem:
                    item.blackCover.visible = False
                else:
                    item.blackCover.visible = True
                    ASUtils.setHitTestDisable(item, True)

            if not self.treeCanvas:
                self.treeCanvas = self.widget.createMoveClip()
            else:
                while self.treeCanvas.numChildren > 0:
                    self.treeCanvas.removeChildAt(0)

            self.widget.mainMC.activationPanel.dailyList.scrollEnable = False
            self.widget.mainMC.activationPanel.dailyList.addEventListener(events.MOUSE_CLICK, self.handleDailyListClick, False, 0, True)
            self.widget.addChild(self.treeCanvas)
            bg = None
            if curItem.index % 2:
                bg = self.widget.getInstByClsName('PlayRecommV2Activity_PlayRecomm_DailyChildBgRight')
            else:
                bg = self.widget.getInstByClsName('PlayRecommV2Activity_PlayRecomm_DailyChildBgLeft')
            self.treeCanvas.addChild(bg)
            data = self.getDailyItems(DAILY_ITEM_TYPE_DAILY, curItem.id)
            bg.width = dailyList.itemWidth + 4
            bg.height = dailyList.itemHeight * len(data) + 20
            treeItem = None
            for j in xrange(len(data)):
                treeItem = self.widget.getInstByClsName('PlayRecommV2Activity_PlayRecomm_DayItem')
                if type(treeItem) == str:
                    BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, ['jbx:getInstByClsName return stirng:' + treeItem], 0, {})
                treeItem.prModel = self.uiAdapter.playRecomm.getPrModel()
                treeItem.prMediator = self.uiAdapter.playRecomm.getPrMediator()
                treeItem.data = data[j]
                treeItem.itemName.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.itemName.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.hideTipListener, False, 0, True)
                treeItem.itemIcon.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.mainDesc.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.timeDesc.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.comFlag.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.activation.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.bg.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.newExpandBtn.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
                treeItem.newExpandBtn.visible = data[j]['canExpand']
                treeItem.addEventListener(events.MOUSE_CLICK, self.handleClickDailyItem, False, 0, True)
                treeItem.x = 6
                treeItem.y = dailyList.itemHeight * j + 14
                self.treeCanvas.addChild(treeItem)

            globalPos = ASUtils.local2Global(curItem, 0, 0)
            activationLocalPos = ASUtils.global2Local(self.widget, globalPos[0], globalPos[1])
            self.treeCanvas.x = activationLocalPos[0] - 5
            self.treeCanvas.y = activationLocalPos[1] + curItem.height - 5
            self.blackCoverItemId = curItem.id
            return

    def handleClickBackBtn(self, *args):
        self.isClickCompleteHint = True
        self.widget.mainMC.activationPanel.completeHint.visible = False

    def handleClickGotoWeekBtn(self, *args):
        self.isClickCompleteHint = True
        self.widget.mainMC.activationPanel.completeHint.visible = False
        self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB)

    def handleClickGotoLvUpBtn(self, *args):
        self.isClickCompleteHint = True
        self.widget.mainMC.activationPanel.completeHint.visible = False
        self.uiAdapter.playRecomm.setTabIdx(uiConst.PLAY_RECOMMV2_TAB_MORE_IDX)

    def handleSetUseFly(self, *args):
        self.useFly = self.widget.mainMC.activationPanel.checkBoxUseFly.selected

    def buttonClickEventListener(self, *args):
        e = ASObject(args[3][0])
        name = e.target.name
        data = e.target.data
        if name == 'continueGameBtn':
            self.uiAdapter.playRecomm.hide()
        elif name == 'exitGameBtn':
            self.uiAdapter.playRecomm.exitGame()

    def handleSetAdvanced(self, *args):
        if self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB:
            self.clearBlackCover()
            self.showDayAdvanceLvItem = not self.showDayAdvanceLvItem
            self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB, True)
        elif self.activationTabIdx == uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB:
            self.clearBlackCover()
            self.showWeekAdvanceLvItem = not self.showWeekAdvanceLvItem
            self.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB, True)

    def clickAvoidDoingBtn(self, *args):
        p = BigWorld.player()
        if hasattr(p, 'avoidDoingActivity'):
            for activityType, activity in getattr(p, 'avoidDoingActivity', {}).iteritems():
                if self.inAvoidDoingOpenTime(activity.activityKey):
                    self.uiAdapter.avoidDoingActivity.show()
                    return

        BigWorld.player().showGameMsg(GMDD.data.AVOID_DOING_TIP, ())

    def inAvoidDoingOpenTime(self, activityKey):
        adad = ADAD.data.get(activityKey, ())
        openTime = adad.get('openTime', None)
        closeTime = adad.get('closeTime', None)
        tWhen = utils.getNow()
        if openTime and closeTime and utils.getDisposableCronTabTimeStamp(openTime) <= tWhen <= utils.getDisposableCronTabTimeStamp(closeTime):
            return True
        else:
            return False

    def clearBlackCover(self, *args):
        gamelog.info('@jbx:clearBlackCover')
        self.widget.mainMC.activationPanel.dailyList.scrollEnable = True
        self.widget.mainMC.activationPanel.dailyList.removeEventListener(events.MOUSE_CLICK, self.handleDailyListClick)
        items = self.widget.mainMC.activationPanel.dailyList.items
        for item in items:
            item.blackCover.visible = False
            ASUtils.setHitTestDisable(item, False)

        if self.treeCanvas:
            self.widget.removeChild(self.treeCanvas)
        self.blackCoverItemId = 0

    def handleDailyListClick(self, *args):
        e = ASObject(args[3][0])
        if e.target.name == 'dailList' or e.target.parent.name == 'dailyList':
            self.clearBlackCover()

    def fillWeekPanelItemH(self, *args):
        itemData = ASObject(args[3][0])
        dailyItem = ASObject(args[3][1])
        drItem = dailyItem
        drItem.prModel = self.uiAdapter.playRecomm.getPrModel()
        drItem.data = itemData
        drItem.itemName.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.itemName.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.hideTipListener, False, 0, True)
        drItem.itemIcon.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.btn1Area.alpha = 0
        drItem.btn2Area.alpha = 0
        drItem.mainDesc.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.timeDesc.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.comFlag.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.activation.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.bg.addEventListener(events.MOUSE_CLICK, self.weekItemClickListener, False, 0, True)
        drItem.addEventListener(events.MOUSE_CLICK, self.handleClickWeeklyItem, False, 0, True)
        drItem.newExpandBtn.visible = itemData.canExpand == True
        if self.selectedWeeklyId == itemData.id:
            if self.selectedWeeklyItem:
                self.selectedWeeklyItem.selected = False
            drItem.selected = True
            self.selectedDailyItem = drItem
            if itemData.moreInfoId:
                data = self.uiAdapter.playRecomm.getPlayTipData(itemData.moreInfoId, itemData.seekId, itemData.id)
                self.showActivityTips(drItem, data)
            else:
                self.hideActivityTips()
            self.selectedWeeklyItem = drItem
        else:
            drItem.selected = False

    def weekItemClickListener(self, *args):
        gameglobal.rds.sound.playSound(2)
        e = ASObject(args[3][0])
        data = self.uiAdapter.playRecomm.getPlayTipData(e.currentTarget.parent.moreInfoId, e.currentTarget.parent.seekId, e.currentTarget.parent.id)
        tipsMc = self.tipsMc
        if tipsMc and tipsMc.refMc == e.currentTarget.parent:
            self.hideActivityTips()
        else:
            self.showActivityTips(e.currentTarget.parent, data)

    def handleClickWeeklyItem(self, *args):
        e = ASObject(args[3][0])
        curItem = e.currentTarget
        if self.selectedWeeklyId == curItem.id:
            return
        if self.selectedWeeklyItem:
            self.selectedWeeklyItem.selected = False
        self.selectedWeeklyId = curItem.id
        self.selectedWeeklyItem = curItem
        self.selectedWeeklyItem.selected = True

    def handleShowWeekLoppBtnClick(self, *args):
        weekPanel = self.widget.mainMC.activationPanel.weekActivation
        weekPanel.parent.setChildIndex(weekPanel, weekPanel.parent.numChildren - 1)
        weekPanel.visible = True
        weekData = self.getWeekLoopTable()
        for i in range(1, 8):
            data = weekData[i]
            weekMc = weekPanel.getChildByName('week%d' % i)
            if data['now']:
                weekMc.weekFlag.gotoAndStop('now')
                weekMc.hoverMc.visible = True
            else:
                weekMc.weekFlag.gotoAndStop('normal')
                weekMc.hoverMc.visible = False
            weekMc.weekFlag.txtWeekName.text = gameStrings.PLAY_RECOMM_V2_WEEK_NAME_LIST[i - 1]
            activeData = data['activeData']
            for j in xrange(3):
                weekItemMc = weekMc.getChildByName('item%d' % j)
                if j < len(activeData) and activeData[j]:
                    weekItemMc.visible = True
                    weekItemMc.selectedSign.visible = False
                    weekItemMc.id = activeData[j]['id']
                    weekItemMc.moreInfoId = activeData[j]['moreInfoId']
                    weekItemMc.itemBtn.itemName.text = activeData[j]['name']
                    weekItemMc.itemBtn.itemTime.htmlText = activeData[j]['time']
                    ASUtils.setHitTestDisable(weekItemMc.activeFlag, True)
                    TipManager.addTip(weekItemMc.itemBtn, activeData[j]['timeTip'])
                    weekItemMc.activeFlag.visible = activeData[j]['activeFlag']
                    weekItemMc.activeFlag.mouseEnabled = False
                    if activeData[j]['id'] == self.selectedWeeklyId:
                        tipData = self.uiAdapter.playRecomm.getPlayTipData(weekItemMc.moreInfoId, '', weekItemMc.id)
                        self.showActivityTips(weekItemMc, tipData)
                        weekItemMc.selectedSign.visible = True
                else:
                    weekItemMc.visible = False
                weekItemMc.addEventListener(events.MOUSE_CLICK, self.handleWeekItemMouseClick, False, 0, True)

            weekMc.hoverMc.mouseEnabled = False

    def handleWeekItemMouseClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        tipsMc = self.tipsMc
        if itemMc.moreInfoId:
            data = self.uiAdapter.playRecomm.getPlayTipData(itemMc.moreInfoId, '', itemMc.id)
            if tipsMc and tipsMc.refMc == itemMc:
                self.hideActivityTips()
            else:
                self.showActivityTips(itemMc, data)
        else:
            self.hideActivityTips()

    def handleHideWeekLoopBtnClick(self, *args):
        self.widget.mainMC.activationPanel.weekActivation.visible = False

    def handleClickFree(self, *args):
        e = ASObject(args[3][0])
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 0)
        e.stopImmediatePropagation()

    def handleClickDailyActivatonItem(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.name == 'juexingRebuildFree':
            return
        BigWorld.player().cell.receiveActivationReward()

    def handleGetDailyRewardBtnClick(self, *args):
        BigWorld.player().cell.receiveActivationReward()

    def updateWorldQuestRefreshFilterDict(self, info):
        self.worldQuestRefreshFilterDict = {}
        for value in info.itervalues():
            self.worldQuestRefreshFilterDict[WQRD.data.get(value, {}).get('recommend', 0)] = value

        self.refreshRecomm()

    def setPlayRecommendedFinishedActivities(self, playRecommendedFinishedActivities):
        self.playRecommendedFinishedActivities = playRecommendedFinishedActivities
        self.refreshRecomm()

    def setPlayRecHofFinishedActivities(self, hofFinishActivities):
        self.hofFinishActivities = hofFinishActivities
        self.refreshRecomm()

    def setBonusHistory(self, data):
        _, res = data
        needRefresh = False
        for cid, value in res.iteritems():
            if cid not in self.bonusHistory:
                self.bonusHistory[cid] = 0
            if self.bonusHistory[cid] != value:
                self.bonusHistory[cid] = value
                needRefresh = True

        if needRefresh:
            self.refreshRecomm()

    def refreshItemTip(self):
        if self.tipsMc and self.tipsMc.refMc:
            data = self.uiAdapter.playRecomm.getPlayTipData(self.tipsMc.refMc.moreInfoId, self.tipsMc.refMc.seekId, self.tipsMc.refMc.id)
            self.showActivityTips(self.tipsMc.refMc, data)

    def checkDailyItemByFuncType(self, funcType):
        if funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_OPENDOOR:
            if gameglobal.rds.ui.wingWorldRemoveSeal.checkWingWorldRemoveMileStone('finish'):
                return False
        if funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_WAR:
            step = BigWorld.player().wingWorld.step
            if step < gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 or step > gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_4:
                return False
        if funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_XINMO:
            step = BigWorld.player().wingWorld.step
            if step < gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 or step > gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
                return False
        return True

    def checkByDailyItemActive(self, rdata):
        funcType = rdata.get('funcType', -1)
        if funcType == gametypes.RECOMMEND_TYPE_WINGWORLD_OPENDOOR:
            return gameglobal.rds.ui.wingWorldRemoveSeal.isWingWorldDiGongExist()
        return True

    def hasNotReceivedRewards(self):
        p = BigWorld.player()
        hasReward = False
        for key, value in PROAD.data.iteritems():
            startTime = value.get('startTime', None)
            endTime = value.get('endTime', None)
            conditionType = value.get('conditionType', gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY)
            conditionProgress = value.get('conditionProgress', 0)
            if not startTime or not endTime or not utils.inTimeTuplesRange(startTime, endTime):
                continue
            activityInfo = p.weekOperationActivityInfo.get(key, None)
            complete = activityInfo and activityInfo.status
            if conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                continue
            elif conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_SHOW_ONLY:
                continue
            elif utils.inTimeTuplesRange(startTime, endTime):
                if activityInfo and activityInfo.status:
                    continue
                elif activityInfo and activityInfo.progress >= conditionProgress or conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_REWARD_ONLY and not complete:
                    hasReward = True
                    break

        if not hasReward:
            hasReward = self.getWeekActivationPointInfo().get('btnEnable', False)
        return hasReward

    def getWeekActivationPointInfo(self):
        info = {}
        p = BigWorld.player()
        ard = {}
        for minLv, maxLv in WARD.data.keys():
            if minLv <= p.activationLv <= maxLv:
                ard = WARD.data.get((minLv, maxLv), {})
                break

        if not ard:
            return info
        activationMargins = ard.get('activationMargins')
        bonusIds = ard.get('bonusIds')
        crontabStart = ard.get('extraCrontabStart')
        crontabEnd = ard.get('extraCrontabEnd')
        if crontabStart and crontabEnd:
            if utils.inTimeTuplesRange(crontabStart, crontabEnd):
                bonusIdsEx = ard.get('extraBonusIds', ())
            else:
                bonusIdsEx = ()
        else:
            bonusIdsEx = ard.get('extraBonusIds', ())
        if not activationMargins or not bonusIds:
            return info
        stepInfoList = []
        btnEnabled = False
        bonusLen = min(len(bonusIds), len(activationMargins))
        satisfyCount = 0
        bonusExLen = len(bonusIdsEx)
        for i in xrange(bonusLen):
            activationMargin = activationMargins[i]
            itemInfo = {}
            bonusId = bonusIds[i]
            itemBonus = clientUtils.genItemBonus(bonusId)
            itemId, itemNum = itemBonus[0]
            itemInfo['slotInfo'] = uiUtils.getGfxItemById(itemId, itemNum)
            itemInfo['margin'] = activationMargin / 1000
            if i < bonusExLen and bonusIdsEx[i] != 0:
                bonusIdEx = bonusIdsEx[i]
                itemBonusEx = clientUtils.genItemBonus(bonusIdEx)
                itemIdEx, itemNumEx = itemBonusEx[0]
                itemInfo['slotExInfo'] = uiUtils.getGfxItemById(itemIdEx, itemNumEx)
                itemInfo['showSlotEx'] = True
            else:
                itemInfo['showSlotEx'] = False
            if activationMargin <= p.weekActivation:
                satisfyCount += 1
                if bonusId in p.weekActivationRewards:
                    itemInfo['state'] = uiConst.WEEK_ACTIVATION_STATE_REVEIVED
                else:
                    itemInfo['state'] = uiConst.WEEK_ACTIVATION_STATE_SATISFIED
                    btnEnabled = True
            else:
                itemInfo['state'] = uiConst.WEEK_ACTIVATION_STATE_NOT_SATISFIED
            stepInfoList.append(itemInfo)

        info['nowPoint'] = p.weekActivation / 1000
        info['stepsInfoList'] = stepInfoList
        info['btnEnable'] = btnEnabled
        info['status'] = '%d/3' % satisfyCount
        return info

    def onPushMessageClick(self, *args):
        self.uiAdapter.playRecomm.show(tabIdx=uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX, subTabIdx=uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB)

    def updateWeekActivationPushMsg(self):
        p = BigWorld.player()
        if not p:
            return
        if p.lv < PRCD.data.get('playRecommShowLv', 20):
            return
        hasReward = self.hasNotReceivedRewards()
        self.startCheckTimer()
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WEEK_ACTIVATION, {'click': self.onPushMessageClick})
        if hasReward and not self.uiAdapter.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_WEEK_ACTIVATION):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WEEK_ACTIVATION)
        elif not hasReward and self.uiAdapter.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_WEEK_ACTIVATION):
            self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WEEK_ACTIVATION)

    def startCheckTimer(self):
        if not self.hadCheckTimer:
            self.hadCheckTimer = True
            self.checkTimer()

    def checkTimer(self):
        timeList = []
        for key, value in PROAD.data.iteritems():
            startTime = value.get('startTime', None)
            endTime = value.get('endTime', None)
            conditionType = value.get('conditionType', gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY)
            if not conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_REWARD_ONLY:
                continue
            sec = utils.getNow()
            nextStart = min([ utils.nextByTimeTuple(s, sec) for s in startTime ]) + 60
            nextEnd = min([ utils.nextByTimeTuple(e, sec) for e in endTime ]) + 60
            nextStart and timeList.append(nextStart)
            nextEnd and timeList.append(nextEnd)

        if len(timeList):
            self.updateWeekActivationPushMsg()
            self.callbackTimer = BigWorld.callback(min(timeList), self.checkTimer)

    def checkCanGetAward(self):
        p = BigWorld.player()
        if not p or not hasattr(p, 'activationLv'):
            return False
        ard = {}
        for minLv, maxLv in ARD.data.keys():
            if minLv <= p.activationLv <= maxLv:
                ard = ARD.data.get((minLv, maxLv), {})
                break

        if not ard:
            return False
        activationMargins = ard.get('activationMargins')
        bonusIds = ard.get('bonusIds')
        if not activationMargins or not bonusIds:
            return False
        bonusLen = min(len(bonusIds), len(activationMargins))
        for i in xrange(bonusLen):
            bonusId = bonusIds[i]
            activationMargin = activationMargins[i]
            if activationMargin <= p.activation:
                if bonusId not in p.activationRewards:
                    return True

        return False
