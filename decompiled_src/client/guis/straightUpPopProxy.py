#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/straightUpPopProxy.o
import BigWorld
import gameglobal
import uiConst
from guis import events
from uiProxy import UIProxy
from guis import uiUtils
from data import sys_config_data as SCD
from gamestrings import gameStrings
MAX_ITEM_COUNT = 10

class StraightUpPopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(StraightUpPopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_STRAIGHT_UP_POP, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_STRAIGHT_UP_POP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_STRAIGHT_UP_POP)

    def show(self):
        if not gameglobal.rds.configData.get('enableStraightLvUpV2', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_STRAIGHT_UP_POP)

    def initUI(self):
        mainMc = self.widget.giftMc
        popMc = self.widget.popMc
        self.setMainMc(mainMc)
        self.setMainMc(popMc.mainMc)
        self.setMainMc(popMc.mainMc2)

    def setMainMc(self, mainMc):
        mainMc.okBtn.addEventListener(events.BUTTON_CLICK, self.onOkBtnClick)
        mainMc.detail.htmlText = SCD.data.get('straightUpPopText', gameStrings.STRAIGHT_UP_POP_TIP)
        itemList = SCD.data.get('straightUpPopItems', ())
        for i in xrange(MAX_ITEM_COUNT):
            if i < len(itemList):
                itemId = itemList[i]
                slotMc = mainMc.getChildByName('slot%d' % i)
                slotMc.visible = True
                slotMc.dragable = False
                itemInfo = uiUtils.getGfxItemById(itemId, 1)
                slotMc.setItemSlotData(itemInfo)
            else:
                slotMc = mainMc.getChildByName('slot%d' % i)
                slotMc.visible = False

        p = BigWorld.player()
        mainMc.level.htmlText = str(p.lv)

    def onOkBtnClick(self, *args):
        self.hide()
        gameglobal.rds.ui.straightUp.show()

    def refreshInfo(self):
        if not self.widget:
            return
