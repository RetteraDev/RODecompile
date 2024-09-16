#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/festivalPushProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis import tipUtils
from data import item_data as ID
from cdata import font_config_data as FCD

class FestivalPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FestivalPushProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'applyReward': self.onApplyReward,
         'initData': self.onInitData,
         'getTooltip': self.onGetTooltip}
        self.mediator = None
        self.itemList = None
        self.actId = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FESTIVAL_PUSH:
            self.mediator = mediator

    def refresh(self):
        if self.mediator:
            pushData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_FESTIVAL_REWARD)
            if pushData:
                self.actId, self.itemList = pushData.get('data', (None, None))
                self.refreshData()

    def show(self):
        if self.mediator:
            return None
        else:
            pushData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_FESTIVAL_REWARD)
            if pushData:
                self.actId, self.itemList = pushData.get('data', (None, None))
                if self.itemList and self.actId:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FESTIVAL_PUSH)
            return None

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FESTIVAL_PUSH)

    def reset(self):
        self.itemList = None
        self.actId = None

    def onClickClose(self, *arg):
        self.hide()

    def onApplyReward(self, *arg):
        BigWorld.player().cell.getFestivalBonus(self.actId)
        self.hide()

    def onInitData(self, *arg):
        self.refreshData()

    def refreshData(self):
        if self.itemList == None:
            return
        else:
            data = {}
            data['icon'] = []
            for item in self.itemList:
                path = uiUtils.getItemIconFile40(item[0])
                quality = ID.data.get(item[0], {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                ar = [path,
                 item[1],
                 color,
                 item[0]]
                data['icon'].append(ar)

            if self.mediator:
                self.mediator.Invoke('refreshData', uiUtils.dict2GfxDict(data))
            return

    def onGetTooltip(self, *arg):
        idx = int(arg[3][0].GetString())
        return tipUtils.getItemTipById(idx)
