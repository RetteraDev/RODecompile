#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impQuest.o
from gamestrings import gameStrings
import random
import copy
import BigWorld
import const
import commcalc
import gameglobal
import gametypes
import commQuest
import utils
import gamelog
import clientcom
import formula
import keys
import Math
import commActivity
from sfx import sfx
from callbackHelper import Functor
from item import Item
from guis import events
from guis import messageBoxProxy
from guis import uiConst
from guis import uiUtils
from helpers import scenario
from helpers.eventDispatcher import Event
from helpers import gameAntiCheatingManager
from sfx import birdEffect
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
from data import quest_data as QD
from data import npc_data as ND
from data import dialogs_data as DD
from data import quest_dialog_data as QDD
from data import item_data as ID
from data import state_data as SD
from data import monster_data as MD
from data import quest_marker_data as QMD
from data import npc_model_client_data as NMCD
from data import quest_loop_data as QLD
from data import quest_story_avl_data as QAD
from data import sys_config_data as SCD
from data import activity_basic_data as ABD
from data import consumable_item_data as CID
from data import quest_group_data as QGD
from data import quest_extra_data as QED
from data import quest_goal_order_data as QOD
from data import quest_loop_avl_data as QLAD
from data import game_msg_data as GMD
from data import monster_event_trigger_data as METD
from data import monster_model_client_data as MMCD
from data import seeker_data as SKD
from cdata import quest_delegation_inverted_data as QDID
from cdata import quest_loop_inverted_data as QLID
from data import avl_quest_update_relation_data as AQURD
from data import avl_quest_loop_update_relation_data as AQLURD
from data import avl_quest_update_lv_data as AQULD
from cdata import business_lv_config_data as BLCD
from data import business_config_data as BCD
from cdata import quest_reward_data as QRD
from cdata import quest_npc_relation as QNR
from cdata import game_msg_def_data as GMDD
from data import intimacy_quest_update_relation_data as IQURD
from data import intimacy_data as IMD
from data import intimacy_config_data as ICD
from data import qiren_quest_update_relation_data as QQURD
from data import jingjie_data as JJD
from data import tutorial_quest_data as TQD
from data import world_quest_refresh_data as WQRD
from data import interactive_data as ITD
from cdata import quest_marker_group_data as QMGD
from cdata import quest_npc_group_data as QNGD
from cdata import quest_monster_group_data as QMOGD
from cdata import quest_item_group_data as QIGD

class ImpQuest(object):
    QUEST_INTERVAL = 5

    def acceptQuest(self, questId, isSucc):
        if isSucc:
            gameglobal.rds.ui.littleMap.acceptQuestDone(questId)
            gameglobal.rds.tutorial.onAcceptQuest(questId)
            qd = QD.data[questId]
            if (gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow) and not self.hasQuestData(questId, const.QD_PUZZLE) and not (QD.data.get(questId, {}).get('displayType', 0) == gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION and gameglobal.rds.ui.noticeBoard.med):
                if gameglobal.rds.ui.jobBoard.detailMed:
                    gameglobal.rds.ui.jobBoard.closeDetail()
                else:
                    if gameglobal.rds.ui.quest.isShow:
                        gameglobal.rds.ui.quest.close(showCursor=True)
                    if gameglobal.rds.ui.npcV2.isShow:
                        gameglobal.rds.ui.npcV2.leaveStage()
            gameglobal.rds.ui.taskShare.close()
            questName = qd.get('name', '')
            if commQuest.isDelegation(questId):
                BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.DELEGATE_ACCEPTED, (questName,)))
            else:
                acMsgNotShow = qd.get('acMsgNotShow', 0)
                if not acMsgNotShow:
                    BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.QUEST_ACCEPTED, (questName, qd.get('autoAc', 0))))
            self._addBoxFx(questId)
            self._addMarkFx(questId)
            self._addChatFx(questId)
            self._addMonsterFx(questId)
            self._addJobMarkFx(questId)
            self._addDebateFx(questId)
            self._addFunNpcFx(questId)
            gameglobal.rds.sound.playSound(gameglobal.SD_18)
            oldQuestMonsterInfo = copy.deepcopy(self.questMonsterInfo)
            self.questMonsterInfo = self._getQuestMonserInfoByQuestId(questId, self.questMonsterInfo)
            addQuestMonsterTypes = [ item for item in self.questMonsterInfo.keys() if item not in oldQuestMonsterInfo.keys() ]
            gameglobal.rds.ui.refreshQuestIcon(addQuestMonsterTypes, True)
            self._updateQuestMonsterLogo()
            if qd.get('afterAcDialog', 0):
                acNpcId = commQuest.getAcNpc(self, questId)
                self.autoServerShowQuestWindow(questId, acNpcId, True)
            if self.hasQuestData(questId, const.QD_PUZZLE):
                if not qd.get('notPuzzleDirectUI'):
                    self.puzzleQuestUI(questId)
            if gameglobal.rds.ui.jobBoard.detailMed:
                gameglobal.rds.ui.jobBoard.closeDetail()
            if gameglobal.rds.ui.jobBoard.mediator:
                gameglobal.rds.ui.jobBoard.startPolling()
            gameglobal.rds.ui.lifeSkillNew.refreshPanel()
            aEvent = Event(events.EVENT_QUEST_ACCEPT, {'questId': questId})
            gameglobal.rds.ui.dispatchEvent(aEvent)
            quests = SCD.data.get('jingSuQuests', (const.QINGGONG_JINGSU_QUEST,))
            for questId in quests:
                if questId in self.quests:
                    if getattr(self, 'groupNUID', None):
                        self.cell.cancelGroupFollow()

            questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
            if QLD.data.get(questLoopId, {}).get('guideMode', 0):
                self.queryTeamGuideQuestStatusWithQid(questId)
            gameAntiCheatingManager.getInstance().startRecordLog()

    def acceptQuestLoopByDiceInClient(self, eventType, questLoopId):
        birdEffect.showBirdEffect(Functor(self._acceptQuestLoopByDiceInClient, eventType, questLoopId))

    def _acceptQuestLoopByDiceInClient(self, eventType, questLoopId):
        if questLoopId in self.questLoopInfo:
            questIds = self.questLoopInfo[questLoopId].getNextQuests(self)
        else:
            questIds = commQuest.getAvaiNextQuestsInLoop(self, questLoopId, 0)
        gamelog.debug('_acceptQuestLoopByDiceInClient', questIds)
        chatId = 0
        if questIds:
            questId = questIds[0]
            chatId = QD.data[questId].get('acDialog', 0)
        if chatId:
            gameglobal.rds.ui.diceQuest.show(questLoopId, chatId)
        else:
            self.cell.acceptQuestLoopByDice(questLoopId)

    def isKuiLingQuest(self, questId):
        if self.kuilingQuests.has_key(questId):
            return True
        else:
            return False

    def completeQuest(self, questId, isSucc):
        if isSucc:
            self.updateLastCompletedQuestInfo(questId)
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            questName = QD.data[questId].get('name', '')
            if commQuest.isDelegation(questId):
                BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.DELEGATE_COMPLETED, (questName,)))
            else:
                comMsgNotShow = QD.data[questId].get('comMsgNotShow', 0)
                if not comMsgNotShow:
                    BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.QUEST_COMPLETED, (questName, QD.data[questId].get('autoComp', 0))))
            self._removeBoxFx(questId)
            self._removeMarkFx(questId)
            self._removeChatFx(questId)
            self._removeMonsterFx(questId)
            self._removeJobMarkFx(questId)
            self._removeDebateFx(questId)
            self._removeFunNpcFx(questId)
            gameglobal.rds.sound.playSound(gameglobal.SD_19)
            self._removeQuestMonsterByQuestId(questId)
            self._updateQuestMonsterLogo()
            self.onFinishQuest(questId)
            if QD.data.get(questId, {}).get('afterSucDialog', 0):
                compNpc = QD.data.get(questId, {}).get('compNpc', 0)
                self.autoServerShowQuestWindow(questId, compNpc, False)
            if gameglobal.rds.ui.puzzle.mediator:
                gameglobal.rds.ui.puzzle.questFinished()
            if self.isKuiLingQuest(questId):
                gameglobal.rds.ui.lifeSkillNew.refreshPanel()
            gameglobal.rds.tutorial.onCompletedQuest(questId)
            cEvent = Event(events.EVENT_QUEST_COMPLETE, {'questId': questId})
            gameglobal.rds.ui.dispatchEvent(cEvent)
            enableCompleteQuestTip = gameglobal.rds.configData.get('enableCompleteQuestTip', True)
            if enableCompleteQuestTip and QD.data.get(questId, {}).get('completeAni', 0):
                offsetH, offsetV = SCD.data.get('QuestCompleteTipPos', (0, 0))
                gameglobal.rds.ui.showScreenUI('widgets/QuestCompleteTip.swf', 46, True, offsetH, offsetV)
            for id in self.transportIdSet:
                entity = BigWorld.entities.get(id, None)
                if entity:
                    entity.refreshOpacityState()

            gameglobal.rds.ui.excitementIcon.refreshInfo()
            gameglobal.rds.ui.excitementDetail.refreshInfo()
            gameglobal.rds.ui.roleInfoFame.updateFameByQuestId(questId)
            questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
            if QLD.data.get(questLoopId, {}).get('guideMode', 0):
                self.queryTeamGuideQuestStatusWithQid(questId)
            gameAntiCheatingManager.getInstance().startRecordLog()

    def abandonQuest(self, questId, isSucc):
        if isSucc:
            if questId in self.quests:
                self.quests.remove(questId)
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            questName = QD.data[questId].get('name', '')
            if commQuest.isDelegation(questId):
                BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.DELEGATE_ABORTED, (questName,)))
            else:
                BigWorld.callback(2, Functor(self.showGameMsg, GMDD.data.QUEST_ABORTED, (questName,)))
            self._removeBoxFx(questId)
            self._removeMarkFx(questId)
            self._removeChatFx(questId)
            self._removeMonsterFx(questId)
            self._removeJobMarkFx(questId)
            self._removeDebateFx(questId)
            self._removeQuestMonsterByQuestId(questId)
            self._updateQuestMonsterLogo()
            self._removeFunNpcFx(questId)
            scenarioIns = scenario.Scenario.getInstanceInPlay()
            if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_END:
                scenarioIns.stopPlay()
            if gameglobal.rds.ui.puzzle.mediator:
                gameglobal.rds.ui.puzzle.questFinished()
            reAccSeekId = QD.data.get(questId, {}).get('reAccSeekId', 0)
            if reAccSeekId:
                seekData = SKD.data.get(reAccSeekId, {})
                if seekData:
                    msg = gameStrings.TEXT_IMPQUEST_297 % (reAccSeekId, seekData.get('name', ''))
                    linkTip = '(%s, %s, %s)' % (int(seekData.get('xpos', '')), int(seekData.get('ypos', '')), int(seekData.get('zpos', '')))
                    gameglobal.rds.ui.messageBox.showAlertBox(msg, linkOverTip=linkTip)
            abEvent = Event(events.EVENT_QUEST_ABANDON, {'questId': questId})
            gameglobal.rds.ui.dispatchEvent(abEvent)
            questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
            if QLD.data.get(questLoopId, {}).get('guideMode', 0):
                self.queryTeamGuideQuestStatusWithQid(questId)

    def checkTeleport(self, questId, questStage):
        if not QD.data.has_key(questId):
            return False
        td = QD.data[questId]
        keyName = ''
        if questStage == 1:
            keyName = 'acEvent'
        elif questStage == 2:
            keyName = 'comEvent'
        elif questStage == 3:
            keyName = 'cclEvent'
        if td.has_key(keyName):
            for item in td[keyName]:
                if 'teleport' == item[0]:
                    return True

        return False

    def checkAcZaijuQst(self, questId):
        if not QD.data.has_key(questId):
            return False
        else:
            td = QD.data[questId]
            if td.has_key('acReqZaiju'):
                return True
            return False

    def checkAddBuff(self, questId, questStage):
        if not QD.data.has_key(questId):
            return False
        td = QD.data[questId]
        keyName = ''
        if questStage == 1:
            keyName = 'acEvent'
        elif questStage == 2:
            keyName = 'comEvent'
        elif questStage == 3:
            keyName = 'cclEvent'
        if td.has_key(keyName):
            for item in td[keyName]:
                if 'addBuff' == item[0]:
                    return True

        return False

    def checkRewardItems(self, questId, rewardChoice):
        rewardChoiceItems = commQuest.genQuestRewardChoice(self, questId)
        if rewardChoice < 0 or rewardChoice >= len(rewardChoiceItems):
            return False
        itemId, itemNum = rewardChoiceItems[rewardChoice]
        item = Item(itemId, itemNum)
        if ID.data[item.id].has_key('schReq') and self.school not in ID.data[item.id]['schReq']:
            return False
        return True

    def getQuestFlag(self, questId):
        return commcalc.getQuestFlag(self, questId)

    def getQuestLoopFlag(self, questLoopId):
        return commcalc.getBit(self.questLoopFlag, questLoopId)

    def getQuestForbidFlag(self, questId):
        return commcalc.getBit(self.questForbidFlag, questId)

    def getQuestLoopForbidFlag(self, questLoopId):
        return commcalc.getBit(self.questLoopForbidFlag, questLoopId)

    def getPuzzleChoiceFlag(self, choiceId):
        return commcalc.getBit(self.puzzleChoiceFlag, choiceId)

    def hasQuestData(self, key1, key2):
        if not self.questData.has_key(key1):
            return False
        if not self.questData[key1].has_key(key2):
            return False
        return True

    def setQuestData(self, key1, key2, data):
        if self.questData.has_key(key1):
            self.questData[key1][key2] = data
        else:
            self.questData[key1] = {}
            self.questData[key1][key2] = data

    def getQuestData(self, key1, key2, default = None):
        if not self.hasQuestData(key1, key2):
            return default
        return self.questData[key1][key2]

    def onShowQuestWindow(self, questInfo, questNpcId):
        npc = BigWorld.entities.get(questNpcId)
        npcId = None
        if npc and npc.inWorld:
            npcId = npc.npcId
        if npc is None:
            return
        else:
            gamelog.debug('@szh: onShowQuestWindow', questInfo)
            if ND.data[npc.npcId].has_key('Uichat'):
                uiChat = ND.data[npc.npcId].get('Uichat')
                uiChat = random.choice(uiChat)
                chatContent = DD.data.get(uiChat, {}).get('details', '')
            else:
                chatContent = ''
            res = {'available_tasks': [],
             'unfinished_tasks': [],
             'complete_tasks': [],
             'available_taskLoops': [],
             'unfinished_taskLoops': [],
             'complete_taskLoops': [],
             'chat': self._getDialog(chatContent)}
            for questId, reward in questInfo['available_tasks']:
                chatId = QD.data[questId].get('acDialog', 0)
                if commQuest.isQuestDisable(questId) or chatId == 0:
                    continue
                bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                quest = {'id': questId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': chatId,
                 'words': self._getDialog(QDD.data[chatId]['chat'], questId),
                 'aside': QDD.data[chatId]['aside'],
                 'interval': QDD.data[chatId].get('interval', []),
                 'speaker_ids': self._getSpeakIds(chatId, npcId),
                 'speakEvents': QDD.data[chatId].get('speakEvent', None),
                 'overTaken_tasks': QD.data[questId].get('acPreQst', ()),
                 'expBonus': int(reward[0] * bonusFactor),
                 'goldBonus': int(reward[1] * bonusFactor),
                 'socExp': int(reward[2] * bonusFactor),
                 'compFame': [ (fameId, int(fameVal * bonusFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId) if not QD.data.get(questId, {}).get('rewardItemsRate', 0) else [],
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                res['available_tasks'].append(quest)

            for questId in questInfo['unfinished_tasks']:
                failWords = QD.data[questId].get('failDialog', '')
                if commQuest.isQuestDisable(questId):
                    continue
                bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                quest = {'id': questId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': 0,
                 'words': self._getDialog([failWords], questId),
                 'aside': [0],
                 'interval': [],
                 'speaker_ids': [npc.npcId],
                 'compFame': [ (fameId, int(fameVal * bonusFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId) if not QD.data.get(questId, {}).get('rewardItemsRate', 0) else [],
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                res['unfinished_tasks'].append(quest)

            for questId in questInfo['complete_tasks']:
                chatId = QD.data[questId].get('sucDialog', -1)
                if commQuest.isQuestDisable(questId) or chatId == -1:
                    continue
                bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                quest = {'id': questId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': chatId,
                 'words': self._getDialog(QDD.data[chatId]['chat'], questId),
                 'aside': QDD.data[chatId]['aside'],
                 'interval': QDD.data[chatId].get('interval', []),
                 'speaker_ids': self._getSpeakIds(chatId, npcId),
                 'speakEvents': QDD.data[chatId].get('speakEvent', None),
                 'compFame': [ (fameId, int(fameVal * bonusFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId) if not QD.data.get(questId, {}).get('rewardItemsRate', 0) else [],
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                if commQuest.completeQuestExtraCheck(self, questId):
                    quest['hasExtraReward'] = True
                    quest['extraRewardItems'] = commQuest.genQuestExtraRewardItems(self, questId)
                    quest['extraRewardChoice'] = commQuest.genQuestExtraRewardChoice(self, questId)
                res['complete_tasks'].append(quest)

            for questLoopId, reward in questInfo['available_taskLoops']:
                if questLoopId in self.questLoopInfo:
                    questIds = self.questLoopInfo[questLoopId].getNextQuests(self)
                else:
                    questIds = commQuest.getAvaiNextQuestsInLoop(self, questLoopId, 0)
                if commQuest.isQuestLoopDisable(questLoopId):
                    continue
                if len(questIds) > 0:
                    questId = questIds[0]
                    chatId = QD.data[questId].get('acDialog', 0)
                    qld = QLD.data.get(questLoopId, {})
                    randType = qld.get('ranType', 1)
                    bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                    fameAwardFactor = commQuest.getQuestLoopAwardFactorByType(self, questLoopId, gametypes.QUEST_REWARD_CREDIT)
                    quest = {'id': questId,
                     'questLoopId': questLoopId,
                     'questNpcId': questNpcId,
                     'name': QD.data.get(questId, {}).get('name', ''),
                     'chatId': chatId,
                     'words': self._getDialog(QDD.data.get(chatId, {}).get('chat', ''), questId),
                     'aside': QDD.data.get(chatId, {}).get('aside', []),
                     'interval': QDD.data.get(chatId, {}).get('interval', []),
                     'speaker_ids': self._getSpeakIds(chatId, npcId),
                     'speakEvents': QDD.data.get(chatId, {}).get('speakEvent', None),
                     'overTaken_tasks': QD.data.get(chatId, {}).get('acPreQst', ()),
                     'expBonus': reward[0],
                     'goldBonus': reward[1],
                     'socExp': reward[2],
                     'compFame': reward[3] if reward[3] else [ (fameId, int(fameVal * bonusFactor * fameAwardFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                     'rewardItems': commQuest.genQuestRewardItems(self, questId, True) if randType == gametypes.QUEST_LOOP_SELECT_SEQUENCE and not self._isFirstClueQuest(questId, questLoopId) else qld.get('bonusItem', ()),
                     'rewardChoice': commQuest.genQuestRewardChoice(self, questId) if randType == gametypes.QUEST_LOOP_SELECT_SEQUENCE else (),
                     'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId) if randType == gametypes.QUEST_LOOP_SELECT_SEQUENCE else (),
                     'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                    self.checkLoopReward(questId, questLoopId, quest)
                    res['available_taskLoops'].append(quest)

            for questLoopId in questInfo['unfinished_taskLoops']:
                if commQuest.isQuestLoopDisable(questLoopId):
                    continue
                questId = self.questLoopInfo[questLoopId].getCurrentQuest()
                failWords = QD.data[questId].get('failDialog', '')
                bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                fameAwardFactor = commQuest.getQuestLoopAwardFactorByType(self, questLoopId, gametypes.QUEST_REWARD_CREDIT)
                quest = {'id': questId,
                 'questLoopId': questLoopId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': 0,
                 'words': self._getDialog([failWords], questId),
                 'aside': [0],
                 'interval': [],
                 'speaker_ids': [npc.npcId],
                 'compFame': [ (fameId, int(fameVal * bonusFactor * fameAwardFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId),
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                self.checkLoopReward(questId, questLoopId, quest)
                res['unfinished_taskLoops'].append(quest)

            for questLoopId in questInfo['complete_taskLoops']:
                if commQuest.isQuestLoopDisable(questLoopId):
                    continue
                questId = self.questLoopInfo[questLoopId].getCurrentQuest()
                chatId = QD.data[questId].get('sucDialog', -1)
                if chatId == -1:
                    continue
                bonusFactor = self.getQuestData(questId, const.QD_BONUS_FACTOR, 1.0)
                fameAwardFactor = commQuest.getQuestLoopAwardFactorByType(self, questLoopId, gametypes.QUEST_REWARD_CREDIT)
                quest = {'id': questId,
                 'questLoopId': questLoopId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': chatId,
                 'words': self._getDialog(QDD.data[chatId]['chat'], questId),
                 'aside': QDD.data[chatId]['aside'],
                 'interval': QDD.data[chatId].get('interval', []),
                 'speaker_ids': self._getSpeakIds(chatId, npcId),
                 'speakEvents': QDD.data[chatId].get('speakEvent', None),
                 'compFame': [ (fameId, int(fameVal * bonusFactor * fameAwardFactor)) for fameId, fameVal in QD.data.get(questId, {}).get('compFame', []) ],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId),
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                if commQuest.completeQuestExtraCheck(self, questId):
                    quest['hasExtraReward'] = True
                    quest['extraRewardItems'] = commQuest.genQuestExtraRewardItems(self, questId)
                    quest['extraRewardChoice'] = commQuest.genQuestExtraRewardChoice(self, questId)
                self.checkLoopReward(questId, questLoopId, quest)
                res['complete_taskLoops'].append(quest)

            gamelog.debug('@szh: onShowQuestWindow res', res)
            if gameglobal.rds.configData.get('enableNpcV2', False) and not gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.npcV2.showQuest(res, npc)
            else:
                gameglobal.rds.ui.quest.openQuestWindow(res, npc)
            return

    def checkLoopReward(self, questId, questLoopId, questInfo):
        qd = QD.data.get(questId, {})
        qld = QLD.data.get(questLoopId, {})
        if qd.get('showLoopReward', 0):
            loopRewardDesc = qd.get('loopRewardDesc', '')
            loopRewardItems = qld.get('bonusItem', ())
            questInfo['loopRewardDesc'] = loopRewardDesc
            questInfo['loopRewardItems'] = loopRewardItems

    def _getSpeakIds(self, chatId, npcId = None):
        data = QDD.data.get(chatId, {})
        npcIds = list(data.get('npcId', []))
        ignoreNpc = data.get('ignoreNpc', 0)
        if ignoreNpc and npcId:
            for i, item in enumerate(npcIds):
                if item:
                    npcIds[i] = npcId

        return npcIds

    def _getDialog(self, content, questId = None):
        if isinstance(content, tuple) or isinstance(content, list):
            content = list(content)
        acName = None
        comName = None
        itemsName = None
        if questId:
            acNpc = commQuest.getAcNpc(self, questId)
            acName = uiUtils.getNpcName(acNpc)
            comNpc = commQuest.getQuestCompNpc(self, questId)
            comName = uiUtils.getNpcName(comNpc)
            qd = QD.data.get(questId, {})
            if commQuest.enableQuestMaterialBag(self, qd):
                compMaterialItemCollectAndConsume = qd.get('compMaterialItemCollectAndConsume', [])
                compItemCollect = []
                compItemCollectMulti = []
            else:
                compMaterialItemCollectAndConsume = []
                compItemCollect = qd.get('compItemCollect', [])
                compItemCollectMulti = qd.get('compItemCollectMulti', [])
            collectItems = []
            if compItemCollect:
                collectItems += compItemCollect
            if compMaterialItemCollectAndConsume:
                collectItems += compMaterialItemCollectAndConsume
            if compItemCollectMulti:
                collectItems += [ its[0] for its in compItemCollectMulti ]
            if collectItems:
                itemsName = [ '%sx%d' % (ID.data.get(itemId, {}).get('name', ''), num) for itemId, num in collectItems ]
                itemsName = ','.join(itemsName)
        if isinstance(content, str):
            content = self._getDialogContent(content, acName, comName, itemsName)
        elif isinstance(content, list):
            for i, item in enumerate(content):
                content[i] = self._getDialogContent(item, acName, comName, itemsName)

        return content

    def _getDialogContent(self, content, acName = None, comName = None, itemsName = None):
        content = content.replace('$p', self.schoolSwitchName)
        if acName:
            content = content.replace('$a', acName)
        if comName:
            content = content.replace('$c', comName)
        if itemsName:
            content = content.replace('$ic', itemsName)
        return content

    def showQuestWindowByItem(self, vpage, vpos):
        gamelog.debug('@szh showQuestWindowByItem', vpage, vpos)
        bag, page, pos = utils.getRealPos(self, vpage, vpos)
        item = bag.getQuickVal(page, pos)
        if item == const.CONT_NO_POS:
            return
        cid = CID.data.get(item.id, {})
        acQuest = cid.get('quest', 0)
        acQuestLoops = cid.get('questLoop', {})
        questInfo = commQuest.getQuestInfo(self, (acQuest,), (), acQuestLoops, {})
        questInfo = self._genBonusInfoInQuestInfo(questInfo)
        if questInfo['available_tasks'] or questInfo['available_taskLoops']:
            self.onShowQuestWindowByItem(questInfo, item.id, vpage, vpos)
        else:
            if acQuest:
                commQuest.gainQuestCheck(self, acQuest, bMsg=True)
            if acQuestLoops:
                for questLoopId in acQuestLoops.keys():
                    for questId in acQuestLoops[questLoopId]:
                        commQuest.gainQuestCheck(self, questId, bMsg=True)

    def onShowQuestWindowByItem(self, questInfo, itemId, vpage, vpos):
        res = {'available_tasks': [],
         'available_taskLoops': [],
         'unfinished_tasks': [],
         'complete_tasks': [],
         'chat': ''}
        if len(questInfo['available_tasks']) > 0:
            for questId, reward in questInfo['available_tasks']:
                quest = {'id': questId,
                 'questNpcId': itemId,
                 'name': QD.data[questId].get('name', ''),
                 'words': self._getDialog(QD.data[questId].get('acItemDesc', ''), questId),
                 'aside': [0],
                 'interval': [],
                 'speaker_ids': [],
                 'overTaken_tasks': QD.data[questId].get('acPreQst', ()),
                 'expBonus': reward[0],
                 'goldBonus': reward[1],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId),
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId)}
                res['available_tasks'].append(quest)

        hasZhuXie = False
        if len(questInfo['available_taskLoops']) > 0:
            for questLoopId, reward in questInfo['available_taskLoops']:
                if questLoopId in self.questLoopInfo:
                    questIds = self.questLoopInfo[questLoopId].getNextQuests(self)
                else:
                    questIds = commQuest.getAvaiNextQuestsInLoop(self, questLoopId, 0)
                if commQuest.isQuestLoopDisable(questLoopId):
                    continue
                if len(questIds) > 0:
                    questId = questIds[0]
                    chatId = QD.data[questId].get('acDialog', 0)
                    qld = QLD.data.get(questLoopId, {})
                    randType = qld.get('ranType', 1)
                    linshi = 0
                    if qld.get('bonusInfo', ((0, 0),))[0][0] == const.LOOP_QUEST_XIUWEI:
                        linshi = qld.get('bonusInfo', ())[0][1]
                    if qld.get('isZhuXie', 0):
                        hasZhuXie = True
                    quest = {'id': questId,
                     'questLoopId': questLoopId,
                     'questNpcId': itemId,
                     'name': QD.data[questId].get('name', ''),
                     'words': self._getDialog(QDD.data.get(chatId, {}).get('chat', ''), questId),
                     'aside': QDD.data.get(chatId, {}).get('aside', []),
                     'interval': QDD.data.get(chatId, {}).get('interval', []),
                     'speaker_ids': self._getSpeakIds(chatId, None),
                     'speakEvents': QDD.data.get(chatId, {}).get('speakEvent', None),
                     'overTaken_tasks': QD.data.get(chatId, {}).get('acPreQst', ()),
                     'expBonus': reward[0],
                     'goldBonus': reward[1],
                     'lingshi': linshi,
                     'rewardItems': commQuest.genQuestRewardItems(self, questId) if randType == 1 else qld.get('bonusItem', ()),
                     'rewardChoice': commQuest.genQuestRewardChoice(self, questId) if randType == 1 else (),
                     'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId) if randType == 1 else ()}
                    res['available_taskLoops'].append(quest)

        if hasZhuXie:
            gameglobal.rds.ui.itemQuestV2.show(uiConst.ITEM_QUEST_V2_TYPE_QUEST, res, vpage, vpos)
        else:
            gameglobal.rds.ui.itemQuest.show(res, itemId, vpage, vpos)

    def showItemIconNearMarker(self, entId, markerId, icon):
        npc = BigWorld.entities.get(entId)
        if not npc or not npc.inWorld or npc.beHide:
            return
        else:
            qmd = QMD.data[markerId]
            triggerType = qmd.get('triggerType', -1)
            gamelog.debug('hjx debug showItemIconNearMarker:', triggerType, icon)
            isItemMarker = False
            itemId = 0
            path = None
            if triggerType == const.PROP_TRIGGER:
                itemId = commQuest.getPropItemId(markerId)
                path = 'item/icon/%d.dds' % icon
                isItemMarker = True
            elif triggerType in (const.EMOTION_TRIGGER, const.BIGEMOTION_TRIGGER, const.HAND_CLIMB_TRIGGER):
                path = 'emote/%d.dds' % icon
            elif triggerType in (const.CLIMB_WING_WORLD_TOWER, const.CLIMB_DOWN_WING_WORLD_TOWER, const.SWITCH_WING_WORLD_GATE):
                pass
            else:
                gamelog.debug('hjx triggerType error:', triggerType)
                return
            gameglobal.rds.ui.npcSlot.path = path
            gameglobal.rds.ui.npcSlot.params = [markerId, isItemMarker, itemId]
            gameglobal.rds.ui.pressKeyF.addMarker(entId)
            return

    def hideItemIconNearMarker(self, entId, markerId):
        gameglobal.rds.ui.pressKeyF.removeMarker(entId)
        if gameglobal.rds.ui.dynamicFCastBar.markerId == markerId:
            gameglobal.rds.ui.dynamicFCastBar.hide()
        if not gameglobal.rds.ui.pressKeyF.isMarkerNpc:
            gameglobal.rds.ui.npcSlot.path = None
            gameglobal.rds.ui.npcSlot.params = None

    def fetchAcceptedQuestInfos(self):
        quests = [ x for x in self.quests ]
        questLoops = {}
        for questLoopId in self.questLoopInfo:
            questId = self.questLoopInfo[questLoopId].getCurrentQuest()
            if questId is not None:
                questLoops[questLoopId] = []

        questInfo = commQuest.getQuestInfo(self, [], quests, {}, questLoops)
        return questInfo

    def getAcceptedLoopIdByQuestId(self, questId):
        loopId = 0
        for questLoopId in self.questLoopInfo:
            qId = self.questLoopInfo[questLoopId].getCurrentQuest()
            if qId == questId:
                loopId = questId
                break

        return loopId

    def availabelTutorialCheck(self, qId):
        if QD.data.get(qId, {}).get('displayType', 0) not in (gametypes.QUEST_DISPLAY_TYPE_TUTORIAL_NEWTASK, gametypes.QUEST_DISPLAY_TYPE_SPCIAL):
            return False
        if utils.getEnableCheckServerConfig():
            serverConfigId = TQD.data.get(qId, {}).get('serverConfigId', 0)
            if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                return False
        return commQuest.gainQuestCheck(self, qId, False)

    def fetchAcQuestsList(self, questType):
        quests = []
        trackQuests = []
        if questType in gametypes.QUEST_LOOP_DISPLAY_TYPES:
            for questLoopId in self.questLoopInfo:
                if commQuest.getQuestLoopDisplayType(questLoopId) != questType:
                    continue
                qld = QLD.data.get(questLoopId)
                if not qld or commQuest.isQuestLoopDisable(questLoopId):
                    continue
                questId = self.questLoopInfo[questLoopId].getCurrentQuest()
                if questId is not None:
                    quests.append(questLoopId)
                    if self.getQuestData(questId, const.QD_QUEST_TRACKED):
                        trackQuests.append(questLoopId)
                elif QDID.data.get(questLoopId, 0) in self.delegations and self.getDelegationData(QDID.data.get(questLoopId, 0), const.DD_FAIL):
                    quests.append(questLoopId)

        else:
            for questId in self.quests:
                qd = QD.data.get(questId)
                if not qd or commQuest.isQuestDisable(questId):
                    continue
                if questType == gametypes.QUEST_DISPLAY_TYPE_SCHOOL_ONCE and qd['displayType'] in [gametypes.QUEST_DISPLAY_TYPE_SCHOOL_ONCE, gametypes.QUEST_DISPLAY_TYPE_SCHOOL_DAILY] or qd['displayType'] == questType:
                    quests.append(questId)
                    if self.getQuestData(questId, const.QD_QUEST_TRACKED):
                        trackQuests.append(questId)

        return (quests, trackQuests)

    def getLoopNpc(self, loopId):
        firstQuestId = None
        info = BigWorld.player().questLoopInfo.get(loopId, None)
        if info:
            quests = info.getNextQuests(BigWorld.player())
            if len(quests) > 0:
                firstQuestId = quests[0]
            else:
                firstQuestId = None
        else:
            qld = QLD.data.get(loopId)
            if len(qld['quests']) > 0:
                firstQuestId = qld['quests'][0]
                if isinstance(firstQuestId, tuple):
                    firstQuestId = firstQuestId[0]
        return firstQuestId

    def fetchQuestLoopDetail(self, questLoopId, fetchType = None):
        if fetchType == const.TYPE_FETCH_QUEST_DETAIL_ACTIVITYTIP:
            if questLoopId not in self.questLoopInfo or self.questLoopInfo[questLoopId].getCurrentQuest() is None:
                return
            else:
                return self.fetchQuestDetail(self.questLoopInfo[questLoopId].getCurrentQuest(), questLoopId, fetchType=const.TYPE_FETCH_QUEST_DETAIL_ACTIVITYTIP)
        elif gameglobal.rds.ui.questLog.isAvailable:
            gameglobal.rds.ui.questLog.setTaskDetail(self.genQuestLoopDetail(questLoopId))
        else:
            if questLoopId not in self.questLoopInfo or self.questLoopInfo[questLoopId].getCurrentQuest() is None:
                return
            self.fetchQuestDetail(self.questLoopInfo[questLoopId].getCurrentQuest(), questLoopId)

    def fetchQuestDetail(self, questId, loopId = -1, fetchType = None):
        if fetchType == const.TYPE_FETCH_QUEST_DETAIL_ACTIVITYTIP:
            questDetail = self.genQuestDetail(questId, loopId, False, False)
            return questDetail
        questDetail = self.genQuestDetail(questId, loopId, False, gameglobal.rds.ui.questLog.getAvailable(questId, loopId))
        gameglobal.rds.ui.questLog.setTaskDetail(questDetail)

    def genQuestLoopDetail(self, questLoopId):
        qld = QLD.data.get(questLoopId, {})
        loopQuests = qld.get('quests', [])
        needLoop = True
        if len(loopQuests) > 0:
            questLoopInfo = BigWorld.player().questLoopInfo.get(questLoopId, None)
            if questLoopInfo:
                if questLoopInfo.isLastStep():
                    groupNum = qld.get('groupNum', 0)
                    loopIndex = groupNum
                else:
                    loopIndex = questLoopInfo.getNextLoopIndex()
            if not questLoopInfo or loopIndex <= 0:
                questId = loopQuests[0]
            else:
                needLoop = False
                questId = loopQuests[loopIndex - 1]
            if isinstance(questId, tuple):
                questId = questId[0]
        else:
            questId = questLoopId
        qd = qld
        if not needLoop:
            qd = QD.data.get(questId, {})
        questDetail = {'id': questId,
         'loopId': questLoopId}
        questDetail['taskName'] = qd.get('name', gameStrings.TEXT_ITEMQUESTPROXY_87)
        if qld:
            questDetail['taskDesc'] = qd.get('desc', '')
            questDetail['loopInfo'] = self._genLoopInfo(questLoopId)
        else:
            questDetail['taskDesc'] = gameStrings.TEXT_ITEMQUESTPROXY_99
        questDetail['taskAward'] = {}
        questDetail['taskAward']['icon'] = qld.get('bonusItem', [])
        questDetail['extraItems'] = QED.data.get(questLoopId, {}).get('rewardItems', [])
        questDetail['taskAward']['money'] = 0
        questDetail['taskAward']['exp'] = 0
        questDetail['taskAward']['extraMoney'] = 0
        questDetail['taskAward']['extraExp'] = 0
        questDetail['taskAward']['fame'] = {}
        bonusInfo = qld.get('bonusInfo', [])
        for item in bonusInfo:
            if item[0] == const.LOOP_QUEST_MONEY:
                questDetail['taskAward']['money'] = item[1]
            elif item[0] == const.LOOP_QUEST_EXP:
                questDetail['taskAward']['exp'] = item[1]
            elif item[0] == const.LOOP_QUEST_FAME and len(item) > 2:
                questDetail['taskAward']['fame'][item[1]] = item[2]
            elif item[0] == const.LOOP_QUEST_RENPIN:
                questDetail['taskAward']['renpin'] = item[1]

        cashRewardType = gametypes.QUEST_CASHREWARD_BIND
        firstQuestId = self.getLoopNpc(questLoopId)
        if firstQuestId:
            qd = QD.data.get(firstQuestId, {})
            acNpc = commQuest.getAcNpc(self, firstQuestId)
            if type(acNpc) in (tuple, list):
                for npcId in acNpc:
                    deliveryNpc = ND.data.get(npcId, None)
                    if deliveryNpc:
                        break

            else:
                deliveryNpc = ND.data.get(acNpc, None)
            if deliveryNpc != None:
                questDetail['taskDeliveryNPC'] = uiUtils.getNpcName(acNpc)
                questDetail['taskDeliveryNPCTk'] = str(uiUtils.getNpcTrackId(firstQuestId, acNpc, 'acNpc'))
                questDetail['taskDeliveryNPCTkType'] = self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_AC)
            else:
                questDetail['taskDeliveryNPC'] = ''
                questDetail['taskDeliveryNPCTk'] = 0
                questDetail['taskDeliveryNPCTkType'] = 0
            questDetail['taskPlace'] = qd.get('region', '')
            rewardMode = qd.get('reward')
            if rewardMode:
                cashRewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
        questDetail['taskAward']['cashRewardType'] = cashRewardType
        loopReward = qld.get('loopReward', {})
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId, None)
        if info:
            curLoop = info.loopCnt
        else:
            curLoop = 0
        moneyUp = loopReward.get(const.LOOP_QUEST_MONEY, [])
        if curLoop < len(moneyUp):
            isMoneyUp = True if moneyUp[curLoop] == 2 else False
        else:
            isMoneyUp = False
        questDetail['moneyUp'] = isMoneyUp
        expUp = loopReward.get(const.LOOP_QUEST_EXP, [])
        if curLoop < len(expUp):
            isExpUp = True if expUp[curLoop] == 2 else False
        else:
            isExpUp = False
        questDetail['expUp'] = isExpUp
        return questDetail

    def genQuestDetail(self, questId, loopId, isShare = False, isAvailable = False):
        questDetail = {'id': questId,
         'loopId': loopId}
        qd = QD.data.get(questId, {})
        if qd:
            questDetail['taskPlace'] = qd.get('region', '')
            questDetail['taskName'] = qd.get('name', gameStrings.TEXT_IMPQUEST_1069)
            questDetail['taskDesc'] = qd.get('desc', '')
            questDetail['taskShortDesc'] = qd.get('shortDesc', '')
        else:
            questDetail['taskPlace'] = ''
            questDetail['taskName'] = gameStrings.TEXT_ITEMQUESTPROXY_87
            questDetail['taskDesc'] = gameStrings.TEXT_ITEMQUESTPROXY_99
            questDetail['taskShortDesc'] = gameStrings.TEXT_ITEMQUESTPROXY_99
        if loopId != -1:
            qld = QLD.data.get(loopId, {})
            if qld:
                questDetail['loopInfo'] = self._genLoopInfo(loopId)
            else:
                questDetail['taskPlace'] = ''
                questDetail['taskName'] = gameStrings.TEXT_ITEMQUESTPROXY_87
                questDetail['taskDesc'] = gameStrings.TEXT_ITEMQUESTPROXY_99
                questDetail['taskShortDesc'] = gameStrings.TEXT_ITEMQUESTPROXY_99
            loopReward = qld.get('loopReward', {})
            p = BigWorld.player()
            info = p.questLoopInfo.get(loopId, None)
            if info:
                curLoop = info.loopCnt
            else:
                curLoop = 0
            moneyUp = loopReward.get(const.LOOP_QUEST_MONEY, [])
            if curLoop < len(moneyUp):
                isMoneyUp = True if moneyUp[curLoop] == 2 else False
            else:
                isMoneyUp = False
            questDetail['moneyUp'] = isMoneyUp
            expUp = loopReward.get(const.LOOP_QUEST_EXP, [])
            if curLoop < len(expUp):
                isExpUp = True if expUp[curLoop] == 2 else False
            else:
                isExpUp = False
            questDetail['expUp'] = isExpUp
        questDetail['taskAward'] = {}
        questDetail['taskAward']['icon'] = commQuest.genQuestRewardItems(self, questId)
        questDetail['rewardChoice'] = commQuest.genQuestRewardChoice(self, questId)
        questDetail['groupHeaderItems'] = commQuest.genGroupHeaderRewardItems(self, questId)
        questDetail['extraItems'] = commQuest.genQuestExtraRewardItems(self, questId)
        current = BigWorld.player().getServerTime()
        if not isShare and not isAvailable:
            if not isShare and questId not in self.quests:
                return questDetail
            questDetail['taskAward']['money'] = self.getQuestData(questId, const.QD_QUEST_CASH)
            questDetail['taskAward']['exp'] = self.getQuestData(questId, const.QD_QUEST_EXP)
            questDetail['taskAward']['xiuwei'] = self.getQuestData(questId, const.LOOP_QUEST_XIUWEI)
            if qd.has_key('questGroup'):
                questGroupId = qd['questGroup']
                if QGD.data.has_key(questGroupId):
                    qgd = QGD.data[questGroupId]
                    lastQuestId = qgd['quests'][-1]
                    questDetail['taskAward']['exp'], questDetail['taskAward']['money'], socExp, _ = commQuest.calcReward(self, lastQuestId)
                    questDetail['taskDesc'] = qgd.get('desc', '')
                    questDetail['taskShortDesc'] = questDetail['taskDesc']
            questDetail['taskAward']['extraMoney'] = self.getQuestData(questId, const.QD_EXTRA_QUEST_CASH)
            questDetail['taskAward']['extraExp'] = self.getQuestData(questId, const.QD_EXTRA_QUEST_EXP)
            firstQuestId = None
            if self._isQuestFailed(questId):
                if qd.has_key('questGroup') and not commQuest.isQuestGroupMatch(self, qd['questGroup']):
                    questGroupId = qd['questGroup']
                    if QGD.data.has_key(questGroupId):
                        qgd = QGD.data[questGroupId]
                        firstQuestId = qgd['quests'][0]
                        qd = QD.data.get(firstQuestId)
                if firstQuestId is not None:
                    compNpc = commQuest.getAcNpc(self, firstQuestId)
                else:
                    compNpc = commQuest.getAcNpc(self, questId)
            else:
                compNpc = commQuest.getQuestCompNpc(self, questId)
            if type(compNpc) in (tuple, list):
                for npcId in compNpc:
                    deliveryNpc = ND.data.get(npcId, None)
                    if deliveryNpc:
                        break

            else:
                deliveryNpc = ND.data.get(compNpc, None)
            if deliveryNpc != None:
                if self._isQuestFailed(questId) and firstQuestId is not None:
                    questDetail['taskDeliveryNPC'] = uiUtils.getNpcName(compNpc)
                    questDetail['taskDeliveryNPCTk'] = str(uiUtils.getNpcTrackId(firstQuestId, compNpc, 'acNpc'))
                    questDetail['taskDeliveryNPCTkType'] = self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_AC)
                else:
                    questDetail['taskDeliveryNPC'] = uiUtils.getNpcName(compNpc)
                    questDetail['taskDeliveryNPCTk'] = str(uiUtils.getNpcTrackId(questId, compNpc, 'comNpc'))
                    questDetail['taskDeliveryNPCTkType'] = self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_COM)
            else:
                questDetail['taskDeliveryNPC'] = ''
                questDetail['taskDeliveryNPCTk'] = 0
                questDetail['taskDeliveryNPCTkType'] = 0
            if qd.has_key('timeLimit') and not self.getQuestData(questId, const.QD_FAIL):
                limit = qd['timeLimit']
                timeout = self.getQuestData(questId, const.QD_BEGIN_TIME) + limit - current
                questDetail['timeOut'] = timeout
            else:
                questDetail['timeOut'] = -1
            questDetail['taskGoal'] = self._genQuestGoal(questId, True)
            if QED.data.get(questId, {}).get('hideExtra', 0):
                if commQuest.completeQuestExtraCheck(self, questId):
                    questDetail['taskGoal'] += self._genQuestExtraGoal(questId, True)
            else:
                questDetail['taskGoal'] += self._genQuestExtraGoal(questId, True)
        else:
            expBonus, moneyBonus = gameglobal.rds.ui.questLog.getTaskBonus(questId)
            questDetail['taskAward']['money'] = moneyBonus
            questDetail['taskAward']['exp'] = expBonus
            acNpc = commQuest.getAcNpc(self, questId)
            if type(acNpc) in (tuple, list):
                for npcId in acNpc:
                    deliveryNpc = ND.data.get(npcId, None)
                    if deliveryNpc:
                        break

            else:
                deliveryNpc = ND.data.get(acNpc, None)
            if deliveryNpc != None:
                questDetail['taskDeliveryNPC'] = uiUtils.getNpcName(acNpc)
                questDetail['taskDeliveryNPCTk'] = str(uiUtils.getNpcTrackId(questId, acNpc, 'acNpc'))
                questDetail['taskDeliveryNPCTkType'] = self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_AC)
            else:
                questDetail['taskDeliveryNPC'] = ''
                questDetail['taskDeliveryNPCTk'] = 0
                questDetail['taskDeliveryNPCTkType'] = 0
            questDetail['taskGoal'] = []
            questDetail['timeOut'] = -1
        cashRewardType = gametypes.QUEST_CASHREWARD_BIND
        rewardMode = QD.data.get(questId, {}).get('reward')
        if rewardMode:
            cashRewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
        questDetail['taskAward']['cashRewardType'] = cashRewardType
        return questDetail

    def genTrackedQuestInfo(self, questId):
        quest = []
        qd = QD.data.get(questId, {})
        loopId = self.getQuestLoopId(questId)
        if not self.isQuestTracked(questId):
            return quest
        elif not qd or qd.get('hideInLog', 0):
            return quest
        else:
            quest.append(qd['type'])
            stateType = 1 if commQuest.completeQuestCheck(self, questId) else 0
            self._addTimerLimitQuestTrack(quest, questId, stateType, loopId)
            quest.append(qd['name'])
            questGoal = self._genQuestGoal(questId)
            if QED.data.get(questId, {}).get('hideExtra', 0):
                if commQuest.completeQuestExtraCheck(self, questId):
                    questGoal += self._genQuestExtraGoal(questId)
            else:
                questGoal += self._genQuestExtraGoal(questId)
            if self._isQuestFinished(questId, questGoal) or self._isQuestFailed(questId):
                questGoal = []
                compNpcGoal = self._genComNpcGoal(questId)
                questGoal.append(compNpcGoal)
            if questGoal == None:
                questGoal = []
            quest.append(questGoal)
            quest.append(questId)
            return quest

    def onFetchQuestTrackInfo(self, questInfo):
        results = []
        for questId in questInfo['unfinished_tasks']:
            quest = self.genTrackedQuestInfo(questId)
            if not quest:
                continue
            results.append(quest)

        for questId in questInfo['complete_tasks']:
            quest = self.genTrackedQuestInfo(questId)
            if not quest:
                continue
            results.append(quest)
            gameglobal.rds.tutorial.onCompleteQuestCondition(questId)
            gameglobal.rds.tutorial.onCompletedQuest(questId)

        gameglobal.rds.ui.questTrack.onAllTrackedQuestFetched(results)

    def _addTimerLimitQuestTrack(self, quests, questId, questType, loopId):
        timeLeft = commQuest.questTimeLeft(self, questId)
        delId = QDID.data.get(loopId, 0)
        qd = QD.data[questId]
        if qd.has_key('timeLimit'):
            if timeLeft > 0:
                quests.append(questType)
                quests.append([const.QD_BEGIN_TIME, timeLeft])
            else:
                quests.append(2)
                quests.append([const.QD_BEGIN_TIME, 0])
        elif qd.has_key('timeRemain'):
            quests.append(questType)
            quests.append([const.QD_TIME_REMAIN, timeLeft])
        elif self.hasDelegationData(delId, const.DD_TIME_LIMIT):
            leftTime = self.getDelegationData(delId, const.DD_BEGIN_TIME) + self.getDelegationData(delId, const.DD_TIME_LIMIT) - BigWorld.player().getServerTime()
            if leftTime > 0:
                quests.append(questType)
                quests.append([const.QD_TIME_REMAIN, leftTime])
            else:
                quests.append(questType)
                quests.append([-1, -1])
        else:
            if self._isQuestFailed(questId):
                quests.append(3)
            else:
                quests.append(questType)
            quests.append([-1, -1])

    def _isQuestFinished(self, questId, questGoal):
        if questGoal == None:
            return False
        else:
            qd = QD.data.get(questId, {})
            if qd.has_key('timeRemain'):
                duration = qd['timeRemain']
                current = self.getServerTime()
                timeBegin = self.getQuestData(questId, const.QD_TIME_REMAIN, current)
                if timeBegin + duration > current:
                    return False
            orRelation = qd.get('condRelation', 0)
            if orRelation:
                for goal in questGoal:
                    if goal[1] == True:
                        return True

                return False
            for goal in questGoal:
                if goal[1] == False:
                    return False

            return True

    def _isQuestFailed(self, questId):
        return self.getQuestData(questId, const.QD_FAIL, False)

    def _genQuestExtraGoal(self, questId, isQuestLog = False):
        qed = QED.data.get(questId, {})
        qd = QD.data.get(questId, {})
        if self.getQuestData(questId, const.QD_EXTRA_FAIL, False):
            return []
        if qd.get('shareExtraBonusRate'):
            if not self.getQuestData(questId, const.QD_EXTRA_BONUS_NUID, 0) or self.getQuestData(questId, const.QD_EXTRA_BONUS_NUID) != self.gbId:
                return []
        questGoals = []
        if qed.has_key('compItemCollect'):
            for i, (itemId, cnt) in enumerate(qed['compItemCollect']):
                done = False
                curCnt = self.questCountItem(questId, itemId)
                if curCnt >= cnt:
                    done = True
                    curCnt = cnt
                name = ID.data[itemId]['name']
                if qed.has_key('comCltItemTk'):
                    isTrack = True
                    trackId = qed['comCltItemTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1386 % (name, curCnt, cnt),
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                 const.QUEST_GOAL_TYPE: False,
                 const.QUEST_GOAL_ORDER: 'compItemCollect'})

        elif qed.has_key('compItemCollectMulti'):
            for i, collItems in enumerate(qed['compItemCollectMulti']):
                count = 0
                totalNeed = 0
                for itemId, cnt in collItems:
                    count += self.questCountItem(questId, itemId)
                    totalNeed = cnt
                    name = ID.data[itemId]['name']
                    if count >= totalNeed:
                        count = totalNeed
                        break

                if qed.has_key('comCltItemTk'):
                    isTrack = True
                    trackId = qed['comCltItemTk'][i] if i < len(qed['comCltItemTk']) else 0
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1386 % (name, count, totalNeed),
                 const.QUEST_GOAL_STATE: count == totalNeed,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                 const.QUEST_GOAL_TYPE: False,
                 const.QUEST_GOAL_ORDER: 'compItemCollectMulti'})

        if qed.has_key('needMonsters'):
            monsterInfo = self.getQuestData(questId, const.QD_EXTRA_MONSTER_KILL, {})
            for i, (mType, cnt) in enumerate(qed['needMonsters']):
                if cnt == monsterInfo.get(mType, 0):
                    done = True
                else:
                    done = False
                name = MD.data[mType]['name']
                if qed.has_key('needMonsterTk'):
                    isTrack = True
                    trackId = qed['needMonsterTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1435 % (name, monsterInfo.get(mType, 0), cnt),
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_NEED_MONSTER),
                 const.QUEST_GOAL_TYPE: False,
                 const.QUEST_GOAL_ORDER: 'needMonsters'})

        if qed.has_key('beatMonsterNo'):
            qmb = self.getQuestData(questId, const.QD_EXTRA_MONSTER_BEAT)
            mNo = qed['beatMonsterNo']
            if qmb['beatMonsterNo'] == mNo and qmb['done']:
                done = True
            else:
                done = False
            name = MD.data[mNo]['name']
            if qed.has_key('beatMonsterTk'):
                isTrack = True
                trackId = qed['beatMonsterTk']
            else:
                isTrack = False
                trackId = 0
            questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1459 % name,
             const.QUEST_GOAL_STATE: done,
             const.QUEST_GOAL_TRACK: isTrack,
             const.QUEST_GOAL_TRACK_ID: trackId,
             const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_BEAT_MONSTER),
             const.QUEST_GOAL_TYPE: False,
             const.QUEST_GOAL_ORDER: 'beatMonsterNo'})
        if qed.has_key('pvpKill'):
            pvpKillInfo = self.getQuestData(questId, const.QD_EXTRA_PVP_KILL, {})
            for camp, cnt in qed['pvpKill'].iteritems():
                if cnt == pvpKillInfo.get(camp, 0):
                    done = True
                else:
                    done = False
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1475 % (pvpKillInfo.get(camp, 0), cnt),
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: False})

        if qed.has_key('questVars'):
            for i, (var, cnt) in enumerate(qed['questVars']):
                if cnt <= self.questVars.get(var, 0):
                    done = True
                    canGuildHelp = 0
                else:
                    done = False
                    canGuildHelp = qd.get('canGuildHelp', 0) if gameglobal.rds.configData.get('enableGuildQuestOptimize', False) else 0
                if qed.has_key('questVarsTk'):
                    isTrack = True
                    trackId = qed['questVarsTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                desc = qed.get('questVarsDesc', '').split(',')
                if i >= len(desc):
                    desc = gameStrings.TEXT_IMPQUEST_1500
                else:
                    desc = desc[i] if desc[i] else gameStrings.TEXT_IMPQUEST_1500
                try:
                    if desc.find('%s') != -1:
                        desc = desc % (self.questVars.get(var, 0), cnt)
                    else:
                        desc = desc % (self.questVars.get(var, 0), cnt)
                except:
                    pass

                questGoals.append({const.QUEST_GOAL_DESC: desc,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_VAR),
                 const.QUEST_GOAL_TYPE: True,
                 const.QUEST_GOAL_ORDER: 'questVars',
                 const.QUEST_GOAL_GUILD_HELP: canGuildHelp})

        questGoals = self.sortQuestGoal(questGoals, questId, isQuestLog)
        return questGoals

    def _filterCommitTrackType(self, qd, trackType):
        if not qd.get('teleportCommit', 0):
            return 0
        else:
            return trackType

    def _filterTargetTrackType(self, qd, trackType):
        if not qd.get('teleportTarget', 0):
            return 0
        else:
            return trackType

    def getSeekerInfo(self):
        seekerInfo = {}
        for questId in self.quests:
            questGoals = self._genQuestGoal(questId)
            if QED.data.get(questId, {}).get('hideExtra', 0):
                if commQuest.completeQuestExtraCheck(self, questId):
                    questGoals.extend(self._genQuestExtraGoal(questId))
            else:
                questGoals.extend(self._genQuestExtraGoal(questId))
            for questGoal in questGoals:
                if not questGoal.has_key(const.QUEST_GOAL_TRACK_ID):
                    continue
                seekerId = questGoal[const.QUEST_GOAL_TRACK_ID]
                if seekerInfo.get(seekerId, False) == False:
                    seekerInfo[seekerId] = questGoal[const.QUEST_GOAL_STATE]

        return seekerInfo

    def isItemClickSearch(self, questId, itemId):
        qd = QD.data.get(questId, {})
        isItemClickSearch = 0
        if qd.has_key('isItemClickSearch'):
            for i, (itemIdSearch, isSearch) in enumerate(qd.get('isItemClickSearch')):
                if itemId == itemIdSearch:
                    isItemClickSearch = isSearch

        return isItemClickSearch

    def _genQuestGoal(self, questId, isQuestLog = False):
        qd = QD.data.get(questId, {})
        if self.getQuestData(questId, const.QD_FAIL, False):
            return []
        else:
            questGoals = []
            if not commQuest.enableQuestMaterialBag(self, qd):
                if qd.has_key('compItemCollect'):
                    compCondType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
                    if compCondType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY, const.QUEST_COMPCOND_EXACT):
                        for i, (itemId, cnt) in enumerate(qd['compItemCollect']):
                            curCnt = self.questCountItem(questId, itemId)
                            if compCondType == const.QUEST_COMPCOND_DISTINCT:
                                goalState = curCnt >= cnt
                            else:
                                goalState = commQuest.isQuestItemCollectComplete(self, questId)
                            if curCnt >= cnt and compCondType != const.QUEST_COMPCOND_EXACT:
                                curCnt = cnt
                            name = ID.data[itemId]['name']
                            if qd.has_key('comCltItemTk'):
                                isTrack = True
                                trackId = qd['comCltItemTk'][i]
                            else:
                                isTrack = False
                                trackId = 0
                            desc = qd.get('itemCollectDesc', '').split(',')
                            showDiffDesc = qd.get('showDiffDesc', 0)
                            if not showDiffDesc and compCondType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_EXACT):
                                desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_1386
                            else:
                                desc = desc[i] if i < len(desc) and desc[i] else gameStrings.TEXT_IMPQUEST_1386
                            try:
                                if desc.find('%s') != -1:
                                    desc = desc % (name, curCnt, cnt)
                                else:
                                    desc = desc % (curCnt, cnt)
                            except:
                                pass

                            if compCondType == const.QUEST_COMPCOND_ANY and i != 0:
                                continue
                            questGoals.append({const.QUEST_GOAL_DESC: desc,
                             const.QUEST_GOAL_STATE: goalState,
                             const.QUEST_GOAL_TRACK: isTrack,
                             const.QUEST_GOAL_TRACK_ID: trackId,
                             const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                             const.QUEST_GOAL_TYPE: True,
                             const.QUEST_GOAL_ORDER: 'compItemCollect',
                             const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, itemId),
                             const.QUEST_GOAL_ITEM_ID: itemId})

                    elif compCondType == const.QUEST_COMPCOND_ALL:
                        totalNeed = 0
                        count = 0
                        desc = qd.get('itemCollectDesc', '')
                        for i, (itemId, cnt) in enumerate(qd['compItemCollect']):
                            name = ID.data[itemId]['name']
                            if qd.has_key('comCltItemTk'):
                                isTrack = True
                                trackId = qd['comCltItemTk'][0]
                            else:
                                isTrack = False
                                trackId = 0
                            totalNeed = cnt
                            count += self.questCountItem(questId, itemId)

                        if count > totalNeed:
                            count = totalNeed
                        desc = desc % (count, totalNeed)
                        questGoals.append({const.QUEST_GOAL_DESC: desc,
                         const.QUEST_GOAL_STATE: commQuest.isQuestItemCollectComplete(self, questId),
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'compItemCollect',
                         const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, itemId),
                         const.QUEST_GOAL_ITEM_ID: itemId})
                elif qd.has_key('yaoJingQitanCompItemMulti') and gameglobal.rds.configData.get('enableYaojingqitanCustomCost', False):
                    desc = qd.get('itemCollectDesc', '').split(',')
                    for i, collItems in enumerate(qd['yaoJingQitanCompItemMulti']):
                        count = 0
                        totalNeed = 0
                        firstItemId = collItems[0]
                        name = ID.data.get(firstItemId, {}).get('name', '')
                        p = BigWorld.player()
                        for itemId in collItems:
                            count += self.questCountItem(questId, itemId)
                            costList = SCD.data.get('yaojingqitanCost', {})
                            costType = getattr(p, 'yaojingqitanCostType', 1)
                            costInfo = costList.get(costType, None)
                            if costInfo:
                                totalNeed = costInfo[0]
                            else:
                                totalNeed = 0
                            if count >= totalNeed:
                                count = totalNeed
                                break

                        if qd.has_key('comCltItemTk'):
                            isTrack = True
                            trackId = qd['comCltItemTk'][i] if i < len(qd['comCltItemTk']) else 0
                        else:
                            isTrack = False
                            trackId = 0
                        tmpDesc = desc[i] if i < len(desc) and desc[i] else gameStrings.TEXT_IMPQUEST_1386
                        try:
                            if tmpDesc.find('%s') != -1:
                                tmpDesc = tmpDesc % (name, count, totalNeed)
                            else:
                                tmpDesc = tmpDesc % (count, totalNeed)
                        except:
                            pass

                        questGoals.append({const.QUEST_GOAL_DESC: tmpDesc,
                         const.QUEST_GOAL_STATE: count >= totalNeed,
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'compItemCollectMulti',
                         const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, firstItemId),
                         const.QUEST_GOAL_ITEM_ID: firstItemId})

                elif qd.has_key('compItemCollectMulti'):
                    desc = qd.get('itemCollectDesc', '').split(',')
                    for i, collItems in enumerate(qd['compItemCollectMulti']):
                        count = 0
                        totalNeed = 0
                        firstItemId = collItems[0][0]
                        name = ID.data.get(firstItemId, {}).get('name', '')
                        for itemId, cnt in collItems:
                            count += self.questCountItem(questId, itemId)
                            totalNeed = cnt
                            if count >= totalNeed:
                                count = totalNeed
                                break

                        if qd.has_key('comCltItemTk'):
                            isTrack = True
                            trackId = qd['comCltItemTk'][i] if i < len(qd['comCltItemTk']) else 0
                        else:
                            isTrack = False
                            trackId = 0
                        tmpDesc = desc[i] if i < len(desc) and desc[i] else gameStrings.TEXT_IMPQUEST_1386
                        try:
                            if tmpDesc.find('%s') != -1:
                                tmpDesc = tmpDesc % (name, count, totalNeed)
                            else:
                                tmpDesc = tmpDesc % (count, totalNeed)
                        except:
                            pass

                        questGoals.append({const.QUEST_GOAL_DESC: tmpDesc,
                         const.QUEST_GOAL_STATE: commQuest.isQuestItemCollectCompleteMulti(self, questId),
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'compItemCollectMulti',
                         const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, firstItemId),
                         const.QUEST_GOAL_ITEM_ID: firstItemId})

            else:
                for i, (itemId, cnt) in enumerate(qd['compMaterialItemCollectAndConsume']):
                    curCnt = self.questCountMaterialItem(itemId)
                    if curCnt >= cnt:
                        curCnt = cnt
                    name = ID.data[itemId]['name']
                    if qd.has_key('comCltItemTk'):
                        isTrack = True
                        trackId = qd['comCltItemTk'][i]
                    else:
                        isTrack = False
                        trackId = 0
                    desc = qd.get('itemCollectDesc', '').split(',')
                    showDiffDesc = qd.get('showDiffDesc', 0)
                    if not showDiffDesc:
                        desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_1386
                    else:
                        desc = desc[i] if i < len(desc) and desc[i] else gameStrings.TEXT_IMPQUEST_1386
                    try:
                        if desc.find('%s') != -1:
                            desc = desc % (name, curCnt, cnt)
                        else:
                            desc = desc % (curCnt, cnt)
                    except:
                        pass

                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: curCnt >= cnt,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_CTRL_ITEM),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'compMaterialItemCollectAndConsume',
                     const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, itemId),
                     const.QUEST_GOAL_ITEM_ID: itemId})

            if qd.has_key('comSmtItem'):
                for itemId, cnt in qd['comSmtItem']:
                    curCnt = self.questCountItem(questId, itemId)
                    if curCnt >= cnt:
                        curCnt = cnt
                    name = ID.data[itemId]['name']
                    questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1783 % (name, curCnt, cnt),
                     const.QUEST_GOAL_STATE: commQuest.isQuestItemSubmitComplete(self, questId),
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('randomItemCommit'):
                rIndex = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT)
                itemId, cnt = qd['randomItemCommit'][rIndex]
                curCnt = self.questCountItem(questId, itemId)
                if curCnt >= cnt:
                    curCnt = cnt
                name = ID.data[itemId]['name']
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1783 % (name, curCnt, cnt),
                 const.QUEST_GOAL_STATE: curCnt >= cnt,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('randomItemCommitEx'):
                items = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_EX)
                enableQuestMaterialBag = gameglobal.rds.configData.get('enableQuestMaterialBag', False)
                for itemId, cnt in items:
                    if enableQuestMaterialBag:
                        curCnt = self.questCountMaterialItem(itemId)
                    else:
                        curCnt = self.questCountItem(questId, itemId, enableParentCheck=True)
                    if curCnt >= cnt:
                        curCnt = cnt
                    if qd.has_key('randomItemCommitExTk'):
                        isTrack = True
                        trackId = qd['randomItemCommitExTk'][itemId]
                    else:
                        isTrack = False
                        trackId = 0
                    desc = qd.get('randomItemCommitExMsg', {}).get(itemId, '')
                    if desc != '':
                        desc = desc % (curCnt, cnt)
                    else:
                        itemName = ID.data.get(itemId, {}).get('name', '')
                        desc = gameStrings.TEXT_IMPQUEST_1827 % (itemName, curCnt, cnt)
                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: curCnt >= cnt,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'randomItemCommitEx',
                     const.QUEST_GOAL_CLICK_FUNC_TYPE: self.isItemClickSearch(questId, itemId),
                     const.QUEST_GOAL_ITEM_ID: itemId})

            if qd.has_key('randomItemCommitMulti'):
                items = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_MULTI)
                for itemListId, cnt in items:
                    qigdData = QIGD.data.get(itemListId, {})
                    curCnt = sum((self.questCountItem(questId, itemId, enableParentCheck=True) for itemId in qigdData.get('itemList', [])))
                    if curCnt >= cnt:
                        curCnt = cnt
                    if qigdData.has_key('itemTk'):
                        isTrack = True
                        trackId = qigdData.get('itemTk')
                    else:
                        isTrack = False
                        trackId = 0
                    questGoals.append({const.QUEST_GOAL_DESC: qigdData.get('itemMsg', '%d/%d') % (curCnt, cnt),
                     const.QUEST_GOAL_STATE: curCnt >= cnt,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('needMonsters'):
                monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
                needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
                if needMonstersType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY):
                    for i, (mType, cnt) in enumerate(qd['needMonsters']):
                        if needMonstersType == const.QUEST_COMPCOND_ANY and i != 0:
                            continue
                        name = MD.data[mType]['name']
                        if qd.has_key('needMonsterTk'):
                            isTrack = True
                            trackId = qd['needMonsterTk'][i]
                        else:
                            isTrack = False
                            trackId = 0
                        desc = qd.get('needMonsterDesc', '').split(',')
                        if i >= len(desc):
                            desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_1435
                        else:
                            desc = desc[i] if i < len(desc) and desc[i] else gameStrings.TEXT_IMPQUEST_1435
                        try:
                            if needMonstersType == const.QUEST_COMPCOND_ANY:
                                killNum = commQuest.getQuestMonsterKillNumCompAny(self, questId)
                            else:
                                killNum = monsterInfo.get(mType, 0)
                            if desc.find('%s') != -1:
                                desc = desc % (name, killNum, cnt)
                            else:
                                desc = desc % (killNum, cnt)
                        except:
                            pass

                        questGoals.append({const.QUEST_GOAL_DESC: desc,
                         const.QUEST_GOAL_STATE: commQuest.isQuestMonsterKillComplete(self, questId),
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_NEED_MONSTER),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'needMonsters'})

                elif needMonstersType == const.QUEST_COMPCOND_ALL:
                    totalNeed = 0
                    count = 0
                    desc = qd.get('needMonsterDesc', '')
                    for i, (mType, cnt) in enumerate(qd['needMonsters']):
                        name = MD.data[mType]['name']
                        if qd.has_key('needMonsterTk'):
                            isTrack = True
                            trackId = qd['needMonsterTk'][0]
                        else:
                            isTrack = False
                            trackId = 0
                        totalNeed = cnt
                        count += monsterInfo.get(mType, 0)

                    if count > totalNeed:
                        count = totalNeed
                    desc = desc % (count, totalNeed)
                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: commQuest.isQuestMonsterKillComplete(self, questId),
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_NEED_MONSTER),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'needMonsters'})
            if qd.has_key('needMonstersGroup'):
                self._genMonsterGroupGoal(questId, qd, questGoals)
            if qd.has_key('questInteractive'):
                interactiveInfo = self.getQuestData(questId, const.QD_QUEST_INTERACTIVE, {})
                descs = qd.get('interactiveMsg', [])
                for i, (interactiveId, cnt) in enumerate(qd['questInteractive']):
                    finishedNum = cnt - interactiveInfo.get(interactiveId, 0)
                    descCount = gameStrings.TEXT_IMPQUEST_1939 % (finishedNum, cnt)
                    if i < len(descs):
                        desc = qd.get('interactiveMsg')[i]
                        desc += descCount
                    else:
                        desc = gameStrings.DESC_QUEST_INTERACTIVE
                        desc += '%s%s' % (ITD.data.get(interactiveId, {}).get('name', ''), descCount)
                    if qd.has_key('interactiveTk'):
                        isTrack = True
                        trackId = qd['interactiveTk'][i]
                    else:
                        isTrack = False
                        trackId = 0
                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: finishedNum == cnt,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_INTERACTIVE),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'questInteractive'})

            if qd.has_key('fishingScore'):
                score = self.getQuestData(questId, const.QD_FISHING_SCORE, -1)
                if score >= qd['fishingScore']:
                    done = True
                else:
                    done = False
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1970 % (score, qd['fishingScore']),
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: True,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TRACK_TYPE: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('beatMonsterNo'):
                qmb = self.getQuestData(questId, const.QD_MONSTER_BEAT)
                mNo = qd['beatMonsterNo']
                if qmb['beatMonsterNo'] == mNo and qmb['done']:
                    done = True
                else:
                    done = False
                name = MD.data[mNo]['name']
                if qd.has_key('beatMonsterTk'):
                    isTrack = True
                    trackId = qd['beatMonsterTk']
                else:
                    isTrack = False
                    trackId = 0
                desc = qd.get('beatMonsterDesc', '').split(',')
                desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_1459
                try:
                    desc = desc % name
                except:
                    pass

                questGoals.append({const.QUEST_GOAL_DESC: desc,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_BEAT_MONSTER),
                 const.QUEST_GOAL_TYPE: True,
                 const.QUEST_GOAL_ORDER: 'beatMonsterNo'})
            if qd.has_key('comBuff'):
                stateId = qd['comBuff']
                if stateId in self.statesServerAndOwn:
                    done = True
                    cnt = 1
                else:
                    done = False
                    cnt = 0
                if qd.has_key('comBuffTk'):
                    isTrack = True
                    trackId = qd['comBuffTk']
                else:
                    isTrack = False
                    trackId = 0
                if qd.has_key('comBuffMsg'):
                    msg = qd['comBuffMsg']
                else:
                    name = SD.data[stateId]['name']
                    msg = gameStrings.TEXT_IMPQUEST_2030 % (name, cnt)
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF),
                 const.QUEST_GOAL_TYPE: True,
                 const.QUEST_GOAL_ORDER: 'comBuff'})
            if qd.has_key('comBuffEx'):
                stateIds = qd['comBuffEx']
                if stateIds[0] == 0:
                    done = True
                    for index, stateId in enumerate(stateIds[1:]):
                        if stateId not in self.statesServerAndOwn and not self._checkTempStateIdInQuestData(questId, stateId):
                            done = False
                            break

                    if not done:
                        questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_CHATPROXY_2571,
                         const.QUEST_GOAL_STATE: False,
                         const.QUEST_GOAL_TRACK: False,
                         const.QUEST_GOAL_TRACK_ID: 0,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF_EX),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'comBuffEx'})
                        for index, stateId in enumerate(stateIds[1:]):
                            if stateId not in self.statesServerAndOwn and not self._checkTempStateIdInQuestData(questId, stateId):
                                name = SD.data[stateId]['name']
                                msg = gameStrings.TEXT_IMPQUEST_2061 % name
                                if qd.has_key('comBuffExTk'):
                                    trackId = qd['comBuffExTk'][index]
                                else:
                                    trackId = 0
                                questGoals.append({const.QUEST_GOAL_DESC: msg,
                                 const.QUEST_GOAL_STATE: False,
                                 const.QUEST_GOAL_TRACK: False,
                                 const.QUEST_GOAL_TRACK_ID: trackId,
                                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF_EX),
                                 const.QUEST_GOAL_TYPE: True,
                                 const.QUEST_GOAL_ORDER: 'comBuffEx'})
                                continue
                            name = SD.data[stateId]['name']
                            msg = gameStrings.TEXT_IMPQUEST_2077 % name
                            if qd.has_key('comBuffExTk'):
                                trackId = qd['comBuffExTk'][index]
                            else:
                                trackId = 0
                            questGoals.append({const.QUEST_GOAL_DESC: msg,
                             const.QUEST_GOAL_STATE: True,
                             const.QUEST_GOAL_TRACK: False,
                             const.QUEST_GOAL_TRACK_ID: trackId,
                             const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF_EX),
                             const.QUEST_GOAL_TYPE: True,
                             const.QUEST_GOAL_ORDER: 'comBuffEx'})

                elif stateIds[0] == 1:
                    done = False
                    for index, stateId in enumerate(stateIds[1:]):
                        if stateId in self.statesServerAndOwn or self._checkTempStateIdInQuestData(questId, stateId):
                            done = True
                            break

                    if not done:
                        questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_CHATPROXY_2577,
                         const.QUEST_GOAL_STATE: False,
                         const.QUEST_GOAL_TRACK: False,
                         const.QUEST_GOAL_TRACK_ID: 0,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF_EX),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'comBuffEx'})
                        for index, stateId in enumerate(stateIds[1:]):
                            name = SD.data[stateId]['name']
                            msg = gameStrings.TEXT_IMPQUEST_2061 % name
                            if qd.has_key('comBuffExTk'):
                                trackId = qd['comBuffExTk'][index]
                            else:
                                trackId = 0
                            questGoals.append({const.QUEST_GOAL_DESC: msg,
                             const.QUEST_GOAL_STATE: False,
                             const.QUEST_GOAL_TRACK: False,
                             const.QUEST_GOAL_TRACK_ID: trackId,
                             const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_COM_BUFF_EX),
                             const.QUEST_GOAL_TYPE: True,
                             const.QUEST_GOAL_ORDER: 'comBuffEx'})

            if qd.has_key('markerNpcs'):
                markerMsgs = qd['markerNpcsMsg']
                if self.getQuestData(questId, const.QD_QUEST_MARKER):
                    markerInfo, _ = self.getQuestData(questId, const.QD_QUEST_MARKER)
                    if not qd.has_key('triggerPartial'):
                        for i, markerId in enumerate(qd['markerNpcs']):
                            curCnt = markerInfo.get(markerId, 0)
                            if curCnt == 0:
                                done = False
                            else:
                                done = True
                            msg = '%s' % (markerMsgs[i],)
                            if qd.has_key('markerNpcsTk'):
                                isTrack = True
                                if gameglobal.rds.configData.get('enableRandomQuest', False) and qd.has_key('questTkRandom'):
                                    trackId = self.getQuestData(questId, const.QD_RANDOM_TKS, {1: (110157086,)}).get(uiConst.RANDOM_QUEST_TYPE, 1)
                                    questGoals.append({const.QUEST_GOAL_DESC: msg,
                                     const.QUEST_GOAL_STATE: done,
                                     const.QUEST_GOAL_TRACK: isTrack,
                                     const.QUEST_GOAL_TRACK_ID: trackId,
                                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_MARKER_NPCS),
                                     const.QUEST_GOAL_TYPE: True,
                                     const.QUEST_GOAL_ORDER: 'markerNpcs'})
                                    break
                                else:
                                    trackId = qd['markerNpcsTk'][i]
                            else:
                                isTrack = False
                                trackId = 0
                            questGoals.append({const.QUEST_GOAL_DESC: msg,
                             const.QUEST_GOAL_STATE: done,
                             const.QUEST_GOAL_TRACK: isTrack,
                             const.QUEST_GOAL_TRACK_ID: trackId,
                             const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_MARKER_NPCS),
                             const.QUEST_GOAL_TYPE: True,
                             const.QUEST_GOAL_ORDER: 'markerNpcs'})

                    else:
                        hasDoneCnt = 0
                        for i, markerId in enumerate(qd['markerNpcs']):
                            curCnt = markerInfo.get(markerId, 0)
                            if curCnt > 0:
                                hasDoneCnt += 1

                        done = hasDoneCnt == len(qd['markerNpcs'])
                        if qd.has_key('markerNpcsTk'):
                            isTrack = True
                            trackId = qd['markerNpcsTk'][hasDoneCnt]
                        else:
                            isTrack = False
                            trackId = 0
                        msg = markerMsgs[0] % (hasDoneCnt, len(qd['markerNpcs']))
                        questGoals.append({const.QUEST_GOAL_DESC: msg,
                         const.QUEST_GOAL_STATE: done,
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_MARKER_NPCS),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'markerNpcs'})
            if qd.has_key('markerNpcsGroup'):
                self._genMarkerNpcGroupGoal(questId, qd, questGoals)
            if qd.has_key('debateChatId'):
                flag = self.getQuestData(questId, const.QD_QUEST_DEBATE)
                cnt = 1 if flag == True else 0
                msg = '%s' % qd['debateMsg']
                if qd.has_key('debateNpcTk'):
                    isTrack = True
                    trackId = qd['debateNpcTk']
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: flag,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_DETATE_NPC),
                 const.QUEST_GOAL_TYPE: True,
                 const.QUEST_GOAL_ORDER: 'debateNpc'})
            if qd.has_key('puzzleId'):
                puzzleType = qd.get('puzzleType', const.PUZZLE_ANSWER_RIGHT)
                puzzleInfo = self.getQuestData(questId, const.QD_PUZZLE, {0: const.PUZZLE_EMPTY})
                answer = puzzleInfo.values()[0]
                if puzzleType == const.PUZZLE_ANSWER_RIGHT and answer == const.PUZZLE_RIGHE or puzzleType == const.PUZZLE_ANSWER_ANY and answer != const.PUZZLE_EMPTY:
                    cnt = 1
                else:
                    cnt = 0
                msg = gameStrings.TEXT_IMPQUEST_2218 % cnt
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: True if cnt else False,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('kingRoad'):
                from helpers import importantPlayRecommend as IPR
                inCompleteNum, allNum = IPR.incompleteItemsNum(self)
                desc = qd.get('kingRoadDesc', gameStrings.TEXT_IMPQUEST_2229)
                if desc.find('%d/%d') >= 0:
                    msg = desc % (allNum - inCompleteNum, 2)
                else:
                    msg = desc
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: self.getQuestData(questId, const.QD_KING_ROAD, False),
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('arenaWin'):
                cnt = self.getQuestData(questId, const.QD_ARENA_WIN)
                done = True if cnt >= qd['arenaWin'] else False
                msg = gameStrings.TEXT_IMPQUEST_2245 % (gameStrings.TEXT_IMPQUEST_2245_1, cnt, qd['arenaWin'])
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needDialog'):
                npcIds = qd['needDialog']
                dialogMsg = qd['needDialogMsg']
                dialogInfo = self.getQuestData(questId, const.QD_QUEST_CHAT)
                for i, npcId in enumerate(npcIds):
                    cnt = dialogInfo[npcId]
                    if cnt > 0:
                        done = True
                    else:
                        done = False
                    msg = '%s' % dialogMsg[i]
                    if qd.has_key('needDialogTk'):
                        isTrack = True
                        trackId = qd['needDialogTk'][i]
                    else:
                        isTrack = False
                        trackId = 0
                    questGoals.append({const.QUEST_GOAL_DESC: msg,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_NEED_DIALOG),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'needDialog'})

            if qd.has_key('needDialogGroup'):
                self._genDialogGroupGoal(questId, qd, questGoals)
            if qd.has_key('needConvoy'):
                charType = qd['needConvoy']
                done = self.getQuestData(questId, const.QD_CONVOY, 0) == charType
                name = MD.data[charType]['name']
                if qd.has_key('needMonsterTk'):
                    isTrack = True
                    trackId = qd['needMonsterTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                desc = qd.get('convoyDesc', '').split(',')
                desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_2295
                try:
                    desc = desc % (name,)
                except:
                    pass

                questGoals.append({const.QUEST_GOAL_DESC: desc,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_NEED_MONSTER),
                 const.QUEST_GOAL_TYPE: True,
                 const.QUEST_GOAL_ORDER: 'needConvoy'})
            if qd.has_key('questEquip'):
                if qd.has_key('questEquipTk'):
                    isTrack = True
                    trackId = qd['questEquipTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                questEquipReq = qd['questEquip']
                questEquip = self.getQuestData(questId, const.QD_EQUIPMENT, set())
                for itemId in questEquipReq:
                    if itemId in questEquip:
                        done = True
                    else:
                        done = False
                    name = ID.data[itemId]['name']
                    desc = qd.get('questEquipDesc', '').split(',')
                    desc = desc[0] if desc[0] else gameStrings.TEXT_IMPQUEST_2327
                    try:
                        desc = desc % (name,)
                    except:
                        pass

                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_EQUIP),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'questEquip'})

            if qd.has_key('pvpKill'):
                pvpKillInfo = self.getQuestData(questId, const.QD_PVP_KILL, {})
                for camp, cnt in qd['pvpKill'].iteritems():
                    if cnt == pvpKillInfo.get(camp, 0):
                        done = True
                    else:
                        done = False
                    questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_1475 % (pvpKillInfo.get(camp, 0), cnt),
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('playerSafe'):
                if qd.has_key('playerSafeTk'):
                    isTrack = True
                    trackId = qd['playerSafeTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                msg = qd.get('playerSafeMsg', gameStrings.TEXT_IMPQUEST_2364)
                done = self.getQuestData(questId, const.QD_PLAYER_SAFE, True)
                questGoals.append({const.QUEST_GOAL_DESC: msg,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: isTrack,
                 const.QUEST_GOAL_TRACK_ID: trackId,
                 const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_PLAYER_SAFE),
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('monsterSafe'):
                if qd.has_key('monsterSafeTk'):
                    isTrack = True
                    trackId = qd['monsterSafeTk'][i]
                else:
                    isTrack = False
                    trackId = 0
                monsterSafe = self.getQuestData(questId, const.QD_MONSTER_SAFE, {})
                for charType in monsterSafe:
                    monsterSafeName = qd.get('monsterSafeName', '')
                    if monsterSafeName:
                        msg = monsterSafeName
                    else:
                        name = MD.data[charType].get('name', gameStrings.TEXT_IMPQUEST_2388)
                        msg = qd.get('monsterSafeMsg', gameStrings.TEXT_IMPQUEST_2389 % (name,))
                    done = monsterSafe[charType]
                    questGoals.append({const.QUEST_GOAL_DESC: msg,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_MONSTER_SAFE),
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('isMinLvTrack') and qd.has_key('comMinLv'):
                minLv = qd.get('comMinLv')
                done = minLv <= self.lv
                questGoals.append({const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_2402 % (minLv,),
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('questVars'):
                for i, (var, cnt) in enumerate(qd['questVars']):
                    if cnt <= self.questVars.get(var, 0):
                        done = True
                        canGuildHelp = 0
                    else:
                        done = False
                        canGuildHelp = qd.get('canGuildHelp', 0) if gameglobal.rds.configData.get('enableGuildQuestOptimize', False) else 0
                    if qd.has_key('questVarsTk'):
                        isTrack = True
                        trackId = qd['questVarsTk'][i]
                    else:
                        isTrack = False
                        trackId = 0
                    desc = qd.get('questVarsDesc', '').split(',')
                    if i >= len(desc):
                        desc = gameStrings.TEXT_IMPQUEST_1500
                    else:
                        desc = desc[i] if desc[i] else gameStrings.TEXT_IMPQUEST_1500
                    try:
                        if desc.find('%s') != -1:
                            desc = desc % (self.questVars.get(var, 0), cnt)
                        else:
                            desc = desc % (self.questVars.get(var, 0), cnt)
                    except:
                        pass

                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_VAR),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'questVars',
                     const.QUEST_GOAL_GUILD_HELP: canGuildHelp})

            if qd.has_key('questAchieve'):
                achieveIds = qd['questAchieve']
                achieveInfo = self.getQuestData(questId, const.QD_ACHIEVE, {})
                if not isinstance(achieveIds, tuple):
                    achieveIds = (achieveIds,)
                if qd.has_key('questAchieveTk'):
                    isTrack = True
                    questAchieveTks = qd['questAchieveTk']
                    if not isinstance(questAchieveTks, tuple):
                        questAchieveTks = (questAchieveTks,)
                else:
                    isTrack = False
                if qd.has_key('questAchieveDesc'):
                    isDesc = True
                    questAchieveDescs = qd['questAchieveDesc']
                    if not isinstance(questAchieveDescs, tuple):
                        questAchieveDescs = (questAchieveDescs,)
                else:
                    isDesc = False
                for i, achieveId in enumerate(achieveIds):
                    if achieveInfo.get(achieveId, False):
                        done = True
                    else:
                        done = False
                    if isTrack:
                        trackId = questAchieveTks[i]
                    else:
                        trackId = 0
                    if isDesc:
                        desc = questAchieveDescs[i]
                    else:
                        desc = gameStrings.TEXT_IMPQUEST_1500
                    try:
                        if desc.find('%d') != -1:
                            cur = 1 if done else 0
                            desc = desc % (cur, 1)
                    except:
                        pass

                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_ACHIEVE),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'questAchieve'})

            if qd.has_key('questAchieveOr'):
                achieveIds = qd['questAchieveOr']
                achieveInfo = self.getQuestData(questId, const.QD_ACHIEVE, {})
                isShowOne = qd.get('questAchieveOrShowOne', 0)
                if isShowOne:
                    for i, achieveId in enumerate(achieveIds):
                        if achieveInfo.get(achieveId, False):
                            done = True
                            break
                    else:
                        done = False

                    if qd.has_key('questAchieveOrTk'):
                        isTrack = True
                        trackId = qd['questAchieveOrTk'][0]
                    else:
                        isTrack = False
                        trackId = 0
                    if qd.has_key('questAchieveOrOneDesc'):
                        desc = qd.get('questAchieveOrOneDesc')
                    else:
                        desc = '...'
                    questGoals.append({const.QUEST_GOAL_DESC: desc,
                     const.QUEST_GOAL_STATE: done,
                     const.QUEST_GOAL_TRACK: isTrack,
                     const.QUEST_GOAL_TRACK_ID: trackId,
                     const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_ACHIEVE),
                     const.QUEST_GOAL_TYPE: True,
                     const.QUEST_GOAL_ORDER: 'questAchieve'})
                else:
                    for i, achieveId in enumerate(achieveIds):
                        if achieveInfo.get(achieveId, False):
                            done = True
                        else:
                            done = False
                        if qd.has_key('questAchieveOrTk'):
                            isTrack = True
                            trackId = qd['questAchieveOrTk'][i]
                        else:
                            isTrack = False
                            trackId = 0
                        if qd.has_key('questAchieveOrDesc'):
                            desc = qd.get('questAchieveOrDesc')[i]
                        else:
                            desc = gameStrings.TEXT_IMPQUEST_1500
                        try:
                            if desc.find('%d') != -1:
                                cur = 1 if done else 0
                                desc = desc % (cur, 1)
                        except:
                            pass

                        questGoals.append({const.QUEST_GOAL_DESC: desc,
                         const.QUEST_GOAL_STATE: done,
                         const.QUEST_GOAL_TRACK: isTrack,
                         const.QUEST_GOAL_TRACK_ID: trackId,
                         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, gametypes.TRACK_TYPE_QUEST_ACHIEVE),
                         const.QUEST_GOAL_TYPE: True,
                         const.QUEST_GOAL_ORDER: 'questAchieve'})

            if qd.has_key('needZaiju'):
                describe = qd.get('needZaijuDesc', '')
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: True,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('skillEnhancePoint'):
                skillPoints = qd['skillEnhancePoint']
                describe = qd.get('skillEnhancePointDesc', '')
                describe = describe % (utils.getTotalSkillEnhancePoint(self), skillPoints)
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: utils.getTotalSkillEnhancePoint(self) >= skillPoints,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needSkillEnhance'):
                skillEnhanceInfo = qd['needSkillEnhance']
                describes = qd['needSkillEnhanceDesc']
                for i, (partLv, cnt) in enumerate(skillEnhanceInfo):
                    describe = describes[i] % (utils.getSkillEnhanceCntByPart(self, partLv), cnt)
                    questGoals.append({const.QUEST_GOAL_DESC: describe,
                     const.QUEST_GOAL_STATE: utils.getSkillEnhanceCntByPart(self, partLv) >= cnt,
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('needSkillEnhancePartOr'):
                skillEnhancePartInfo = qd['needSkillEnhancePartOr']
                describe = qd['needSkillEnhancePartOrDesc']
                done = False
                for skillId, part in skillEnhancePartInfo:
                    if utils.isSkillEnhanced(self, skillId, part):
                        done = True

                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needSkillEnhancePartAnd'):
                skillEnhancePartInfo = qd['needSkillEnhancePartAnd']
                describes = qd['needSkillEnhancePartAndDesc']
                for i, (skillId, part) in enumerate(skillEnhancePartInfo):
                    describe = describes[i]
                    questGoals.append({const.QUEST_GOAL_DESC: describe,
                     const.QUEST_GOAL_STATE: utils.isSkillEnhanced(self, skillId, part),
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('needDaoheng'):
                describe = qd['needDaohengDesc']
                done = False
                for sVal in self.wsSkills.itervalues():
                    if sum(sVal.daoHeng.values()) > 0 or len(sVal.slots) > 0:
                        done = True
                        break

                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needShenli'):
                shenliCnt = qd['needShenli']
                describe = qd['needShenliDesc']
                describe = describe % (len(self.runeBoard.pskillSet), shenliCnt)
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: len(self.runeBoard.pskillSet) >= shenliCnt,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needShenliPartOr'):
                shenliInfo = qd['needShenliPartOr']
                describes = qd['needShenliPartOrDesc']
                for i, (shenliId,) in enumerate(shenliInfo):
                    describe = describes[i]
                    questGoals.append({const.QUEST_GOAL_DESC: describe,
                     const.QUEST_GOAL_STATE: shenliId in self.runeBoard.pskillSet,
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TYPE: True})

            if qd.has_key('needShenliPartAnd'):
                shenliInfo = qd['needShenliPartAnd']
                describe = qd['needShenliPartAndDesc']
                done = False
                for shenliId in shenliInfo:
                    if shenliId in self.runeBoard.pskillSet:
                        done = True

                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('needRuneEquipLv'):
                runeEquipLv, runeEquipCnt = qd['needRuneEquipLv']
                describe = qd['needRuneEquipLvDesc']
                describe = describe % (commQuest.getRuneLvLarger(self, runeEquipLv), runeEquipCnt)
                done = commQuest.getRuneLvLarger(self, runeEquipLv) >= runeEquipCnt
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: done,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('businessLv'):
                businessLv = qd['businessLv']
                blcd = BLCD.data[businessLv]
                fameId = BCD.data['businessFameId']
                maxFame = blcd['maxFame']
                curFame = self.fame.get(fameId, 0)
                describe = qd['businessLvDesc']
                describe = describe % (curFame, maxFame)
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: curFame >= maxFame,
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('fireworkVar'):
                describe = qd['fireworkVarDesc']
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: self.getQuestData(questId, const.QD_FIREWORK, False),
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('cmpReqCombatScore'):
                describe = qd.get('cmpReqCombatScoreDesc', gameStrings.TEXT_IMPQUEST_2707 % qd.get('cmpReqCombatScore', gameStrings.TEXT_LIFESKILLFACTORY_247))
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: self.combatScoreList[const.COMBAT_SCORE] >= qd['cmpReqCombatScore'],
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('cmpReqApprenticeVal'):
                describe = qd.get('cmpReqApprenticeValDesc', gameStrings.TEXT_IMPQUEST_2715 % qd.get('cmpReqApprenticeVal', gameStrings.TEXT_LIFESKILLFACTORY_247))
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: commQuest.apprenticeValCheckEx(self, qd.get('cmpReqApprenticeVal', 0)),
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            if qd.has_key('jingJieLimit'):
                describe = qd.get('jingJieLimitDesc', gameStrings.TEXT_IMPQUEST_2723 % JJD.data.get(qd.get('jingJieLimit', 0), {}).get('name', gameStrings.TEXT_FRIENDPROXY_1834))
                questGoals.append({const.QUEST_GOAL_DESC: describe,
                 const.QUEST_GOAL_STATE: self.jingJie >= qd.get('jingJieLimit'),
                 const.QUEST_GOAL_TRACK: False,
                 const.QUEST_GOAL_TRACK_ID: 0,
                 const.QUEST_GOAL_TYPE: True})
            questGoals = self.sortQuestGoal(questGoals, questId, isQuestLog)
            return questGoals

    def _genComNpcGoal(self, questId):
        qd = QD.data.get(questId)
        if self._isQuestFailed(questId):
            if qd.get('type') == gametypes.QUEST_TYPE_LOOP:
                qloopId = None
                for loopId, questInfo in BigWorld.player().questLoopInfo.items():
                    if questInfo.getCurrentQuest() == questId:
                        qloopId = loopId
                        break

                if qloopId and QDID.data.has_key(qloopId):
                    return {const.QUEST_GOAL_DESC: gameStrings.TEXT_IMPQUEST_2747,
                     const.QUEST_GOAL_STATE: False,
                     const.QUEST_GOAL_TRACK: False,
                     const.QUEST_GOAL_TRACK_ID: 0,
                     const.QUEST_GOAL_TRACK_TYPE: 0,
                     const.QUEST_GOAL_TYPE: True}
            if qd.has_key('questGroup') and not commQuest.isQuestGroupMatch(self, qd['questGroup']):
                questGroupId = qd['questGroup']
                if QGD.data.has_key(questGroupId):
                    qgd = QGD.data[questGroupId]
                    firstQuestId = qgd['quests'][0]
                    qd = QD.data.get(firstQuestId)
            if not qd.has_key('acNpc'):
                return {}
            if qd.get('canReAcc', 1) == 0:
                return {}
            acNpcId = qd.get('acNpc', '')
            name = uiUtils.getNpcName(acNpcId)
            msg = gameStrings.TEXT_IMPQUEST_2770 % name
            if qd.has_key('acNpcTk'):
                isTrack = True
                trackId = qd['acNpcTk']
            else:
                isTrack = False
                trackId = 0
            if QD.data.get(questId, {}).get('autoAc', 0):
                msg = gameStrings.TEXT_IMPQUEST_2779
                isTrack = False
                trackId = 0
            return {const.QUEST_GOAL_DESC: msg,
             const.QUEST_GOAL_STATE: False,
             const.QUEST_GOAL_TRACK: isTrack,
             const.QUEST_GOAL_TRACK_ID: trackId,
             const.QUEST_GOAL_TRACK_TYPE: self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_AC),
             const.QUEST_GOAL_TYPE: True}
        elif not qd.has_key('compNpc'):
            return {}
        elif qd.get('comMinLv', 0) > self.lv:
            return {}
        else:
            compNpcId = commQuest.getQuestCompNpc(self, questId)
            name = uiUtils.getNpcName(compNpcId)
            msg = qd.get('compNpcDesc', '')
            try:
                msg = msg % name
            except:
                msg = gameStrings.TEXT_IMPQUEST_2805 % name

            if qd.has_key('comNpcTk'):
                isTrack = True
                compNpc = commQuest.getQuestCompNpc(self, questId)
                trackId = str(uiUtils.getNpcTrackId(questId, compNpc, 'comNpc'))
            else:
                isTrack = False
                trackId = 0
            return {const.QUEST_GOAL_DESC: msg,
             const.QUEST_GOAL_STATE: False,
             const.QUEST_GOAL_TRACK: isTrack,
             const.QUEST_GOAL_TRACK_ID: trackId,
             const.QUEST_GOAL_TRACK_TYPE: self._filterCommitTrackType(qd, gametypes.TRACK_TYPE_NPC_COM),
             const.QUEST_GOAL_TYPE: True}

    def _updateQuestInfoCacheByPatch(self, questDataId, exData):
        if len(self.questInfoCache) == 0 or questDataId == const.QD_FETCH_ALL:
            self.fetchQuestsInfo()
            if questDataId == const.QD_FETCH_ALL:
                self.initQuestLoopModifyTimer()
                self.fetchAllTrackedQuest()
            return
        if questDataId == const.QD_ACCEPT:
            avlQuestIds = []
            avlQuestLoopIds = []
            if exData and exData.has_key('questIds'):
                avlQuestIds.extend(exData['questIds'])
                for questId in [ x for x in avlQuestIds ]:
                    if AQURD.data.has_key(questId):
                        aqurd = AQURD.data[questId]
                        avlQuestIds.extend(aqurd['acQuests'])
                    if QLID.data.has_key(questId):
                        questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
                        if AQLURD.data.has_key(questLoopId):
                            avlQuestLoopIds.extend(AQLURD.data.get(questLoopId, {}).get('acQuestLoops', []))

            self._onUpdateQuestInfoCacheModified(avlQuestIds, avlQuestLoopIds)
        elif questDataId == const.QD_COMPLETE:
            avlQuestIds = []
            comSucQstLoop = []
            if exData and exData.has_key('questIds'):
                avlQuestIds.extend(exData['questIds'])
                for questId in [ x for x in avlQuestIds ]:
                    if AQURD.data.has_key(questId):
                        aqurd = AQURD.data[questId]
                        avlQuestIds.extend(aqurd['compQuests'])
                    if QLID.data.has_key(questId):
                        questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
                        if AQLURD.data.has_key(questLoopId) and QLD.data.has_key(questLoopId):
                            comSucQstLoop.extend(AQLURD.data.get(questLoopId, {}).get('comSucQstLoop', []))
                            comSucQstLoop.extend(AQLURD.data.get(questLoopId, {}).get('compQuestLoops', []))

            self._onUpdateQuestInfoCacheModified(avlQuestIds, comSucQstLoop)
        elif questDataId == const.QD_ABANDON:
            avlQuestIds = []
            avlQuestLoopIds = []
            if exData and exData.has_key('questIds'):
                avlQuestIds.extend(exData['questIds'])
                for questId in [ x for x in avlQuestIds ]:
                    if AQURD.data.has_key(questId):
                        aqurd = AQURD.data[questId]
                        for abandonQuestId in aqurd['abandonQuests']:
                            if abandonQuestId not in avlQuestIds:
                                avlQuestIds.append(abandonQuestId)

                    if QLID.data.has_key(questId):
                        questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
                        if AQLURD.data.has_key(questLoopId):
                            avlQuestLoopIds.extend(AQLURD.data.get(questLoopId, {}).get('abandonQuests', []))

            self._onUpdateQuestInfoCacheModified(avlQuestIds, avlQuestLoopIds)
            if gameglobal.rds.ui.dynamicFCastBar.widget:
                gameglobal.rds.ui.pressKeyF.hide()
        elif questDataId == const.QD_LV_UP:
            newLv = exData['lv']
            avlQuestIds = []
            if AQULD.data.has_key((newLv, const.QD_LV_UP)):
                avlQuestIds.extend(AQULD.data[newLv, const.QD_LV_UP])
            if AQULD.data.has_key((newLv - 1, const.QD_LV_UP)):
                avlQuestIds.extend(AQULD.data[newLv - 1, const.QD_LV_UP])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_APPRENTICE:
            avlQuestIds = []
            if AQULD.data.has_key((0, const.QD_APPRENTICE)):
                avlQuestIds.extend(AQULD.data[0, const.QD_APPRENTICE])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_JUNJIE_LV_UP:
            avlQuestIds = []
            junjieLv = exData['junJieLv']
            if exData.has_key('questIds'):
                avlQuestIds.extend(exData['questIds'])
            if AQULD.data.has_key((junjieLv, const.QD_JUNJIE_LV_UP)):
                avlQuestIds.extend(AQULD.data[junjieLv, const.QD_JUNJIE_LV_UP])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_JINGJIE_UP:
            avlQuestIds = []
            jingjieLimit = exData['jingjieLimit']
            if AQULD.data.has_key((jingjieLimit, const.QD_JINGJIE_UP)):
                avlQuestIds.extend(AQULD.data[jingjieLimit, const.QD_JINGJIE_UP])
                exData.update({'questIds': AQULD.data[jingjieLimit, const.QD_JINGJIE_UP]})
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_JUEWEI_LV_UP:
            jueWeiLv = exData['jueWeiLv']
            avlQuestIds = []
            if AQULD.data.has_key((jueWeiLv, const.QD_JUEWEI_LV_UP)):
                avlQuestIds.extend(AQULD.data[jueWeiLv, const.QD_JUEWEI_LV_UP])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_QUMO_LV:
            qumoLv = exData['qumoLv']
            avlQuestIds = []
            if AQULD.data.has_key((qumoLv, const.QD_QUMO_LV)):
                avlQuestIds.extend(AQULD.data[qumoLv, const.QD_QUMO_LV])
            if AQULD.data.has_key((qumoLv - 1, const.QD_QUMO_LV)):
                avlQuestIds.extend(AQULD.data[qumoLv - 1, const.QD_QUMO_LV])
            if AQULD.data.has_key((qumoLv + 1, const.QD_QUMO_LV)):
                avlQuestIds.extend(AQULD.data[qumoLv + 1, const.QD_QUMO_LV])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_PREQUMO_LV:
            acPreQumoLv = exData['preQumoLv']
            avlQuestIds = []
            if AQULD.data.has_key((acPreQumoLv, const.QD_PREQUMO_LV)):
                avlQuestIds.extend(AQULD.data[acPreQumoLv, const.QD_PREQUMO_LV])
            if AQULD.data.has_key((acPreQumoLv - 1, const.QD_PREQUMO_LV)):
                avlQuestIds.extend(AQULD.data[acPreQumoLv - 1, const.QD_PREQUMO_LV])
            if AQULD.data.has_key((acPreQumoLv + 1, const.QD_QUMO_LV)):
                avlQuestIds.extend(AQULD.data[acPreQumoLv + 1, const.QD_PREQUMO_LV])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_TMT_CAMP:
            avlQuestIds = []
            if AQULD.data.has_key((0, const.QD_TMT_CAMP)):
                avlQuestIds.extend(AQULD.data[0, const.QD_TMT_CAMP])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_LOOP_TIME:
            avlQuestLoopIds = AQULD.data['questLoopTime']
            self._onUpdateQuestInfoCacheModified([], avlQuestLoopIds)
        elif questDataId == const.QD_SERVER_PROCESS:
            msId = exData.get('msId', 0)
            avlQuestIds = []
            if AQULD.data.has_key((msId, const.QD_SERVER_PROCESS)):
                avlQuestIds.extend(AQULD.data[msId, const.QD_SERVER_PROCESS])
            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_WW_CAMP:
            camps = exData.get('wwTempCamp', [])
            avlQuestIds = []
            for camp in camps:
                if AQULD.data.has_key((camp, const.QD_WW_CAMP)):
                    avlQuestIds.extend(AQULD.data[camp, const.QD_WW_CAMP])

            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        elif questDataId == const.QD_JIEQI:
            if exData and exData.has_key('refreshAll'):
                avlQuestIds = []
                avlQuestLoopIds = []
                if exData.get('refreshAll', 0):
                    for key, value in IQURD.data.iteritems():
                        if key[1] == 0:
                            for quest in value:
                                if quest not in avlQuestIds:
                                    avlQuestIds.append(quest)

                        else:
                            for quest in value:
                                if quest not in avlQuestLoopIds:
                                    avlQuestLoopIds.append(quest)

                    self._onUpdateQuestInfoCacheModified(avlQuestIds, avlQuestLoopIds)
            elif exData and exData.has_key('intimacy'):
                avlQuestIds = []
                avlQuestLoopIds = []
                intimacy = exData['intimacy']
                intimacyLv = 0
                MAX_INTIMACY_LV = ICD.data.get('MAX_INTIMACY_LV', const.MAX_INTIMACY_LV)
                for i in xrange(1, MAX_INTIMACY_LV + 1):
                    lastMaxVal = IMD.data.get(i, {}).get('maxVal', const.MAX_INTIMACY_VALUE)
                    if intimacy <= lastMaxVal:
                        intimacyLv = i
                        break

                if intimacyLv:
                    for quest in IQURD.data.get((intimacyLv, 0), []):
                        if quest not in avlQuestIds:
                            avlQuestIds.append(quest)

                    for quest in IQURD.data.get((intimacyLv, 1), []):
                        if quest not in avlQuestLoopIds:
                            avlQuestLoopIds.append(quest)

                    if intimacyLv > 1:
                        for quest in IQURD.data.get((intimacyLv - 1, 0), []):
                            if quest not in avlQuestIds:
                                avlQuestIds.append(quest)

                        for quest in IQURD.data.get((intimacyLv - 1, 1), []):
                            if quest not in avlQuestLoopIds:
                                avlQuestLoopIds.append(quest)

                    self._onUpdateQuestInfoCacheModified(avlQuestIds, avlQuestLoopIds)
        elif questDataId == const.QD_QIREN:
            avlQuestIds = []
            if exData and exData.has_key('cids'):
                cids = exData.get('cids', ())
                for cid in cids:
                    comSucQsts = QQURD.data.get(cid, {}).get('comSucQst', [])
                    avlQuestIds.extend(comSucQsts)

            self._onUpdateQuestInfoCacheModified(avlQuestIds)
        else:
            self._onUpdateQuestInfoCacheModified([])
        mQuests = exData.get('questIds', [])
        if len(mQuests) > 0:
            for questId in mQuests:
                if commQuest.completeQuestCheck(self, questId):
                    gameglobal.rds.tutorial.onCompleteQuestCondition(questId)

            cEvent = Event(events.EVENT_QUEST_INFO_CHANGE, {'mqList': mQuests})
            gameglobal.rds.ui.dispatchEvent(cEvent)

    def _onUpdateQuestInfoCacheModified(self, allQuestIds, allQuestLoopIds = []):
        if not self.questInfoCache.has_key('available_tasks'):
            return
        questIds = []
        questLoopIds = [ x for x in allQuestLoopIds ]
        for questId in allQuestIds:
            if QLID.data.has_key(questId):
                questLoopId = QLID.data[questId]['questLoop']
                if questLoopId not in questLoopIds:
                    questLoopIds.append(questLoopId)
            elif questId not in questIds:
                questIds.append(questId)

        tmpQuestInfos = commQuest.getQuestInfo(self, questIds, [ x for x in self.quests ], {x:[] for x in questLoopIds}, {x:[] for x in self.questLoopInfo.keys()})
        self.questInfoCache['unfinished_tasks'] = tmpQuestInfos['unfinished_tasks']
        self.questInfoCache['complete_tasks'] = tmpQuestInfos['complete_tasks']
        self.questInfoCache['complete_extra_tasks'] = tmpQuestInfos['complete_extra_tasks']
        tmpAvlQuestsIds = tmpQuestInfos['available_tasks']
        rmQuestIds = []
        for questId in self.questInfoCache['available_tasks']:
            if questId in questIds and questId not in tmpAvlQuestsIds:
                rmQuestIds.append(questId)
                continue
            if questId in self.questInfoCache['complete_tasks']:
                rmQuestIds.append(questId)
                continue
            if questId in self.questInfoCache['complete_extra_tasks']:
                rmQuestIds.append(questId)
                continue
            if self.getQuestFlag(questId):
                rmQuestIds.append(questId)
                continue

        for questId in rmQuestIds:
            self.questInfoCache['available_tasks'].remove(questId)

        for questId in tmpAvlQuestsIds:
            if questId not in self.questInfoCache['available_tasks']:
                self.questInfoCache['available_tasks'].append(questId)

        self.questInfoCache['unfinished_taskLoops'] = tmpQuestInfos['unfinished_taskLoops']
        self.questInfoCache['complete_taskLoops'] = tmpQuestInfos['complete_taskLoops']
        self.questInfoCache['complete_extra_taskLoops'] = tmpQuestInfos['complete_extra_taskLoops']
        tmpAvlQuestLoopIds = tmpQuestInfos['available_taskLoops']
        rmQuestLoopIds = []
        for questLoopId in self.questInfoCache['available_taskLoops']:
            if questLoopId in self.questInfoCache['complete_taskLoops']:
                rmQuestLoopIds.append(questLoopId)
                continue
            if questLoopId in self.questInfoCache['complete_extra_tasks']:
                rmQuestLoopIds.append(questLoopId)
                continue
            if questLoopId in questLoopIds and questLoopId not in tmpAvlQuestLoopIds:
                rmQuestLoopIds.append(questLoopId)
                continue
            if self.questLoopInfo.has_key(questLoopId) and self.questLoopInfo[questLoopId].getCurrentQuest():
                rmQuestLoopIds.append(questLoopId)
                continue

        for questLoopId in rmQuestLoopIds:
            self.questInfoCache['available_taskLoops'].remove(questLoopId)

        for questLoopId in tmpAvlQuestLoopIds:
            if questLoopId not in self.questInfoCache['available_taskLoops']:
                self.questInfoCache['available_taskLoops'].append(questLoopId)

    def closePuzzleWindow(self):
        gameglobal.rds.ui.puzzle.hideQuestChoicePuzzle()

    def onQuestInfoModifiedAtClient(self, questDataId, exData = {}):
        if not self.inWorld:
            return
        if gameglobal.rds.configData.get('enableQuestTempStateId', False) and questDataId == const.QD_STATE:
            if exData.has_key('questIds') and exData.has_key('qstateId'):
                tempStateIdTime = utils.getNow()
                for questId in exData.get('questIds'):
                    self.setQuestData(questId, const.QD_TEMP_STATE_ID, (exData.get('qstateId'), tempStateIdTime))

        self._updateQuestInfoCacheByPatch(questDataId, exData)
        gameglobal.rds.ui.questLog.refreshTaskList()
        gameglobal.rds.ui.delegationBook.refreshAcceptedPanel()
        if questDataId != const.QD_ACCEPT:
            if questDataId == const.QD_FAIL:
                if gameglobal.rds.ui.puzzle.mediator:
                    gameglobal.rds.ui.puzzle.questFinished()
                if gameglobal.rds.ui.quest.isShow:
                    gameglobal.rds.ui.quest.close()
                if gameglobal.rds.ui.npcV2.isShow:
                    gameglobal.rds.ui.npcV2.leaveStage()
            elif questDataId == const.QD_PUZZLE:
                questIds = exData.get('questIds', [])
                puzzleInfo = {}
                if questIds:
                    puzzleInfo = self.getQuestData(questIds[0], const.QD_PUZZLE, {})
                if gameglobal.rds.ui.puzzle.mediator:
                    gameglobal.rds.ui.puzzle.puzzleAnswerUpdate(puzzleInfo)
        questIds = exData.get('questIds', [])
        if questDataId == const.QD_ACCEPT and len(questIds) > 0 and QD.data[questIds[0]].get('notPuzzleDirectUI'):
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
        if questDataId == const.QD_LV_UP and self == BigWorld.player() and exData.has_key('lvUpQuestId'):
            birdEffect.showBirdEffect()
        pickNearDist = SCD.data.get('pickNearQuestBoxLength', 6) * SCD.data.get('pickNearQuestBoxLength', 6)
        entities = BigWorld.entities.values()
        questBoxes = [ x for x in entities if utils.instanceof(x, 'QuestBox') ]
        questBoxTraps = []
        for questBox in questBoxes:
            questBox.updateBoxState()
            if (questBox.position - BigWorld.player().position).lengthSquared < pickNearDist:
                questBoxTraps.append(questBox)

        BigWorld.player().boxTrapCallback(questBoxTraps)
        npcs = []
        pots = []
        for x in BigWorld.entities.values():
            if x.__class__.__name__ in ('Npc', 'ClientNpc', 'MovableNpc') and x.isScenario == gameglobal.NORMAL_NPC:
                npcs.append(x)
            if x.IsPot:
                pots.append(x)

        questNpcIds = []
        for npc in npcs:
            if npc._isQuestNpc():
                questNpcIds.append(npc.id)
                if questDataId == const.QD_FAIL and utils.isEntitiyInRange2D(self, npc, const.QUEST_TRAP_LENGTH):
                    npc.autoDelQuestNearBy()

        for pot in pots:
            pot.refreshOpacityState()

        BigWorld.callback(0.1, Functor(self.refreshMarkNpcStates, npcs))
        self.updateQuestDisplayFromCache(questNpcIds)
        self.showQuestProgressMsg(questDataId, exData)
        self._updateQuestMonsterInfo(questDataId, exData)
        self._updateQuestMonsterLogo()
        if questDataId == const.QD_MONSTER_KILL:
            self._updateFunNpcFx(exData)
        elif questDataId == const.QD_QUEST_CHAT and exData.has_key('questIds'):
            self._upateChatFx(exData['questIds'])
        elif questDataId == const.QD_VARS:
            for questId in self.quests:
                if commQuest.reachMaxJobScore(self, questId):
                    self._removeJobMarkFx(questId)
                if commQuest.reachExtraVarBonux(self, questId):
                    if self.getQuestData(questId, const.QD_EXTRA_BONUS_NUID) == self.gbId:
                        self.showGameMsg(GMDD.data.QUEST_EXTRA_BONUS_COMP_OWNER, ())
                    else:
                        self.showGameMsg(GMDD.data.QUEST_EXTRA_BONUS_COMP_OTHERS, ())

        elif questDataId == const.QD_FAIL:
            for questId in self.quests:
                if self.getQuestData(questId, const.QD_FAIL, False):
                    self._removeJobMarkFx(questId)
                    if gameglobal.rds.ui.dynamicFCastBar.widget:
                        gameglobal.rds.ui.pressKeyF.hide()

        elif questDataId == const.QD_QUEST_DEBATE:
            for questId in self.quests:
                if self.getQuestData(questId, const.QD_QUEST_DEBATE, False):
                    self._removeDebateFx(questId)

        elif questDataId == const.QD_ITEM_COLLECT:
            for questId in self.quests:
                self._addMarkFx(questId)

            gameglobal.rds.ui.shop.refreshInfoByCache()
            gameglobal.rds.ui.compositeShop.refreshInfoByCache()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        self.queryTeamGuideQuestStatus()
        gameAntiCheatingManager.getInstance().startRecordLog()

    def refreshMarkNpcStates(self, npcs):
        for npc in npcs:
            if npc.inWorld and npc._isMarkerNpc() and not npc._isQuestNpc():
                npc.refreshOpacityState()

    def initQuestLoopModifyTimer(self):
        if not self.inWorld:
            return
        if self.questLoopModifyTimer > 0:
            BigWorld.cancelCallback(self.questLoopModifyTimer)
            self.questLoopModifyTimer = 0
        current = utils.getNow()
        nextTime = 0
        for questLoopId in AQULD.data['questLoopTime']:
            qld = QLD.data[questLoopId]
            timerIntervals = qld.get('acStartTimes', ()) + qld.get('acEndTimes', ())
            for interval in timerIntervals:
                tmpNextTime = utils.nextByTimeTuple(interval, current)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime

            for startXingjiTime, endXingjiTime in qld.get('acXingjiTimes', ()):
                tmpNextTime = formula.getRealTimeToAXingJiMoment(startXingjiTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime
                tmpNextTime = formula.getRealTimeToAXingJiMoment(endXingjiTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime

        self._updateQuestInfoCacheByPatch(const.QD_LOOP_TIME, {})
        if nextTime > 0:
            self.questLoopModifyTimer = BigWorld.callback(nextTime + 2, Functor(self.initQuestLoopModifyTimer))

    def displayChahua(self, picId):
        pass

    def _showItemMsg(self, exData):
        itemId = exData.get('itemId', 0)
        itemName = ID.data.get(itemId, {}).get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
        for questId in self.quests:
            qd = QD.data.get(questId, {})
            curNum = 0
            needNum = -1
            itemCollectType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
            if not commQuest.enableQuestMaterialBag(self, qd):
                if qd.has_key('compItemCollect'):
                    cmpItem = qd.get('compItemCollect', None)
                    if not cmpItem:
                        continue
                    cmpItem = dict(cmpItem)
                    if not cmpItem.has_key(itemId):
                        continue
                    if itemCollectType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY, const.QUEST_COMPCOND_EXACT):
                        needNum = cmpItem[itemId]
                        curNum = self.questCountItem(questId, itemId)
                    elif itemCollectType == const.QUEST_COMPCOND_ALL:
                        needNum = cmpItem[itemId]
                        curNum = sum(map(lambda itemId: self.questCountItem(questId, itemId), cmpItem))
                elif qd.has_key('yaoJingQitanCompItemMulti') and gameglobal.rds.configData.get('enableYaojingqitanCustomCost', False):
                    cmpItems = qd.get('yaoJingQitanCompItemMulti', None)
                    if not cmpItems:
                        continue
                    p = BigWorld.player()
                    costList = SCD.data.get('yaojingqitanCost', {})
                    costType = getattr(p, 'yaojingqitanCostType', 1)
                    costInfo = costList.get(costType, None)
                    for cmpItemIds in cmpItems:
                        if costInfo:
                            needNum = costInfo[0]
                        else:
                            needNum = 0
                        curNum = sum(map(lambda itemId: self.questCountItem(questId, itemId), cmpItemIds))

                elif qd.has_key('compItemCollectMulti'):
                    cmpItems = qd.get('compItemCollectMulti', None)
                    if not cmpItems:
                        continue
                    for cmpItem in cmpItems:
                        cmpItem = dict(cmpItem)
                        if not cmpItem.has_key(itemId):
                            continue
                        needNum = cmpItem[itemId]
                        curNum = sum(map(lambda itemId: self.questCountItem(questId, itemId), cmpItem))
                        break

            else:
                cmpItem = qd.get('compMaterialItemCollectAndConsume', None)
                if not cmpItem:
                    continue
                cmpItem = dict(cmpItem)
                if not cmpItem.has_key(itemId):
                    continue
                needNum = cmpItem[itemId]
                curNum = self.questCountMaterialItem(itemId)
            if curNum > needNum and itemCollectType != const.QUEST_COMPCOND_EXACT:
                continue
            questName = qd.get('name', '')
            self.showGameMsg(GMDD.data.QUEST_PROGRESS_PROMPT, (questName,
             itemName,
             curNum,
             needNum))

    def _showKillMonsterMsg(self, exData):
        for questId in self.quests:
            qd = QD.data.get(questId, {})
            needMonsters = qd.get('needMonsters', None)
            if needMonsters == None:
                continue
            needMonsters = dict(needMonsters)
            monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
            needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
            mType = exData.get('mType', 0)
            if not needMonsters.has_key(mType):
                continue
            if needMonstersType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY):
                needNum = needMonsters[mType]
                curNum = monsterInfo.get(mType, 0)
            elif needMonstersType == const.QUEST_COMPCOND_ALL:
                needNum = needMonsters.values()[0]
                curNum = sum(monsterInfo.values())
            if curNum > needNum:
                continue
            questName = qd.get('name', '')
            monsterName = MD.data[mType].get('name', gameStrings.TEXT_IMPQUEST_2388)
            self.showGameMsg(GMDD.data.QUEST_PROGRESS_PROMPT, (questName,
             monsterName,
             curNum,
             needNum))

    def showQuestProgressMsg(self, questDataId, exData):
        if questDataId == const.QD_ITEM_COLLECT:
            self._showItemMsg(exData)
        elif questDataId == const.QD_MONSTER_KILL:
            self._showKillMonsterMsg(exData)

    def isQuestTracked(self, questId):
        if not questId:
            return False
        return self.getQuestData(questId, const.QD_QUEST_TRACKED) or commQuest.getJobIdByQuest(questId)

    def fetchAllTrackedQuest(self):
        quests = [ questId for questId in self.quests if self.isQuestTracked(questId) ]
        questLoops = {qld:[] for qld in self.questLoopInfo if self.isQuestTracked(self.questLoopInfo[qld].getCurrentQuest())}
        questInfo = commQuest.getQuestInfo(self, quests, quests, questLoops, questLoops)
        uLoopTasks = [ self.questLoopInfo[qld].getCurrentQuest() for qld in questInfo['unfinished_taskLoops'] ]
        cLoopTasks = [ self.questLoopInfo[qld].getCurrentQuest() for qld in questInfo['complete_taskLoops'] ]
        questInfo['unfinished_tasks'].extend(uLoopTasks)
        questInfo['complete_tasks'].extend(cLoopTasks)
        self.onFetchQuestTrackInfo(questInfo)

    def showQuestTrackWindow(self):
        pass

    def updateQuestDisplay(self, questNpcIds):
        for questNpcId in questNpcIds:
            questNpc = BigWorld.entities.get(questNpcId)
            if questNpc is None:
                continue
            if QNR.data.has_key(questNpc.npcId):
                acQuests = QNR.data[questNpc.npcId].get('acQuests', ())
                comQuests = QNR.data[questNpc.npcId].get('comQuests', ())
                acQuestLoops = QNR.data[questNpc.npcId].get('acQuestGroups', {})
                comQuestLoops = QNR.data[questNpc.npcId].get('comQuestGroups', ())
            else:
                acQuests = ()
                comQuests = ()
                acQuestLoops = {}
                comQuestLoops = {}
            questInfo = commQuest.getQuestInfo(self, acQuests, comQuests, acQuestLoops, comQuestLoops, questNpc.npcId)
            questNpc.onUpdateQuestDisplay(questInfo)

    def updateQuestDisplayFromCache(self, questNpcIds):
        for questNpcId in questNpcIds:
            questNpc = BigWorld.entities.get(questNpcId)
            if questNpc is None:
                continue
            questInfo = {'available_tasks': [],
             'unfinished_tasks': [],
             'complete_tasks': [],
             'complete_extra_tasks': [],
             'available_taskLoops': [],
             'unfinished_taskLoops': [],
             'complete_taskLoops': [],
             'complete_extra_taskLoops': []}
            if QNR.data.has_key(questNpc.npcId):
                acQuests = QNR.data[questNpc.npcId].get('acQuests', ())
                for questId in acQuests:
                    if questId in self.questInfoCache['available_tasks']:
                        questInfo['available_tasks'].append(questId)

                comQuests = QNR.data[questNpc.npcId].get('comQuests', ())
                for questId in comQuests:
                    if questId in self.questInfoCache['unfinished_tasks']:
                        questInfo['unfinished_tasks'].append(questId)
                    if questId in self.questInfoCache['complete_tasks']:
                        questInfo['complete_tasks'].append(questId)

                acQuestLoops = QNR.data[questNpc.npcId].get('acQuestGroups', {})
                for questLoopId in acQuestLoops.keys():
                    if questLoopId in self.questInfoCache['available_taskLoops']:
                        for questId in acQuestLoops[questLoopId]:
                            if commQuest.gainQuestLoopCheck(self, questLoopId, bMsg=False, npcNo=questNpc.npcId):
                                questInfo['available_taskLoops'].append(questLoopId)
                                break

                comQuestLoops = QNR.data[questNpc.npcId].get('comQuestGroups', {})
                for questLoopId in comQuestLoops.keys():
                    if questLoopId in self.questInfoCache['unfinished_taskLoops']:
                        for questId in self.quests:
                            if questId in comQuestLoops[questLoopId]:
                                questInfo['unfinished_taskLoops'].append(questLoopId)
                                break

                    if questLoopId in self.questInfoCache['complete_taskLoops']:
                        for questId in self.quests:
                            if questId in comQuestLoops[questLoopId]:
                                if not self.checkQuestNpc(questId, questNpc.npcId):
                                    continue
                                questInfo['complete_taskLoops'].append(questLoopId)
                                break

            questNpc.onUpdateQuestDisplay(questInfo)

    def checkQuestNpc(self, questId, npcId):
        comQuestId = self.getQuestData(questId, const.QD_COMPNPC, 0)
        if not comQuestId:
            return True
        return comQuestId == npcId

    def fetchAvailableQuestsByType(self, displayType):
        aqsDict = SCD.data.get('alphaQuestServerList', {})
        questsInfo = self.questInfoCache
        res = []
        for questId in questsInfo['available_tasks']:
            td = QD.data.get(questId, None)
            if td.get('displayType') == gametypes.QUEST_DISPLAY_TYPE_HIDE:
                continue
            if td.get('displayType') == displayType:
                if td.get('rolecard', None) and formula.getMapId(self.spaceNo) not in td.get('rolecard', None):
                    continue
                alphaFlag = td.get('alphaFlag', 0)
                aqsList = aqsDict.get(alphaFlag, ())
                showAlpha = gameglobal.rds.g_serverid in aqsList
                if alphaFlag and not showAlpha:
                    continue
                res.append({'questId': questId,
                 'isLoop': False})

        for questLoopId in questsInfo['available_taskLoops']:
            firstQuestId = self.getLoopNpc(questLoopId)
            if firstQuestId:
                qd = QD.data.get(firstQuestId, {})
                if qd.get('rolecard', None) and formula.getMapId(self.spaceNo) not in qd.get('rolecard', None):
                    continue
                    alphaFlag = qd.get('alphaFlag', 0)
                    aqsList = aqsDict.get(alphaFlag, ())
                    showAlpha = gameglobal.rds.g_serverid in aqsList
                    if alphaFlag and not showAlpha:
                        continue
                if qd.get('displayType', 0) == displayType:
                    res.append({'questId': questLoopId,
                     'isLoop': True})
            else:
                continue

        return res

    def fetchAvailableQuests(self):
        aqsDict = SCD.data.get('alphaQuestServerList', {})
        questsInfo = self.questInfoCache
        res = []
        for questId in questsInfo['available_tasks']:
            td = QD.data.get(questId, None)
            if td.get('displayType') == gametypes.QUEST_DISPLAY_TYPE_HIDE:
                continue
            if td == None:
                continue
            if td.get('rolecard', None) and formula.getMapId(self.spaceNo) not in td.get('rolecard', None):
                continue
            alphaFlag = td.get('alphaFlag', 0)
            aqsList = aqsDict.get(alphaFlag, ())
            showAlpha = gameglobal.rds.g_serverid in aqsList
            if alphaFlag and not showAlpha:
                continue
            res.append((questId, {'expBonus': 0,
              'cashBonus': 0}))

        loopRes = []
        for questLoopId in questsInfo['available_taskLoops']:
            firstQuestId = self.getLoopNpc(questLoopId)
            if firstQuestId:
                qd = QD.data.get(firstQuestId, {})
                if qd.get('rolecard', None) and formula.getMapId(self.spaceNo) not in qd.get('rolecard', None):
                    continue
                alphaFlag = qd.get('alphaFlag', 0)
                aqsList = aqsDict.get(alphaFlag, ())
                showAlpha = gameglobal.rds.g_serverid in aqsList
                if alphaFlag and not showAlpha:
                    continue
            else:
                continue
            loopRes.append((questLoopId, {'expBonus': 0,
              'cashBonus': 0}))

        gameglobal.rds.ui.questLog.setQuestList(res, loopRes)

    def _addBoxFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('questBox'):
            questBox = data['questBox']
            self._realAddFx(questBox, 'npcId', NMCD.data)

    def _addMarkFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('markerNpcs'):
            markerNpc = list(data['markerNpcs'])
            l = len(markerNpc)
            for i in xrange(l - 1, -1, -1):
                npcId = markerNpc[i]
                qmd = QMD.data.get(npcId, {})
                needRemove = False
                markerInfo, _ = self.getQuestData(questId, const.QD_QUEST_MARKER, ({}, None))
                needRemove = markerInfo and markerInfo.get(npcId, 1) > 0
                if qmd.has_key('useItems') and not needRemove:
                    useItems = qmd['useItems']
                    for itemId, cnt in useItems:
                        amount = self.questBag.countItemInPages(itemId)
                        if amount < cnt:
                            needRemove = True
                            break

                if needRemove:
                    markerNpc.remove(npcId)

            self._realAddFx(markerNpc, 'npcId', NMCD.data)

    def _addMonsterFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('markerMonsters'):
            markerMonsters = data['markerMonsters']
            self._realAddFx(markerMonsters, 'charType', MMCD.data)

    def _addDebateFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('debateNpc'):
            debateNpc = data['debateNpc']
            self._realAddFx(debateNpc, 'npcId', NMCD.data)

    def _addJobMarkFx(self, questId):
        ents = BigWorld.entities.values()
        for en in ents:
            if en.inWorld and hasattr(en, 'npcId'):
                if QMD.data.has_key(en.npcId):
                    if questId in QMD.data[en.npcId].get('needAcceptQuests', []):
                        nmcd = NMCD.data.get(en.npcId, {})
                        if nmcd.get('triggerEff', None):
                            eff = nmcd['triggerEff']
                            effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                            if eff not in en.attachFx:
                                fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (en.getBasicEffectLv(),
                                 en.getBasicEffectPriority(),
                                 en.model,
                                 eff,
                                 sfx.EFFECT_UNLIMIT))
                                if fxs:
                                    for fx in fxs:
                                        fx.scale(effScale, effScale, effScale)

                                    en.addFx(eff, fxs)

    def _addChatFx(self, questId):
        chaterInfo = self.getQuestData(questId, const.QD_QUEST_CHAT, {})
        chaterInfo = [ npcId for npcId, isTriggered in chaterInfo.iteritems() if not isTriggered ]
        self._realAddFx(chaterInfo, 'npcId', NMCD.data)

    def _upateChatFx(self, questIds):
        ents = BigWorld.entities.values()
        for questId in questIds:
            chaterInfo = self.getQuestData(questId, const.QD_QUEST_CHAT, {})
            for en in ents:
                npcId = None
                if hasattr(en, 'npcId'):
                    npcId = en.npcId
                if en.inWorld and npcId in chaterInfo.keys() and chaterInfo[npcId]:
                    nmcd = NMCD.data.get(npcId, {})
                    if nmcd.get('triggerEff', None):
                        en.removeFx(nmcd['triggerEff'])

    def _addFunNpcFx(self, questId):
        monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
        if not monsterInfo:
            return
        npcList = []
        for mType in monsterInfo:
            killNum = monsterInfo.get(mType, 0)
            if not killNum:
                funNpcInfo = self.getQuestData(questId, const.QD_QUEST_QIECUO, {})
                if mType in funNpcInfo:
                    npcList.append(funNpcInfo[mType])

        if npcList:
            self._realAddFx(npcList, 'npcId', NMCD.data)

    def _updateFunNpcFx(self, exData):
        ents = BigWorld.entities.values()
        questIds = exData.get('questIds', [])
        mType = exData.get('mType', None)
        for questId in questIds:
            monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
            killNum = monsterInfo.get(mType, 0)
            if not killNum:
                continue
            funNpcInfo = self.getQuestData(questId, const.QD_QUEST_QIECUO, {})
            for en in ents:
                npcId = None
                if hasattr(en, 'npcId'):
                    npcId = en.npcId
                if en.inWorld and npcId and mType in funNpcInfo:
                    nmcd = NMCD.data.get(npcId, {})
                    if killNum and npcId == funNpcInfo[mType] and nmcd.get('triggerEff', None):
                        en.removeFx(nmcd['triggerEff'])

    def _realAddFx(self, ids, idType, data):
        eff = {}
        if not isinstance(ids, list) and not isinstance(ids, tuple):
            ids = (ids,)
        for id in ids:
            nmcd = data.get(id, {})
            if nmcd.get('triggerEff', None):
                effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                eff[id] = (nmcd['triggerEff'], effScale)

        if eff:
            ents = BigWorld.entities.values()
            for en in ents:
                id = getattr(en, idType, 0)
                if en.inWorld and id in eff and eff[id][0] not in en.attachFx:
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (en.getBasicEffectLv(),
                     en.getBasicEffectPriority(),
                     en.model,
                     eff[id][0],
                     sfx.EFFECT_UNLIMIT))
                    effScale = eff[id][1]
                    if fxs:
                        for fx in fxs:
                            fx.scale(effScale, effScale, effScale)

                        en.addFx(eff[id][0], fxs)

    def _removeBoxFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('questBox'):
            questBox = data['questBox']
            self._realRemoveFx(questBox, 'npcId', NMCD.data)

    def _removeMarkFx(self, questId):
        data = QD.data.get(questId, None)
        if data:
            if data.has_key('markerNpcs'):
                self._realRemoveFx(data['markerNpcs'], 'npcId', NMCD.data)
            elif data.has_key('markerNpcsGroup'):
                markerNpcsGroup = data.get('markerNpcsGroup', [])
                for group in markerNpcsGroup:
                    qmgd = QMGD.data.get(group, {})
                    self._realRemoveFx(qmgd['markerList'], 'npcId', NMCD.data)

    def _removeDebateFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('debateNpc'):
            self._realRemoveFx(data['debateNpc'], 'npcId', NMCD.data)

    def _removeChatFx(self, questId):
        chater = []
        chaterInfo = self.getQuestData(questId, const.QD_QUEST_CHAT, {})
        if chaterInfo:
            chater = chaterInfo.keys()
        else:
            data = QD.data.get(questId, None)
            if data and data.has_key('needDialog'):
                chater = data['needDialog']
        self._realRemoveFx(chater, 'npcId', NMCD.data)

    def _removeFunNpcFx(self, questId):
        monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
        if not monsterInfo:
            return
        npcList = []
        for mType in monsterInfo:
            killNum = monsterInfo.get(mType, 0)
            if killNum:
                funNpcInfo = self.getQuestData(questId, const.QD_QUEST_QIECUO, {})
                if mType in funNpcInfo:
                    npcList.append(funNpcInfo[mType])

        if npcList:
            self._realRemoveFx(npcList, 'npcId', NMCD.data)

    def _removeMonsterFx(self, questId):
        data = QD.data.get(questId, None)
        if data and data.has_key('markerMonsters'):
            self._realRemoveFx(data['markerMonsters'], 'charType', MMCD.data)

    def _removeJobMarkFx(self, questId):
        ents = BigWorld.entities.values()
        for en in ents:
            if en.inWorld and hasattr(en, 'npcId'):
                if QMD.data.has_key(en.npcId):
                    if questId in QMD.data[en.npcId].get('needAcceptQuests', []):
                        nmcd = NMCD.data.get(en.npcId, {})
                        if nmcd.get('triggerEff', None):
                            eff = nmcd['triggerEff']
                            en.removeFx(eff)

    def _realRemoveFx(self, ids, idType, data):
        eff = {}
        if not isinstance(ids, list) and not isinstance(ids, tuple):
            ids = (ids,)
        for id in ids:
            nmcd = data.get(id, {})
            if nmcd.get('triggerEff', None):
                effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                eff[id] = (nmcd['triggerEff'], effScale)

        if eff:
            ents = BigWorld.entities.values()
            for en in ents:
                id = getattr(en, idType, 0)
                if en.inWorld and id in eff:
                    en.removeFx(eff[id][0])

    def showQuestWindow(self, npcId):
        questNpc = BigWorld.entities.get(npcId)
        if questNpc is None:
            return
        else:
            qnr = QNR.data.get(questNpc.npcId, {})
            acQuests = qnr.get('acQuests', ())
            comQuests = qnr.get('comQuests', ())
            acQuestLoops = qnr.get('acQuestGroups', {})
            comQuestLoops = qnr.get('comQuestGroups', {})
            questInfo = commQuest.getQuestInfo(self, acQuests, comQuests, acQuestLoops, comQuestLoops, questNpc.npcId)
            questInfo = self._genBonusInfoInQuestInfo(questInfo)
            self.onShowQuestWindow(questInfo, npcId)
            return

    def autoCompleteQuestLoop(self, entId):
        questNpc = BigWorld.entities.get(entId)
        if questNpc is None:
            return False
        else:
            qnr = QNR.data.get(questNpc.npcId, {})
            comQuestLoops = qnr.get('comQuestGroups', {})
            autoQuestLoopId = 0
            for questLoopId in comQuestLoops:
                if QLD.data.get(questLoopId, {}).get('auto', 0):
                    autoQuestLoopId = questLoopId
                    break

            if autoQuestLoopId:
                questInfo = commQuest.getQuestInfo(self, (), (), {}, {autoQuestLoopId: comQuestLoops[autoQuestLoopId]}, questNpc.npcId)
                if questInfo['complete_taskLoops']:
                    self.onShowQuestWindow(questInfo, entId)
                    return True
            return False

    def _genBonusInfoInQuestInfo(self, questInfo):
        questReward = []
        for questId in questInfo['available_tasks']:
            totalExp, cashBonus, socExp, _ = commQuest.calcReward(self, questId)
            questReward.append((questId, (totalExp,
              cashBonus,
              socExp,
              [])))

        questInfo['available_tasks'] = questReward
        questLoopReward = []
        for questLoopId in questInfo['available_taskLoops']:
            qld = QLD.data.get(questLoopId, {})
            randType = qld.get('ranType', gametypes.QUEST_LOOP_SELECT_SEQUENCE)
            displayType = qld.get('displayType', 0)
            cashBonus = 0
            totalExp = 0
            socExp = 0
            xieWeiExp = 0
            fames = []
            if randType != gametypes.QUEST_LOOP_SELECT_SEQUENCE:
                for item in qld.get('bonusInfo', ()):
                    if item[0] == const.LOOP_QUEST_MONEY:
                        cashBonus = item[1]
                    elif item[0] == const.LOOP_QUEST_EXP:
                        totalExp = item[1]
                    elif item[0] == const.LOOP_QUEST_XIUWEI:
                        xieWeiExp = item[1]
                    elif item[0] == const.LOOP_QUEST_FAME and displayType == gametypes.QUEST_DISPLAY_TYPE_SCHOOL_DAILY:
                        fames.append(item[1:])

            else:
                if questLoopId in self.questLoopInfo:
                    questIds = self.questLoopInfo[questLoopId].getNextQuests(self)
                else:
                    questIds = commQuest.getAvaiNextQuestsInLoop(self, questLoopId, 0)
                if len(questIds) > 0:
                    questId = questIds[0]
                    totalExp, cashBonus, socExp, _ = commQuest.calcReward(self, questId, questLoopId)
                    if self._isFirstClueQuest(questId, questLoopId):
                        for item in qld.get('bonusInfo', ()):
                            if item[0] == const.LOOP_QUEST_MONEY:
                                cashBonus = item[1]
                            elif item[0] == const.LOOP_QUEST_EXP:
                                totalExp = item[1]

            questLoopReward.append((questLoopId, (totalExp,
              cashBonus,
              socExp,
              fames)))

        questInfo['available_taskLoops'] = questLoopReward
        return questInfo

    def _isFirstClueQuest(self, questId, questLoopId):
        displayType = QD.data.get(questId, {}).get('displayType')
        qld = QLD.data.get(questLoopId, {})
        if displayType == gametypes.QUEST_DISPLAY_TYPE_CLUE:
            if questId == qld.get('quests', [0])[0]:
                return True
        return False

    def autoServerShowQuestWindow(self, questId, npcId, isAccept):
        questInfo = {'available_tasks': [],
         'unfinished_tasks': [],
         'complete_tasks': [],
         'available_taskLoops': [],
         'unfinished_taskLoops': [],
         'complete_taskLoops': []}
        questReward = []
        totalExp, cashBonus, socExp, _ = commQuest.calcReward(self, questId)
        questReward.append((questId, (totalExp, cashBonus)))
        if isAccept:
            questInfo['available_tasks'] = questReward
        else:
            questInfo['complete_tasks'] = (questId,)
        questOpen = QD.data.get(questId, {}).get('afterDialogOpen', uiConst.QUEST_OPEN_SMALL)
        self.onAutoShowQuestWindow(questInfo, npcId, isAccept, questOpen)

    def onAutoShowQuestWindow(self, questInfo, npcId, isAccept = True, questOpen = uiConst.QUEST_OPEN_SMALL):
        questNpcId = 0
        res = {'available_tasks': [],
         'unfinished_tasks': [],
         'complete_tasks': [],
         'available_taskLoops': [],
         'unfinished_taskLoops': [],
         'complete_taskLoops': [],
         'chat': '',
         'ignoreButton': True}
        hasDialog = False
        for questId, reward in questInfo['available_tasks']:
            chatId = QD.data[questId].get('afterAcDialog', 0)
            if chatId:
                quest = {'id': questId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': chatId,
                 'words': self._getDialog(QDD.data[chatId]['chat'], questId),
                 'aside': QDD.data[chatId]['aside'],
                 'interval': QDD.data[chatId].get('interval', []),
                 'speaker_ids': self._getSpeakIds(chatId, npcId),
                 'speakEvents': QDD.data[chatId].get('speakEvent', None),
                 'overTaken_tasks': QD.data[questId].get('acPreQst', ()),
                 'expBonus': reward[0],
                 'goldBonus': reward[1],
                 'rewardItems': commQuest.genQuestRewardItems(self, questId),
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                res['available_tasks'].append(quest)
                hasDialog = True

        for questId in questInfo['complete_tasks']:
            chatId = QD.data[questId].get('afterSucDialog', 0)
            if chatId:
                quest = {'id': questId,
                 'questNpcId': questNpcId,
                 'name': QD.data[questId].get('name', ''),
                 'chatId': chatId,
                 'words': self._getDialog(QDD.data[chatId]['chat'], questId),
                 'aside': QDD.data[chatId]['aside'],
                 'interval': QDD.data[chatId].get('interval', []),
                 'speaker_ids': self._getSpeakIds(chatId, npcId),
                 'speakEvents': QDD.data[chatId].get('speakEvent', None),
                 'rewardItems': commQuest.genQuestRewardItems(self, questId),
                 'rewardChoice': commQuest.genQuestRewardChoice(self, questId),
                 'groupHeaderItems': commQuest.genGroupHeaderRewardItems(self, questId),
                 'displayType': QD.data.get(questId, {}).get('displayType', gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN)}
                res['complete_tasks'].append(quest)
                hasDialog = True

        if hasDialog:
            if questOpen == uiConst.QUEST_OPEN_SMALL:
                target = None
                if npcId:
                    entities = BigWorld.entities.values()
                    for entity in entities:
                        if getattr(entity, 'npcId', 0) == npcId:
                            target = entity
                            break

                gameglobal.rds.ui.autoQuest.openQuestWindow(res, target, isAccept, True)
            elif gameglobal.rds.configData.get('enableNpcV2', False) and not gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.npcV2.showQuest(res, None)
            else:
                gameglobal.rds.ui.quest.openQuestWindow(res, None)

    def fetchQuestsInfoByNpcs(self, npcIds):
        acQuests = []
        acQuestLoops = {}
        for npcId in npcIds:
            if not QNR.data.has_key(npcId):
                continue
            qnr = QNR.data[npcId]
            for questId in qnr.get('acQuests', []):
                if questId not in acQuests:
                    acQuests.append(questId)

            for questLoopId in qnr.get('acQuestGroups', {}):
                if not acQuestLoops.has_key(questLoopId):
                    acQuestLoops[questLoopId] = []

        comQuests = [ x for x in self.quests ]
        comQuestLoops = {}
        for questLoopId in self.questLoopInfo.keys():
            comQuestLoops[questLoopId] = []

        questsInfo = commQuest.getQuestInfo(self, acQuests, comQuests, acQuestLoops, comQuestLoops)
        return questsInfo

    def fetchQuestsInfo(self):
        seq = self.lv / ImpQuest.QUEST_INTERVAL
        questInfo = QAD.data.get(seq, [])
        acQuests = [ x[0] for x in questInfo if not self.getQuestFlag(x[0]) ]
        comQuests = [ x for x in self.quests ]
        acQuestLoops = {}
        for questLoopId in QLAD.data[seq]:
            if questLoopId in self.questLoopInfo.keys() and self.questLoopInfo[questLoopId].getCurrentQuest():
                continue
            acQuestLoops[questLoopId] = []

        comQuestLoops = {}
        for questLoopId in self.questLoopInfo.keys():
            comQuestLoops[questLoopId] = []

        self.questInfoCache = commQuest.getQuestInfo(self, acQuests, comQuests, acQuestLoops, comQuestLoops)
        return self.questInfoCache

    def hideQuestNpc(self, npcId, monsterCnt):
        self.hideNpcs[npcId] = monsterCnt
        for entity in BigWorld.entities.values():
            if hasattr(entity, 'npcId') and entity.npcId == npcId:
                entity.refreshOpacityState()

    def hideQuestNpcByMonster(self, npcId):
        self.hideNpcs.setdefault(npcId, 0)
        self.hideNpcs[npcId] += 1
        for entity in BigWorld.entities.values():
            if hasattr(entity, 'npcId') and entity.npcId == npcId:
                entity.refreshOpacityState()

    def onQuestMonsterKilled(self, npcId):
        if self.hideNpcs.has_key(npcId):
            self.hideNpcs[npcId] -= 1
            if self.hideNpcs[npcId] == 0:
                del self.hideNpcs[npcId]
                for entity in BigWorld.entities.values():
                    if hasattr(entity, 'npcId') and entity.npcId == npcId:
                        entity.refreshOpacityState()

    def _genLoopInfo(self, questLoopId):
        maxLoop = QLD.data.get(questLoopId, {}).get('groupNum', 0)
        maxLoopCnt = QLD.data.get(questLoopId, {}).get('maxLoopCnt', 0)
        hideLoopCnt = QLD.data.get(questLoopId, {}).get('hideLoopCnt', 0)
        p = BigWorld.player()
        info = p.questLoopInfo.get(questLoopId, None)
        isDelegetion = QDID.data.has_key(questLoopId)
        if info:
            if info.getCurrentQuest():
                curLoop = info.getCurrentStep() + 1
            else:
                curLoop = info.getCurrentStep()
            curLoopCnt = info.loopCnt + 1
        else:
            curLoop = 0
            curLoopCnt = 1
        if isDelegetion:
            ret = gameStrings.TEXT_IMPQUEST_4119 % (curLoop, maxLoop)
        elif hideLoopCnt:
            ret = gameStrings.TEXT_IMPQUEST_4121 % (curLoop, maxLoop)
        elif maxLoopCnt == const.ENDLESS_LOOP_CNT:
            ret = gameStrings.TEXT_IMPQUEST_4123 % (curLoop, maxLoop, curLoopCnt)
        else:
            ret = gameStrings.TEXT_IMPQUEST_4125 % (curLoop,
             maxLoop,
             curLoopCnt,
             maxLoopCnt)
        return ret

    def questMarkerTriggered(self, markerNpcId, npcEntId):
        npc = BigWorld.entity(npcEntId)
        if npc:
            nmcd = NMCD.data.get(markerNpcId, None)
            if nmcd and nmcd.has_key('triggerEff'):
                npc.removeFx(nmcd['triggerEff'])
        if QMD.data.has_key(markerNpcId):
            qmd = QMD.data[markerNpcId]
            if qmd.has_key('itemGain'):
                itemList = []
                for itemId, amount in qmd['itemGain']:
                    itemList.append(itemId)

                self.onQuestAward(itemList)
            if qmd.has_key('comMsg'):
                msgId = qmd['comMsg']
                self.showGameMsg(msgId, ())

    def responseToPlayer(self, npcId, actionId, faceTo, showDlg):
        gamelog.debug('responseToPlayer', npcId, actionId, faceTo, showDlg)
        npc = BigWorld.entity(npcId)
        actionId = str(actionId)
        delayTime = 0.0
        if faceTo:
            npc.faceTo(self)
            delayTime += 0.1
        if actionId and actionId in npc.fashion.getActionNameList():
            act = npc.model.action(actionId)
            act(delayTime, None, 0)
            delayTime += act.duration
        if showDlg:
            BigWorld.callback(delayTime, npc.use)

    def beSharedQuest(self, ownerId, questId):
        owner = BigWorld.entities.get(ownerId)
        qd = QD.data.get(questId, {})
        if owner:
            self.showGameMsg(GMDD.data.SHARE_QUEST, (owner.roleName, qd.get('name', '')))
        gameglobal.rds.ui.taskShare.show(ownerId, questId)

    def _getQuestMonserInfoByQuestId(self, questId, res):
        gamelog.debug('@zsquest _getQuestMonserInfoByQuestId1', res)
        if not self.questData.has_key(questId):
            return res
        else:
            qd = QD.data.get(questId, None)
            if qd == None:
                return {}
            needMonsters = qd.get('needMonsters', ())
            monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
            for mType, numNeed in needMonsters:
                curNum = monsterInfo.get(mType, 0)
                if curNum < numNeed:
                    res.setdefault(mType, set()).add(questId)

            if QD.data.get(questId, {}).has_key('monsterDropItems'):
                dropItems = QD.data[questId]['monsterDropItems']
                items = commQuest.getCompItemCollect(self, qd)
                for itemId, mType, _ in dropItems:
                    curCnt = self.questCountItem(questId, itemId)
                    itemNeed = -1
                    for item, cnt in items:
                        if item == itemId:
                            itemNeed = cnt
                            break

                    if itemNeed != -1 and curCnt < itemNeed:
                        res.setdefault(mType, set()).add(questId)

            gamelog.debug('@zsquest _getQuestMonserInfoByQuestId2', res)
            return res

    def _getQuestMonsterInfo(self):
        gamelog.debug('@zsquest _getQuestMonsterInfo1', self.questMonsterInfo)
        res = {}
        if not hasattr(self, 'questData'):
            return res
        quests = [ x for x in self.quests ]
        for questId in quests:
            res = self._getQuestMonserInfoByQuestId(questId, res)

        gamelog.debug('@zsquest _getQuestMonsterInfo2', quests, res)
        return res

    def _removeQuestMonsterByQuestId(self, questId):
        gamelog.debug('@zsquest _removeQuestMonsterByQuestId1', questId, self.questMonsterInfo)
        if not self.questData.has_key(questId):
            return
        qd = self.questData[questId]
        removeMonsterTypes = []
        if qd.has_key(const.QD_MONSTER_KILL):
            for mType in qd[const.QD_MONSTER_KILL].keys():
                self._removeQuestMonster(mType, questId)
                removeMonsterTypes.append(mType)

        if QD.data.get(questId, {}).has_key('monsterDropItems'):
            dropItems = QD.data[questId]['monsterDropItems']
            for _, mType, _ in dropItems:
                self._removeQuestMonster(mType, questId)
                removeMonsterTypes.append(mType)

        gameglobal.rds.ui.refreshQuestIcon(removeMonsterTypes, False)
        gamelog.debug('@zsquest _removeQuestMonsterByQuestId2', questId, self.questMonsterInfo)

    def _updateQuestMonsterLogo(self):
        if self.targetLocked and self.targetLocked.IsMonster:
            m = self.targetLocked
            if getattr(m, 'charType', None):
                if m.charType in self.questMonsterInfo.keys():
                    gameglobal.rds.ui.target.updateQuestMonsterLogo(True)
                else:
                    gameglobal.rds.ui.target.updateQuestMonsterLogo(False)
        if self.optionalTargetLocked and self.optionalTargetLocked.IsMonster:
            m = self.optionalTargetLocked
            if getattr(m, 'charType', None):
                if m.charType in self.questMonsterInfo.keys():
                    gameglobal.rds.ui.subTarget.updateQuestMonsterLogo(True)
                else:
                    gameglobal.rds.ui.subTarget.updateQuestMonsterLogo(False)

    def _updateQuestMonsterInfoByItemClt(self, itemId):
        gamelog.debug('@zsquest _updateQuestMonsterInfoByItemClt1', itemId, self.questMonsterInfo)
        for questId in self.quests:
            curCnt = self.questCountItem(questId, itemId)
            qd = QD.data.get(questId, None)
            if not qd:
                continue
            monsterDropItems = qd.get('monsterDropItems', None)
            if monsterDropItems == None:
                return
            for itemIdDrop, mType, _ in monsterDropItems:
                if itemIdDrop != itemId:
                    continue
                items = commQuest.getCompItemCollect(self, qd)
                itemNeed = -1
                for item, cnt in items:
                    if item == itemId:
                        itemNeed = cnt
                        break

                if itemNeed == -1:
                    continue
                if curCnt >= itemNeed:
                    self._removeQuestMonster(mType, questId)
                    gameglobal.rds.ui.refreshQuestIcon([mType], False)

        gamelog.debug('@zsquest _updateQuestMonsterInfoByItemClt2', itemId, self.questMonsterInfo)

    def _updateQuestMonsterInfoByKillMonster(self, mType):
        for questId in self.quests:
            qd = QD.data.get(questId, None)
            if qd == None:
                continue
            needMonsters = qd.get('needMonsters', None)
            if needMonsters == None:
                continue
            monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
            numNeed = -1
            for monsterType, cnt in needMonsters:
                if mType == monsterType:
                    numNeed = cnt
                    break

            if numNeed == -1:
                continue
            curNum = monsterInfo.get(mType, 0)
            if curNum >= numNeed:
                self._removeQuestMonster(monsterType, questId)
                gameglobal.rds.ui.refreshQuestIcon([monsterType], False)

    def _removeQuestMonster(self, mType, questId):
        gamelog.debug('@zsquest _removeQuestMonster1', mType, questId, self.questMonsterInfo)
        if not self.questMonsterInfo.has_key(mType):
            gamelog.error('@zsquest _removeQuestMonster2', self.questMonsterInfo)
            return
        questSet = self.questMonsterInfo[mType]
        gamelog.debug('@zsquest _removeQuestMonster3', questSet, self.questMonsterInfo)
        if questId in questSet:
            questSet.remove(questId)
        if len(questSet) == 0:
            self.questMonsterInfo.pop(mType)
        gamelog.debug('@zsquest _removeQuestMonster4', questSet, self.questMonsterInfo, questSet)

    def _addQuestMonster(self, mType, questId):
        self.questMonsterInfo.setdefault(mType, set()).add(questId)

    def _updateQuestMonsterInfo(self, questDataId, exData):
        gamelog.debug('@zsquest _updateQuestMonsterInfo1', questDataId, exData, self.questMonsterInfo)
        if not exData:
            return
        if questDataId == const.QD_ITEM_COLLECT:
            itemId = exData['itemId']
            self._updateQuestMonsterInfoByItemClt(itemId)
        elif questDataId == const.QD_MONSTER_KILL:
            mType = exData['mType']
            self._updateQuestMonsterInfoByKillMonster(mType)
        gamelog.debug('@zsquest _updateQuestMonsterInfo2', questDataId, exData, self.questMonsterInfo)

    def useRewardPointOK(self, questLoopId, npcId):
        self.cell.useRewardPoints(questLoopId, npcId)

    def showUseRewardPointConfirm(self, questLoopId, refType, npcId):
        activityId = commActivity.getActivityIdByRef(questLoopId, refType)
        extraPoint = ABD.data.get(activityId, {}).get('extraPoint', 0)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.useRewardPointOK, questLoopId, npcId), True, False), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_IMPQUEST_4383 % extraPoint, buttons)

    def needQuestItems(self, items, questId):
        qd = QD.data.get(questId, {})
        needItems = commQuest.getCompItemCollect(self, qd)
        needItems = dict(needItems)
        if not qd:
            return False
        if self.getQuestData(questId, const.QD_FAIL):
            return False
        if len(items) == 0:
            return True
        for itemId in items:
            itemCnt = self.questCountItem(questId, itemId)
            if needItems.has_key(itemId) and itemCnt < needItems[itemId]:
                return True
            if ID.data.get(itemId, {}).get('holdMax'):
                if Item.isQuestItem(itemId):
                    num = self.questBag.countItemInPages(itemId, includeExpired=True, includeLatch=True)
                else:
                    num = self.realInv.countItemInPages(itemId, includeExpired=True, includeLatch=True)
                if num >= ID.data[itemId]['holdMax']:
                    gamelog.debug('zt: item reach holdMax', itemId, ID.data[itemId]['holdMax'], num)
                    return False
            if self._needJobStats(questId, gametypes.JOB_STATS_ITEM, itemId):
                return True

        return False

    def onQuestAward(self, itemList):
        gameglobal.rds.ui.showSpecialCurve(itemList)

    def onQuestCollect(self, entityId, itemList):
        entity = BigWorld.entities.get(entityId)
        if not entity:
            return
        if not entity.inWorld:
            return
        x, y = clientcom.worldPointToScreen(entity.position)
        itemArr = []
        for itemId in itemList:
            it = Item(itemId)
            if it.isOneQuest():
                itemArr.append([x, y, itemId])

        gameglobal.rds.ui.showCurve(itemArr, uiConst.ITEM_TO_INVENTORY)

    def setQuestScenario(self, scenName):
        self.scenarioAfterTeleport = scenName

    def scenarioPlayAfterTeleport(self):
        if hasattr(self, 'scenarioAfterTeleport') and self.scenarioAfterTeleport:
            BigWorld.worldDrawEnabled(False)
            self.scenarioPlay(self.scenarioAfterTeleport, 0)
            self.scenarioAfterTeleport = None

    def questPlayScenario(self, scenName, questId, bAccept, expBonus):
        self.scenarioPlay(scenName, 0)

    def questCountItem(self, questId, itemId, enableParentCheck = False):
        if Item.isQuestItem(itemId):
            return self.questBag.countItemInPages(itemId, enableParentCheck=enableParentCheck)
        else:
            questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
            if questLoopId:
                qld = QLD.data[questLoopId]
                if qld.get('isCross'):
                    return self.crossInv.countItemInPages(itemId, enableParentCheck=enableParentCheck)
            return self.realInv.countItemInPages(itemId, enableParentCheck=enableParentCheck)

    def _getOrderIdxByName(self, name):
        for key, value in QOD.data.items():
            if name == value.get('name', ''):
                return key

        return 99

    def sortQuestGoal(self, questGoals, questId, isQuestLog = False):
        ret = []
        leftGoals = copy.deepcopy(questGoals)
        orders = QD.data.get(questId, {}).get('questGoalOrder', [])
        needSort = QD.data.get(questId, {}).get('showQuestGoalOrder', 0)
        if needSort:
            for order in orders:
                for goal in questGoals:
                    if self._getOrderIdxByName(goal.get(const.QUEST_GOAL_ORDER, None)) == order:
                        ret.append(goal)
                        if goal in leftGoals:
                            leftGoals.remove(goal)

        for goal in leftGoals:
            ret.append(goal)

        if needSort and not isQuestLog:
            startPos = 0
            type = 0
            for index, goal in enumerate(ret):
                state = goal.get(const.QUEST_GOAL_STATE, False)
                startPos = index
                if not state:
                    type = goal.get(const.QUEST_GOAL_ORDER)
                    break

            endPos = startPos + 1
            for i in range(endPos, len(ret)):
                goal = ret[i]
                if type == goal.get(const.QUEST_GOAL_ORDER):
                    endPos += 1
                else:
                    break

            ret = ret[startPos:endPos]
        return ret

    def showQuestPuzzle(self, puzzleId, answers, puzzleIdx, puzzleCnt):
        if puzzleIdx == 1:
            gameglobal.rds.ui.puzzle.show(puzzleId, answers, puzzleIdx, puzzleCnt)
        else:
            gameglobal.rds.ui.puzzle.refreshPuzzle(puzzleId, answers, puzzleIdx, puzzleCnt)

    def onGetNextQuestPuzzle(self, puzzleIdx, questId):
        if not QD.data.has_key(questId):
            return
        qd = QD.data[questId]
        questMode = qd.get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE)
        if questMode not in gametypes.PUZZLE_MODE_MULTI:
            return
        puzzleInfo = self.getQuestData(questId, const.QD_PUZZLE, {0: 0})
        for idx, key in enumerate(sorted(puzzleInfo.keys())):
            if key and puzzleInfo[key] == const.PUZZLE_EMPTY:
                if puzzleIdx != idx:
                    self.puzzleMsgHandler(gametypes.PUZZLE_MSG_INDEX_ERR)
                    return
                self.cell.filterQuestPuzzle(key, idx + 1, len(puzzleInfo))
                break

    def puzzleMsgHandler(self, msgId):
        if gametypes.PUZZLE_MSG_CONTINUE_ERR == msgId:
            pass
        elif gametypes.PUZZLE_MSG_INDEX_ERR == msgId:
            pass
        elif gametypes.PUZZLE_MSG_ACCEPT_LIMIT == msgId:
            self.showGameMsg(GMDD.data.PUZZLE_MSG_NPC_ACCEPT_LIMIT, ())

    def showQingGongJingSuTime(self, isShow):
        if not gameglobal.rds.ui.qingGongJingSuTime.mediator and isShow == 1:
            gameglobal.rds.ui.qingGongJingSuTime.show()
        else:
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_QING_GONG_JING_SU_TIME, False)
            gameglobal.rds.ui.qingGongJingSuTime.close()

    def getQuestLoopId(self, questId):
        for qId, info in self.questLoopInfo.items():
            if info.getCurrentQuest() == questId:
                return qId

    def getDelegationId(self, questId):
        qloopId = self.getQuestLoopId(questId)
        if qloopId:
            return QDID.data.get(qloopId)

    def qeApplyGroupMatch(self, groupMatchNo, firstLevelMode, secondLevelMode, fbNo):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(GMD.data[GMDD.data.QUEST_APPLY_GROUP_MATCH]['text'], lambda : self.onQEApplyGroupMatch(groupMatchNo, firstLevelMode, secondLevelMode, fbNo))

    def onQEApplyGroupMatch(self, groupMatchNo, firstLevelMode, secondLevelMode, fbNo):
        secondLevelMode = uiUtils.genGroupMatchSecondMode(secondLevelMode)
        if self.isInTeam():
            self.cell.applyGroupMatchOfTeam(gametypes.GROUP_MATCH_CLASS_FB, gametypes.GROUP_MATCH_TYPE_TIE_SANJIAO, (groupMatchNo,
             firstLevelMode,
             secondLevelMode,
             fbNo))
        else:
            self.cell.applyGroupMatchOfPerson(gametypes.GROUP_MATCH_CLASS_FB, gametypes.GROUP_MATCH_TYPE_TIE_SANJIAO, (groupMatchNo,
             firstLevelMode,
             secondLevelMode,
             fbNo))

    def onTriggerMonsterEvent(self, charType, eventIndex, succ):
        try:
            eventData = METD.data[charType][eventIndex]
        except:
            eventData = None

        if not eventData:
            return
        else:
            if succ and eventData.has_key('succMsgId'):
                self.showGameMsg(eventData['succMsgId'], ())
            if not succ and eventData.has_key('failMsgId'):
                self.showGameMsg(eventData['failMsgId'], ())
            return

    def getQuestLv(self, questId, qd):
        if qd.get('lvSelType', gametypes.QUEST_LEVEL_RECOMMEND) == gametypes.QUEST_LEVEL_RECOMMEND:
            lv = qd.get('recLv')
        else:
            lv = self.getQuestData(questId, const.QD_QUEST_LV, self.lv)
        return lv

    def onQuestTrackChanged(self, questId, questType, isTracked):
        if questType == gametypes.QUEST_TYPE_LOOP:
            if QDID.data.has_key(questId):
                gameglobal.rds.ui.delegationBook.onQuestTrackChanged(questId, questType, isTracked)
            if questId in self.questLoopInfo:
                questId = self.questLoopInfo[questId].getCurrentQuest()
            else:
                questId = None
        if questId is None:
            return
        else:
            cEvent = Event(events.EVENT_QUEST_TRACK_CHANGED, {'questId': questId,
             'tracked': isTracked})
            gameglobal.rds.ui.dispatchEvent(cEvent)
            return

    def showChatWindow(self, chatId, questNpcId, callback = None):
        npc = BigWorld.entities.get(questNpcId)
        npcId = None
        if npc and npc.inWorld:
            npcId = npc.npcId
        if npc is None:
            return
        else:
            res = {'complete_tasks': [],
             'chat': '',
             'ignorePanel': True}
            quest = {'id': 0,
             'questNpcId': questNpcId,
             'name': '',
             'chatId': chatId,
             'words': self._getDialog(QDD.data[chatId]['chat']),
             'aside': QDD.data[chatId]['aside'],
             'interval': QDD.data[chatId].get('interval', []),
             'speaker_ids': self._getSpeakIds(chatId, npcId),
             'speakEvents': QDD.data[chatId].get('speakEvent', None),
             'rewardItems': [],
             'rewardChoice': [],
             'displayType': gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN}
            res['complete_tasks'].append(quest)
            if gameglobal.rds.configData.get('enableNpcV2', False) and not gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.npcV2.showQuest(res, npc)
                if callback:
                    gameglobal.rds.ui.npcV2.setCallback(callback)
            else:
                gameglobal.rds.ui.quest.openQuestWindow(res, npc)
                if callback:
                    gameglobal.rds.ui.quest.setCallback(callback)
            return

    def showCarrierChatWindow(self, chatId, npcId = 0):
        res = {'complete_tasks': [],
         'complete_taskLoops': [],
         'available_tasks': [],
         'chat': '',
         'available_taskLoops': [],
         'unfinished_tasks': [],
         'ignoreButton': True,
         'unfinished_taskLoops': []}
        questId = 0
        quest = {'id': questId,
         'questNpcId': 0,
         'name': '',
         'chatId': chatId,
         'words': self._getDialog(QDD.data[chatId]['chat'], questId),
         'aside': QDD.data[chatId]['aside'],
         'interval': QDD.data[chatId].get('interval', []),
         'speaker_ids': self._getSpeakIds(chatId, npcId),
         'speakEvents': [()],
         'overTaken_tasks': (),
         'expBonus': 0,
         'goldBonus': 0,
         'rewardItems': [],
         'rewardChoice': [],
         'groupHeaderItems': [],
         'displayType': gametypes.QUEST_DISPLAY_TYPE_MING_YANG}
        res['available_tasks'] = [quest]
        gameglobal.rds.ui.autoQuest.openQuestWindow(res, None, True, True)

    def showQuestBook(self, questId, bookId):
        gameglobal.rds.ui.book.show(bookId)

    def _warStr(self, info):
        return uiUtils.toHtml(info, '#cc2929')

    def onSharedQuestLoop(self, questLoopId, questId, shareNUID, acStep, extraBonusNUID):
        gamelog.info('@szh onSharedQuestLoop', questLoopId, questId, shareNUID, acStep, extraBonusNUID)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.cell.acceptQuestLoopByShared, questLoopId, questId, acStep, shareNUID, extraBonusNUID, True)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        if not self.questLoopInfo.has_key(questLoopId):
            curStep = 0
        else:
            curStep = self.questLoopInfo[questLoopId].getCurrentStep()
        if acStep > curStep:
            gameglobal.rds.ui.messageBox.show(False, '', self._warStr(gameStrings.TEXT_IMPQUEST_4705) + gameStrings.TEXT_IMPQUEST_4706 % (self._warStr(acStep + 1),
             self._warStr(curStep + 1),
             self._warStr(curStep + 1),
             self._warStr(acStep)), buttons)
        else:
            gameglobal.rds.ui.messageBox.show(False, '', gameStrings.TEXT_IMPQUEST_4709, buttons)
        if QLD.data.get(questLoopId, {}).get('guideMode', 0):
            self.queryTeamGuideQuestStatusWithQid(questId)

    def otherAcceptQuestLoop(self, gbId, questLoopId, bGainQuest):
        if not self._getSortedMembers():
            return
        if not self.memberGuideQuests.has_key(gbId):
            self.memberGuideQuests[gbId] = {}
        self.memberGuideQuests[gbId][questLoopId] = bGainQuest
        self.refreshTeamGuideBuff()

    def onDelegationBusinessQuest(self, res, questLoopId, loopCnt, loopReward):
        gamelog.info('@szh onDelegationBusinessQuest', res, questLoopId, loopCnt, loopReward)
        p = BigWorld.player()
        if res == gametypes.BUSINESS_DGT_SUC:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_SUC, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_LEVEL:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_LEVEL, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_PERSON_PUBLISH_LIMIT:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_PERSON_PUBLISH_LIMIT, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_GUILD_PUBLISH_LIMIT:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_GUILD_PUBLISH_LIMIT, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_PUBLISH_ALREADY:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_PUBLISH_ALREADY, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_NOT_ENOUGH_CASH:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_NOT_ENOUGH_CASH, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_MAX_CASH:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_MAX_CASH, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_MIN_CASH:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_MIN_CASH, ())
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_NO_GUILD:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
        elif res == gametypes.BUSINESS_DGT_FAIL_BY_IN_GUILD_MERGER_STATE:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_FAIL_BY_IN_GUILD_STATE, ())

    def onAcceptBusinessQuestLoop(self, res, questLoopId, dgtNUID):
        gamelog.info('@szh onAcceptBusinessQuestLoop', res, questLoopId, dgtNUID)
        p = BigWorld.player()
        if res == gametypes.BUSINESS_ACCEPT_SUC:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_SUC, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_NO_GUILD:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_DGT_MISS:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_DGT_MISS, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_NO_BUSINESS:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_NO_BUSINESS, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_LV:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_LV, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_SELF:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_SELF, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_MUTEX:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_MUTEX, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_CASH:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_CASH, ())
        elif res == gametypes.BUSINESS_ACCEPT_FAIL_BY_COND_FAIL:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ACCEPT_FAIL_BY_COND_FAIL, ())

    def onAbandonDgtBusinessQuestLoop(self, res, questLoopId, dgtNUID):
        gamelog.info('@szh onAbandonDgtBusinessQuestLoop', res, questLoopId, dgtNUID)
        p = BigWorld.player()
        if res == gametypes.BUSINESS_DGT_ABANDON_SUC:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_ABANDON_SUC, ())
        elif res == gametypes.BUSINESS_DGT_ABANDON_FAIL_BY_NO_GUILD:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
        elif res == gametypes.BUSINESS_DGT_ABANDON_FAIL_BY_DGT_MISS:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_ABANDON_FAIL_BY_DGT_MISS, ())
        elif res == gametypes.BUSINESS_DGT_ABANDON_FAIL_BY_COND_FAIL:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_DGT_ABANDON_FAIL_BY_COND_FAIL, ())

    def onFetchDelegationBusinessQuestLoop(self, businessDgts):
        gamelog.info('@szh onFetchDelegationBusinessQuestLoop', businessDgts, type(businessDgts), dir(businessDgts))
        gameglobal.rds.ui.guildBusinessDelegate.show(businessDgts)

    def pushLoopProgress(self, teamProgressInfo):
        p = BigWorld.player()
        ret = []
        qType = teamProgressInfo.get('type', {})
        options = teamProgressInfo.get('options', {})
        teamInfo = teamProgressInfo.get('teamInfos', {})
        invalidMates = teamProgressInfo.get('invalidMates', {})
        npcId = teamProgressInfo.get('npcId', 0)
        loopId = None
        hasTeamPlayer = False
        teamInfoMsg = ''
        for gbId, player in teamInfo.items():
            isHeader = p.members.get(gbId, {}).get('isHeader', False)
            roleName = p.members.get(gbId, {}).get('roleName', '')
            loopId = player.keys()[0]
            if not isHeader:
                hasTeamPlayer = True
            if roleName in invalidMates[0] or roleName in invalidMates[1]:
                continue
            questName = "<font color= \'#ffcf40\'>%s</font>" % QLD.data.get(loopId, {}).get('name', '')
            times = player.get(loopId, {}).get('loopCnt', 0)
            status = player.get(loopId, {}).get('status')
            maxCount = QLD.data.get(loopId, {}).get('maxLoopCnt', 0)
            statusDesc = self.getStatusDesc(times, status)
            if isHeader:
                teamInfoMsg = '%s %d/%d %s' % (questName,
                 times,
                 maxCount,
                 statusDesc)
            else:
                string = '%s/%s %s' % (times, maxCount, statusDesc)
                ret.append((roleName, string))

        for outOfScopeMate in invalidMates[0]:
            string = gameStrings.TEXT_IMPQUEST_4836
            ret.append((outOfScopeMate, string))

        for outOfScopeMate in invalidMates[1]:
            string = gameStrings.TEXT_IMPQUEST_4840
            ret.append((outOfScopeMate, string))

        if hasTeamPlayer or invalidMates[0] or invalidMates[1]:
            gameglobal.rds.ui.interactiveObjConfirm.setTeamInfo(teamInfoMsg)
            gameglobal.rds.ui.interactiveObjConfirm.setConfirmDetail(ret)
            gameglobal.rds.ui.interactiveObjConfirm.setCallback(Functor(self.onRealQuest, qType, loopId, options, npcId))
            gameglobal.rds.ui.interactiveObjConfirm.show()
        else:
            self.onRealQuest(qType, loopId, options, npcId)

    def getStatusDesc(self, loopCnt, status):
        ret = ''
        if loopCnt:
            if status == gametypes.QUEST_STAGE_ACCEPT:
                ret = gameStrings.TEXT_IMPQUEST_4858
            elif status == gametypes.QUEST_STAGE_COMPLETE:
                ret = gameStrings.TEXT_IMPQUEST_4860
        else:
            ret = gameStrings.TEXT_IMPQUEST_4862
        return ret

    def onRealQuest(self, qType, loopId, options, npcId):
        target = BigWorld.entities.get(npcId)
        if not target:
            return
        if qType == 1:
            target.acceptQuestLoop(loopId)
        elif qType == 2:
            target.completeQuestLoop(loopId, options)

    def onGetHeaderLoopProgress(self, questLoopId, npcId, info, checkStage, extra):
        if not self.inWorld:
            return
        if gameglobal.rds.ui.quest.isShow:
            gameglobal.rds.ui.quest.onGetHeaderLoopProgress(questLoopId, npcId, info, checkStage, extra)
        elif gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.onGetHeaderLoopProgress(questLoopId, npcId, info, checkStage, extra)

    def hideTeamLoopQstTwiceCheckBox(self):
        if gameglobal.rds.ui.quest.isShow:
            gameglobal.rds.ui.quest.hideTwiceCheckBox()
        elif gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.hideTwiceCheckBox()

    def fubenQuestUI(self, questId, isOpen):
        if isOpen:
            gameglobal.rds.ui.fubenQuest.show(questId)
        else:
            gameglobal.rds.ui.fubenQuest.hide()

    def puzzleQuestUI(self, questId):
        if self.hasQuestData(questId, const.QD_PUZZLE):
            puzzles = sorted(self.getQuestData(questId, const.QD_PUZZLE).keys())
            gameglobal.rds.ui.puzzle.questId = questId
            gameglobal.rds.ui.puzzle.intervalTime = QD.data.get(questId, {}).get('intervalTime', 3)
            puzzleTitle = QD.data.get(questId, {}).get('puzzleTitle', '')
            if puzzleTitle:
                gameglobal.rds.ui.puzzle.titleText = puzzleTitle
            self.cell.filterQuestPuzzle(puzzles[0], 1, len(puzzles))

    def completeQuestOnStraightLvUp(self):
        straightLvUpCompleteQuests = SCD.data.get('straightLvUpCompleteQuests', {})
        if not straightLvUpCompleteQuests:
            return
        for questId in straightLvUpCompleteQuests:
            self.completeQuest(questId, True)

    def isQuestMaterialItemCollectComplete(self, questId):
        qd = QD.data[questId]
        if not qd.has_key('compMaterialItemCollectAndConsume'):
            return False
        compItemCollect = qd['compMaterialItemCollectAndConsume']
        for itemId, amount in compItemCollect:
            itemOwn = self.realInv.countItemInPages(itemId, enableParentCheck=True)
            if itemOwn < amount and self.materialBag.getBagItemCount(itemId, enableParentCheck=True) + itemOwn < amount:
                return False

        return True

    def isQuestRandomItemCommitExComplete(self, questId):
        if not self.hasQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_EX):
            return False
        enableQuestMaterialBag = gameglobal.rds.configData.get('enableQuestMaterialBag', False)
        randomItems = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_EX)
        for itemId, cnt in randomItems:
            if Item.isQuestItem(itemId):
                if enableQuestMaterialBag:
                    itemOwn = self.questBag.countItemInPages(itemId, enableParentCheck=True) + self.materialBag.getBagItemCount(itemId, enableParentCheck=True)
                else:
                    itemOwn = self.questBag.countItemInPages(itemId, enableParentCheck=True)
                if itemOwn < cnt:
                    return False
            else:
                if enableQuestMaterialBag:
                    itemOwn = self.realInv.countItemInPages(itemId, enableParentCheck=True) + self.materialBag.getBagItemCount(itemId, enableParentCheck=True)
                else:
                    itemOwn = self.realInv.countItemInPages(itemId, enableParentCheck=True)
                if itemOwn < cnt:
                    return False

        return True

    def questCountMaterialItem(self, itemId):
        return self.realInv.countItemInPages(itemId, enableParentCheck=True) + self.materialBag.getBagItemCount(itemId, enableParentCheck=True)

    def onWorldQuestLoopRefresh(self, info):
        self.currentWorldRefreshQuestInfo = info
        gameglobal.rds.ui.playRecommActivation.updateWorldQuestRefreshFilterDict(info)

    def checkWorldRefreshQuestLoop(self, questLoopId):
        if not gameglobal.rds.configData.get('enableWorldQuestLoopRefresh', False):
            return True
        if self.currentWorldRefreshQuestInfo and WQRD.data.get(self.currentWorldRefreshQuestInfo.get(gametypes.WORLD_QUEST_REFRESH_EXCLUDE, 0), {}).get('para', 0) == questLoopId:
            return True
        info = commQuest.getWorldRefreshQuestGroup(gametypes.WORLD_QUEST_REFRESH_EXCLUDE)
        if info and questLoopId in [ WQRD.data.get(ent, {}).get('para', 0) for ent in info[gametypes.WORLD_QUEST_REFRESH_EXCLUDE] ]:
            return False
        return True

    def isQuestAvailable(self, questId):
        return questId in self.questInfoCache.get('available_tasks', [])

    def isQuestUnfinished(self, questId):
        return questId in self.questInfoCache.get('unfinished_tasks', [])

    def isQuestComplete(self, questId):
        return questId in self.questInfoCache.get('complete_tasks', [])

    def isQuestCompleted(self, questId):
        return self.getQuestFlag(questId)

    def onSendQuestLoopChain(self, dto):
        self.questLoopChain.fromDTO(dto)
        if BigWorld.player().questLoopInfo.get(SCD.data.get('questLoopChainDefault')) is None:
            gameglobal.rds.ui.questTrack.showFindBeastTrack(False)
            gameglobal.rds.ui.findBeastRecover.resetPushed()
        gameglobal.rds.ui.findBeastRecover.pushFindBeastRecoverMsg()
        gameglobal.rds.ui.welfareRewardRecovery.refreshInfo()

    def onGetBackQuestLoopChainExpOK(self):
        gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()
        gameglobal.rds.ui.findBeastRecover.removeFindBeastRecoverMsg()

    def _genSubQuestGoal(self, msg, done, isTrack, trackId, qd, trackType, orderDesc):
        return {const.QUEST_GOAL_DESC: msg,
         const.QUEST_GOAL_STATE: done,
         const.QUEST_GOAL_TRACK: isTrack,
         const.QUEST_GOAL_TRACK_ID: trackId,
         const.QUEST_GOAL_TRACK_TYPE: self._filterTargetTrackType(qd, trackType),
         const.QUEST_GOAL_TYPE: True,
         const.QUEST_GOAL_ORDER: orderDesc}

    def _genMarkerNpcGroupGoal(self, questId, qd, questGoals):
        if self.getQuestData(questId, const.QD_QUEST_MARKER):
            markerInfo, _ = self.getQuestData(questId, const.QD_QUEST_MARKER)
            markerIndex = self.getQuestData(questId, const.QD_QUEST_MARKER_INDEX)
            if not markerIndex:
                return
            for groupId, index in markerIndex:
                qmgd = QMGD.data.get(groupId, {})
                markerId = qmgd.get('markerList')[index]
                markerMsgList = qmgd.get('markerMsgList', [])
                markerTkList = qmgd.get('markerTkList', [])
                msg = ''
                if index < len(markerMsgList):
                    msg = markerMsgList[index]
                curCnt = markerInfo.get(markerId, 0)
                if curCnt == 0:
                    done = False
                else:
                    done = True
                if index < len(markerTkList):
                    isTrack = True
                    if gameglobal.rds.configData.get('enableRandomQuest', False) and qd.has_key('questTkRandom'):
                        trackId = self.getQuestData(questId, const.QD_RANDOM_TKS, {1: (110157086,)}).get(uiConst.RANDOM_QUEST_TYPE, 1)
                        questGoals.append(self._genSubQuestGoal(msg, done, isTrack, trackId, qd, gametypes.TRACK_TYPE_MARKER_NPCS, 'markerNpcs'))
                        break
                    else:
                        trackId = markerTkList[index]
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append(self._genSubQuestGoal(msg, done, isTrack, trackId, qd, gametypes.TRACK_TYPE_MARKER_NPCS, 'markerNpcs'))

    def _genDialogGroupGoal(self, questId, qd, questGoals):
        dialogGroup, _ = qd['needDialogGroup']
        dialogInfo = self.getQuestData(questId, const.QD_QUEST_CHAT)
        dialogIndex = self.getQuestData(questId, const.QD_QUEST_CHAT_INDEX)
        qngd = QNGD.data.get(dialogGroup, {})
        if dialogIndex:
            for index in dialogIndex:
                npcId = qngd.get('npcList')[index]
                npcTkList = qngd.get('npcTkList')
                npcMsgList = qngd.get('npcMsgList')
                cnt = dialogInfo[npcId]
                if cnt > 0:
                    done = True
                else:
                    done = False
                msg = ''
                if index < len(npcMsgList):
                    msg = npcMsgList[index]
                if index < len(npcTkList):
                    isTrack = True
                    trackId = npcTkList[index]
                else:
                    isTrack = False
                    trackId = 0
                questGoals.append(self._genSubQuestGoal(msg, done, isTrack, trackId, qd, gametypes.TRACK_TYPE_NEED_DIALOG, 'needDialog'))

    def _genMonsterGroupGoal(self, questId, qd, questGoals):
        needMonstersGroup = qd.get('needMonstersGroup', 0)
        qmgd = QMOGD.data.get(needMonstersGroup, {})
        monsterList = qmgd.get('monsterList', [])
        monsterMsgList = qmgd.get('monsterMsgList', [])
        monsterTkList = qmgd.get('monsterTkList', [])
        monsterInfo = self.getQuestData(questId, const.QD_MONSTER_KILL, {})
        randomMonstersGroup, randomIndex = self.getQuestData(questId, const.QD_GROUP_MONSTER_INFO, ({}, []))
        needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
        if needMonstersType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY):
            for i, index in enumerate(randomIndex):
                if needMonstersType == const.QUEST_COMPCOND_ANY and i != 0:
                    continue
                mType = monsterList[index][0]
                cnt = randomMonstersGroup.get(mType, 0)
                if not cnt:
                    continue
                name = MD.data[mType]['name']
                if index < len(monsterTkList):
                    isTrack = True
                    trackId = monsterTkList[index]
                else:
                    isTrack = False
                    trackId = 0
                if index < len(monsterMsgList):
                    desc = monsterMsgList[index] + gameStrings.TEXT_IMPQUEST_1939
                else:
                    desc = gameStrings.DESC_NEED_MONSTER
                try:
                    if needMonstersType == const.QUEST_COMPCOND_ANY:
                        killNum = commQuest.getQuestMonsterKillNumCompAny(self, questId)
                    else:
                        killNum = monsterInfo.get(mType, 0)
                    if desc.find('%s') != -1:
                        desc = desc % (name, killNum, cnt)
                    else:
                        desc = desc % (killNum, cnt)
                except:
                    pass

                questGoals.append(self._genSubQuestGoal(desc, commQuest.isQuestMonsterKillComplete(self, questId), isTrack, trackId, qd, gametypes.TRACK_TYPE_NEED_MONSTER, 'needMonsters'))

        elif needMonstersType == const.QUEST_COMPCOND_ALL:
            totalNeed = 0
            count = 0
            for i, index in enumerate(randomIndex):
                mType = monsterList[index][0]
                cnt = randomMonstersGroup.get(mType, 0)
                if not cnt:
                    continue
                if index < len(monsterTkList):
                    isTrack = True
                    trackId = monsterTkList[0]
                else:
                    isTrack = False
                    trackId = 0
                totalNeed = cnt
                count += monsterInfo.get(mType, 0)

            if count > totalNeed:
                count = totalNeed
            desc = monsterMsgList[0] + gameStrings.TEXT_IMPQUEST_1939
            desc = desc % (count, totalNeed)
            questGoals.append(self._genSubQuestGoal(desc, commQuest.isQuestMonsterKillComplete(self, questId), isTrack, trackId, qd, gametypes.TRACK_TYPE_NEED_MONSTER, 'needMonsters'))

    def onAcceptSchoolEntrustQuestLoop(self, msgId, refreshEntrustInfo):
        """
        \xe6\x8e\xa5\xe5\x8f\x96\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x9b\x9e\xe8\xb0\x83
        :param msgId:
        :param refreshEntrustInfo: \xe5\xbd\x93msgId\xe4\xb8\xbaGMDD.data.SCHOOL_ENTRUST_ACCEPT_SUC\xe6\x97\xb6,refreshEntrustInfo\xe4\xb8\xba\xe8\xaf\xa5\xe6\x8e\xa5\xe5\x8f\x96\xe5\xa7\x94\xe6\x89\x98\xe7\xad\x89\xe7\xba\xa7\xe5\x88\xb7\xe6\x96\xb0\xe5\x90\x8e\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x8c\xe5\x8f\x8d\xe4\xb9\x8b\xe4\xb8\xba\xe7\xa9\xba
        :return:
        """
        self.showGameMsg(msgId, ())
        if gameglobal.rds.ui.schoolEntrust.widget:
            gameglobal.rds.ui.schoolEntrust.show(refreshEntrustInfo)
        if msgId == GMDD.data.SCHOOL_ENTRUST_ACCEPT_SUC:
            gameglobal.rds.ui.schoolEntrustBuild.hide()
            gameglobal.rds.ui.schoolEntrust.hide()
        else:
            self.cell.querySchoolEntrustInfo()

    def onQueryAcceptQuestStatus(self, gbId, questLoopId, bHave):
        if not self._getSortedMembers():
            return
        if not self.memberGuideQuests.has_key(gbId):
            self.memberGuideQuests[gbId] = {}
        self.memberGuideQuests[gbId][questLoopId] = bHave
        self.refreshTeamGuideBuff()

    def sendQuestDialog(self, questId, dialogId, index):
        if QD.data.get(questId, {}).get('shareDialog') and self.isInTeam() and self.isHeader():
            qdd = QDD.data.get(dialogId, {})
            if len(qdd.get('npcId', [])) > index:
                msg = qdd.get('chat', [])[index]
                msgContent = self._getDialog(msg, questId)
                npcId = qdd.get('npcId', [])[index]
                self.cell.shareQuestDialog(npcId, msgContent)

    def getAcceptedQuestIds(self):
        questInfo = self.questInfoCache
        questIds = []
        if not questInfo:
            return questIds
        for questId in questInfo['unfinished_tasks']:
            questIds.append(questId)

        for questId in questInfo['complete_tasks']:
            questIds.append(questId)

        for questLoopId in questInfo['complete_taskLoops']:
            if commQuest.isQuestLoopDisable(questLoopId):
                continue
            questId = self.questLoopInfo[questLoopId].getCurrentQuest()
            questIds.append(questId)

        return questIds

    def removeTeamGuideBuff(self):
        teamGuideBuff = SCD.data.get('teamGuideBuff')
        teamGuideMacBuff = SCD.data.get('teamGuideMacBuff')
        self.removeBuffIconByClient(teamGuideBuff)
        self.removeBuffIconByClient(teamGuideMacBuff)

    def refreshTeamGuideBuff(self):
        questIds = self.getAcceptedQuestIds()
        teamGuideBuff = SCD.data.get('teamGuideBuff', 0)
        teamGuideMacBuff = SCD.data.get('teamGuideMacBuff', 0)
        teamGuideTeacherBuff = SCD.data.get('fbQuestTeacherBuffId', 0)
        teamGuideModes = []
        team = self._getSortedMembers()
        for questId in self.quests:
            qd = QD.data.get(questId, {})
            if not qd or commQuest.isQuestDisable(questId):
                continue
            else:
                questIds.append(questId)

        for questId in questIds:
            questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
            if QLD.data.get(questLoopId, {}).get('guideMode', 0):
                for gbId, value in team:
                    if gbId == self.gbId:
                        continue
                    teamGuideModes.append(self.getQuestLoopGuideMode(questLoopId, gbId))

        if const.GUIDE_MASTER_MODE in teamGuideModes or const.GUIDE_TEACHER_MODE in teamGuideModes:
            self.addBuffIconByClient(teamGuideBuff)
        elif const.GUIDE_SAME_MAC_MODE in teamGuideModes:
            self.addBuffIconByClient(teamGuideMacBuff)
        else:
            self.removeTeamGuideBuff()
        if const.GUIDE_TEACHER_MODE in teamGuideModes:
            self.addBuffIconByClient(teamGuideTeacherBuff)
        else:
            self.removeBuffIconByClient(teamGuideTeacherBuff)

    def queryTeamGuideQuestStatusWithQid(self, questId):
        team = self._getSortedMembers()
        if not team:
            return
        questLoop = QLID.data.get(questId, {}).get('questLoop', 0)
        gbIdList = []
        for key, value in team:
            if key == self.gbId:
                continue
            gbIdList.append(key)

        self.cell.queryAcceptQuestStatus(gbIdList, questLoop)

    def queryTeamGuideQuestStatus(self):
        team = self._getSortedMembers()
        if not team:
            return
        if not hasattr(self, 'quests'):
            return
        questIds = self.getAcceptedQuestIds()
        for questId in self.quests:
            qd = QD.data.get(questId, {})
            if not qd or commQuest.isQuestDisable(questId):
                continue
            else:
                questIds.append(questId)

        for questId in questIds:
            questLoop = QLID.data.get(questId, {}).get('questLoop', 0)
            gbIdList = []
            for gbId, value in team:
                if gbId == self.gbId:
                    continue
                gbIdList.append(gbId)

            qld = QLD.data.get(questLoop, {})
            guideMode = qld.get('guideMode', 0)
            if guideMode:
                self.cell.queryAcceptQuestStatus(gbIdList, questLoop)

    def getQuestLoopGuideMode(self, questLoopId, gbId):
        qld = QLD.data[questLoopId]
        guideMode = qld.get('guideMode', 0)
        team = self._getSortedMembers()
        mac = self.members[self.gbId].get('macAddress', '')
        member = None
        for key, value in team:
            if gbId == key:
                member = value

        if not guideMode or not self.groupHeader:
            return const.GUIDE_NONE_MODE
        else:
            teamerLvs = [ x[1]['level'] for x in team if x[1]['isOn'] ]
            length = len(teamerLvs)
            if length == 0:
                return const.GUIDE_NONE_MODE
            guideLowLv = 0
            guideUpLv = 0
            if guideMode == gametypes.QUEST_GUIDE_MODE_NORMAL:
                guideLowLv = qld['guideLowLv']
                guideUpLv = qld['guideThresholdLv']
            elif guideMode == gametypes.QUEST_GUIDE_MODE_AVE_LV:
                totalLv = 0
                for lv in teamerLvs:
                    totalLv += lv

                avgLv = int(totalLv / length)
                guideLowLvFId = qld.get('guideLowLvFId')
                guideUpLvFId = qld.get('guideUpLvFId')
                guideLowLv = formula.calcFormulaById(guideLowLvFId, {'mlLv': avgLv})
                guideUpLv = formula.calcFormulaById(guideUpLvFId, {'mlLv': avgLv})
            elif guideMode == gametypes.QUEST_GUIDE_MODE_RANK_DIFF:
                guideModeLevelDiff = SCD.data.get('guideModeLevelDiff', 1)
                if member.get('level', 0) + guideModeLevelDiff <= self.lv:
                    if self.isApprentice(gbId):
                        if member.get('macAddress', 0) != mac:
                            return const.GUIDE_TEACHER_MODE
                    elif member.get('macAddress', 0) != mac:
                        return const.GUIDE_MASTER_MODE
                else:
                    return const.GUIDE_NONE_MODE
            else:
                return const.GUIDE_NONE_MODE
            if self.lv >= guideUpLv:
                if self.memberGuideQuests.get(gbId, {}).get(questLoopId, False):
                    if member.get('level', 0) <= guideLowLv:
                        if self.isApprentice(gbId):
                            if member.get('macAddress', 0) != mac:
                                return const.GUIDE_TEACHER_MODE
                            else:
                                return const.GUIDE_SAME_MAC_MODE
                        elif member.get('macAddress', 0) != mac:
                            return const.GUIDE_MASTER_MODE
                        else:
                            return const.GUIDE_SAME_MAC_MODE

                else:
                    return const.GUIDE_NONE_MODE
            return const.GUIDE_NONE_MODE

    def checkQuestCompleteMsgBox(self, questLoopId, yesCallback = None):
        qld = QLD.data.get(questLoopId, {})
        if not qld:
            return False
        else:
            msgBoxType = qld.get('msgBoxType', 0)
            if msgBoxType == uiConst.QUEST_COMPLETE_MSG_BOX_TYPE_MENPAI:
                qlVal = self.questLoopInfo.get(questLoopId, None)
                if not qlVal:
                    return False
                loopCnt = qlVal.loopCnt if qlVal else 0
                if loopCnt == 0:
                    return False
                curGroupNum = len(qlVal.questInfo)
                if curGroupNum != 0:
                    return False
                msg, yesBtnText, noBtnText = SCD.data.get('questCompleteMsgBox', {}).get(msgBoxType)
                msg = msg % (loopCnt, qld.get('name', ''))
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=yesCallback, yesBtnText=yesBtnText, noBtnText=noBtnText)
                return True
            return False

    def getUnfinishedQuestNeedItemIdList(self):
        if not gameglobal.rds.configData.get('enableQuestFlagInShop', False):
            return []
        itemIdList = []
        for questId in self.questInfoCache.get('unfinished_tasks', []):
            itemIdList.extend(self.getQuestNeedItemIdListByQuestId(questId))

        for questLoopId in self.questInfoCache.get('unfinished_taskLoops', []):
            if commQuest.isQuestLoopDisable(questLoopId):
                continue
            questId = self.questLoopInfo[questLoopId].getCurrentQuest()
            itemIdList.extend(self.getQuestNeedItemIdListByQuestId(questId))

        return itemIdList

    def getQuestNeedItemIdListByQuestId(self, questId):
        qd = QD.data.get(questId, {})
        if not qd:
            return []
        itemIdList = []
        if not commQuest.enableQuestMaterialBag(self, qd):
            if qd.has_key('compItemCollect'):
                compCondType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
                if compCondType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_ANY, const.QUEST_COMPCOND_EXACT):
                    for i, (itemId, cnt) in enumerate(qd['compItemCollect']):
                        curCnt = self.questCountItem(questId, itemId)
                        if compCondType == const.QUEST_COMPCOND_DISTINCT:
                            goalState = curCnt >= cnt
                        else:
                            goalState = commQuest.isQuestItemCollectComplete(self, questId)
                        if goalState:
                            continue
                        itemIdList.append(itemId)

                elif compCondType == const.QUEST_COMPCOND_ALL:
                    totalNeed = 0
                    curCnt = 0
                    tmpIdList = []
                    for i, (itemId, cnt) in enumerate(qd['compItemCollect']):
                        totalNeed = cnt
                        curCnt += self.questCountItem(questId, itemId)
                        tmpIdList.append(itemId)

                    if curCnt < totalNeed:
                        itemIdList.extend(tmpIdList)
            elif qd.has_key('compItemCollectMulti'):
                for i, collItems in enumerate(qd['compItemCollectMulti']):
                    totalNeed = 0
                    curCnt = 0
                    tmpIdList = []
                    for itemId, cnt in collItems:
                        totalNeed = cnt
                        curCnt += self.questCountItem(questId, itemId)
                        tmpIdList.append(itemId)

                    if curCnt < totalNeed:
                        itemIdList.extend(tmpIdList)

        else:
            for i, (itemId, cnt) in enumerate(qd['compMaterialItemCollectAndConsume']):
                curCnt = self.questCountMaterialItem(itemId)
                if curCnt < cnt:
                    itemIdList.append(itemId)

        if qd.has_key('comSmtItem'):
            for itemId, cnt in qd['comSmtItem']:
                curCnt = self.questCountItem(questId, itemId)
                if curCnt < cnt:
                    itemIdList.append(itemId)

        if qd.has_key('randomItemCommit'):
            rIndex = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT)
            itemId, cnt = qd['randomItemCommit'][rIndex]
            curCnt = self.questCountItem(questId, itemId)
            if curCnt < cnt:
                itemIdList.append(itemId)
        if qd.has_key('randomItemCommitEx'):
            items = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_EX)
            enableQuestMaterialBag = gameglobal.rds.configData.get('enableQuestMaterialBag', False)
            for itemId, cnt in items:
                if enableQuestMaterialBag:
                    curCnt = self.questCountMaterialItem(itemId)
                else:
                    curCnt = self.questCountItem(questId, itemId, enableParentCheck=True)
                if curCnt < cnt:
                    itemIdList.append(itemId)

        if qd.has_key('randomItemCommitMulti'):
            items = self.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_MULTI)
            for itemListId, cnt in items:
                curCnt = 0
                tmpIdList = []
                for itemId in QIGD.data.get(itemListId, {}).get('itemList', []):
                    curCnt += self.questCountItem(questId, itemId, enableParentCheck=True)
                    tmpIdList.append(itemId)

                if curCnt < cnt:
                    itemIdList.extend(tmpIdList)

        return itemIdList

    def updateLastCompletedQuestInfo(self, questId):
        self.lastCompletedQuestInfo = {'questId': questId,
         'inAuto': self.checkInAutoQuest(),
         'time': utils.getNow()}

    def checkInLastCompletedQuestTime(self):
        return self.lastCompletedQuestInfo.get('time', 0) + 5 > utils.getNow()

    def checkInAutoQuest(self):
        return self.inAutoQuest

    def stopAutoQuest(self):
        if not self.checkInAutoQuest():
            return
        self.inAutoQuest = False
        self.stopAutoQuestTimer()
        self.stopDelayQuestSimpleFindPos()
        clientcom.resetLimitFps()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_AUTO_QUEST_STOP)

    def startAutoQuest(self):
        if not gameglobal.rds.configData.get('enableAutoQuest', False):
            return
        if not uiUtils.hasVipBasic():
            return
        if not int(AppSettings.get(keys.SET_AUTO_QUEST, 1)):
            return
        if self.checkInAutoQuest():
            return
        self.inAutoQuest = True
        gameglobal.rds.ui.dispatchEvent(events.EVENT_AUTO_QUEST_START)

    def updateAutoQuestLoopId(self, questLoopId):
        self.autoQuestLoopId = questLoopId

    def isSameAutoQuestLoopId(self, questLoopId):
        return self.autoQuestLoopId == questLoopId

    def stopAutoQuestTimer(self):
        if self.autoQuestTimer:
            BigWorld.cancelCallback(self.autoQuestTimer)
            self.autoQuestTimer = None
        self.autoQuestLastPos = None

    def updateAutoQuestTimer(self):
        if not self.inWorld or not self.checkInAutoQuest():
            self.autoQuestTimer = None
            return
        else:
            if not self.clientLoadingState and not self.inCombat and self.autoSkill and not self.autoSkill.inSkillMacroTimer() and self.autoQuestLastPos and (self.autoQuestLastPos - self.position).length < 1 and not gameglobal.rds.ui.quest.isShow and not gameglobal.rds.ui.npcV2.isShow and not gameglobal.rds.ui.puzzle.mediator:
                self.delayQuestSimpleFindPos()
            self.autoQuestLastPos = self.position
            self.autoQuestTimer = BigWorld.callback(SCD.data.get('updateAutoQuestTimerCD', 10), self.updateAutoQuestTimer)
            return

    def startAutoQuestTimer(self):
        if not self.checkInAutoQuest():
            return
        self.stopAutoQuestTimer()
        self.autoQuestLastPos = self.position
        self.autoQuestTimer = BigWorld.callback(SCD.data.get('updateAutoQuestTimerCD', 10), self.updateAutoQuestTimer)

    def _checkTempStateIdInQuestData(self, questId, stateId):
        if not gameglobal.rds.configData.get('enableQuestTempStateId', False):
            return False
        else:
            v = self.getQuestData(questId, const.QD_TEMP_STATE_ID)
            if v:
                tempStateId, t = v
                return stateId == tempStateId and utils.getNow() - t < 5
            return False

    def onSelectYaoJingQitanCost(self):
        p = BigWorld.player()
        quests = []
        yaoJingQuests = SCD.data.get('yaojingqitanStartQuestIds', ())
        for questId in p.quests:
            if questId in yaoJingQuests:
                quests.append(questId)

        aEvent = Event(events.EVENT_QUEST_INFO_CHANGE, {'mqList': quests})
        gameglobal.rds.ui.dispatchEvent(aEvent)
