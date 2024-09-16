#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemSettingV2Proxy.o
import BigWorld
import events
import uiConst
import uiUtils
import gameglobal
import gamelog
import gametypes
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import sys_config_data as SCD

class SystemSettingV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemSettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SYSTEM_SETTING_V2, self.close)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SYSTEM_SETTING_V2:
            self.widget = widget
            self.initUI()

    def initUI(self):
        self.widget.continueGameBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.gameSettingbtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.leavePointBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.gotoLoginBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.websiteBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.quitGameBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)

    def handleBtnClick(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        if targetBtn.name == 'continueGameBtn':
            self.close()
        elif targetBtn.name == 'gameSettingbtn':
            gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_VIDEO)
        elif targetBtn.name == 'leavePointBtn':
            self.close()
            BigWorld.player().fangKaDian()
        elif targetBtn.name == 'gotoLoginBtn':
            gameglobal.rds.ui.returnLoginView()
        elif targetBtn.name == 'websiteBtn':
            BigWorld.openUrl('https://revonline.ru/')
            self.close()
        elif targetBtn.name == 'quitGameBtn':
            uiUtils.onQuit()
        gameglobal.rds.sound.playSound(gameglobal.SD_6)

    def show(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_SYS_SETTING):
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SYSTEM_SETTING_V2)

    def close(self):
        self.hide(True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SYSTEM_SETTING_V2)

    def isShow(self):
        if self.widget:
            return True
        return False
