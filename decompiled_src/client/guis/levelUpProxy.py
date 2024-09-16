#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/levelUpProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import clientUtils
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis import tipUtils
from cdata import lv_up_award_data as LUAD

class LevelUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LevelUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickIcon': self.onClickIcon,
         'getLevelUpAward': self.onGetLevelUpAward,
         'getInfo': self.onGetInfo,
         'closePanel': self.onClosePanel,
         'getAwardInfo': self.onGetAwardInfo}
        self.levelUpMediator = None
        self.levelUpPanelMediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_LEVELUP_PANEL, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LEVELUP:
            self.levelUpMediator = mediator
            self.levelUpMediator.Invoke('setVisible', GfxValue(False))
            if self.isActive():
                self.setState('active')
            else:
                self.setState('normal')
        elif widgetId == uiConst.WIDGET_LEVELUP_PANEL:
            self.levelUpPanelMediator = mediator

    def clearWidget(self):
        self.levelUpPanelMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LEVELUP_PANEL)

    def onClosePanel(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LEVELUP_PANEL)

    def onClickIcon(self, *arg):
        pass

    def onGetInfo(self, *arg):
        ret = [BigWorld.player().lv]
        for key in LUAD.data.keys():
            if BigWorld.player().lvUpRewardData.get(key):
                ret.append([2, key])
            elif key <= BigWorld.player().lv:
                ret.append([1, key])
            else:
                ret.append([0, key])

        return uiUtils.array2GfxAarry(ret)

    def onGetLevelUpAward(self, *arg):
        lv = int(arg[3][0].GetString())
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LEVELUP_PANEL)
        BigWorld.player().cell.getLvUpReward(lv)

    def setState(self, state):
        if self.levelUpMediator:
            self.levelUpMediator.Invoke('setState', GfxValue(state))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, idItem = key.split('.')
        index = int(idItem[4:])
        return tipUtils.getItemTipById(index)

    def onGetAwardInfo(self, *arg):
        num = arg[3][0].GetNumber()
        data = []
        bonusId = LUAD.data.get(num, {}).get('bonusId', 0)
        items = clientUtils.genItemBonus(bonusId)
        for item in items:
            it = {}
            it['id'] = item[0]
            it['num'] = item[1]
            it['iconPath'] = uiUtils.getItemIconFile40(item[0])
            data.append(it)

        return uiUtils.array2GfxAarry(data)

    def isActive(self):
        isActive = False
        for key in LUAD.data.keys():
            if not BigWorld.player().lvUpRewardData.get(key[0]) and key[0] <= BigWorld.player().lv:
                isActive = True

        return isActive

    def refreshPanel(self):
        ret = [BigWorld.player().lv]
        isActive = False
        for key in LUAD.data.keys():
            if BigWorld.player().lvUpRewardData.get(key):
                ret.append([2, key])
            elif key <= BigWorld.player().lv:
                isActive = True
                ret.append([1, key])
            else:
                ret.append([0, key])

        if isActive:
            self.setState('active')
        else:
            self.setState('normal')
        if self.levelUpPanelMediator:
            self.levelUpPanelMediator.Invoke('initPanel', uiUtils.array2GfxAarry(ret))
