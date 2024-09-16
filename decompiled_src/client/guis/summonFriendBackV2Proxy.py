#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendBackV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import events
import gameglobal
import gametypes
import utils
import uiConst
from uiProxy import UIProxy
from Scaleform import GfxValue
from asObject import ASObject
from guis import summonFriendRecall
from asObject import RedPotManager
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import school_data as SD
from data import friend_recall_data as FRD
INVITE_SHOP_ID = 308
TAB_MAX_COUNT = 6
TABLE_BTN_NAME_BATTLE = 'battleBtn'
TABLE_BTN_NAME_RECALL = 'recallBtn'
m_tTabBtnDict = {TABLE_BTN_NAME_BATTLE: 'battleMc',
 TABLE_BTN_NAME_RECALL: 'recallMc'}

class SummonFriendBackV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendBackV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectTabBtnName = ''
        self.tabBtnList = []
        self.summonFriendList = []
        self.summonedFriendList = []
        self.stateMap = {0: gameStrings.TEXT_UIUTILS_1414,
         1: gameStrings.TEXT_FRIENDPROXY_293_1,
         2: gameStrings.TEXT_FRIENDPROXY_293_2,
         3: gameStrings.TEXT_FRIENDPROXY_293_3,
         4: gameStrings.TEXT_FRIENDPROXY_293_4}
        self.recallProxy = summonFriendRecall.SummonFriendRecall(self)
        self.subProxys = {TABLE_BTN_NAME_BATTLE: self,
         TABLE_BTN_NAME_RECALL: self.recallProxy}

    def reset(self):
        self.selectTabBtnName = ''
        self.tabBtnList = []

    def unRegisterPanel(self):
        self.recallProxy.hideWidget()
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.tabBtnList = []
        for i, btnName in enumerate(m_tTabBtnDict):
            tabBtn = self.widget.recallFriendPanel.getChildByName(btnName)
            tabBtn.removeEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
            if tabBtn.name == TABLE_BTN_NAME_RECALL:
                RedPotManager.removeRedPotById(uiConst.SUMMON_FRIEND_RECALL_BTN_RED_POT)
                if self.isBackInValidTime() and self.enableRecall():
                    self.tabBtnList.append(tabBtn)
                    tabBtn.visible = True
                    RedPotManager.addRedPot(tabBtn, uiConst.SUMMON_FRIEND_RECALL_BTN_RED_POT, (tabBtn.width - 7, -4), self.visiblePotFunRecallBtn)
                else:
                    tabBtn.visible = False
            else:
                self.tabBtnList.append(tabBtn)
            if tabBtn.visible and not self.selectTabBtnName:
                self.selectTabBtnName = btnName
            tabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)

        self.refreshTabBtns()

    def visiblePotFunRecallBtn(self, *args):
        isRedPot = self.checkRedFlag()
        return GfxValue(isRedPot)

    def updateRedPotRecallBtn(self):
        RedPotManager.updateRedPot(uiConst.SUMMON_FRIEND_RECALL_BTN_RED_POT)

    def enableRecall(self):
        return gameglobal.rds.configData.get('enableFriendRecall', False)

    def isBackInValidTime(self):
        frdData = FRD.data.get(SCD.data.get('friendRecallActivityId', gametypes.FRIEND_RECALL_ID), {})
        flag = False
        openOp = frdData.get('openOp', 0)
        if not openOp:
            return flag
        beginTime = frdData.get('crontabStart')
        endTime = frdData.get('crontabEnd')
        if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() and utils.getNow() <= utils.getDisposableCronTabTimeStamp(endTime):
            flag = True
        return flag

    def refreshTabBtns(self):
        tabCount = len(self.tabBtnList)
        for i in range(tabCount):
            tabBtn = self.tabBtnList[i]
            tabBtn.x = 102 * i
            tabBtn.focusable = False

    def refreshInfo(self):
        if not self.widget:
            return
        self.getSelectedSubProxy().showWidget()

    def getSelectedSubProxy(self):
        return self.subProxys.get(self.selectTabBtnName)

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        self.setTabSelected(btnName)

    def setTabSelected(self, btnName):
        if btnName != self.selectTabBtnName:
            self.selectTabBtnName = btnName
            subProxy = self.subProxys.get(btnName)
            if subProxy:
                subProxy.showWidget()

    def showWidget(self):
        self.updateTabBtnState()

    def updateTabBtnState(self):
        for i, btnName in enumerate(m_tTabBtnDict):
            btnMc = self.widget.recallFriendPanel.getChildByName(btnName)
            panelMc = self.widget.recallFriendPanel.getChildByName(m_tTabBtnDict[btnName])
            if btnName == self.selectTabBtnName:
                btnMc.selected = True
                if panelMc:
                    panelMc.visible = True
                    self.updateSelectTabMc(panelMc)
            else:
                btnMc.selected = False
                if panelMc:
                    panelMc.visible = False

    def updateSelectTabMc(self, panelMc):
        if panelMc.name == 'battleMc':
            self.refreshWidget()
        else:
            self.recallProxy.refreshWidget()

    def refreshWidget(self):
        battleMc = self.widget.recallFriendPanel.battleMc
        battleMc.textField.text = str(SCD.data.get('INVITE_POINT_WITH_FLOWBACK_SEND_MSG', 0))
        battleMc.textField2.text = str(SCD.data.get('INVITE_POINT_WITH_FLOWBACK_SUCC', 0))
        battleMc.summonFrame.itemRenderer = 'SummonFriendBackV2_PlayerItem'
        battleMc.summonFrame.lableFunction = self.summonFirendLabelFun
        battleMc.summonedFrame.itemRenderer = 'SummonFriendBackV2_PlayerItem'
        battleMc.summonedFrame.lableFunction = self.summonedFriendLabelFun
        self.refreshSummonFriend()

    def refreshSummonFriend(self):
        if not self.widget:
            return
        if not self.widget.recallFriendPanel:
            return
        if not self.widget.recallFriendPanel.battleMc:
            return
        battleMc = self.widget.recallFriendPanel.battleMc
        self.summonFriendList = self.friendListFilter(self.summonFriendList)
        self.summonedFriendList = self.friendListFilter(self.summonedFriendList)
        battleMc.summonFrame.dataArray = range(len(self.summonFriendList))
        battleMc.summonFrame.validateNow()
        battleMc.summonedFrame.dataArray = range(len(self.summonedFriendList))
        battleMc.summonedFrame.validateNow()
        battleMc.onLineCount.text = '%d/%d' % (self.getOnLineCount(self.summonedFriendList), len(self.summonedFriendList))

    def friendListFilter(self, list):
        list = [ element for element in list if not self.isDeleted(element) ]
        return list

    def getOnLineCount(self, list):
        p = BigWorld.player()
        count = 0
        for fid in self.summonedFriendList:
            friendInfo = p.getFValByGbId(fid)
            if friendInfo.state == gametypes.FRIEND_STATE_ONLINE:
                count += 1

        return count

    def isDeleted(self, fid):
        friendInfo = BigWorld.player().getFValByGbId(fid)
        if friendInfo:
            return False
        else:
            return True

    def summonFirendLabelFun(self, *args):
        index = int(args[3][0].GetNumber())
        id = self.summonFriendList[index]
        mc = ASObject(args[3][1])
        p = BigWorld.player()
        friendInfo = p.friend.get(id, None)
        if not friendInfo:
            return
        else:
            mc.isOnLine.visible = False
            mc.name = str(index)
            mc.ruleIcon.fitSize = True
            photo = 'headIcon/%s.dds' % str(friendInfo.school * 10 + friendInfo.sex)
            mc.ruleIcon.loadImage(photo)
            mc.txtName.text = friendInfo.name
            mc.txtSchool.text = SD.data[friendInfo.school]['name']
            mc.txtLv.text = 'LV.%d' % friendInfo.level
            mc.chatBtn.label = gameStrings.TEXT_SUMMONFRIENDBACKV2PROXY_222
            mc.chatBtn.removeEventListener(events.MOUSE_CLICK, self.onChatClick)
            mc.chatBtn.addEventListener(events.MOUSE_CLICK, self.onCallBackClick, False, 0, True)
            return

    def onCallBackClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.parent.name)
        fid = self.summonFriendList[index]
        gameglobal.rds.ui.callFriend.show(fid)

    def summonedFriendLabelFun(self, *args):
        index = int(args[3][0].GetNumber())
        id = self.summonedFriendList[index]
        mc = ASObject(args[3][1])
        p = BigWorld.player()
        friendInfo = p.getFValByGbId(id)
        if not friendInfo:
            return
        stateName = self.stateMap[friendInfo.state]
        mc.isOnLine.visible = True
        mc.isOnLine.text = stateName
        mc.name = str(index)
        mc.ruleIcon.fitSize = True
        photo = 'headIcon/%s.dds' % str(friendInfo.school * 10 + friendInfo.sex)
        mc.ruleIcon.loadImage(photo)
        mc.txtName.text = friendInfo.name
        mc.txtSchool.text = SD.data[friendInfo.school]['name']
        mc.txtLv.text = 'LV.%d' % friendInfo.level
        mc.chatBtn.label = gameStrings.TEXT_GAMECONST_116
        mc.chatBtn.removeEventListener(events.MOUSE_CLICK, self.onCallBackClick)
        mc.chatBtn.addEventListener(events.MOUSE_CLICK, self.onChatClick, False, 0, True)

    def onChatClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.parent.name)
        fid = self.summonedFriendList[index]
        gameglobal.rds.ui.friend.beginChat(fid)

    def setSummonFriendList(self, summonFriendList):
        self.summonFriendList = self.removeKuaFuFriend(summonFriendList)
        self.refreshSummonFriend()

    def setSummonedFriendList(self, summonedFriendList):
        self.summonedFriendList = summonedFriendList
        self.refreshSummonFriend()

    def refreshCallFriendsList(self, inviteList):
        self.summonFriendList = self.removeKuaFuFriend(inviteList)
        self.refreshSummonFriend()

    def removeKuaFuFriend(self, friendList):
        list = []
        p = BigWorld.player()
        for id in friendList:
            if not p.isGobalFirendGbId(id):
                list.append(id)

        return list

    def setBtnTabName(self, btnName):
        if not btnName:
            return
        if self.widget:
            ASUtils.DispatchButtonEvent(getattr(self.widget.recallFriendPanel, btnName))
        else:
            self.selectTabBtnName = btnName

    def checkRedFlag(self):
        if not self.isBackInValidTime() or not self.enableRecall():
            return False
        p = BigWorld.player()
        myScore = p.friendRecallStatics.get('totalScore', 0)
        finishRewardScroreBonusIds = p.friendRecallStatics.get('finishRewardScroreBonusIds', [])
        getedRewards = len(finishRewardScroreBonusIds)
        frdData = FRD.data.get(SCD.data.get('friendRecallActivityId', gametypes.FRIEND_RECALL_ID), {})
        scoreMargins = frdData.get('scoreMargins', [])
        nextPoint = 0
        if getedRewards + 1 <= len(scoreMargins):
            nextPoint = scoreMargins[getedRewards]
        isRedPot = True if myScore and nextPoint and myScore >= nextPoint else False
        return isRedPot
