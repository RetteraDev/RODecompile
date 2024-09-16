#Embedded file name: /WORKSPACE/data/entities/common/teamendlessinfo.o
from userInfo import UserInfo
from teamEndless import TeamEndlessProgressVal, TeamEndlessProgress, TeamEndlessVal, TeamEndless

class TeamEndlessInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = TeamEndless()
        obj.tLastReset = d['tLastReset']
        for tVal in d['teamEndless']:
            progress = TeamEndlessProgress()
            for pVal in tVal['progress']:
                progress.pushVal(pVal['lv'], pVal['onceRewardState'], pVal['levelRewardState'])

            lvType = tVal['lvType']
            item = TeamEndlessVal(lvType=lvType, maxLv=tVal['maxLv'], maxEnableLv=tVal['maxEnableLv'], progress=progress, bestRecordWeekly=tVal['bestRecordWeekly'])
            obj.setItem(lvType, item)

        return obj

    def getDictFromObj(self, obj):
        data = []
        for lvType, item in obj.iteritems():
            progress = []
            for pVal in item.progress.itervalues():
                progress.append({'lv': pVal.lv,
                 'onceRewardState': pVal.onceRewardState,
                 'levelRewardState': pVal.levelRewardState})

            data.append({'lvType': lvType,
             'maxLv': item.maxLv,
             'maxEnableLv': item.maxEnableLv,
             'progress': progress,
             'bestRecordWeekly': item.bestRecordWeekly})

        return {'teamEndless': data,
         'tLastReset': obj.tLastReset}

    def isSameType(self, obj):
        return type(obj) is TeamEndless


instance = TeamEndlessInfo()
