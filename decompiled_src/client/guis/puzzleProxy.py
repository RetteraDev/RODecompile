#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/puzzleProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
from Scaleform import GfxValue
from uiProxy import UIProxy
import const
import gametypes
from guis.ui import gbk2unicode
from guis import asObject
from callbackHelper import Functor
from data import puzzle_data as PD
from data import quest_data as QD
from data import item_data as ID
from data import quest_loop_data as QLD
from cdata import quest_loop_inverted_data as QLID
from cdata import game_msg_def_data as GMDD
from data import npc_puzzle_data as NPD
from data import sys_config_data as SCD
from data import keju_data as KJD
from data import world_puzzle_config_data as WPCD
from data import game_msg_data as GMD
ANS_TYPE_NORMAL = 0
ANS_TYPE_DELETE = 1

class PuzzleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PuzzleProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPuzzleInfo': self.onGetPuzzleInfo,
         'sendAnswer': self.onSendAnswer,
         'clickFightBtn': self.onClickFightBtn,
         'clickItemBtn': self.onClickItemBtn,
         'clickErrorBtn': self.onClickErrorBtn,
         'clickCloseBtn': self.onClickCloseBtn}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PUZZLE:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PUZZLE)

    def clearWidgetBySmall(self):
        self.clearWidget()
        self.addKejuPuzzlePush()

    def reset(self):
        self.mediator = None
        self.puzzleInfo = None
        self.ansList = []
        self.puzzleId = 0
        self.puzzleIdx = 0
        self.puzzleCnt = 0
        self.questId = None
        self.intiMacyType = 0
        self.npcName = ''
        self.npcEntityId = 0
        self.npcIndex = -1
        self.puzzleIndex = -1
        self.npcId = 0
        self.roundFlag = False
        self.intervalTime = 3
        self.titleText = None

    def hide(self, destroy = True):
        p = BigWorld.player()
        if self.questId:
            p.showGameMsg(GMDD.data.ABANDON_PUZZLE_QUEST, ())
        elif self.npcType(self.npcId) in const.PUZZLE_NPC_KEJU:
            pass
        elif self.npcType(self.npcId) == const.PUZZLE_NPC_WORLD:
            p.showGameMsg(GMDD.data.LEAVE_PUZZLE_BY_NPC, ())
            p.cell.abandonNpcPuzzle()
        elif self.npcType(self.npcId) == const.PUZZLE_NPC_TRIGGER:
            p.showGameMsg(GMDD.data.LEAVE_PUZZLE_BY_NPC, ())
            p.cell.abandonNpcPuzzleTrigger()
        p.cell.onQuestPuzzleWindowClosed()
        self.questId = None
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        super(PuzzleProxy, self).hide(destroy)

    def hideByTriggerFail(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.NPC_PUZZLE_TRIGGER_FAIL, ())
        if not self.ansList:
            p.cell.onQuestPuzzleWindowClosed()
            self.questId = None
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        super(PuzzleProxy, self).hide()

    def hideQuestChoicePuzzle(self):
        if not self.ansList:
            self.questId = None
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        super(PuzzleProxy, self).hide()

    def questFinished(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.LEAVE_PUZZLE_QUEST, ())
        if not self.ansList:
            p.cell.onQuestPuzzleWindowClosed()
            self.questId = None
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        super(PuzzleProxy, self).hide()

    def onClickCloseBtn(self, *args):
        self.hidePuzzle()

    def hidePuzzle(self):
        self.closePuzzle()

    def puzzleAnswerUpdate(self, puzzleInfo):
        anwser = puzzleInfo.get(self.puzzleId, const.PUZZLE_RIGHE)
        pd = PD.data.get(self.puzzleId, {})
        questMode = QD.data.get(self.questId, {}).get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE)
        if questMode == gametypes.PUZZLE_MODE_SINGLE:
            if pd.get('multiOpportunity', 0) and anwser == const.PUZZLE_WRONG:
                self.mediator.Invoke('setPuzzleInfo', self.onGetPuzzleInfo())
            else:
                self.questFinished()
        elif questMode in gametypes.PUZZLE_MODE_MULTI:
            if questMode in gametypes.PUZZLE_MODE_RIGHT_CONTINUE and anwser == const.PUZZLE_WRONG:
                self.mediator.Invoke('setPuzzleInfo', self.onGetPuzzleInfo())
            elif self.puzzleIdx != self.puzzleCnt:
                self.showAnswerTag(anwser)
                BigWorld.callback(self.intervalTime, Functor(self.getNextQuestPuzzle))
            else:
                self.showAnswerTag(anwser)
                BigWorld.callback(self.intervalTime, Functor(self.questFinished))

    def puzzleAnswerUpdateByNpc(self, anwser):
        p = BigWorld.player()
        if self.npcType(self.npcId) == const.PUZZLE_NPC_WORLD:
            npd = NPD.data.get(p.weeklyPuzzleNpcNo, {})
        elif self.npcType(self.npcId) == const.PUZZLE_NPC_TRIGGER:
            npd = NPD.data.get(p.triggerPuzzleNpcNo, {})
        else:
            npd = NPD.data.get(p.weeklyPuzzleNpcNo, {})
        puzzleMode = npd.get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE)
        if puzzleMode == gametypes.PUZZLE_MODE_SINGLE:
            if PD.data.get(self.puzzleId, {}).get('multiOpportunity', 0) and anwser == const.PUZZLE_WRONG:
                self.mediator.Invoke('setPuzzleInfo', self.onGetPuzzleInfo())
            else:
                self.questFinished()
        elif puzzleMode in gametypes.PUZZLE_MODE_MULTI:
            self.getNextPuzzleByNpc(puzzleMode, anwser)

    def getNextPuzzleByNpc(self, puzzleMode, anwser):
        if puzzleMode in gametypes.PUZZLE_MODE_FALSE_CONTINUE and anwser == const.PUZZLE_WRONG:
            self.mediator.Invoke('setPuzzleInfo', self.onGetPuzzleInfo())
        if self.puzzleIdx != self.puzzleCnt:
            self.showAnswerTag(anwser)
            BigWorld.callback(self.intervalTime, Functor(self.refreshSetPuzzleInfo))
        else:
            self.showAnswerTag(anwser)
            BigWorld.callback(self.intervalTime, Functor(self.questFinished))

    def refreshSetPuzzleInfo(self):
        p = BigWorld.player()
        if self.npcType(self.npcId) == const.PUZZLE_NPC_WORLD:
            puzzleCnt = len(p.weeklyPuzzleInfo)
            for puzzleIdx in p.weeklyPuzzleInfo:
                result = p.weeklyPuzzleInfo[puzzleIdx].get('result', 0)
                if result == const.PUZZLE_EMPTY:
                    puzzleId = p.weeklyPuzzleInfo[puzzleIdx].get('puzzleId')
                    answers = utils.randomAnswers(puzzleId)
                    self.intervalTime = NPD.data.get(p.weeklyPuzzleNpcNo, {}).get('intervalTime', 3)
                    if puzzleIdx == 0:
                        self.show(puzzleId, answers, puzzleIdx + 1, puzzleCnt)
                    else:
                        self.refreshPuzzle(puzzleId, answers, puzzleIdx + 1, puzzleCnt)
                    break

        elif self.npcType(self.npcId) == const.PUZZLE_NPC_TRIGGER:
            puzzleCnt = len(p.puzzleTriggerInfo)
            for puzzleIdx in p.puzzleTriggerInfo:
                result = p.puzzleTriggerInfo[puzzleIdx].get('result', 0)
                if result == const.PUZZLE_EMPTY:
                    puzzleId = p.puzzleTriggerInfo[puzzleIdx].get('puzzleId')
                    answers = utils.randomAnswers(puzzleId)
                    self.intervalTime = NPD.data.get(p.triggerPuzzleNpcNo, {}).get('intervalTime', 3)
                    if puzzleIdx == 0:
                        self.show(puzzleId, answers, puzzleIdx + 1, puzzleCnt)
                    else:
                        self.refreshPuzzle(puzzleId, answers, puzzleIdx + 1, puzzleCnt)
                    break

    def showAnswerTag(self, anwser, needShowRight = False):
        if not self.mediator:
            return
        if anwser == const.PUZZLE_WRONG:
            self.mediator.Invoke('setAnswerTag', (GfxValue(0), GfxValue(needShowRight)))
        elif anwser == const.PUZZLE_RIGHE:
            self.mediator.Invoke('setAnswerTag', (GfxValue(1), GfxValue(needShowRight)))
        elif anwser in const.PUZZLE_PASS:
            self.mediator.Invoke('setAnswerTag', (GfxValue(2), GfxValue(needShowRight)))

    def showKeJuPanel(self, npcName, npcId, npcEntityId):
        self.npcName = npcName
        self.npcId = npcId
        self.npcEntityId = npcEntityId
        p = BigWorld.player()
        kejuLvLimit = WPCD.data.get('kejuThredholdLv', 15)
        if p.realLv < kejuLvLimit:
            BigWorld.player().showGameMsg(GMDD.data.KEJU_LV_LIMIT, ())
            return
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            if self.npcType(self.npcId) == const.PUZZLE_NPC_KEJU_CHUSAI:
                BigWorld.player().showGameMsg(GMDD.data.CHUSAI_NOT_START, ())
            elif self.npcType(self.npcId) == const.PUZZLE_NPC_KEJU_FUSAI:
                BigWorld.player().showGameMsg(GMDD.data.FUSAI_NOT_START, ())
            return
        kejuId = kejuInfo.get('kejuId', 0)
        self.intervalTime = KJD.data.get(kejuId, {}).get('intervalTime', 3)
        self.puzzleIndex = self.getKeJuCnt()
        if self.puzzleIndex == -1:
            return
        puzzleId = kejuInfo.get('puzzleIds', {}).get(self.puzzleIndex, {}).get('puzzleId', 0)
        answers = utils.randomAnswers(puzzleId)
        rightAnswer = PD.data.get(puzzleId, {}).get('rightAnswer', 0)
        rightAnswerIdx = -1
        for idx, ans in enumerate(answers):
            if ans[0] == rightAnswer:
                rightAnswerIdx = idx

        if not self.mediator:
            self.show(puzzleId, answers, self.puzzleIndex + 1, len(kejuInfo['puzzleIds']), rightAnswerIdx=rightAnswerIdx)
        else:
            self.refreshPuzzle(puzzleId, answers, self.puzzleIndex + 1, len(kejuInfo['puzzleIds']), rightAnswerIdx=rightAnswerIdx)

    def getKeJuCnt(self):
        kejuInfo = BigWorld.player().kejuInfo
        cnt = -1
        if not kejuInfo:
            return cnt
        if self.npcType(self.npcId) not in const.PUZZLE_NPC_KEJU:
            return cnt
        kejuId = kejuInfo.get('kejuId')
        kejuType = kejuInfo.get('kejuType')
        self.npcIndex = -1
        for index, npcId in enumerate(KJD.data.get(kejuId, {}).get('npcList', ())):
            if npcId == self.npcId:
                self.npcIndex = index
                break

        if self.npcIndex == -1:
            return cnt
        startPuzzleIndex = 0
        endPuzzleIndex = 0
        puzzleRate = KJD.data.get(kejuId, {}).get('puzzleRate', ())
        for i in xrange(self.npcIndex):
            startPuzzleIndex += puzzleRate[i]
            endPuzzleIndex += puzzleRate[i]

        endPuzzleIndex += puzzleRate[self.npcIndex] - 1
        for puzzleCnt in kejuInfo['puzzleIds'].keys():
            if kejuInfo.get('puzzleIds', {}).get(puzzleCnt, {}).get('result', -1) == const.PUZZLE_EMPTY:
                cnt = puzzleCnt
                break

        if cnt == -1:
            if kejuType == gametypes.KEJU_PRELIMINALY_TYPE:
                BigWorld.player().showGameMsg(GMDD.data.END_KEJU_PRELIMINALY_QUEST, ())
                gameglobal.rds.ui.kejuGuide.refreshGuideInfo()
            elif kejuType == gametypes.KEJU_FINAL_TYPE:
                if self.roundFlag:
                    self.roundFlag = False
                    rightCnt, useTime, _ = self.getKejuResult()
                    BigWorld.player().showGameMsg(GMDD.data.END_KEJU_FINAL_QUEST, (rightCnt, useTime))
                else:
                    BigWorld.player().showGameMsg(GMDD.data.END_KEJU_FINAL_DESC, ())
                gameglobal.rds.ui.kejuGuide.refreshGuideInfo()
            return cnt
        if self.roundFlag:
            self.roundFlag = False
            gameglobal.rds.ui.kejuGuide.refreshGuideInfo()
            return -1
        if cnt < startPuzzleIndex:
            BigWorld.player().showGameMsg(GMDD.data.ANSWER_BEFORE_PUZZLE_FIRST, ())
            gameglobal.rds.ui.kejuGuide.refreshGuideInfo()
            cnt = -1
        if cnt > endPuzzleIndex:
            BigWorld.player().showGameMsg(GMDD.data.LEAVE_KEJU_PUZZLE_QUEST, ())
            gameglobal.rds.ui.kejuGuide.refreshGuideInfo()
            cnt = -1
        return cnt

    def updateRoundFinish(self):
        self.roundFlag = True
        kejuInfo = BigWorld.player().kejuInfo
        kejuType = kejuInfo.get('kejuType')
        kejuPreliminalyTime = kejuInfo.get('kejuPreliminalyTime', 0)
        rightCnt, useTime, _ = self.getKejuResult()
        if kejuType == gametypes.KEJU_PRELIMINALY_TYPE:
            dataDesc = 'END_KEJU_PRELIMINALY_QUEST_%d' % (kejuPreliminalyTime + 1)
            BigWorld.player().showGameMsg(getattr(GMDD.data, dataDesc), (rightCnt, useTime))
            gameglobal.rds.ui.kejuGuide.refreshGuideInfo()

    def getKejuResult(self):
        kejuInfo = BigWorld.player().kejuInfo
        rightCnt = 0
        lastTime = utils.getNow()
        useTime = lastTime - kejuInfo.get('startTime')
        for puzzle in kejuInfo.get('puzzleIds').values():
            if puzzle['result'] in (const.PUZZLE_RIGHE, const.PUZZLE_MONSTER_PASS, const.PUZZLE_ITEM_PASS):
                rightCnt += 1

        return (str(rightCnt), uiUtils.formatTime(useTime), uiUtils.formatTime(lastTime))

    def puzzleAnswerUpdateByKeJu(self):
        p = BigWorld.player()
        kejuInfo = p.kejuInfo
        anwser = kejuInfo.get('puzzleIds', {}).get(self.puzzleIndex, {}).get('result', 2)
        self.showAnswerTag(anwser, True)
        if not self.intervalTime:
            kejuId = kejuInfo.get('kejuId', 0)
            self.intervalTime = KJD.data.get(kejuId, {}).get('intervalTime', 3)
        BigWorld.callback(self.intervalTime, Functor(self.refreshKeJuInfo))

    def refreshKeJuInfo(self):
        p = BigWorld.player()
        kejuInfo = BigWorld.player().kejuInfo
        self.puzzleIndex = self.getKeJuCnt()
        if self.puzzleIndex == -1:
            self.hide()
            return
        else:
            puzzleId = kejuInfo.get('puzzleIds', {}).get(self.puzzleIndex, {}).get('puzzleId', 0)
            answers = utils.randomAnswers(puzzleId)
            rightAnswer = PD.data.get(puzzleId, {}).get('rightAnswer', 0)
            rightAnswerIdx = -1
            for idx, ans in enumerate(answers):
                if ans[0] == rightAnswer:
                    rightAnswerIdx = idx

            if not self.mediator:
                npc = BigWorld.entities.get(self.npcEntityId, None)
                if not npc:
                    BigWorld.player().showGameMsg(GMDD.data.LEAVE_PUZZLE_NPC, ())
                else:
                    if p.position.distSqrTo(npc.position) > const.NPC_USE_DIST_SQUARED:
                        BigWorld.player().showGameMsg(GMDD.data.LEAVE_PUZZLE_NPC, ())
                        return
                    self.show(puzzleId, answers, self.puzzleIndex + 1, len(kejuInfo['puzzleIds']), rightAnswerIdx=rightAnswerIdx)
            else:
                self.refreshPuzzle(puzzleId, answers, self.puzzleIndex + 1, len(kejuInfo['puzzleIds']), rightAnswerIdx=rightAnswerIdx)
            return

    def getNextQuestPuzzle(self):
        BigWorld.player().onGetNextQuestPuzzle(self.puzzleIdx, self.questId)

    def refreshPuzzle(self, puzzleId, answers, puzzleIdx, puzzleCnt, rightAnswerIdx = -1):
        self.puzzleId = puzzleId
        self.puzzleIdx = puzzleIdx
        self.puzzleCnt = puzzleCnt
        self.puzzleInfo = {'puzzleId': puzzleId,
         'answers': answers,
         'rightAnswerIdx': rightAnswerIdx}
        self.ansList = []
        if self.mediator:
            self.mediator.Invoke('setPuzzleInfo', self.onGetPuzzleInfo())
            if self.puzzleCnt > 1:
                precentStr = str(self.puzzleIdx) + '/' + str(self.puzzleCnt)
                self.mediator.Invoke('setPrecent', GfxValue(gbk2unicode(precentStr)))

    def addKejuPuzzlePush(self):
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            return
        if self.npcType(self.npcId) not in const.PUZZLE_NPC_KEJU:
            return
        msgId = uiConst.MESSAGE_TYPE_KEJU_PUZZLE
        pushMsg = gameglobal.rds.ui.pushMessage
        pushMsg.addPushMsg(msgId)

    def kejuPuzzlePushClick(self):
        msgId = uiConst.MESSAGE_TYPE_KEJU_PUZZLE
        pushMsg = gameglobal.rds.ui.pushMessage
        pushMsg.removePushMsg(msgId)
        self.puzzleAnswerUpdateByKeJu()

    def show(self, puzzleId, answers, puzzleIdx, puzzleCnt, intiMacyType = 0, rightAnswerIdx = -1):
        if not self.mediator:
            self.puzzleId = puzzleId
            self.puzzleIdx = puzzleIdx
            self.puzzleCnt = puzzleCnt
            self.puzzleInfo = {'puzzleId': puzzleId,
             'answers': answers,
             'rightAnswerIdx': rightAnswerIdx}
            self.ansList = []
            self.intiMacyType = intiMacyType
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PUZZLE)

    def autoQuestPuzzle(self, rightAnswer):
        if self.mediator:
            self._sendAnswer(rightAnswer)

    def closePuzzle(self):
        loopId = QLID.data.get(self.questId, {}).get('questLoop', 0)
        qld = QLD.data.get(loopId, {})
        loopInfo = BigWorld.player().questLoopInfo.get(loopId, None)
        if not qld or not loopInfo:
            msg = gameStrings.TEXT_PUZZLEPROXY_451
        else:
            msg = ''
            abandonCD = qld.get('abandonCD', -1)
            abandonItemRm = qld.get('abandonItemRm', [])
            abandonCashRm = qld.get('abandonCashRm', -1)
            abandonType = qld.get('abandonType', 1)
            step = len(loopInfo.questInfo)
            if step > 0 and loopInfo.questInfo[-1][1] == False:
                step -= 1
            avlAbandonCnt = max(0, loopInfo.avlAcCnt - qld.get('avlAcCnt', 0) + step)
            if abandonCD != -1:
                msg += gameStrings.TEXT_PUZZLEPROXY_465 % abandonCD
            if abandonItemRm != []:
                msg += gameStrings.TEXT_PUZZLEPROXY_468 % (ID.data.get(abandonItemRm[0], {}).get('name', gameStrings.TEXT_GAME_1747), abandonItemRm[1])
            if abandonCashRm != -1:
                msg += gameStrings.TEXT_PUZZLEPROXY_471 % abandonCashRm
            if abandonType != gametypes.QUEST_LOOP_ABANDON_TYPE_ONE:
                if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO:
                    msg += gameStrings.TEXT_PUZZLEPROXY_475 % max(avlAbandonCnt, 0)
                elif abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_THREE:
                    msg += gameStrings.TEXT_PUZZLEPROXY_477
            else:
                msg += gameStrings.TEXT_PUZZLEPROXY_451
        if self.npcType(self.npcId) in const.PUZZLE_NPC_KEJU:
            msg = SCD.data.get('LEAVE_KEJU_BY_PLAYER_MSG', gameStrings.TEXT_PUZZLEPROXY_482)
        elif self.npcType(self.npcId) in (const.PUZZLE_NPC_WORLD, const.PUZZLE_NPC_TRIGGER):
            msg = gameStrings.TEXT_PUZZLEPROXY_484
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.hide)

    def onGetPuzzleInfo(self, *arg):
        if self.puzzleInfo is None:
            return uiUtils.dict2GfxDict({}, True)
        else:
            p = BigWorld.player()
            ret = {}
            pData = PD.data.get(self.puzzleInfo['puzzleId'], {})
            ret['content'] = pData.get('desc', '')
            ret['answer'] = []
            ret['rightAnswerIdx'] = self.puzzleInfo['rightAnswerIdx']
            ret['time'] = 0
            limit = QD.data.get(self.questId, {}).get('timeLimit', 0)
            if limit and not p.getQuestData(self.questId, const.QD_FAIL):
                ret['time'] = p.getQuestData(self.questId, const.QD_BEGIN_TIME) + limit - p.getServerTime()
            for idx, ans in enumerate(self.puzzleInfo['answers']):
                label = pData.get('a%d' % ans[0], '')
                enabled = ans[1] == ANS_TYPE_NORMAL
                desc = ''
                if ans[1] != ANS_TYPE_NORMAL and pData.get('reduceDesc', None):
                    desc = pData['reduceDesc'][ans[1][1]]
                ret['answer'].append((label, enabled, desc))

            ret['ansList'] = self.ansList
            if self.puzzleCnt > 1:
                precentStr = str(self.puzzleIdx) + '/' + str(self.puzzleCnt)
                self.mediator.Invoke('setPrecent', GfxValue(gbk2unicode(precentStr)))
            if p.kejuInfo and self.npcType(self.npcId) in const.PUZZLE_NPC_KEJU:
                ret['keju'] = True
                ret['npcName'] = self.npcName + ':'
                ret['count'] = gameStrings.TEXT_PUZZLEPROXY_520
                ret['errorTimeRemain'] = gameStrings.TEXT_PUZZLEPROXY_521
                passItemId = self.getPassItemId()
                deleteErrorItemId = self.getErrorItemId()
                ret['passItemCount'] = p.inv.countItemInPages(passItemId, enableParentCheck=True)
                ret['deleteErrorItemCount'] = p.inv.countItemInPages(deleteErrorItemId, enableParentCheck=True)
                now = utils.getNow()
                if now - p.lastKejuMonsterTime > WPCD.data.get('kejuMonsterInterval', 300):
                    ret['killMonsterEnable'] = True
                else:
                    ret['killMonsterEnable'] = False
            else:
                ret['keju'] = False
            ret['intiMacyType'] = self.intiMacyType
            if self.titleText:
                ret['titleText'] = self.titleText
            loopId = QLID.data.get(self.questId, {}).get('questLoop', 0)
            qld = QLD.data.get(loopId, {})
            isAutoQuest = qld.get('auto', 0)
            pData = PD.data.get(self.puzzleInfo['puzzleId'], {})
            rAnswer = pData.get('rightAnswer', -1)
            rIdx = -1
            for idx, ans in enumerate(self.puzzleInfo['answers']):
                if rAnswer == ans[0]:
                    rIdx = idx

            p = BigWorld.player()
            if isAutoQuest and p.checkInAutoQuest():
                BigWorld.callback(1.5, Functor(self.autoQuestPuzzle, rIdx))
            return uiUtils.dict2GfxDict(ret, True)

    def canUseDeleteErrorItem(self):
        p = BigWorld.player()
        count = 0
        deleteErrorItemId = self.getErrorItemId()
        deleteErrorItemCount = p.inv.countItemInPages(deleteErrorItemId, enableParentCheck=True)
        for answer in self.puzzleInfo.get('answers', []):
            if answer[1] == ANS_TYPE_DELETE:
                count += 1

        if count < 3 and deleteErrorItemCount >= 0:
            return True
        else:
            return False

    def onSendAnswer(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self._sendAnswer(idx)

    def _sendAnswer(self, idx):
        if self.puzzleInfo == None:
            return
        else:
            puzzleId = self.puzzleInfo['puzzleId']
            answerId = self.puzzleInfo['answers'][idx][0]
            self.ansList.append(idx)
            p = BigWorld.player()
            if self.questId:
                p.cell.onQuestPuzzle(self.questId, puzzleId, answerId)
            elif self.npcType(self.npcId) in const.PUZZLE_NPC_KEJU:
                npc = BigWorld.entities.get(self.npcEntityId)
                if npc:
                    if not p or p.position.distSqrTo(npc.position) > const.NPC_USE_DIST_SQUARED:
                        p.showGameMsg(GMDD.data.LEAVE_PUZZLE_NPC, ())
                        return
                    if self.checkKeJuEnd():
                        return
                    npc.cell.answerKejuPuzzle(p.kejuInfo.get('kejuId'), puzzleId, answerId)
                else:
                    p.showGameMsg(GMDD.data.LEAVE_PUZZLE_NPC, ())
            elif self.npcType(self.npcId) == const.PUZZLE_NPC_WORLD:
                p.cell.answerNpcPuzzle(puzzleId, answerId)
            elif self.npcType(self.npcId) == const.PUZZLE_NPC_TRIGGER:
                p.cell.answerNpcPuzzleTrigger(puzzleId, answerId)
            return

    def onClickFightBtn(self, *args):
        if self.checkKeJuEnd():
            return
        text = GMD.data.get(GMDD.data.FIGHT_MONSTER_TEXT, {}).get('text', gameStrings.TEXT_PUZZLEPROXY_602)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, self.fight)

    def onClickItemBtn(self, *args):
        if self.checkKeJuEnd():
            return
        itemId = self.getPassItemId()
        itemData = self._getItemData(itemId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_PUZZLEPROXY_610, self.useItem, itemData=itemData)

    def onClickErrorBtn(self, *args):
        if self.checkKeJuEnd():
            return
        itemId = self.getErrorItemId()
        itemData = self._getItemData(itemId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_PUZZLEPROXY_617, self.deleteError, itemData=itemData)

    def fight(self):
        BigWorld.player().cell.genPuzzleMonster()
        self.clearWidgetBySmall()

    def getPassItemId(self):
        kejuInfo = BigWorld.player().kejuInfo
        kejuType = kejuInfo.get('kejuType')
        if kejuType == gametypes.KEJU_PRELIMINALY_TYPE:
            itemId = SCD.data.get('KE_JU_PASS_ITEM_PRELIMINALY', 400581)
        else:
            itemId = SCD.data.get('KE_JU_PASS_ITEM_FINAL', 400581)
        return itemId

    def getErrorItemId(self):
        kejuInfo = BigWorld.player().kejuInfo
        kejuType = kejuInfo.get('kejuType')
        if kejuType == gametypes.KEJU_PRELIMINALY_TYPE:
            itemId = SCD.data.get('KE_JU_DELETE_ERROR_ITEM_PRELIMINALY', 400581)
        else:
            itemId = SCD.data.get('KE_JU_DELETE_ERROR_ITEM_FINAL', 400581)
        return itemId

    def useItem(self):
        kejuItemId = self.getPassItemId()
        self._useItem(kejuItemId)

    def deleteError(self):
        kejuErrorItemId = self.getErrorItemId()
        self._useItem(kejuErrorItemId)

    def setWrongAnswer(self):
        wrongIndex = -1
        for index, answer in enumerate(self.puzzleInfo.get('answers', [])):
            if answer[0] != 0 and answer[1] == ANS_TYPE_NORMAL:
                wrongIndex = index
                tempAnswer = list(answer)
                tempAnswer[1] = ANS_TYPE_DELETE
                self.puzzleInfo.get('answers', [])[index] = tuple(tempAnswer)
                break

        if wrongIndex == -1:
            return
        if self.mediator:
            enabled = self.canUseDeleteErrorItem()
            self.mediator.Invoke('setWrongAnswer', (GfxValue(wrongIndex), GfxValue(enabled)))

    def _useItem(self, itemId):
        if itemId == 0:
            return
        p = BigWorld.player()
        page, pos = p.inv.findItemInPages(itemId, enableParentCheck=True)
        item = p.inv.getQuickVal(page, pos)
        if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
            p.cell.usePassItem(page, pos)

    def _getItemData(self, itemId):
        p = BigWorld.player()
        iconPath, color = uiUtils.getItemDataByItemId(itemId)
        count = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if count <= 0:
            count = "<font color = \'#FB0000\'>0/1</font>"
        else:
            count = '%d/1' % count
        return {'itemId': itemId,
         'iconPath': iconPath,
         'color': color,
         'count': count}

    def npcType(self, npcId):
        return NPD.data.get(npcId, {}).get('npcType', 0)

    def checkKeJuEnd(self):
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_PUZZLEPROXY_689,))
            self.hidePuzzle()
            return True
        return False

    def setTitle(self, title):
        if self.mediator:
            self.mediator.Invoke('setTitle', GfxValue(gbk2unicode(title)))

    @property
    def visible(self):
        if not self.mediator:
            return False
        mediatorAsObject = asObject.ASObject(self.mediator)
        widget = mediatorAsObject.getWidget()
        if widget and widget.visible:
            return True
        return False
