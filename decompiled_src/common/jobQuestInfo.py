#Embedded file name: I:/bag/tmp/tw2/res/entities\common/jobQuestInfo.o
from userInfo import UserInfo
from jobQuest import JobGroup, JobVal

class JobGroupInfo(UserInfo):

    def createObjFromDict(self, dict):
        jobGroup = JobGroup()
        jobGroup.startTimerId = dict['startTimerId']
        jobGroup.endTimerId = dict['endTimerId']
        jobGroup.state = dict['state']
        jobGroup.version = dict['version']
        jobGroup.jobTimeInfo = dict['jobTimeInfo']
        jobGroup.nextJobTimeInfo = dict['nextJobTimeInfo']
        jobGroup.lastJobInfo = dict['lastJobInfo']
        jobGroup.bonusFactor = dict['bonusFactor']
        jobGroup.tAllAccept = dict['tAllAccept']
        jobGroup.tHalfAccept = dict['tHalfAccept']
        jobGroup.jobGroupId = dict['jobGroupId']
        jobGroup.cnt = dict['cnt']
        for jobDict in dict['jobs']:
            jobGroup[jobDict['jobId']] = JobVal(jobDict['jobId'], jobDict['count'], jobDict['rest'])

        return jobGroup

    def getDictFromObj(self, obj):
        dict = {'startTimerId': obj.startTimerId,
         'endTimerId': obj.endTimerId,
         'state': obj.state,
         'version': obj.version,
         'jobs': [],
         'jobTimeInfo': obj.jobTimeInfo,
         'nextJobTimeInfo': obj.nextJobTimeInfo,
         'lastJobInfo': obj.lastJobInfo,
         'bonusFactor': obj.bonusFactor,
         'tAllAccept': obj.tAllAccept,
         'tHalfAccept': obj.tHalfAccept,
         'jobGroupId': obj.jobGroupId,
         'cnt': obj.cnt}
        for jobId, jobVal in obj.iteritems():
            dict['jobs'].append({'jobId': jobId,
             'count': jobVal.count,
             'rest': jobVal.rest,
             'blacklist': jobVal.blacklist})

        return dict

    def isSameType(self, obj):
        return type(obj) is JobGroup


instance = JobGroupInfo()
