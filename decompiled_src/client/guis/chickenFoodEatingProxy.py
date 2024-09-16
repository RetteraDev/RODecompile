#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodEatingProxy.o
import BigWorld
import gameglobal
import gamelog
import random
import formula
import const
import time
import events
import keys
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import chickenFoodFactory
from guis import uiUtils
from asObject import ASUtils
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import fame_data as FD
BENGIN_COUNT_NUM = 3
OVER_COUNT_NUM = 10
OVER_COUNT_BEGIN = 12
PHASE_INFO_DICT = {1: ((0, False), ()),
 2: ((0, True), (1, False)),
 3: ((1, True), (2, False)),
 4: ((2, True), (3, False)),
 5: ((3, True), ())}
PROGRESS_MAX_VALUE = 10000
RESIDUE_NUM_MAX = 50

class ChickenFoodEatingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodEatingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.disappearCallback = None
        self.refreshCallBack = None
        self.reset()
        self.cfFactory = chickenFoodFactory.getInstance()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_EATING:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_EATING)

    def clearWidget(self):
        gameglobal.rds.sound.stopSound(5771)
        p = BigWorld.player()
        if p:
            p.unlockKey(gameglobal.KEY_POS_CHICKEN_QTE)
        self.cancelDisappearCB()
        self.cancelrefreshCB()
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_EATING)

    def reset(self):
        self.beginTime = -1
        self.overTime = -1
        self.pressCount = 0
        self.curPhase = 0
        self.isActive = False
        self.pressBtnValue = None
        self.countInfo = {}
        self.countTime = 0
        self.getRewardTime = 0
        self.residueDict = {}
        self.residueNum = 0

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.curPhase = 0

    def initState(self):
        p = BigWorld.player()
        p.lockKey(gameglobal.KEY_POS_CHICKEN_QTE)
        self.widget.bigCountDownMc.visible = False
        self.widget.smallCountDownMc.visible = False
        self.widget.actionTxtMc.visible = False
        self.widget.indirectPress.visible = False
        chickenQteInfo = SCD.data.get('chickenQteInfo', {})
        keyList = chickenQteInfo.get('key', ())
        if keyList:
            key = keyList[random.randint(0, len(keyList) - 1)].upper()
            self.pressBtnValue = getattr(keys, 'KEY_' + key, None)
            self.widget.indirectPress.pressTxt.txtMc.innerTxt.keyTxt.text = key
        for x in xrange(0, RESIDUE_NUM_MAX):
            residue = getattr(self.widget, 'residue' + str(x), None)
            if residue:
                residue.visible = False
                self.residueNum += 1
            else:
                break

        self.widget.foodProgressMc.foodProgress.maxValue = PROGRESS_MAX_VALUE
        self.widget.foodProgressMc.foodProgress.currentValue = PROGRESS_MAX_VALUE
        self.setChickenPhase(1)
        self.countDownWithBegin()

    def refreshInfo(self):
        if self.hasBaseData():
            self.countTime += 1
            p = BigWorld.player()
            p.cell.getChickenQteTickReward(self.pressCount)
            self.pressCount = 0
            chickenQteInfo = SCD.data.get('chickenQteInfo', {})
            totalCount = chickenQteInfo.get('chickQteFinishCountNeed', 0)
            if totalCount:
                clickCount = 0
                for k, v in self.countInfo.iteritems():
                    clickCount += v

                clickRate = float(clickCount) / float(totalCount) if float(clickCount) / float(totalCount) <= 1 else 1
                curValue = PROGRESS_MAX_VALUE * (1 - clickRate)
                _curPhase = self.genPhase(curValue)
                if _curPhase != self.genPhase(self.widget.foodProgressMc.foodProgress.currentValue):
                    self.setChickenPhase(_curPhase)
                    gameglobal.rds.sound.playSound(5772)
                self.widget.foodProgressMc.foodProgress.currentValue = curValue
            chickenPersistTime = chickenQteInfo.get('chickenPersistTime', 0)
            if chickenPersistTime - self.countTime <= OVER_COUNT_BEGIN and self.overTime == -1:
                self.countDownWithOver()
            self.refreshCallBack = BigWorld.callback(1, self.refreshInfo)

    def genPhase(self, value):
        PHASEVALUE = ((PROGRESS_MAX_VALUE, PROGRESS_MAX_VALUE * 0.9),
         (PROGRESS_MAX_VALUE * 0.9, PROGRESS_MAX_VALUE * 0.6),
         (PROGRESS_MAX_VALUE * 0.6, PROGRESS_MAX_VALUE * 0.4),
         (PROGRESS_MAX_VALUE * 0.4, PROGRESS_MAX_VALUE * 0.1),
         (PROGRESS_MAX_VALUE * 0.1, 0))
        curPhase = 0
        for _max, _min in PHASEVALUE:
            curPhase += 1
            if _max >= value >= _min:
                return curPhase

        return curPhase

    def disappearCB(self, *arg):
        if self.hasBaseData():
            self.hide()

    def hasBaseData(self):
        if self.cfFactory and self.widget:
            return True
        else:
            return False

    def countDownWithBegin(self):
        self.beginTime = BENGIN_COUNT_NUM
        self.beginCallBack()

    def countDownWithOver(self, immediately = False):
        if immediately:
            self.overTime = 0
            self.overCallBack()
        else:
            self.overTime = OVER_COUNT_NUM
            self.overCallBack()

    def overCallBack(self):
        if self.isActive:
            if self.overTime > 0:
                self.setSmallCountDownMc(self.overTime)
                BigWorld.callback(1, Functor(self.overCallBack))
            else:
                self.setActionTxtMc('over')
                self.overDone()
            self.overTime -= 1

    def beginCallBack(self):
        if self.beginTime > 0:
            self.setBigCountDownMc(self.beginTime)
            BigWorld.callback(1, Functor(self.beginCallBack))
        else:
            self.setActionTxtMc('begin')
            self.beginDone()
        self.beginTime -= 1

    def setSmallCountDownMc(self, num):
        if self.hasBaseData():
            self.widget.smallCountDownMc.visible = True
            self.widget.actionTxtMc.visible = False
            self.widget.smallCountDownMc.gotoAndPlay('num' + str(num))
            gameglobal.rds.sound.playSound(5769)

    def setBigCountDownMc(self, num):
        if self.hasBaseData():
            self.widget.bigCountDownMc.visible = True
            self.widget.actionTxtMc.visible = False
            self.widget.bigCountDownMc.gotoAndPlay(0)
            self.widget.bigCountDownMc.numMc1.gotoAndPlay('num' + str(num))
            self.widget.bigCountDownMc.numMc2.gotoAndPlay('num' + str(num))
            gameglobal.rds.sound.playSound(5769)

    def setActionTxtMc(self, state):
        if self.hasBaseData():
            self.widget.bigCountDownMc.visible = False
            self.widget.smallCountDownMc.visible = False
            self.widget.actionTxtMc.visible = True
            self.widget.actionTxtMc.gotoAndPlay(0)
            self.widget.actionTxtMc.action1.gotoAndPlay(state)
            self.widget.actionTxtMc.action2.gotoAndPlay(state)

            def _disappearCB(*arg):
                self.disappearCB(state, *arg)

            self.cancelDisappearCB()
            self.disappearCallback = ASUtils.callbackAtFrame(self.widget.actionTxtMc, 45, _disappearCB)

    def beginActionDone(self):
        pass

    def beginDone(self):
        if self.hasBaseData():
            self.isActive = True
            self.appearTypeBtn()
            self.countingBegin()
            gameglobal.rds.sound.playSound(5770)
            gameglobal.rds.sound.playSound(5771)

    def countingBegin(self):
        self.refreshInfo()

    def overDone(self):
        if self.hasBaseData():
            self.widget.indirectPress.visible = False
            self.isActive = False
            gameglobal.rds.sound.playSound(5773)
            gameglobal.rds.sound.stopSound(5771)

    def overActionDone(self):
        self.hide()

    def cancelDisappearCB(self):
        if self.disappearCallback:
            ASUtils.cancelCallBack(self.disappearCallback)
            self.disappearCallback = None

    def cancelrefreshCB(self):
        if self.refreshCallBack:
            BigWorld.cancelCallback(self.refreshCallBack)
            self.refreshCallBack = None

    def disappearCB(self, state, *arg):
        if state == 'begin':
            self.beginActionDone()
        elif state == 'over':
            self.overActionDone()

    def appearTypeBtn(self):
        if self.hasBaseData():
            self.widget.indirectPress.visible = True
            self.widget.indirectPress.gotoAndPlay('up')

    def pressBtn(self):
        if self.hasBaseData():
            if self.widget.indirectPress.currentFrameLabel != 'charge':
                self.widget.indirectPress.gotoAndStop('charge')
            self.widget.indirectPress.typeBtn.gotoAndPlay(0)
            self.widget.indirectPress.pressTxt.gotoAndPlay(0)
            self.widget.foodProgressMc.gotoAndPlay(0)
            choiceList = []
            for x in xrange(0, self.residueNum):
                if not self.residueDict.get(x, None):
                    choiceList.append(x)

            if choiceList:
                num = random.choice(choiceList)
                residue = getattr(self.widget, 'residue' + str(num), None)
                if residue:
                    residue.gotoAndPlay(0)
                    residue.visible = True
                    self.residueDict[num] = True

                    def _disappearCB(*arg):
                        self.residueActionDone(num)

                    ASUtils.callbackAtFrame(residue, 25, _disappearCB)

    def residueActionDone(self, num):
        if self.hasBaseData():
            self.residueDict[num] = False
            residue = getattr(self.widget, 'residue' + str(num), None)
            if residue:
                residue.visible = False

    def addPhaseAction(self):
        self.curPhase += 1
        self.setChickenPhase(self.curPhase)

    def setChickenPhase(self, num):
        if self.hasBaseData():
            phaseInfo = PHASE_INFO_DICT.get(num, None)
            changeInfo, steadyInfo = phaseInfo
            isChange = False
            if changeInfo:
                phase, isPlay = changeInfo
                self.widget.chickenMc.gotoAndPlay('phase' + str(phase))
                if isPlay:
                    self.widget.chickenMc.chickenFood.gotoAndPlay(0)
                    isChange = True
                else:
                    self.widget.chickenMc.chickenFood.gotoAndStop(0)
            if isChange and steadyInfo:

                def _disappearCB(*arg):
                    if self.hasBaseData():
                        _phase, _isPlay = steadyInfo
                        self.widget.chickenMc.gotoAndPlay('phase' + str(_phase))
                        if _isPlay:
                            self.widget.chickenMc.chickenFood.gotoAndPlay(0)
                        else:
                            self.widget.chickenMc.chickenFood.gotoAndStop(0)

                ASUtils.callbackAtFrame(self.widget.chickenMc.chickenFood, 50, _disappearCB)

    def handleInputKey(self, down, key, vk, mods):
        if self.hasBaseData() and down and key == self.pressBtnValue and self.isActive:
            chickenQteInfo = SCD.data.get('chickenQteInfo', {})
            typeLimit = chickenQteInfo.get('typeLimit', 0)
            if self.pressCount < typeLimit:
                p = BigWorld.player()
                self.pressCount += 1
                fameId = chickenQteInfo.get('chickenQteTickFameId', 0)
                fData = FD.data.get(fameId, {})
                fameName = fData.get('name', '')
                formulaId = chickenQteInfo.get('typeRewardFormula', 0)
                fInfo = {'lv': p.lv,
                 'times': 1}
                diff = formula.calcFormulaById(formulaId, fInfo)
                self.uiAdapter.showRewardLabel(diff, const.REWARD_LABEL_EXP)
            self.pressBtn()
            return True

    def getFormulaValue(self, expformula):
        p = BigWorld.player()
        expformula = expformula.replace('lv', str(p.lv))
        val = 0
        try:
            val = eval(expformula)
        except:
            val = 0

        return val

    def onSyncChickenQteClickCount(self, countInfo):
        if self.hasBaseData():
            self.countInfo = countInfo

    def onEnd(self, chickenQteResult):
        if self.hasBaseData():
            self.countDownWithOver(True)
