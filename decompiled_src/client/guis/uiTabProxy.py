#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiTabProxy.o
from uiProxy import UIProxy
from asObject import ASObject

class UITabProxy(UIProxy):
    TAB_TYPE_PATH = 0
    TAB_TYPE_CLS = 1

    def __init__(self, uiAdapter):
        super(UITabProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tabType = UITabProxy.TAB_TYPE_PATH
        self.tabList = []
        self.tabMap = {}
        self.showTabIndex = -1
        self.currentTabIndex = -1
        self.currentView = None

    def clearWidget(self):
        self.unRegisterPanel()

    def reset(self):
        self.showTabIndex = -1
        self.currentTabIndex = -1
        self.currentView = None

    def _getTabList(self):
        return []

    def initTabUI(self):
        if not self.widget:
            return
        else:
            self.tabList = self._getTabList()
            self.tabMap = {}
            tabButtons = []
            tabViewPaths = []
            tabViewClsNames = []
            for tabInfo in self.tabList:
                tabIdx = tabInfo.get('tabIdx', 0)
                tabName = tabInfo.get('tabName', '')
                view = tabInfo.get('view', '')
                self.tabMap[tabIdx] = tabInfo
                tabButtons.append(getattr(self.widget, tabName, None))
                if self.tabType == UITabProxy.TAB_TYPE_PATH:
                    tabViewPaths.append('widgets/%s.swf' % view)
                elif self.tabType == UITabProxy.TAB_TYPE_CLS:
                    tabViewClsNames.append(view)

            self.widget.tabButtons = tabButtons
            if self.tabType == UITabProxy.TAB_TYPE_PATH:
                self.widget.tabViewPaths = tabViewPaths
            elif self.tabType == UITabProxy.TAB_TYPE_CLS:
                self.widget.tabViewClsNames = tabViewClsNames
            self.widget.onTabChanged = self.onTabChanged
            return

    def getCurrentProxy(self):
        return getattr(self.uiAdapter, self.tabMap.get(self.currentTabIndex, {}).get('proxy', ''), None)

    def onTabChanged(self, *args):
        currentTabIndex = int(args[3][0].GetNumber())
        currentView = ASObject(args[3][1])
        if self.currentTabIndex >= 0:
            self.unRegisterPanel()
        self.currentTabIndex = currentTabIndex
        self.currentView = currentView
        if self.currentView:
            pos = self.tabMap.get(self.currentTabIndex, {}).get('pos', (0, 0))
            self.currentView.x = pos[0]
            self.currentView.y = pos[1]
        if self.tabType == UITabProxy.TAB_TYPE_PATH:
            proxy = self.getCurrentProxy()
            if proxy and hasattr(proxy, 'initPanel'):
                proxy.initPanel(currentView)

    def unRegisterPanel(self):
        if self.tabType == UITabProxy.TAB_TYPE_PATH:
            proxy = self.getCurrentProxy()
            if proxy and hasattr(proxy, 'unRegisterPanel'):
                proxy.unRegisterPanel()

    def setTabVisible(self, tabIdx, visible, needRelayout):
        tabMc = getattr(self.widget, self.tabMap.get(tabIdx, {}).get('tabName', ''), None)
        if not tabMc:
            return
        else:
            tabMc.visible = visible
            if needRelayout:
                self.relayoutTab()
            return

    def relayoutTab(self):
        if len(self.tabList) < 2:
            return
        else:
            tabPosX = None
            tabPosY = None
            tabOffsetX = 0
            tabOffsetY = 0
            for tabInfo in self.tabList:
                tabMc = getattr(self.widget, tabInfo.get('tabName', ''), None)
                if not tabMc:
                    continue
                if tabPosX == None:
                    tabPosX = tabMc.x
                    tabPosY = tabMc.y
                elif tabOffsetX == 0 and tabOffsetY == 0:
                    tabOffsetX = tabMc.x - tabPosX
                    tabOffsetY = tabMc.y - tabPosY
                else:
                    break

            for tabInfo in self.tabList:
                tabMc = getattr(self.widget, tabInfo.get('tabName', ''), None)
                if not tabMc or tabMc.visible == False:
                    continue
                tabMc.x = tabPosX
                tabMc.y = tabPosY
                tabPosX += tabOffsetX
                tabPosY += tabOffsetY

            return
