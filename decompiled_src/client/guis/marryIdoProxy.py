#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryIdoProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_config_data as MCD

class MarryIdoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryIdoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.tgtType = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_IDO:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_IDO)

    def show(self, tgtType):
        self.tgtType = tgtType
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_IDO)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        p = BigWorld.player()
        desc = ''
        if self.tgtType == const.SEX_MALE:
            desc = MCD.data.get('hunsbandIdoDesc', '%s')
        elif self.tgtType == const.SEX_FEMALE:
            desc = MCD.data.get('wifeIdoDesc', '%s')
        msg = desc % (p.intimacyTgtName,)
        self.widget.desc.htmlText = msg

    def refreshInfo(self):
        if not self.hasBaseData():
            return

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def _onLeftBtnClick(self, e):
        self.doPledge()

    def _onRightBtnClick(self, e):
        self.doPledge()

    def doPledge(self):
        p = BigWorld.player()
        if self.tgtType == const.SEX_MALE:
            p.cell.marriagePledgeHusbandOk()
        elif self.tgtType == const.SEX_FEMALE:
            p.cell.marriagePledgeWifeOk()
        self.hide()
