#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gmWidgetProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import utils
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy

class GmWidgetProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(GmWidgetProxy, self).__init__(uiAdapter)
        self.bindType = 'GMWidget'
        self.modelMap = {'registerGMWidget': self.onRegisterGMWidget,
         'ClickAction': self.onClickAction,
         'getSearchAcResult': self.onGetSearchAcResult}
        self.mc = None

    def onRegisterGMWidget(self, *arg):
        self.mc = arg[3][0]

    def getValue(self, key):
        gamelog.debug('hjx getValue')
        if key == 'GMWidget.GMList':
            i = 0
            ar = self.movie.CreateArray()
            for name in gameglobal.rds.gmMsg:
                value = GfxValue(gbk2unicode(name))
                ar.SetElement(i, value)
                i = i + 1

            return ar

    def onClickAction(self, *arg):
        gmString = arg[3][0].GetString()
        gmString = '$kindhelp ' + gmString.decode('utf-8').encode(utils.defaultEncoding())
        gamelog.debug('gmString:', gmString)
        BigWorld.player().cell.adminOnCell(gmString)

    def onGetSearchAcResult(self, *arg):
        gamelog.debug('gmhelp onGetSearchAcResult')
        i = 0
        ar = self.movie.CreateArray()
        subString = arg[3][0].GetString()
        if not subString:
            return None
        else:
            for name in gameglobal.rds.gmMsg:
                if name.find(subString) != -1:
                    value = GfxValue(gbk2unicode(name))
                    ar.SetElement(i, value)
                    i = i + 1

            return ar
