#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inGameEvaluationProxy.o
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst

class InGameEvaluationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InGameEvaluationProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'submitResult': self.submitResult}
        self.urs = -1
        self.aid = -1
        self.mediator = None
        self.keyMembers = ['isDetail',
         'solved',
         'nps',
         'feeling',
         'react_speed',
         'gm_communication_skill',
         'gm_service_quality',
         'gm_mark']
        uiAdapter.registerEscFunc(uiConst.WIDGET_INGAME_EVALUATION, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INGAME_EVALUATION:
            self.mediator = mediator

    def show(self, urs, aid):
        self.urs = urs
        self.aid = aid
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INGAME_EVALUATION)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INGAME_EVALUATION)

    def submitResult(self, *arg):
        data = arg[3][0]
        ret = {}
        for m in self.keyMembers:
            if data.GetMember(m):
                ret[m] = int(data.GetMember(m).GetNumber())

        if len(ret) == 0:
            return
        BigWorld.player().base.evalFeedbackReport(self.urs, self.aid, ret.keys(), ret.values())
        self.hide()
