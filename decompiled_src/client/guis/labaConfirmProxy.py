#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/labaConfirmProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
from data import laba_config_data as LCD

class LabaConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LabaConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'ClickConfirmBtn': self.onClickConfirmBtn,
         'getLabaInfo': self.onGetLabaInfo}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_LABA_CONFIRM, self.hide)

    def reset(self):
        self.mediator = None
        self.labaId = None
        self.page = None
        self.pos = None
        self.useType = None

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LABA_CONFIRM)

    def show(self, labaId, useType, page, pos):
        self.labaId = labaId
        self.useType = useType
        self.page = page
        self.pos = pos
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LABA_CONFIRM)

    def onASWidgetClose(self, *arg):
        self.hide()

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def getTypeNameById(self, labaId):
        ret = ''
        lData = LCD.data.get(labaId, {})
        _type = lData.get('type', -1)
        _str = lData.get('typeDesc', '')
        if (_type == gametypes.LABA_TEMPLATE_SELF_SERVER or _type == gametypes.LABA_TEMPLATE_CROSS_SERVER) and _str:
            ret = _str
        return ret

    def getMsgById(self, labaId):
        p = BigWorld.player()
        ret = ''
        lcdData = LCD.data.get(labaId, {})
        msg = lcdData.get('msg')
        msgArgs = lcdData.get('msgArgs')
        if msg:
            if msgArgs:
                argMap = {'roleName': p.roleName,
                 'serverName': gameglobal.rds.hostName,
                 'ownerGbID': p.gbId,
                 'hostId': int(gameglobal.rds.gServerid)}
                args = tuple([ argMap.get(k) for k in msgArgs ])
                try:
                    ret = msg % args
                except:
                    ret = gameStrings.TEXT_LABACONFIRMPROXY_73

            else:
                ret = msg
        return ret

    def getTitleName(self, labaId):
        titleStr = LCD.data.get(labaId, {}).get('title', gameStrings.TEXT_LABACONFIRMPROXY_80)
        return titleStr

    def onGetLabaInfo(self, *args):
        ret = {}
        ret['typeName'] = self.getTypeNameById(self.labaId)
        ret['msg'] = self.getMsgById(self.labaId)
        ret['titleName'] = self.getTitleName(self.labaId)
        return uiUtils.dict2GfxDict(ret, True)

    def onClickConfirmBtn(self, *args):
        p = BigWorld.player()
        p.cell.usePreDefinedLaba(self.page, self.pos, self.labaId, self.useType)
        self.hide()
