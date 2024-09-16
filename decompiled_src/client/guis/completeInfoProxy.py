#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/completeInfoProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
from data import sys_config_data as SCD
from data import bonus_data as BD

class CompleteInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CompleteInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'openWebToComplete': self.onOpenWebToComplete,
         'updateState': self.onUpdateState,
         'getRewards': self.onGetRewards,
         'closePage': self.onClosePage}
        self.secuInfoIdNum = 0
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_COMPLETE_INFO, self.hide)

    def show(self):
        if not gameglobal.rds.configData.get('enableSecInfo', False):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_COMPLETE_INFO)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_COMPLETE_INFO:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self._getInfoData(), True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMPLETE_INFO)
        if gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_COMPLETE_INFO):
            if self.secuInfoIdNum:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO)

    def _getInfoData(self):
        ret = {}
        isComplete = self.secuInfoIdNum
        ret['rewardItems'] = self._getInfoRewards()
        ret['state'] = isComplete
        ret['content'] = SCD.data.get('SECU_INFO_COMPLETE_DESC', gameStrings.TEXT_COMPLETEINFOPROXY_53) if isComplete else SCD.data.get('SECU_INFO_UNCOMPLETE_DESC', gameStrings.TEXT_COMPLETEINFOPROXY_53_1)
        return ret

    def _getInfoRewards(self):
        bonusId = SCD.data.get('SECU_INFO_BONUS_ID', 0)
        items = BD.data.get(bonusId, {}).get('fixedBonus', [])
        fixedBonus = utils.filtItemByConfig(items, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        itemList = []
        for item in items:
            if item[0] == 1:
                data = uiUtils.getGfxItemById(item[1], item[2])
                itemList.append(data)

        return itemList

    def onOpenWebToComplete(self, *arg):
        BigWorld.openUrl('http://reg.163.com/change/showPasswordInfo.do')

    def onUpdateState(self, *arg):
        p = BigWorld.player()
        p.base.updateSecuInfoIdNum()

    def onGetRewards(self, *arg):
        p = BigWorld.player()
        p.cell.applySecuInfoReward()
        self.hide()

    def onClosePage(self, *arg):
        self.hide()

    def updatePageView(self):
        if self.mediator:
            ret = self._getInfoData()
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))

    def pushRewardMsg(self):
        if self.mediator:
            self.hide()
        self.secuInfoIdNum = 1
        if gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_COMPLETE_INFO):
            if self.secuInfoIdNum:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO)
        if gameglobal.rds.configData.get('enableSecInfo', False):
            if BigWorld.player().lv >= SCD.data.get('MIN_SECU_INFO_REWARD_LEVEL', 40):
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO_REWARD)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_COMPLETE_INFO_REWARD, {'click': self.openCompleteInfoPage})

    def pushCompleteMsg(self):
        self.secuInfoIdNum = 0
        if gameglobal.rds.configData.get('enableSecInfo', False):
            if BigWorld.player().lv >= SCD.data.get('MIN_SECU_INFO_REWARD_LEVEL', 40):
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_COMPLETE_INFO, {'click': self.openCompleteInfoPage})

    def openCompleteInfoPage(self):
        self.show()
