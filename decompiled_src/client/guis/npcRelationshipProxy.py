#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcRelationshipProxy.o
import BigWorld
import uiConst
from guis.asObject import ASObject
from uiTabProxy import UITabProxy

class NpcRelationshipProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(NpcRelationshipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NPC_RELATIONSHIP, self.hide)

    def reset(self):
        self.npcId = 0
        self.isFromNpc = True
        super(NpcRelationshipProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NPC_RELATIONSHIP:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)
            self.refreshInfo()

    def clearWidget(self):
        super(NpcRelationshipProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_RELATIONSHIP)

    def show(self, tabIdx = uiConst.NPC_RELATIONSHIP_TAB_GUANXI, npcPId = 0, fromNpc = True):
        self.isFromNpc = fromNpc
        if tabIdx == uiConst.NPC_RELATIONSHIP_TAB_OVERVIEW and npcPId:
            self.uiAdapter.npcRelationshipOverView.selectedNpcId = npcPId
        if not npcPId:
            self.npcId = self.uiAdapter.npcRelationshipOverView.getNpcList()[0]
        else:
            self.npcId = npcPId
        self.showTabIndex = tabIdx
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_RELATIONSHIP)

    def _getTabList(self):
        return [{'tabIdx': uiConst.NPC_RELATIONSHIP_TAB_GUANXI,
          'tabName': 'guanxiBtn',
          'proxy': 'npcRelationshipGuanxi',
          'view': 'NpcRelationshipNpcWidget'},
         {'tabIdx': uiConst.NPC_RELATIONSHIP_TAB_HAOGAN,
          'tabName': 'haoganBtn',
          'proxy': 'npcRelationshipHaogan',
          'view': 'NpcRelationshipHaoganWidget'},
         {'tabIdx': uiConst.NPC_RELATIONSHIP_TAB_XINDONG,
          'tabName': 'xindongBtn',
          'proxy': 'npcRelationshipXindong',
          'view': 'NpcRelationshipXindongWidget'},
         {'tabIdx': uiConst.NPC_RELATIONSHIP_TAB_OVERVIEW,
          'tabName': 'overViewBtn',
          'proxy': 'npcRelationshipOverView',
          'view': 'NpcRelationshipOverViewWidget'}]

    def initUI(self):
        self.initTabUI()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.haoganBtn.visible = self.isFromNpc
        self.widget.guanxiBtn.visible = self.isFromNpc

    def refreshInfo(self):
        if not self.widget:
            return
