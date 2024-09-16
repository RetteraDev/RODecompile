#Embedded file name: I:/bag/tmp/tw2/res/entities\common/zhenyaoRankInfo.o
from userInfo import UserInfo
from zhenyaoRank import ZhenyaoGroupVal, ZhenyaoScore, ZhenyaoFinalRankVal, ZhenyaoFinalRank, ZhenyaoFinalRankList

class ZhenyaoFinalRankInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = ZhenyaoFinalRank()
        for val in dict['rank']:
            groupLv = val['groupLv']
            finalRank = val['rVal']
            subObj = ZhenyaoFinalRankList()
            subObj.finalRank = []
            for fVal in finalRank:
                scoreInfo = fVal['score']
                groupInfo = fVal['group']
                groupNUID = fVal['groupNUID']
                scoreObj = ZhenyaoScore(scoreInfo['score'], scoreInfo['interval'], scoreInfo['tWhen'])
                groupName = groupInfo['groupName']
                groupObj = ZhenyaoGroupVal(groupName)
                for m in groupInfo['groupMember']:
                    groupObj.groupMember.pushMember(m['gbId'], m['isHeader'], m['roleName'], m['school'], m['lv'])

                subObj.finalRank.append(ZhenyaoFinalRankVal(scoreObj, groupObj, groupNUID))

            obj[groupLv] = subObj

        return obj

    def getDictFromObj(self, obj):
        finalRankInfo = []
        for k, v in obj.iteritems():
            subRank = []
            for val in v.finalRank:
                groupMember = []
                for gk, gVal in val.group.groupMember.iteritems():
                    groupMember.append({'gbId': gk,
                     'isHeader': gVal.isHeader,
                     'roleName': gVal.roleName,
                     'school': gVal.school,
                     'lv': gVal.lv})

                score = {'score': val.scoreInfo.score,
                 'interval': val.scoreInfo.interval,
                 'tWhen': val.scoreInfo.tWhen}
                group = {'groupName': val.group.groupName,
                 'groupMember': groupMember}
                subRank.append({'score': score,
                 'group': group,
                 'groupNUID': val.groupNUID})

            finalRankInfo.append({'groupLv': k,
             'rVal': subRank})

        data = {'rank': finalRankInfo}
        return data

    def isSameType(self, obj):
        return type(obj) is ZhenyaoFinalRank


instance = ZhenyaoFinalRankInfo()
