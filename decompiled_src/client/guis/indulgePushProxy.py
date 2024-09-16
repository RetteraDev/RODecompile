#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/indulgePushProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import const
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class IndulgePushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(IndulgePushProxy, self).__init__(uiAdapter)
        self.modelMap = {'goto': self.onGoto,
         'check': self.onCheck}
        self.mediator = None
        self.lastSt = 0
        self.msg = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_INDULGE_PUSH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INDULGE_PUSH:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INDULGE_PUSH)

    def show(self):
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INDULGE_PUSH)

    def refreshInfo(self):
        if self.mediator:
            info = {'msg': self.msg}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def pushMsg(self, onlineTime, offlineTime, st):
        if st == const.INDULGE_PROFIT_HALF_TIRED:
            self.msg = uiUtils.getTextFromGMD(GMDD.data.ANTIINDULGE_HALF_TIRED_NOTIFY, '')
        elif st == const.INDULGE_PROFIT_TIRED:
            self.msg = uiUtils.getTextFromGMD(GMDD.data.ANTIINDULGE_TIRED_NOTIFY, '')
        else:
            self.msg = uiUtils.getTextFromGMD(GMDD.data.ANTIINDULGE_LOGIN_NOTIFY, '%s') % uiUtils.formatTime(onlineTime)
        self.refreshInfo()
        if self.lastSt != st:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_INDULGE_PUSH)
        self.lastSt = st
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_INDULGE_PUSH)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_INDULGE_PUSH, {'click': self.show})

    def clearMsg(self):
        self.hide()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_INDULGE_PUSH)

    def onGoto(self, *arg):
        url = SCD.data.get('indulgeUrl', 'http://reg.163.com/smdj/index.jsp')
        BigWorld.openUrl(url)

    def onCheck(self, *arg):
        BigWorld.player().base.updateIndulgeStage()
        self.hide()
