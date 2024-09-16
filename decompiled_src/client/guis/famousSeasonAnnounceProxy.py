#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousSeasonAnnounceProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from data import famous_general_config_data as FGCD

class FamousSeasonAnnounceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousSeasonAnnounceProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_SEASON_ANNOUNCE_INTRO, self.hidePanel)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.content.text = FGCD.data.get('seasonAnnounceContent', '')
        reward = FGCD.data.get('seasonAnnounceReward', ())
        rankReward = FGCD.data.get('seasonAnnounceRankReward', ())
        for i in xrange(0, len(reward)):
            self.widget.getChildByName('rewardLv%d' % i).htmlText = reward[i].get('lv', '')
            self.widget.getChildByName('reward%d' % i).htmlText = reward[i].get('rewardTxt', '')

        for i in xrange(0, len(rankReward)):
            self.widget.getChildByName('rankRewardLv%d' % i).htmlText = rankReward[i].get('lv', '')
            self.widget.getChildByName('rankReward%d' % i).htmlText = rankReward[i].get('rewardTxt', '')

        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)

    def show(self):
        if self.widget:
            self.clearWidget()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_SEASON_ANNOUNCE_INTRO)

    def hidePanel(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_SEASON_ANNOUNCE_INTRO)

    def handleHidePanel(self, *args):
        self.clearWidget()
