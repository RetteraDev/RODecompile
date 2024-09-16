#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tinkerProxy.o
from Scaleform import GfxValue
import Tinker
import gameglobal
import gamelog
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import DataProxy
from guis import uiConst

class TinkerProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(TinkerProxy, self).__init__(uiAdapter)
        self.bindType = 'tinker'
        self.modelMap = {'registerTinkerOptionsPage': self.onRegisterTinkerOptionsPage,
         'tinkerProPageConfirmBtnClick': self.onConfirmBtnClick}

    def getValue(self, key):
        gamelog.debug('@hjx tinker#getValue:', key)
        self.desc = Tinker.Obj.desc
        if key == 'tinkerPro.list':
            ar = self.movie.CreateArray()
            self.entType = Tinker.Obj.entType
            self.property = Tinker.Obj.property
            i = 0
            for name in self.property:
                print 'creatorPro', name, self.desc, self.property
                data = self.movie.CreateArray()
                data.SetElement(0, GfxValue(gbk2unicode(name)))
                data.SetElement(1, GfxValue(gbk2unicode(self.desc[self.entType][name])))
                data.SetElement(2, GfxValue(gbk2unicode(str(self.property[name]))))
                ar.SetElement(i, data)
                i = i + 1

            return ar

    def onRegisterTinkerOptionsPage(self, *arg):
        self.handler = arg[3][0]

    def onConfirmBtnClick(self, *arg):
        gamelog.debug('@hjx tinker#onConfirmBtnClick')
        listdata = arg[3][0]
        i = 0
        for name in self.property:
            value = listdata.GetElement(i)
            newValue = unicode2gbk(value.GetString())
            print 'onConfirmBtnClick0', name, newValue
            _type = type(self.property[name])
            if _type == tuple:
                newValue = eval(newValue)
            if newValue != None or name == 'publishTag':
                self.property[name] = _type(newValue)
            i = i + 1

        gamelog.debug('@hjx tinker#onConfirmBtnClick:', self.property)
        print 'onConfirmBtnClick1', self.property
        Tinker.Obj.onEdited(self.property)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TINKER_PROPAGE)

    def _asTuple(self, mt, name):
        mt = mt.strip(')')
        mt = mt.strip('(')
        mt = mt.rstrip(',')
        eles = mt.split(',')
        ret = []
        t = type(self.property[name][0])
        for e in eles:
            ret.append(t(e))

        return tuple(ret)

    def addItem(self, str):
        self.handler.Invoke('addItem', GfxValue(gbk2unicode(str)))
        print 'addItem'

    def showTinkerProPage(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TINKER_PROPAGE)
