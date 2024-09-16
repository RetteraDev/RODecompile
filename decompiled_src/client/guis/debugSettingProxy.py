#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/debugSettingProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import uiConst
import appSetting
import gameglobal
import gamelog
from uiProxy import UIProxy
from ui import gbk2unicode
from appSetting import Obj as AppSettings

class DebugSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DebugSettingProxy, self).__init__(uiAdapter)
        self.modelMap = {'onConfirm': self.onConfirm,
         'onCancel': self.onCancel,
         'getDebugConfig': self.onGetDebugConfig,
         'getDebugContent': self.onGetDebugContent,
         'debugClick': self.onDebugClick}
        self.debugFuncList = [[gameStrings.TEXT_DEBUGSETTINGPROXY_25, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_25_1, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_25_2, None],
         ['Sea', None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_26, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27_1, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27_2, None]]
        self.mapFunc = {'debug': (self.debugConfirm, self.debugCancel)}
        uiAdapter.registerEscFunc(uiConst.WIDGET_DEBUG_SETTING, self.close)
        self.destroyOnHide = True
        self.mediator = None

    def _getAllData(self, *arg):
        tag = arg[3][0].GetString()
        array = arg[3][1].GetString().split(',')
        array = [ int(x) for x in array ]
        if tag == 'video':
            if array[2] == 0:
                array[0], array[1] = BigWorld.getScreenSize()
        return (tag, array)

    def onConfirm(self, *arg):
        tag, data = self._getAllData(*arg)
        gamelog.debug('bgf:onConfirm', tag, data)
        self.mapFunc[tag][0](data)
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onCancel(self, *arg):
        tag, data = self._getAllData(*arg)
        gamelog.debug('bgf:onCancel', tag, data)
        self.mapFunc[tag][1](data)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def onGetDebugConfig(self, *arg):
        arr = self.movie.CreateArray()
        i = 0
        for item in appSetting.DebugSettingObj._value:
            arr.SetElement(i, GfxValue(item))
            i += 1

        return arr

    def onDebugClick(self, *arg):
        index = int(arg[3][0].GetString())
        selected = arg[3][1].GetBool()
        gamelog.debug('debug wy:', index, selected)

    def onGetDebugContent(self, *arg):
        arr = self.movie.CreateArray()
        if self.debugFuncList == None:
            return arr
        else:
            i = 0
            for item in self.debugFuncList:
                arr.SetElement(i, GfxValue(gbk2unicode(item[0])))
                i += 1

            gamelog.debug('onGetDebugContent', i)
            return arr

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_DEBUG_SETTING)

    def close(self):
        self.hide(True)

    def debugConfirm(self, data):
        appSetting.DebugSettingObj.apply(data)
        appSetting.DebugSettingObj._value = data
        self.hide(True)

    def debugCancel(self, data):
        self.hide(True)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DEBUG_SETTING)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DEBUG_SETTING:
            self.mediator = mediator
