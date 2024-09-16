#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/quest.o
import BigWorld
import const
from data import item_data as ID
from data import quest_data as QD
from data import monster_data as MD
NORMAL_QUEST = 1
SCHOOL_QUEST = 2
RING_QUEST = 3
CIRCLE_QUEST = 4

class _QuestDataFacade(object):

    def __init__(self, data):
        self._data = data
        self._questid = 0

    def getName(self):
        return self._data.get('name', '该任务已删除')

    def getCNpc(self):
        return self._data.get('cnpc', 0)

    def getANpc(self):
        return self._data.get('anpc', 0)

    def getId(self):
        return self._questid

    def getHint(self):
        text = self._data.get('hint', '')
        return text

    def getIntro(self):
        text = self._data.get('intro', '该任务已删除，请放弃')
        text = text.replace('$P', BigWorld.player().realRoleName)
        return text

    def getBriefIntro(self):
        return self._data.get('brief', '该任务已删除，请放弃')

    def getQuestColor(self):
        return self._data.get('taskType', 0)

    def getNeededItems(self):
        return self._data.get('needItems', ())

    def getNeededMonsters(self):
        need = self._data.get('needMonsters', {})
        return need


class _NormalDataFacade(_QuestDataFacade):

    def __init__(self, id):
        super(_NormalDataFacade, self).__init__(QD.data.get(id, {}))
        self._questid = id

    def getLevel(self):
        return self._data.get('qlv', 0)

    def getStar(self):
        return self._data.get('qstar', 1)

    def getHard(self):
        return self._data.get('hard', 0)

    def getQuestType(self):
        return self._data.get('taskType', 0)

    def getArea(self):
        return self._data.get('area', '未知')


class _Quest(object):

    def __init__(self, id, data, questType):
        self._data = data
        self._questType = questType
        self._id = id

    def getId(self):
        return self._id

    def getCNpc(self):
        return self._data.getCNpc()

    def getANpc(self):
        return self._data.getANpc()

    def isMainQuest(self):
        return False

    def getType(self):
        return self._questType

    def getQuestColor(self):
        return self._data.getQuestColor()

    def getName(self):
        return self._data.getName()

    def getArea(self):
        return self._data.getArea()

    def getHint(self):
        text = self._data.getHint()
        return text

    def getIntro(self):
        return self._data.getIntro()

    def getBriefIntro(self):
        return self._data.getBriefIntro()

    def getNeededItems(self):
        return self._data.getNeededItems()

    def isCommitedAll(self):
        for desc, isDone, reclaim, started, targetType in self.getTargets():
            if isDone == False:
                return False

        return True

    def isRequestSatisfy(self):
        for desc, isDone, reclaim, started, targetType in self.getTargets():
            if isDone == False and not reclaim:
                return False

        return True

    def canBeCompleted(self):
        return self.isCommitedAll() and not self.isFailed()

    def getHard(self):
        return 0

    def getQuestType(self):
        return 0

    def getLevel(self):
        return 0

    def isDone(self):
        return self.isRequestSatisfy() and not self.isFailed()

    def isAccepted(self):
        return False

    def isItemDesired(self, obj):
        for id, count in self._data.getNeededItems():
            if obj.id == id:
                return True

        return False

    def getTargets(self):
        p = BigWorld.player()
        targets = []
        killed = self._getQuestMonsterData()
        needed = self._data.getNeededMonsters()
        for id in needed:
            name = MD.data.get(id, {}).get('name', None)
            if name:
                num = killed.get(id, 0)
                count = needed[id]
                desc = '需要消灭:%s(%d/%d)' % (name, num, count)
                targets.append((desc,
                 num >= count,
                 False,
                 num > 0,
                 (0, id)))
            else:
                desc = '需要消灭:未知名怪物'
                targets.append((desc,
                 False,
                 False,
                 False,
                 (0, id)))

        for id, count in self._data.getNeededItems():
            itNum = p.inv.countAll(id, const.INV_PAGE_QUEST)
            name = ID.data.get(id, {}).get('name', '未知名物品')
            desc = '需要物品:%s(%d/%d)' % (name, itNum, count)
            targets.append((desc,
             itNum >= count,
             False,
             itNum > 0,
             (1, id)))

        return targets

    def _getQuestMonsterData(self):
        return {}

    def isFailed(self):
        return False


class _NormalQuest(_Quest):
    FAILED_QUEST = {}

    def __init__(self, id):
        data = _NormalDataFacade(id)
        super(_NormalQuest, self).__init__(id, data, NORMAL_QUEST)

    def getTargets(self):
        targets = super(_NormalQuest, self).getTargets()
        questID = self.getId()
        clv = QD.data.get(questID, {}).get('complete_lower_lv', 0)
        p = BigWorld.player()
        if clv:
            plv = p.lv
            desc = '需要等级:(%d/%d)' % (clv, plv)
            targets.append((desc,
             clv <= plv,
             False,
             False,
             (-1, 0)))
        return targets

    def isAccepted(self):
        return self.getId() in BigWorld.player().quests

    def getLevel(self):
        return self._data.getLevel()

    def getHard(self):
        return self._data.getHard()

    def getQuestType(self):
        return self._data.getQuestType()

    def getStar(self):
        return self._data.getStar()

    def _getQuestMonsterData(self):
        return BigWorld.player().questData.get(self.getId(), {}).get(const.QD_MONSTER_KILL, {})


def createQuest(id, questType = NORMAL_QUEST):
    if questType == NORMAL_QUEST:
        return _NormalQuest(id)
