#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/notifyProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
from ui import gbk2unicode
from guis.uiProxy import UIProxy
from data import game_msg_data as GMD
notifyIconPath = 'notify/icon/'
iconSuffix = '.dds'

class NotifyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NotifyProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerSysNotify': self.onRegisterSysNotify}
        self.callbackHandler = None
        self.notify = None
        self.content = None
        self.mc = None

    def onRegisterSysNotify(self, *arg):
        gamelog.debug('onRegisterSysNotify')
        self.mc = arg[3][0]
        self.notify = self.mc.GetMember('notify')
        self.content = self.notify.GetMember('content')
        self.mc.SetVisible(False)
        self.visible = False

    def showSysNotifyDirect(self, str, color = None):
        if self.callbackHandler != None:
            BigWorld.cancelCallback(self.callbackHandler)
        self.showContent2(str, color)
        if self.mc != None:
            self.mc.SetVisible(True)
            self.callbackHandler = BigWorld.callback(5, self._goToEnd)

    def showSysNotify(self, sysId, argTuple = None):
        if self.callbackHandler != None:
            BigWorld.cancelCallback(self.callbackHandler)
        self.showContent(sysId, argTuple)
        if self.mc != None:
            self.mc.SetVisible(True)
            self.callbackHandler = BigWorld.callback(5, self._goToEnd)

    def showContent2(self, str, color = None):
        if self.content == None:
            return
        else:
            self._goToStart()
            if color != None:
                self.content.GotoAndPlay(color)
            data = self.movie.CreateObject()
            data.SetMember('text', GfxValue(gbk2unicode(str)))
            self.mc.Invoke('setInfo', data)
            return

    def showContent(self, sysId, argTuple = None):
        info = GMD.data.get(sysId, None)
        if info != None:
            color = info.get('color', 'white')
            icon = info.get('icon', 0)
            if argTuple != None:
                content = info['text'] % argTuple
            else:
                content = info['text']
            self._goToStart()
            self.content.GotoAndPlay(color)
            iconPath = self._getIconPath(icon)
            data = self.movie.CreateObject()
            data.SetMember('text', GfxValue(gbk2unicode(content)))
            data.SetMember('iconPath', GfxValue(iconPath))
            self.mc.Invoke('setInfo', data)

    def getContent(self, sysId, argTuple = None):
        info = GMD.data.get(sysId, None)
        if info != None:
            if argTuple != None:
                content = info['text'] % argTuple
            else:
                content = info['text']
        return content

    def _goToStart(self):
        if self.notify != None:
            self.notify.GotoAndPlay('start')

    def _goToEnd(self):
        if self.notify != None:
            self.notify.GotoAndPlay('end')

    def _getIconPath(self, id):
        gamelog.debug('_getIconPath', notifyIconPath + str(id) + iconSuffix)
        return notifyIconPath + str(id) + iconSuffix
