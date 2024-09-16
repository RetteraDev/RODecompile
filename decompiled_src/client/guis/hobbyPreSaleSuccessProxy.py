#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hobbyPreSaleSuccessProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from data import hobby_presale_schedule_data as HPSD
from data import hobby_presale_config_data as HPCD

class HobbyPreSaleSuccessProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HobbyPreSaleSuccessProxy, self).__init__(uiAdapter)
        self.widget = None
        self.goodsId = -1
        self.code = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOBBY_PRESALE_SUCCESS, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HOBBY_PRESALE_SUCCESS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOBBY_PRESALE_SUCCESS)

    def reset(self):
        self.goodsId = -1
        self.code = ''

    def show(self, ok, goodsId, code, rc, errCode):
        if ok:
            self.goodsId = goodsId
            self.code = code
            if self.widget:
                self.refreshInfo()
                return
            self.uiAdapter.loadWidget(uiConst.WIDGET_HOBBY_PRESALE_SUCCESS, isModal=True)
        else:
            if rc < 0:
                msg = HPCD.data.get('reserveOvertime', '')
            elif errCode == 1001:
                msg = HPCD.data.get('alreadyGeted', '')
            elif errCode == 1002:
                msg = HPCD.data.get('alreadyFinished', '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def initUI(self):
        self.widget.copyCode.addEventListener(events.MOUSE_CLICK, self.handleCopyClick, False, 0, True)
        self.widget.confirm.addEventListener(events.MOUSE_CLICK, self.handleCloseClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.orderGoodsName.text = gameStrings.HOBBY_PRESALE_RESERVE_NAME % HPSD.data.get(self.goodsId, 0).get('name', '')
        self.widget.orderCode.text = self.code
        self.widget.effectDate.text = gameStrings.HOBBY_PRESALE_TIME_LIMIT % HPSD.data.get(self.goodsId, 0).get('validTime', '')
        self.widget.linkToShop.htmlText = HPCD.data.get('successGuide', {})

    def handleCopyClick(self, *args):
        codeText = self.widget.orderCode.text
        BigWorld.setClipBoardText(codeText)

    def handleCloseClick(self, *args):
        self.hide()
        if gameglobal.rds.ui.hobbyPreSaleShop.widget:
            gameglobal.rds.ui.hobbyPreSaleShop.hide()

    def showHobbyPush(self, ok, goodsId, code, rc, errCode):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_HOBBY_PRESALE_SUCCESS_STATE)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_HOBBY_PRESALE_SUCCESS_STATE, {'click': Functor(self.show, ok, goodsId, code, rc, errCode)})
