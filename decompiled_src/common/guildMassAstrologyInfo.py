#Embedded file name: I:/bag/tmp/tw2/res/entities\common/guildMassAstrologyInfo.o
from userInfo import UserInfo
from guild import GuildMassAstrology
import utils

class GuildMassAstrologyInfo(UserInfo):

    def createObjFromDict(self, dict):
        massAstrology = GuildMassAstrology(state=dict['state'], cntDaily=dict['cntDaily'], selectBuffId=dict['selectBuffId'], lastRandomList=dict['lastRandomList'])
        for buffVal in dict['currBuffIds']:
            if utils.getNow() < buffVal['expiredTime']:
                massAstrology[buffVal['buffId']] = buffVal['expiredTime']

        return massAstrology

    def getDictFromObj(self, obj):
        currBuffIds = []
        for buffId, expiredTime in obj.iteritems():
            currBuffIds.append({'buffId': buffId,
             'expiredTime': expiredTime})

        return {'state': obj.state,
         'cntDaily': obj.cntDaily,
         'selectBuffId': obj.selectBuffId,
         'currBuffIds': currBuffIds,
         'lastRandomList': obj.lastRandomList}

    def isSameType(self, obj):
        return type(obj) is GuildMassAstrology


instance = GuildMassAstrologyInfo()
