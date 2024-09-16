#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiTab2Proxy.o
from guis import events
from guis.asObject import ASObject
from guis.asObject import Tweener
from uiProxy import UIProxy
from data import sys_config_data as SCD

class UITab2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UITab2Proxy, self).__init__(uiAdapter)
        self.tabList = self._getTabList()
        self.widget = None
        self.currentTabIdx = -1
        self.currentView = None

    def reset(self):
        self.widget = None
        self.currentTabIdx = -1
        self.currentView = None

    def initPanel(self, widget):
        self.currentTabIdx = -1
        self.widget = widget
        self.initTabBtn()

    def unRegisterPanel(self):
        self.unRegisterSubPanel()
        self.reset()

    def initTabBtn(self):
        if self.widget.btnList:
            itemList = self.widget.btnList.itemList
            itemList.labelFunction = self.btnlistlabelFunc
            itemList.dataArray = self._getTabList()
        for idx, tabInfo in enumerate(self.tabList):
            btnName = tabInfo['btnName']
            btn = getattr(self.widget, btnName, None)
            btn.idx = idx
            btn.tabInfo = tabInfo
            btn.groupName = self.__class__.__name__
            btn.addEventListener(events.BUTTON_CLICK, self.onClickSubTabBtn, False, 0, True)

    def btnlistlabelFunc(self, *args):
        data = ASObject(args[3][0])
        btn = ASObject(args[3][1])
        btn.label = data.btnLabel
        setattr(self.widget, data.btnName, btn)

    def initSubPanel(self, currentView):
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'initPanel'):
            proxy.initPanel(currentView)

    def unRegisterSubPanel(self):
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'unRegisterPanel'):
            proxy.unRegisterPanel()
        if self.currentView:
            self.addFadeOutEffect(self.currentView)

    def _getTabList(self):
        return []

    def onClickSubTabBtn(self, *args):
        btn = ASObject(args[3][0]).currentTarget
        self.selectSubTab(btn.idx)

    def selectSubTab(self, newTabIdx):
        if not self.widget:
            return
        if newTabIdx == self.currentTabIdx:
            return
        tabInfo = self.tabList[newTabIdx]
        btn = getattr(self.widget, tabInfo['btnName'])
        btn.selected = True
        newView = self.widget.getInstByClsName(tabInfo['clsName'])
        newView.visible = True
        self.widget.addChild(newView)
        self.widget.setChildIndex(newView, 0)
        newView.x, newView.y = tabInfo.get('pos', (0, 0))
        self.unRegisterSubPanel()
        self.onTabChanged(newView, newTabIdx)
        self.addFadeInEffect(newView, newView.x, newView.y)

    def onTabChanged(self, newView, newTabIdx):
        self.currentTabIdx = newTabIdx
        self.currentView = newView
        self.initSubPanel(newView)

    def getCurrentProxy(self):
        if self.currentTabIdx == -1:
            return None
        else:
            return getattr(self.uiAdapter, self.tabList[self.currentTabIdx].get('proxy', ''), None)

    def addFadeInEffect(self, mc, targetX, targetY):
        if not mc:
            return
        Tweener.removeTweens(mc)
        mc.x = targetX - SCD.data.get('tabFadeInOffsetX', 0)
        mc.y = targetY
        mc.alpha = 0
        effect = {'alpha': 1,
         'time': SCD.data.get('tabFadeInTime', 0.1),
         'transition': 'easeInOutCubic',
         'x': targetX}
        Tweener.addTween(mc, effect)

    def addFadeOutEffect(self, mc):
        if not mc or not mc.parent:
            return
        Tweener.removeTweens(mc)
        effect = {'alpha': 0,
         'time': SCD.data.get('tabFadeOutTime', 0.1),
         'onComplete': self._fadeOutComplete,
         'onCompleteParams': [mc]}
        Tweener.addTween(mc, effect)

    def _fadeOutComplete(self, *args):
        mc = ASObject(args[3][0])
        if mc and mc.parent:
            mc.parent.removeChild(mc)
