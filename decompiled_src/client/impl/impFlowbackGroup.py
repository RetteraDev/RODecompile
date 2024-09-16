#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFlowbackGroup.o
from gamestrings import gameStrings
import gamelog
import gametypes
import gameglobal
import const
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class ImpFlowbackGroup(object):

    def onReceiveFlowbackTargetReward(self, ret):
        gamelog.info('@zmm onReceiveFlowbackTargetReward', ret)
        if ret == gametypes.FLOWBACK_GROUP_TARGET_REWARD_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_TARGET_REWARD_SUC, ())
            gameglobal.rds.ui.backflowCatchExp.refreshInfo()
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_TARGET_REWARD_FAIL, ())

    def confirmReceiveFlowbackTargetReward(self, targetId):
        msg = gameglobal.rds.ui.arena.genConfirmDesc(gameStrings.TEXT_IMPFLOWBACKGROUP_28)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doConfirmReceiveFlowbackTargetReward, targetId), yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_128, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmReceiveFlowbackTargetReward(self, targetId):
        self.cell.receiveFlowbackTargetReward(targetId, False)

    def confirmReceiveFlowbackTargetPointReward(self):
        msg = gameglobal.rds.ui.arena.genConfirmDesc(gameStrings.TEXT_IMPFLOWBACKGROUP_28)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._doConfirmReceiveFlowbackTargetPointReward, yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_128, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmReceiveFlowbackTargetPointReward(self):
        self.cell.receiveFlowbackGroupTargetPointReward(False)

    def onReceiveFlowbackPrivilegeReward(self, ret):
        gamelog.info('@zmm onReceiveFlowbackPrivilegeReward', ret)
        if ret == gametypes.FLOWBACK_GROUP_PRIVILEGE_REWARD_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_PRIVILEGE_REWARD_SUC, ())
            gameglobal.rds.ui.backflowPriviege.refreshInfo()
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_PRIVILEGE_REWARD_FAIL, ())

    def onReceiveFlowbackRechargeReward(self, ret):
        gamelog.info('@zmm onReceiveFlowbackRechargeReward', ret)
        if ret == gametypes.FLOWBACK_GROUP_RECHARGE_REWARD_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_RECHARGE_REWARD_SUC, ())
            gameglobal.rds.ui.backflowDiscount.refreshInfo()
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.FLOWBACK_GROUP_REWARD_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_FLOWBACK_GROUP_RECHARGE_REWARD_FAIL, ())
