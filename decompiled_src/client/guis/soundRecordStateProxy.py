#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/soundRecordStateProxy.o
import base64
import BigWorld
import gameglobal
import uiConst
import events
import utils
import gamelog
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import asObject
from guis import uiUtils
from data import sys_config_data as SCD
STATE_NO_DEVICE = 'noDevice'
STATE_TOO_SHORT = 'tooShort'
STATE_RECORDING = 'recording'

class SoundRecordStateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SoundRecordStateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SOUND_RECORD_STATE, self.hide)

    def reset(self):
        self.startTime = None
        self.durationTime = None
        self.timeDelta = 0.05
        self.circlePercent = 0
        self.circleCallback = None
        self.state = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SOUND_RECORD_STATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            if self.state:
                self.setState(self.state, self.durationTime)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SOUND_RECORD_STATE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SOUND_RECORD_STATE)

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return

    def setState(self, state = STATE_NO_DEVICE, time = 0):
        self.state = state
        self.durationTime = time
        if not self.widget:
            self.show()
        else:
            soundState = self.widget.soundState
            soundState.gotoAndStop(state)
            if state == STATE_RECORDING:
                self.startRecording(time)
                return
            if state == STATE_NO_DEVICE:
                self.showQrcCode()
                BigWorld.callback(5, self.hide)
            else:
                BigWorld.callback(2, self.hide)

    def startRecording(self, time):
        circleMask = self.widget.soundState.recording.circle.circleMask
        circleMask.radius = 57
        self.startTime = utils.getNow()
        self.durationTime = time
        self.circlePercent = 0
        delta = 1.0 / time * self.timeDelta
        self._startCircle(delta)
        gamelog.debug('bgf@SoundRecordStateProxy startRecording', utils.getNow())

    def _startCircle(self, delta):
        if not self.widget:
            return
        if self.state != STATE_RECORDING:
            return
        if self.circleCallback:
            BigWorld.cancelCallback(self.circleCallback)
        if self.circlePercent >= 1:
            self.timeOut()
            return
        self.circlePercent += delta
        self.widget.soundState.recording.circle.circleMask.percent = self.circlePercent
        self.circleCallback = BigWorld.callback(self.timeDelta, Functor(self._startCircle, delta))

    def timeOut(self):
        gamelog.debug('bgf@SoundRecordStateProxy timeOut', utils.getNow())
        self.hide()
        p = BigWorld.player()
        p.soundRecordTimeOut()

    def showQrcCode(self):
        if self.widget:
            url = SCD.data.get('TIANYU_APP_URL', 'https://tianyu.163.com/download/app/')
            buffer = uiUtils.getQRCodeBuff(url)
            asObject.ASUtils.setQRCode(self.widget.soundState.content.qrcode, buffer)
