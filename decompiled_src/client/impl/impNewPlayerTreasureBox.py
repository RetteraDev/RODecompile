#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNewPlayerTreasureBox.o
import gamelog
import gametypes
import gameglobal
import utils
import const
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import game_msg_data as GMD
MAX_CHOOSE_NUM = 8

class ImpNewPlayerTreasureBox(object):

    def chatNpcCreateTreasureBox(self):
        if not gameglobal.rds.configData.get('enableNewPlayerTreasureBox', False):
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SYSTEM_NIOT_OPEN)
            return
        tWhen = utils.getNow()
        beginTime = SCD.data.get('ntBeginTime', '0 0 * * 3 *')
        endTime = SCD.data.get('ntEndTime', '0 9 * * 3 *')
        if tWhen < utils.getDisposableCronTabTimeStamp(endTime) and utils.getDisposableCronTabTimeStamp(endTime) < utils.getDisposableCronTabTimeStamp(beginTime):
            self.showGameMsg(GMDD.data.NEW_PLAYER_TREASURE_BOX_NOT_IN_VALID_TIME, ())
            return
        if self.ntStatus not in [gametypes.NT_STATUS_NPC_NO_TRIGGER]:
            if self.ntStatus == gametypes.NT_STATUS_HELP_NEW_PLAYER_OPEN_BOX:
                self.showGameMsg(GMDD.data.NEW_PLAYER_TREASURE_BOX_STATE_HELP, ())
            elif self.ntStatus == gametypes.NT_STATUS_NPC_TRIGGER_AND_NO_OPEN_BOX:
                self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.NEWP_TREASURE_BOX_OPENING_BOX,))
            else:
                self.showGameMsg(GMDD.data.NEW_PLAYER_TREASURE_BOX_NOT_TIGGER, ())
            return
        self.cell.getNewPlayerMaxNum()

    def onGetNewPlayerMaxNum(self, maxCnt):
        gamelog.debug('zmm #impNewPlayerTreasureBox onGetNewPlayerMaxNum client', maxCnt)
        if maxCnt >= 500:
            self.showGameMsg(GMDD.data.NEW_PLAYER_CREATE_TREASURE_BOX_TOO_MANY, ())
            return
        elif self.isInTeamOrGroup():
            msg = GMD.data.get(GMDD.data.NEW_PLAYER_TREASURE_BOX_CONFIRM_LEAVE, {}).get('text', gameStrings.FRIEND_TREASURE_BOX_INGROUP)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._doQuitGroup, yesBtnText=gameStrings.CONFIRM, noCallback=None, noBtnText=gameStrings.CANCEL)
            return
        elif not self.isInTeam() and not self.isInGroup():
            gameglobal.rds.ui.team.quickCreateGroup(gametypes.TEAM_REASON_NEW_PLAYER_TREASURE)
            return
        else:
            return

    def chatToWorldForNT(self):
        lastChatTime = getattr(self, 'lastChatTime', 0)
        if lastChatTime and abs(utils.getNow() - lastChatTime) < 30:
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.NPC_FUNC_INVITE_TEAM_FOR_NEW_PLAYER_TREASURE_BOX) % self.roleName
        msg = uiUtils.generateStr(msg)
        if not msg:
            return
        self.lastChatTime = utils.getNow()
        self.cell.chatToWorldWithoutCostForAction(msg + ':role', 0, const.NORMAL_CHAT_MSG)

    def checkGetNewPlayerReward(self):
        if not self.ntPartnerGbId:
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.NEWP_TREASURE_BOX_CHECK_NO_PARTNER)
            return False
        if not self.isInTeamOrGroup():
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.NEWP_TREASURE_BOX_CHECK_GET_REWARD)
            return False
        if not self.isTeamLeader():
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.NEWP_TREASURE_BOX_CHECK_GET_REWARD)
            return False
        members = getattr(self, 'members', {})
        if self.ntPartnerGbId and self.ntPartnerGbId in members:
            pass
        else:
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.NEWP_TREASURE_BOX_CHECK_GET_REWARD)
            return False
        if len(members) != 2:
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.NEWP_TREASURE_BOX_CHECK_INVALID_TEAM_NUMBER)
            return False
        return True

    def chatNpcNewPlayerReward(self):
        if self.checkGetNewPlayerReward():
            self.cell.getParterNewPlayerReward()
