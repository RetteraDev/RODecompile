#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommTopPushProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import uiConst
import events
import keys
from uiProxy import UIProxy
from guis.asObject import ASUtils
from appSetting import Obj as AppSettings
PUSH_INCOMPLETE_ITEMS = '/playRecommend/autoPush'
from data import play_recomm_config_data as PRCD

class PlayRecommTopPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommTopPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.pendingNotify = False

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PLAY_RECOMM_TOP_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PLAY_RECOMM_TOP_PUSH)

    def show(self, noPush = False):
        gamelog.info('@jbx:playRecommTopPush.show', noPush)
        if not self.widget:
            if not self.getShowPushIconSetting():
                return
            if noPush:
                self.pendingNotify = False
            if BigWorld.player().lv < PRCD.data.get('importantRecommMinLv', 20):
                return
            self.uiAdapter.loadWidget(uiConst.WIDGET_PLAY_RECOMM_TOP_PUSH)

    def initUI(self):
        pass

    def getTips(self):
        if gameglobal.rds.ui.playRecommActivation.checkCanGetAward():
            return gameStrings.TEXT_PLAYRECOMMPUSHICONPROXY_62
        else:
            return gameStrings.TEXT_PLAYRECOMMPUSHICONPROXY_64

    def refreshInfo(self):
        if not self.widget:
            return
        gamelog.info('@jbx:refreshInfo')
        if self.pendingNotify:
            if 'expand' not in self.widget.currentFrameLabel:
                self.widget.gotoAndPlay('expand')
                ASUtils.callbackAtFrame(self.widget, 15, self.setTipsInfo)
            else:
                self.setTipsInfo()
        elif 'normal' not in self.widget.currentFrameLabel:
            self.widget.gotoAndPlay('normal')
            self.widget.normalBtn.addEventListener(events.BUTTON_CLICK, self.handleNormalClick, False, 0, True)

    def cancelNotify(self):
        self.pendingNotify = False
        self.refreshInfo()

    def notifyIncompleteItems(self):
        self.pendingNotify = True
        if not self.widget:
            self.show()
        else:
            if gameglobal.rds.ui.playRecomm.mediator:
                return
            self.refreshInfo()

    def setTipsInfo(self, *args):
        (gamelog.info('setTipsInfo'), self.widget.expandBtn)
        if self.widget and self.widget.expandBtn:
            tips = self.getTips()
            self.widget.expandBtn.label = tips
            if self.widget.textMc:
                self.widget.textMc.txtDesc.htmlText = tips
            self.widget.expandBtn.addEventListener(events.BUTTON_CLICK, self.handleExpandClick, False, 0, True)

    def getShowPushIconSetting(self):
        confKey = keys.SET_UI_INFO + PUSH_INCOMPLETE_ITEMS
        if gameglobal.rds.ui.playRecomm.autoShowPlayRecomm():
            AppSettings[confKey] = 1
        return AppSettings.get(confKey, 1)

    def handleNormalClick(self, *args):
        gamelog.info('@jbx:handleNormalClick')
        self.doOpenPlayRecomm()

    def handleExpandClick(self, *args):
        gamelog.info('@jbx:handleExpandClick')
        self.doOpenPlayRecomm()

    def doOpenPlayRecomm(self):
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM_TOP_PUSH)
        gameglobal.rds.ui.playRecomm.show()
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM_TOP_PUSH * 100 + 7)
        self.pendingNotify = False
        self.refreshInfo()

    def setShowPushIconSetting(self, show):
        confKey = keys.SET_UI_INFO + PUSH_INCOMPLETE_ITEMS
        AppSettings[confKey] = int(show)
        AppSettings.save()
