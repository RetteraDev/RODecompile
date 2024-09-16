#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBusinessDelegateProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class GuildBusinessDelegateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBusinessDelegateProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'confirm': self.onConfirm}
        self.mediator = None
        self.entityId = 0
        self.op = 0
        self.businessDelegations = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUSINESS_DELEGATE:
            self.mediator = mediator

    def reset(self):
        self.entityId = 0
        self.op = 0
        self.businessDelegations = None

    def needShow(self, entityId, op):
        self.entityId = entityId
        self.op = op
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return
        npc.cell.fetchDelegationBusinessQuestLoop()

    def show(self, businessDgts):
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            self.hide()
            return
        if self.op == gametypes.BUSINESS_NPC_OPTION_VIEW:
            self.businessDelegations = businessDgts
            if self.mediator:
                self.refreshInfo()
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE)
        elif self.op == gametypes.BUSINESS_NPC_OPTION_PUBLISH:
            gameglobal.rds.ui.guildBusinessDelegatePublish.show(self.entityId, businessDgts)
        elif self.op == gametypes.BUSINESS_NPC_OPTION_ABANDON:
            gameglobal.rds.ui.guildBusinessDelegatePublish.showAbandon(self.entityId, businessDgts)
        else:
            self.hide()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def onGetInfo(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            delegateList = []
            for nuid, delegation in self.businessDelegations.iteritems():
                itemInfo = {}
                itemInfo['dgtNUID'] = str(nuid)
                itemInfo['questLoopId'] = delegation.questLoopId if hasattr(delegation, 'questLoopId') else 0
                itemInfo['playerName'] = delegation.roleName if hasattr(delegation, 'roleName') else ''
                dgtCnt = delegation.dgtCnt if hasattr(delegation, 'dgtCnt') else 0
                useCnt = 0
                finishCnt = 0
                for accDgt in delegation.itervalues():
                    if accDgt.isFinish():
                        finishCnt += 1
                    useCnt += 1

                itemInfo['allNum'] = '%d/%d/%d' % (useCnt, finishCnt, dgtCnt)
                itemInfo['canNum'] = dgtCnt - useCnt
                itemInfo['delegateFee'] = format(delegation.loopCashReward if hasattr(delegation, 'loopCashReward') else 0, ',')
                delegateList.append(itemInfo)

            info['delegateList'] = delegateList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        dgtNUID = int(arg[3][0].GetString())
        questLoopId = int(arg[3][1].GetNumber())
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_ACCEPT_HINT, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.accept, self.entityId, dgtNUID, questLoopId))

    def accept(self, entityId, dgtNUID, questLoopId):
        npc = BigWorld.entities.get(entityId)
        if not npc:
            self.hide()
            return
        npc.cell.acceptBusinessQuestLoop(questLoopId, dgtNUID)
        self.hide()
