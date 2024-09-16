#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qinggongWingTutorialProxy.o
import BigWorld
import gameglobal
import uiConst
from helpers import cgPlayer
from uiTabProxy import UITabProxy
from data import sys_config_data as SCD
TAB_QING_GONG_INDEX = 0
TAB_WING_INDEX = 1

class QinggongWingTutorialProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(QinggongWingTutorialProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.cgPlayer = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_QING_GONG_WING_TUTORIAL, self.hide)

    def reset(self):
        super(QinggongWingTutorialProxy, self).reset()
        self.endMovie()
        self.isMoviePlaying = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QING_GONG_WING_TUTORIAL:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(QinggongWingTutorialProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QING_GONG_WING_TUTORIAL)

    def _getTabList(self):
        return [{'tabIdx': TAB_QING_GONG_INDEX,
          'tabName': 'tabBtn0',
          'view': 'QinggongWingTutorial_MoviePanelMC_0',
          'pos': (27, 95)}, {'tabIdx': TAB_WING_INDEX,
          'tabName': 'tabBtn1',
          'view': 'QinggongWingTutorial_MoviePanelMC_1',
          'pos': (27, 95)}]

    def show(self, showTabIndex = -1):
        if showTabIndex == TAB_WING_INDEX and BigWorld.player().lv < SCD.data.get('minTutorialWingTabEnableLevel', 29):
            msg = SCD.data.get('wingTutorialUnableSpriteMsg', '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            return
        if not self.widget:
            self.showTabIndex = showTabIndex
            self.uiAdapter.loadWidget(uiConst.WIDGET_QING_GONG_WING_TUTORIAL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        if self.showTabIndex == -1:
            if BigWorld.player().lv >= SCD.data.get('minTutorialWingTabEnableLevel', 29):
                self.widget.setTabIndex(TAB_WING_INDEX)
        else:
            self.widget.setTabIndex(self.showTabIndex)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentView:
            self.currentView.playBtn.visible = not self.isMoviePlaying
            self.currentView.playCanvas.visible = not self.isMoviePlaying
        if BigWorld.player().lv >= SCD.data.get('qinggongWingTutorialEnableLevel', {}).get('wing', 29):
            self.setTabVisible(TAB_WING_INDEX, True, False)
        else:
            self.setTabVisible(TAB_WING_INDEX, False, False)

    def onTabChanged(self, *args):
        self.endMovie()
        super(QinggongWingTutorialProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def endMovie(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None
        self.isMoviePlaying = False

    def onMovieEnd(self):
        self.isMoviePlaying = False
        self.refreshInfo()

    def _onPlayBtnClick(self, e):
        self.isMoviePlaying = True
        self.refreshInfo()
        self.playMovie()

    def playMovie(self):
        config = {'position': (1, 1, 1.0),
         'w': 890,
         'h': 502,
         'loop': False,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/QinggongWingTutorialWidget' + self.uiAdapter.getUIExt(), 'QinggongWingTutorial_movieLoader_%d' % self.currentTabIndex, 890, 502)
        movieName = SCD.data.get('qinggongWingTutorialMovieNames', {}).get(self.currentTabIndex, None)
        if movieName:
            self.cgPlayer.playMovie(movieName, config)
