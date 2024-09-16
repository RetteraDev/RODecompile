#Embedded file name: /WORKSPACE/data/entities/common/questloops.o
import BigWorld
import time
import const
import random
import gametypes
import commQuest
import commActivity
import gamelog
import utils
from userDictType import UserDictType
from userSoleType import UserSoleType
from data import quest_data as QD
from data import quest_loop_data as QLD
from data import quest_loop_chain_data as QLCD
from data import sys_config_data as SCD
from cdata import quest_loop_inverted_data as QLID
from cdata import game_msg_def_data as GMDD
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import gameengine
    import gamebonus
    from data import formula_server_data as FMD
elif BigWorld.component in ('client',):
    if not getattr(BigWorld, 'isBot', False):
        from data import formula_client_data as FMD

def getOtherQuestIdsOfStep(questLoopId, questId):
    questIds = QLD.data.get(questLoopId, {}).get('quests')
    for ids in questIds:
        if isinstance(ids, int):
            if questId == ids:
                return None
        elif isinstance(ids, tuple):
            if questId in ids:
                r = list(ids)
                r.remove(questId)
                return r


class QuestLoopVal(UserSoleType):
    YESTERDAY_TYPE_NORMAL = 1
    YESTERDAY_TYPE_QUEST = 2
    YESTERDAY_TYPE_LOOP = 3

    def __init__(self, questLoopId):
        super(QuestLoopVal, self).__init__()
        self.questLoopId = questLoopId
        self.loopCnt = 0
        self.beginIndex = 0
        self.abandonQuestId = 0
        self.lastAbandonTime = 0.0
        self.predictQuestId = 0
        self.avlAcCnt = QLD.data.get(questLoopId, {}).get('avlAcCnt', 0) + QLD.data.get(questLoopId, {}).get('avlAbandonCnt', 0)
        self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_NORMAL
        self.lastCompNpc = 0
        self.startAcceptTime = utils.getNow()
        self.questInfo = []
        self.extraInfo = {}

    def getCurrentQuest(self):
        if len(self.questInfo) == 0:
            return None
        elif self.questInfo[-1][1] == True:
            return None
        else:
            return self.questInfo[-1][0]

    def getNextQuests(self, owner, acStep = -1, bMsg = False):
        reAcType = QLD.data.get(self.questLoopId, {}).get('reAcType', gametypes.QUEST_LOOP_REAC_ONE)
        if acStep == -1 and self.predictQuestId > 0 and reAcType == gametypes.QUEST_LOOP_REAC_ONE:
            if commQuest.gainQuestCheck(owner, self.predictQuestId, bMsg):
                return [self.predictQuestId]
            else:
                return []
        else:
            if not QLD.data.has_key(self.questLoopId):
                return []
            if acStep >= 0:
                step = acStep
            else:
                step = self.getCurrentStep()
            avlQuestIds = commQuest.getAvaiNextQuestsInLoop(owner, self.questLoopId, step, bMsg)
            if reAcType == gametypes.QUEST_LOOP_REAC_THREE and self.predictQuestId in avlQuestIds:
                avlQuestIds.remove(self.predictQuestId)
            return avlQuestIds

    def getCurrentStep(self):
        groupNum = QLD.data[self.questLoopId]['groupNum']
        step = len(self.questInfo)
        if step > 0 and self.questInfo[-1][1] == False:
            step -= 1
        return (self.beginIndex + step) % groupNum

    def getRealCurrentStep(self):
        groupNum = QLD.data[self.questLoopId]['groupNum']
        step = len(self.questInfo)
        if step == 0:
            return (0, 0)
        elif self.questInfo[-1][1] == False:
            return ((self.beginIndex + step) % groupNum, gametypes.QUEST_STAGE_ACCEPT)
        else:
            return ((self.beginIndex + step) % groupNum, gametypes.QUEST_STAGE_COMPLETE)

    def isLastStep(self):
        refreshType = QLD.data[self.questLoopId]['refreshType']
        if refreshType in gametypes.QL_CIRCLE_REFRESH_THREE:
            return self.getNextLoopIndex() == 0
        else:
            return self.getNextLoopIndex() == self.beginIndex

    def getNextLoopIndex(self):
        groupNum = QLD.data[self.questLoopId]['groupNum']
        step = self.getCurrentStep()
        return (step + 1) % groupNum

    def getQuestLoopCnt(self, owner, questLoopId):
        info = owner.questLoopInfo.get(questLoopId)
        qldata = QLD.data.get(questLoopId)
        if not qldata:
            return 0
        if not info:
            loopCnt = 0
        else:
            loopCnt = info.loopCnt
            if info.isYesterday():
                loopCnt = 0
        return loopCnt

    def acQuestCheck(self, owner, acStep = -1, bMsg = False):
        if BigWorld.component in 'cell':
            channel = owner.client
        elif BigWorld.component in 'client':
            channel = owner
        if not QLD.data.has_key(self.questLoopId):
            bMsg and channel.chatToEventEx('不存在任务%d' % self.questLoopId, const.CHANNEL_COLOR_RED)
            return False
        qld = QLD.data[self.questLoopId]
        maxLoopCnt = qld['maxLoopCnt']
        canExtraActivity = commActivity.canExtraActivity(self.questLoopId, gametypes.ACTIVITY_REF_QUESTLOOP, owner.rewardPoints, owner.rewardExtraEvents)
        if self.loopCnt >= maxLoopCnt and maxLoopCnt != const.ENDLESS_LOOP_CNT and not canExtraActivity:
            gamelog.debug('@szh: player can not accept loop quest due to maxLoopCnt', self.questLoopId)
            bMsg and channel.chatToEventEx('已经达到最大轮数', const.CHANNEL_COLOR_RED)
            return False
        if len(self.questInfo) > 0 and self.questInfo[-1][1] == False:
            gamelog.debug('@szh: player can not accept loop quest due to curQuestSeq', self.questLoopId)
            bMsg and channel.chatToEventEx('已经领取了任务', const.CHANNEL_COLOR_RED)
            return False
        if acStep >= 0 and self.getCurrentStep() > acStep:
            gamelog.debug('@szh: player can not accept loop quest due to acStep', self.questLoopId)
            bMsg and channel.chatToEventEx('组队任务进度太超前', const.CHANNEL_COLOR_RED)
            return False
        abandonType = QLD.data.get(self.questLoopId, {}).get('abandonType', gametypes.QUEST_LOOP_ABANDON_TYPE_ONE)
        if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO and self.avlAcCnt <= 0:
            gamelog.debug('@szh: player can not accept loop quest due to avlAcCnt', self.questLoopId)
            bMsg and channel.chatToEventEx('已经达到最大环数', const.CHANNEL_COLOR_RED)
            return False
        if BigWorld.component in ('cell',) and qld.has_key('abandonCD'):
            current = time.time()
            if current < self.lastAbandonTime + qld['abandonCD']:
                gamelog.debug('@szh: player can not accept loop quest due to abandon cd', self.questLoopId)
                duration = '%ds' % int(self.lastAbandonTime + qld['abandonCD'] - current)
                bMsg and channel.showGameMsg(GMDD.data.QUEST_WAIT_CD, (duration,))
                return False
        return True

    def acceptQuestInLoop(self, owner, questId, acStep = -1):
        if acStep >= 0 and acStep > self.getCurrentStep():
            qld = QLD.data[self.questLoopId]
            quests = qld['quests']
            for step in xrange(self.getCurrentStep(), acStep):
                choiceQuest = quests[step]
                if type(choiceQuest) is tuple:
                    choiceQuest = random.choice(choiceQuest)
                self.questInfo.append((choiceQuest, True))
                owner.setQuestFlag(choiceQuest)

        self.questInfo.append((questId, False))
        self.predictQuestId = 0
        self.abandonQuestId = 0
        owner.questLoopInfo = owner.questLoopInfo

    def completeQuestCheck(self):
        if len(self.questInfo) == 0:
            return False
        if self.questInfo[-1][1] == True:
            return False
        return True

    def completeQuest(self, owner, npcNo):
        self.questInfo[-1] = (self.questInfo[-1][0], True)
        abandonType = QLD.data.get(self.questLoopId, {}).get('abandonType', gametypes.QUEST_LOOP_ABANDON_TYPE_ONE)
        if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO:
            self.avlAcCnt -= 1
        if not QLD.data.has_key(self.questLoopId):
            return
        self.lastCompNpc = npcNo
        qld = QLD.data[self.questLoopId]
        groupNum = qld['groupNum']
        refreshType = QLD.data[self.questLoopId]['refreshType']
        canFinished = False
        if refreshType in gametypes.QL_CIRCLE_REFRESH_THREE:
            if len(self.questInfo) + self.beginIndex >= groupNum:
                canFinished = True
        elif len(self.questInfo) >= groupNum:
            canFinished = True
        abandonType = QLD.data.get(self.questLoopId, {}).get('abandonType', gametypes.QUEST_LOOP_ABANDON_TYPE_ONE)
        if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO and self.avlAcCnt <= 0:
            canFinished = True
        if self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_QUEST:
            canFinished = True
        if canFinished:
            self._finishLoop(owner)
        owner.questLoopInfo = owner.questLoopInfo

    def _finishLoop(self, owner):
        if self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_LOOP:
            self.loopCnt = 0
        elif self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_QUEST:
            self.loopCnt = 0
        else:
            self.loopCnt += 1
            if gameconfig.enableNewAddDaoHengType():
                owner.checkAddDaoHengByQuestLoop(self.questLoopId, self.loopCnt)
        self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_NORMAL
        for questId in [ x[0] for x in self.questInfo ]:
            owner.cleanQuestFlag(questId)

        self.predictQuestId = 0
        self.abandonQuestId = 0
        self.avlAcCnt = QLD.data.get(self.questLoopId, {}).get('avlAcCnt', 0) + QLD.data.get(self.questLoopId, {}).get('avlAbandonCnt', 0)
        self.questInfo = []
        refreshType = QLD.data.get(self.questLoopId, {}).get('refreshType')
        if refreshType not in gametypes.QL_CIRCLE_REFRESH_TWO:
            self.beginIndex = 0
        self.lastCompNpc = 0
        qldGoldQuestTime = 0
        if self.extraInfo.get(const.QLD_GOLD_QUEST_TIME) and utils.isSameDay(self.extraInfo.get(const.QLD_GOLD_QUEST_TIME), utils.getNow()):
            qldGoldQuestTime = self.extraInfo[const.QLD_GOLD_QUEST_TIME]
        self.extraInfo = {}
        if qldGoldQuestTime:
            self.extraInfo[const.QLD_GOLD_QUEST_TIME] = qldGoldQuestTime
        owner.onOtherAcceptQuestLoopNotify(self.questLoopId, False)
        if QLD.data[self.questLoopId].get('guideMode', 0):
            owner.callTeamMateMethod(const.COMPONENT_CELL, 'onSyncTeamQuestLoopStatus', (owner.gbId, self.questLoopId, const.QLD_FINISH), True, 0)
        if BigWorld.component in ('base', 'cell'):
            shareGroupId = QLD.data[self.questLoopId].get('sharegroupid', 0)
            weight = QLD.data[self.questLoopId].get('weight', 0)
            if shareGroupId and weight:
                questLimit = owner.getOwnClientMiscProperty(gametypes.MISC_VAR_OCLI_LOOP_QUEST_WEIGHT_LIMIT, {})
                if not questLimit.has_key(shareGroupId):
                    questLimit[shareGroupId] = {}
                for limitType in gametypes.LOOP_QUEST_WEIGHT_LIMIT_TYPES:
                    questLimit[shareGroupId][limitType] = questLimit[shareGroupId].get(limitType, 0) + weight

                owner.setOwnClientMiscProperty(gametypes.MISC_VAR_OCLI_LOOP_QUEST_WEIGHT_LIMIT, questLimit)

    def abandonQuestCheck(self):
        if len(self.questInfo) == 0:
            return False
        if self.questInfo[-1][1] == True:
            gamelog.debug('@szh: no quest can be abandoned', self.questLoopId)
            return False
        return True

    def abandonQuest(self, owner):
        if len(self.questInfo) == 0:
            return None
        if self.questInfo[-1][1] == True:
            return None
        self.abandonQuestId = self.getCurrentQuest()
        self.lastAbandonTime = time.time()
        abandonType = QLD.data.get(self.questLoopId, {}).get('abandonType', gametypes.QUEST_LOOP_ABANDON_TYPE_ONE)
        questId = self.questInfo[-1][0]
        canFinishLoop = False
        if self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_QUEST:
            canFinishLoop = True
        if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO:
            if self.avlAcCnt > 0:
                self.avlAcCnt -= 1
            del self.questInfo[-1]
            if self.avlAcCnt <= 0:
                canFinishLoop = True
        elif abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_THREE:
            canFinishLoop = True
        else:
            del self.questInfo[-1]
        if canFinishLoop is True:
            self._finishLoop(owner)
        else:
            reAcType = QLD.data.get(self.questLoopId, {}).get('reAcType', gametypes.QUEST_LOOP_REAC_TWO)
            if reAcType == gametypes.QUEST_LOOP_REAC_ONE or reAcType == gametypes.QUEST_LOOP_REAC_THREE:
                self.predictQuestId = questId
        owner.questLoopInfo = owner.questLoopInfo
        return questId

    def abandonProgress(self, owner):
        qld = QLD.data[self.questLoopId]
        abProgressType = qld.get('abProgressType', gametypes.QUEST_LOOP_ABANDON_PROGRESS_ONE)
        if abProgressType == gametypes.QUEST_LOOP_ABANDON_PROGRESS_ONE:
            return
        self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_NORMAL
        for questId in [ x[0] for x in self.questInfo ]:
            owner.cleanQuestFlag(questId)

        self.predictQuestId = 0
        self.abandonQuestId = 0
        self.avlAcCnt = QLD.data.get(self.questLoopId, {}).get('avlAcCnt', 0) + QLD.data.get(self.questLoopId, {}).get('avlAbandonCnt', 0)
        self.questInfo = []
        self.beginIndex = 0
        if abProgressType == gametypes.QUEST_LOOP_ABANDON_PROGRESS_THREE:
            self.loopCnt += 1
        owner.questLoopInfo = owner.questLoopInfo

    def needActiveReward(self):
        qld = QLD.data[self.questLoopId]
        maxLoopCnt = qld['maxLoopCnt']
        if self.loopCnt >= maxLoopCnt and maxLoopCnt != const.ENDLESS_LOOP_CNT:
            return True
        else:
            return False

    def refreshQuest(self, owner):
        if not QLD.data.has_key(self.questLoopId):
            return
        qld = QLD.data[self.questLoopId]
        refreshType = qld['refreshType']
        maxLoop = qld['maxLoopCnt']
        if len(self.questInfo) == 0 or self.questInfo[-1][1] == True:
            acQuestId = None
        else:
            acQuestId = self.questInfo[-1][0]
        comQuestIds = []
        for questId, flag in self.questInfo:
            if flag == True:
                comQuestIds.append(questId)

        tmpCurrentStep = self.getCurrentStep()
        canRemove = True
        if refreshType in gametypes.QL_LOOPCNT_REFRESH_ONE or refreshType in gametypes.QL_LOOPCNT_REFRESH_TRHEE and acQuestId is None or refreshType in gametypes.QL_LOOPCNT_REFRESH_TWO and self.loopCnt >= maxLoop and maxLoop != const.ENDLESS_LOOP_CNT:
            self.loopCnt = 0
            self.abandonQuestId = 0
            self.lastAbandonTime = 0.0
            self.predictQuestId = 0
            self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_NORMAL
            for questId in comQuestIds:
                owner.cleanQuestFlag(questId)

        elif refreshType in gametypes.QL_LOOPCNT_REFRESH_TWO:
            self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_LOOP
            canRemove = False
        elif refreshType in gametypes.QL_LOOPCNT_REFRESH_TRHEE:
            self.yesterdayType = QuestLoopVal.YESTERDAY_TYPE_QUEST
            canRemove = False
        if refreshType in gametypes.QL_LOOPCNT_REFRESH_ONE or refreshType in gametypes.QL_LOOPCNT_REFRESH_TRHEE and acQuestId is None or refreshType in gametypes.QL_LOOPCNT_REFRESH_TWO and self.loopCnt >= maxLoop and maxLoop != const.ENDLESS_LOOP_CNT:
            if refreshType in gametypes.QL_CIRCLE_REFRESH_ONE:
                self.beginIndex = 0
                self.avlAcCnt = QLD.data.get(self.questLoopId, {}).get('avlAcCnt', 0) + QLD.data.get(self.questLoopId, {}).get('avlAbandonCnt', 0)
            elif refreshType in gametypes.QL_CIRCLE_REFRESH_TWO:
                self.beginIndex = tmpCurrentStep
                self.avlAcCnt = QLD.data.get(self.questLoopId, {}).get('avlAcCnt', 0) + QLD.data.get(self.questLoopId, {}).get('avlAbandonCnt', 0)
                canRemove = False
            elif refreshType in gametypes.QL_CIRCLE_REFRESH_THREE:
                self.beginIndex = tmpCurrentStep
                canRemove = False
            if refreshType in gametypes.QL_ACQUEST_REFRESH_ONE:
                self.questInfo = []
                if acQuestId is not None:
                    if owner._isBody() and qld.get('isCross'):
                        owner.quests.remove(acQuestId)
                        owner.questData.pop(acQuestId)
                    else:
                        owner.abandonQuest(owner.id, acQuestId, isForce=True)
            elif refreshType in gametypes.QL_ACQUEST_REFRESH_TWO:
                self.questInfo = []
                if acQuestId is not None:
                    self.questInfo.append((acQuestId, False))
                    canRemove = False
        owner.questLoopInfo = owner.questLoopInfo
        return canRemove

    def isYesterday(self):
        return self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_LOOP or self.yesterdayType == QuestLoopVal.YESTERDAY_TYPE_QUEST

    def __str__(self):
        return '(' + str(self.loopCnt) + ', ' + str(self.beginIndex) + ', ' + str(self.questInfo) + ')'


class QuestLoops(UserDictType):

    def _lateReload(self):
        super(QuestLoops, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


def getQuestLoopChainNodeIds(questLoopId, hasExp = False):
    nodeIds = []
    i = 0
    while True:
        i += 1
        d = QLCD.data.get((questLoopId, i))
        if d is None:
            break
        if hasExp and not d.get('getBackExpFormula') and not d.get('getBackExpFormulaVip'):
            continue
        nodeIds.append(i)

    return nodeIds


class QuestLoopChainVal(UserSoleType):

    def __init__(self, done = False, lv = 0, closed = False):
        self.done = done
        self.lv = lv
        self.nodeIds = []
        self.acNodeIds = []
        self.closed = closed

    def isHistory(self):
        return self.lv

    def onNodeComplete(self, nodeId):
        if nodeId not in self.nodeIds:
            self.nodeIds.append(nodeId)

    def onGainNode(self, nodeId):
        if nodeId not in self.acNodeIds:
            self.acNodeIds.append(nodeId)
            return True
        return False

    def setCompleted(self, done = True):
        self.done = done


class QuestLoopChainOfDays(UserDictType):

    def __init__(self, questLoopId = 0, getBackFreeCnt = 0, teamQuestId = 0, startTime = 0):
        self.questLoopId = questLoopId
        self.getBackFreeCnt = getBackFreeCnt
        self.teamQuestId = teamQuestId
        self.helpNums = {}
        self.startTime = startTime

    def _lateReload(self):
        super(QuestLoopChainOfDays, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getCurrKey(self):
        keys = self.keys()
        if not keys:
            return 0
        return max(keys)

    def getCurr(self):
        t = self.getCurrKey()
        if not t:
            return None
        return self[t]

    def onQuestCompleted(self, owner, questId):
        if not len(self):
            gamelog.warning('QuestLoopChainOfDays.onQuestCompleted empty', owner.gbId, questId)
            return
        v = self.getCurr()
        i = 0
        bUpdate = False
        while True:
            i += 1
            d = QLCD.data.get((self.questLoopId, i))
            if d is None:
                break
            questIds = d.get('questIds')
            if questIds and questId in questIds:
                r = v.onGainNode(i)
                bUpdate = bUpdate or r
                r = v.onNodeComplete(i)
                bUpdate = bUpdate or r
                break

        if bUpdate:
            self.transfer(owner)

    def onGainQuest(self, owner, questId):
        if not len(self):
            gamelog.warning('QuestLoopChainOfDays.onQuestCompleted empty', owner.gbId, questId)
            return
        v = self.getCurr()
        i = 0
        bUpdate = False
        while True:
            i += 1
            d = QLCD.data.get((self.questLoopId, i))
            if d is None:
                break
            questIds = d.get('acQuestIds')
            if questIds and questId in questIds:
                bUpdate = v.onGainNode(i)
                break

        if bUpdate:
            self.transfer(owner)

    def onQuestLoopCompleted(self, owner):
        if not len(self):
            gamelog.warning('QuestLoopChainOfDays.onQuestLoopCompleted empty', owner.gbId, self.questLoopId)
            return
        v = self.getCurr()
        v.setCompleted()
        self.transfer(owner)

    def closeHistories(self):
        for t, v in self.iteritems():
            if v.isHistory():
                v.closed = True

    def clearHistories(self):
        for t, v in self.items():
            if v.isHistory():
                self.pop(t)

    def getHistories(self, owner):
        d = [ (t, v) for t, v in self.iteritems() if v.isHistory() and not v.closed ]
        d.sort(key=lambda x: x[0])
        d = [ x[1] for x in d ]
        if not owner.isValidVipProp(gametypes.VIP_SERVICE_QUEST_LOOP_CHAIN_GET_BACK_DAY) and len(d) >= self.getHistoryDays():
            d.pop(0)
        return d

    def calcGetBackFreeCnt(self, owner):
        nodeIds = getQuestLoopChainNodeIds(self.questLoopId, hasExp=True)
        freeCnt = 0
        for v in self.getHistories(owner):
            for nodeId in nodeIds:
                if nodeId not in v.acNodeIds:
                    freeCnt += 1

        return freeCnt

    def calcGetBackConsumeFame(self, owner, idx):
        nodeIds = getQuestLoopChainNodeIds(self.questLoopId)
        fames = {}
        for v in self.getHistories(owner):
            for nodeId in nodeIds:
                if nodeId not in v.acNodeIds:
                    consumeFames = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpConsumeFames')
                    if consumeFames:
                        fameId, formulaId = consumeFames[idx]
                        f = FMD.data.get(formulaId, {}).get('formula')
                        if f:
                            if fames.has_key(fameId):
                                fames[fameId] += f({'lv': owner.lv})
                            else:
                                fames[fameId] = f({'lv': owner.lv})

        return [ (fameId, int(cnt)) for fameId, cnt in fames.iteritems() ]

    def calcGetBackCoin(self, owner):
        nodeIds = getQuestLoopChainNodeIds(self.questLoopId)
        coins = 0
        for v in self.getHistories(owner):
            for nodeId in nodeIds:
                if nodeId not in v.acNodeIds:
                    consumeCoinFid = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpConsumeCoinsFid', 0)
                    if consumeCoinFid:
                        f = FMD.data.get(consumeCoinFid, {}).get('formula')
                        if f:
                            coins += f({'lv': owner.lv})

        return int(coins)

    def calcHistoryExp(self, owner, isTpByCoin = False):
        import gamescript
        nodeIds = getQuestLoopChainNodeIds(self.questLoopId)
        exp = 0
        if not isTpByCoin:
            for v in self.getHistories(owner):
                for nodeId in nodeIds:
                    if nodeId not in v.acNodeIds:
                        if owner.isValidVipProp(gametypes.VIP_SERVICE_QUEST_LOOP_CHAIN_GET_BACK_EXP):
                            canBackExpFormula = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpFormulaVip')
                        else:
                            canBackExpFormula = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpFormula')
                        if canBackExpFormula:
                            exp += canBackExpFormula({'lv': v.lv,
                             'flv': gamescript.FORMULA_FLV})

        else:
            for v in self.getHistories(owner):
                for nodeId in nodeIds:
                    if nodeId not in v.acNodeIds:
                        if owner.isValidVipProp(gametypes.VIP_SERVICE_QUEST_LOOP_CHAIN_GET_BACK_EXP):
                            canBackExpFormula = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpFormulaVipByCoins')
                        else:
                            canBackExpFormula = QLCD.data.get((self.questLoopId, nodeId)).get('getBackExpFormulaByCoins')
                        if canBackExpFormula:
                            exp += canBackExpFormula({'lv': v.lv,
                             'flv': gamescript.FORMULA_FLV})

        return int(exp)

    def calcHistoryBonusIds(self, owner, isTpByCoin = False):
        nodeIds = getQuestLoopChainNodeIds(self.questLoopId)
        bonusIds = []
        bonusIdName = 'bonusIdByFame' if not isTpByCoin else 'bonusIdByCoin'
        for v in self.getHistories(owner):
            for nodeId in nodeIds:
                if nodeId not in v.acNodeIds:
                    canBackBonus = QLCD.data.get((self.questLoopId, nodeId)).get(bonusIdName, {})
                    for lvKey, bonusId in canBackBonus.iteritems():
                        if lvKey[0] <= v.lv <= lvKey[1]:
                            bonusIds.append(bonusId)
                            break

        return bonusIds

    def getEnableRewardRecovery(self):
        if BigWorld.component == 'client':
            import gameglobal
            enableRewardRecovery = gameglobal.rds.configData.get('enableRewardRecovery', 0)
        else:
            enableRewardRecovery = gameconfig.enableRewardRecovery()
        return enableRewardRecovery

    def getHistoryDays(self):
        from data import reward_getback_data as RGD
        rgd = RGD.data.get(gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_XUN_LING, {})
        beginTime = rgd.get('consumeItemStartTime')
        endTime = rgd.get('consumeItemEndTime')
        holidayGetBackCount = rgd.get('holidayGetBackCount', 0)
        tNow = utils.getNow()
        if self.getEnableRewardRecovery() and holidayGetBackCount and beginTime and endTime and utils.inTimeTupleRange(beginTime[0], endTime[0], tNow):
            internalSecond = 0
            baset = utils.getMonthSecond()
            i = 0
            while internalSecond <= 0:
                baset -= i * const.TIME_INTERVAL_DAY
                baset = utils.getMonthSecond(baset)
                internalSecond = utils.getDaySecond() - (utils.nextByTimeTuple(beginTime[0], baset) + baset)
                i += 1

            if 365 <= int(round(internalSecond / const.TIME_INTERVAL_DAY)) <= 366:
                return SCD.data.get('questLoopChainHistoryNum', const.QUEST_LOOP_CHAIN_HISTORY_NUM)
            return SCD.data.get('questLoopChainHistoryNum', const.QUEST_LOOP_CHAIN_HISTORY_NUM) + min(int(round(internalSecond / const.TIME_INTERVAL_DAY)), holidayGetBackCount)
        else:
            return SCD.data.get('questLoopChainHistoryNum', const.QUEST_LOOP_CHAIN_HISTORY_NUM)

    def refresh(self, owner, useBirthAsStartTime = True):
        if BigWorld.component == 'client':
            return
        if owner.lv < SCD.data.get('questLoopChainMinLv', 20):
            return
        if not self.startTime:
            if useBirthAsStartTime:
                self.startTime = owner.birthInDBCell or utils.getNow()
            else:
                self.startTime = utils.getNow()
        t = utils.getDaySecond(utils.getNow() - const.EARLY_MORNING_HOUR * const.TIME_INTERVAL_HOUR)
        if self.has_key(t):
            return
        questIds = QLD.data.get(self.questLoopId, {}).get('quests')
        if questIds:
            for _id in questIds:
                if isinstance(_id, tuple):
                    for questId in _id:
                        owner.cleanQuestInfo(questId, syncClient=False)

                elif isinstance(_id, int):
                    owner.cleanQuestInfo(_id, syncClient=False)

        self.helpNums.clear()
        self.teamQuestId = 0
        mint = t - const.TIME_INTERVAL_DAY * self.getHistoryDays()
        mint = max(gameconfig.questLoopChainStartTime(), utils.getServerOpenTime(), self.startTime - const.EARLY_MORNING_HOUR * const.TIME_INTERVAL_HOUR, mint)
        mint = utils.getDaySecond(mint)
        for oldt in self.keys():
            if oldt < mint:
                self.pop(oldt)

        for i in range(self.getHistoryDays()):
            ot = t - (i + 1) * const.TIME_INTERVAL_DAY
            if ot < mint:
                break
            v = self.get(ot)
            if v is None:
                v = QuestLoopChainVal()
                self[ot] = v
            v.lv = owner.lv

        self[t] = QuestLoopChainVal()

    def getDTO(self):
        return (self.questLoopId,
         self.getBackFreeCnt,
         self.teamQuestId,
         [ (tWhen,
          x.lv,
          x.done,
          x.nodeIds,
          x.acNodeIds,
          x.closed) for tWhen, x in self.iteritems() ])

    def fromDTO(self, dto):
        self.questLoopId, self.getBackFreeCnt, self.teamQuestId, vals = dto
        self.clear()
        for d in vals:
            tWhen, lv, done, nodeIds, acNodeIds, closed = d
            val = QuestLoopChainVal(done=done, lv=lv, closed=closed)
            val.nodeIds = nodeIds
            val.acNodeIds = acNodeIds
            self[tWhen] = val

        return self

    def transfer(self, owner):
        owner.client.onSendQuestLoopChain([(self.questLoopId, self.getDTO())])


class QuestLoopChain(UserDictType):

    def _lateReload(self):
        super(QuestLoopChain, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getChainQuestLoopId(self, questId):
        questLoopId = QLID.data.get(questId, {}).get('questLoop')
        return QLCD.data.has_key((questLoopId, 1)) and questLoopId or 0

    def getChain(self, questLoopId = 0):
        if not questLoopId:
            questLoopId = SCD.data.get('questLoopChainDefault')
        if not QLCD.data.has_key((questLoopId, 1)):
            return
        v = self.get(questLoopId)
        if v is None:
            v = QuestLoopChainOfDays(questLoopId=questLoopId)
            self[questLoopId] = v
        return v

    def onQuestCompleted(self, owner, questId):
        questLoopId = QLID.data.get(questId, {}).get('questLoop')
        if not QLCD.data.has_key((questLoopId, 1)):
            return
        v = self.getChain(questLoopId)
        v.onQuestCompleted(owner, questId)
        if owner.groupHeader == owner.id:
            gameengine.getGlobalBase('GroupStub').updateQuestLoopChain(owner.groupNUID, owner.base, owner.gbId, questLoopId, questId, gametypes.QUEST_STAGE_COMPLETE, v.getCurrKey())

    def onGainQuest(self, owner, questId):
        questLoopId = QLID.data.get(questId, {}).get('questLoop')
        if not QLCD.data.has_key((questLoopId, 1)):
            return
        v = self.getChain(questLoopId)
        v.onGainQuest(owner, questId)
        qd = QD.data.get(questId)
        if qd.get('keepGroupGbIds'):
            qlVal = owner.questLoopInfo.get(questLoopId)
            if qlVal and owner.groupNUID and owner.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                qlVal.extraInfo[const.QLD_LAST_GROUP_GBIDS] = (owner.groupNUID, owner.team.keys())
        if owner.groupHeader == owner.id:
            d = [(questLoopId, questId, utils.getDaySecondByEarlyMorning())]
            owner.onSyncQuestLoopChainTeamQuest(d)
            owner.callTeamMateMethod(const.COMPONENT_CELL, 'onSyncQuestLoopChainTeamQuest', (d,), False, 0)
            gameengine.getGlobalBase('GroupStub').updateQuestLoopChain(owner.groupNUID, owner.base, owner.gbId, questLoopId, questId, gametypes.QUEST_STAGE_ACCEPT, v.getCurrKey() or utils.getDaySecondByEarlyMorning())

    def onQuestLoopCompleted(self, owner, questLoopId):
        if not QLCD.data.has_key((questLoopId, 1)):
            return
        v = self.getChain(questLoopId)
        v.onQuestLoopCompleted(owner)

    def onCompShareQuestLoop(self, owner, questLoopId, step):
        if not QLCD.data.has_key((questLoopId, 1)):
            return
        qld = QLD.data.get(questLoopId, {})
        helpBonus = qld.get('helpBonus')
        if helpBonus and len(helpBonus) == len(qld['quests']):
            bonusId, numLimit = helpBonus[step]
            if not bonusId:
                return
            v = self.getChain(questLoopId)
            if numLimit > 0:
                n = v.helpNums.get(step, 0)
                if n >= numLimit:
                    owner.client.showGameMsg(GMDD.data.QUEST_LOOP_CHAIN_HELP_NUM_LIMIT, ())
                    return
            if v.helpNums.has_key(step):
                v.helpNums[step] += 1
            else:
                v.helpNums[step] = 1
            if numLimit:
                owner.client.showGameMsg(GMDD.data.QUEST_LOOP_CHAIN_HELP_NUM, (v.helpNums[step], numLimit))
            owner._assignQuestLoopChainHelpBonus(bonusId)

    def refresh(self, owner, useBirthAsStartTime = True):
        self.getChain()
        for v in self.itervalues():
            v.refresh(owner, useBirthAsStartTime=useBirthAsStartTime)

    def transfer(self, owner):
        owner.client.onSendQuestLoopChain(self.getDTO())

    def getDTO(self):
        return [ (questLoopId, x.getDTO()) for questLoopId, x in self.iteritems() ]

    def fromDTO(self, dto):
        if not dto:
            self.clear()
            return self
        for questLoopId, d in dto:
            self[questLoopId] = QuestLoopChainOfDays().fromDTO(d)

        return self

    def onJoinGroup(self):
        pass

    def onQuitGroup(self):
        for v in self.itervalues():
            v.teamQuestId = 0

    def onBonusHistory(self, owner, questId):
        questLoopId = self.getChainQuestLoopId(questId)
        if not questLoopId:
            return
        v = self.getChain(questLoopId)
        v.onGainQuest(owner, questId)
