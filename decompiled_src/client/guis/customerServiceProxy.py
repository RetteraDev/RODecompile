#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/customerServiceProxy.o
import json
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
TYPE_WEB_LINK = 0
TYPE_SPRITE = 1
TYPE_SECOND = 2
TYPE_USER_BIND_PAGE = 3

class CustomerServiceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CustomerServiceProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmRequest': self.onConfirmRequest,
         'refreshContent': self.onRefreshContent}
        self.buttonData = []
        self.announcement = ''
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CUSTOMER_SERVICE, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CUSTOMER_SERVICE:
            self.mediator = mediator

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CUSTOMER_SERVICE)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CUSTOMER_SERVICE)

    def onRefreshContent(self, *args):
        if self.mediator:
            self.mediator.Invoke('setAnnouncement', GfxValue(gbk2unicode(self.announcement)))
            self.mediator.Invoke('setButtonData', uiUtils.array2GfxAarry(self.buttonData, True))

    def onConfirmRequest(self, *args):
        idx = int(args[3][0].GetNumber())
        if idx < len(self.buttonData):
            data = self.buttonData[idx]
            if data['btnType'] == TYPE_WEB_LINK:
                BigWorld.openUrl(data['content'])
            elif data['btnType'] == TYPE_SPRITE:
                gameglobal.rds.ui.help.show(data['content'])
            elif data['btnType'] == TYPE_SECOND:
                gameglobal.rds.ui.customerServiceSecond.queryToShow(idx)
            elif data['btnType'] == TYPE_USER_BIND_PAGE:
                if gameglobal.rds.configData.get('enableBindReward', False):
                    gameglobal.rds.ui.accountBind.show()
                else:
                    gameglobal.rds.ui.userAccountBind.show()

    def queryToShow(self):
        p = BigWorld.player()
        if p:
            if p.__class__.__name__ == 'PlayerAvatar':
                p.base.getCustomerServiceAnnouncement()

    def showCallBack(self, announcement, category):
        self.buttonData = []
        for item in category:
            if item:
                itemData = json.loads(item, encoding=utils.defaultEncoding())
                newData = {}
                newData['content'] = itemData['Content'].encode(utils.defaultEncoding())
                newData['btnName'] = itemData['BtnName'].encode(utils.defaultEncoding())
                newData['btnType'] = int(itemData['BtnType'])
                self.buttonData.append(newData)

        self.announcement = announcement
        self.show()
