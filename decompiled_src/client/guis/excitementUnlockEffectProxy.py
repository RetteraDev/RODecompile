#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/excitementUnlockEffectProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import Tweener
from asObject import TipManager
from asObject import ASObject
from gameStrings import gameStrings
from callbackHelper import Functor
from data import excitement_data as ED
from data import quest_data as QD
from cdata import excitement_quest_list_data as EQLD
from data import play_recomm_config_data as PRCD
NOR_COLOR = '#E5CFA1'
COM_COLOR = '#7ACC29'
INIT_MAINMC_WIDTH = 268
INIT_MAINMC_HEIGHT = 146
INIT_MAINMC_X = 0
INIT_MAINMC_Y = 0
FLY_OFFSET_X_1 = -97
FLY_OFFSET_X_2 = -112
FLY_OFFSET_Y = -137

class ExcitementUnlockEffectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExcitementUnlockEffectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.appearCallback = None
        self.disappearCallback = None
        self.exId = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EXCITEMENT_UNLOCK_EFFECT:
            self.widget = widget
            self.initUI()

    def show(self, exId):
        self.exId = exId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXCITEMENT_UNLOCK_EFFECT)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXCITEMENT_UNLOCK_EFFECT)
        self.widget = None

    def reset(self):
        self.exId = None
        if self.appearCallback:
            ASUtils.cancelCallBack(self.appearCallback)
            self.appearCallback = None
        if self.disappearCallback:
            ASUtils.cancelCallBack(self.disappearCallback)
            self.disappearCallback = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.visible = False
        self.widget.addEventListener(events.EVENT_RESIZE, self.handleResize, False, 0, True)
        self.refreshInfo()

    def handleResize(self, *args):
        _x, _y = ASUtils.global2Local(self.widget, 0, 0)
        self.widget.bg.x = _x
        self.widget.bg.y = _y
        self.widget.bg.width = self.widget.stage.stageWidth + 15
        self.widget.bg.height = self.widget.stage.stageHeight + 2

    @ui.callAfterTime()
    def refreshInfo(self):
        if self.hasBaseData():
            self.playAppear()

    def hasBaseData(self):
        if self.widget and self.exId:
            return True
        else:
            return False

    def loadIcon(self, mc):
        mc.fitSize = True
        icon = ED.data.get(self.exId, {}).get('icon', None)
        if icon:
            mc.visible = True
            mc.loadImage(uiConst.EXCITEMENT_IMPAGE_PATH % icon)
        else:
            mc.visible = False

    def playAppear(self):
        if self.hasBaseData():
            self.widget.visible = True
            gameglobal.rds.sound.playSound(39)
            self.widget.mainMc.gotoAndPlay('appear')
            self.handleResize()
            self.loadIcon(self.widget.mainMc.iconMc.insideIconMc.innerIcon.canvas)
            _type = ED.data.get(self.exId, {}).get('type', 0)
            name = ED.data.get(self.exId, {}).get('name', 0)
            typeTxt = ''
            if _type == uiConst.EXCITEMENT_OPEN_TYPE_FUNC:
                typeTxt = gameStrings.ECXITEMENT_OPEN_TYPE_1
            elif _type == uiConst.EXCITEMENT_OPEN_TYPE_PLAY:
                typeTxt = gameStrings.ECXITEMENT_OPEN_TYPE_2
            self.widget.mainMc.iconMc.typeTxt.contentTxt.text = typeTxt
            self.widget.mainMc.iconMc.nameTxt.contentTxt.text = name
            if self.appearCallback:
                ASUtils.cancelCallBack(self.appearCallback)
                self.appearCallback = None
            self.appearCallback = ASUtils.callbackAtFrame(self.widget.mainMc.iconMc, 60, self.appearCB)

    def appearCB(self, *arg):
        if self.hasBaseData():
            self.flyToPos()
        else:
            self.disappearCB()

    def initMainMc(self):
        self.widget.mainMc.x = INIT_MAINMC_X
        self.widget.mainMc.y = INIT_MAINMC_Y
        self.widget.mainMc.width = INIT_MAINMC_WIDTH
        self.widget.mainMc.height = INIT_MAINMC_HEIGHT

    def flyToPos(self):
        self.initMainMc()
        _x, _y, cantFly = self.calcFlyPos()
        if cantFly:
            self.disappearCB()
        else:
            Tweener.addTween(self.widget.mainMc, {'x': _x,
             'y': _y,
             'width': self.widget.mainMc.width / 2,
             'height': self.widget.mainMc.height / 2,
             'time': 0.7,
             'transition': 'easeinsine',
             'onComplete': self.flyCompleted})

    def calcFlyPos(self):
        flyTo = ED.data.get(self.exId, {}).get('flyTo', (0, 0))
        _type, _param = flyTo
        tempWidget = None
        offsetWidget = None
        _x, _y = (0, 0)
        cantFly = True
        if _type == uiConst.EXCITEMENT_EFFECT_FLY_TYPE_PLAY:
            tempWidget = self.getPlayRecommPushIcon()
            if tempWidget != None:
                _x, _y = ASUtils.local2Global(tempWidget, 0, 0)
                _x, _y = ASUtils.global2Local(self.widget, _x, _y)
                _x, _y = _x + FLY_OFFSET_X_1, _y + FLY_OFFSET_Y
                cantFly = False
        elif _type == uiConst.EXCITEMENT_EFFECT_FLY_TYPE_SYSBTN:
            tempWidget = self.getSysBtnIcon()
            offsetWidget = getattr(tempWidget, _param + 'Btn', None)
            if tempWidget != None and offsetWidget != None:
                _x, _y = ASUtils.local2Global(tempWidget, offsetWidget.x, offsetWidget.y)
                _x, _y = ASUtils.global2Local(self.widget, _x, _y)
                _x, _y = _x + FLY_OFFSET_X_2, _y + FLY_OFFSET_Y
                cantFly = False
        return (_x, _y, cantFly)

    def flyCompleted(self, *arg):
        if self.hasBaseData():
            self.widget.mainMc.gotoAndPlay('disappear')
            self.loadIcon(self.widget.mainMc.iconMc.insideIconMc.canvas)
            if self.disappearCallback:
                ASUtils.cancelCallBack(self.disappearCallback)
                self.disappearCallback = None
            self.disappearCallback = ASUtils.callbackAtFrame(self.widget.mainMc.iconMc, 16, self.disappearCB)

    def disappearCB(self, *arg):
        if self.hasBaseData():
            tempWidget = self.getSysBtnIcon()
            flyTo = ED.data.get(self.exId, {}).get('flyTo', (0, 0))
            _type, _param = flyTo
            blinkWidget = None
            if _type == uiConst.EXCITEMENT_EFFECT_FLY_TYPE_SYSBTN:
                blinkWidget = getattr(tempWidget, _param + 'BlinkEx', None)
            if tempWidget != None and blinkWidget != None:
                blinkWidget.visible = True
                blinkWidget.gotoAndPlay('begin')
            self.openUI()
            gameglobal.rds.tutorial.onExcitementActivate(self.exId)
            self.delayItemPushUseUI()
            self.hide()

    def getPlayRecommPushIcon(self):
        if self.uiAdapter.playRecommPushIcon.mediator:
            return ASObject(self.uiAdapter.playRecommPushIcon.mediator.Invoke('getWidget'))
        else:
            return self.uiAdapter.playRecommTopPush.widget

    def getSysBtnIcon(self):
        if self.uiAdapter.systemButton.mediator:
            return ASObject(self.uiAdapter.systemButton.mediator.Invoke('getWidget'))
        else:
            return None

    def openUI(self):
        txtCmd = ED.data.get(self.exId, {}).get('pushUI', '')
        if txtCmd:
            try:
                eval('gameglobal.rds.ui.' + txtCmd)
            except:
                pass

    def delayItemPushUseUI(self):
        if self.uiAdapter.itemPushUse.mediator:
            self.uiAdapter.itemPushUse.startTimeOut()
