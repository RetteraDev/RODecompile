#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcQuest.o
import BigWorld
import gameglobal
import const
import commcalc
import commQuest
import gamelog
import npcConst
import gametypes
import formula
import utils
from guis import uiUtils
from data import quest_loop_data as QLD
from data import quest_npc_data as QND
from data import quest_data as QD
from data import npc_data as ND
from data import quest_group_data as QGD
from data import sys_config_data as SCD
from cdata import quest_loop_inverted_data as QLID
from cdata import quest_npc_relation as QNR
from cdata import game_msg_def_data as GMDD
from data import quest_type_show_data as QTSD

class ImpNpcQuest(object):

    def showQuestWindow(self):
        gamelog.debug('@szh: npc.showQuestWindow', self.id)
        if self._isQuestNpc():
            actionName = self.fashion.getTalkActionName()
            gamelog.debug('showQuestWindow:', actionName)
            if actionName:
                self.fashion.playSingleAction(actionName)
            BigWorld.player().showQuestWindow(self.id)

    def onUpdateQuestDisplay(self, questInfo):
        if self._isQuestNpc():
            resArr = None
            completeResArr = SCD.data.get('sceneQuest', {}).get('complete', ())
            unfinishedResArr = SCD.data.get('sceneQuest', {}).get('unfinished', ())
            availableResArr = SCD.data.get('sceneQuest', {}).get('available', ())
            displayType = None
            if len(questInfo['unfinished_taskLoops']) > 0:
                displayType = self._getMaxPriorityQuestLoopType(questInfo['unfinished_taskLoops'], 'unfinished_taskLoops')
                resArr = unfinishedResArr
            if len(questInfo['unfinished_tasks']) > 0:
                displayType = self._getMaxPriorityQuestType(questInfo['unfinished_tasks'], 'unfinished_tasks')
                resArr = unfinishedResArr
            if len(questInfo['available_taskLoops']) > 0:
                displayType = self._getMaxPriorityQuestLoopType(questInfo['available_taskLoops'], 'available_taskLoops')
                resArr = availableResArr
            if len(questInfo['available_tasks']) > 0:
                displayType = self._getMaxPriorityQuestType(questInfo['available_tasks'], 'available_tasks')
                resArr = availableResArr
            if len(questInfo['complete_taskLoops']) > 0:
                displayType = self._getMaxPriorityQuestLoopType(questInfo['complete_taskLoops'], 'complete_taskLoops')
                resArr = completeResArr
            if len(questInfo['complete_tasks']) > 0:
                displayType = self._getMaxPriorityQuestType(questInfo['complete_tasks'], 'complete_tasks')
                resArr = completeResArr
            if displayType and resArr and int(displayType) > 0 and int(displayType) <= len(resArr):
                effectId = resArr[int(displayType) - 1]
                self.showTaskIndicator(effectId)
            else:
                self.showTaskIndicator(None)
            self.refreshOpacityState()

    def availableQuestEffectShow(self, questId):
        questNeedShow = QD.data.get(questId, {}).get('showCanAcceptNpcLogo', -1)
        if questNeedShow >= 0:
            return questNeedShow
        else:
            displayType = QD.data.get(questId, {}).get('displayType', 0)
            questNeedShow = QTSD.data.get(displayType, {}).get('showCanAcceptNpcLogo', False)
            return questNeedShow
        return True

    def availableQuestLoopEffectShow(self, questId):
        questNeedShow = QLD.data.get(questId, {}).get('showCanAcceptNpcLogo', -1)
        if questNeedShow >= 0:
            return questNeedShow
        else:
            displayType = QLD.data.get(questId, {}).get('displayType', 0)
            questNeedShow = QTSD.data.get(displayType, {}).get('showCanAcceptNpcLogo', False)
            return questNeedShow
        return True

    def _getMaxPriorityQuestType(self, quests, questType):
        qTypes = []
        for questId in quests:
            qData = QD.data.get(questId, {})
            qtype = qData.get('displayType', 0)
            if questType == 'available_tasks':
                if self.availableQuestEffectShow(questId):
                    qTypes.append(qtype)
            else:
                qTypes.append(qtype)

        for qtype in gametypes.ALL_QUEST_DISPLAY_TYPE:
            if qtype in qTypes:
                return qtype

        return -1

    def _getMaxPriorityQuestLoopType(self, questLoops, questType):
        qTypes = []
        for loopId in questLoops:
            if questType == 'available_taskLoops':
                if self.availableQuestLoopEffectShow(loopId):
                    qtype = commQuest.getQuestLoopDisplayType(loopId)
                    qTypes.append(qtype)
            else:
                qTypes.append(commQuest.getQuestLoopDisplayType(loopId))

        for qtype in gametypes.ALL_QUEST_DISPLAY_TYPE:
            if qtype in qTypes:
                return qtype

        return -1

    def getOpacityValueByQuest(self, opacityVal):
        if self.isScenario in (gameglobal.SCENARIO_EDIT_NPC, gameglobal.SCENARIO_PLAY_NPC):
            return (gameglobal.OPACITY_FULL, True)
        elif self.inScenario:
            return (gameglobal.OPACITY_HIDE, False)
        elif opacityVal[0] == gameglobal.OPACITY_HIDE:
            return opacityVal
        player = BigWorld.player()
        if self.npcId in player.hideNpcs.keys():
            return (gameglobal.OPACITY_HIDE, False)
        visibility = self.visibility
        if not QND.data.has_key(self.npcId):
            return opacityVal
        qnd = QND.data[self.npcId]
        if qnd.has_key('initHide'):
            visibility = qnd['initHide']
        if qnd.has_key('status5'):
            for questId in qnd['status5']:
                if questId not in player.quests:
                    break
                needConvoy = QD.data.get(questId, {}).get('needConvoy')
                convoyChartype = player.getQuestData(questId, const.QD_CONVOY, 0)
                if needConvoy and needConvoy == convoyChartype or not needConvoy and convoyChartype:
                    visibility = const.VISIBILITY_SHOW
                    break

        if qnd.has_key('status4'):
            for questId in qnd['status4']:
                if questId in player.quests and not player.getQuestData(questId, const.QD_FAIL, False):
                    visibility = const.VISIBILITY_SHOW
                    break

        if qnd.has_key('status3'):
            for questId in qnd['status3']:
                if commcalc.getQuestFlag(player, questId):
                    visibility = const.VISIBILITY_SHOW
                    break

        if qnd.has_key('status2'):
            for questId in qnd['status2']:
                if questId in player.quests and not player.getQuestData(questId, const.QD_FAIL, False):
                    visibility = const.VISIBILITY_HIDE
                    break

        if qnd.has_key('status1'):
            for questId in qnd['status1']:
                if commcalc.getQuestFlag(player, questId):
                    visibility = const.VISIBILITY_HIDE
                    break

        if visibility == const.VISIBILITY_SHOW:
            return (gameglobal.OPACITY_FULL, True)
        else:
            return (gameglobal.OPACITY_HIDE, False)

    def hideByScenario(self, isHide):
        if isHide == const.VISIBILITY_HIDE:
            self.inScenario = True
            self.hide(isHide)
        else:
            self.inScenario = False
            self.refreshOpacityState()

    def showDebateWindow(self):
        qnd = QND.data[self.npcId]
        if qnd.has_key('debateQst'):
            debateQstId = qnd['debateQst']
            debateChatId = QD.data[debateQstId]['debateChatId']
            gamelog.debug('@szh showDebateWindow', debateQstId, debateQstId)
            gameglobal.rds.ui.debate.openDebatePanel(self.npcId, self.id, debateChatId)

    def onShowDebateWindow(self, result):
        npcName = uiUtils.getNpcName(self.npcId)
        p = BigWorld.player()
        debateQstId = 0
        qnd = QND.data[self.npcId]
        if qnd.has_key('debateQst'):
            debateQstId = qnd['debateQst']
        if result == -1:
            if debateQstId > 0:
                BigWorld.player().cell.onQuestDebate(debateQstId, 1)
            p.showGameMsg(GMDD.data.QUEST_ARGUE_COMPLETE, (npcName,))
        else:
            if debateQstId > 0:
                BigWorld.player().cell.onQuestDebate(debateQstId, 0)
            p.showGameMsg(GMDD.data.QUEST_ARGUE_FAIL, (npcName,))
        gameglobal.rds.ui.debate.closeDebatePanel()

    def onAcceptQuest(self, questId):
        actionName = self.fashion.action.getAcceptAction()
        self.fashion.playSingleAction(actionName)
        if self.topLogo:
            failDialog = QD.data.get(questId, {}).get('bubbleDialog', '')
            if failDialog:
                self.topLogo.setChatMsg(failDialog, SCD.data.get('NpcTopLogoTime', 3))

    def onCompleteQuest(self, questId):
        actionName = self.fashion.action.getSubmitAction()
        self.fashion.playSingleAction(actionName)
        if self.getNpcPriority() not in (gameglobal.NPC_WITH_AVAILABLE_QUEST, gameglobal.NPC_WITH_COMPLETE_QUEST):
            return
        p = BigWorld.player()
        qnr = QNR.data.get(self.npcId, {})
        acQuests = qnr.get('acQuests', ())
        comQuests = qnr.get('comQuests', ())
        acQuestLoops = qnr.get('acQuestGroups', {})
        comQuestLoops = qnr.get('comQuestGroups', {})
        questInfo = commQuest.getQuestInfo(p, acQuests, comQuests, acQuestLoops, comQuestLoops, self.npcId)
        acSucQst = []
        if QLID.data.has_key(questId):
            questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
            if qnr.has_key('acQuestGroups') and qnr['acQuestGroups'].has_key(questLoopId) and questLoopId in questInfo['available_taskLoops']:
                nextIds = p.questLoopInfo[questLoopId].getNextQuests(p)
                acSucQst = [ x for x in qnr['acQuestGroups'][questLoopId] if x in nextIds ]
        else:
            td = QD.data.get(questId, {})
            if td.has_key('acSucQst'):
                acSucQst = [ x for x in td['acSucQst'] if x in questInfo['available_tasks'] ]
        acAvlQst = []
        for sucQuestId in acSucQst:
            popMode = QD.data.get(sucQuestId, {}).get('acSucPopMode', gametypes.QUEST_SUC_AUTO_POP)
            if popMode == gametypes.QUEST_SUC_AUTO_POP:
                acAvlQst.append(sucQuestId)
            elif popMode == gametypes.QUEST_SUC_LEADER_POP:
                if self.id == self.groupHeader:
                    acAvlQst.append(sucQuestId)

        if len(acAvlQst) > 0:
            p.showQuestWindow(self.id)

    def acceptQuest(self, questId):
        if not self.inWorld:
            return
        if not QD.data.has_key(questId) or commQuest.isQuestDisable(questId):
            gamelog.error('@szh: the quest %d does not exist' % questId)
            return
        anpc = QD.data[questId]['acNpc']
        if not isinstance(anpc, tuple):
            anpc = tuple([anpc])
        if self.npcId not in anpc:
            gamelog.error('@szh: the quest %d can not assign the quest %d' % self.npcId)
            return
        player = BigWorld.player()
        if not commQuest.gainQuestCheck(player, questId, True):
            return
        self.cell.acceptQuest(questId)

    def completeQuest(self, questId, options):
        if not self.inWorld:
            return
        else:
            player = BigWorld.player()
            if player is None:
                gamelog.error('@szh: the completeQuest quest player is None')
                return
            if not QD.data.has_key(questId):
                gamelog.error('@szh: the completeQuest quest does not exist', questId)
                return
            cnpc = QD.data[questId]['compNpc']
            if not isinstance(cnpc, tuple):
                cnpc = tuple([cnpc])
            if self.npcId not in cnpc:
                gamelog.error('@szh: the quest %d can not complete the quest %d' % (self.npcId, questId))
                return
            if not commQuest.completeQuestCheck(player, questId, True):
                return
            optionKeys = options.keys()
            optionVals = [ options[k] for k in optionKeys ]
            self.cell.completeQuest(questId, optionKeys, optionVals)
            return

    def acceptQuestLoop(self, questLoopId):
        player = BigWorld.player()
        if player is None:
            gamelog.error('@szh: the acceptQuest quest player is None')
            return
        elif not QLD.data.has_key(questLoopId) or commQuest.isQuestLoopDisable(questLoopId):
            gamelog.error('@szh: the questLoopId does not exist', questLoopId)
            return
        elif not hasattr(self, 'npcId'):
            gamelog.error('jjh@impNpcQuest: Npc object has no attribute npcId', questLoopId)
            return
        else:
            qnr = QNR.data.get(getattr(self, 'npcId', 0), {})
            acQuestloops = qnr.get('acQuestGroups', [])
            if questLoopId not in acQuestloops:
                gamelog.error('@szh: the npc can not accept the quest loop', self.npcId, questLoopId)
                return
            elif not commQuest.gainQuestLoopCheck(player, questLoopId, True, npcNo=self.npcId):
                return
            self.cell.acceptQuestLoop(questLoopId)
            return

    def completeQuestLoop(self, questLoopId, options):
        player = BigWorld.player()
        if not self.inWorld:
            return
        elif player is None:
            gamelog.error('@szh: the completeQuest quest player is None')
            return
        elif not QLD.data.has_key(questLoopId):
            gamelog.error('@szh: the questLoopId does not exist', questLoopId)
            return
        else:
            qnr = QNR.data.get(self.npcId)
            comQuestLoops = qnr.get('comQuestGroups', [])
            if questLoopId not in comQuestLoops:
                gamelog.error('@szh: the npc can not accept the quest loop', self.npcId, questLoopId)
                return
            elif not commQuest.completeQuestLoopCheck(player, questLoopId, True):
                return
            optionKeys = options.keys()
            optionVals = [ options[k] for k in optionKeys ]
            self.cell.completeQuestLoop(questLoopId, optionKeys, optionVals)
            return

    def showMultiNpcChatWindow(self, chatId):
        actionName = self.fashion.action.getTalkAction()
        self.fashion.playSingleAction(actionName)
        gameglobal.rds.ui.multiNpcChat.openMultiNpcChatWindow(self.id, self.npcId, chatId, False, False)

    def autoDelQuestNearBy(self):
        player = BigWorld.player()
        if not QNR.data.has_key(self.npcId):
            return
        acQuests = QNR.data[self.npcId].get('acQuests', ())
        for questId in player.quests:
            if not player._isQuestFailed(questId):
                continue
            qd = QD.data.get(questId, {})
            if qd.has_key('questGroup') and not commQuest.isQuestGroupMatch(player, qd['questGroup']):
                questGroupId = qd['questGroup']
                firstQuestId = QGD.data[questGroupId]['quests'][0]
            else:
                firstQuestId = questId
            if firstQuestId not in acQuests:
                continue
            if qd.get('notAutoAbandon', 0) > 0:
                continue
            player.cell.abandonQuest(questId)

        acQuestLoops = QNR.data[self.npcId].get('acQuestGroups', {})
        for questLoopId, acQuests in acQuestLoops.iteritems():
            if questLoopId not in player.questLoopInfo:
                continue
            for questId in acQuests:
                if questId not in player.quests:
                    continue
                if not player._isQuestFailed(questId):
                    continue
                qd = QD.data[questId]
                if qd.get('notAutoAbandon', 0) > 0:
                    continue
                player.cell.abandonQuestLoop(questLoopId)
                break

    def getNpcPriority(self):
        p = BigWorld.player()
        npcData = ND.data.get(self.npcId, {})
        functions = self.filterFunctions()
        funcs = [ x[1] for x in functions ]
        if npcConst.NPC_FUNC_QUEST in funcs:
            completeResArr = SCD.data.get('sceneQuest', {}).get('complete', ())
            unfinishedResArr = SCD.data.get('sceneQuest', {}).get('unfinished', ())
            availableResArr = SCD.data.get('sceneQuest', {}).get('available', ())
            if self.taskEffect:
                effectId = self.taskEffect[0]
                if effectId in completeResArr:
                    return gameglobal.NPC_WITH_COMPLETE_QUEST
                if effectId in availableResArr:
                    return gameglobal.NPC_WITH_AVAILABLE_QUEST
                if effectId in unfinishedResArr:
                    return gameglobal.NPC_WITH_UNCOMPLETE_QUEST
            qnr = QNR.data.get(self.npcId, {})
            acQuests = qnr.get('acQuests', ())
            comQuests = qnr.get('comQuests', ())
            acQuestLoops = qnr.get('acQuestGroups', {})
            comQuestLoops = qnr.get('comQuestGroups', ())
            if commQuest.hasCompleteQuests(p, comQuests, self.npcId) or commQuest.hasCompleteQuestLoops(p, comQuestLoops, self.npcId):
                return gameglobal.NPC_WITH_COMPLETE_QUEST
            if commQuest.hasAcceptQuests(p, acQuests, self.npcId) or commQuest.hasAcceptQuestLoops(p, acQuestLoops, self.npcId):
                return gameglobal.NPC_WITH_AVAILABLE_QUEST
            if commQuest.hasUncompleteQuests(p, comQuests, self.npcId) or commQuest.hasUnCompleteQuestLoops(p, comQuestLoops, self.npcId):
                return gameglobal.NPC_WITH_UNCOMPLETE_QUEST
            debateQuestId = QND.data.get(self.npcId, {}).get('debateQst', -1)
            if debateQuestId in p.quests and not p.getQuestData(debateQuestId, const.QD_QUEST_DEBATE):
                return gameglobal.NPC_WITH_UNCOMPLETE_QUEST
            funcs.remove(npcConst.NPC_FUNC_QUEST)
        if npcConst.NPC_FUNC_MARKER in funcs:
            funcs.remove(npcConst.NPC_FUNC_MARKER)
        if funcs:
            return gameglobal.NPC_WITH_FUNC
        chat = npcData.get('chat', [])
        if chat:
            return gameglobal.NPC_WITH_NO_FUNC
        return gameglobal.NPC_WITH_NO_CHAT

    def getCompleteQuests(self):
        qnr = QNR.data.get(self.npcId, {})
        comQuests = qnr.get('comQuests', ())
        if not comQuests:
            return []
        acQuests = ()
        acQuestLoops = {}
        comQuestLoops = {}
        p = BigWorld.player()
        questInfo = commQuest.getQuestInfo(p, acQuests, comQuests, acQuestLoops, comQuestLoops, self.npcId)
        return questInfo['complete_tasks']

    def showSucBubbleDialog(self):
        quests = self.getCompleteQuests()
        if self.topLogo:
            for questId in quests:
                dialog = QD.data.get(questId, {}).get('sucBubbleDialog', '')
                if dialog:
                    self.topLogo.setChatMsg(dialog, SCD.data.get('NpcTopLogoTime', 3))
                    break

    def questTopLogoRefresh(self):
        if not self.inWorld:
            return
        nextTime = 0
        qnr = QNR.data.get(self.npcId, {})
        acQuestLoops = qnr.get('acQuestGroups', {})
        comQuestLoops = qnr.get('comQuestGroups', {})
        questLoopIds = acQuestLoops.keys() + comQuestLoops.keys()
        current = BigWorld.player().getServerTime()
        for questLoopId in questLoopIds:
            qld = QLD.data[questLoopId]
            weekSet = qld.get('weekSet', 0)
            timerIntervals = qld.get('acStartTimes', ()) + qld.get('acEndTimes', ()) + qld.get('comStartTimes', ()) + qld.get('comEndTimes', ())
            for interval in timerIntervals:
                tmpNextTime = utils.nextByTimeTuple(interval, current)
                if not utils.isInvalidWeek(weekSet, tmpNextTime + current) and (nextTime == 0 or tmpNextTime < nextTime):
                    nextTime = tmpNextTime

            for startXingjiTime, endXingjiTime in qld.get('acXingjiTimes', ()) + qld.get('comXingjiTimes', ()):
                tmpNextTime = formula.getRealTimeToAXingJiMoment(startXingjiTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime
                tmpNextTime = formula.getRealTimeToAXingJiMoment(endXingjiTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime

        BigWorld.player().updateQuestDisplay((self.id,))
        if nextTime > 0:
            self.questTopLogoTimer = BigWorld.callback(nextTime + 2, self.questTopLogoRefresh)

    def pushToHeaderB4DoWithQuestLoop(self, questLoopId, type, options):
        if not self.inWorld:
            return
        else:
            player = BigWorld.player()
            if player is None:
                gamelog.error('@zkl: the pushToHeaderB4DoWithQuestLoop player is None with qid and type', questLoopId, type)
                return
            if not QLD.data.has_key(questLoopId):
                gamelog.error('@zkl: the questLoopId does not exist', questLoopId)
                return
            if type == 1 and commQuest.isQuestLoopDisable(questLoopId):
                gamelog.error('@zkl: the questLoopId does not exist', questLoopId)
                return
            if not hasattr(self, 'npcId'):
                gamelog.error('@zkl: Npc object has no attribute npcId with qid and type', questLoopId, type)
                return
            qnr = QNR.data.get(getattr(self, 'npcId', 0), {})
            if 1 == type:
                questLoops = qnr.get('acQuestGroups', [])
            elif 2 == type:
                questLoops = qnr.get('comQuestGroups', [])
            if questLoopId not in questLoops:
                gamelog.error('@zkl: the npc can not accept/complete the quest loop', self.npcId, questLoopId, type)
                return
            if 1 == type:
                if not commQuest.gainQuestLoopCheck(player, questLoopId, True, npcNo=self.npcId):
                    return
            elif 2 == type:
                if not commQuest.completeQuestLoopCheck(player, questLoopId, True):
                    return
            optionKeys = options.keys()
            optionVals = [ options[k] for k in optionKeys ]
            self.cell.pushToHeaderB4DoWithQuestLoop(questLoopId, type, optionKeys, optionVals)
            return
