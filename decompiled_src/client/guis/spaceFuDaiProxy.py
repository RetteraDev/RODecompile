#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceFuDaiProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from data import personal_zone_bonus_data as PZBD

class SpaceFuDaiProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(SpaceFuDaiProxy, self).__init__(uiAdapter)
        self.bindType = 'spaceFuDai'
        self.modelMap = {'initData': self.onInitData,
         'sendBuyInfo': self.onSendBuyInfo}
        self.bindInfo = {'Blue': 1,
         'Purple': 2,
         'Glod': 3}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACE_FUDAI, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACE_FUDAI:
            self.mediator = mediator

    def onSendBuyInfo(self, *arg):
        bonusType = int(arg[3][0].GetNumber())
        totleNumber = int(arg[3][1].GetNumber())
        if bonusType < 3:
            self.confirmBuyAllPreviewItems(bonusType, totleNumber)
        else:
            totalPay = PZBD.data.get(bonusType, {}).get('coinNeed', 30.0) * totleNumber
            msg = gameStrings.TEXT_SPACEFUDAIPROXY_40 % totalPay
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmBuyAllPreviewItems, bonusType, totleNumber))

    def confirmBuyAllPreviewItems(self, bonusType, totleNumber):
        p = BigWorld.player()
        p.cell.addZoneBonus(bonusType, totleNumber)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACE_FUDAI)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACE_FUDAI)

    def reset(self):
        pass

    def onInitData(self, *args):
        p = BigWorld.player()
        fudaiInfo = {'Glod': 10,
         'Blue': 20,
         'Purple': 30,
         'yunBi': 10000,
         'GlodTips': '',
         'BlueTips': '',
         'PurpleTips': '',
         'tianBi': 0}
        fudaiInfo['yunBi'] = p.cash
        fudaiInfo['BlueTips'] = PZBD.data.get(1, {}).get('tips', '')
        fudaiInfo['Blue'] = PZBD.data.get(1, {}).get('cashNeed', 10.0)
        fudaiInfo['PurpleTips'] = PZBD.data.get(2, {}).get('tips', '')
        fudaiInfo['Purple'] = PZBD.data.get(2, {}).get('cashNeed', 20.0)
        fudaiInfo['GlodTips'] = PZBD.data.get(3, {}).get('tips', '')
        fudaiInfo['Glod'] = PZBD.data.get(3, {}).get('coinNeed', 30.0)
        fudaiInfo['tianBi'] = p.getTianBi()
        return uiUtils.dict2GfxDict(fudaiInfo, True)
