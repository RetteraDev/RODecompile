#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achievePushProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import clientUtils
import const
from item import Item
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiUtils
from data import achievement_data as AD
from data import item_data as ID
from cdata import font_config_data as FCD

class AchievePushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchievePushProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'applyReward': self.onApplyReward,
         'initData': self.onInitData,
         'getTooltip': self.onGetTooltip,
         'gotoAchieve': self.onGotoAchieve}
        self.mediator = None
        self.achieveId = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACHIEVE_PUSH:
            self.mediator = mediator

    def refresh(self):
        pass

    def show(self):
        if self.mediator:
            return
        else:
            self.achieveId = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD).get('data', None)
            if self.achieveId in AD.data:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACHIEVE_PUSH)
            return

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACHIEVE_PUSH)

    def reset(self):
        super(self.__class__, self).reset()
        self.achieveId = None

    def onClickClose(self, *arg):
        self.hide()

    def onGotoAchieve(self, *arg):
        self.gotoAchieveNew()

    def gotoAchieveNew(self):
        if not gameglobal.rds.ui.achvment.widget:
            gameglobal.rds.ui.achvment.linkAchieveId = self.achieveId
            gameglobal.rds.ui.achvment.getAchieveData()
        else:
            gameglobal.rds.ui.achvment.link2AchvmentDetailView(achieveId=self.achieveId)

    def onApplyReward(self, *arg):
        p = BigWorld.player()
        p.cell.applyAchieveAward(self.achieveId)

    def onInitData(self, *arg):
        movie = arg[0]
        obj = movie.CreateObject()
        itemList = self.movie.CreateArray()
        adData = AD.data[self.achieveId]
        obj.SetMember('achieveName', GfxValue(gbk2unicode(adData['name'])))
        bonusId = adData.get('bonusId', 0)
        itemBonus = clientUtils.genItemBonus(bonusId)
        if itemBonus:
            i = 0
            for item in itemBonus:
                ar = self.movie.CreateArray()
                path = uiUtils.getItemIconFile40(item[0])
                ar.SetElement(0, GfxValue(path))
                ar.SetElement(1, GfxValue(item[1]))
                quality = ID.data.get(item[0], {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                ar.SetElement(2, GfxValue(color))
                ar.SetElement(3, GfxValue(item[0]))
                itemList.SetElement(i, ar)
                i += 1

            obj.SetMember('icon', itemList)
        return obj

    def onGetTooltip(self, *arg):
        idx = int(arg[3][0].GetString())
        i = Item(idx)
        return self.uiAdapter.inventory.GfxToolTip(i, const.ITEM_IN_NONE)
