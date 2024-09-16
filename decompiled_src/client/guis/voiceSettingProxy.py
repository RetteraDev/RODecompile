#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voiceSettingProxy.o
import BigWorld
import events
import gameglobal
import const
import uiConst
from uiProxy import UIProxy
from asObject import ASObject
from helpers import ccManager
from cdata import game_msg_def_data as GMDD

class VoiceSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoiceSettingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.resetMode()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOICE_SETTING, self.hide)

    def resetMode(self):
        self.mode = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOICE_SETTING:
            self.widget = widget
            self.initUI()

    def initUI(self):
        self.selected = self.mode
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onClickConfirmBtn, False, 0, True)
        self.widget.setting.addEventListener(events.MOUSE_CLICK, self.handleClickSetting, False, 0, True)
        for i in xrange(3):
            mc = getattr(self.widget, 'mode%d' % i)
            mc.idx = i
            if i == self.mode:
                mc.selected.visible = True
                mc.radio.selected = True
            else:
                mc.selected.visible = False
                mc.radio.selected = False
            mc.addEventListener(events.MOUSE_CLICK, self.handleClickMc, False, 0, True)

    def handleClickMc(self, *args):
        idx = ASObject(args[3][0]).currentTarget.idx
        if idx == self.selected:
            return
        mc = getattr(self.widget, 'mode%d' % self.selected)
        mc.selected.visible = False
        mc.radio.selected = False
        mc = getattr(self.widget, 'mode%d' % idx)
        mc.selected.visible = True
        mc.radio.selected = True
        self.selected = idx

    def onClickCloseBtn(self, *args):
        self.hide()

    def onClickConfirmBtn(self, *args):
        if self.selected != self.mode:
            if ccManager.instance().startUp():
                self.mode = self.selected
                if self.mode == 0:
                    ccManager.instance().muteCapture(1, const.CC_SESSION_TEAM)
                    ccManager.instance().mutePlayBack(1, const.CC_SESSION_TEAM)
                elif self.mode == 1:
                    ccManager.instance().muteCapture(1, const.CC_SESSION_TEAM)
                    ccManager.instance().mutePlayBack(0, const.CC_SESSION_TEAM)
                elif self.mode == 2:
                    ccManager.instance().muteCapture(0, const.CC_SESSION_TEAM)
                    ccManager.instance().mutePlayBack(0, const.CC_SESSION_TEAM)
                p = BigWorld.player()
                p.base.changeCCMode(p.groupNUID, self.mode)
                gameglobal.rds.ui.teamComm.setSelfVoiceMode(self.mode)
            else:
                BigWorld.player().showGameMsg(GMDD.data.CC_TEAM_NO_START_UP, ())
        self.hide()

    def handleClickSetting(self, *args):
        gameglobal.rds.ui.soundSettingV2.setVoiceSetting()
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_SOUND)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOICE_SETTING)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOICE_SETTING)
