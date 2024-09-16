#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generaldebugProxy.o
import BigWorld
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import DataProxy
from guis import uiConst

class GeneraldebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(GeneraldebugProxy, self).__init__(uiAdapter)
        self.bindType = 'generaldebug'
        self.modelMap = {'ClickFuncItem': self.onClickFuncItem,
         'registerGeneralDebug': self.onRegisterGeneralDebug,
         'getTextFieldTitle': self.onGetTextField,
         'changeValue': self.onChangeValue}
        self.info = None
        self.funcList = None
        self.textField = []
        self.func = []
        self.distance = []
        self.offset = 0

    def setFuncList(self, title, desc, option):
        self.title = title
        self.desc = desc
        self.funcList = option
        for i, item in enumerate(self.funcList):
            if item[2] == uiConst.SLIDER:
                self.textField.append(item[0][0])
                self.distance.append(item[0][2] - item[0][1])

    def onGetTextField(self, *arg):
        if self.textField is not None:
            return GfxValue(gbk2unicode(self.textField))
        else:
            return

    def onChangeValue(self, *arg):
        value = float(arg[3][0].GetNumber())
        func = self.funcList[self.index][1]
        if func is not None:
            func(value * self.distance[self.index - self.offset])

    def getValue(self, key):
        if self.funcList == None:
            return
        elif key == 'generaldebug.funclist':
            ar = self.movie.CreateArray()
            for i, item in enumerate(self.funcList):
                if item[2] == uiConst.WIDGET:
                    self.offset += 1
                    value = GfxValue(gbk2unicode(item[0]))
                elif item[2] == uiConst.SLIDER:
                    value = GfxValue(gbk2unicode(item[0][0]))
                ar.SetElement(i, value)

            return ar
        elif key == 'generaldebug.desc':
            ar = self.movie.CreateArray()
            title = GfxValue(gbk2unicode(self.title))
            desc = GfxValue(gbk2unicode(self.desc))
            ar.SetElement(0, title)
            ar.SetElement(1, desc)
            return ar
        else:
            return

    def onClickFuncItem(self, *arg):
        self.index = int(arg[3][0].GetNumber())
        if self.funcList[self.index][2] == uiConst.WIDGET:
            self.funcList[self.index][1]()
        elif self.funcList[self.index][2] == uiConst.SLIDER:
            self._silderProcess()

    def _silderProcess(self):
        if self.debugView is not None:
            self.debugView.Invoke('setSliderName', GfxValue(self.textField[self.index - self.offset]))

    def onSetGroup(self):
        p = BigWorld.player()
        if p.lockedId == 0:
            return
        en = BigWorld.entities.get(p.lockedId)
        if en.__class__.__name__ == 'Avatar':
            p.cell.applyBloc(en.roleName)

    def onSetCamp1(self):
        p = BigWorld.player()
        p.cell.setCamp(1)

    def onSetCamp2(self):
        p = BigWorld.player()
        p.cell.setCamp(2)

    def onRegisterGeneralDebug(self, *arg):
        self.debugView = arg[3][0]

    def showGeneralDebugView(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_GENERAL_DEBUG)))
