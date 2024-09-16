#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldResourceProxy.o
import BigWorld
import events
from uiProxy import UIProxy
from asObject import ASObject
from gameStrings import gameStrings
from guis import wingWorldResourceCountryPanel as P1
from guis import wingWorldResourceCollectPanel as P2
from data import wing_world_config_data as WWCD
TAB_MAIN = 'TAB_MAIN'
TAB_MAIN_COLLECT = 'TAB_MAIN_COLLECT'
TAB_MAIN_COUNTRY = 'TAB_MAIN_COUNTRY'
TAB_SUB = 'TAB_SUB'
TAB_SUB_POINT = 'TAB_SUB_POINT'
TAB_SUB_RECORD = 'TAB_SUB_RECORD'

class WingWorldResourceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldResourceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.countryPanel = P1.WingWorldResourceCountryPanel()
        self.collectPanel = P2.WingWorldResourceCollectPanel()
        self.groupMain = {}
        self.groupSub = {}
        self.tabGroupSelected = {}
        self.panelCache = {}

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.widget.selectSpritePanel.visible = False
        self.countryPanel.initPanel(self.widget.countryPanel, widget)
        self.collectPanel.initPanel(self.widget.collectPanel, widget)
        self.initUI()

    def unRegisterPanel(self):
        if not self.widget:
            return
        else:
            if self.countryPanel:
                self.countryPanel.unRegisterPanel()
            if self.collectPanel:
                self.collectPanel.unRegisterPanel()
            self.widget = None
            return

    def refreshInfo(self):
        if not self.widget:
            return

    def initUI(self):
        self.initGourps()
        if not self.tabGroupSelected:
            self.tabGroupSelected = {TAB_MAIN: '',
             TAB_SUB: ''}
            self.selectTab(TAB_MAIN, TAB_MAIN_COLLECT)
            self.selectTab(TAB_SUB, TAB_SUB_POINT)
        else:
            oldMain = self.tabGroupSelected[TAB_MAIN]
            oldSub = self.tabGroupSelected[TAB_SUB]
            self.tabGroupSelected = {TAB_MAIN: '',
             TAB_SUB: ''}
            self.selectTab(TAB_MAIN, oldMain)
            self.selectTab(TAB_SUB, oldSub)

    def initGourps(self):
        self.groupMain = {TAB_MAIN_COLLECT: {'tabBtn': self.widget.collectTab,
                            'panel': self.widget.collectPanel},
         TAB_MAIN_COUNTRY: {'tabBtn': self.widget.countryTab,
                            'panel': self.widget.countryPanel}}
        self.groupSub = {TAB_SUB_POINT: {'tabBtn': self.widget.countryPanel.pointSubTab,
                         'panel': self.widget.countryPanel.pointSubPanel},
         TAB_SUB_RECORD: {'tabBtn': self.widget.countryPanel.recordSubTab,
                          'panel': self.widget.countryPanel.recordSubPanel}}
        for tabIndex, groupInfo in self.groupMain.items():
            groupInfo['tabBtn'].data = TAB_MAIN + '.' + tabIndex
            groupInfo['tabBtn'].addEventListener(events.MOUSE_CLICK, self.handleTabBtnClick, False, 0, True)
            groupInfo['panel'].visible = False

        for tabIndex, groupInfo in self.groupSub.items():
            groupInfo['tabBtn'].data = TAB_SUB + '.' + tabIndex
            groupInfo['tabBtn'].addEventListener(events.MOUSE_CLICK, self.handleTabBtnClick, False, 0, True)
            groupInfo['panel'].visible = False

    def selectTab(self, groupName, index):
        group = self.getTabGroupByName(groupName)
        if not group or index == self.tabGroupSelected[groupName]:
            return
        selectIndex = self.tabGroupSelected[groupName]
        if selectIndex:
            group[selectIndex]['tabBtn'].selected = False
            group[selectIndex]['panel'].visible = False
        group[index]['tabBtn'].selected = True
        group[index]['panel'].visible = True
        self.tabGroupSelected[groupName] = index
        self.onPanelShow(groupName, index)

    def getTabGroupByName(self, name):
        if name == TAB_MAIN:
            return self.groupMain
        elif name == TAB_SUB:
            return self.groupSub
        else:
            return None

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.data:
            return
        names = e.currentTarget.data.split('.')
        groupName = names[0]
        tabName = names[1]
        self.selectTab(groupName, tabName)

    def onPanelShow(self, groupName, tabName):
        if groupName == TAB_MAIN:
            if tabName == TAB_MAIN_COUNTRY:
                if self.countryPanel:
                    self.countryPanel.onShow()
                    self.widget.selectSpritePanel.visible = False
            if tabName == TAB_MAIN_COLLECT:
                if self.collectPanel:
                    self.collectPanel.onShow()
