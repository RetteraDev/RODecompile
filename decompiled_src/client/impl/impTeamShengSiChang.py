#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTeamShengSiChang.o
import BigWorld
import gameglobal
import gametypes
import const
import gamelog
import utils
from cdata import game_msg_def_data as GMDD
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from data import sheng_si_chang_data as SSCD
SSC_START = 1
SSC_QUIT = 2
MONSTER_BLOOD_NUM = 0
MONSTER_BLOOD_PERSENT = 1

class ImpTeamShengSiChang(object):

    def enterTeamSSCBefore(self):
        gameglobal.rds.ui.target.setHpMode(MONSTER_BLOOD_PERSENT)
        self.shengSiChangFbNo = const.FB_NO_TEAM_SHENG_SI_CHANG
        gameglobal.rds.ui.teamSSCMsgBox.onEnterTeamSSC()
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        filterWidgets = [uiConst.WIDGET_CHAT_LOG,
         uiConst.WIDGET_BF_STATS,
         uiConst.WIDGET_BULLET,
         uiConst.WIDGET_SKILL_PUSH,
         uiConst.WIDGET_DEAD_RELIVE,
         uiConst.WIDGET_ARENA_COUNT_DOWN,
         uiConst.WIDGET_FEEDBACK_ICON,
         uiConst.WIDGET_ACTIVITY_HALL_ICON,
         uiConst.WIDGET_REWARD_GIFT_ACTIVITY_ICONS,
         uiConst.WIDGET_TEAM_SSC_STATE,
         uiConst.WIDGET_TEAM_SSC_MSGBOX,
         uiConst.WIDGET_BUFF_LISTENER_SHOW]
        filterWidgets.extend(uiConst.HUD_WIDGETS)
        gameglobal.rds.ui.unLoadAllWidget(filterWidgets)
        gameglobal.rds.ui.map.realClose()
        gameglobal.rds.ui.player.setName(const.SSC_ROLENAME)
        gameglobal.rds.ui.player.setLv(self.lv)
        self.topLogo.hideName(True)
        self.topLogo.hideAvatarTitle(True)
        self.showCancelHideInBFConfirm()
        gameglobal.CLAN_WAR_FASHION_TYPE = gameglobal.CLAN_WAR_FASHION_TYPE_NO_COLOR
        uiUtils.enabledClanWarArmorMode()

    def onLeaveTeamShengSiChang(self):
        gameglobal.rds.ui.target.setHpMode(MONSTER_BLOOD_NUM)
        gameglobal.rds.ui.player.setName(self.roleName)
        gameglobal.rds.ui.player.setLv(self.lv)
        self.topLogo.updateRoleName(self.topLogo.name)
        self.topLogo.hideName(gameglobal.gHidePlayerName)
        self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
        self.motionUnpin()
        self.isNeedCounting = False
        if hasattr(self, 'operation'):
            self.operation['commonSetting'][17] = 0
            self.sendOperation()
            gameglobal.CLAN_WAR_FASHION_TYPE = gameglobal.CLAN_WAR_FASHION_TYPE_COLOR
            uiUtils.setClanWarArmorMode()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        gameglobal.rds.ui.teamSSCMsgBox.onLeaveTeamSSC()
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()
        self.addTeamSSCFriend()

    def addTeamSSCFriend(self):
        if not getattr(self, 'teamSSCMemberData', {}):
            return
        mateGbId = self.teamSSCMemberData.keys()[0]
        if self.friend.isFriend(mateGbId):
            return
        gameglobal.rds.ui.addFriendPop.show(gametypes.GET_ZONE_TOUCH_NUM_FOR_TEAM_SSC_END, self.teamSSCMemberData)

    def onNotifyTeamShengSiChangStart(self, isFirstRound):
        """
        \xe5\x8f\x8c\xe4\xba\xba\xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe5\xbc\x80\xe5\x90\xaf\xe9\x80\x9a\xe7\x9f\xa5
        Returns:
        
        """
        self.setTeamSSCCountDownInfo(isFirstRound)
        gamelog.debug('@hjx team ssc#onNotifyTeamShengSiChangStart:', isFirstRound)
        if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and not isFirstRound:
            if getattr(self, 'enterTeamSSCCallBack', None):
                BigWorld.cancelCallback(self.enterTeamSSCCallBack)
            quitTime = SSCD.data.get(BigWorld.player().getShengSiChangFbNo(), {}).get('quitTime', 30)
            self.enterTeamSSCCallBack = BigWorld.callback(quitTime, self.delayShowTeamSSCMsgBox)
        else:
            gameglobal.rds.ui.teamSSCMsgBox.showConfirmMsg(isFirstRound)
            BigWorld.callback(3, Functor(gameglobal.rds.ui.teamSSCMsgBox.checkEnterWndShow, isFirstRound))
        uiUtils.showWindowEffect()

    def setTeamSSCCountDownInfo(self, isFirst):
        if isFirst:
            totalTime = const.DUEL_PREPARE_DELAY
        else:
            quitTime = SSCD.data.get(BigWorld.player().getShengSiChangFbNo(), {}).get('quitTime', 30)
            roundIntervalTime = SSCD.data.get(const.FB_NO_TEAM_SHENG_SI_CHANG, {}).get('nextRoundPrepareTime', 120)
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
                totalTime = quitTime + roundIntervalTime
            else:
                totalTime = quitTime + roundIntervalTime - 10
        data = {'totalTime': totalTime,
         'startTime': utils.getNow(),
         'isFirst': isFirst}
        self.teamSSCCountDownData = data

    def delayShowTeamSSCMsgBox(self):
        if self.inWorld:
            gameglobal.rds.ui.teamSSCMsgBox.showConfirmMsg(False)

    def autoConfirmEnterTeamSSC(self):
        if self.inWorld:
            self.cell.confirmEnterTeamShengSiChang()

    def notifyInvitedTeamShengSiChang(self, invitorRoleName):
        """
        \xe8\xa2\xab\xe4\xba\xba\xe9\x82\x80\xe8\xaf\xb7\xe5\x8f\x82\xe4\xb8\x8e\xe5\x8f\x8c\xe4\xba\xba\xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba
        Args:
            invitorRoleName:  \xe9\x82\x80\xe8\xaf\xb7\xe8\x80\x85\xe5\xa7\x93\xe5\x90\x8d
        Returns:`
        
        """
        gameglobal.rds.ui.teamSSCMsgBox.showInviteApplyMsg(invitorRoleName)

    def onTeamShengSiChangLuckyGuyNotify(self):
        """
        \xe8\xbd\xae\xe7\xa9\xba\xe9\x80\x9a\xe7\x9f\xa5
        Returns:
        
        """
        gamelog.debug('@hjx team ssc#teamShengSiChangLuckyGuyNotify')
        msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_LUCKY_GUY_NOTIFY, 'luck')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def onTeamShengSiChangCurRoundEndNotify(self):
        """
        \xe6\x9c\xac\xe8\xbd\xae\xe7\xbb\x93\xe6\x9d\x9f
        Returns:
        
        """
        gamelog.debug('@hjx team ssc#onTeamShengSiChangCurRoundEndNotify')
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()

    def onApplyTeamShengSiChangSucc(self, mateGbId, mateRoleName):
        """
        \xe5\x9b\xa2\xe9\x98\x9f\xe7\x94\xb3\xe8\xaf\xb7\xe5\x8f\x8c\xe4\xba\xba\xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe6\x88\x90\xe5\x8a\x9f
        Args:
            mateGbId:  \xe9\x98\x9f\xe5\x8f\x8b\xe7\x9a\x84gbId
            mateRoleName: \xe9\x98\x9f\xe5\x8f\x8b\xe7\x9a\x84\xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d
        
        Returns:
        
        """
        if uiUtils.isJieQiTgt(mateGbId):
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_INTIMACY
        elif uiUtils.isMentor(mateGbId):
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_MENTOR
        elif uiUtils.isApprentice(mateGbId):
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_APPRENTICE
        elif uiUtils.isSameMentor(mateGbId):
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_DISCIPLES
        elif self.friend.isFriend(mateGbId):
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_FRIEND
        elif self.isInTeamOrGroup():
            msgId = GMDD.data.TEAM_SHENG_SI_CHANG_APPLY_SUCC_WITH_MATE
        msg = uiUtils.getTextFromGMD(msgId, 'apply together with %s') % mateRoleName
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def onTeamSSCChangCiEndNotify(self, cnt):
        """
        \xe5\x8f\x8c\xe4\xba\xba\xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe5\x9c\xba\xe6\xac\xa1\xe7\xbb\x93\xe6\x9d\x9f
        Args:
            cnt: \xe6\xb2\xa1\xe7\xbb\x93\xe6\x9d\x9f\xe5\x9c\xba\xe6\xac\xa1
        
        Returns:
        
        """
        self.teamSSCRoundNotFinishCnt = cnt
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()

    def teamShengSiChangEndNotify(self, mateGbId, mateRoleName, result, mateLv, mateSchool, isFinalMatch):
        """
        \xe6\x9c\xac\xe5\x9c\xba\xe6\xac\xa1\xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe7\xbb\x93\xe6\x9d\x9f\xe4\xba\x86
        Args:
            mateGbId:  \xe9\x98\x9f\xe5\x8f\x8b\xe7\x9a\x84gbId
            mateRoleName: \xe9\x98\x9f\xe5\x8f\x8b\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97
            result:  \xe7\xbb\x93\xe6\x9e\x9c
            mateLv: \xe9\x98\x9f\xe5\x8f\x8b\xe7\xad\x89\xe7\xba\xa7
            mateSchool: \xe9\x98\x9f\xe5\x8f\x8b\xe8\x81\x8c\xe4\xb8\x9a
            isFinalMatch: \xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe5\x9c\xba
        Returns:
        
        """
        gamelog.debug('@hjx team ssc#teamShengSiChangEndNotify:end ', self.id, mateGbId, mateRoleName, result, mateLv, mateSchool)
        if mateGbId and mateLv and mateSchool:
            self.teamSSCMemberData = {mateGbId: {'roleName': mateRoleName,
                        'level': mateLv,
                        'school': mateSchool}}
        else:
            self.teamSSCMemberData = {}
        if result:
            if isFinalMatch:
                self.showGameMsg(GMDD.data.TEAM_SSC_WIN_FINAL, ())
            else:
                self.showGameMsg(GMDD.data.TEAM_SSC_WIN_ROUND, ())
            gameglobal.rds.ui.teamSSCMsgBox.showRoundWinMsg(isFinalMatch)
        elif self.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            self.showGameMsg(GMDD.data.TEAM_SSC_LOSE_ROUND, ())
        else:
            self.addTeamSSCFriend()
        if self.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_QUIT_IN_30S, ())
            self.addTimerCount(SSC_QUIT, uiUtils.getDuelCountTime('quitTime', self.getShengSiChangFbNo()))

    def teamShengSiChangCountDown(self, occupyTime):
        """
        \xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe5\x80\x92\xe8\xae\xa1\xe6\x97\xb6
        Args:
            occupyTime: \xe7\x94\x9f\xe6\xad\xbb\xe5\x9c\xba\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4
        
        Returns:
        
        """
        gamelog.debug('@hjx team ssc#teamShengSiChangCountDown: ', self.id, occupyTime)
        uiUtils.enabledClanWarArmorMode()
        gameglobal.rds.ui.arena.openArenaMsg()
        self.addTimerCount(SSC_START, uiUtils.getDuelCountTime('readyTime', self.getShengSiChangFbNo()), occupyTime)
