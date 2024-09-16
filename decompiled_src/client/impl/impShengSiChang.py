#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impShengSiChang.o
from gamestrings import gameStrings
import gameglobal
import gametypes
import const
import gamelog
from crontab import CronTab
from cdata import game_msg_def_data as GMDD
from data import sheng_si_chang_data as SSCD
from guis import uiConst
from guis import uiUtils
SSC_START = 1
SSC_QUIT = 2
MONSTER_BLOOD_NUM = 0
MONSTER_BLOOD_PERSENT = 1

class ImpShengSiChang(object):

    def _refreshSSCInfo(self):
        if self.getShengSiChangFbNo() == const.FB_NO_SHENG_SI_CHANG:
            gameglobal.rds.ui.shengSiChang.refreshSSCStats(uiConst.SSC_STATS_IN_SSC)
        else:
            gameglobal.rds.ui.teamSSCState.onRefreshStateText()

    def shengSiChangQuery(self, statsInfo, sscStage):
        gamelog.debug('@hjx ssc#shengSiChangQuery:', statsInfo, sscStage)
        self.sscStatsInfo = statsInfo
        self.sscStage = sscStage
        self._refreshSSCInfo()

    def showShengSiChangConfirmMsg(self, shengSiChangPrepareTimestamp):
        gamelog.debug('@hjx ssc#showShengSiChangConfirmMsg:', shengSiChangPrepareTimestamp)
        gameglobal.rds.ui.shengSiChang.tipsTimeStamp = shengSiChangPrepareTimestamp
        gameglobal.rds.ui.shengSiChang.showConfirmTip(uiConst.SSC_TIPS_STAGE_START)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SHENG_SI_CHANG_START)
        self.shengSiChangFbNo = const.FB_NO_SHENG_SI_CHANG
        uiUtils.showWindowEffect()

    def onConfirmEnterShengSiChang(self):
        gamelog.debug('@hjx ssc#onConfirmEnterShengSiChang')
        gameglobal.rds.ui.shengSiChang.showConfirmTip(uiConst.SSC_TIPS_STAGE_WAITING)
        gameglobal.rds.ui.shengSiChang.setDesc(gameStrings.TEXT_IMPSHENGSICHANG_47)

    def onCancelEnterShengSiChang(self):
        gameglobal.rds.ui.shengSiChang.closeTips()

    def getShengSiChangFbNo(self):
        if hasattr(self, 'shengSiChangFbNo'):
            return self.shengSiChangFbNo
        else:
            return const.FB_NO_SHENG_SI_CHANG

    def onRoundEndNotify(self, result):
        gamelog.debug('@hjx ssc#onRoundEndNotify:', result)
        if result == const.WIN:
            gameglobal.rds.ui.shengSiChang.tipsTimeStamp = self.getServerTime()
            gameglobal.rds.ui.shengSiChang.showConfirmTip(uiConst.SSC_TIPS_STAGE_END)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SHENG_SI_CHANG_START)
            self.showGameMsg(GMDD.data.SSC_WIN_STAND_BY, ())
        elif result == const.LOSE:
            self.showGameMsg(GMDD.data.SSC_LOSE_ROUND, ())

    def onMatchFinalEndNotify(self):
        gamelog.debug('@hjx ssc#onMatchFinalEndNotify:', self.id)
        gameglobal.rds.ui.shengSiChang.showConfirmTip(uiConst.SSC_TIPS_STAGE_FINAL_END)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SHENG_SI_CHANG_START)
        self.showGameMsg(GMDD.data.SSC_WIN_FINAL_MATCH, ())

    def onNotifyCurRoundEnd(self):
        gamelog.debug('@hjx ssc#onNotifyCurRoundEnd:SSC_STATS_START_COUNTING:', self.id)
        gameglobal.rds.ui.shengSiChang.refreshSSCStats(uiConst.SSC_STATS_START_COUNTING, self.getServerTime())

    def onChangCiEndNotify(self, cnt):
        gamelog.debug('@hjx ssc#onChangCiEndNotify:SSC_STATS_STANDBY', cnt, self.id)
        if cnt == 0:
            return
        self.roundCurNotFinishedCnt = cnt
        gameglobal.rds.ui.shengSiChang.refreshSSCStats(uiConst.SSC_STATS_STANDBY)

    def quitWaitingShengSiChang(self, fbNo):
        gameglobal.rds.ui.shengSiChang.closeTips()

    def enterSSCBefore(self):
        gameglobal.rds.ui.target.setHpMode(MONSTER_BLOOD_PERSENT)
        gameglobal.rds.ui.shengSiChang.closeTips()
        filterWidgets = [uiConst.WIDGET_TEAM_INVITE_V2,
         uiConst.WIDGET_CHAT_LOG,
         uiConst.WIDGET_BF_STATS,
         uiConst.WIDGET_BULLET,
         uiConst.WIDGET_SKILL_PUSH,
         uiConst.WIDGET_DEAD_RELIVE,
         uiConst.WIDGET_ARENA_COUNT_DOWN,
         uiConst.WIDGET_FEEDBACK_ICON,
         uiConst.WIDGET_SHENG_SI_CHANG_STATS,
         uiConst.WIDGET_ACTIVITY_HALL_ICON,
         uiConst.WIDGET_REWARD_GIFT_ACTIVITY_ICONS,
         uiConst.WIDGET_BUFF_LISTENER_SHOW]
        filterWidgets.extend(uiConst.HUD_WIDGETS)
        gameglobal.rds.ui.unLoadAllWidget(filterWidgets)
        gameglobal.rds.ui.map.realClose()
        self.topLogo.updateRoleName(const.SSC_ROLENAME)
        self.topLogo.setAvatarTitle(const.SSC_TITLENAME, 1)
        self.topLogo.hideGuildIcon(True)
        self.topLogo.hideTitleEffect(True)
        gameglobal.rds.ui.player.setName(const.SSC_ROLENAME)
        gameglobal.rds.ui.player.setLv(self.lv)
        gameglobal.rds.ui.shengSiChang.closeSSCDelayNotify()
        self.showCancelHideInBFConfirm()
        gameglobal.CLAN_WAR_FASHION_TYPE = gameglobal.CLAN_WAR_FASHION_TYPE_NO_COLOR
        uiUtils.enabledClanWarArmorMode()
        self.resetEntityMark()

    def onLeaveShengSiChang(self):
        gameglobal.rds.ui.target.setHpMode(MONSTER_BLOOD_NUM)
        gameglobal.rds.ui.shengSiChang.closeTips()
        if self.shengSiChangStatus not in (gametypes.SHENG_SI_CHANG_STATUS_WIN_STANDBY, gametypes.SHENG_SI_CHANG_STATUS_NEW_RULE_SPECIAL):
            gameglobal.rds.ui.shengSiChang.closeSSCStats()
        elif gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and not self.isSSCFinalRound():
            gameglobal.rds.ui.shengSiChang.refreshSSCStats(uiConst.SSC_STATS_STANDBY)
        self.topLogo.updateRoleName(self.topLogo.name)
        name, style = self.getActivateTitleStyle()
        self.topLogo.setAvatarTitle(name, style)
        self.topLogo.hideGuildIcon(False)
        self.topLogo.hideTitleEffect(False)
        gameglobal.rds.ui.player.setName(self.roleName)
        gameglobal.rds.ui.player.setLv(self.lv)
        self.motionUnpin()
        self.isNeedCounting = False
        self.topLogo.hideName(gameglobal.gHidePlayerName)
        self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
        if hasattr(self, 'operation'):
            self.operation['commonSetting'][17] = 0
            self.sendOperation()
            gameglobal.CLAN_WAR_FASHION_TYPE = gameglobal.CLAN_WAR_FASHION_TYPE_COLOR
            uiUtils.setClanWarArmorMode()

    def shengSiChangCountDown(self, enterSSCTimeStamp):
        gamelog.debug('@hjx ssc#shengSiChangCountDown:', self.id, enterSSCTimeStamp)
        uiUtils.enabledClanWarArmorMode()
        gameglobal.rds.ui.shengSiChang.closeTips()
        gameglobal.rds.ui.arena.openArenaMsg()
        self.addTimerCount(SSC_START, uiUtils.getDuelCountTime('readyTime', self.getShengSiChangFbNo()), enterSSCTimeStamp)

    def shengSiChangEndNotify(self):
        gamelog.debug('@hjx ssc#shengSiChangEndNotify:', self.id)
        self.showGameMsg(GMDD.data.BATTLE_FIELD_QUIT_IN_30S, ())
        self.addTimerCount(SSC_QUIT, uiUtils.getDuelCountTime('quitTime', self.getShengSiChangFbNo()))

    def onSSCRoundNotify(self, curRound):
        gamelog.debug('@hjx ssc#onSSCRoundNotify:', curRound)
        self.sscStageLv = curRound + 1
        gameglobal.rds.ui.shengSiChang.onGetRoundInfo()
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()

    def onUpdateSSCCurLevel(self, curLevel):
        gamelog.debug('@hjx ssc#onUpdateSSCCurLevel:', curLevel)
        self.sscRankLv = curLevel + 1
        gameglobal.rds.ui.shengSiChang.onGetRoundInfo()
        gameglobal.rds.ui.teamSSCState.onRefreshStateText()

    def isSSCFinalRound(self):
        return getattr(self, 'sscStageLv', 0) >= SSCD.data.get(const.FB_NO_SHENG_SI_CHANG, {}).get('roundNum', 4) + 1

    def isTeamSSCFinalRound(self):
        return getattr(self, 'sscStageLv', 0) >= SSCD.data.get(const.FB_NO_TEAM_SHENG_SI_CHANG, {}).get('roundNum', 4) + 1

    def set_shengSiChangStatus(self, old):
        gamelog.debug('@dxk ssc#set_shengSiChangStatus:', self.shengSiChangStatus)
        if not gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
            return
        if self.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_DEFAULT:
            gameglobal.rds.ui.shengSiChang.closeSSCStats()
        elif self.shengSiChangStatus in (gametypes.SHENG_SI_CHANG_STATUS_WIN_STANDBY, gametypes.SHENG_SI_CHANG_STATUS_NEW_RULE_SPECIAL):
            if not self.isSSCFinalRound():
                gameglobal.rds.ui.shengSiChang.refreshSSCStats(uiConst.SSC_STATS_STANDBY)
