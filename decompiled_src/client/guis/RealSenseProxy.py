#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/RealSenseProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import gametypes
from uiProxy import UIProxy
from guis import uiConst
from ui import gbk2unicode
try:
    import RealSense as rs
except:
    rs = None

from data import sys_config_data as SCD
emotionMap = {'joy': 'standard_1',
 'anger': 'standard_2',
 'surprise': 'special_2'}

class RealSenseProxy(UIProxy):
    DEV_UNKNOWN = 0
    DEV_AVAILABLE = 1
    DEV_NOT_AVAILABLE = 2

    def __init__(self, uiAdapter):
        super(RealSenseProxy, self).__init__(uiAdapter)
        self.modelMap = {'reset': self.countDown,
         'enable': self.enable,
         'timeReady': self.onTiemReady}
        self.currentEmotion = ''
        self.mapEmotion = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_REAL_SENSE_BTN:
            self.med = mediator

    def initCamera(self):
        BigWorld.callback(3, self._initCamera)

    def _initCamera(self):
        self.dev = RealSenseProxy.DEV_UNKNOWN
        if rs and gameglobal.rds.configData.get('enableRealSense', False):
            rs.init(self.onInitOK, self.onInitFail, self.onEmotionChanged)

    def closeCamera(self):
        self.dev = RealSenseProxy.DEV_UNKNOWN
        if rs:
            rs.cleanup()

    def onInitOK(self):
        self.dev = RealSenseProxy.DEV_AVAILABLE
        self.show()

    def onInitFail(self):
        self.dev = RealSenseProxy.DEV_NOT_AVAILABLE

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REAL_SENSE_BTN)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(SCD.data.get('REAL_SENSE_DETECTED', gameStrings.TEXT_REALSENSEPROXY_67), yesCallback=self.countDown, noCallback=self.closeRealSense)

    def closeRealSense(self):
        self.closeCamera()

    def openRealSense(self):
        self._initCamera()

    def countDown(self, *arg):
        if self.dev != RealSenseProxy.DEV_AVAILABLE:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REAL_SENSE_CLOCK)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REAL_SENSE_TITLE)
        if rs:
            rs.resetSamples()
            rs.setDynamic(True)
        self.mapEmotion = False

    def onTiemReady(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REAL_SENSE_CLOCK)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REAL_SENSE_TITLE)
        gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_REALSENSEPROXY_94)
        if rs:
            rs.setDynamic(False)
        self.mapEmotion = True

    def enable(self, *arg):
        self.mapEmotion = not self.mapEmotion
        p = self.getPlayer()
        p.endFaceEmote()
        if self.dev == RealSenseProxy.DEV_AVAILABLE:
            self.closeRealSense()
            self.setEnableText(gameStrings.TEXT_REALSENSEPROXY_107)
        else:
            self.openRealSense()
            self.setEnableText(gameStrings.TEXT_REALSENSEPROXY_110)

    def setEnableText(self, msg):
        if self.med:
            self.med.Invoke('setEnableText', GfxValue(gbk2unicode(msg)))

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REAL_SENSE_BTN)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REAL_SENSE_CLOCK)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REAL_SENSE_TITLE)

    def onEmotionChanged(self, emo):
        if not self.mapEmotion:
            return
        p = self.getPlayer()
        if self.currentEmotion != '':
            p.endFaceEmote()
        if emo == 'none':
            return
        try:
            self.currentEmotion = emotionMap[emo]
            p.startFaceEmote(self.currentEmotion)
        except:
            gamelog.debug('unknown emotion: ' + emo)

    def getPlayer(self):
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return gameglobal.rds.loginScene.player
        p = BigWorld.player()
        return p

    def reset(self):
        self.med = None
        self.closeRealSense()
