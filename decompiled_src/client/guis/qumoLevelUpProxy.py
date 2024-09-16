#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qumoLevelUpProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import qumo_lv_data as QLD
from data import famous_general_lv_data as FGLD

class QumoLevelUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QumoLevelUpProxy, self).__init__(uiAdapter)
        self.qumoMediator = None
        self.jingjieMediator = None
        self.famousMediator = None
        self.maxLevel = 10

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QUMO_LEVELUP:
            self.qumoMediator = mediator
            return self._getQumoData()
        if widgetId == uiConst.WIDGET_JINGJIE_LEVELUP:
            self.jingjieMediator = mediator
            return self._getJingjieData()
        if widgetId == uiConst.WIDGET_JUNJIE_LEVELUP:
            self.junjieMediator = mediator
            return self._getJunjieData()
        if widgetId == uiConst.WIDGET_FAMOUS_LEVEL_UP:
            self.famousMediator = mediator
            return self._getFamousData()

    def showQumoPop(self):
        if BigWorld.player().qumoLv > 0:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QUMO_LEVELUP)

    def showJingjiePop(self):
        if BigWorld.player().jingJie > 0:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JINGJIE_LEVELUP)

    def showJunjiePop(self):
        if BigWorld.player().junJieLv > 0:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JUNJIE_LEVELUP)

    def showFamousPop(self):
        if BigWorld.player().famousGeneralLv > 0:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_LEVEL_UP)

    def _getQumoData(self, *arg):
        p = BigWorld.player()
        qumoLv = p.qumoLv
        ret = {}
        ret['maxLevel'] = self.maxLevel
        ret['level'] = qumoLv
        ret['title'] = QLD.data.get(qumoLv, {}).get('name', gameStrings.TEXT_QUMOLEVELUPPROXY_58)
        return uiUtils.dict2GfxDict(ret, True)

    def _getJingjieData(self, *arg):
        p = BigWorld.player()
        jingJieLv = p.jingJie
        ret = {}
        ret['level'] = jingJieLv
        return uiUtils.dict2GfxDict(ret, True)

    def _getJunjieData(self, *arg):
        p = BigWorld.player()
        junJieLv = p.junJieLv
        ret = {}
        ret['level'] = junJieLv
        return uiUtils.dict2GfxDict(ret, True)

    def _getFamousData(self, *arg):
        p = BigWorld.player()
        famousLv = p.famousGeneralLv
        ret = {}
        ret['level'] = famousLv
        if FGLD.data.get(famousLv, 'pskills'):
            ret['isZhizun'] = 0
        else:
            ret['isZhizun'] = 1
        return uiUtils.dict2GfxDict(ret, True)

    def _asWidgetClose(self, widgetId, multiID):
        super(self.__class__, self)._asWidgetClose(widgetId, multiID)
        if widgetId == uiConst.WIDGET_QUMO_LEVELUP:
            self.qumoMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUMO_LEVELUP)
        if widgetId == uiConst.WIDGET_JINGJIE_LEVELUP:
            self.jingjieMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JINGJIE_LEVELUP)
        if widgetId == uiConst.WIDGET_JUNJIE_LEVELUP:
            self.junjieMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JUNJIE_LEVELUP)
        if widgetId == uiConst.WIDGET_FAMOUS_LEVEL_UP:
            self.famousMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_LEVEL_UP)
