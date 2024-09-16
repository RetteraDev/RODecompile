#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipchangeGemProxy.o
import BigWorld
from Scaleform import GfxValue
import gameconfigCommon
import uiConst
from guis import events
from guis.asObject import ASObject
from gamestrings import gameStrings
from uiProxy import UIProxy

class EquipChangeGemProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeGemProxy, self).__init__(uiAdapter)
        self.widget = None
        self.proxyArray = ['equipChangeUnlock', 'equipChangeInlayV2', 'equipChangeGemLvUpV2']
        self.reset()

    def reset(self):
        self.panelArr = []
        self.tabArr = []

    def registerEquipChangeGem(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterEquipChangeGem(self):
        self.widget = None
        self.reset()
        for proxy in self.proxyArray:
            getattr(self.uiAdapter, proxy).unRegisterPanel(None)

    def initUI(self):
        self.widget.tab0.label = gameStrings.EQUIP_CHANGE_GEM_UNLOCK
        self.widget.tab1.label = gameStrings.EQUIP_CHANGE_GEM_INLAY
        self.widget.tab2.label = gameStrings.EQUIP_CHANGE_GEM_COMPOUND
        self.widget.tab2.visible = gameconfigCommon.enableEquipChangeGemLvUp()
        self.panelArr = [self.widget.equipChangeUnlock, self.widget.equipChangeInlayPanel, self.widget.equipChangeGemLvUpPanel]
        self.tabArr = [self.widget.tab0, self.widget.tab1, self.widget.tab2]
        for i, tabMc in enumerate(self.tabArr):
            tabMc.tabIdx = i
            tabMc.addEventListener(events.MOUSE_CLICK, self.onTabBtnClick, False, 0, True)

        self.subTabChanged(1)

    def setRedPointVisible(self, visible):
        if self.widget.tab1.visible and visible:
            self.widget.lvUpRedPoint.visible = True
        else:
            self.widget.lvUpRedPoint.visible = False

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.tabIdx)
        self.subTabChanged(index)
        if index == 1:
            self.widget.lvUpRedPoint.visible = False
        self.uiAdapter.equipChange.setSubTabRedPointVisible('gemLvUp')

    def subTabChanged(self, index):
        redPointVisible = self.uiAdapter.equipChange.getSubTabRedPointVisible('gemLvUp')
        self.setRedPointVisible(redPointVisible)
        for i, tabMc in enumerate(self.tabArr):
            tabMc.selected = i == index

        for i, panelMc in enumerate(self.panelArr):
            if index == i:
                panelMc.visible = True
                getattr(self.uiAdapter, self.proxyArray[i]).registerPanel(panelMc)
            else:
                panelMc.visible = False
                getattr(self.uiAdapter, self.proxyArray[i]).unRegisterPanel(panelMc)

    def handleClickSubTab(self, *args):
        e = ASObject(args[3][0])
        self.subTabChanged(e.currentTarget.data.subTabIdx)
