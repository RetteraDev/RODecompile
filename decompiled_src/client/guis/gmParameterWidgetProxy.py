#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gmParameterWidgetProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import utils
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy

class GmParameterWidgetProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(GmParameterWidgetProxy, self).__init__(uiAdapter)
        self.bindType = 'GMParameterWidget'
        self.modelMap = {'submitGMText': self.onSubmitGMText}

    def onSubmitGMText(self, *arg):
        subString = arg[3][0].GetString()
        BigWorld.player().cell.adminOnCell(gameglobal.rds.gmParameterOrder + subString.decode('utf-8').encode(utils.defaultEncoding()))
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GMPARAMETERWIDGET)

    def getValue(self, key):
        gamelog.debug('Parameter getValue')
        if key == 'GMParameterWidget.GMList':
            ar = self.movie.CreateArray()
            i = 0
            for j, name in enumerate(gameglobal.rds.gmParameterMsg):
                sep = name.splitlines()
                for item in sep:
                    value = GfxValue(gbk2unicode(item))
                    ar.SetElement(i, value)
                    i = i + 1

                if j < len(gameglobal.rds.gmParameterMsg) - 1:
                    ar.SetElement(i, GfxValue('----------------------------------------------------------'))
                    i += 1

            return ar
