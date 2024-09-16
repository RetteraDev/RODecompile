#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryRedPacketResultProxy.o
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

class MarryRedPacketResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryRedPacketResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_RED_PACKET_RESULT, self.hide)

    def reset(self):
        self.packetInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_RED_PACKET_RESULT:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_RED_PACKET_RESULT)

    def show(self, srcName, msg, money):
        self.packetInfo = {}
        self.packetInfo['srcName'] = srcName
        self.packetInfo['msg'] = msg
        self.packetInfo['money'] = money
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_RED_PACKET_RESULT)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.mainMc.roleName.text = self.packetInfo.get('srcName', '')
        self.widget.mainMc.msgTxt.text = self.packetInfo.get('msg', '')
        self.widget.mainMc.moneyMc.bonusMc.bonusNum.text = self.packetInfo.get('money', '')

    def refreshInfo(self):
        if not self.hasBaseData():
            return

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False
