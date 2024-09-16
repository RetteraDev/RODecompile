#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameGuideProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
from uiTabProxy import UITabProxy
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
TAB_RULE_INDEX = 0
TAB_GUIDE_INDEX = 1
TAB_OTHER_INDEX = 2
TAB_NUM = 3
BOSS_STAGE_FAKE = 0
BOSS_STAGE_BOSS1 = 1
BOSS_STAGE_BOSS2 = 2
BOSS_STAGE_GRAVE = 3
BOSS_STAGE_GRAVE_END = 4
STAGE_FRAME_MAP = [0,
 1,
 1,
 2,
 2]

class MapGameGuideProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(MapGameGuideProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_GUIDE, self.hide)

    def reset(self):
        super(MapGameGuideProxy, self).reset()
        self.stage = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_GUIDE:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(MapGameGuideProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_GUIDE)

    def _getTabList(self):
        return [{'tabIdx': TAB_RULE_INDEX,
          'tabName': 'tab0',
          'view': 'MapGameGuide_ruleMc',
          'pos': (26, 102)}, {'tabIdx': TAB_GUIDE_INDEX,
          'tabName': 'tab1',
          'view': 'MapGameGuide_guideMc',
          'pos': (26, 102)}, {'tabIdx': TAB_OTHER_INDEX,
          'tabName': 'tab2',
          'view': 'MapGameGuide_otherMc',
          'pos': (26, 102)}]

    def show(self):
        if not gameglobal.rds.configData.get('enableMapGame', False):
            return
        if not self.widget:
            self.showTabIndex = TAB_RULE_INDEX
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_GUIDE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        tabTitle = MGCD.data.get('mapGameGuideTabTitle', '')
        if tabTitle and len(tabTitle) == TAB_NUM:
            for i in xrange(TAB_NUM):
                tabMc = self.widget.getChildByName('tab%d' % i)
                tabMc.label = tabTitle[i]

        self.initTabUI()
        self.widget.setTabIndex(self.showTabIndex)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.stage = gameglobal.rds.ui.mapGameMapV2.getStage()
        self.widget.title.tf.text = gameglobal.rds.ui.mapGameMapV2.getTitle()
        self.changeModeGuide()
        self.widget.swapPanelToFront()

    def onTabChanged(self, *args):
        super(MapGameGuideProxy, self).onTabChanged(*args)
        if not self.widget:
            return
        if not self.currentView:
            return
        self.changeModeGuide()
        if self.currentTabIndex == TAB_RULE_INDEX:
            if self.currentView.canvas.rule:
                self.currentView.canvas.rule.htmlText = MGCD.data.get('MAP_GAME_GUIDE_RULE', '')
        elif self.currentTabIndex == TAB_OTHER_INDEX:
            if self.currentView.canvas.sprite:
                self.currentView.canvas.sprite.htmlText = MGCD.data.get('MAP_GAME_GUIDE_SPRITE', '')
            if self.currentView.canvas.power:
                self.currentView.canvas.power.htmlText = MGCD.data.get('MAP_GAME_GUIDE_POWER', '')

    def changeModeGuide(self):
        mainMc = self.currentView.canvas.mainMc
        if MGCD.data.get('isSecondBossMode', False) and mainMc:
            mainMc.gotoAndStop('stage%d' % STAGE_FRAME_MAP[self.stage])
