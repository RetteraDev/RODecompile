#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impJobQuest.o
import BigWorld
import const
import gameglobal
import commQuest
from data import quest_data as QD
from data import job_action_data as JAD
from data import npc_data as ND

class ImpJobQuest(object):

    def onGetAvailableJobs(self, jobRefId, index, version, jobList, jobTimeInfo, bonusFactor, npcEntId):
        ent = BigWorld.entities.get(npcEntId)
        npcID = ent.npcId
        boardType = ND.data.get(npcID, {}).get('boardType', 2)
        if gameglobal.rds.ui.jobBoard.mediator:
            gameglobal.rds.ui.jobBoard.refreshJobBoardInfo(jobRefId, index, version, jobList, jobTimeInfo, bonusFactor)
        else:
            gameglobal.rds.ui.jobBoard.show(jobRefId, index, version, jobList, jobTimeInfo, boardType, bonusFactor)

    def onGetJobDetail(self, jobId):
        gameglobal.rds.ui.jobBoard.showDetail(jobId)

    def _needJobStats(self, questId, statsType, charType):
        if commQuest.reachMaxJobScore(self, questId):
            return False
        actionGroupId = QD.data[questId].get('jobGroup', 0)
        if actionGroupId:
            jobActions = self.getQuestData(questId, const.QD_JOBS, ())
            for jobAction in JAD.data.get(actionGroupId, []):
                if jobAction['jobId'] not in jobActions:
                    continue
                if jobAction['jobType'] == statsType and jobAction['jobArgs'] == charType:
                    return True

        return False

    def _isJobCharType(self, questId, statsType, charType):
        actionGroupId = QD.data[questId].get('jobGroup', 0)
        if actionGroupId:
            for jobAction in JAD.data.get(actionGroupId, []):
                if jobAction['jobType'] == statsType and jobAction['jobArgs'] == charType:
                    return True

        return False

    def onGetJobsCount(self, cntDict):
        self.jobsCount = cntDict
        gameglobal.rds.ui.map.refreshNpcPos()
