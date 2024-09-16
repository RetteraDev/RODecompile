#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodPhaseProxy.o
import BigWorld
import gameglobal
import gamelog
import time
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import chickenFoodFactory
from guis import uiUtils
from asObject import ASUtils
from data import sys_config_data as SCD

class ChickenFoodPhaseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodPhaseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.disappearCallback = None
        self.reset()
        self.cfFactory = chickenFoodFactory.getInstance()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_PHASE:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_PHASE)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_PHASE)

    def reset(self):
        self.typeStr = ''
        if self.disappearCallback:
            ASUtils.cancelCallBack(self.disappearCallback)
            self.disappearCallback = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        if self.typeStr:
            self.widget.actionMc.gotoAndPlay(self.typeStr)
            sDict = SCD.data.get('chickenPhaseSound', {})
            soundId = sDict.get(self.typeStr, 0)
            gameglobal.rds.sound.playSound(soundId)
        if self.disappearCallback:
            ASUtils.cancelCallBack(self.disappearCallback)
            self.disappearCallback = None
        self.disappearCallback = ASUtils.callbackAtFrame(self.widget.actionMc.txtMc, 75, self.disappearCB)

    def disappearCB(self, *arg):
        if self.hasBaseData():
            self.hide()

    def showActionByAi(self, typeStr):
        self.typeStr = typeStr
        if self.widget:
            self.initUI()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_PHASE)

    def hasBaseData(self):
        if self.cfFactory and self.typeStr and self.widget:
            return True
        else:
            return False
