#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/actionDebugProxy.o
import BigWorld
from Scaleform import GfxValue
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst

class ActionDebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ActionDebugProxy, self).__init__(uiAdapter)
        self.bindType = 'actionDebug'
        self.modelMap = {'ClickAction': self.onClickAction,
         'getSearchAcResult': self.onGetSearchAcResult,
         'changeCheckBox': self.onChangeCheckBox,
         'switchWeapon': self.onSwitchWeapon}
        self.isTrans = False
        self.actionPair = None

    def getActionPair(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.actionPair:
            self.actionPair = BigWorld.player().model.actionNamePair()
        for actionId, actionName in self.actionPair:
            value = GfxValue(gbk2unicode(actionId + ':' + actionName))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getValue(self, key):
        if key == 'actionDebug.actionList':
            ar = self.getActionPair()
            return ar

    def onClickAction(self, *arg):
        actionId = arg[3][0].GetString()
        actionId = actionId.split(',')
        actionId = [ (item,
         None,
         self.isTrans,
         0) for item in actionId ]
        p = BigWorld.player()
        p.fashion.playActionSequence2(p.model, actionId)

    def onGetSearchAcResult(self, *arg):
        i = 0
        ar = self.movie.CreateArray()
        if not self.actionPair:
            self.actionPair = BigWorld.player().model.actionNamePair()
        subString = arg[3][0].GetString()
        if not subString:
            return self.getActionPair()
        for actionId, actionName in self.actionPair:
            sourceValue = actionId + ':' + actionName
            if sourceValue.find(subString) != -1:
                value = GfxValue(gbk2unicode(actionId + ':' + actionName))
                ar.SetElement(i, value)
                i = i + 1

        return ar

    def onChangeCheckBox(self, *arg):
        isTrans = arg[3][0].GetBool()
        self.isTrans = isTrans

    def showActionDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_ACTION)))

    def onSwitchWeapon(self, *arg):
        p = BigWorld.player()
        oldInCombat = p.inCombat
        p.inCombat = not p.inCombat
        p.set_inCombat(oldInCombat)
