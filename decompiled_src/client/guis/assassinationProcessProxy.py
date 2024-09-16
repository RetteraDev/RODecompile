#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationProcessProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import gametypes
import const
import ui
from sfx import screenEffect
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
import clientUtils
from cdata import assassination_config_data as ACD
from data import sys_config_data as SCD

class AssassinationProcessProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationProcessProxy, self).__init__(uiAdapter)
        self.widget = None
        self.name = ''
        self.startTimeStamp = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_PROCESS:
            self.widget = widget
            self.initUI()
            self.showCenterMc()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_PROCESS)

    def show(self, name, startTimeStamp = 0):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        self.name = name
        self.startTimeStamp = startTimeStamp
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_PROCESS)
        else:
            self.showCenterMc()

    def initUI(self):
        self.widget.centerMC.visible = False
        self.showTimeMc(False)
        self.showHintMc(False)
        self.endAssassinationEffect()

    def showCenterMc(self):
        self.widget.centerMC.visible = True
        isHidden = False
        if self.name == '':
            self.widget.centerMC.visible = False
            self.showTimeMc(False)
            self.showHintMc(False)
            self.endAssassinationEffect()
            self.hide()
            return
        else:
            if self.name == 'start':
                self.showTimeMc(True)
                self.showHintMc(True)
                self.startAssassinationEffect()
            if self.name == 'success' or self.name == 'fail' or self.name == 'defendSuccess' or self.name == 'defendFail':
                self.showTimeMc(False)
                self.showHintMc(False)
                self.endAssassinationEffect()
                isHidden = True
            self.widget.centerMC.gotoAndStop(str(self.name))
            playMc = getattr(self.widget.centerMC, str(self.name), None)
            if playMc:
                if self.name == 'start' and utils.getNow() - self.startTimeStamp > ACD.data.get('assassinationProcessHintTime', 3):
                    playMc.visible = False
                else:
                    playMc.visible = True
                    playMc.gotoAndPlay(0)
                    displayedTime = ACD.data.get('assassinationProcessHintTime', 3)
                    BigWorld.callback(displayedTime, Functor(self.playMcDisplayCallBack, playMc, isHidden))
            return

    def playMcDisplayCallBack(self, playMc, isHidden):
        if not self.widget:
            return
        else:
            if playMc:
                playMc.visible = False
                playParentMc = getattr(playMc, 'parent', None)
                if playParentMc:
                    playParentMc.visible = False
            if isHidden and self.widget:
                self.hide()
            return

    def showTimeMc(self, enable):
        if self.widget and self.widget.timeMc:
            self.widget.timeMc.visible = enable
            self.widget.timeMc.y = 0
            if enable and self.startTimeStamp != 0:
                timeErrorOffsetStamp = utils.getNow() - self.startTimeStamp
                timeDurationOffsetStamp = ACD.data.get('assassinationKillTimeLimit', 300)
                realTimeDurationOffsetStamp = timeDurationOffsetStamp - timeErrorOffsetStamp
                BigWorld.callback(1, Functor(self.timeMcPlayCallBack, realTimeDurationOffsetStamp))
                self.showTimeCountMc(realTimeDurationOffsetStamp)

    def timeMcPlayCallBack(self, durationOffsetStamp):
        if not self.widget:
            return
        durationOffsetStamp = durationOffsetStamp - 1
        if durationOffsetStamp < 0:
            self.showTimeMc(False)
            self.showHintMc(False)
            self.endAssassinationEffect()
        else:
            BigWorld.callback(1, Functor(self.timeMcPlayCallBack, durationOffsetStamp))
            self.showTimeCountMc(durationOffsetStamp)

    def showTimeCountMc(self, stamp):
        if not self.widget:
            return
        minute = stamp // 60
        second = stamp % 60
        self.widget.timeMc.countMc.text = '%d:%.2d' % (minute, second)

    def showHintMc(self, enable):
        if self.widget and self.widget.hintMc:
            self.widget.hintMc.visible = enable
            self.widget.hintMc.y = self.widget.timeMc.height

    def startAssassinationEffect(self):
        if not self.widget:
            return
        effectId = SCD.data.get('screenEffectHp', 1016)
        screenEffect.startEffect(gameglobal.EFFECT_TAG_HP, effectId)

    def endAssassinationEffect(self):
        if not self.widget:
            return
        screenEffect.delEffect(gameglobal.EFFECT_TAG_HP)
