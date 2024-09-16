#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/carnivalPushProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis import tipUtils
from data import item_data as ID
from cdata import font_config_data as FCD

class CarnivalPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CarnivalPushProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'applyReward': self.onApplyReward,
         'initData': self.onInitData,
         'getTooltip': self.onGetTooltip}
        self.mediator = None
        self.itemBonus = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CARNIVAL_PUSH:
            self.mediator = mediator

    def refresh(self):
        self.itemBonus = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD).get('data', None)
        if self.mediator:
            self.refreshData()

    def show(self):
        if self.mediator:
            return
        else:
            self.itemBonus = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD).get('data', None)
            if self.itemBonus:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CARNIVAL_PUSH)
            return

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CARNIVAL_PUSH)

    def reset(self):
        self.itemBonus = None

    def onClickClose(self, *arg):
        self.hide()

    def onApplyReward(self, *arg):
        BigWorld.player().cell.getCarnivalBonus()
        self.hide()

    def onInitData(self, *arg):
        self.refreshData()

    def refreshData(self):
        if self.itemBonus == None:
            return
        else:
            data = {}
            data['icon'] = []
            for item in self.itemBonus:
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
