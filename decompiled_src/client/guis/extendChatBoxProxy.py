#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/extendChatBoxProxy.o
import BigWorld
import gameglobal
import uiConst
import commQuest
import gametypes
from guis import asObject
from guis import events
from guis import ui
from uiProxy import UIProxy
from gamestrings import gameStrings
from callbackHelper import Functor

class ExtendChatBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExtendChatBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handle = None
        self.questData = None
        self.addEvent(events.EVENT_AUTO_QUEST_CHANGE, self.updateAutoQuest, isGlobal=True)
        self.addEvent(events.EVENT_AUTO_QUEST_START, self.updateAutoQuest, isGlobal=True)
        self.addEvent(events.EVENT_AUTO_QUEST_STOP, self.updateAutoQuest, isGlobal=True)
        self.reset()

    def reset(self):
        self.oldStageX = None
        self.oldStageY = None
        self.prevStageX = None
        self.prevStageY = None
        self.isMoving = False
        self.movingCallback = None
        self.isDebugMode = False
        self.hpMask = None
        self.mpMask = None
        self.isAddPushMessage = False
        self.isAddChatLog = False
        self.questItemHeight = 0
        self.chatLogMc = None
        self.pushMsgMc = None
        self.chatLogMcSize = []
        if hasattr(BigWorld, 'setWindowAlpha'):
            BigWorld.setWindowAlpha(255)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EXTEND_CHAT_BOX:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.removePushMessage()
        self.removeChatLog()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EXTEND_CHAT_BOX)

    def show(self, isDebug = False):
        self.isDebugMode = isDebug
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_EXTEND_CHAT_BOX)

    def initUI(self):
        self.setTransparentBoxVisible(False)
        self.hpMask = self.widget.questBall.hpMask
        self.mpMask = self.widget.questBall.mpMask
        self.hpMask.minAngle = 180
        self.mpMask.minAngle = 180
        self.mpMask.scaleX = -1
        self.widget.transparentBox.tranparentBar.minimum = 51
        self.widget.transparentBox.tranparentBar.maximum = 255
        self.widget.transparentBox.tranparentBar.value = 255
        self.widget.transparentBox.tranparentBar.addEventListener(events.EVENT_VALUE_CHANGE, self.handleMoveSlider, False, 0, True)
        self.widget.addEventListener(events.EVENT_RESIZE, self.onResize, False, 0, True)
        asObject.TipManager.addTipByFunc(self.widget.questBall, self.showQuestBallTip, self.widget.questBall, False)
        self.showFriendTip(False)
        self.refreshUI()

    def showQuestBallTip(self, *args):
        targetMc = asObject.ASObject(args[3][0])
        p = BigWorld.player()
        tipMc = asObject.TipManager.getInstance().getDefaultTipMc('HP:%d MP:%d' % (p.hp, p.mp))
        asObject.TipManager.showImediateTip(targetMc, tipMc)

    def showFriendTip(self, value = True):
        if self.widget:
            self.widget.msgArea.redIcon.visible = value
        if value:
            self.flashWindow()

    def handleMouseDown(self, *args):
        self.startMoveWindow()

    def handleMouseRollOut(self, *args):
        self.stopMoveWindow()

    def handleMouseUp(self, *args):
        self.stopMoveWindow()

    def realMoveWindow(self):
        if not self.isMoving:
            return
        elif not self.widget:
            return
        else:
            if self.movingCallback:
                BigWorld.cancelCallback(self.movingCallback)
                self.movingCallback = None
            mouseX = self.widget.stage.mouseX
            mouseY = self.widget.stage.mouseY
            if self.prevStageX != mouseX or self.prevStageY != mouseY:
                if hasattr(BigWorld, 'moveWindow'):
                    BigWorld.moveWindow(mouseX - self.oldStageX, mouseY - self.oldStageY, 0, 0, True)
            self.prevStageX = mouseX
            self.prevStageY = mouseY
            self.movingCallback = BigWorld.callback(0.03, self.realMoveWindow)
            return

    def startMoveWindow(self):
        if not self.widget:
            return
        self.isMoving = True
        self.oldStageX = self.widget.stage.mouseX
        self.oldStageY = self.widget.stage.mouseY
        self.realMoveWindow()

    def stopMoveWindow(self):
        self.isMoving = False
        if self.movingCallback:
            BigWorld.cancelCallback(self.movingCallback)
            self.movingCallback = None
        self.oldStageX = None
        self.oldStageY = None

    def _onMenuBtnClick(self, *args):
        self.setTransparentBoxVisible(True)

    def _onFriendTipClick(self, *args):
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)
        friendListLen = len(gameglobal.rds.ui.friendFlowBack.friendList)
        if BigWorld.player().handleFriendMsg(0, 0) or friendListLen != 0:
            if friendListLen:
                gameglobal.rds.ui.friendFlowBack.show()
        elif gameglobal.rds.ui.friend.isShow:
            gameglobal.rds.ui.friend.hide(False)
        else:
            gameglobal.rds.ui.friend.show()

    def _onMinBtnClick(self, *args):
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_FLOAT_BALL)

    def _onCloseBtnClick(self, *args):
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)

    def _onGoBackGameBtnClick(self, *args):
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)

    def _onBarCloseBtnClick(self, *args):
        self.setTransparentBoxVisible(False)

    @ui.uiEvent(uiConst.WIDGET_EXTEND_CHAT_BOX, events.EVENT_HP_CHANGE)
    def setHp(self):
        self.showHp()
        p = BigWorld.player()
        if p.hp == 0:
            self.updateQuestState()
            if self.widget:
                self.flashWindow()

    def setMhp(self):
        self.showHp()

    def showHp(self):
        p = BigWorld.player()
        percent = 1.0 * p.hp / p.mhp
        if self.widget:
            self.hpMask.percent = percent

    @ui.uiEvent(uiConst.WIDGET_EXTEND_CHAT_BOX, events.EVENT_MP_CHANGE)
    def setMp(self):
        self.showMp()

    def setMmp(self):
        self.showMp()

    def showMp(self):
        p = BigWorld.player()
        percent = 1.0 * p.mp / p.mmp
        if self.widget:
            self.mpMask.percent = percent

    def updateAutoQuest(self, event = None):
        self.updateQuestState()
        oldQuestData = self.questData
        if event and event.data:
            self.questData = event.data
        if oldQuestData == self.questData:
            return
        self.updateQuestDesc(self.questData)

    def updateAutoQuestFromUI(self):
        self.updateQuestState()
        self.updateQuestDesc(self.questData)

    def refreshUI(self):
        self.showHp()
        self.showMp()
        self.addPushMesage()
        self.addChatLog()
        self.updateAutoQuestFromUI()

    def setTransparentBoxVisible(self, value):
        if self.widget:
            self.widget.transparentBox.visible = value

    def updateQuestState(self):
        if not self.widget:
            return
        p = BigWorld.player()
        questDesc = ''
        questState = 'meiyou'
        if p.life == gametypes.LIFE_DEAD:
            questDesc = gameStrings.PLAYER_DEAD
            questState = 'zhenwang'
        elif p.checkInAutoQuest():
            questDesc = gameStrings.AUTO_QUEST_GOING
            questState = 'jinxing'
        else:
            questDesc = gameStrings.AUTO_QUEST_STOP
            questState = 'zanting'
            self.flashWindow()
        if questDesc != self.widget.stateDesc.text:
            self.widget.stateDesc.text = questDesc
        if questState != self.widget.questBall.state.currentLabel:
            self.widget.questBall.state.gotoAndStop(questState)
            self.widget.questDesc.questName.state.gotoAndStop(questState)

    def updateQuestDesc(self, data = None):
        if not self.widget:
            return
        else:
            questDesc = self.widget.questDesc
            questDesc.questName.icon.visible = False
            if not data:
                return
            goalList = data.get('goalList', [])
            questName = data.get('questName', '')
            questDesc.questName.nameDesc.text = questName
            content = questDesc.content
            self.widget.removeAllInst(content)
            y = 0
            for i, item in enumerate(goalList):
                mc = self.widget.getInstByClsName('ExtendChatBox_QuestItem')
                if not item[1]:
                    mc.gotoAndStop('up')
                    mc.state.visible = False
                else:
                    mc.gotoAndStop('disable')
                    mc.state.visible = True
                mc.desc.text = item[0]
                content.addChild(mc)
                mc.y = y
                y += mc.height

            self.questItemHeight = y + 10
            self.onResize(None)
            return

    def addPushMesage(self):
        if self.isAddPushMessage:
            return
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PUSH_MESSSAGES)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXTEND_PUSH_MESSSAGES)
        self.isAddPushMessage = True

    def removePushMessage(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXTEND_PUSH_MESSSAGES)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PUSH_MESSSAGES)
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_FLOAT_BALL:
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_PUSH_MESSSAGES, False)
        self.isAddPushMessage = False

    def addChatLog(self):
        if self.isAddChatLog:
            return
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHAT_LOG)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXTEND_CHAT_LOG)
        self.isAddChatLog = True

    def removeChatLog(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXTEND_CHAT_LOG)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHAT_LOG)
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_FLOAT_BALL:
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_CHAT_LOG, False)
        self.isAddChatLog = False

    def handleMoveSlider(self, *args):
        e = asObject.ASObject(args[3][0])
        value = e.target.value
        self.widget.transparentBox.textDesc.text = gameStrings.TRANSPARENT_SLIDER_DESC % int(e.target.value / 2.55)
        if hasattr(BigWorld, 'setWindowAlpha'):
            BigWorld.setWindowAlpha(value)

    def onResize(self, *args):
        if not self.widget:
            return
        stage = self.widget.stage
        self.widget.x = 0
        self.widget.y = 0
        stageWidth = stage.stageWidth
        stageHeight = stage.stageHeight
        if not self.isDebugMode:
            self.widget.questBg.width = stageWidth
            self.widget.questBg.height = 30 + self.questItemHeight
            self.widget.dashLine1.height = 26 + self.questItemHeight
            self.widget.questBg1.width = stageWidth
            self.widget.dashLine.width = stageWidth
            self.widget.allBg.width = stageWidth
            self.widget.allBg.height = stageHeight
            self.widget.msgArea.y = self.widget.questBg.y + self.widget.questBg.height + 10
            self.widget.goBackGameBtn.x = stageWidth - self.widget.goBackGameBtn.width - 10
        self.onResizePushMsg()
        self.onResizeChatLog()

    def registerPushMsg(self, mediator):
        mediatorAsObject = asObject.ASObject(mediator)
        self.pushMsgMc = mediatorAsObject.getWidget()
        BigWorld.callback(0.2, self.onResizePushMsg)

    def regisiterChatLog(self, mc):
        self.chatLogMc = asObject.ASObject(mc)
        self.chatLogMc.drawBtn.visible = False
        self.chatLogMc.reduceBtn.visible = False
        self.chatLogMc.chatLogManageBtn.visible = False
        if self.chatLogMc.alphaBtn:
            self.chatLogMc.alphaBtn.addEventListener(events.MOUSE_DOWN, self.handleClickAlphaBtn, False, 0, True)
        gameglobal.rds.ui.chat.hideWorldExMessage()
        self.chatLogMcSize = [self.chatLogMc.width,
         self.chatLogMc.height,
         self.chatLogMc.bg.width,
         self.chatLogMc.bg.height]
        BigWorld.callback(0.1, self.onResizeChatLog)

    def handleClickAlphaBtn(self, *args):
        if self.widget:
            if self.widget.transparentBox.visible:
                self.setTransparentBoxVisible(False)
            else:
                self.setTransparentBoxVisible(True)

    def onResizeChatLog(self):
        if not self.chatLogMc:
            return
        stage = self.widget.stage
        stageWidth = stage.stageWidth
        stageHeight = stage.stageHeight
        self.chatLogMc.validateNow()
        height = stageHeight - self.widget.questBg1.height - self.widget.questBg.height - self.widget.msgArea.height
        deltaHeight = height - self.chatLogMcSize[3] - 60
        deltaWidth = stageWidth - self.chatLogMcSize[2] + 80
        self.chatLogMc.setChatSize(self.chatLogMcSize[0] + deltaWidth, self.chatLogMcSize[1] + deltaHeight)
        self.chatLogMc.bg.width = stageWidth - 30
        self.chatLogMc.chatLogArea.width = stageWidth - 30
        self.chatLogMc.chatLogArea.refreshText()

    def onResizePushMsg(self):
        if not self.pushMsgMc:
            return
        self.pushMsgMc.x = 45 + self.widget.msgArea.x
        self.pushMsgMc.y = 4 + self.widget.msgArea.y

    def flashWindow(self):
        BigWorld.flashWindow(2)
