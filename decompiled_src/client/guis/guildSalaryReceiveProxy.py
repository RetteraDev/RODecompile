#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildSalaryReceiveProxy.o
import time
import BigWorld
from uiProxy import UIProxy
import gameglobal
import utils
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class GuildSalaryReceiveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildSalaryReceiveProxy, self).__init__(uiAdapter)
        self.modelMap = {'getSalarylist': self.onGetSalaryList,
         'getSalary': self.onGetSalary}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SALARY_RECEIVE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SALARY_RECEIVE:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SALARY_RECEIVE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SALARY_RECEIVE)

    def onGetSalaryList(self, *arg):
        return self._getSalaryList()

    def _getSalaryList(self):
        ret = []
        now = utils.getNow()
        payments = BigWorld.player().guild.memberMe.payments.values()
        for payment in payments:
            if payment.tExpire > now and not payment.tPaid:
                paymentObj = {}
                paymentObj['mtype'] = payment.mtype
                paymentObj['nuid'] = payment.nuid
                paymentObj['amount'] = payment.amount
                beginT = time.localtime(payment.tWhen)
                endT = time.localtime(payment.tExpire)
                paymentObj['time'] = time.strftime('%Y-%m-%d %H:%M', beginT)
                paymentObj['endtime'] = time.strftime('%Y-%m-%d  %H:%M', endT)
                ret.append(paymentObj)

        ret = sorted(ret, key=lambda x: x['time'], reverse=True)
        return uiUtils.array2GfxAarry(ret, True)

    def onGetSalary(self, *arg):
        nuid = long(arg[3][0].GetString())
        mtype = int(arg[3][1].GetNumber())
        amount = int(arg[3][2].GetNumber())
        p = BigWorld.player()
        if nuid == '0':
            p.showGameMsg(GMDD.data.SALARY_RECEIVE_NONE_SELECITEM_ITEM, ())
            return
        p.cell.getGuildPayment(mtype, nuid, amount)

    def updateView(self):
        data = self._getSalaryList()
        if self.mediator:
            self.mediator.Invoke('updateView', data)
