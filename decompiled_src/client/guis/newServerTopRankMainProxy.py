#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServerTopRankMainProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
from uiTabProxy import UITabProxy
TAB_BTN_NUM_MAX = 1
TAB_ONE_IDX = 0
PRIVIEGE_DAY_TO_SECOND = 86400

class NewServerTopRankMainProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(NewServerTopRankMainProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_SERVER_TOP_MAIN, self.hide)

    def reset(self):
        super(NewServerTopRankMainProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NEW_SERVER_TOP_MAIN:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(NewServerTopRankMainProxy, self).clearWidget()
        self.widget = None
        self.cleanTimer()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEW_SERVER_TOP_MAIN)

    def _getTabList(self):
        return [{'tabIdx': TAB_ONE_IDX,
          'tabName': 'tab0',
          'view': 'NewServerTopRankTab0Widget',
          'proxy': 'newServerTopRankGuild'}]

    def show(self):
        if not self.checkOpen():
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEW_SERVER_TOP_MAIN)

    def checkOpen(self):
        if self.checkGuildTab():
            return True
        else:
            return False

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        p = BigWorld.player()
        p.newServerRankType = None
        self.refreshAllTab()

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def onTabChanged(self, *args):
        super(NewServerTopRankMainProxy, self).onTabChanged(*args)
        self.refreshInfo()
        currentTabIndex = int(args[3][0].GetNumber())
        self.widget.helpBtn.helpKey = 351 + currentTabIndex

    def updateInfo(self):
        if not self.checkOpen():
            self.hide()

    def getFirstTabIndex(self):
        for i in range(0, 4):
            tab = getattr(self.widget, 'tab%s' % i)
            if tab.visible:
                return i

        return -1

    def refreshAllTab(self):
        if not self.checkOpen():
            self.hide()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        for i in range(0, TAB_BTN_NUM_MAX):
            tab = getattr(self.widget, 'tab%s' % i)
            isVisible = self.getTabCheckByIndex(i)
            tab.visible = isVisible

        if self.showTabIndex == -1:
            self.widget.setTabIndex(self.getFirstTabIndex())
            self.showTabIndex = self.getFirstTabIndex()
        elif not self.getTabCheckByIndex(self.showTabIndex):
            self.widget.setTabIndex(self.getFirstTabIndex())
            self.showTabIndex = self.getFirstTabIndex()
        self.timer = BigWorld.callback(1, self.refreshAllTab)

    def getTabCheckByIndex(self, index):
        isVisible = False
        if index == 0:
            isVisible = self.checkGuildTab()
        return isVisible

    def checkGuildTab(self):
        if not gameglobal.rds.configData.get('enableNewServerGuildPrestige', False):
            return False
        configData = utils.getNSPrestigeActivityConfigData()
        if configData.get('fromMergeTime', 0) == 1:
            serverOpenTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0) or utils.getServerOpenTime()
            stage = utils.getGuildPrestigeEnableStageAndOneDay(serverOpenTime)
            enableTime = configData.get('enableTime%s' % stage)
            if not enableTime:
                return False
            periodType, nWeeksOffset, nLastWeeks = enableTime
            tStart, tEnd = utils.calcTimeDuration(periodType, serverOpenTime, nWeeksOffset, nLastWeeks)
            if tStart <= utils.getNow() <= tEnd + PRIVIEGE_DAY_TO_SECOND:
                return True
            else:
                return False
        return False

    def cleanTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def _onTab0Click(self, *args):
        self.showTabIndex = 0
