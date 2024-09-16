#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingCombatPushProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import utils
import const
import gamelog
import gametypes
from callbackHelper import Functor
from uiProxy import UIProxy
from guis.asObject import ASUtils
from helpers import tickManager
from data import sys_config_data as SCD
from crontab import CronTab
from data import wing_world_config_data as WWCD
import wingWorldUtils

class WingCombatPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingCombatPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tickId = None
        self.timer = 0
        self.endTime = utils.getNow()
        self.isExpand = False
        self.reset()
        self.wingWorldStepRefreshed = False
        self.activityState = const.WING_WORLD_XINMO_STATE_CLOSE
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_PUSH, self.hide)

    def reset(self):
        pass

    def clearAll(self):
        self.wingWorldStepRefreshed = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_PUSH)
        if self.tickId:
            tickManager.stopTick(self.tickId)
            self.tickId = None

    def show(self, state, startTime = None):
        if not gameglobal.rds.configData.get('enableWingWorldXinMo', False):
            return
        if not wingWorldUtils.isOpenWingWorld():
            return
        if self.wingWorldStepRefreshed:
            p = BigWorld.player()
            if p.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_CLOSE or p.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_ADJOURNING:
                return
        if state == const.WING_WORLD_XINMO_STATE_CLOSE:
            self.clearWidget()
            return
        if state == const.WING_WORLD_XINMO_STATE_ARENA:
            gameglobal.rds.ui.wingStageChoose.currChoose = {}
        if startTime:
            self.endTime = startTime
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = 0
        self.activityState = state
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_PUSH)

    def initUI(self):
        widget = self.widget
        ASUtils.setHitTestDisable(widget.hintEff, True)
        widget.pushIcon.tipsText.gotoAndPlay('off')
        widget.pushIcon.tipsText.textMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseTipClick, False, 0, True)
        widget.pushIcon.prepareBtn.addEventListener(events.BUTTON_CLICK, self.onPrepareBtnClick, False, 0, True)
        widget.pushIcon.expandBtn.addEventListener(events.BUTTON_CLICK, self.onExpandTipClick, False, 0, True)
        widget.pushIcon.zhiGaoBtn.addEventListener(events.MOUSE_CLICK, self.onZhiGaoBtnClick, False, 0, True)
        widget.pushIcon.zhiQiangBtn.addEventListener(events.MOUSE_CLICK, self.onZhiQiangBtnClick, False, 0, True)
        widget.pushIcon.yuHuangBtn.addEventListener(events.MOUSE_CLICK, self.onYuHuangBtnClick, False, 0, True)
        widget.pushIcon.preEndBtn.addEventListener(events.MOUSE_CLICK, self.onPreEndBtnClick, False, 0, True)
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshInfo)

    def onZhiGaoBtnClick(self, *args):
        gameglobal.rds.ui.zhiQiangDuiJue.hide()
        gameglobal.rds.ui.zhiQiangDuiJue.show(1)

    def onZhiQiangBtnClick(self, *args):
        gameglobal.rds.ui.zhiQiangDuiJue.showFromPushWidget()

    def onYuHuangBtnClick(self, *args):
        gameglobal.rds.ui.yuHuang.show(self.activityState, self.endTime)

    def onPrepareBtnClick(self, *args):
        gameglobal.rds.ui.yuHuang.show(self.activityState, self.endTime)

    def onPreEndBtnClick(self, *args):
        gameglobal.rds.ui.yuHuang.show(self.activityState, self.endTime)

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def onCloseTipClick(self, *args):
        widget = self.widget
        self.isExpand = False
        widget.pushIcon.tipsText.gotoAndPlay('off')
        widget.pushIcon.expandBtn.visible = True

    def onExpandTipClick(self, *args):
        widget = self.widget
        self.isExpand = True
        widget.pushIcon.tipsText.gotoAndPlay('on')
        widget.pushIcon.expandBtn.visible = False
        widget.pushIcon.tipsText.textMc.htmltext.text = WWCD.data.get('wingWorldXinMoArenaPrepareTip', gameStrings.TEXT_WINGCOMBATPUSHPROXY_130)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.wingWorldStepRefreshed:
            p = BigWorld.player()
            if p.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_CLOSE:
                self.clearWidget()
                return
        widget = self.widget
        widget.pushIcon.expandBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE and not self.isExpand
        widget.pushIcon.tipsText.visible = self.activityState == const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE
        widget.pushIcon.prepareBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE or self.activityState == const.WING_WORLD_XINMO_STATE_ENTER_ML
        widget.pushIcon.zhiQiangBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_ARENA
        widget.pushIcon.zhiGaoBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS
        widget.pushIcon.yuHuangBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_NORMAL_BOSS
        widget.pushIcon.preEndBtn.visible = self.activityState == const.WING_WORLD_XINMO_STATE_PRE_END
        leftTime = self.endTime - utils.getNow()
        if leftTime < 0:
            leftTime = 0
            if self.activityState == const.WING_WORLD_XINMO_STATE_PRE_END:
                self.clearWidget()
                self.activityState = const.WING_WORLD_XINMO_STATE_CLOSE
                return
        if self.activityState == const.WING_WORLD_XINMO_STATE_ARENA:
            widget.pushIcon.countdown.visible = False
        else:
            widget.pushIcon.countdown.visible = True
            widget.pushIcon.countdown.textField.text = self.formateTime(leftTime)

    def onWingWorldStepChange(self):
        self.wingWorldStepRefreshed = True
        self.refreshInfo()

    def tryStartTimer(self):
        if not wingWorldUtils.isOpenWingWorld():
            return
        else:
            now = utils.getNow()
            startTimeCrontabStr = WWCD.data.get('xinmoStartCrontab', None)
            prepareTime = WWCD.data.get('xinmoPrepareTime', 1200)
            if not startTimeCrontabStr:
                return
            startTime = utils.getNextCrontabTime(startTimeCrontabStr)
            startTime += 3
            deltaTime = startTime - now
            gamelog.debug('dxk @wingCombatPushProxy [deltaTime]', deltaTime)
            if self.timer:
                BigWorld.cancelCallback(self.timer)
                self.timer = 0
            if utils.isSameWeek(startTime, now):
                if deltaTime < 0:
                    pass
                elif deltaTime > prepareTime:
                    self.timer = BigWorld.callback(deltaTime - prepareTime, Functor(gameglobal.rds.ui.wingCombatPush.show, const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE, startTime))
                elif self.widget:
                    pass
                else:
                    gameglobal.rds.ui.wingCombatPush.show(const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE, startTime)
            return
