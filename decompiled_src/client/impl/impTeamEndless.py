#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTeamEndless.o
import gamelog
import copy
import gameglobal
import gametypes
from guis import events

class ImpTeamEndless(object):
    """\xe8\xbd\xae\xe5\x9b\x9e\xe9\xa2\x86\xe5\x9f\x9f\xe5\x89\xaf\xe6\x9c\xac"""

    def updateTeamEndless(self, data):
        """
        \xe5\xa2\x9e\xe9\x87\x8f\xe6\x9b\xb4\xe6\x96\xb0teamEndless
        :param data: {lvType:{maxLv, maxEnableLv, bestRecordWeekly, progress:{lv:{onceRewardState, levelRewardState}}
        :return:
        """
        gamelog.debug('@zhangkuo updateTeamEndless', data)
        self.teamEndless.updateBySyncData(data)

    def onPushTeamEndlessGlobalInfo(self, fbType, affix, nextFbType, nextAffix):
        """\xe6\x9c\xac\xe5\x91\xa8\xe8\xbd\xae\xe5\x9b\x9e\xe9\xa2\x86\xe5\x9f\x9f\xe5\x89\xaf\xe6\x9c\xac\xe7\xb1\xbb\xe5\x9e\x8b\xe3\x80\x81\xe8\xaf\x8d\xe7\xbc\x80\xe4\xbf\xa1\xe6\x81\xaf"""
        gamelog.debug('@zhangkuo onPushTeamEndlessGlobalInfo', fbType, affix, nextFbType, nextAffix)
        self.teamEndlessGlobalInfo = {'fbType': fbType,
         'affix': affix,
         'nextFbType': nextFbType,
         'nextAffix': nextAffix}

    def onUpdateTeamEndlessProgress(self, bossOrder, progress):
        """\xe6\x9b\xb4\xe6\x96\xb0\xe5\x89\xaf\xe6\x9c\xac\xe8\xbf\x9b\xe5\xba\xa6"""
        gamelog.debug('@zhangkuo onUpdateTeamEndlessProgress', bossOrder, progress)
        gameglobal.rds.ui.voidLunHuiBar.onBossFinished(bossOrder, progress)

    def onQueryFriendTeamEndlessRank(self, data):
        """
        \xe6\x98\xbe\xe7\xa4\xba\xe8\xbe\xbe\xe5\x88\xb0\xe5\xaf\xb9\xe5\xba\x94\xe9\x9a\xbe\xe5\xba\xa6\xe7\x9a\x84\xe5\xa5\xbd\xe5\x8f\x8b\xe5\xa4\xb4\xe5\x83\x8f
        :param data: {\xe7\xad\x89\xe7\xba\xa7\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x9a{\xe9\x9a\xbe\xe5\xba\xa6\xef\xbc\x9a[gbId,]}}
        :return:
        """
        gamelog.debug('@zhangkuo onQueryFriendTeamEndlessRank', data)
        self.friendTeamEndlessRank = data
        gameglobal.rds.ui.voidLunHui.onGetFriendTeamEndlessRank()

    def onInviteEnterTeamEndless(self, fbNo, teamEndlessLv, players, timestamp):
        """
        \xe9\x82\x80\xe8\xaf\xb7\xe9\x98\x9f\xe5\x91\x98\xe8\xbf\x9b\xe5\x85\xa5\xe5\x89\xaf\xe6\x9c\xac
        :param fbNo: \xe5\x89\xaf\xe6\x9c\xac\xe5\x8f\xb7
        :param teamEndlessLv: \xe9\x9a\xbe\xe5\xba\xa6\xe7\xad\x89\xe7\xba\xa7
        :param players: [(gbId, roleName, photo, school),]
        :param timestamp: \xe5\x80\x92\xe8\xae\xa1\xe6\x97\xb6\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        :return:
        """
        gamelog.debug('@zhangkuo onInviteEnterTeamEndless', fbNo, teamEndlessLv, players, timestamp)
        playersInfo = {}
        for player in players:
            gbId = player[0]
            playerInfo = copy.deepcopy(self.members.get(gbId, {}))
            playerInfo['photo'] = player[2]
            playersInfo[gbId] = playerInfo

        startData = {'fbNo': fbNo,
         'teamEndlessLv': teamEndlessLv,
         'endTime': timestamp,
         'players': playersInfo}
        gameglobal.rds.ui.voidLunHuiStart.show(startData)

    def onConfirmEnterTeamEndless(self, gbID):
        """\xe9\x98\x9f\xe5\x91\x98\xe7\xa1\xae\xe8\xae\xa4\xe8\xbf\x9b\xe5\x85\xa5"""
        gamelog.debug('@zhangkuo onConfirmEnterTeamEndless', gbID)
        gameglobal.rds.ui.voidLunHuiStart.onPlayerReady(gbID)

    def onCancelEnterTeamEndless(self, gbID):
        """\xe9\x98\x9f\xe5\x91\x98\xe5\x8f\x96\xe6\xb6\x88\xe7\xa1\xae\xe8\xae\xa4"""
        gamelog.debug('@zhangkuo onCancelEnterTeamEndless', gbID)
        gameglobal.rds.ui.voidLunHuiStart.onPlayerRefuse(gbID)

    def onEndTeamEndless(self, isOk, teamEndlessLv, rank, friends, timeCost, fbNo, lastFriendRank, curFriendRank):
        """
        \xe5\x89\xaf\xe6\x9c\xac\xe7\xbb\x93\xe7\xae\x97
        :param isOk: \xe6\x98\xaf\xe5\x90\xa6\xe9\x80\x9a\xe5\x85\xb3
        :param teamEndlessLv: \xe9\x9a\xbe\xe5\xba\xa6\xe7\xad\x89\xe7\xba\xa7
        :param rank: \xe6\x9c\xac\xe6\x9c\x8d\xe6\x8e\x92\xe5\x90\x8d\xef\xbc\x8c0\xe8\xa1\xa8\xe7\xa4\xba\xe6\x9c\xaa\xe4\xb8\x8a\xe6\xa6\x9c
        :param friends: \xe5\xa5\xbd\xe5\x8f\x8b\xe6\x8e\x92\xe5\x90\x8d\xe4\xbf\xa1\xe6\x81\xaf
        :param timeCost: \xe8\x8a\xb1\xe8\xb4\xb9\xe6\x97\xb6\xe9\x97\xb4
        :param fbNo: \xe5\x89\xaf\xe6\x9c\xac\xe5\x8f\xb7
        :param lastFriendRank: \xe4\xb8\x8a\xe6\xac\xa1\xe5\x9c\xa8\xe5\xa5\xbd\xe5\x8f\x8b\xe4\xb8\xad\xe7\x9a\x84\xe6\x8e\x92\xe5\x90\x8d
        :param curFriendRank: \xe5\xbd\x93\xe5\x89\x8d\xe5\x9c\xa8\xe5\xa5\xbd\xe5\x8f\x8b\xe4\xb8\xad\xe7\x9a\x84\xe6\x8e\x92\xe5\x90\x8d
        :return:
        """
        gamelog.debug('@zhangkuo endTeamEndless isOk:{}, teamEndlessLv:{}, rank:{}, friends:[gbId,teamEndlessLv,timeCost,timestamp],timeCost:{}, fbNo:{}'.format(isOk, teamEndlessLv, rank, friends, timeCost, fbNo))
        friends.sort(key=lambda x: (-x[1],
         x[2],
         x[3],
         x[0]))
        resultData = {'isOk': isOk,
         'teamEndlessLv': teamEndlessLv,
         'rank': rank,
         'friends': friends,
         'timeCost': timeCost,
         'fbNo': fbNo,
         'lastFriendRank': lastFriendRank,
         'curFriendRank': curFriendRank}
        gameglobal.rds.ui.voidLunHuiRank.show(resultData)

    def enterTeamEndlessFailed(self, reason):
        """\xe8\xbf\x9b\xe5\x85\xa5\xe5\xa4\xb1\xe8\xb4\xa5"""
        gamelog.debug('@zhangkuo enterTeamEndlessFailed', reason)
        if reason != gametypes.TEAM_ENDLESS_FAILED_NOT_CONFIRMED:
            gameglobal.rds.ui.voidLunHuiStart.clearAll()
        gameglobal.rds.ui.voidLunHuiStart.onConfirmCanceled(reason)

    def onEnterTeamEndlessFuben(self, data):
        """
        \xe8\xbf\x9b\xe5\x85\xa5\xe5\x89\xaf\xe6\x9c\xac\xe5\x90\x8c\xe6\xad\xa5\xe4\xbf\xa1\xe6\x81\xaf
        :param data {gametypes.TEAM_ENDLESS_INFO_PROGRESS: boss\xe8\xbf\x9b\xe5\xba\xa6, gametypes.TEAM_ENDLESS_INFO_LV\xef\xbc\x9a\xe9\x9a\xbe\xe5\xba\xa6, gametypes.TEAM_ENDLESS_INFO_PROGRESS_EX: \xe5\xb0\x8f\xe6\x80\xaa\xe8\xbf\x9b\xe5\xba\xa6}
        """
        gamelog.debug('@zhangkuo onEnterTeamEndlessFuben', data)
        self.teamEndlessFubenData = data
        bossOrderList = data.get(gametypes.TEAM_ENDLESS_INFO_PROGRESS, [])
        orchiProgress = data.get(gametypes.TEAM_ENDLESS_INFO_PROGRESS_EX, 0)
        gameglobal.rds.ui.voidLunHuiBar.onGetBossOrders(bossOrderList, orchiProgress)
        deadline = data.get(gametypes.TEAM_ENDLESS_INFO_DEADLINE)
        if deadline:
            self.onPushTeamEndlessDeadline(deadline)

    def onPushTeamEndlessDeadline(self, deadline):
        """\xe6\x8e\xa8\xe9\x80\x81\xe9\x80\x9a\xe5\x85\xb3\xe6\x88\xaa\xe6\xad\xa2\xe6\x97\xb6\xe9\x97\xb4"""
        gamelog.debug('@zhangkuo onPushTeamEndlessDeadline', deadline)
        gameglobal.rds.ui.voidLunHuiBar.updateEndTime(deadline)

    def onTakenTeamEndlessLevelReward(self, lvType, teamEndlessLv):
        """\xe9\xa2\x86\xe5\x8f\x96\xe4\xba\x86\xe9\x80\x9a\xe5\x85\xb3\xe5\xa5\x96\xe5\x8a\xb1"""
        gamelog.debug('@zhangkuo onTakenTeamEndlessLevelReward', lvType, teamEndlessLv)
        gameglobal.rds.ui.voidLunHuiRank.onGetReward(lvType, teamEndlessLv)

    def updateGlobalMaxTeamEndlessLv(self, data):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe5\x85\xa8\xe6\x9c\x8d\xe6\x9c\x80\xe5\xa4\xa7\xe5\x8f\xaf\xe6\x8c\x91\xe6\x88\x98\xe9\x9a\xbe\xe5\xba\xa6
        :param data {lvType: lv}
        """
        gamelog.debug('@zhangkuo updateGlobalMaxTeamEndlessLv', data)
        self.teamEndlessMaxLvs = data
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TEAMENDLESS_CHANGED)

    def updateTeamEndlessRewardTimes(self, data):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe5\xaf\xb9\xe5\xba\x94\xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5\xe7\xb1\xbb\xe5\x9e\x8b\xe5\xb7\xb2\xe7\xbb\x8f\xe9\xa2\x86\xe5\x8f\x96\xe8\xbf\x87\xe5\xa5\x96\xe5\x8a\xb1\xe7\x9a\x84\xe6\xac\xa1\xe6\x95\xb0
        :param data: {lvType: times}
        """
        gamelog.debug('@zhangkuo updateTeamEndlessRewardTimes', data)
        self.teamEndlessRewardTimes.update(data)
        gameglobal.rds.ui.voidLunHui.updateTabInfoMc()
        gameglobal.rds.ui.voidLunHuiRank.refreshRewardState()
