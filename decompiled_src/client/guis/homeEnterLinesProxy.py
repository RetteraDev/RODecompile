#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeEnterLinesProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
LINESNUM = 10

class HomeEnterLinesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HomeEnterLinesProxy, self).__init__(uiAdapter)
        self.modelMap = {'getLinesData': self.onGetLinesData,
         'getTitleName': self.onGetTitleName,
         'getPicData': self.onGetPicData,
         'getDescData': self.onGetDescData,
         'enterHome': self.onEnterHome}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_ENTERLINES, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOME_ENTERLINES:
            self.mediator = mediator

    def show(self, lines):
        self.linesData = lines
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_ENTERLINES)

    def clearWidget(self):
        self.mediator = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_ENTERLINES)

    def reset(self):
        self.linesData = []

    def appendLinesData(self, ret):
        for lineNo in self.linesData:
            info = {'lineNo': lineNo,
             'serverName': utils.getServerName(lineNo),
             'isShow': True}
            ret.append(info)

        while len(ret) < LINESNUM:
            info = {'isShow': False}
            ret.append(info)

    def onGetLinesData(self, *args):
        ret = []
        self.appendLinesData(ret)
        return uiUtils.array2GfxAarry(ret, True)

    def onGetTitleName(self, *args):
        return GfxValue(gbk2unicode(gameStrings.TEXT_HOMEENTERLINESPROXY_65))

    def onGetPicData(self, *args):
        return GfxValue(gbk2unicode('diGong/460.dds'))

    def onGetDescData(self, *args):
        return GfxValue(gbk2unicode(gameStrings.TEXT_HOMEENTERLINESPROXY_71))

    def onEnterHome(self, *args):
        lineNo = int(args[3][0].GetNumber())
        BigWorld.player().cell.enterHomeCommunity(lineNo)
        self.hide()
