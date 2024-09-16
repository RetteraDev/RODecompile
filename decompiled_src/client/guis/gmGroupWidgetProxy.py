#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gmGroupWidgetProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import utils
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from guis.uiProxy import DataProxy

class GmGroupWidgetProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(GmGroupWidgetProxy, self).__init__(uiAdapter)
        self.bindType = 'GMGroupWidget'
        self.modelMap = {'registerGMGroupWidget': self.onRegisterGMGroupWidget,
         'ClickAction': self.onClickAction,
         'getSearchAcResult': self.onGetSearchAcResult}
        self.mc = None

    def onRegisterGMGroupWidget(self, *arg):
        self.mc = arg[3][0]
        gamelog.debug('onRegisterGMGroupWidget')

    def getValue(self, key):
        gamelog.debug('getValue')
        if key == 'GMGroupWidget.GMGroupList':
            i = 0
            ar = self.movie.CreateArray()
            for name in gameglobal.rds.gmGroupMsg:
                value = GfxValue(gbk2unicode(name))
                ar.SetElement(i, value)
                i = i + 1

            return ar

    def onClickAction(self, *arg):
        gmGroupString = arg[3][0].GetString().decode('utf-8').encode(utils.defaultEncoding())
        gamelog.debug('gmGroupString:', gmGroupString)
        sep = gmGroupString.split(':')
        gameglobal.rds.gmParameterOrder = '$' + sep[0] + ' '
        gamelog.debug('sep:', sep[0])
        BigWorld.player().cell.adminOnCell('$' + sep[0] + '$')

    def onGetSearchAcResult(self, *arg):
        gamelog.debug('gmhelp onGetSearchAcResult')
        i = 0
        ar = self.movie.CreateArray()
        subString = unicode2gbk(arg[3][0].GetString())
        if not subString:
            return None
        else:
            for name in gameglobal.rds.gmGroupMsg:
                if name.find(subString) != -1:
                    value = GfxValue(gbk2unicode(name))
                    ar.SetElement(i, value)
                    i = i + 1

            return ar
