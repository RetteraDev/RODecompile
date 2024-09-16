#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalCountDownProxy.o
import BigWorld
from helpers import tickManager
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASUtils
DEFAULT_COUNT_DOWN_15 = 'GeneralCountDown_CountDownText_15'
DEFAULT_COUNT_DOWN_10 = 'GeneralCountDown_CountDownText_10'
DEFAULT_COUNT_DOWN_9 = 'GeneralCountDown_CountDown5'
DEFAULT_COUNT_DOWN_OVER = 'GeneralCountDown_ArenaGameOver'
DEFAULT_OVER_SOUND = gameglobal.SD_62
DEFAULT_COUNT_SOUND = gameglobal.SD_60
DEFAULT_COUNT_DOWN_NUM = 5

class GeneralCountDownProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralCountDownProxy, self).__init__(uiAdapter)
        self.widget = None
        self.destoryCallBack = None
        self.tickId = 0
        self.time = 0
        self.cd15Cls = DEFAULT_COUNT_DOWN_15
        self.cd10Cls = DEFAULT_COUNT_DOWN_10
        self.cd9Cls = DEFAULT_COUNT_DOWN_9
        self.overCls = DEFAULT_COUNT_DOWN_OVER
        self.overSound = DEFAULT_OVER_SOUND
        self.countSound = DEFAULT_COUNT_SOUND
        self.countStart = DEFAULT_COUNT_DOWN_NUM
        self.msgId = 0
        self.msgTime = 5
        self.reset()

    def showCountDown(self, time, paramDict = None):
        self.stopTick()
        self.time = time
        if paramDict == None:
            paramDict = {}
        self.cd15Cls = paramDict.get('cd15Cls', DEFAULT_COUNT_DOWN_15)
        self.cd10Cls = paramDict.get('cd10Cls', DEFAULT_COUNT_DOWN_10)
        self.cd9Cls = paramDict.get('cd9Cls', DEFAULT_COUNT_DOWN_9)
        self.overCls = paramDict.get('overCls', DEFAULT_COUNT_DOWN_OVER)
        self.overSound = paramDict.get('overSound', DEFAULT_OVER_SOUND)
        self.countSound = paramDict.get('countSound', DEFAULT_COUNT_SOUND)
        self.countStart = paramDict.get('countStart', DEFAULT_COUNT_DOWN_NUM)
        self.msgId = paramDict.get('msgId', 0)
        self.msgTime = paramDict.get('msgTime', 5)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_COUNT_DOWN)
        else:
            self.removeAllChild(self.widget.countCanvas)
        self.tickId = tickManager.addTick(1, self.refreshInfo)

    def reset(self):
        self.stopTick()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_COUNT_DOWN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def stopTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        if self.destoryCallBack:
            BigWorld.cancelCallback(self.destoryCallBack)
        self.destoryCallBack = None

    def clearWidget(self):
        self.widget = None
        self.stopTick()
        self.tickId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_COUNT_DOWN)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget, True)
        self.removeAllChild(self.widget.countCanvas)

    def showOverMc(self):
        self.removeAllChild(self.widget.countCanvas)
        overMc = self.widget.getInstByClsName(self.overCls)
        if overMc:
            self.widget.countCanvas.addChild(overMc)
        else:
            return
        self.setPosition(overMc, 0)
        if self.overSound:
            gameglobal.rds.sound.playSound(self.overSound)

    def show15Mc(self, time):
        if time == 15:
            cd15Mc = self.widget.getInstByClsName(self.cd15Cls)
            if not cd15Mc:
                return
            if cd15Mc:
                self.widget.countCanvas.addChild(cd15Mc)
            self.setPosition(cd15Mc, -10)

    def show10Mc(self, time):
        if time == 10:
            cd10Mc = self.widget.getInstByClsName(self.cd10Cls)
            if not cd10Mc:
                return
            if cd10Mc:
                self.widget.countCanvas.addChild(cd10Mc)
            self.setPosition(cd10Mc, -10)

    def show9Mc(self, time):
        if time > self.countStart:
            return
        cd9Mc = self.widget.getChildByName('cd9')
        if not cd9Mc:
            cd9Mc = self.widget.getInstByClsName(self.cd9Cls)
            if cd9Mc:
                cd9Mc.name = 'cd9'
                self.widget.countCanvas.addChild(cd9Mc)
        if not cd9Mc:
            return
        self.setPosition(cd9Mc, 20)
        cd9Mc.gotoAndPlay(1)
        frameName = 'count%s' % str(time)
        if cd9Mc.floor1:
            cd9Mc.floor1.gotoAndPlay(frameName)
        if cd9Mc.floor2:
            cd9Mc.floor2.gotoAndPlay(frameName)
        if cd9Mc.floor3:
            cd9Mc.floor3.gotoAndPlay(frameName)
        if self.countSound:
            gameglobal.rds.sound.playSound(self.countSound)

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)

    def setPosition(self, mc, posX = 0, posY = 0):
        self.widget.countCanvas.x = (self.widget.stage.stageWidth - mc.width) / 2
        self.widget.countCanvas.y = (self.widget.stage.stageHeight - mc.height) / 2
        mc.x = posX
        mc.y = posY

    def refreshInfo(self):
        if not self.widget:
            return
        if self.time <= 0:
            self.time = 0
            self.stopTick()
            self.showOverMc()
            self.destoryCallBack = BigWorld.callback(5, self.clearWidget)
            return
        if self.time <= 9:
            self.show9Mc(self.time)
        elif self.time <= 10:
            self.show10Mc(self.time)
        elif self.time <= 15:
            self.show15Mc(self.time)
        if self.time <= self.msgTime:
            if self.msgId:
                p = BigWorld.player()
                p.showGameMsg(self.msgId, str(self.time))
        self.time -= 1
