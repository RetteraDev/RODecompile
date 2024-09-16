#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillShareBGProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
import events
from guis.asObject import ASObject
from uiProxy import UIProxy
COMMON_SKILL_TAB = 'widgets/CommonSkillSharePanel.swf'
WUSHUANG_SKILL_TAB = 'widgets/WuShuangSkillSharePanel.swf'
FIRST_TAB_INDEX = 0
SECOND_TAB_INDEX = 1
TAB_VIEW_MAP = {FIRST_TAB_INDEX: 'commonSkillShare',
 SECOND_TAB_INDEX: 'wuShuangSkillShare'}

class SkillShareBGProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillShareBGProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_SHARE_BG, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.tabButtons = [self.widget.hit.commonSkillTab, self.widget.hit.wsSkillTab]
        self.widget.tabViewPaths = [COMMON_SKILL_TAB, WUSHUANG_SKILL_TAB]
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.onTabChanged = self.onTabChanged
        self.tabIdx = FIRST_TAB_INDEX
        self.tabButtonsLen = 2

    def show(self):
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_SHARE_BG)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.unRegisterCurrPanel()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_SHARE_BG)

    def hidePanel(self, *args):
        self.clearWidget()

    def getTabViewProxy(self, index):
        return getattr(self.uiAdapter, TAB_VIEW_MAP.get(index, ''), None)

    def setTabBtnSelected(self):
        for i in range(0, self.tabButtonsLen):
            if i == self.tabIdx:
                self.widget.tabButtons[i].selected = True
            else:
                self.widget.tabButtons[i].selected = False

    def unRegisterCurrPanel(self):
        lastProxy = self.getTabViewProxy(self.tabIdx)
        if lastProxy and hasattr(lastProxy, 'unRegisterPanel'):
            lastProxy.unRegisterPanel()

    def onTabChanged(self, *args):
        currentTabIndex = int(args[3][0].GetNumber())
        currentView = ASObject(args[3][1])
        if currentTabIndex != self.tabIdx:
            self.unRegisterCurrPanel()
            self.tabIdx = currentTabIndex
        currentProxy = self.getTabViewProxy(self.tabIdx)
        if currentProxy and hasattr(currentProxy, 'initPanel'):
            currentProxy.initPanel(currentView)
        self.setTabBtnSelected()
