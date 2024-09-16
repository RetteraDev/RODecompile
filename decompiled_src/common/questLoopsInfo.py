#Embedded file name: I:/bag/tmp/tw2/res/entities\common/questLoopsInfo.o
import BigWorld
from userDictType import UserDictType
from questLoops import QuestLoops, QuestLoopVal
if BigWorld.component == 'client':
    from iStreamInfoCommon import bindStream
else:
    from iStreamInfo import bindStream

class QuestLoopsInfo(UserDictType):

    def createObjFromDict(self, dict):
        questLoops = QuestLoops()
        vals = dict['groups']
        for questLoop in vals:
            questLoopId = questLoop['questLoopId']
            loopCnt = questLoop['loopCnt']
            beginIndex = questLoop['beginIndex']
            abandonQuestId = questLoop['abandonQuestId']
            lastAbandonTime = questLoop['lastAbandonTime']
            predictQuestId = questLoop['predictQuestId']
            avlAcCnt = questLoop['avlAcCnt']
            yesterdayType = questLoop['yesterdayType']
            lastCompNpc = questLoop['lastCompNpc']
            if questLoop.has_key('startAcceptTime'):
                startAcceptTime = questLoop['startAcceptTime']
            else:
                startAcceptTime = 0
            questInfo = questLoop['questInfo']
            extraInfo = questLoop['extraInfo']
            questLoopVal = QuestLoopVal(questLoopId)
            questLoopVal.loopCnt = loopCnt
            questLoopVal.beginIndex = beginIndex
            questLoopVal.abandonQuestId = abandonQuestId
            questLoopVal.lastAbandonTime = lastAbandonTime
            questLoopVal.predictQuestId = predictQuestId
            questLoopVal.avlAcCnt = avlAcCnt
            questLoopVal.yesterdayType = yesterdayType
            questLoopVal.lastCompNpc = lastCompNpc
            questLoopVal.startAcceptTime = startAcceptTime
            questLoopVal.questInfo = questInfo
            questLoopVal.extraInfo = extraInfo
            questLoops[questLoopId] = questLoopVal

        return questLoops

    def getDictFromObj(self, obj):
        res = []
        for questLoopId, questLoopVal in obj.iteritems():
            val = {}
            val['questLoopId'] = questLoopId
            val['loopCnt'] = questLoopVal.loopCnt
            val['beginIndex'] = questLoopVal.beginIndex
            val['abandonQuestId'] = questLoopVal.abandonQuestId
            val['lastAbandonTime'] = questLoopVal.lastAbandonTime
            val['predictQuestId'] = questLoopVal.predictQuestId
            val['avlAcCnt'] = questLoopVal.avlAcCnt
            val['yesterdayType'] = questLoopVal.yesterdayType
            val['lastCompNpc'] = questLoopVal.lastCompNpc
            val['startAcceptTime'] = questLoopVal.startAcceptTime
            val['questInfo'] = questLoopVal.questInfo
            val['extraInfo'] = questLoopVal.extraInfo
            res.append(val)

        return {'groups': res}

    def _createObjFromStream(self, stream):
        questLoops = QuestLoops()
        for questLoopId, loopCnt, beginIndex, abandonQuestId, lastAbandonTime, predictQuestId, avlAcCnt, yesterdayType, lastCompNpc, startAcceptTime, questInfo, extraInfo in stream:
            questLoopVal = QuestLoopVal(questLoopId)
            questLoopVal.loopCnt = loopCnt
            questLoopVal.beginIndex = beginIndex
            questLoopVal.abandonQuestId = abandonQuestId
            questLoopVal.lastAbandonTime = lastAbandonTime
            questLoopVal.predictQuestId = predictQuestId
            questLoopVal.avlAcCnt = avlAcCnt
            questLoopVal.yesterdayType = yesterdayType
            questLoopVal.lastCompNpc = lastCompNpc
            questLoopVal.startAcceptTime = startAcceptTime
            questLoopVal.questInfo = questInfo
            questLoopVal.extraInfo = extraInfo
            questLoops[questLoopId] = questLoopVal

        return questLoops

    def _getStreamFromObj(self, obj):
        return [ (questLoopId,
         x.loopCnt,
         x.beginIndex,
         x.abandonQuestId,
         x.lastAbandonTime,
         x.predictQuestId,
         x.avlAcCnt,
         x.yesterdayType,
         x.lastCompNpc,
         x.startAcceptTime,
         x.questInfo,
         x.extraInfo) for questLoopId, x in obj.iteritems() ]

    def isSameType(self, obj):
        return type(obj) is QuestLoops


instance = QuestLoopsInfo()
bindStream(instance)
