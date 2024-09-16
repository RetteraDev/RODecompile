#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hideModeSettingProxy.o
import BigWorld
import uiConst
import uiUtils
import gameglobal
import keys
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
HIDE_MODE_PRE_NUM = 5

class HideModeSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HideModeSettingProxy, self).__init__(uiAdapter)
        self.nowtick = 0
        self.lefttick = 0
        self.Mode = uiConst.MODE_Inactive
        self.modelMap = {'getModeData': self.onGetModeData,
         'saveModeData': self.onSaveModeData,
         'close': self.onClose}
        uiAdapter.registerEscFunc(uiConst.WIDGET_HIDEMODE_SETTING, self.hide)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def onGetModeData(self, *arg):
        setting = self.getHideModeSetting()
        return uiUtils.array2GfxAarry(setting)

    def onSaveModeData(self, *arg):
        setstr = arg[3][0].GetString()
        self.saveHideModeSetting(setstr)

    def onClose(self, *arg):
        self.hide()

    def saveHideModeSetting(self, setstr):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.HIDE_MODE_SAVE, ())
        curSetting = AppSettings.get(keys.SET_HIDEMODE_OPTION, '')
        if curSetting != setstr:
            AppSettings[keys.SET_HIDEMODE_OPTION] = setstr
            AppSettings.save()
            p.refreshCurrMode()

    def getHideModeSetting(self):
        settingStr = AppSettings.get(keys.SET_HIDEMODE_OPTION, '')
        if settingStr:
            ret = []
            for i in settingStr.split('@'):
                l = [ int(j) for j in i.split(',') ]
                if len(l) == HIDE_MODE_PRE_NUM:
                    l.extend([0, 0])
                ret.append(l)

            return ret
        return SCD.data.get('DEFAULT_HIDE_MODE', [(0, 1, 0, 0, 1, 0, 0), (0, 1, 1, 0, 1, 0, 0), (0, 0, 0, 0, 0, 0, 0)])

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HIDEMODE_SETTING)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HIDEMODE_SETTING)
