#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/baiDiShiLianPushProxy.o
import BigWorld
import uiConst
import events
import utils
import formula
import keys
import gamelog
import gameglobal
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.messageBoxProxy import MBButton
from uiProxy import UIProxy
ACTIVITY_PREPARE = 1
ACTIVITY_START = 2
ACTIVITY_END = 3
ACTIVITY_END_CLOSE = 4
PLAY_RECOMM_BAIDI_SHILIAN_ID = 10015
from data import sky_wing_challenge_config_data as SWCCD
from data import game_msg_data as GMD
from data import play_recomm_item_data as PRID
from cdata import game_msg_def_data as GMDD

class BaiDiShiLianPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BaiDiShiLianPushProxy, self).__init__(uiAdapter)
        self.timer = 0
        self.widget = None
        self.reset()

    def reset(self):
        self.activityState = 0

    def clearAll(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BAIDI_SHILIAN_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BAIDI_SHILIAN_PUSH)

    def show(self):
        if not gameglobal.rds.configData.get('enableSkyWingChallenge', False):
            return
        p = BigWorld.player()
        lvRange = PRID.data.get(PLAY_RECOMM_BAIDI_SHILIAN_ID, {}).get('lv', (0, 79))
        if p.lv < lvRange[0] or p.lv > lvRange[1]:
            return
        if not self.widget:
            self.timer = 0
            self.uiAdapter.loadWidget(uiConst.WIDGET_BAIDI_SHILIAN_PUSH)

    def initUI(self):
        widget = self.widget
        ASUtils.setHitTestDisable(widget.hintEff, True)
        ASUtils.setHitTestDisable(widget.pushIcon.touMing, True)
        widget.hintEff.visible = False
        widget.pushIcon.tipsText.gotoAndPlay('off')
        widget.pushIcon.tipsText.textMc.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseTipClick, False, 0, True)
        widget.pushIcon.expandBtn.addEventListener(events.MOUSE_CLICK, self.onExpandTipClick, False, 0, True)
        widget.pushIcon.icon.addEventListener(events.MOUSE_CLICK, self.onOpenBaiDiShiLian, False, 0, True)
        widget.pushIcon.endBtn.addEventListener(events.MOUSE_CLICK, self.onOpenBaiDiShiLian, False, 0, True)
        widget.pushIcon.prepareBtn.addEventListener(events.MOUSE_CLICK, self.onOpenBaiDiShiLian, False, 0, True)
        ASUtils.callbackAtFrame(widget.pushIcon, 10, self.setEffectHitTestEnable)

    def setEffectHitTestEnable(self, *args):
        if not self.widget or self.widget.pushIcon.bgEff:
            return
        ASUtils.setHitTestDisable(self.widget.pushIcon.bgEff, True)

    def onCloseTipClick(self, *args):
        widget = self.widget
        widget.pushIcon.tipsText.gotoAndPlay('off')
        widget.pushIcon.expandBtn.visible = True

    def onExpandTipClick(self, *args):
        widget = self.widget
        widget.pushIcon.tipsText.gotoAndPlay('on')
        widget.pushIcon.expandBtn.visible = False
        widget.pushIcon.tipsText.textMc.score.htmlText = self.getData()[2]

    def onOpenBaiDiShiLian(self, *args):
        widget = self.widget
        widget.hintEff.visible = False
        widget.hintEff.gotoAndStop(1)
        p = BigWorld.player()
        if self.getData()[0] == ACTIVITY_END:
            self.uiAdapter.baiDiShiLian.show()
        elif self.getData()[0] >= ACTIVITY_END_CLOSE:
            return
        if formula.inSkyWingFubenSpace(p.spaceNo):
            self.uiAdapter.baiDiShiLian.show()
        else:
            text = GMD.data.get(GMDD.data.SKY_WING_PUSH_CLICK, {}).get('text', '')
            buttons = [MBButton(gameStrings.BAIDI_SHILIAN_ENTER_FUBEN, p.cell.applySkyWingFuben, enable=True, fastKey=keys.KEY_Y), MBButton(gameStrings.BAIDI_SHILIAN_OPEN, self.uiAdapter.baiDiShiLian.show, fastKey=keys.KEY_N), MBButton(gameStrings.BAIDI_SHILIAN_CANCEL, fastKey=keys.KEY_ESCAPE)]
            self.uiAdapter.messageBox.show(True, '', text, buttons, style=0, textAlign='center', canEsc=True)

    def getData(self):
        state, timeStr, scoreStr = (0, 0, 0)
        now = utils.getNow()
        prepareTime, startTime, endTime = self.getTime()
        startTime += 3
        if self.uiAdapter.baiDiShiLian.startTime:
            startTime = self.uiAdapter.baiDiShiLian.startTime
            endTime = startTime + SWCCD.data.get('duration', 720)
        if now < startTime:
            state = ACTIVITY_PREPARE
            timeStr = utils.formatTimeStr(int(startTime - now), 'm:s', True, 2, 2)
        elif now < endTime:
            if not self.uiAdapter.baiDiShiLian.startTime:
                state = ACTIVITY_PREPARE
                timeStr = utils.formatTimeStr(0, 'm:s', True, 2, 2)
            else:
                state = ACTIVITY_START
                timeStr = utils.formatTimeStr(int(endTime - now), 'm:s', True, 2, 2)
        elif now < endTime + SWCCD.data.get('endDuration', 10):
            state = ACTIVITY_END
            timeStr = utils.formatTimeStr(0, 'm:s', True, 2, 2)
        else:
            state = ACTIVITY_END_CLOSE
        scoreStr = str(self.uiAdapter.baiDiShiLian.selfScore)
        return (state, timeStr, scoreStr)

    def refreshInfo(self):
        if not self.widget:
            return
        state, timeStr, scoreStr = self.getData()
        if state == ACTIVITY_END_CLOSE:
            self.hide()
            return
        widget = self.widget
        if state != self.activityState and state == ACTIVITY_START:
            widget.hintEff.visible = True
            widget.hintEff.gotoAndPlay(1)
        self.activityState = state
        widget.pushIcon.countdown.visible = self.activityState == ACTIVITY_START or self.activityState == ACTIVITY_PREPARE
        widget.pushIcon.endBtn.visible = self.activityState == ACTIVITY_END
        widget.pushIcon.icon.visible = self.activityState == ACTIVITY_START
        widget.pushIcon.prepareBtn.visible = self.activityState == ACTIVITY_PREPARE
        widget.pushIcon.tipsText.textMc.score.htmlText = scoreStr
        widget.pushIcon.countdown.textField.text = timeStr
        BigWorld.callback(0.3, self.refreshInfo)

    def getTime(self):
        startTime = utils.getNextCrontabTime(SWCCD.data.get('startCrontab'))
        if not utils.isSameWeek(startTime, utils.getNow()):
            startTime = utils.getPreCrontabTime(SWCCD.data.get('startCrontab'))
        endTime = startTime + SWCCD.data.get('duration', 720)
        prepareTime = startTime - SWCCD.data.get('prepareTime', 10)
        return (prepareTime, startTime, endTime)

    def tryStartTimer(self):
        prepareTime, startTime, endTime = self.getTime()
        now = utils.getNow()
        p = BigWorld.player()
        lvRange = PRID.data.get(PLAY_RECOMM_BAIDI_SHILIAN_ID, {}).get('lv', (0, 79))
        if p.lv < lvRange[0] or p.lv > lvRange[1]:
            return
        if utils.isSameDay(prepareTime, now):
            if now < prepareTime:
                if self.timer:
                    BigWorld.cancelCallback(self.timer)
                    self.timer = 0
                self.timer = BigWorld.callback(prepareTime - now, self.show)
            elif now > endTime + SWCCD.data.get('endDuration', 10):
                self.hide()
            else:
                self.show()
