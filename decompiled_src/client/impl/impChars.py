#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impChars.o
import gameglobal
import const
import commcalc
from data import qiren_clue_data as QCD

class ImpChars(object):

    def setCharClueFlags(self, conditions, val):
        for cid in conditions:
            commcalc.setBit(self.charClueFlags, cid, val)
            if val and hasattr(gameglobal.rds, 'tutorial'):
                gameglobal.rds.tutorial.onFinishClue(cid)

        if val:
            gameglobal.rds.ui.rolecard.onClueInfoUpdate(conditions)
            gameglobal.rds.ui.fengWuZhi.onClueInfoUpdate(conditions)
            gameglobal.rds.ui.rolecard.refreshRewardInfo()

    def setStoryBonusFlags(self, storyIds, val):
        for sid in storyIds:
            commcalc.setBit(self.storyBonusFlags, sid, val)

        gameglobal.rds.ui.rolecard.checkAndPushBonus()
        if val:
            gameglobal.rds.ui.rolecard.refreshRewardInfo()

    def setQirenBonusFlag(self, qirenIds, val):
        for qid in qirenIds:
            commcalc.setBit(self.qirenBonusFlags, qid, val)

    def setFengwuzhiBonusFlag(self, areaId, val):
        self.fengwuzhiBonusFlags[areaId] = val
        gameglobal.rds.ui.fengWuZhi.refreshAwardInfo(areaId)

    def setCharGroupBonusFlags(self, groupIds, val):
        for gid in groupIds:
            commcalc.setBit(self.charGroupBonusFlags, gid, val)

        gameglobal.rds.ui.rolecard.checkAndPushBonus()

    def getClueFlag(self, cid):
        if cid == 0:
            return True
        if not QCD.data.has_key(cid):
            return False
        if not hasattr(self, 'charClueFlags'):
            return False
        qcd = QCD.data[cid]
        val = commcalc.getBit(self.charClueFlags, cid)
        if qcd.get('conditionType') == const.CHAR_STORY_CON_COMBINATION and not val:
            try:
                subClues = qcd['condition']({})
            except:
                subClues = ()

            if all([ commcalc.getBit(self.charClueFlags, sid) for sid in subClues ]):
                return True
        return val

    def getCharGroupBonusFlag(self, cid):
        return commcalc.getBit(self.charGroupBonusFlags, cid)

    def getStoryBonusFlag(self, cid):
        return commcalc.getBit(self.storyBonusFlags, cid)

    def sendCharStoryFlags(self, charClueFlags, storyBonusFlags, charGroupBonusFlags, qirenBonusFlags):
        self.charClueFlags = charClueFlags
        self.storyBonusFlags = storyBonusFlags
        self.charGroupBonusFlags = charGroupBonusFlags
        self.qirenBonusFlags = qirenBonusFlags
        gameglobal.rds.ui.rolecard.onClueInfoInit()

    def sendFengwuzhiBonusFlags(self, fengwuzhiBonusFlags):
        self.fengwuzhiBonusFlags = fengwuzhiBonusFlags

    def onStartCharStory(self, storyId):
        gameglobal.rds.ui.rolecard.onEnterStorySucc()

    def startQiRenBarrage(self, questId, barrageId):
        gameglobal.rds.ui.Barrage.startQiRenBarrageByGroupId(barrageId)
