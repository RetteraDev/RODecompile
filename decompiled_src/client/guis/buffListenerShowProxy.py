#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/buffListenerShowProxy.o
import BigWorld
import const
import utils
import math
import gameglobal
import uiConst
import uiUtils
import events
import tipUtils
import gameconfigCommon
from asObject import Tweener
from asObject import TipManager
from asObject import ASUtils
from uiProxy import UIProxy
from data import conditional_prop_data as CPD
SLOT_NUM = 12
CANVAS_OFFSET_X = 36
CANVAS_OFFSET_Y = 36
CANVAS_COLUMN = 6
N_A_TIME = -100

class BuffListenerShowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BuffListenerShowProxy, self).__init__(uiAdapter)
        self.widget = None
        self.updateCallBack = None
        self.reset()

    def reset(self):
        self.curShowCardState = {}
        self.curOldCondPropStartTime = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BUFF_LISTENER_SHOW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BUFF_LISTENER_SHOW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BUFF_LISTENER_SHOW)

    def initUI(self):
        self.widget.settingBtn.visible = False
        self.widget.bg.visible = False
        self.widget.addEventListener(events.MOUSE_ROLL_OVER, self.handleMouseRollOver, False, 0, True)
        self.widget.addEventListener(events.MOUSE_ROLL_OUT, self.handleMouseRollOut, False, 0, True)
        self.widget.settingBtn.addEventListener(events.BUTTON_CLICK, self.handleSettingBtnClick, False, 0, True)
        for i in xrange(SLOT_NUM):
            buffMc = getattr(self.widget.canvas, 'slot' + str(i), None)
            if buffMc:
                self.resetBuffMc(buffMc)

        self.startUpdateTimer()

    def startUpdateTimer(self):
        self.cancelUpdateCallBack()
        self.updateCallBack = BigWorld.callback(1, self.startUpdateTimer)
        self.updateTimer()

    def cancelUpdateCallBack(self):
        if self.updateCallBack:
            BigWorld.cancelCallback(self.updateCallBack)
            self.updateCallBack = None

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        self.widget.visible = gameconfigCommon.enableBuffListener() and p.buffListenerConfig.get('buffListenerEnable', 0)
        if not self.widget.visible:
            return
        self.resetInvalidBuffMc()
        self.refreshCardBuff()
        self.updateTimer()
        self.relayout()

    def updateTimer(self):
        if not self.hasBaseData():
            return
        self.calcBuffTime()

    def calcBuffTime(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        for k, v in self.curShowCardState.iteritems():
            if not v:
                continue
            slotData = v.slot1.data
            totalTime = slotData.totalTime
            startTime = slotData.startTime
            cd = slotData.cd
            cdLeftTime = max(startTime + cd - utils.getNow(), 0)
            duringLeftTime = max(startTime + totalTime - utils.getNow(), 0)
            if totalTime == N_A_TIME:
                v.slot1.slot.timer.textField.visible = False
            elif duringLeftTime <= 0:
                v.slot1.slot.timer.textField.visible = False
            else:
                v.slot1.slot.timer.textField.visible = True
                v.slot1.slot.timer.textField.text = v.slot1.formatTime(duringLeftTime)
            if cdLeftTime > 0 and cd > 0 and not v.slot1.slot.timer.textField.visible:
                v.slot1.slot.coolDownTime.visible = True
                v.slot1.slot.coolDown.visible = True
                v.slot1.slot.coolDownTime.text = v.slot1.formatTime(cdLeftTime)
                frame = math.floor((v.slot1.slot.coolDown.totalFrames - 2) * min(float(cd - cdLeftTime) / cd, 1)) + 3
                v.slot1.slot.coolDown.gotoAndStop(frame)
            else:
                v.slot1.slot.coolDownTime.visible = False
                v.slot1.slot.coolDown.visible = False

    def refreshCardBuff(self):
        p = BigWorld.player()
        listenerCardDict = p.buffListenerConfig.get('buffConfig', {}).get(const.LISTENER_TYPE_CARD_CONDITION, {})
        num = 0
        for k, v in p.listeningBuffShowData.iteritems():
            if not v.get('bListener', 0):
                continue
            if num >= const.BUFF_LISTENER_NUM_MAX:
                continue
            buffMc = self.getBuffMc(const.LISTENER_TYPE_CARD_CONDITION, k)
            if buffMc:
                condPropData = CPD.data.get(k, {})
                validBuff = bool(p.conditionalPropTips.get(k, ()))
                buffMc.visible = True
                buffMc.slot1.slot.timer.textField.visible = False
                buffMc.slot1.slot.coolDownTime.visible = False
                buffMc.slot1.slot.coolDown.visible = False
                conPropType = condPropData.get('conPropType', 1)
                iconPath = v.get('icon', 0)
                if not iconPath:
                    if conPropType == const.COND_PROP_TYPE_ATTACK:
                        iconPath = uiConst.BUFF_LISTENER_DEFAULT_ICON_1
                    elif conPropType == const.COND_PROP_TYPE_DEFENSE:
                        iconPath = uiConst.BUFF_LISTENER_DEFAULT_ICON_2
                iconPath = uiConst.MACRO_COMMON_ICON % iconPath
                lastTime = condPropData.get('lastTime', -100)
                cd = condPropData.get('cd', 0)
                startTime = p.conditionalPropTime.get(k, 0)
                if startTime:
                    self.curOldCondPropStartTime[k] = startTime
                remaintime = max(startTime + lastTime - utils.getNow(), 0)
                bData = {'iconPath': iconPath,
                 'timer': remaintime,
                 'totalTime': lastTime,
                 'startTime': self.curOldCondPropStartTime.get(k, 0),
                 'cd': cd,
                 'count': 1}
                buffMc.listenerType = const.LISTENER_TYPE_CARD_CONDITION
                buffMc.listenerId = k
                buffMc.slot1.setItemSlotData(bData)
                buffMc.slot1.validateNow()
                propVal = v.get('propVal', 0)
                desc = self.uiAdapter.buffListenerSetting.formatCondStr(k, propVal)
                TipManager.addTip(buffMc.slot1, desc, tipUtils.TYPE_DEFAULT_BLACK)
                if validBuff:
                    buffMc.slot1.slot.dark.visible = False
                else:
                    buffMc.slot1.slot.dark.visible = True
                self.curShowCardState[k] = buffMc
                num += 1

    def resetInvalidBuffMc(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        invalidIds = []
        delArr = []
        for k, v in self.curShowCardState.iteritems():
            invalid = False
            needDel = False
            if not v:
                continue
            if v.listenerType == const.LISTENER_TYPE_CARD_CONDITION:
                if v.listenerId not in p.conditionalPropTips:
                    invalid = True
            if invalid:
                self.resetBuffMc(v)
            bListener = p.listeningBuffShowData.get(v.listenerId, {}).get('bListener', 0)
            if not bListener:
                needDel = True
            if needDel:
                delArr.append(k)

        for listenerId in delArr:
            if listenerId in self.curShowCardState:
                self.resetBuffMc(self.curShowCardState[listenerId])
                del self.curShowCardState[listenerId]

    def getBuffMc(self, listenerType, listenerId):
        buffMc = None
        if listenerType == const.LISTENER_TYPE_CARD_CONDITION:
            buffMc = self.curShowCardState.get(listenerId, None)
        if not buffMc:
            for i in xrange(SLOT_NUM):
                buffSlot = getattr(self.widget.canvas, 'slot' + str(i), None)
                if not self.bUsedBuffMc(buffSlot) and buffSlot:
                    buffMc = buffSlot

        return buffMc

    def calcBuffMcKey(self, listenerType, id):
        return ''.join((str(listenerType), '_', str(id)))

    def parseBuffMcKey(self, key):
        return key.split('_')

    def resetBuffMc(self, buffMc):
        if buffMc:
            buffMc.visible = False

    def bUsedBuffMc(self, buffMc):
        if buffMc in self.curShowCardState.values():
            return True
        return False

    def relayout(self):
        if not self.hasBaseData():
            return
        i = 0
        for k, v in self.curShowCardState.iteritems():
            v.x = i % CANVAS_COLUMN * CANVAS_OFFSET_X
            v.y = i / CANVAS_COLUMN * CANVAS_OFFSET_Y
            i += 1

        p = BigWorld.player()
        buffListenerConfig = p.buffListenerConfig
        widgetSize = buffListenerConfig.get('size', uiConst.BUFF_LISTENER_SIZE_1)
        if widgetSize == uiConst.BUFF_LISTENER_SIZE_1:
            self.widget.bg.scaleX = 2.799
            self.widget.bg.scaleY = 2.799
            self.widget.canvas.scaleX = 1
            self.widget.canvas.scaleY = 1
            self.widget.touchMc.scaleX = 1
            self.widget.touchMc.scaleY = 1
        elif widgetSize == uiConst.BUFF_LISTENER_SIZE_2:
            self.widget.bg.scaleX = 4.199
            self.widget.bg.scaleY = 4.199
            self.widget.canvas.scaleX = 1.5
            self.widget.canvas.scaleY = 1.5
            self.widget.touchMc.scaleX = 1.5
            self.widget.touchMc.scaleY = 1.5
        self.widget.settingBtn.x = self.widget.bg.x + self.widget.bg.width - 25

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def handleMouseRollOver(self, *arg):
        if not self.hasBaseData():
            return
        Tweener.removeTweens(self.widget.settingBtn)
        Tweener.removeTweens(self.widget.bg)
        self.widget.settingBtn.alpha = 1
        self.widget.bg.alpha = 1
        self.widget.settingBtn.visible = True
        self.widget.bg.visible = True

    def handleMouseRollOut(self, *arg):
        if not self.hasBaseData():
            return
        tweenData = {'alpha': 0,
         'time': 0.8,
         'onComplete': self.disappearedCompleted}
        Tweener.addTween(self.widget.settingBtn, tweenData)
        Tweener.addTween(self.widget.bg, tweenData)

    def disappearedCompleted(self, *arg):
        if not self.hasBaseData():
            return
        self.widget.settingBtn.visible = False
        self.widget.bg.visible = False

    def handleSettingBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        gameglobal.rds.ui.buffListenerSetting.show()
