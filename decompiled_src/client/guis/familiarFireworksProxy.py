#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/familiarFireworksProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import item_data as ID
from data import personal_zone_gift_data as PZGD

class FamiliarFireworksProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamiliarFireworksProxy, self).__init__(uiAdapter)
        self.widget = None
        self.srcName = ''
        self.giftId = 0
        self.giftNum = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMILIAR_FIREWORKS, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FAMILIAR_FIREWORKS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, srcName, giftId, giftNum):
        p = BigWorld.player()
        if p.inCombat:
            return
        self.srcName = srcName
        self.giftId = giftId
        self.giftNum = giftNum
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMILIAR_FIREWORKS)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMILIAR_FIREWORKS)

    def reset(self):
        self.srcName = ''
        self.giftId = 0
        self.giftNum = 0

    def initUI(self):
        self.widget.giftMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        self.widget.giftMc.thanksBtn.addEventListener(events.BUTTON_CLICK, self.handleThanksBtnClick, False, 0, True)
        giftName = PZGD.data.get(self.giftId, {}).get('name', '')
        self.widget.giftMc.srcName.textField.text = self.srcName
        self.widget.giftMc.giftNameT.textField.text = gameStrings.FAMILIAR_FIREWORKS_GIFT_DESC % (self.giftNum, giftName)
        BigWorld.callback(15, self.hide)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleCloseBtnClick(self, *args):
        self.hide()

    def handleThanksBtnClick(self, *args):
        gameglobal.rds.ui.friend.chatToPlayer(self.srcName)
        self.hide()
