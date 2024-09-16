#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/activationProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import clientUtils
import ui
import utils
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import activation_reward_data as ARD

class ActivationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivationProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'clickFree': self.onClickFree}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVATION:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVATION)

    def show(self):
        if not gameglobal.rds.configData.get('enableActivation', False):
            return
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVATION)

    @ui.callAfterTime()
    def refreshInfoLater(self):
        self.refreshInfo()

    def refreshInfo(self, playSound = False):
        if self.mediator:
            p = BigWorld.player()
            ard = {}
            for minLv, maxLv in ARD.data.keys():
                if minLv <= p.activationLv <= maxLv:
                    ard = ARD.data.get((minLv, maxLv), {})
                    break

            if not ard:
                self.hide()
                return
            activationMargins = ard.get('activationMargins')
            bonusIds = ard.get('bonusIds')
            crontabStart = ard.get('crontabStart')
            crontabEnd = ard.get('crontabEnd')
            if crontabStart and crontabEnd:
                if utils.inDateRange(crontabStart, crontabEnd):
                    bonusIdsEx = ard.get('bonusIds2', ())
                else:
                    bonusIdsEx = ()
            else:
                bonusIdsEx = ard.get('bonusIds2', ())
            showFreeJuexingRebuildActivation = ard.get('showFreeJuexingRebuildActivation', 0)
            if not activationMargins or not bonusIds:
                self.hide()
                return
            maxValue = activationMargins[-1]
            itemList = []
            btnEnabled = False
            isMultiple = False
            bonusLen = min(len(bonusIds), len(activationMargins))
            bonusExLen = len(bonusIdsEx)
            marginsLen = len(activationMargins)
            subValue = 1 if marginsLen == bonusLen else 0
            currentValue = 0.0
            lastStepMargin = 0
            for i in xrange(bonusLen):
                activationMargin = activationMargins[i]
                itemInfo = {}
                itemInfo['offest'] = (bonusLen - subValue - i) * 1.0 / marginsLen
                bonusId = bonusIds[i]
                itemBonus = clientUtils.genItemBonus(bonusId)
                itemId, itemNum = itemBonus[0]
                itemInfo['slotInfo'] = uiUtils.getGfxItemById(itemId, itemNum)
                if i < bonusExLen and bonusIdsEx[i] != 0:
                    bonusIdEx = bonusIdsEx[i]
                    itemBonusEx = clientUtils.genItemBonus(bonusIdEx)
                    itemIdEx, itemNumEx = itemBonusEx[0]
                    itemInfo['slotExInfo'] = uiUtils.getGfxItemById(itemIdEx, itemNumEx)
                    itemInfo['showSlotEx'] = True
                else:
                    bonusIdEx = 0
                    itemInfo['showSlotEx'] = False
                if activationMargin <= p.activation:
                    itemInfo['value'] = uiUtils.toHtml(str(activationMargin / 1000), '#66CC66')
                    currentValue += 1.0 / marginsLen
                    if bonusId in p.activationRewards:
                        itemInfo['state'] = 'finish'
                        multiple = p.activationRewards.get(bonusId, 1)
                        isMultiple = True if multiple > 1 else isMultiple
                        itemInfo['multipleEffectType'] = 'type%d' % multiple
                        if bonusIdEx:
                            multiple = p.activationRewards.get(bonusIdEx, 1)
                            isMultiple = True if multiple > 1 else isMultiple
                            itemInfo['multipleEffectExType'] = 'type%d' % multiple
                    else:
                        itemInfo['state'] = 'normal'
                        itemInfo['effectVisible'] = True
                        btnEnabled = True
                else:
                    itemInfo['value'] = activationMargin / 1000
                    itemInfo['state'] = 'normal'
                    itemInfo['effectVisible'] = False
                    currentValue += max(0.0, p.activation - lastStepMargin) * 1.0 / (activationMargin - lastStepMargin) * (1.0 / marginsLen)
                if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False) and activationMargin == showFreeJuexingRebuildActivation:
                    itemInfo['showFree'] = True
                    itemInfo['freeState'] = 'valid' if activationMargin <= p.activation else 'invalid'
                    itemInfo['freeTips'] = SCD.data.get('equipChangeJuexingRebuildFreeTips', '')
                else:
                    itemInfo['showFree'] = False
                lastStepMargin = activationMargin
                itemList.append(itemInfo)

            currentValue += max(0.0, p.activation - lastStepMargin) * 1.0 / (maxValue - lastStepMargin) * (1.0 / marginsLen)
            currentValue = min(100.0, currentValue * 100.0)
            info = {'itemList': itemList,
             'btnEnabled': btnEnabled,
             'currentValue': currentValue,
             'dayActivation': p.activation / 1000,
             'weekActivation': p.weekActivation / 1000,
             'lastWeekActivation': p.lastWeekActivation / 1000}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            if playSound and isMultiple:
                gameglobal.rds.sound.playSound(5635)

    def onConfirm(self, *args):
        BigWorld.player().cell.receiveActivationReward()

    def checkCanGetAward(self):
        p = BigWorld.player()
        if not p or not hasattr(p, 'activationLv'):
            return False
        ard = {}
        for minLv, maxLv in ARD.data.keys():
            if minLv <= p.activationLv <= maxLv:
                ard = ARD.data.get((minLv, maxLv), {})
                break

        if not ard:
            return False
        activationMargins = ard.get('activationMargins')
        bonusIds = ard.get('bonusIds')
        if not activationMargins or not bonusIds:
            return False
        bonusLen = min(len(bonusIds), len(activationMargins))
        for i in xrange(bonusLen):
            bonusId = bonusIds[i]
            activationMargin = activationMargins[i]
            if activationMargin <= p.activation:
                if bonusId not in p.activationRewards:
                    return True

        return False

    def onClickFree(self, *args):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 0)
