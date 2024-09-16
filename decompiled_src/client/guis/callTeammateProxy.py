#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/callTeammateProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import groupUtils
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from callbackHelper import Functor

class CallTeammateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CallTeammateProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'getInitData': self.onGetInitData}
        self.mediator = None
        self.sid = 0
        self.beCalledGbId = 0
        self.confirmHandler = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CALL_TEAMMATE, self.hide)

    def reset(self):
        self.sid = 0

    def show(self, sid):
        self.sid = sid
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CALL_TEAMMATE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CALL_TEAMMATE:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CALL_TEAMMATE)

    def onConfirm(self, *arg):
        gbid = int(arg[3][0].GetString())
        BigWorld.player().cell.useGuildMemberSkillWithGbId(self.sid, gbid)

    def onGetInitData(self, *arg):
        p = BigWorld.player()
        list = []
        for key, value in p._getMembers().iteritems():
            if key == p.gbId or not groupUtils.isInSameTeam(p.gbId, key):
                continue
            name = value.get('roleName', '')
            level = 'Lv.%d' % value.get('level', 0)
            isOn = value.get('isOn', False)
            list.append([str(key),
             name,
             level,
             isOn])

        return uiUtils.array2GfxAarry(list, True)

    def clearGbId(self):
        self.beCalledGbId = 0
        self.confirmHandler = 0

    def beCalled(self, gbId):
        if self.beCalledGbId == gbId:
            return
        if self.confirmHandler:
            gameglobal.rds.ui.messageBox.dismiss(self.confirmHandler)
        p = BigWorld.player()
        player = p._getMembers().get(gbId, {})
        if not player:
            return
        sex = gameStrings.TEXT_CALLTEAMMATEPROXY_70 if player.get('sex', const.SEX_MALE) == const.SEX_MALE else gameStrings.TEXT_CALLTEAMMATEPROXY_70_1
        msg = gameStrings.TEXT_CALLTEAMMATEPROXY_71 % (player.get('roleName'), sex, sex)
        self.beCalledGbId = gbId
        self.confirmHandler = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self._accept, gbId), noCallback=Functor(self._reject, gbId), yesBtnText=gameStrings.TEXT_CALLTEAMMATEPROXY_73, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False)

    def _accept(self, gbId):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CALLED_BY_TEAMMATE):
            BigWorld.callback(0.1, Functor(self.beCalled, gbId))
            return
        BigWorld.player().cell.acceptGuildCallTeamMate(gbId)

    def _reject(self, gbId):
        BigWorld.player().cell.rejectGuildCallTeamMate(gbId)
