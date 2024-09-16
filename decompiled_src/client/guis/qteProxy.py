#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qteProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
from callbackHelper import Functor
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy

class QteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QteProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerQTE': self.onRegisterQTE,
         'registerQTEResult': self.onRegisterQTEResult,
         'registerQTECombo': self.onRegisterQTECombo}
        self.times = 0
        self.prev = 0
        self.result = False

    def onRegisterQTE(self, *arg):
        self.mc = arg[3][0]
        self.barRef1 = self.mc.GetMember('castbar').GetMember('castbar1')
        self.maskRef1 = self.barRef1.GetMember('percent')
        self.fillRef1 = self.barRef1.GetMember('fill')
        self.shineRef1 = self.barRef1.GetMember('shine')
        self.times = 0
        self.prev = 0
        self.result = False
        self.updateQTE()

    def onRegisterQTEResult(self, *arg):
        if self.result == True:
            arg[3][0].GotoAndPlay('success')
        else:
            arg[3][0].GotoAndPlay('fail')
        BigWorld.callback(2, Functor(self.uiAdapter.movie.invoke, ('_root.unloadWidget', GfxValue(uiConst.WIDGET_QTE_RESULT))))

    def onRegisterQTECombo(self, *arg):
        arg[3][0].GetMember('comboField').SetText(gbk2unicode(gameStrings.TEXT_QTEPROXY_51) + str(self.getSpaceCnt()))
        BigWorld.callback(2, Functor(self.uiAdapter.movie.invoke, ('_root.unloadWidget', GfxValue(uiConst.WIDGET_QTE_COMBO))))

    def startQTE(self, playerCount):
        self.playerCount = playerCount
        self.uiAdapter.loadWidget(uiConst.WIDGET_QTE)

    def updateQTE(self):
        self.times = self.times + 1
        count = self.getSpaceCnt()
        BigWorld.player().cell.uploadQTEInfo(count - self.prev)
        self.prev = count
        if self.times < 16:
            BigWorld.callback(0.5, self.updateQTE)
        else:
            self.mc.Invoke('removeSpaceListener')

    def showResult(self, res):
        self.result = res
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_QTE)))
        self.uiAdapter.loadWidget(uiConst.WIDGET_QTE_RESULT)
        self.uiAdapter.loadWidget(uiConst.WIDGET_QTE_COMBO)

    def setPercent(self, hitNum):
        playerNum = self.playerCount
        pct = int(hitNum * 100 / (60 * playerNum))
        if pct > 100:
            pct = 100
        self.maskRef1.SetXScale(pct)
        self.shineRef1.SetX(self.maskRef1.GetMember('width').GetNumber())
        self.mc.GetMember('castbar').GetMember('achieveScore').SetText(str(pct) + '%')
        self.mc.GetMember('castbar').GetMember('leftScore').SetText(str(100 - pct) + '%')

    def getSpaceCnt(self):
        return int(self.mc.GetMember('spaceCnt').GetNumber())
