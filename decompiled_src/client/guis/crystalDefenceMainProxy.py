#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crystalDefenceMainProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import sMath
import utils
import clientUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis import uiUtils
from callbackHelper import Functor
from data import hand_in_item_data as HIID
from cdata import hand_in_item_pos2item_data as HIIPD
from data import activity_basic_data as ABD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
RIGHTPANEL_PERSON_REWARD_NUMS = 4
LEFTPANEL_CRYSTAL_TYPE_NUMS = 4
LEFTPANEL_SPECIAL_TYPE_INDEX = 4
UPDATE_BTN_ENABLE_COUNT_DOWN_TIME = 30
TEMP_ICON_PATH = 'item/icon/42236.dds'

class CrystalDefenceMainProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrystalDefenceMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.activityID = 0
        self.HIID_ID = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CRYSTAL_DEFENCE_MAIN, self.hide)

    def reset(self):
        self.handInCntDict = {}
        self.needHandInCnt = 0
        self.uiTempData = {}
        self.currentServerRoundNums = 0
        self.currentPersonGetRewardRoundNums = 0
        self.serverPersonSubmitLimitNums = 0
        self.serverRoundNumsList = []
        self.serveRoundBonusList = []
        self.currentPersonSubmitNums = 0
        self.personSubmitNumsLimit = 0
        self.currentPersonGetRewardNums = 0
        self.personSubmitNumsList = []
        self.personSubmitNumsRewardList = []
        self.updateTimeCB = None
        self.updateTimeCountDown = 0
        self.isShowPushMessage = True
        self.activityEnd = False
        self.updatePanelFlag = False
        self.leftProgressBarDict = {}
        self.leftBottomBtnMC = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CRYSTAL_DEFENCE_MAIN:
            self.widget = widget
            self.reset()
            self.removeNewUpdateMsg()
            self.setNewUpdateMsgCallBack()
            self.getUIInitTempData()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CRYSTAL_DEFENCE_MAIN)
        if self.isShowPushMessage and not self.activityEnd:
            self.isShowPushMessage = False
            if self.checkActivityAllTime(self.activityID):
                self.pushNewUpdateMsg()

    def show(self, activityID, HIID_ID):
        if not self.widget:
            self.activityID = activityID
            self.HIID_ID = HIID_ID
            self.uiAdapter.loadWidget(uiConst.WIDGET_CRYSTAL_DEFENCE_MAIN)
            self.requestServerData()

    def getUIInitTempData(self):
        if 'curRewardPosX' not in self.uiTempData:
            self.uiTempData['curRewardPosX'] = self.widget.rewardPanel.currentReward.x
        if 'nextRewardPosX' not in self.uiTempData:
            self.uiTempData['nextRewardPosX'] = self.widget.rewardPanel.nextReward.x

    def initUI(self):
        self.initAllStaticDesc()
        self.initLeftPanelUI()
        self.initRightPanelUI()

    def initAllStaticDesc(self):
        allDesc = self.getCurDataFromHIIDByAttr('allDesc', {})
        self.widget.title.text.text = allDesc.get('mainTitle', gameStrings.NEED_CONFIG_DESC)
        self.widget.successRoundDesc.text = allDesc.get('mainSuccessRoundDesc', gameStrings.NEED_CONFIG_DESC)
        self.widget.itemClickDesc.text = allDesc.get('mainItemClickDesc', gameStrings.NEED_CONFIG_DESC)
        self.widget.mySubmitNumsDesc.text = allDesc.get('mainMySubmitNumsDesc', gameStrings.NEED_CONFIG_DESC)
        rp = self.widget.rewardPanel
        rp.rewardDesc.text = allDesc.get('RPDesc', gameStrings.NEED_CONFIG_DESC)
        rp.progress3.text = allDesc.get('RPProgressDesc', gameStrings.NEED_CONFIG_DESC)
        rp.tips.text = allDesc.get('RPBottomTips', gameStrings.NEED_CONFIG_DESC)
        rp.currentReward.rewardLabel.text = gameStrings.CRYSTAL_DEFENCE_SERVER_REWARD_CURRENT_DESC
        rp.nextReward.rewardLabel.text = gameStrings.CRYSTAL_DEFENCE_SERVER_REWARD_NEXT_DESC

    def initLeftPanelUI(self):
        self.widget.defaultCloseBtn = self.widget.minBtn
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)
        self.widget.helpIcon.visible = True
        self.widget.helpIcon.helpKey = self.getCurDataFromHIIDByAttr('helpKeyID', 0)
        self.widget.updateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickUpdateBtn, False, 0, True)
        self.widget.toggleReward.addEventListener(events.MOUSE_CLICK, self.handleClickToggleRewardBtn, False, 0, True)
        HIIPDIDList = self.getCurDataFromHIIDByAttr('positions', [])
        for index in xrange(LEFTPANEL_CRYSTAL_TYPE_NUMS):
            pathList = self.getCurDataFromHIIDByAttr('iconPath', [])
            path = pathList[index] if len(pathList) > index else TEMP_ICON_PATH
            cpMC = getattr(self.widget, 'crystalProgress%d' % index)
            cpMC.currentSubmitProgress.labelFunction = self.progressLableFunc
            cpMC.icon.fitSize = True
            cpMC.icon.clear()
            cpMC.icon.loadImage(path)
            cpMC.submit.HIIPD_ID = HIIPDIDList[index]
            cpMC.submit.itemID = self.getDataFromHIIPDByID(HIIPDIDList[index], 'originItem', 0)
            cpMC.submit.replaceItemID = self.getDataFromHIIPDByID(HIIPDIDList[index], 'replaceItems', 0)[0]
            cpMC.submit.addEventListener(events.MOUSE_CLICK, self.handleClickSubmitBtn, False, 0, True)
            self.leftProgressBarDict[HIIPDIDList[index]] = cpMC.currentSubmitProgress

        for index in xrange(LEFTPANEL_CRYSTAL_TYPE_NUMS):
            itemMC = getattr(self.widget, 'item%d' % index)
            if itemMC is None:
                continue
            itemMC.visible = False
            itemMC.dragable = False
            if index < len(HIIPDIDList):
                itemMC.visible = True
                itemMC.pathNPCData = self.getDataFromHIIPDByID(HIIPDIDList[index], 'pathNpc', None)
                itemMC.itemID = self.getDataFromHIIPDByID(HIIPDIDList[index], 'originItem', 0)
                itemMC.replaceItemID = self.getDataFromHIIPDByID(HIIPDIDList[index], 'replaceItems', 0)[0]
                itemMC.addEventListener(events.MOUSE_CLICK, self.handleClickItemBtnToNavigate, False, 0, True)
                self.leftBottomBtnMC.append(itemMC)

        specialItemMC = getattr(self.widget, 'item%d' % LEFTPANEL_SPECIAL_TYPE_INDEX)
        specialItemMC.dragable = False
        if specialItemMC is not None:
            specialItemID = self.getDataFromHIIPDByID(HIIPDIDList[0], 'replaceItems', 0)[0]
            specialItemMC.itemID = specialItemID
            self.leftBottomBtnMC.append(specialItemMC)

    def initRightPanelUI(self):
        self.widget.rewardPanel.visible = True
        self.widget.rewardPanel.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickToggleRewardCloseBtn, False, 0, True)
        self.widget.rewardPanel.serverRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickServerRewardBtn, False, 0, True)
        self.widget.rewardPanel.personRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPersonRewardBtn, False, 0, True)

    def requestServerData(self):
        BigWorld.player().base.getHandInItemAllDailyData(self.activityID)

    def getServerDataDict(self):
        p = BigWorld.player()
        handInItemDict = p.handInItemDict if hasattr(p, 'handInItemDict') else {}
        return handInItemDict.get(self.activityID, {})

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshData()
        self.refreshLeftPanelUI()
        self.refreshRightPanelUI()
        self.showRefreshMsg()

    def refreshData(self):
        if not self.widget:
            return
        handInItemDict = self.getServerDataDict()
        self.handInCntDict = handInItemDict.get('posInfo', {})
        self.needHandInCnt = handInItemDict.get('needItemCnt', 1)
        self.currentServerRoundNums = handInItemDict.get('roundNo', 0) - 1
        self.currentPersonGetRewardRoundNums = handInItemDict.get('bGetRewards', 0)
        self.serverPersonSubmitLimitNums = self.getCurDataFromHIIDByAttr('personSubmitLimit', 0)
        self.serverRoundNumsList = self.getCurDataFromHIIDByAttr('dailyReward', {}).keys()
        self.serveRoundBonusList = self.getCurDataFromHIIDByAttr('dailyReward', {}).values()
        self.currentPersonSubmitNums = handInItemDict.get('handInCnt', 0)
        self.personSubmitNumsLimit = self.getCurDataFromHIIDByAttr('handInLimt', 0)
        self.currentPersonGetRewardNums = handInItemDict.get('bGetHandInCntRewards', 0)
        self.personSubmitNumsList = self.getCurDataFromHIIDByAttr('dailyCntReward', {}).keys()
        self.personSubmitNumsRewardList = self.getCurDataFromHIIDByAttr('dailyCntReward', {}).values()

    def showRefreshMsg(self):
        if self.updatePanelFlag:
            self.showGameMsgByID(GMDD.data.CRYSTAL_DEFENCE_UPDATE_PANEL_SUCCESS)
            self.updatePanelFlag = False

    def refreshLeftPanelUI(self):
        if not self.widget:
            return
        else:
            self.refreshUpdateBtn()
            self.refreshCountDownUI()
            if len(self.handInCntDict) >= 0:
                for posID, handInCnt in self.handInCntDict.iteritems():
                    cpMC = self.leftProgressBarDict[posID]
                    cpMC.currentValue = handInCnt
                    cpMC.maxValue = self.needHandInCnt

            else:
                for cpMC in self.leftProgressBarDict.values():
                    cpMC.currentValue = 0
                    cpMC.maxValue = self.needHandInCnt

            self.widget.mySubmitNums.text = '%d/%d' % (self.currentPersonSubmitNums, self.personSubmitNumsLimit)
            self.widget.serverCleanseNums.text = str(self.currentServerRoundNums)
            for itemMC in self.leftBottomBtnMC:
                if itemMC is None:
                    continue
                count = BigWorld.player().inv.countItemInPages(itemMC.itemID, enableParentCheck=True)
                itemMC.setItemSlotData(uiUtils.getGfxItemById(itemMC.itemID))
                itemMC.validateNow()
                itemMC.setValueAmountTxt('%d' % count)

            return

    def refreshCountDownUI(self):
        nextTimeStamp = self.getNearStartTimeStamp()
        if nextTimeStamp is None:
            countDownContent = self.getCurDataFromHIIDByAttr('allDesc', {}).get('mainCenterHintTime', '')
            if countDownContent:
                self.widget.countDown.visible = True
                self.widget.countDownBg.visible = True
                self.widget.countDown.text = self.getCurDescFromCID('mainCenterHintTime')
            else:
                self.widget.countDown.visible = False
                self.widget.countDownBg.visible = False
        else:
            self.widget.countDown.visible = True
            self.widget.countDownBg.visible = True
            self.widget.countDown.text = self.getCurDescFromCID('mainCenterHintTime') + self.getTimeStrByCountDownStamp(nextTimeStamp - utils.getNow())

    def refreshUpdateBtn(self):
        if not self.widget:
            return
        if self.updateTimeCountDown > 0:
            self.widget.updateBtn.enable = False
            self.widget.updateBtn.label = gameStrings.UPDATE_TIME_IN_CD % self.updateTimeCountDown
        else:
            self.widget.updateBtn.enable = True
            self.widget.updateBtn.label = gameStrings.UPDATE_TIME

    def handleClickCloseBtn(self, *args):
        self.showYesNoMsgBoxByMsgID(GMDD.data.CRYSTAL_DEFENCE_FORCE_CLOSE_MSG, self.closeUIWithFlag)

    def closeUIWithFlag(self):
        self.isShowPushMessage = False
        self.hide()

    def handleClickToggleRewardBtn(self, *args):
        self.widget.rewardPanel.visible = True
        self.refreshRightPanelUI()

    def handleClickUpdateBtn(self, *args):
        if self.updateTimeCB is None:
            self.updateTimeCountDown = UPDATE_BTN_ENABLE_COUNT_DOWN_TIME
            self.updateTimeCB = BigWorld.callback(1, self.updateBtnTimer)
            self.refreshUpdateBtn()
            self.updatePanelFlag = True
            self.requestServerData()

    def updateBtnTimer(self):
        if not self.widget:
            return
        else:
            self.updateTimeCountDown -= 1
            if self.updateTimeCountDown > 0:
                self.updateTimeCB = BigWorld.callback(1, self.updateBtnTimer)
            else:
                self.updateTimeCB = None
            self.refreshUpdateBtn()
            return

    def handleClickItemBtnToNavigate(self, *args):
        itemMC = ASObject(args[3][0]).currentTarget
        pathData = getattr(itemMC, 'pathNPCData')
        if pathData:
            uiUtils.findPosById(tuple(pathData))

    def handleClickSubmitBtn(self, *args):
        itemMC = ASObject(args[3][0]).currentTarget
        itemNums = self.getItemNumnsByID(itemMC.itemID)
        replaceItemNums = self.getItemNumnsByID(itemMC.replaceItemID)
        if self.currentPersonSubmitNums >= self.personSubmitNumsLimit:
            self.showGameMsg(self.getCurDescFromCID('personSubmitLimitMsg'))
            return
        if itemNums == 0 and replaceItemNums == 0:
            self.showGameMsg(self.getCurDescFromCID('personSubmitNumsNoneMsg'))
            return
        if itemNums == 0 and replaceItemNums != 0:
            self.showYesNoMsgBox(self.getCurDescFromCID('personSubmitHaveReplaceItemMsg'), Functor(self.requestSubmitReplaceItem, self.activityID, itemMC.HIIPD_ID))
            return
        itemName = self.getDataFromHIIPDByID(itemMC.HIIPD_ID, 'name', '')
        configMsg = self.getCurDescFromCID('ifSubmitItemMsg')
        configMsg = configMsg % itemName if configMsg else gameStrings.IF_SUBMIT_ITEM
        self.showYesNoMsgBox(configMsg, Functor(self.requestSubmitItem, self.activityID, itemMC.HIIPD_ID))

    def requestSubmitItem(self, activityID, HIIPD_ID):
        BigWorld.player().base.handInCollectItems(activityID, HIIPD_ID)

    def requestSubmitReplaceItem(self, activityID, HIIPD_ID):
        BigWorld.player().base.handInCollectItemsReplace(activityID, HIIPD_ID)

    def progressLableFunc(self, *args):
        currentVal = int(args[3][0].GetNumber())
        maxVal = int(args[3][1].GetNumber())
        return GfxValue('%d%%' % round(currentVal * 100.0 / maxVal, 2))

    def handleClickToggleRewardCloseBtn(self, *args):
        self.widget.rewardPanel.visible = False

    def refreshRightPanelUI(self):
        if not self.widget:
            return
        if not self.widget.rewardPanel.visible:
            return
        self.refreshRightPanelServerUI()
        self.refreshRightPanelPersonUI()

    def refreshRightPanelServerUI(self):
        if not self.widget:
            return
        else:
            rpMC = self.widget.rewardPanel
            rpMC.serverRewardDesc.text = self.getCurDescFromCID('RPSubmitLimitDesc') % self.serverPersonSubmitLimitNums
            if self.currentServerRoundNums <= self.serverRoundNumsList[0]:
                progressBgHeight = rpMC.progress.bg.height * 1.0 / len(self.serverRoundNumsList)
                roundRatio = self.currentServerRoundNums * 1.0 / self.serverRoundNumsList[0]
                rpMC.progress.barMask.height = sMath.clamp(roundRatio * progressBgHeight, 0, progressBgHeight)
            else:
                progressBgHeight = rpMC.progress.bg.height - rpMC.progress.bg.height * 1.0 / len(self.serverRoundNumsList)
                ratioUp = self.currentServerRoundNums - self.serverRoundNumsList[0]
                ratioDown = self.serverRoundNumsList[len(self.serverRoundNumsList) - 1] - self.serverRoundNumsList[0]
                roundRatio = ratioUp * 1.0 / ratioDown
                rpMC.progress.barMask.height = sMath.clamp(roundRatio * progressBgHeight, 0, progressBgHeight) + rpMC.progress.bg.height * 1.0 / len(self.serverRoundNumsList)
            rpMC.progress.barMask.y = rpMC.progress.bg.height - rpMC.progress.barMask.height
            currentRoundNumsIndex = None
            for index in xrange(len(self.serverRoundNumsList)):
                serverRoundNums = self.serverRoundNumsList[index]
                progressRoundMC = getattr(rpMC, 'progress%d' % index)
                if progressRoundMC is not None:
                    progressRoundMC.text = self.getCurDescFromCID('RPProgressNumsDesc') % serverRoundNums
                if self.currentServerRoundNums >= serverRoundNums:
                    currentRoundNumsIndex = index

            self.refreshRightPanelServerRewardBtnUI(currentRoundNumsIndex)
            self.refreshRightPanelServerRewardItemUI(currentRoundNumsIndex)
            return

    def refreshRightPanelServerRewardBtnUI(self, currentRoundNumsIndex):
        rpMC = self.widget.rewardPanel
        rpMC.serverRewardBtn.enabled = False
        rpMC.serverRewardBtn.label = gameStrings.UNABLE_TO_GET_REWARD
        if self.currentPersonSubmitNums >= self.serverPersonSubmitLimitNums:
            if currentRoundNumsIndex is not None and currentRoundNumsIndex >= 0:
                if self.currentPersonGetRewardRoundNums < self.serverRoundNumsList[currentRoundNumsIndex]:
                    rpMC.serverRewardBtn.enabled = True
                    rpMC.serverRewardBtn.label = gameStrings.GET_REWARD
                else:
                    rpMC.serverRewardBtn.enabled = False
                    rpMC.serverRewardBtn.label = gameStrings.HAVE_GOT_REWARD

    def refreshRightPanelServerRewardItemUI(self, currentRoundNumsIndex):
        rpMC = self.widget.rewardPanel
        curRMC = rpMC.currentReward
        nextRMC = rpMC.nextReward
        curRItemMC = curRMC.Item
        nextRItemMC = nextRMC.Item
        curRMC.visible = False
        nextRMC.visible = False
        curRItemMC.dragable = False
        nextRItemMC.dragable = False
        curRItemID = None
        curRItemNums = 0
        nextRItemID = None
        nextRItemNums = 0
        if currentRoundNumsIndex is None:
            nextRMC.visible = True
            nextRMC.x = self.uiTempData['curRewardPosX']
            nextRItemID, nextRItemNums = self.getOneItemDataByBonusID(self.serveRoundBonusList[0])
        elif currentRoundNumsIndex == len(self.serverRoundNumsList) - 1:
            curRMC.visible = True
            curRItemID, curRItemNums = self.getOneItemDataByBonusID(self.serveRoundBonusList[currentRoundNumsIndex])
        else:
            curRMC.visible = True
            nextRMC.visible = True
            nextRMC.x = self.uiTempData['nextRewardPosX']
            curRItemID, curRItemNums = self.getOneItemDataByBonusID(self.serveRoundBonusList[currentRoundNumsIndex])
            nextRItemID, nextRItemNums = self.getOneItemDataByBonusID(self.serveRoundBonusList[currentRoundNumsIndex + 1])
        if curRItemID:
            curRItemMC.setItemSlotData(uiUtils.getGfxItemById(curRItemID, count=curRItemNums))
        if nextRItemID:
            nextRItemMC.setItemSlotData(uiUtils.getGfxItemById(nextRItemID, count=nextRItemNums))

    def refreshRightPanelPersonUI(self):
        if not self.widget:
            return
        else:
            rpMC = self.widget.rewardPanel
            rpMC.personSubmitNums.text = self.getCurDescFromCID('RPCurSubmitDesc') + str(self.currentPersonSubmitNums)
            ASUtils.setHitTestDisable(rpMC.slotFrame, True)
            curPersonHasGetRewardIndex = -1
            for index in xrange(len(self.personSubmitNumsList)):
                if self.currentPersonGetRewardNums >= self.personSubmitNumsList[index]:
                    curPersonHasGetRewardIndex = index

            rpMC.personRewardBtn.enabled = False
            rpMC.personRewardBtn.label = gameStrings.UNABLE_TO_GET_REWARD
            for index in xrange(RIGHTPANEL_PERSON_REWARD_NUMS):
                bonusMC = getattr(rpMC, 'bonus%d' % index)
                bonusConditionMC = getattr(rpMC, 'bonusCondition%d' % index)
                if bonusMC is not None:
                    bonusMC.visible = False
                    bonusMC.dragable = False
                    bonusConditionMC.visible = False
                    if index < len(self.personSubmitNumsList):
                        bonusMC.visible = True
                        itemID, itemNums = self.getOneItemDataByBonusID(self.personSubmitNumsRewardList[index])
                        bonusMC.setItemSlotData(uiUtils.getGfxItemById(itemID, itemNums))
                        bonusConditionMC.visible = True
                        bonusConditionMC.text = self.getCurDescFromCID('RPNeedNumsDesc') % self.personSubmitNumsList[index]
                        if index <= curPersonHasGetRewardIndex:
                            bonusConditionMC.htmlText = uiUtils.toHtml(gameStrings.HAVE_GOT_REWARD, '#808080')
                            rpMC.personRewardBtn.enabled = False
                            rpMC.personRewardBtn.label = gameStrings.HAVE_GOT_REWARD
                        if index > curPersonHasGetRewardIndex:
                            if self.currentPersonSubmitNums >= self.personSubmitNumsList[index]:
                                bonusConditionMC.htmlText = uiUtils.toHtml(gameStrings.GET_REWARD, '#79C725')
                                rpMC.personRewardBtn.enabled = True
                                rpMC.personRewardBtn.label = gameStrings.GET_REWARD

            return

    def handleClickServerRewardBtn(self, *args):
        BigWorld.player().base.getHandInItemDailyReward(self.activityID)

    def handleClickPersonRewardBtn(self, *args):
        BigWorld.player().base.getHandInItemDailyCntReward(self.activityID)

    def signUpOrShowCrystalMain(self, actID, HIID_ID):
        isSignUp = False
        if hasattr(BigWorld.player(), 'handInItemActSignUpData'):
            isSignUp = BigWorld.player().handInItemActSignUpData.get(actID, False)
        waitActivityTimeMsgContent = self.getDescFromCID(HIID_ID, 'waitActivityTimeMsg')
        notActivityTimeMsgContent = self.getDescFromCID(HIID_ID, 'notActivityTimeMsg')
        if isSignUp:
            if self.checkActivityAllTime(actID):
                self.show(actID, HIID_ID)
            else:
                msg = self.getTimeStrFromActivityStart(actID)
                if msg is None:
                    BigWorld.player().showTopMsg(notActivityTimeMsgContent)
                else:
                    BigWorld.player().showTopMsg(waitActivityTimeMsgContent + msg)
        elif self.checkSignUpTime(actID):
            BigWorld.player().base.getSignUpFlag(actID)
            BigWorld.player().base.signupHandInItem(actID)
        else:
            BigWorld.player().showTopMsg(notActivityTimeMsgContent)
        self.removeNewUpdateMsg()

    def getDescFromCID(self, HIID_ID, name):
        allDesc = self.getDataFromHIIDByAttr(HIID_ID, 'allDesc', {})
        return allDesc.get(name, gameStrings.NEED_CONFIG_DESC + name)

    def getDataFromHIIDByAttr(self, HIID_ID, attribute, default):
        activityData = HIID.data.get(HIID_ID, None)
        if activityData is None:
            return default
        else:
            return activityData.get(attribute, default)

    def getCurDescFromCID(self, name):
        allDesc = self.getCurDataFromHIIDByAttr('allDesc', {})
        return allDesc.get(name, gameStrings.NEED_CONFIG_DESC + name)

    def getCurDataFromHIIDByAttr(self, attribute, default):
        activityData = HIID.data.get(self.HIID_ID, None)
        if activityData is None:
            return default
        else:
            return activityData.get(attribute, default)

    def getDataFromHIIPDByID(self, ID, attribute, default):
        itemData = HIIPD.data.get(ID, None)
        if itemData is None:
            return default
        else:
            return itemData.get(attribute, default)

    def pushNewUpdateMsg(self):
        if gameglobal.rds.configData.get('enableCollectItemMessagePush', False):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE, {'data': (self.activityID, self.HIID_ID)})

    def removeNewUpdateMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE)

    def setNewUpdateMsgCallBack(self):
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE, {'click': self.pushNewUpdateCallBack})

    def pushNewUpdateCallBack(self):
        activityID, HIID_ID = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE).get('data', (0, 0))
        if activityID and HIID_ID:
            gameglobal.rds.ui.crystalDefenceMain.signUpOrShowCrystalMain(activityID, HIID_ID)

    def getPushMsgTip(self):
        tipMsg = GMD.data.get(GMDD.data.CRYSTAL_DEFENCE_PUSH_MSG_TIPS, {}).get('text', gameStrings.CRYSTAL_DEFENCE_PUSH_MESSAGE_TIPS)
        return tipMsg

    def setActivityEnd(self, actID):
        if not self.widget:
            return
        if self.activityID == actID:
            self.activityEnd = True
            self.refreshInfo()
            self.showGameMsg(self.getCurDescFromCID('activityEndMsg'))

    def getOneItemDataByBonusID(self, bonusID):
        itemDataList = clientUtils.genItemBonus(bonusID)
        if itemDataList:
            return (itemDataList[0][0], itemDataList[0][1])
        else:
            return (0, 0)

    def getItemNumnsByID(self, itemID):
        p = BigWorld.player()
        return p.inv.countItemInPages(itemID)

    def showGameMsgByID(self, gameMsgId):
        BigWorld.player().showGameMsg(gameMsgId, ())

    def showGameMsg(self, content):
        BigWorld.player().showTopMsg(content)

    def showYesNoMsgBoxByMsgID(self, gameMsgId, funcName):
        msg = GMD.data.get(gameMsgId, {}).get('text', None)
        if not msg:
            funcName()
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(funcName))

    def showYesNoMsgBox(self, content, funcName):
        if not content:
            funcName()
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(content, Functor(funcName))

    def showSubmitSuccessMsg(self, activityID, HIIPD_ID):
        if activityID == self.activityID:
            successMsg = self.getCurDescFromCID('successSubmitItemMsg')
            itemName = self.getDataFromHIIPDByID(HIIPD_ID, 'name', '')
            successMsg = successMsg % itemName if successMsg else gameStrings.SUCCESS_SUBMIT_ITEM
            self.showGameMsg(successMsg)

    def checkSignUpTime(self, activityID):
        data = ABD.data.get(activityID, {})
        joinActTimeList = data.get('joinActTime', ())
        weekSet = data.get('weekSet', 0)
        for joinActTime in joinActTimeList:
            if utils.inCrontabRange(joinActTime[0], joinActTime[1], weekSet=weekSet):
                return True

        return False

    def checkActivityTime(self, activityID):
        data = ABD.data.get(activityID, {})
        weekSet = data.get('weekSet', 0)
        startTimes = data.get('startTimes', ())
        endTimes = data.get('endTimes', ())
        if endTimes and startTimes:
            for index in xrange(len(startTimes)):
                if utils.inCrontabRange(startTimes[index], endTimes[index], weekSet=weekSet):
                    return True

        return False

    def checkActivityAllTime(self, activityID):
        data = ABD.data.get(activityID, {})
        weekSet = data.get('weekSet', 0)
        startTimes = data.get('startTimes', ())
        endTimes = data.get('endTimes', ())
        if endTimes and startTimes:
            if utils.inCrontabRange(startTimes[0], endTimes[-1], weekSet=weekSet):
                return True
        return False

    def checkServerTime(self):
        now = utils.getNow()
        serverDataDict = self.getServerDataDict()
        startTime = serverDataDict.get('start', 0)
        endTime = serverDataDict.get('end', 0)
        if startTime < now < endTime:
            return True
        return False

    def getNearStartTimeStamp(self):
        refreshTime = self.getCurDataFromHIIDByAttr('refreshTime', ())
        nextTime = None
        nowTime = utils.getNow()
        for rTime in refreshTime:
            tempNextTime = utils.getNextCrontabTime(rTime[0])
            if nowTime < tempNextTime:
                if nextTime is None:
                    nextTime = tempNextTime
                else:
                    nextTime = min(nextTime, tempNextTime)

        return nextTime

    def getTimeStrByCountDownStamp(self, stamp):
        day = stamp // 86400
        stamp = stamp % 86400
        hour = stamp // 3600
        minute = stamp % 3600 // 60
        second = stamp % 60
        if day != 0:
            return gameStrings.COUNT_DOWN_TIME_DAY % (day,
             hour,
             minute,
             second)
        if hour != 0:
            return gameStrings.COUNT_DOWN_TIME_HOUR % (hour, minute, second)
        return gameStrings.COUNT_DOWN_TIME_MINUTE % (minute, second)

    def getTimeStrFromActivityStart(self, activityID):
        data = ABD.data.get(activityID, {})
        weekSet = data.get('weekSet', 0)
        startTimes = data.get('startTimes', ())
        resultStamp = None
        if startTimes:
            for startTime in startTimes:
                tempStartStamp = utils.getNextCrontabTime(startTime, weekSet=weekSet)
                if utils.getNow() < tempStartStamp:
                    if resultStamp is None:
                        resultStamp = tempStartStamp
                    else:
                        resultStamp = min(resultStamp, tempStartStamp)

        if resultStamp and resultStamp - utils.getNow() < 2592000:
            return self.getTimeStrByCountDownStamp(resultStamp - utils.getNow())
        else:
            return
