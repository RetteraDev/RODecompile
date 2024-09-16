#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/loadingProxy.o
from Scaleform import GfxValue
import gameglobal
import uiUtils
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy

class LoadingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LoadingProxy, self).__init__(uiAdapter)
        self.modelMap = {'register': self.onRegister,
         'getText': self.onGetText,
         'getFirstPic': self.onGetFirstPic,
         'getMode': self.onGetMode}
        self.mc = None
        self.text = ''
        self.pic1Path = ''
        self.pic2Path = ''
        self.mode = 'normal'

    def onRegister(self, *args):
        self.mc = args[3][0]
        if self.mode == 'normal':
            self.play()

    def setProgress(self, num):
        if self.mc:
            self.mc.Invoke('setProgress', GfxValue(num))

    def setText(self, txt):
        self.text = txt

    def onGetMode(self, *args):
        return GfxValue(self.mode)

    def onGetText(self, *args):
        return GfxValue(gbk2unicode(self.text))

    def fadeTo(self, path, dynamicPath, time):
        if not self.mc:
            return
        newPath = dynamicPath if dynamicPath else path
        if newPath == self.pic2Path:
            return
        self.pic2Path = newPath
        self.mc.Invoke('fadeTo', (GfxValue(self.pic2Path), GfxValue(time)))

    def setMode(self, mode):
        self.mode = mode

    def setFirstPic(self, picPath):
        self.pic1Path = picPath

    def onGetFirstPic(self, *args):
        return GfxValue(self.pic1Path)

    def reset(self):
        self.mc = None
        self.text = ''
        self.pic1Path = ''
        self.pic2Path = ''
        self.mode = 'normal'

    def show(self, isShow):
        if isShow:
            if gameglobal.rds.configData.get('enableChatTopWhenLoading', False):
                gameglobal.rds.ui.setTempWeight(uiConst.WIDGET_CHAT_LOG, uiConst.TOP_WIDGET_WEIGHT)
                gameglobal.rds.ui.setWidgetLevel(uiConst.WIDGET_CHAT_LOG, -1)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LOADING)
        else:
            self.reset()
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOADING)
            if gameglobal.rds.configData.get('enableChatTopWhenLoading', False):
                gameglobal.rds.ui.setTempWeight(uiConst.WIDGET_CHAT_LOG, -1)

    def play(self):
        if self.mc:
            self.mc.Invoke('show')
