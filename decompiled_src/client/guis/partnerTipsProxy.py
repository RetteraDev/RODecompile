#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/partnerTipsProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import utils
import commQuest
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor

class PartnerTipsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PartnerTipsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PARTNER_TIPS, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PARTNER_TIPS:
            self.widget = widget
            self.initUI()

    def show(self, entTime):
        self.entTime = entTime
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PARTNER_TIPS)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PARTNER_TIPS)
        self.widget = None

    def reset(self):
        self.cancelCallBack()
        self.leftTime = 0
        self.entTime = 0

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.leftTime = const.PARTNER_CONFIRM_LIMIT_TIME

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            self.updateTime()

    def updateTime(self):
        if self.hasBaseData():
            p = BigWorld.player()
            self.leftTime = self.entTime - utils.getNow()
            self.widget.timeTxt.text = utils.formatTimeStr(self.leftTime)
            if self.leftTime:
                self.cancelCallBack()
                self.timer = BigWorld.callback(1, self.updateTime)
            else:
                self.hide()
        else:
            self.cancelCallBack()

    def cancelCallBack(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False
