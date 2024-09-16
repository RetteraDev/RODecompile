#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/floatBallProxy.o
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
from data import quest_data as QD
from data import quest_loop_data as QLD
from cdata import quest_delegation_inverted_data as QDID

class FloatBallProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FloatBallProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handle = None
        self.reset()

    def reset(self):
        self.oldStageX = None
        self.oldStageY = None
        self.prevStageX = None
        self.prevStageY = None
        self.isMoving = False
        self.movingCallback = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FLOAT_BALL:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FLOAT_BALL)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FLOAT_BALL)

    def initUI(self):
        self.setFriendTipVisible(False)
        self.setMenuVisible(False)
        self.setTransparentBoxVisible(False)
        self.widget.mainMc.hpMask.minAngle = 180
        self.widget.mainMc.mpMask.minAngle = 180
        self.widget.mainMc.mpMask.scaleX = -1
        self.widget.mainMc.addEventListener(events.MOUSE_DOWN, self.handleMouseDown, False, 0, True)
        self.widget.mainMc.addEventListener(events.MOUSE_UP, self.handleMouseUp, False, 0, True)
        self.widget.mainMc.addEventListener(events.MOUSE_UP, self.onMainMcClick, False, 0, True)
        self.widget.transparentBox.tranparentBar.value = 100
        self.widget.transparentBox.tranparentBar.addEventListener(events.EVENT_VALUE_CHANGE, self.handleMoveSlider, False, 0, True)
        self.refreshUI()

    def showFriendTip(self, value = True):
        if self.widget:
            self.widget.friendTip.visible = value

    def handleMouseDown(self, *args):
        self.startMoveWindow()

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
            self.movingCallback = BigWorld.callback(0.05, self.realMoveWindow)
            return

    def startMoveWindow(self):
        if not self.widget:
            return
        self.oldStageX = self.widget.stage.mouseX
        self.oldStageY = self.widget.stage.mouseY
        self.isMoving = True
        self.realMoveWindow()

    def stopMoveWindow(self):
        self.isMoving = False
        if self.movingCallback:
            BigWorld.cancelCallback(self.movingCallback)
            self.movingCallback = None
        self.oldStageX = None
        self.oldStageY = None

    def onMainMcClick(self, *args):
        e = asObject.ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.setMenuVisible(True)

    def _onMenuBtn0Click(self, *args):
        self.setMenuVisible(False)
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)

    def _onMenuBtn1Click(self, *args):
        self.setMenuVisible(False)
        p = BigWorld.player()
        p.setWindowStyle(gameglobal.WINDOW_STYLE_CHAT)

    def _onMenuBtn2Click(self, *args):
        self.setMenuVisible(False)
        self.setTransparentBoxVisible(True)

    def _onMenuBtn3Click(self, *args):
        self.setMenuVisible(False)

    def _onCloseBtnClick(self, *args):
        self.setTransparentBoxVisible(False)

    @ui.uiEvent(uiConst.WIDGET_FLOAT_BALL, events.EVENT_HP_CHANGE)
    def setHp(self):
        self.showHp()

    def setMhp(self):
        self.showHp()

    def showHp(self):
        p = BigWorld.player()
        percent = 1.0 * p.hp / p.mhp
        if self.widget:
            self.widget.mainMc.hpMask.percent = percent

    @ui.uiEvent(uiConst.WIDGET_FLOAT_BALL, events.EVENT_MP_CHANGE)
    def setMp(self):
        self.showMp()

    def setMmp(self):
        self.showMp()

    def showMp(self):
        p = BigWorld.player()
        percent = 1.0 * p.mp / p.mmp
        if self.widget:
            self.widget.mainMc.mpMask.percent = percent

    @ui.uiEvent(uiConst.WIDGET_FLOAT_BALL, events.EVENT_AUTO_QUEST_CHANGE)
    def updateAutoQuest(self):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            questName = -1
            questDesc = gameStrings.PLAYER_DEAD
        elif p.checkInAutoQuest():
            info = gameglobal.rds.ui.questTrack.simpleFindPosInfo
            questId = info.get('questId', 0)
            questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
            questName = QD.data.get(questId, {}).get('name', '')
            questDesc = ''
            maxLoop = QLD.data.get(questLoopId, {}).get('groupNum', 0)
            hideLoopCnt = QLD.data.get(questLoopId, {}).get('hideLoopCnt', 0)
            info = p.questLoopInfo.get(questLoopId, None)
            isDelegetion = QDID.data.has_key(questLoopId)
            if info:
                if info.getCurrentQuest():
                    curLoop = info.getCurrentStep() + 1
                else:
                    curLoop = info.getCurrentStep()
                if isDelegetion:
                    questDesc = '%d/%d' % (curLoop, maxLoop)
                elif hideLoopCnt:
                    questDesc = '%d/%d' % (curLoop, maxLoop)
        else:
            questName = -1
            questDesc = gameStrings.AUTO_QUEST_STOP
        if self.widget:
            if questName != -1:
                self.widget.mainMc.questName.text = questName
            self.widget.mainMc.questDesc.text = questDesc

    def refreshUI(self):
        self.showHp()
        self.showMp()
        self.updateAutoQuest()

    def setFriendTipVisible(self, value):
        if self.widget:
            self.widget.friendTip.visible = value

    def setMenuVisible(self, value):
        if self.widget:
            self.widget.menu.visible = value

    def setTransparentBoxVisible(self, value):
        if self.widget:
            self.widget.transparentBox.visible = value

    def handleMoveSlider(self, *args):
        e = asObject.ASObject(args[3][0])
        value = e.target.value
        self.widget.transparentBox.textDesc.text = gameStrings.TRANSPARENT_SLIDER_DESC % e.target.value
        self.widget.alpha = value * 0.01

    def handleMoveSlider(self, *args):
        e = asObject.ASObject(args[3][0])
        value = e.target.value
        self.widget.transparentBox.textDesc.text = gameStrings.TRANSPARENT_SLIDER_DESC % e.target.value
        self.widget.alpha = value * 0.01
