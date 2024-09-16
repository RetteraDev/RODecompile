#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/userBackAwardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from callbackHelper import Functor
from data import fame_data as FD
from data import flowback_bonus_type_data as FBTD
from cdata import game_msg_def_data as GMDD

class UserBackAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UserBackAwardProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_USER_BACK_AWARD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_USER_BACK_AWARD:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_USER_BACK_AWARD)

    def show(self, bonusType):
        self.bonusType = bonusType
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_USER_BACK_AWARD)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            if self.bonusType == gametypes.FLOWBACK_BONUS_TYPE_JIULI:
                title = gameStrings.TEXT_USERBACKAWARDPROXY_47
                unit = gameStrings.TEXT_SKILLPROXY_1168_1
                fixedAmount = p.flowbackBonus.jiuliBonus.fixedAmount
                extraAmount = p.flowbackBonus.jiuliBonus.extraAmount
                fameId = FBTD.data.get(p.flowbackBonus.jiuliBonus.lostType, {}).get('jiuliExtraFameId', 0)
                consumeFameVal = p.flowbackBonus.jiuliBonus.consumeFameVal
            elif self.bonusType == gametypes.FLOWBACK_BONUS_TYPE_YAOLI:
                title = gameStrings.TEXT_USERBACKAWARDPROXY_54
                unit = gameStrings.TEXT_USERBACKAWARDPROXY_55
                fixedAmount = p.flowbackBonus.yaoliBonus.fixedAmount / 10
                extraAmount = p.flowbackBonus.yaoliBonus.extraAmount / 10
                fameId = FBTD.data.get(p.flowbackBonus.yaoliBonus.lostType, {}).get('yaoliExtraFameId', 0)
                consumeFameVal = p.flowbackBonus.yaoliBonus.consumeFameVal
            else:
                return
            info['title'] = gameStrings.TEXT_USERBACKAWARDPROXY_63 % title
            info['checkBox0Label'] = gameStrings.TEXT_USERBACKAWARDPROXY_64 % (fixedAmount, unit, title)
            info['checkBox1Label'] = gameStrings.TEXT_USERBACKAWARDPROXY_65 % (fixedAmount,
             extraAmount,
             unit,
             title,
             consumeFameVal,
             FD.data.get(fameId, {}).get('name', ''))
            if extraAmount > 0:
                if p.getFame(fameId) < consumeFameVal:
                    info['checkBox0Selected'] = True
                    info['checkBox1Selected'] = False
                else:
                    info['checkBox0Selected'] = False
                    info['checkBox1Selected'] = True
                info['checkBox1Enabled'] = True
            else:
                info['checkBox0Selected'] = True
                info['checkBox1Selected'] = False
                info['checkBox1Enabled'] = False
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if idx < 0:
            return
        p = BigWorld.player()
        useExtra = idx > 0
        if self.bonusType == gametypes.FLOWBACK_BONUS_TYPE_JIULI:
            amount = p.flowbackBonus.jiuliBonus.fixedAmount
            if useExtra:
                amount += p.flowbackBonus.jiuliBonus.extraAmount
            fameId = gametypes.RECOMMEND_WENQUAN_JIULI
            if amount + p.getFame(fameId) > FD.data.get(fameId, {}).get('maxVal', 0):
                msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_JIULI_APPLY_LIMIT_WARNING, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realConfirm, self.bonusType, useExtra))
                return
        elif self.bonusType == gametypes.FLOWBACK_BONUS_TYPE_YAOLI:
            amount = p.flowbackBonus.yaoliBonus.fixedAmount
            if useExtra:
                amount += p.flowbackBonus.yaoliBonus.extraAmount
            if amount > p.yaoliPoint:
                msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_YAOLI_APPLY_LIMIT_WARNING, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realConfirm, self.bonusType, useExtra))
                return
        self.realConfirm(self.bonusType, useExtra)

    def realConfirm(self, bonusType, useExtra):
        BigWorld.player().cell.applyFlowbackBonus(bonusType, useExtra)
        self.hide()
