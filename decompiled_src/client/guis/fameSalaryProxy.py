#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fameSalaryProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
import gametypes
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import bonus_data as BD
from data import sys_config_data as SCD
from data import fame_data as FD
from data import fame_reward_bonus_data as FRBD

class FameSalaryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FameSalaryProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'close': self.onClose}
        self.mediator = None
        self.entityId = None
        self.fameId = 0
        self.bonusId = 0
        self.rewardType = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAME_SALARY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FAME_SALARY:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, entityId, fameId, bonusId):
        self.entityId = entityId
        self.fameId = fameId
        self.bonusId = bonusId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAME_SALARY)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAME_SALARY)

    def hideByFameId(self, fameId):
        if self.fameId == fameId:
            self.hide()

    def reset(self):
        self.entityId = None
        self.fameId = 0
        self.bonusId = 0
        self.rewardType = 0
        gameglobal.rds.ui.funcNpc.onDefaultState()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            fameLv = p.getFameLv(self.fameId)
            fd = FD.data.get(self.fameId, {})
            info = {}
            info['fameName'] = fd.get('name', '')
            info['fameLvName'] = SCD.data.get('fameLvNameModify', {}).get(fameLv, '')
            salaryInfo = FRBD.data.get(self.bonusId, {})
            bonusData = BD.data.get(salaryInfo.get('bonus', 0), {})
            fixedBonus = bonusData.get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if len(fixedBonus) > 0:
                _, bonusItemId, bonusNum = fixedBonus[0]
            else:
                bonusItemId, bonusNum = (0, 0)
            info['fameSalarySlot'] = uiUtils.getGfxItemById(bonusItemId, bonusNum)
            self.rewardType = salaryInfo.get('rewardType', 0)
            needList = []
            itemNeed = salaryInfo.get('itemNeed', None)
            if itemNeed and len(itemNeed) > 0:
                for itemId, needNum in itemNeed:
                    ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    if ownNum < needNum:
                        count = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                    else:
                        count = '%d/%d' % (ownNum, needNum)
                    needList.append(uiUtils.getGfxItemById(itemId, count))

            info['needList'] = needList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if itemId:
            npc = BigWorld.entities.get(self.entityId)
            if npc:
                npc.cell.applyFameReward(self.fameId, self.rewardType, itemId)
        else:
            BigWorld.player().showGameMsg(GMDD.data.FAME_REWARD_ITEM_NOT_CHOOSE, ())

    def onClose(self, *arg):
        self.hide()
