#Embedded file name: I:/bag/tmp/tw2/res/entities\common/jobQuest.o
import BigWorld
import gametypes
import formula
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType
if BigWorld.component in ('base', 'cell'):
    from data import job_management_data as JMD
    from data import sys_config_data as SCD

class JobGroup(UserDictType):

    def __init__(self, startTimerId = 0, endTimerId = 0, state = gametypes.JOB_GROUP_STATE_NOT_STARTED, version = 1, lastJobInfo = None, bonusFactor = 1.0, jobGroupId = 0):
        self.startTimerId = startTimerId
        self.endTimerId = endTimerId
        self.state = state
        self.lastJobInfo = dict(lastJobInfo) if lastJobInfo else {}
        self.tAllAccept = 0
        self.tHalfAccept = 0
        self.bonusFactor = bonusFactor
        self.jobGroupId = jobGroupId
        self.version = version
        self.cnt = 0

    def _lateReload(self):
        super(JobGroup, self)._lateReload()
        for jVal in self.itervalues():
            jVal.reloadScript()

    def addJob(self, jobId, count):
        self[jobId] = JobVal(jobId=jobId, count=count, rest=count)
        self.version += 1
        self.cnt += count

    def canAcceptJob(self, gbId, refId, jobId, groupIndex):
        if jobId not in self:
            return gametypes.ACCEPT_JOB_FAIL_GENERAL
        if refId not in JMD.data or groupIndex >= len(JMD.data[refId].get('jobGroupInfo', ())):
            return gametypes.ACCEPT_JOB_FAIL_GENERAL
        if self.state != gametypes.JOB_GROUP_STATE_STARTED:
            return gametypes.ACCEPT_JOB_FAIL_NOT_STARTED
        if self[jobId].rest <= 0:
            return gametypes.ACCEPT_JOB_FAIL_NO_JOB
        if self[jobId].blacklist.get(gbId, 0) > utils.getNow():
            return gametypes.ACCEPT_JOB_FAIL_BLACKLIST
        return gametypes.ACCEPT_JOB_SUCC

    def onAcceptJob(self, refId, jobId, groupIndex):
        if jobId not in self:
            return
        self[jobId].rest -= 1
        self.version += 1
        self.cnt -= 1
        jobGroupInfo = JMD.data[refId]['jobGroupInfo'][groupIndex]
        tStart, tEnd, _, _ = jobGroupInfo
        curXingJiTime = formula.getXingJiTime()
        jobAll = sum([ jVal.count for jVal in self.itervalues() ])
        jobRest = sum([ jVal.rest for jVal in self.itervalues() ])
        if jobRest == 0:
            self.tAllAccept = float(curXingJiTime - tStart) / (tEnd - tStart)
        if not self.tHalfAccept and jobRest <= jobAll * 0.5:
            self.tHalfAccept = float(curXingJiTime - tStart) / (tEnd - tStart)

    def onAbandonJob(self, gbId, refId, jobId, groupIndex):
        self[jobId].blacklist[gbId] = utils.getNow() + SCD.data.get('abandonJobPunishTime', 300)
        for gId, tForbidden in self[jobId].blacklist.items():
            if tForbidden < utils.getNow():
                self[jobId].blacklist.pop(gId)

    def onAcceptJobFail(self, jobId):
        if jobId not in self:
            return
        self[jobId].rest += 1
        self.version += 1
        self.cnt += 1

    def setState(self, state):
        self.state = state
        self.version += 1


class JobVal(UserSoleType):

    def __init__(self, jobId = 0, count = 0, rest = 0, blacklist = None):
        self.jobId = jobId
        self.count = count
        self.rest = rest
        self.blacklist = blacklist or {}

    def getDict(self):
        return {'jobId': self.jobId,
         'count': self.count,
         'rest': self.rest}
