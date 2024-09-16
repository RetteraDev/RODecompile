#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impServerProgress.o
import BigWorld
import cPickle
import zlib
import gameglobal
import const
from guis import events
from data import server_progress_data as SPD
from data import sys_config_data as SCD
from data import guild_tournament_data as GTD
from data import qumo_lv_data as QLD
from data import junjie_config_data as JCD
from cdata import game_msg_def_data as GMDD
from cdata import server_progress_qumo_point_limit_data as SPQPLD
from cdata import server_progress_qumo_fame_limit_data as SPQFLD
from cdata import server_progress_zhanxun_limit_data as SPZLD
from cdata import server_progress_junzi_limit_data as SPJLD

class ImpServerProgress(object):

    def onServerProgressData(self, sdata):
        data, msIds = sdata
        self.serverProgressData = cPickle.loads(zlib.decompress(data))
        if msIds != None:
            self.serverProgressRewardMsIds = [ msId for msId in msIds if not SPD.data.get(msId).get('disable', 0) ]
        gameglobal.rds.ui.dispatchEvent(events.EVENT_UPDATE_SERVER_PROGRESS)

    def sendServerProgress(self, serverProgresses):
        self.serverProgresses = serverProgresses
        self.base.checkNotifyServerProgress()
        self.setXConsignStartCallBack()

    def onServerProgressContribMsIds(self, msIds):
        msIds = [ msId for msId in msIds if not SPD.data.get(msId).get('disable', 0) ]
        if hasattr(self, 'serverProgressRewardMsIds'):
            self.serverProgressRewardMsIds.extend(msIds)

    def onServerProgressNotify(self, msId, tWhen):
        self.serverProgresses[msId] = tWhen
        if SPD.data.get(msId).get('disable', 0):
            return
        gtMsIds = [ data.get('serverProgressMsId') for data in GTD.data.itervalues() ]
        if msId in gtMsIds and not gameglobal.rds.configData.get('enableGuildTournament', False):
            return
        if not hasattr(self, '_notifyMsIds'):
            self._notifyMsIds = []
        if not self._notifyMsIds:
            self._notifyMsIds.append(msId)
            self._doNotifyServerProgerss(msId)
        else:
            self._notifyMsIds.append(msId)
        self.onQuestInfoModifiedAtClient(const.QD_SERVER_PROCESS, exData={'msId': msId})
        gameglobal.rds.ui.excitementIcon.refreshInfo()

    def _doNotifyServerProgerss(self, msId):
        repeatCnt = SCD.data.get('serverProgressNotifyRepeatCnt', 3)
        interval = SCD.data.get('serverProgressNotifyInterval', 10)
        if repeatCnt <= 0 or interval <= 0:
            return
        name = (SPD.data.get(msId, {}).get('name', ''),)
        if name[0]:
            self.showSysNotification(GMDD.data.SERVER_PROGRESS_NOTIFY, name, repeatCnt, interval, finishCallback=lambda msId = msId: self._onServerProgressNotifyFinish(msId))

    def _onServerProgressNotifyFinish(self, msId):
        if not self.inWorld:
            return
        if msId in self._notifyMsIds:
            self._notifyMsIds.remove(msId)
        if self._notifyMsIds:
            self._doNotifyServerProgerss(self._notifyMsIds[0])
        else:
            self.base.checkNotifyServerProgress()

    def isServerProgressFinished(self, msId, extra = False):
        return msId in self.serverProgresses or extra and msId in self.extraServerProgresses

    def hadServerProgressFinished(self, msIdList):
        return bool(set(msIdList) & set(self.serverProgresses))

    def getServerProgressFinishTime(self, msId):
        return self.serverProgresses.get(msId)

    def checkServerProgress(self, msId, bMsg = True, extra = False):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return True
        if not self.isServerProgressFinished(msId, extra=extra):
            bMsg and self.showGameMsg(GMDD.data.SERVER_PROGRESS_NOT_FINISHED, (SPD.data.get(msId, {}).get('name', ''),))
            return False
        return True

    def checkHasServerProgress(self, msIds, bMsg = True, extra = False):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return True
        if not msIds:
            return True
        if type(msIds) in (int, long):
            msIds = (msIds,)
        for msId in msIds:
            if self.isServerProgressFinished(msId, extra=extra):
                return True

        bMsg and self.showGameMsg(GMDD.data.SERVER_PROGRESS_NOT_FINISHED, (SPD.data.get(msIds[0], {}).get('name', ''),))
        return False

    def getMaxWeeklyQumoPointsRate(self):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return 1
        msIds = SCD.data.get('qumoServerProgressMsIds')
        if not msIds:
            return 1
        qld = QLD.data.get(self.qumoLv)
        maxLvQumoExp = qld.get('maxLvQumoExp', 0)
        if maxLvQumoExp and self.qumoExp >= maxLvQumoExp:
            return 1
        for msId in msIds:
            if self.isServerProgressFinished(msId):
                return SPQPLD.data.get((msId, self.qumoLv), {}).get('value', 1)

        return 1

    def getMaxQumoFameRate(self):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return 1
        msIds = SCD.data.get('qumoServerProgressMsIds')
        if not msIds:
            return 1
        for msId in msIds:
            if self.isServerProgressFinished(msId):
                return SPQFLD.data.get((msId, self.qumoLv), {}).get('value', 1)

        return 1

    def getMaxZhanxunRate(self):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return 1
        maxJunJieLimit = JCD.data.get(self.junJieLv, {}).get('maxJunJieLimit', 0)
        if maxJunJieLimit and self.junJieVal >= maxJunJieLimit:
            return 1
        msIds = SCD.data.get('junjieServerProgressMsIds')
        if not msIds:
            return 1
        for msId in msIds:
            if self.isServerProgressFinished(msId):
                return SPZLD.data.get((msId, self.junJieLv), {}).get('value', 1)

        return 1

    def getMaxJunziRate(self):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return 1
        maxJunJieLimit = JCD.data.get(self.junJieLv, {}).get('maxJunJieLimit', 0)
        if maxJunJieLimit and self.junJieVal >= maxJunJieLimit:
            return 1
        msIds = SCD.data.get('junjieServerProgressMsIds')
        if not msIds:
            return 1
        for msId in msIds:
            if self.isServerProgressFinished(msId):
                return SPJLD.data.get((msId, self.junJieLv), {}).get('value', 1)

        return 1

    def sendCrossServerProgressIds(self, crossMsIds, ver):
        gameglobal.rds.ui.yunchuiji.crossMsIds = crossMsIds
        gameglobal.rds.ui.yunchuiji.crossMsIdsVer = ver

    def onGetServerProgressInfo(self, progressInfo):
        self.extraServerProgresses.update(progressInfo)

    def getExtraServerProgress(self):
        eventsDict = SCD.data.get('cardAdvanceFuncOpenEvents', ())
        allEventList = list()
        if type(eventsDict) == dict:
            for serverPgsList in eventsDict.itervalues():
                allEventList.extend(serverPgsList)

            allEventList = list(set(allEventList))
        elif type(eventsDict) in (tuple, list):
            allEventList = eventsDict
        self.base.getServerProgressInfo(allEventList)

    def updateSyncProgressStatus(self, statusData):
        """
        statusData : {propId: value, propId: value, ...}
        """
        p = BigWorld.player()
        if not p.serverProgressStatus:
            p.serverProgressStatus = statusData
        else:
            p.serverProgressStatus.update(statusData)

    def getServerProgressStatusData(self, serverProgressStatusId):
        p = BigWorld.player()
        if not p.serverProgressStatus:
            return None
        else:
            return p.serverProgressStatus.get(serverProgressStatusId, None)
