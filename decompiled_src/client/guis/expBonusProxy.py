#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/expBonusProxy.o
from gamestrings import gameStrings
import BigWorld
import time
from uiProxy import UIProxy
import gameglobal
import utils
import formula
import const
import clientUtils
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from data import exp_bonus_data as EBD
from data import fame_data as FD
from data import sys_config_data as SCD
from cdata import exp_bonus_func_data as EBFD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class ExpBonusProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExpBonusProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'getList': self.onGetList,
         'getData': self.onGetData,
         'applyExpBonus': self.onApplyExpBonus}
        self.mediator = None
        self.funcId = 0
        self.expBonusData = []
        self.curSelectId = 0
        self.isFreezed = None
        self.npcId = 0
        self.isEnable = True
        self.forceUpdate = True
        self.vipApply = False
        self.msgBoxId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_EXP_BONUS, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EXP_BONUS:
            self.mediator = mediator

    def show(self, npcId, funcId, vipApply = False):
        self.npcId = npcId
        self.funcId = funcId
        self.isEnable = True
        self.forceUpdate = True
        self.vipApply = vipApply
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXP_BONUS)

    def onClose(self, *arg):
        gameglobal.rds.ui.funcNpc.close()
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.npcId = 0
        self.funcId = 0
        self.vipApply = False
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXP_BONUS)

    def clearData(self):
        self.expBonusData = []
        self.isFreezed = None
        self.msgBoxId = 0

    def freezeOrUnFreezeBonus(self, npcId):
        self.npcId = npcId
        totalTime = self.getTotalRemainTime()
        if totalTime <= 0:
            msg = GMD.data.get(GMDD.data.NONE_REMAIN_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_76)
        elif self.isFreezed:
            msg = GMD.data.get(GMDD.data.CONFIRM_TO_UNFREEZE_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_79) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        else:
            msg = GMD.data.get(GMDD.data.CONFIRM_TO_FREEZE_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_81) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.comfirmfreezeOrUnFreeze, self.isFreezed), noCallback=Functor(self.cancelfreezeOrUnFreeze))

    def comfirmfreezeOrUnFreeze(self, isFreezed):
        totalTime = self.getTotalRemainTime()
        if totalTime <= 0:
            gameglobal.rds.ui.funcNpc.onDefaultState()
            return
        npcEnt = BigWorld.entity(self.npcId)
        if npcEnt:
            if isFreezed:
                npcEnt.cell.unfreezeExpBonus()
            else:
                npcEnt.cell.freezeExpBonus()
        gameglobal.rds.ui.funcNpc.onDefaultState()

    def cancelfreezeOrUnFreeze(self):
        gameglobal.rds.ui.funcNpc.onDefaultState()

    def hasAvaliableExpBonus(self, funcId):
        self.funcId = funcId
        expBonusTypes = EBFD.data.get(self.funcId, {}).get('bonusIds', [])
        nowTime = utils.getNow()
        for idx in range(len(expBonusTypes)):
            id = expBonusTypes[idx]
            beginTime = EBD.data.get(id, {}).get('beginT', None)
            timeArray = self._strptime(beginTime)
            timeStamp = int(time.mktime(timeArray))
            if beginTime != None and timeStamp <= nowTime:
                return True

        return False

    def onGetList(self, *arg):
        expBonusTypes = EBFD.data.get(self.funcId, {}).get('bonusIds', [])
        nowTime = utils.getNow()
        ret = []
        for idx in range(len(expBonusTypes)):
            id = expBonusTypes[idx]
            beginTime = EBD.data.get(id, {}).get('beginT', None)
            timeArray = self._strptime(beginTime)
            if beginTime != None:
                timeStamp = int(time.mktime(timeArray))
                if timeStamp <= nowTime:
                    dataObj = {}
                    dataObj['id'] = id
                    dataObj['label'] = EBD.data.get(id, {}).get('desc', '')
                    ret.append(dataObj)

        return uiUtils.array2GfxAarry(ret, True)

    def _strptime(self, express):
        year = int(express[:4])
        month = int(express[5:7])
        day = int(express[8:])
        return time.struct_time((year,
         month,
         day,
         0,
         0,
         0,
         0,
         0,
         -1))

    def onGetData(self, *arg):
        self.curSelectId = int(arg[3][0].GetNumber())
        data = self._getData()
        return data

    def updateData(self):
        if not self.forceUpdate:
            return
        data = self._getData()
        if self.mediator:
            self.mediator.Invoke('refreshView', data)
        self.forceUpdate = False

    def _getData(self):
        self.isEnable = True
        ret = {}
        ret['period'] = EBD.data.get(self.curSelectId, {}).get('period', 0)
        ret['remainTime'] = self.getTotalRemainTime()
        ret['restTime'] = self.getCertainRestTime(self.curSelectId)
        ret['itemList'] = self.getCostItems(self.curSelectId)
        ret['costList'] = self.getOtherCost(self.curSelectId)
        ret['limitMax'] = EBD.data.get(self.curSelectId, {}).get('duration', 0)
        ret['isFreezed'] = self.isFreezed
        ret['isEnable'] = self.isEnable
        ret['desc'] = self.getCurrentStateDesc()
        return uiUtils.dict2GfxDict(ret, True)

    def getCurrentStateDesc(self):
        msg = ''
        totalTime = self.getTotalRemainTime()
        if totalTime <= 0:
            msg = GMD.data.get(GMDD.data.NONE_REMAIN_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_76)
        elif self.isFreezed:
            msg = GMD.data.get(GMDD.data.FREEZED_EXP_BONUS_TIME, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_180) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        else:
            msg = GMD.data.get(GMDD.data.UNFREEZED_EXP_BONUS_TIME, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_182) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        return msg

    def getCostItems(self, bonusId):
        itemList = []
        items = EBD.data.get(bonusId, {}).get('item', [])
        for item in items:
            ownCount = BigWorld.player().inv.countItemInPages(int(item[0]), enableParentCheck=True)
            count = uiUtils.convertNumStr(ownCount, item[1])
            itemObj = uiUtils.getGfxItemById(item[0], count, srcType='bindFirstInInv')
            itemList.append(itemObj)

        return itemList

    def getOtherCost(self, bonusId):
        costList = []
        p = BigWorld.player()
        cashCost = EBD.data.get(bonusId, {}).get('cash', [])
        if len(cashCost) > 1:
            cashObj = {}
            cashType = cashCost[0]
            ownCash = 0
            if cashType == 1:
                cashObj['type'] = 'bindCash'
                ownCash = p.bindCash
            elif cashType == 2:
                cashObj['type'] = 'cash'
                ownCash = p.cash
            cashObj['num'] = uiUtils.convertNumStr(ownCash, cashCost[1], False)
            costList.append(cashObj)
        expCost = EBD.data.get(bonusId, {}).get('exp', 0)
        if expCost > 0:
            expObj = {}
            expObj['type'] = 'exp'
            ownExp = p.exp
            expObj['num'] = uiUtils.convertNumStr(ownExp, expCost, False)
            costList.append(expObj)
        fameCost = EBD.data.get(bonusId, {}).get('fame', [])
        for fame in fameCost:
            if len(fame) > 1:
                fameObj = {}
                fameObj['type'] = 'fame'
                ownFame = p.fame.get(fame[0], 0)
                fameObj['fameTip'] = FD.data.get(fame[0], {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
                fameObj['num'] = uiUtils.convertNumStr(ownFame, fame[1], False)
                costList.append(fameObj)

        banggongCost = EBD.data.get(bonusId, {}).get('banggong', 0)
        if banggongCost > 0:
            banggongObj = {}
            banggongObj['type'] = 'banggong'
            if p.guild != None:
                ownBanggong = p.guild.memberMe.contrib
            else:
                ownBanggong = 0
            banggongObj['num'] = uiUtils.convertNumStr(ownBanggong, banggongCost, False)
            costList.append(banggongObj)
        return costList

    def getCertainRemainTime(self, bonusId):
        remainTime = 0
        crontab = EBD.data.get(bonusId, {}).get('crontab', '')
        now = utils.getNow()
        for key in self.expBonusData:
            data = self.expBonusData[key]
            if key == bonusId and len(data) > 1:
                if utils.getNextCrontabTime(crontab, data[3]) < utils.getNextCrontabTime(crontab, now):
                    remainTime = 0
                else:
                    remainTime = data[0]
                break

        return remainTime

    def getCertainRestTime(self, bonusId):
        restTime = 0
        currentTime = 0
        now = utils.getNow()
        maxTime = EBD.data.get(bonusId, {}).get('duration', 0)
        crontab = EBD.data.get(bonusId, {}).get('crontab', '')
        for key in self.expBonusData:
            data = self.expBonusData[key]
            if key == bonusId and len(data) > 1:
                if utils.getNextCrontabTime(crontab, data[3]) < utils.getNextCrontabTime(crontab, now):
                    currentTime = 0
                else:
                    currentTime = data[2]
                break

        restTime = max(maxTime - currentTime, 0)
        return restTime

    def getTotalRemainTime(self):
        totalRemainTime = 0
        for key in self.expBonusData:
            data = self.expBonusData[key]
            if len(data) > 1:
                totalRemainTime += data[0]

        return totalRemainTime

    def onApplyExpBonus(self, *arg):
        bonusId = int(arg[3][0].GetNumber())
        hours = int(arg[3][1].GetNumber())
        totalSec = self.getTotalRemainTime()
        if self.isFreezed:
            msg = GMD.data.get(GMDD.data.APPLY_EXP_WHEN_FREEZED_TIP, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_298) % (utils.formatTimeStr(totalSec, gameStrings.TEXT_EXPBONUSPROXY_79_1), utils.formatTimeStr(totalSec + hours * 3600, gameStrings.TEXT_EXPBONUSPROXY_79_1))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmApplyExpBonus, bonusId, hours))
        else:
            self.confirmApplyExpBonus(bonusId, hours)
        self.forceUpdate = True

    def confirmApplyExpBonus(self, bonusId, hours):
        if self.vipApply:
            BigWorld.player().cell.addExpBonusTimeVip(bonusId, hours)
        else:
            ent = BigWorld.entities.get(self.npcId)
            if not ent:
                return
            ent.cell.applyExpBonus(bonusId, hours)
