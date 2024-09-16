#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInfoJingjieProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
import uiUtils
import jingJieUtils
import clientUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import quest_data as QD
from data import jingjie_data as JD
from data import mail_template_data as MTD
from cdata import jingjie_up_award_data as JUAD
MAX_JINGJIE_NUM = 6
MAX_BENEFIT_NUM = 6
MAX_REWARD_NUM = 6
REWARD_ITEM_OFFSET_Y = 25
REWARD_LIST_OFFSET_Y = 290

class RoleInfoJingjieProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoleInfoJingjieProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.curSelectedMC = None
        self.curSelectedJingjie = 0
        self.exciteOpenId = 0

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshLeftInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.helpIcon.helpKey = 1
        for i in xrange(MAX_JINGJIE_NUM):
            itemMc = getattr(self.widget, 'jingjie%d' % i, None)
            if not itemMc:
                continue
            itemMc.icon.jingjie = i + 1
            itemMc.icon.gotoAndStop('disabled')
            itemMc.icon.selectedMc.visible = False
            itemMc.shine.effect.visible = False
            ASUtils.setHitTestDisable(itemMc.shine, True)
            itemMc.icon.addEventListener(events.MOUSE_CLICK, self.handleClickJingjie, False, 0, True)
            itemMc.icon.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverJingjie, False, 0, True)
            itemMc.icon.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutJingjie, False, 0, True)

        self.widget.detail.conditionList.itemRenderer = 'RoleInformationJingjie_ConditionItem'
        self.widget.detail.conditionList.lableFunction = self.conditionItemFunction
        self.widget.detail.conditionList.itemHeight = 24
        self.widget.detail.goBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGoBtn, False, 0, True)

    def refreshLeftInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            curJingjie = p.jingJie
            self.widget.currentJingjieText.text = JD.data.get(curJingjie, {}).get('name', '')
            for i in xrange(MAX_JINGJIE_NUM):
                itemMc = getattr(self.widget, 'jingjie%d' % i, None)
                if not itemMc:
                    continue
                itemMc.icon.gotoAndStop('up' if curJingjie >= i + 1 else 'disabled')
                itemMc.shine.effect.visible = curJingjie == i + 1

            if self.curSelectedMC:
                self.refreshDetailInfo()
            else:
                bestJingjie = curJingjie + 1 if utils.checkUpgradeJingJie(p) else curJingjie
                if self.exciteOpenId:
                    bestJingjie = self.exciteOpenId
                    self.exciteOpenId = 0
                self.clickClickJingjie(bestJingjie if bestJingjie > 0 else 1)
            return

    def refreshDetailInfo(self):
        if not self.widget:
            return
        else:
            jdData = JD.data.get(self.curSelectedJingjie, {})
            if not jdData:
                return
            p = BigWorld.player()
            curJingjie = p.jingJie
            conditionList = self.getJingJieConditionList(jdData, curJingjie >= self.curSelectedJingjie)
            self.widget.detail.conditionList.dataArray = conditionList
            enableYSCheck = gameglobal.rds.configData.get('enableYSCheck', False)
            if curJingjie == 0:
                if not enableYSCheck:
                    result = uiConst.JINGJIE_CAN_REACH
                elif self.curSelectedJingjie == 1:
                    if utils.checkUpgradeJingJie(p):
                        result = uiConst.JINGJIE_CAN_REACH
                    else:
                        result = uiConst.JINGJIE_NOT_AVALIABLE
                else:
                    result = uiConst.JINGJIE_NOT_REACH
            elif self.curSelectedJingjie <= curJingjie:
                result = uiConst.JINGJIE_REACHED
            elif self.curSelectedJingjie == curJingjie + 1:
                if not enableYSCheck:
                    result = uiConst.JINGJIE_CAN_REACH
                elif utils.checkUpgradeJingJie(p):
                    result = uiConst.JINGJIE_CAN_REACH
                else:
                    result = uiConst.JINGJIE_NOT_AVALIABLE
            else:
                result = uiConst.JINGJIE_NOT_REACH
            if result == uiConst.JINGJIE_REACHED:
                self.widget.detail.goBtn.label = gameStrings.JINGJIE_REACHED_LABEL
            else:
                self.widget.detail.goBtn.label = gameStrings.JINGJIE_CAN_REACH_LABEL
            self.widget.detail.goBtn.enabled = result == uiConst.JINGJIE_CAN_REACH
            benefits = jdData.get('benefits', [])
            benefitsLen = len(benefits)
            for i in xrange(MAX_BENEFIT_NUM):
                benefitItemMc = getattr(self.widget.detail.benefitList, 'item%d' % i, None)
                if not benefitItemMc:
                    continue
                if i < benefitsLen:
                    benefitItemMc.visible = True
                    benefitItemMc.textField.htmlText = benefits[i]
                else:
                    benefitItemMc.visible = False

            if not gameglobal.rds.configData.get('enableAutoBreakJingJie', False):
                self.widget.detail.rewardList.visible = False
                return
            self.widget.detail.rewardList.visible = True
            self.widget.detail.rewardList.y = REWARD_LIST_OFFSET_Y + REWARD_ITEM_OFFSET_Y * min(benefitsLen, MAX_BENEFIT_NUM)
            juadData = JUAD.data.get((self.curSelectedJingjie, p.school), {})
            templateId = juadData.get('templateId', 0)
            bonusId = MTD.data.get(templateId, {}).get('bonusId', 0)
            rewardItems = clientUtils.genItemBonus(bonusId)
            totalItems = [ (itemId, itemNum, False) for itemId, itemNum in rewardItems ]
            apprenticeMailId = juadData.get('apprenticeMailId', 0)
            bonusId = MTD.data.get(apprenticeMailId, {}).get('bonusId', 0)
            rewardItems = clientUtils.genItemBonus(bonusId)
            totalItems.extend([ (itemId, itemNum, True) for itemId, itemNum in rewardItems ])
            totalLen = len(totalItems)
            for i in xrange(MAX_REWARD_NUM):
                rewardItemMc = getattr(self.widget.detail.rewardList, 'item%d' % i, None)
                if not rewardItemMc:
                    continue
                if i >= totalLen:
                    rewardItemMc.visible = False
                    continue
                rewardItemMc.visible = True
                itemId, itemNum, isApprentice = totalItems[i]
                itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
                rewardItemMc.slot.setItemSlotData(itemInfo)
                rewardItemMc.slot.dragable = False
                rewardItemMc.apprenticeIcon.visible = isApprentice

            return

    def getJingJieConditionList(self, jdData, reached):
        p = BigWorld.player()
        conditionList = []
        conditionsDesc = jdData.get('condition', [])
        conditionsName = jdData.get('conditionNames', [])
        checkJingJie = jdData.get('checkJingJie', [])
        conditionIdx = 0
        for cType, cond in checkJingJie:
            conditionData = {}
            checkFunc = getattr(jingJieUtils, jingJieUtils.jingJieCondCheckMap[cType], None)
            if checkFunc == None:
                continue
            conditionData['cType'] = cType
            isFinish, rate = checkFunc(p, cond)
            if reached or isFinish:
                conditionData['isFinish'] = True
                conditionData['rate'] = rate
            else:
                conditionData['isFinish'] = False
                conditionData['rate'] = rate
            if len(conditionsDesc) > conditionIdx:
                conditionData['desc'] = conditionsDesc[conditionIdx]
            else:
                conditionData['desc'] = ''
            if len(conditionsName) > conditionIdx:
                conditionData['name'] = conditionsName[conditionIdx]
            else:
                conditionData['name'] = ''
            conditionIdx += 1
            conditionList.append(conditionData)

        return conditionList

    def conditionItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.desc.htmlText = itemData.desc
        if itemData.isFinish:
            itemMc.rate.htmlText = ''
            itemMc.reachMc.gotoAndStop('reach')
            itemMc.searchBtn.visible = False
        else:
            itemMc.rate.htmlText = itemData.rate
            itemMc.reachMc.gotoAndStop('unreach')
            itemMc.searchBtn.cType = itemData.cType
            itemMc.searchBtn.visible = True
            itemMc.searchBtn.validateNow()
            itemMc.searchBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSearchBtn, False, 0, True)

    def handleClickGoBtn(self, *args):
        p = BigWorld.player()
        questList = JD.data.get(self.curSelectedJingjie, {}).get('questList', ())
        for questId in questList:
            if p.isQuestCompleted(questId):
                continue
            qdData = QD.data.get(questId, {})
            if p.isQuestComplete(questId):
                seekId = qdData.get('comNpcTk')
            else:
                seekId = qdData.get('acNpcTk')
            uiUtils.findPosWithAlert(seekId)
            break

    def handleClickJingjie(self, *args):
        p = BigWorld.player()
        if p.isUsingTemp():
            return
        e = ASObject(args[3][0])
        self.clickClickJingjie(e.currentTarget.jingjie)

    def clickClickJingjie(self, jingjie):
        itemMc = getattr(self.widget, 'jingjie%d' % (jingjie - 1), None)
        if not itemMc:
            return
        else:
            if self.curSelectedMC:
                self.curSelectedMC.selectedMc.visible = False
            self.curSelectedMC = itemMc.icon
            self.curSelectedMC.selectedMc.visible = True
            self.curSelectedJingjie = jingjie
            self.refreshDetailInfo()
            return

    def handleRollOverJingjie(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.selectedMc.visible = True

    def handleRollOutJingjie(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.jingjie != self.curSelectedJingjie:
            itemMc.selectedMc.visible = False

    def handleClickSearchBtn(self, *args):
        e = ASObject(args[3][0])
        cType = e.currentTarget.cType
        if cType == jingJieUtils.JINGJIE_CHECK_LV:
            self.uiAdapter.playRecomm.show()
        elif cType in (jingJieUtils.JINGJIE_CHECK_ACTIVE_SKILL_POINT, jingJieUtils.JINGJIE_CHECK_SKILL_ENHANCE_POINT, jingJieUtils.JINGJIE_CHECK_SKILL_ENHANCE):
            self.uiAdapter.skill.show(0)
        elif cType == jingJieUtils.JINGJIE_CHECK_WS:
            self.uiAdapter.skill.show(1)
        elif cType == jingJieUtils.JINGJIE_CHECK_AIR_SKILL:
            self.uiAdapter.skill.show(4)

    def openByExcitement(self, exciteOpenId = 0):
        self.exciteOpenId = exciteOpenId
        self.uiAdapter.roleInfo.show(uiConst.ROLEINFO_TAB_JINGJIE)
