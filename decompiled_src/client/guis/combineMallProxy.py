#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/combineMallProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import ui
from uiProxy import UIProxy
from guis.asObject import ASObject
from cdata import game_msg_def_data as GMDD
TAB_TIANYU_MALL = 0
TAB_YUNCHUI_SHOP = 1
MAX_TAB_NUM = 2

class CombineMallProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CombineMallProxy, self).__init__(uiAdapter)
        self.reset()
        self.currentTab = -1
        self.showLeftTab = True
        uiAdapter.registerEscFunc(uiConst.WIDGET_CONBINE_MALL, self.hide)

    def reset(self):
        super(CombineMallProxy, self).reset()
        self.widget = None
        self.currentTab = -1
        self.showLeftTab = True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CONBINE_MALL:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.currentTab = -1
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CONBINE_MALL)

    def show(self, showTab = 0, showLeftTab = True):
        self.showLeftTab = showLeftTab
        if self.widget:
            self.refreshAllChildVisible()
            return
        self.currentTab = showTab
        self.uiAdapter.loadWidget(uiConst.WIDGET_CONBINE_MALL)
        if showTab == TAB_TIANYU_MALL:
            if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
                if not gameglobal.rds.ui.inventory.canOpenPrivateShop():
                    return
            if not self.uiAdapter.yunChuiShop.mediator:
                gameglobal.rds.ui.inventory.openYunChuiShop()
        elif showTab == TAB_YUNCHUI_SHOP:
            if not gameglobal.rds.ui.tianyuMall.showMallConfig():
                return
            if not self.uiAdapter.tianyuMall.mallMediator:
                gameglobal.rds.ui.tianyuMall.show()

    def initUI(self):
        self.widget.mallTab0.addEventListener(events.BUTTON_CLICK, self.handleClickMallTab0, False, 0, True)
        self.widget.mallTab1.addEventListener(events.BUTTON_CLICK, self.handleClickMallTab1, False, 0, True)
        self.setSelectedBtn(self.currentTab)
        self.refreshAllChildVisible()

    def refreshAllChildVisible(self):
        childrenNums = self.widget.numChildren
        for i in xrange(childrenNums):
            self.widget.getChildAt(i).visible = self.showLeftTab

    def refreshInfo(self):
        if not self.widget:
            return

    def handleClickMallTab0(self, *args):
        if self.currentTab == TAB_TIANYU_MALL:
            return
        if not gameglobal.rds.ui.tianyuMall.showMallConfig():
            gameglobal.rds.ui.tianyuMall.notifyMallCantUse()
            return
        self.currentTab = TAB_TIANYU_MALL
        if gameglobal.rds.ui.yunChuiShop.mediator and gameglobal.rds.ui.tianyuMall.mallMediator:
            tianyuMall = ASObject(gameglobal.rds.ui.tianyuMall.mallMediator)
            YunChuiShop = ASObject(gameglobal.rds.ui.yunChuiShop.mediator)
            tianyuMall.getWidget().x = YunChuiShop.getWidget().x
            tianyuMall.getWidget().y = YunChuiShop.getWidget().y
        gameglobal.rds.ui.yunChuiShop.tabHide()
        self.setSelectedBtn(self.currentTab)

    def handleClickMallTab1(self, *args):
        if self.currentTab == TAB_YUNCHUI_SHOP:
            return
        if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
            if not gameglobal.rds.ui.inventory.canOpenPrivateShop():
                BigWorld.player().showGameMsg(GMDD.data.YUN_CHUI_SHOP_NOT_AVALIBLE, ())
                return
        self.currentTab = TAB_YUNCHUI_SHOP
        if gameglobal.rds.ui.yunChuiShop.mediator and gameglobal.rds.ui.tianyuMall.mallMediator:
            tianyuMall = ASObject(gameglobal.rds.ui.tianyuMall.mallMediator)
            YunChuiShop = ASObject(gameglobal.rds.ui.yunChuiShop.mediator)
            YunChuiShop.getWidget().x = tianyuMall.getWidget().x
            YunChuiShop.getWidget().y = tianyuMall.getWidget().y
        elif not gameglobal.rds.ui.yunChuiShop.mediator:
            gameglobal.rds.ui.inventory.openYunChuiShop()
        gameglobal.rds.ui.tianyuMall.tabHide()
        self.setSelectedBtn(self.currentTab)

    def setSelectedBtn(self, tabToSelected):
        if self.currentTab < 0:
            return
        if self.currentTab == TAB_YUNCHUI_SHOP:
            lastTab = 'mallTab0'
        else:
            lastTab = 'mallTab1'
        self.widget.getChildByName(lastTab).selected = False
        self.widget.getChildByName('mallTab' + str(tabToSelected)).selected = True
