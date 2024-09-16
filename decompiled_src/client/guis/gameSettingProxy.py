#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gameSettingProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiTabProxy import UITabProxy

class GameSettingProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(GameSettingProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GAME_SETTING_BG_V2, self.hide)

    def show(self, showTabIndex = uiConst.GAME_SETTING_BG_V2_TAB_VIDEO):
        self.showTabIndex = showTabIndex
        if self.widget:
            self.widget.swapPanelToFront()
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GAME_SETTING_BG_V2)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GAME_SETTING_BG_V2:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def _getTabList(self):
        return [{'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_VIDEO,
          'tabName': 'tabBtn1',
          'view': 'VideoSettingWidget',
          'proxy': 'videoSetting'},
         {'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_SURFACE,
          'tabName': 'tabBtn2',
          'view': 'SurfaceSettingV2Widget',
          'proxy': 'surfaceSettingV2'},
         {'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_SOUND,
          'tabName': 'tabBtn3',
          'view': 'SoundSettingV2Widget',
          'proxy': 'soundSettingV2'},
         {'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_PERSONAL,
          'tabName': 'tabBtn4',
          'view': 'PersonalSettingV2Widget',
          'proxy': 'personalSettingV2'},
         {'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_CONTROL,
          'tabName': 'tabBtn5',
          'view': 'ControlSettingv2Widget',
          'proxy': 'controlSettingV2'},
         {'tabIdx': uiConst.GAME_SETTING_BG_V2_TAB_KEY,
          'tabName': 'tabBtn6',
          'view': 'KeySettingV2Widget',
          'proxy': 'keySettingV2'}]

    def initUI(self):
        self.initTabUI()
        if gameglobal.rds.ui.loginWin.mc:
            self.widget.tabBtn2.disabled = True
            self.widget.tabBtn3.disabled = True
            self.widget.tabBtn4.disabled = True
            self.widget.tabBtn5.disabled = True
            self.widget.tabBtn6.disabled = True
        self.widget.defaultCloseBtn = self.widget.cancleBtn

    def clearWidget(self):
        super(GameSettingProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GAME_SETTING_BG_V2)

    def reset(self):
        super(GameSettingProxy, self).reset()
