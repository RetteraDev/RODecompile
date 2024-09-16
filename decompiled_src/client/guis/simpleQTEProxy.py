#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/simpleQTEProxy.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gameglobal
from sMath import limit
from uiProxy import UIProxy
from guis import uiConst
from guis.asObject import ASUtils
from guis import uiUtils
from data import simple_qte_data as SQD
COUNTDOWN_INTERVAL = 0.2
QTE_TYPE_AD = 1

class QTEPattern(object):

    def __init__(self, patterns, qteType):
        self.qteType = qteType
        self.nowIndex = 0
        self.patterns = patterns
        gamelog.debug('----m.l@QTEPattern.__init__', patterns)

    def getKey(self):
        return self.patterns[self.nowIndex]

    def handleInput(self, inputKey):
        if inputKey == self.getKey():
            self.nowIndex = self.nowIndex + 1
            return True
        return False

    def isOver(self):
        return self.nowIndex > len(self.patterns) - 1

    def restart(self):
        self.nowIndex = 0


class SimpleQTEProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SimpleQTEProxy, self).__init__(uiAdapter)
        self.widget = None
        self.seconds = 0
        self.duration = 0
        self.vanishCallback = None
        self.countdownCallback = None
        self.simpleQteId = 0
        self.lockCamera = False
        self.oldScrollNum = None
        self.qteType = None
        self.qtePattern = None
        self.simpleQteData = {}
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SIMPLE_QTE:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SIMPLE_QTE)
        gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_SIMPLE_QTE, False)
        self.reset()

    def show(self, simpleQteId):
        simpleQteData = SQD.data.get(simpleQteId, {})
        if not simpleQteData:
            return
        seconds = simpleQteData.get('duration', 0)
        if not seconds:
            return
        self.reset()
        self.simpleQteId = simpleQteId
        self.simpleQteData = simpleQteData
        pattern = self.simpleQteData.get('pattern', ())
        self.qteType = self.simpleQteData.get('qteType', QTE_TYPE_AD)
        self.qtePattern = QTEPattern(pattern, self.qteType)
        self.seconds = seconds
        self.duration = seconds
        self.lockCamera = self.simpleQteData.get('lockCamera', False)
        scrollRange = self.simpleQteData.get('cameraRange', ())
        if scrollRange:
            self.oldScrollNum = gameglobal.rds.cam.currentScrollNum
            BigWorld.player().resetCamera()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SIMPLE_QTE)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        if self.qteType == QTE_TYPE_AD:
            self.widget.gotoAndPlay('texiao01')
            self.widget.countdownTF.text = '%dS' % self.seconds
            self.widget.progress.currentValue = 0
            ASUtils.setMcData(self.widget.btnMC1, 'keyTxt', gameStrings.TEXT_HOTKEYPROXY_24)
            ASUtils.setMcData(self.widget.btnMC2, 'keyTxt', gameStrings.TEXT_HOTKEYPROXY_24_1)
            self.countdown()

    def countdown(self):
        if self.seconds <= 0:
            return
        else:
            if self.countdownCallback:
                BigWorld.cancelCallback(self.countdownCallback)
                self.countdownCallback = None
            self.seconds = self.seconds - COUNTDOWN_INTERVAL
            self.widget.countdownTF.text = uiUtils.gbk2unicode('%dS' % self.seconds)
            self.updateProgressValue()
            self.countdownCallback = BigWorld.callback(COUNTDOWN_INTERVAL, self.countdown)
            return

    def handleInputKey(self, key):
        self.qtePattern.handleInput(key)
        if self.qtePattern.isOver():
            self.decQTETime(self.simpleQteData.get('reduceTime', 0))
            self.qtePattern.restart()

    def updateProgressValue(self):
        if not self.widget:
            return
        percent = (self.duration - self.seconds) * 100.0 / self.duration
        self.widget.progress.currentValue = percent
        if abs(percent - 100) < 0.1 or self.seconds < 0:
            BigWorld.player().cell.endSimpleQte(True, self.simpleQteId)

    def endSimpleQte(self):
        scrollRange = self.simpleQteData.get('cameraRange', ())
        if scrollRange:
            if self.oldScrollNum:
                gameglobal.rds.cam.currentScrollNum = self.oldScrollNum
                BigWorld.player().resetCamera()
                self.oldScrollNum = None
        self.playVanish()

    def decQTETime(self, seconds):
        self.seconds = self.seconds - seconds
        self.updateProgressValue()

    def playVanish(self):
        if not self.widget:
            return
        self.lockCamera = False
        self.widget.gotoAndPlay('texiao02')
        if self.vanishCallback:
            ASUtils.cancelCallBack(self.vanishCallback)
        self.vanishCallback = ASUtils.callbackAtFrame(self.widget.progressv, 30, self.after)

    def after(self, *arg):
        self.hide()

    def playNormal(self):
        if not self.widget:
            return
        self.widget.gotoAndPlay('texiao01')

    def reset(self):
        self.seconds = 0
        self.duration = 0
        self.simpleQteId = 0
        self.lockCamera = False
        self.oldScrollNum = None
        self.qteType = None
        self.qtePattern = None
        self.simpleQteData = {}
        if self.vanishCallback:
            ASUtils.cancelCallBack(self.vanishCallback)
            self.vanishCallback = None
        if self.countdownCallback:
            BigWorld.cancelCallback(self.countdownCallback)
            self.countdownCallback = None
