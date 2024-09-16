#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommPushIconProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import keys
import uiConst
import uiUtils
from Scaleform import GfxValue
from ui import gbk2unicode
from appSetting import Obj as AppSettings
from uiProxy import UIProxy
from data import play_recomm_config_data as PRCD
PUSH_INCOMPLETE_ITEMS = '/playRecommend/autoPush'

class PlayRecommPushIconProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommPushIconProxy, self).__init__(uiAdapter)
        self.modelMap = {'openPlayRecomm': self.onOpenPlayRecomm,
         'quitPushIcon': self.onQuitPushIcon,
         'getConfigData': self.onGetConfigData,
         'openExpPursue': self.onOpenExpPursue}
        self.mediator = None
        self.pendingNotify = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PLAY_RECOMMEND_PUSH:
            self.mediator = mediator
            ret = {}
            ret['pushMessage'] = self.pendingNotify
            ret['tips'] = self.getTips()
            p = BigWorld.player()
            ret['isShowExpPursue'] = getattr(p, 'isShowPursueGuide', False) and gameglobal.rds.configData.get('enableExpPursueGuide', False)
            self.pendingNotify = False
            return uiUtils.dict2GfxDict(ret, True)

    def show(self, noPush = False):
        if self.mediator:
            return
        if not BigWorld.player():
            return
        if BigWorld.player().lv < PRCD.data.get('importantRecommMinLv', 20):
            return
        if not self.getShowPushIconSetting():
            return
        if noPush:
            self.pendingNotify = False
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PLAY_RECOMMEND_PUSH)

    def getTips(self):
        if gameglobal.rds.ui.playRecommActivation.checkCanGetAward():
            return gameStrings.TEXT_PLAYRECOMMPUSHICONPROXY_62
        else:
            return gameStrings.TEXT_PLAYRECOMMPUSHICONPROXY_64

    def notifyIncompleteItems(self):
        if not self.mediator:
            self.pendingNotify = True
        else:
            tips = self.getTips()
            self.mediator.Invoke('pushIncompleteItem', GfxValue(gbk2unicode(tips)))

    def cancelNotify(self):
        if not self.mediator:
            return
        self.mediator.Invoke('cancelNotify')

    def onOpenPlayRecomm(self, *arg):
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMMEND_PUSH)
        gameglobal.rds.ui.playRecomm.show()
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 7)

    def onQuitPushIcon(self, *arg):
        self.setShowPushIconSetting(False)
        self.hide()

    def onGetConfigData(self, *arg):
        ret = {}
        ret['quitable'] = PRCD.data.get('pushQuitable', False)
        return uiUtils.dict2GfxDict(ret, True)

    def onOpenExpPursue(self, *args):
        gameglobal.rds.ui.playRecomm.show(tabIdx=uiConst.PLAY_RECOMMV2_TAB_EXP_IDX)

    def refreshExpPursueVisible(self, *args):
        if not self.mediator:
            return
        p = BigWorld.player()
        isShow = getattr(p, 'isShowPursueGuide', False) and gameglobal.rds.configData.get('enableExpPursueGuide', False)
        self.mediator.Invoke('setExpPursueVisible', GfxValue(isShow))

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PLAY_RECOMMEND_PUSH)

    def getShowPushIconSetting(self):
        confKey = keys.SET_UI_INFO + PUSH_INCOMPLETE_ITEMS
        if gameglobal.rds.ui.playRecomm.autoShowPlayRecomm():
            AppSettings[confKey] = 1
        return AppSettings.get(confKey, 1)

    def setShowPushIconSetting(self, show):
        confKey = keys.SET_UI_INFO + PUSH_INCOMPLETE_ITEMS
        AppSettings[confKey] = int(show)
        AppSettings.save()
