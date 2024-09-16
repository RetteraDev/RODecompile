#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBusinessDelegatePublishProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from callbackHelper import Functor
from data import quest_loop_data as QLD
from data import business_config_data as BCD
from data import business_delegate_quest_data as BDQD
from cdata import game_msg_def_data as GMDD

class GuildBusinessDelegatePublishProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBusinessDelegatePublishProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.entityId = 0
        self.dailyDgtCnt = 0
        self.curDgtCnt = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE_PUBLISH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUSINESS_DELEGATE_PUBLISH:
            self.mediator = mediator
            self.refreshInfo()

    def reset(self):
        self.entityId = 0
        self.dailyDgtCnt = 0
        self.curDgtCnt = 0

    def hasDelegated(self, businessDgts):
        for nuid, delegation in businessDgts.iteritems():
            if hasattr(delegation, 'gbId') and delegation.gbId == BigWorld.player().gbId:
                return (True, nuid, delegation.questLoopId if hasattr(delegation, 'questLoopId') else 0)

        return (False, 0, 0)

    def showAbandon(self, entityId, businessDgts):
        existFlag, dgtNUID, questLoopId = self.hasDelegated(businessDgts)
        if not existFlag:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_NOT_EXIST, ())
            self.hide()
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_DGT_ABANDON_HINT, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.abandonDgt, entityId, dgtNUID, questLoopId))

    def abandonDgt(self, entityId, dgtNUID, questLoopId):
        npc = BigWorld.entities.get(entityId)
        if not npc:
            self.hide()
            return
        npc.cell.abandonDgtBusinessQuestLoop(questLoopId, dgtNUID)
        self.hide()

    def show(self, entityId, businessDgts):
        existFlag, _, _ = self.hasDelegated(businessDgts)
        if existFlag:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_EXIST, ())
            self.hide()
            return
        self.entityId = entityId
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            self.hide()
            return
        self.dailyDgtCnt = businessDgts.dailyDgtCnt if hasattr(businessDgts, 'dailyDgtCnt') else 0
        self.curDgtCnt = businessDgts.curDgtCnt if hasattr(businessDgts, 'curDgtCnt') else 0
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE_PUBLISH)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUSINESS_DELEGATE_PUBLISH)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            info = {}
            info['totalRound'] = self.dailyDgtCnt
            info['usableRound'] = self.dailyDgtCnt - self.curDgtCnt
            info['roundMaxCount'] = BCD.data.get('dgtCntPersonPerday', 0)
            info['roundDefaultText'] = gameStrings.TEXT_GUILDBUSINESSDELEGATEPUBLISHPROXY_96 % format(info['roundMaxCount'], ',')
            info['delegationMinCount'] = BCD.data.get('delegationMinFee', 0)
            info['delegationMaxCount'] = BCD.data.get('delegationMaxFee', 0)
            info['delegationDefaultText'] = gameStrings.TEXT_GUILDBUSINESSDELEGATEPUBLISHPROXY_100 % format(info['delegationMinCount'], ',')
            info['hint'] = gameStrings.TEXT_GUILDBUSINESSDELEGATEPUBLISHPROXY_102 % (format(info['delegationMinCount'], ','), format(info['delegationMaxCount'], ','))
            info['delegationFeeRate'] = BCD.data.get('delegationFeeRate', 0)
            info['own'] = p.cash
            npc = BigWorld.entities.get(self.entityId)
            if not npc:
                return
            questLoopId = BDQD.data.get(npc.npcId, {}).get('questLoopId', 0)
            info['contrib'] = QLD.data.get(questLoopId, {}).get('businessContrib', 0)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        loopCntInput = int(arg[3][0].GetNumber())
        loopCashRewardInput = int(arg[3][1].GetNumber())
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return
        questLoopId = BDQD.data.get(npc.npcId, {}).get('questLoopId', 0)
        npc.cell.delegateBusinessQuestLoop(questLoopId, loopCntInput, loopCashRewardInput)
        self.hide()
