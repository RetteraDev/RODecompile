#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/imeProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import ime

class ImeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ImeProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickCandidate': self.onClickCandidate,
         'registerIme': self.onRegisterIme}
        self.mc = None
        self.comp = None
        self.candidate = None

    def onRegisterIme(self, *arg):
        self.mc = arg[3][0]

    def setCandidate(self, comp, candidate):
        if comp == self.comp and candidate == self.candidate:
            return
        if self.mc:
            self.mc.Invoke('setCandidate', (GfxValue(gbk2unicode(comp)), uiUtils.array2GfxAarry(candidate, True)))
            self.comp = comp
            self.candidate = candidate

    def showIme(self):
        self.uiAdapter.showIme(True)

    def hideIme(self):
        self.uiAdapter.showIme(False)

    def hideMenu(self, beHide):
        if self.mc:
            self.mc.Invoke('hide', GfxValue(beHide))

    def setQuanJiao(self, beQuanJiao):
        if self.mc:
            self.mc.Invoke('setQuanJiao', GfxValue(beQuanJiao))

    def setLanguage(self, beChinese):
        if self.mc:
            self.mc.Invoke('setLanguage', GfxValue(beChinese))

    def enableIme(self):
        ime.onRecreateDevice()

    def onClickCandidate(self, *args):
        index = int(args[3][0].GetNumber())
        BigWorld.imeSelectCandidate(index)
