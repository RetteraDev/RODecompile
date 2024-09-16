#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/questTrackProxy.o
from gamestrings import gameStrings
import types
import re
import BigWorld
from Scaleform import GfxValue
import math
import commNpcFavor
import gameglobal
import const
import uiConst
import utils
import formula
import gametypes
import keys
import commQuest
import activityFactory
import gameconfigCommon
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import events
from guis import hotkey
from guis import ui
from guis import uiUtils
from guis.hotkeyProxy import getKeyContent
from appSetting import Obj as AppSettings
from helpers.guild import getGTSD
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import ASObject
from data import delegation_data as DD
from data import fb_data as FD
from cdata import font_config_data as FCD
from data import formula_client_data as FMLCD
from data import fame_data as FMD
from data import job_action_data as JAD
from data import quest_data as QD
from data import quest_group_data as QGD
from data import tutorial_quest_data as TQD
from data import world_quest_data as WQD
from data import sys_config_data as SCD
from data import fb_guide_data as FGD
from data import seeker_data as SD
from data import crazy_shishen_mode_data as CSMD
from data import quest_type_show_data as QTSD
from cdata import quest_delegation_inverted_data as QDID
from cdata import quest_loop_inverted_data as QLID
from data import item_data as ID
from data import guild_info_activity_data as GIAD
from data import quest_loop_chain_data as QLCD
from data import quest_loop_chain_state_data as QLCSD
from data import play_recomm_item_data as PRID
from data import quest_loop_data as QLD
from cdata import game_msg_def_data as GMDD
from data import duel_config_data as DCD
from guis import worldBossHelper
SUCCESS = 1
FAILED = 2
TAB_SCENARIO = 0
TAB_JOB = 1
TAB_REGION = 2
TAB_GUILD = 3
TAB_FUBEN = 4
TAB_TUTORIAL = 5
TAB_FINDBEAST = 6
TAB_WORLD_BOSS = 7
QUEST_STATE_AVAILABLE = -1
QUEST_STATE_UNFINISH = 0
QUEST_STATE_COMPLETE = 1
QUEST_STATE_TIMEOUT = 2
QUEST_STATE_FAILED = 3
DISPLAY_TYPE_GUILD_TUTORIAL = 99
QUEST_LOOP_DISPLAY_TYPES = (gametypes.QUEST_DISPLAY_TYPE_LOOP,
 gametypes.QUEST_DISPLAY_TYPE_SHIMEN,
 gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION,
 gametypes.QUEST_DISPLAY_TYPE_JOB)
SCENARIO_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_LILIAN,
 gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN,
 gametypes.QUEST_DISPLAY_TYPE_SCHOOL_LUCK,
 gametypes.QUEST_DISPLAY_TYPE_SCHOOL_ONCE,
 gametypes.QUEST_DISPLAY_TYPE_SCHOOL_DAILY,
 gametypes.QUEST_DISPLAY_TYPE_ACTIVITY,
 gametypes.QUEST_DISPLAY_TYPE_LOOP,
 gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION,
 gametypes.QUEST_DISPLAY_TYPE_QI_WEN,
 gametypes.QUEST_DISPLAY_TYPE_MING_YANG,
 gametypes.QUEST_DISPLAY_TYPE_ZHIXIAN,
 gametypes.QUEST_DISPLAY_TYPE_HIDE,
 gametypes.QUEST_DISPLAY_TYPE_SHIMEN,
 gametypes.QUEST_DISPLAY_TYPE_CLUE,
 gametypes.QUEST_DISPLAY_TYPE_FENG_WU)
JOB_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_JOB,)
REGION_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_REGION,)
TUTORIAL_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_SPCIAL,)
GUILD_TAB_DISPLAY_TYPE = (DISPLAY_TYPE_GUILD_TUTORIAL,)
FUBEN_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_FUBEN_NEWTASK,)
FINDBEAST_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_FINDBEAST,)
WORLD_BOSS_TAB_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_WORLD_BOSS,)
RATQ_TRIGGER_EVENT = (events.EVENT_QUEST_COMPLETE,
 events.EVENT_QUEST_ACCEPT,
 events.EVENT_QUEST_ABANDON,
 events.EVENT_LIFE_SKILL_UPDATE,
 events.EVENT_ROLE_SET_LV)
TAB_CONFIG = {TAB_SCENARIO: [SCENARIO_TAB_DISPLAY_TYPE],
 TAB_JOB: [JOB_TAB_DISPLAY_TYPE],
 TAB_REGION: [REGION_TAB_DISPLAY_TYPE],
 TAB_GUILD: [GUILD_TAB_DISPLAY_TYPE],
 TAB_FUBEN: [FUBEN_TAB_DISPLAY_TYPE],
 TAB_TUTORIAL: [TUTORIAL_TAB_DISPLAY_TYPE],
 TAB_FINDBEAST: [FINDBEAST_TAB_DISPLAY_TYPE],
 TAB_WORLD_BOSS: [WORLD_BOSS_TAB_DISPLAY_TYPE]}
TRACK_TYPE_NOT_IN_FB = -1
TRACK_TYPE_QUEST = 1
TRACK_TYPE_FB = 2
TRACK_TYPE_BOTH = 3
TRACK_TYPE_HIDE_IN_FB = 4
GOAL_DESC = 0
GOAL_STATE = 1
GOAL_TRACK = 2
GOAL_TRACK_ID = 3
GOAL_RATE = 4
GOAL_TRACK_TYPE = 5
GOAL_MAGNIFIER_VISIBLE = 6
GOAL_CLICK_FUNC_TYPE = 7
GOAL_ITEM_ID = 8
GOAL_GUILD_HELP = 9
TEXT_COLOR_YELLOW = '#FFE659'
TEXT_COLOR_GREEN = '#5DCA67'
GUILD_TYPE_TIPS = {1: gameStrings.TEXT_QUESTTRACKPROXY_152,
 2: gameStrings.TEXT_QUESTTRACKPROXY_152_1,
 3: gameStrings.TEXT_QUESTTRACKPROXY_152_2,
 4: gameStrings.TEXT_QUESTTRACKPROXY_152_3,
 5: gameStrings.TEXT_QUESTTRACKPROXY_152_4}
SPECIAL_ID = 999
FINDBEAST_START = 1
FINDBEAST_FINISH = 6
FINDBEAST_START_STATE = 0
FINDBEAST_FINISH_STATE = 3
SPECIAL_SEEK_CUREBEAST = 1
SPECIAL_SEEK_MULTICARRIER = 2

class QuestItem(object):

    def __init__(self, questId, questType):
        self.questId = questId
        self.questType = questType
        self.bHasMagnifierInfo = False
        self._inflateBasicQuestInfoFromQD()
        self.modifyTime = 0

    def genGoalList(self, goalData):
        self.goalList = []
        for goalItem in goalData:
            if not goalItem:
                continue
            desc = self._genGoalDesc(goalItem.get(const.QUEST_GOAL_DESC, ''), goalItem.get(const.QUEST_GOAL_TYPE, True))
            rate = (self._genGoalRate(goalItem.get(const.QUEST_GOAL_DESC, '')),)
            state = goalItem.get(const.QUEST_GOAL_STATE, '')
            track = goalItem.get(const.QUEST_GOAL_TRACK, '')
            trackId = goalItem.get(const.QUEST_GOAL_TRACK_ID, '')
            trackType = goalItem.get(const.QUEST_GOAL_TRACK_TYPE, '')
            clickFuncType = goalItem.get(const.QUEST_GOAL_CLICK_FUNC_TYPE, 0)
            itemId = goalItem.get(const.QUEST_GOAL_ITEM_ID, 0)
            guildHelp = goalItem.get(const.QUEST_GOAL_GUILD_HELP, 0)
            bMagnifierVisible = self.calcMagnifierVisible(trackId)
            self.goalList.append([desc,
             state,
             track,
             trackId,
             rate,
             trackType,
             bMagnifierVisible,
             clickFuncType,
             itemId,
             guildHelp])

        self.bHasMagnifierInfo = True

    def setQuestState(self, state):
        self.questState = state

    def setTimeLimitInfo(self, limitType, timeLeft):
        self.timeLimitType = limitType
        self.timeLeft = timeLeft
        self.maxTime = QD.data.get(self.questId, {}).get('timeLimit', timeLeft)

    def _inflateBasicQuestInfoFromQD(self):
        if not hasattr(self, 'qData'):
            self.qData = QD.data.get(self.questId, {})
        self.questName = self.qData.get('name', '')
        self.extraGoal = self.qData.get('extraDesc', '')
        self.additionalDesc = self.qData.get('additionalDesc', '')
        qd = self.qData
        self.extraSituationDesc = []
        if gameconfigCommon.enableNFNewQuestLoop():
            if qd.get('situationType', 0) == gametypes.QUEST_REWARD_ITEM_EXTRA_SITUATION_TYPE:
                situationParamDesc = qd.get('situationParamDesc', ())
                for index, param in enumerate(qd.get('situationParam', ())):
                    statsType, keyName, maxValue = param
                    if statsType == gametypes.STATS_TYPE_QUEST:
                        varList = BigWorld.player().questVars
                        currentVal = varList.get(keyName, 0)
                        goalDesc = uiUtils.toHtml(situationParamDesc[index] % (currentVal, maxValue), TEXT_COLOR_YELLOW)
                        self.extraSituationDesc.append(goalDesc)

            if qd.get('extraRewardDesc', ''):
                self.extraSituationDesc.append(qd['extraRewardDesc'])
        if self.qData.get('condRelation', 0):
            self.orRelationDesc = gameStrings.TEXT_QUESTTRACKPROXY_226
        else:
            self.orRelationDesc = ''

    def _genGoalDesc(self, desc, isNormal):
        ret = re.sub(gameStrings.TEXT_QUESTTRACKPROXY_231, '', desc)
        if not isNormal:
            ret = gameStrings.TEXT_QUESTLOGPROXY_1393 + ret
        return ret

    def _genGoalRate(self, desc):
        ret = re.findall(gameStrings.TEXT_QUESTTRACKPROXY_231, desc)
        if len(ret) > 0:
            ret = ret[0]
            ret = ret[2:-2]
        else:
            ret = ''
        return ret

    def needRefreshTimeInfo(self):
        return QD.data.get(self.questId) and self.questState != QUEST_STATE_AVAILABLE

    def needRefreshMagnifier(self):
        return self.updateMagnifier()

    def updateQuestTimeInfo(self):
        timeInfo = []
        p = BigWorld.player()
        loopId = p.getQuestLoopId(self.questId)
        stateType = 1 if commQuest.completeQuestCheck(p, self.questId) else 0
        p._addTimerLimitQuestTrack(timeInfo, self.questId, stateType, loopId)
        self.setQuestState(timeInfo[0])
        self.setTimeLimitInfo(timeInfo[1][0], timeInfo[1][1])

    def formatReturn(self, questChange = False):
        if self.needRefreshTimeInfo():
            self.updateQuestTimeInfo()
        self.updateMagnifier(True)
        ret = {}
        ret['questId'] = getattr(self, 'questId', 0)
        ret['questName'] = getattr(self, 'questName', '')
        ret['questType'] = getattr(self, 'questType', 0)
        ret['goalList'] = getattr(self, 'goalList', [])
        ret['questState'] = getattr(self, 'questState', 0)
        ret['extraGoal'] = getattr(self, 'extraGoal', '')
        ret['timeInfo'] = [getattr(self, 'timeLimitType', 0), getattr(self, 'timeLeft', 0), getattr(self, 'maxTime', 0)]
        ret['additionalDesc'] = getattr(self, 'additionalDesc', '')
        ret['extraSituationDesc'] = getattr(self, 'extraSituationDesc', [])
        ret['orRelationDesc'] = getattr(self, 'orRelationDesc', '')
        ret['canTransfer'] = self.qData.has_key('questGroup')
        ret['quickGroup'] = self.qData.get('quickGroup', None)
        ret['startTrackId'] = self.qData.get('startTrackId', 0)
        ret.update(self.extraReturnInfo())
        trackIdx = gameglobal.rds.ui.questTrack.getTrackedIds(ret['questId']) - 1
        if trackIdx == 0:
            gameglobal.rds.ui.questTrack.simpleFindPosInfo = {}
            posId = self.calcSimpleFind(ret)
            if posId:
                gameglobal.rds.ui.questTrack.simpleFindPosInfo = {'questId': ret['questId'],
                 'type': uiConst.QUEST_QUICK_COMPLETE_TYPE_FIND_POS,
                 'posId': posId}
            if not gameglobal.rds.ui.questTrack.simpleFindPosInfo:
                itemId = self.calcAuctionItemId(ret)
                if itemId:
                    gameglobal.rds.ui.questTrack.simpleFindPosInfo = {'questId': ret['questId'],
                     'type': uiConst.QUEST_QUICK_COMPLETE_TYPE_AUCTION,
                     'itemId': itemId}
            _, _, hotKeyDesc = getKeyContent(hotkey.KEY_SIMPLE_FIND_POS)
            gameglobal.rds.ui.dispatchEvent(events.EVENT_AUTO_QUEST_CHANGE, ret)
            if hotKeyDesc:
                ret['spFindInfo'] = gameStrings.QUEST_TRACK_QUICK_COMPLETE_DESC % hotKeyDesc
                if questChange:
                    p = BigWorld.player()
                    if p.checkInAutoQuest():
                        questLoopId = commQuest.getQuestLoopIdByQuestId(ret['questId'])
                        if not p.isSameAutoQuestLoopId(questLoopId):
                            p.stopDelayQuestSimpleFindPos()
                        elif QLD.data.get(questLoopId, {}).get('auto', 0):
                            p.delayQuestSimpleFindPos()
                        else:
                            p.stopAutoQuest()
                    else:
                        p.stopDelayQuestSimpleFindPos()
        return ret

    def calcSimpleFind(self, info):
        if not info:
            return None
        else:
            tmpTrackIds = []
            if info.get('questState', 0) == QUEST_STATE_COMPLETE:
                comTrackId = QD.data.get(info.get('questId', 0)).get('comNpcTk', 0)
                p = BigWorld.player()
                comNpcId = commQuest.getQuestCompNpc(p, info.get('questId', 0))
                comNpcIds = QD.data.get(info.get('questId', 0), {}).get('compNpc', 0)
                _index = -1
                try:
                    _index = comNpcIds.index(comNpcId)
                except:
                    _index = -1

                if _index == -1:
                    pass
                else:
                    return comTrackId[_index]
            for item in info['goalList']:
                if item[GOAL_STATE]:
                    continue
                if item[GOAL_TRACK] and item[GOAL_TRACK_TYPE] != '':
                    return item[GOAL_TRACK_ID]
                tmpTrackIds.insert(0, item[GOAL_TRACK_ID])

            for item in tmpTrackIds:
                return item

            return None

    def calcAuctionItemId(self, info):
        if not info:
            return None
        elif info.get('questState', 0) == QUEST_STATE_COMPLETE:
            return None
        else:
            for item in info['goalList']:
                if item[GOAL_STATE]:
                    continue
                if item[GOAL_CLICK_FUNC_TYPE] != uiConst.QUEST_GOAL_ITEM_CLICK_SEARCH:
                    continue
                if item[GOAL_ITEM_ID]:
                    return item[GOAL_ITEM_ID]

            return None

    def updateMagnifier(self, isUpdate = True):
        bChanged = False
        if self.bHasMagnifierInfo:
            if not self.goalList:
                return
            for item in self.goalList:
                trackId = item[3]
                bMagnifierVisible = self.calcMagnifierVisible(trackId)
                if item[6] != bMagnifierVisible:
                    bChanged = True
                    if isUpdate:
                        item[6] = bMagnifierVisible

        return bChanged

    def calcMagnifierVisible(self, trackId):
        seekId = 0
        try:
            seekId = eval(trackId) if type(trackId) == str else trackId
        except:
            seekId = 0

        seekId = seekId[0] if type(seekId) == types.TupleType else seekId
        tempSpaceNo = SD.data.get(seekId, {}).get('spaceNo', 0)
        p = BigWorld.player()
        bMagnifierVisible = False
        if p.mapID == tempSpaceNo:
            bMagnifierVisible = True
        else:
            shareMaps = SD.data.get(seekId, {}).get('sharedMaps', None)
            if shareMaps:
                for value in shareMaps:
                    if p.mapID == value:
                        bMagnifierVisible = True
                        break

        return bMagnifierVisible

    def extraReturnInfo(self):
        return {}


class DelegationQuestItem(QuestItem):

    def setTimeLimitInfo(self, limitType, timeLeft):
        super(DelegationQuestItem, self).setTimeLimitInfo(limitType, timeLeft)
        delegationId = QLID.data.get(self.questId, {}).get('delegationId', 0)
        self.maxTime = DD.data.get(delegationId, {}).get('timeLimit', timeLeft)


class TutorialQuestItem(QuestItem):

    def setQuestState(self, state):
        super(TutorialQuestItem, self).setQuestState(state)
        if self.questState == QUEST_STATE_AVAILABLE:
            self.additionalDesc = ''
            self.orRelationDesc = ''
            self.extraGoal = TQD.data.get(self.questId, {}).get('tutorialDesc', '')

    def extraReturnInfo(self):
        ret = {}
        ret['autoAc'] = self.qData.get('autoAc', 0)
        ret['trackId'] = self.qData.get('acNpcTk', 0)
        return ret


class RegionQuestItem(QuestItem):

    @staticmethod
    def checkValidWorldQuest(questId):
        rqData = WQD.data.get(questId, {})
        if questId == gameglobal.rds.ui.questTrack.completeId:
            return True
        if not (rqData and rqData.get('areaId', 0) == gameglobal.rds.ui.regionQuest.areaId):
            return False
        if not BigWorld.player().worldAreaValid:
            return False
        return True

    def _inflateBasicQuestInfoFromQD(self):
        self.qData = WQD.data.get(self.questId, {})
        super(RegionQuestItem, self)._inflateBasicQuestInfoFromQD()

    def needRefreshTimeInfo(self):
        return bool(WQD.data.get(self.questId, {}))

    def updateQuestTimeInfo(self):
        for goal in self.goalList:
            goal[-1] = BigWorld.player().getServerTime()

    def genGoalList(self, goalData):
        p = BigWorld.player()
        self.goalList = []
        questVars = self.qData.get('questVars', [])
        for questVar in questVars:
            num = p.getWorldQuestData(self.questId, const.WAQD_VARS, {}).get(questVar[0], 0)
            goalDesc = questVar[1]
            showType = questVar[2]
            addtion = questVar[3]
            showStep = questVar[4] if len(questVar) >= 5 else 0
            serverTime = p.getServerTime()
            if goalDesc.find('(%d/%d)') != -1:
                goalDesc = goalDesc % (num, int(addtion))
            self.goalList.append([num,
             goalDesc,
             showType,
             addtion,
             showStep,
             serverTime])

    def _regionStepInfo(self):
        rateArr = []
        stepMax = []
        stepCurrent = []
        p = BigWorld.player()
        for goal in self.goalList:
            tgtVarRange = self.qData.get('tgtVarRange', ())
            for index, range in enumerate(tgtVarRange):
                stepMax.append(range)
                val = p.getWorldQuestData(self.questId, const.WAQD_TGT_VAR, 0)
                for i in xrange(index):
                    val -= tgtVarRange[i]

                stepCurrent.append(val)

            rewardRate = self.qData.get('rewardRate', ())
            for rate in rewardRate:
                rateArr.append(rate)

        ret = {}
        ret['stepMax'] = stepMax
        ret['stepCurrent'] = stepCurrent
        ret['rateArr'] = rateArr
        return ret

    def _regionAwardInfo(self):
        p = BigWorld.player()
        self.cashAward = 0
        self.fameAward = []
        self.expAward = 0
        fmd = FMD.data
        ret = {}
        rewardRate, rewardRatio = commQuest.getWARewardRate(p, self.questId)
        if rewardRate:
            self.cashAward = int(p.getWorldQuestData(self.questId, const.WAQD_CASH, 0) * rewardRatio)
            self.expAward = int(p.getWorldQuestData(self.questId, const.WAQD_EXP, 0) * rewardRatio)
        if self.qData.get('compFame', ()):
            compFame = self.qData['compFame']
            for fameId, fameAmount in compFame:
                self.fameAward.append((fmd.get(fameId, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1), int(fameAmount * rewardRatio)))

        ret['cashAward'] = self.cashAward
        ret['expAward'] = self.expAward
        ret['fameAward'] = self.fameAward[0] if self.fameAward else [gameStrings.TEXT_CHALLENGEPROXY_199_1, 0]
        return ret

    def hasAward(self):
        ret = True
        ret &= getattr(self, 'cashAward', 0)
        ret &= getattr(self, 'fameAward', [])
        ret &= getattr(self, 'expAward', 0)
        return ret

    def extraReturnInfo(self):
        ret = {}
        awardLvNeed = self.qData.get('thresholdLv', 0)
        ret['stepDesc'] = self.qData.get('stepDesc', '')
        ret['awardLvNeed'] = awardLvNeed
        ret['awardLvMatch'] = BigWorld.player().lv >= awardLvNeed
        ret['completeFlag'] = ret['awardLvMatch'] and self.questId == gameglobal.rds.ui.questTrack.completeId
        ret['iconType'] = self.qData.get('tkType', 1)
        ret['quickGroup'] = self.qData.get('activityId', 0)
        ret.update(self._regionStepInfo())
        ret.update(self._regionAwardInfo())
        return ret


class GuildTutorialItem(QuestItem):

    def _inflateBasicQuestInfoFromQD(self):
        self.qData = getGTSD().data.get(self.questId, {})
        self.questName = self.qData.get('name', '')
        self.extraGoal = self.qData.get('description', '')

    def extraReturnInfo(self):
        ret = {}
        p = BigWorld.player()
        ret['maxValue'] = self.qData.get('maxValue', 100)
        ret['progressDispType'] = self.qData.get('progressDispType', 1)
        ret['progressDispName'] = self.qData.get('progressDispName', '')
        ret['contrib'] = self.qData.get('contrib', 0)
        ret['hasAward'] = self.qData.get('contrib', 0) > 0 or self.qData.get('bindCash', 0) > 0 or self.qData.get('wood', 0) > 0 or self.qData.get('mojing', 0) > 0 or self.qData.get('xirang', 0) > 0
        ret['tgtType'] = self.qData.get('targetType', 1)
        if ret['tgtType'] in (2, 4):
            ret['questName'] = uiUtils.toHtml(self.questName, TEXT_COLOR_YELLOW)
        else:
            ret['questName'] = uiUtils.toHtml(self.questName, TEXT_COLOR_GREEN)
        ret['curValue'] = p.guild.getTutorialStepProgress(self.questId) if p.guild else 0
        ret['tips'] = GUILD_TYPE_TIPS.get(ret['tgtType'], '')
        return ret


class ClueQuestItem(QuestItem):

    def _inflateBasicQuestInfoFromQD(self):
        super(ClueQuestItem, self)._inflateBasicQuestInfoFromQD()
        self.extraGoal = ''

    def genGoalList(self, goalData):
        p = BigWorld.player()
        self.goalList = []
        loopId = commQuest.getQuestLoopIdByQuestId(self.questId)
        loopInfo = p.questLoopInfo.get(loopId, None)
        goals = loopInfo.questInfo if loopInfo else []
        for goalId, state in goals[-4:]:
            desc = QD.data.get(goalId, {}).get('shortDesc', '')
            trackId = -1
            track = False
            rate = ''
            trackType = ''
            bMagnifierVisible = False
            self.goalList.append([desc,
             state,
             track,
             trackId,
             rate,
             trackType,
             bMagnifierVisible])

        self.bHasMagnifierInfo = True


class JobQuestItem(QuestItem):

    def _progressInfo(self):
        p = BigWorld.player()
        maxValue = 100
        currentValue = 0
        seperator = []
        ratioTips = []
        needJobScore = self.qData.get('needJobScore', ())
        awardFactor = self.qData.get('awardFactor', ())
        if needJobScore:
            maxValue = needJobScore[-1]
            jobScoreVar = self.qData.get('jobScoreVar', 'jobScoreVar%d' % self.questId)
            currentValue = p.questVars.get(jobScoreVar, 0)
            seperator = [ score * 1.0 / maxValue for score in needJobScore ]
            ratioTips = [ ratio for ratio in awardFactor ]
        progressActionTips = ''
        jobGroup = self.qData.get('jobGroup', 0)
        actions = JAD.data.get(jobGroup, {})
        jobIds = p.questData.get(self.questId, {}).get(const.QD_JOBS, [])
        for action in actions:
            if action.get('jobId', 0) in jobIds and action.get('visible', 0) == 1:
                progressActionTips += '%s    +%s\n' % (action.get('name', ''), action.get('jobScore', 0))

        ret = {}
        ret['jobMaxValue'] = maxValue
        ret['jobCurrentValue'] = currentValue
        ret['jobSeperator'] = seperator
        ret['jobRatioTips'] = ratioTips
        ret['jobActionTips'] = progressActionTips
        return ret

    def _jobQuestTimeInfo(self):
        p = BigWorld.player()
        leftTime = -1
        endTimeXingJi = ''
        isFailed = commQuest.questFailCheck(p, self.questId)
        if not isFailed:
            jobTimeInfo = p.getQuestData(self.questId, const.QD_JOB_TIME, None)
            if jobTimeInfo:
                leftTime = jobTimeInfo[1] - p.getServerTime()
                endTime = math.ceil(formula.getXingJiTime(formula.getFloatDayTime(math.ceil(jobTimeInfo[1]))))
                endTimeXingJi = gameStrings.TEXT_QUESTTRACKPROXY_660 % uiUtils.convertToXingJiWord(uiUtils.getXingJiWordIdx(int(endTime)))
        ret = {}
        ret['jobLeftTime'] = leftTime
        ret['jobEndTimeXingji'] = endTimeXingJi
        ret['jobFailFlag'] = isFailed
        return ret

    def extraReturnInfo(self):
        ret = {}
        ret['jobDesc'] = self.qData.get('jobDesc', gameStrings.TEXT_JOBBOARDPROXY_257)
        ret.update(self._progressInfo())
        ret.update(self._jobQuestTimeInfo())
        return ret


QUEST_TYPE_MAP = {gametypes.QUEST_DISPLAY_TYPE_CLUE: ClueQuestItem,
 gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION: DelegationQuestItem,
 gametypes.QUEST_DISPLAY_TYPE_REGION: RegionQuestItem,
 gametypes.QUEST_DISPLAY_TYPE_JOB: JobQuestItem,
 gametypes.QUEST_DISPLAY_TYPE_SPCIAL: TutorialQuestItem,
 DISPLAY_TYPE_GUILD_TUTORIAL: GuildTutorialItem}

class QuestInflater(object):

    def __init__(self):
        self.questCateDict = {}

    def inflateQuests(self, quests):
        self._clearQuestCateExclude([gametypes.QUEST_DISPLAY_TYPE_REGION, DISPLAY_TYPE_GUILD_TUTORIAL])
        for quest in quests:
            questId = quest[5]
            if not gameglobal.rds.ui.questTrack.needShowQuestInTracker(questId):
                continue
            questType, qItem = self.genQuestItemByQuestData(quest)
            self._addToCateDict(questType, qItem)

    def inflateRegionQuests(self, questIds):
        questType = gametypes.QUEST_DISPLAY_TYPE_REGION
        self._clearQuestCateInclude([questType])
        for questId in questIds:
            if not RegionQuestItem.checkValidWorldQuest(questId):
                continue
            qItem = self._createQuestItem(questId, questType)
            qItem.genGoalList(None)
            self._addToCateDict(questType, qItem)

    def inflateAvailableTutorialQuests(self, questIds):
        questType = gametypes.QUEST_DISPLAY_TYPE_SPCIAL
        for questId in questIds:
            qItem = self._createQuestItem(questId, questType)
            qItem.setQuestState(QUEST_STATE_AVAILABLE)
            self._addToCateDict(questType, qItem, True)

    def inflateGuildTutorialQuests(self, questIds):
        questType = DISPLAY_TYPE_GUILD_TUTORIAL
        self._clearQuestCateInclude([questType])
        for questId in questIds:
            qItem = self._createQuestItem(questId, questType)
            self._addToCateDict(questType, qItem)

        if len(questIds) > 0:
            orderMap = {1: 5,
             2: 2,
             3: 4,
             4: 3,
             5: 1}
            self.questCateDict[questType].sort(key=lambda value: orderMap.get(value.qData.get('targetType', 1)))

    def genQuestItemByQuestData(self, quest):
        questId = quest[5]
        questType = QD.data.get(questId, {}).get('displayType', quest[0])
        qItem = self._createQuestItem(questId, questType)
        qItem.genGoalList(quest[4])
        qItem.setQuestState(quest[1])
        qItem.setTimeLimitInfo(quest[2][0], quest[2][1])
        return (questType, qItem)

    def removeQuest(self, questId):
        for k, v in self.questCateDict.items():
            qids = [ q.questId for q in v ]
            if questId in qids:
                del v[qids.index(questId)]
                return k

        return -1

    def addQuest(self, questId):
        impQdata = BigWorld.player().genTrackedQuestInfo(questId)
        if not impQdata:
            return (-1, None)
        else:
            questType, qItem = self.genQuestItemByQuestData(impQdata)
            self._addToCateDict(questType, qItem)
            self.setQuestModifyTime(qItem, utils.getNow())
            return (questType, qItem)

    def updateQuest(self, questId):
        impQdata = BigWorld.player().genTrackedQuestInfo(questId)
        if not impQdata:
            return (-1, None)
        else:
            questType, qItem = self.genQuestItemByQuestData(impQdata)
            qtList = self.questCateDict.get(questType, [])
            qidList = [ q.questId for q in qtList ]
            if questId not in qidList:
                return (-1, None)
            idx = -1
            for i, value in enumerate(qidList):
                if value == questId:
                    idx = i

            if self.questCateDict[questType][idx].questState == QUEST_STATE_AVAILABLE:
                return (-1, None)
            self.questCateDict[questType][idx] = qItem
            self.setQuestModifyTime(qItem, utils.getNow())
            return (questType, qItem)

    def addAvlTutorialQuest(self, questId):
        self.inflateAvailableTutorialQuests([questId])

    def removeAvlTutorialQuest(self, questId):
        questType = gametypes.QUEST_DISPLAY_TYPE_SPCIAL
        qList = self.questCateDict.get(questType, [])
        for i in xrange(len(qList)):
            qItem = qList[i]
            if qItem.questId == questId:
                del qList[i]
                break

    def formatQuestListInfo(self, typeDisplayOrder):
        if not typeDisplayOrder:
            return []
        questInfoList = []
        for dType in typeDisplayOrder:
            questItemList = self.getDisplayQuest(dType)
            ret = [ qItem.formatReturn() for qItem in questItemList ]
            questInfoList.extend(ret)

        trackIndx = gameglobal.rds.ui.questTrack.trackedIds
        questInfoList.sort(key=lambda q: trackIndx.get(q['questId'], [0])[0])
        return questInfoList

    def isTutorialQuestAvaliable(self, qItem, type):
        if type == gametypes.QUEST_DISPLAY_TYPE_SPCIAL:
            if qItem.questState == QUEST_STATE_AVAILABLE:
                return True
        return False

    def getDisplayQuest(self, dt):
        questItemList = self.questCateDict.get(dt, [])
        if dt == gametypes.QUEST_DISPLAY_TYPE_SPCIAL:
            return [ qItem for qItem in questItemList if qItem.questState != QUEST_STATE_AVAILABLE ]
        return questItemList

    def getQuestItemList(self, typeDisplayOrder):
        if not typeDisplayOrder:
            return []
        allItem = []
        for type in typeDisplayOrder:
            questItemList = self.questCateDict.get(type, [])
            allItem.append(questItemList)

        return allItem

    def countTabContentNum(self, tabId):
        if tabId not in TAB_CONFIG:
            return 0
        num = 0
        displayTypes = TAB_CONFIG[tabId][0]
        for dt in displayTypes:
            questItemList = self.getDisplayQuest(dt)
            num += len(questItemList)

        return num

    def refreshQuestTrackIndex(self, indexCache):
        indexCache.clear()
        self._trackIndexOfTypeList(indexCache, SCENARIO_TAB_DISPLAY_TYPE)
        self._trackIndexOfTypeList(indexCache, JOB_TAB_DISPLAY_TYPE)
        self._trackIndexOfTypeList(indexCache, TUTORIAL_TAB_DISPLAY_TYPE)

    def _trackIndexOfTypeList(self, indexCache, typeList):
        index = 1
        qList = []
        for t in typeList:
            tList = self.questCateDict.get(t, None)
            tList and qList.extend(tList)

        qList.sort(self._questItemCmp)
        for qItem in qList:
            indexCache.setdefault(qItem.questId, [])
            indexCache[qItem.questId].append(index)
            index += 1

    def _trackIndexOfType(self, indexCache, type, index):
        qList = self.questCateDict.get(type, None)
        if not qList:
            return index
        else:
            qList.sort(self._questItemCmp)
            for qItem in qList:
                indexCache.setdefault(qItem.questId, [])
                indexCache[qItem.questId].append(index)
                index += 1

            return index

    def _questItemCmp(self, item1, item2):
        modifyTime1 = item1.modifyTime
        modifyTime2 = item2.modifyTime
        if modifyTime1 == modifyTime2:
            tabType = gameglobal.rds.ui.questTrack.getTrackTabByQuestType(item1.questType)
            trackIdx1 = TAB_CONFIG[tabType][0].index(item1.questType)
            trackIdx2 = TAB_CONFIG[tabType][0].index(item2.questType)
            res = trackIdx1 - trackIdx2
        else:
            res = modifyTime2 - modifyTime1
        if res > 0:
            return 1
        else:
            return -1

    def _addToCateDict(self, questType, qItem, head = False):
        if not self.questCateDict.has_key(questType):
            self.questCateDict[questType] = []
        if head:
            self.questCateDict[questType].insert(0, qItem)
        else:
            self.questCateDict[questType].append(qItem)

    def _clearQuestCateInclude(self, includeFilter):
        for qType in includeFilter:
            self.questCateDict.pop(qType, None)

    def _clearQuestCateExclude(self, exludeFilter):
        for k in self.questCateDict.keys():
            if k in exludeFilter:
                continue
            self.questCateDict.pop(k, None)

    def _createQuestItem(self, questId, questType):
        if QUEST_TYPE_MAP.has_key(questType):
            qItem = QUEST_TYPE_MAP[questType](questId, questType)
        else:
            qItem = QuestItem(questId, questType)
        return qItem

    def setQuestModifyTime(self, qItem, curTime):
        qItem.modifyTime = curTime


class QuestTrackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuestTrackProxy, self).__init__(uiAdapter)
        self.modelMap = {'fetchAllTrackedQuest': self.onFetchAllTrackedQuest,
         'getTabContent': self.onGetTabContent,
         'autoFindPath': self.onAutoFindPath,
         'openTaskLog': self.onOpenTaskLog,
         'sendTask': self.onSendTask,
         'gotoTrack': self.onGotoTrack,
         'guildHelp': self.onGuildHelp,
         'getTrackInfo': self.onGetTrackInfo,
         'saveTrackInfo': self.onSaveTrackInfo,
         'showTargetInltMap': self.onShowTargetInltMap,
         'handleTextEvent': self.onHandleTextEvent,
         'cancelTrack': self.onCancelTrack,
         'showHotKeySetting': self.onShowHotKeySetting,
         'getHotKeyDesc': self.onGetHotKeyDesc,
         'getFubenTrackType': self.onGetFubenTrackType,
         'autoAccQuest': self.onAutoAccQuest,
         'quickGroup': self.onQuickGroup,
         'regionQuickGroup': self.onRegionQuickGroup,
         'getFubenTargetGuideInfo': self.onGetFubenTargetGuideInfo,
         'checkQuestTrackItemInfo': self.onCheckQuestTrackItemInfo,
         'showConsignWindow': self.onShowConsignWindow,
         'useNewGuildTutorial': self.onUseNewGuildTutorial,
         'getFindBeastTargetGuideInfo': self.onGetFindBeastTargetGuideInfo,
         'handleFindBeastGoto': self.onHandleFindBeastGoto,
         'getIsShowFindBeast': self.onGetIsShowFindBeast,
         'isInGuildSpace': self.onIsInGuildSpace,
         'checkRegionComplete': self.onCheckRegionComplete,
         'teleportToStart': self.onTeleportToStart,
         'getWorldBossInfo': self.onGetWorldBossInfo,
         'getIsShowWorldBoss': self.onGetIsShowWorldBoss,
         'showWorldBossDetail': self.onShowWorldBossDetail,
         'seekWorldBoss': self.onSeekWorldBoss}
        self.mediator = None
        self.showRipple = True
        self.curTab = TAB_SCENARIO
        self.completeId = 0
        self.avlTutorialSet = set()
        self.avlRegionSet = set()
        self.avlGuildSet = set()
        self.trackedIds = {}
        self.qif = QuestInflater()
        self.fbNo = None
        self.fbStage = None
        self.fbInfo = {}
        self.cacheWorldQuestInfo = {}
        self.curInfo = None
        self.findBeastQuests = None
        self.questLoopChainId = None
        self.showNews = False
        self.searchPathCallbackHandle = None
        self.searchSpaceNo = None
        self.searchPosition = None
        self.mqList = []
        self.simpleFindPosInfo = None
        self.addEvent(events.EVENT_QUEST_COMPLETE, self.onQuestCompleted, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_ACCEPT, self.onQuestAccepted, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_ABANDON, self.onQuestAbandoned, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_INFO_CHANGE, self.onQuestInfoChanged, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_TRACK_CHANGED, self.onQuestTrackChanged, isGlobal=True)
        self.addEvent(events.EVENT_GUILD_TUTORIAL_UPDATE, self.refreshGuildTutorialList, isGlobal=True)
        self.addEvent(events.EVENT_FINDPOS_STOP, self.dynamicPathSearchStop, isGlobal=True)

    def reset(self):
        self.avlTutorialSet.clear()
        self.avlRegionSet.clear()
        self.avlGuildSet.clear()
        self.qif.questCateDict.clear()
        self.cacheWorldQuestInfo.clear()

    def onFetchAllTrackedQuest(self, *arg):
        BigWorld.player().fetchAllTrackedQuest()

    def isGoalComplete(self, seekId):
        isComplete = False
        hasGoal = False
        checkTab = [TAB_SCENARIO, TAB_JOB, TAB_TUTORIAL]
        try:
            displayTypes = []
            for tab in checkTab:
                displayTypes.extend(TAB_CONFIG[tab][0])

            qItemList = []
            for dt in displayTypes:
                qItemList.extend(self.qif.questCateDict.get(dt, []))

            for qItem in qItemList:
                if qItem.questState == QUEST_STATE_AVAILABLE:
                    continue
                for goal in qItem.goalList:
                    if goal[3] == seekId:
                        hasGoal = True
                        if goal[1]:
                            isComplete = True
                        raise Exception()
                    else:
                        hasGoal = False

        except:
            pass

        if hasGoal:
            return isComplete
        else:
            return True

    def onGetTabContent(self, *arg):
        tabId = int(arg[3][0].GetNumber())
        self.curTab = tabId
        qNums = {}
        ret = {}
        for tId in TAB_CONFIG:
            qNums[tId] = self.qif.countTabContentNum(tId)

        if TAB_CONFIG.has_key(tabId) and TAB_CONFIG[tabId]:
            ret['qList'] = self.qif.formatQuestListInfo(TAB_CONFIG[tabId][0])
        else:
            ret['qList'] = []
        ret['qNums'] = qNums
        return uiUtils.dict2GfxDict(ret, True)

    def onAllTrackedQuestFetched(self, questInfos):
        self.qif.inflateQuests(questInfos)
        self.qif.inflateAvailableTutorialQuests(self.avlTutorialSet)
        self.qif.refreshQuestTrackIndex(self.trackedIds)
        if self.mediator:
            self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
        gameglobal.rds.ui.littleMap.refreshNpcPos(self.qif)
        gameglobal.rds.ui.map.refreshNpcPos(self.qif)

    def resetWidgetUI(self):
        if self.mediator:
            self.mediator.Invoke('resetWidgetUI')

    def onAutoFindPath(self, *arg):
        id = arg[3][0].GetString()
        ret = uiUtils.findPosWithAlert(id)
        if ret == SUCCESS:
            self.showPathFindingIcon(True)
        gameglobal.rds.sound.playSound(98)

    def onShowConsignWindow(self, *arg):
        itemId = arg[3][0].GetNumber()
        name = ID.data.get(itemId, {}).get('name', '')
        BigWorld.player().openAuctionFun(searchItemName=name)

    def onUseNewGuildTutorial(self, *arg):
        useNew = gameglobal.rds.configData.get('enableGuildTutorialNew', False)
        return GfxValue(useNew)

    def updateGuildTutorialLoader(self):
        if self.mediator:
            useNew = gameglobal.rds.configData.get('enableGuildTutorialNew', False)
            self.mediator.Invoke('updateGuildTutorialLoader', GfxValue(useNew))

    def onGotoTrack(self, *arg):
        trackId = arg[3][0].GetString()
        trackId = uiUtils.findTrackId(trackId)
        uiUtils.gotoTrack(trackId)

    def onGuildHelp(self, *arg):
        questId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.seekGuildHelpOnQuest(questId)

    def onShowHotKeySetting(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_KEY)

    def onGetHotKeyDesc(self, *arg):
        key, mods, desc = getKeyContent(hotkey.KEY_NEXT_TRACK_TAB)
        return GfxValue(gbk2unicode(desc))

    def needHideQuestTrackPanel(self):
        p = BigWorld.player()
        if p.inFightObserve():
            return True
        if p.isInPUBG():
            return True
        if p.inFuben():
            fubenNo = formula.getFubenNo(p.spaceNo)
            if self.needHideQuestTrack(fubenNo):
                return True
        return False

    def needHideQuestTrack(self, fubenNo):
        p = BigWorld.player()
        trackType = FD.data.get(fubenNo, {}).get('trackType', None)
        if trackType == TRACK_TYPE_HIDE_IN_FB:
            return True
        elif p.isPUBGFbNo(fubenNo):
            return True
        else:
            return False

    def resetQuestTrackOpacity(self):
        if self.needHideQuestTrackPanel():
            self.hideTrackPanel(1)
        else:
            self.hideTrackPanel(0)

    def hideTrackPanel(self, hide):
        if self.mediator is None:
            return
        else:
            self.mediator.Invoke('hideTrack', (GfxValue(hide), GfxValue(False)))
            gameglobal.rds.ui.questLog.setTrackListShow(not hide)
            return

    def onGetTrackInfo(self, *arg):
        hideKey = keys.SET_UI_INFO + '/questTrackWidget/hide'
        alphaKey = keys.SET_UI_INFO + '/questTrackWidget/alpha'
        autoKey = keys.SET_UI_INFO + '/questTrackWidget/autoTab'
        heightKey = keys.SET_UI_INFO + '/questTrackWidget/height'
        info = {}
        info['hideTrack'] = AppSettings.get(hideKey, 0)
        info['alpha'] = AppSettings.get(alphaKey, 0.0)
        info['autoTab'] = AppSettings.get(autoKey, 0)
        info['trackHeight'] = AppSettings.get(heightKey, 0.0)
        return uiUtils.dict2GfxDict(info)

    def onSaveTrackInfo(self, *arg):
        hide = int(arg[3][0].GetBool())
        alpha = arg[3][1].GetNumber()
        auto = int(arg[3][2].GetBool())
        if len(arg[3]) >= 4 and arg[3][3] is not None:
            height = arg[3][3].GetNumber()
        else:
            height = 0
        hideKey = keys.SET_UI_INFO + '/questTrackWidget/hide'
        alphaKey = keys.SET_UI_INFO + '/questTrackWidget/alpha'
        autoKey = keys.SET_UI_INFO + '/questTrackWidget/autoTab'
        heightKey = keys.SET_UI_INFO + '/questTrackWidget/height'
        AppSettings[hideKey] = hide
        AppSettings[alphaKey] = alpha
        AppSettings[autoKey] = auto
        AppSettings[heightKey] = height
        AppSettings.save()

    def onShowTargetInltMap(self, *arg):
        seekId = 0
        try:
            seekId = eval(arg[3][0].GetString())
        except:
            return

        if type(seekId) == types.TupleType:
            seekId = list(seekId)[0]
        gameglobal.rds.ui.littleMap.showTrackTarget(int(seekId))

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TASK_TRACKING:
            self.mediator = mediator
            self.refreshAvailableTutorialQuest()

    def onOpenTaskLog(self, *arg):
        questType = int(arg[3][0].GetString())
        questId = int(arg[3][1].GetString())
        avl = arg[3][2].GetBool()
        if questType == gametypes.QUEST_DISPLAY_TYPE_REGION:
            gameglobal.rds.ui.regionQuest.show(questId)
        elif questType == gametypes.QUEST_DISPLAY_TYPE_JOB:
            gameglobal.rds.ui.jobBoard.openJobDetail(questId)
        else:
            gameglobal.rds.ui.questLog.taskListIdx = questType
            gameglobal.rds.ui.questLog.isAvailable = avl
            gameglobal.rds.ui.questLog.isJob = False
            gameglobal.rds.ui.questLog._updateCurTaskIdx(questId)
            loopId = commQuest.getQuestLoopIdByQuestId(questId)
            did = QDID.data.get(loopId, 0)
            if did:
                gameglobal.rds.ui.delegationBook.showInitDid = did
                gameglobal.rds.ui.delegationBook.show(2)
            else:
                gameglobal.rds.ui.questLog.showTaskLog()

    def onSendTask(self, *arg):
        stype = int(arg[3][0].GetString())
        if stype == 3:
            return
        idx = int(arg[3][1].GetString())
        qd = QD.data.get(idx, {})
        taskName = qd.get('name', gameStrings.TEXT_ITEMQUESTPROXY_87)
        color = FCD.data['quest', 0]['color']
        msg = "<font color=\'%s\'>[<a href = \'event:task%s\'><u>%s</u></a>]</font>" % (color, str(idx), str(taskName))
        gameglobal.rds.ui.sendLink(msg)

    def gotoNextTab(self):
        if self.mediator:
            self.mediator.Invoke('gotoNextTab')

    def _extraOption(self):
        option = {}
        return option

    def showPathFindingIcon(self, show):
        if self.mediator != None:
            self.mediator.Invoke('showPathFindingIcon', GfxValue(show))
        BigWorld.player().topLogo.setAutoPathingVisible(show)

    def setLeaveBtnVisible(self, visible):
        if self.validateSpaceNo():
            if visible and self.showRipple:
                gameglobal.rds.ui.showStoryModeState('enter')
                self.showRipple = False
        if not visible and not self.showRipple:
            gameglobal.rds.ui.showStoryModeState('leave')
            self.showRipple = True

    def validateSpaceNo(self):
        p = BigWorld.player()
        for quest in p.quests:
            qData = QD.data.get(quest, {})
            if qData.has_key('questGroup'):
                qgData = QGD.data.get(qData['questGroup'], {})
                spaceNo = formula.getMapId(p.spaceNo)
                if spaceNo in qgData.get('mapIds', []):
                    return True

        return False

    def onHandleTextEvent(self, *arg):
        text = arg[3][0].GetString()
        eventType = text.split(',')[0]
        params = text.split(',')[1:]
        if eventType == 'NpcTk':
            ret = uiUtils.findPosWithAlert(params[0])
            if ret == SUCCESS:
                self.showPathFindingIcon(True)
        elif eventType == 'openUI':
            if int(params[0]) == uiConst.LINK_TYPE_PLAY_RECOMM:
                gameglobal.rds.ui.playRecomm.show()
            elif int(params[0]) == uiConst.LINK_TYPE_ROLE_INFO:
                gameglobal.rds.ui.roleInfo.show(int(params[1]))
            elif int(params[0]) == uiConst.LINK_TYPE_INVENTORY:
                gameglobal.rds.ui.inventory.show()
            elif int(params[0]) == uiConst.LINK_TYPE_SKILL:
                gameglobal.rds.ui.skill.show(int(params[1]))
            elif int(params[0]) == uiConst.LINK_TYPE_HELP_SPRITE:
                gameglobal.rds.ui.help.show()
            elif int(params[0]) == uiConst.LINK_TYPE_ABILITY_TREE:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ABILITY_TREE)

    @ui.callAfterTime()
    def refreshRegionList(self):
        wqdd = WQD.data
        p = BigWorld.player()
        questIds = [ qid for qid in getattr(p, 'worldQuests', []) if wqdd.get(qid, {}).get('areaId', 0) == gameglobal.rds.ui.regionQuest.areaId ]
        if self.showRegionComplete() and self.completeId not in questIds:
            questIds.append(self.completeId)
        avlSet = set(questIds)
        newAvl = avlSet.difference(self.avlRegionSet)
        oldAvl = self.avlRegionSet.difference(avlSet)
        self.qif.inflateRegionQuests(avlSet)
        self.avlRegionSet = avlSet
        if not self.mediator:
            return
        if self.curTab != TAB_REGION:
            if len(newAvl) > 0 or self.showRegionComplete():
                self.mediator.Invoke('newQuestNotify', (GfxValue(TAB_REGION), GfxValue(len(newAvl))))
            if len(oldAvl) > 0:
                self.mediator.Invoke('removeQuestNotify', (GfxValue(TAB_REGION), GfxValue(len(oldAvl))))
        else:
            self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
        if self.showRegionComplete():
            BigWorld.callback(10, self.regionCompleteTimeOut)

    def showRegionComplete(self):
        spaceNo = BigWorld.player().spaceNo
        isInFuben = formula.spaceInFuben(spaceNo)
        if isInFuben:
            return False
        if self.completeId == 0:
            return False
        val = BigWorld.player().getWorldQuestData(self.completeId, const.WAQD_TGT_VAR, 0)
        if val == 0:
            return False
        return True

    def onCheckRegionComplete(self, *args):
        return GfxValue(self.showRegionComplete())

    def regionCompleteTimeOut(self):
        self.completeId = 0
        self.refreshRegionList()

    @ui.callAfterTime()
    def refreshGuildTutorialList(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableNewGuild', False):
            guildTutorialSteps = p.guild.getTutorialStepIds() if p.guild else []
        else:
            guildTutorialSteps = []
        avlSet = set(guildTutorialSteps)
        if p.guild:
            giadd = GIAD.data
            for questId in giadd.keys():
                infoType = giadd.get(questId, {}).get('infoType', 0)
                if infoType == 1:
                    if not gameglobal.rds.ui.guild.isGuildActiveFinish(questId):
                        avlSet.add(SPECIAL_ID)
                        break
                elif infoType == 2:
                    if not gameglobal.rds.ui.guild.isLockedState(questId) and not gameglobal.rds.ui.guild.isGuildActiveFinish(questId):
                        avlSet.add(SPECIAL_ID)
                        break

        newAvl = avlSet.difference(self.avlGuildSet)
        oldAvl = self.avlGuildSet.difference(avlSet)
        self.qif.inflateGuildTutorialQuests(avlSet)
        self.avlGuildSet = avlSet
        if not self.mediator:
            return
        if self.curTab != TAB_GUILD:
            if len(newAvl) > 0:
                self.mediator.Invoke('newQuestNotify', (GfxValue(TAB_GUILD), GfxValue(len(newAvl))))
            if len(oldAvl) > 0:
                self.mediator.Invoke('removeQuestNotify', (GfxValue(TAB_GUILD), GfxValue(len(oldAvl))))
        else:
            self.mediator.Invoke('refreshTrackedContent', GfxValue(True))

    @ui.uiEvent(uiConst.WIDGET_TASK_TRACKING, events.EVENT_ENTER_GUILD_SPACE)
    def onEnterGuildSpace(self):
        if not self.mediator:
            return
        self.mediator.Invoke('selectTrackTab', GfxValue(TAB_GUILD))

    @ui.uiEvent(uiConst.WIDGET_TASK_TRACKING, events.EVENT_LEAVE_GUILD_SPACE)
    def onLeaveGuildSpace(self):
        if not self.mediator:
            return
        if self.curTab == TAB_GUILD:
            self.mediator.Invoke('selectTrackTab', GfxValue(TAB_SCENARIO))

    def showRegionNotice(self, questId):
        questName = WQD.data.get(questId, {}).get('name', '')
        path = 'worldQuest/%s.dds' % WQD.data.get(questId, {}).get('worldQuestBg', 'notFound')
        if self.mediator:
            self.mediator.Invoke('showRegionNotice', (GfxValue(gbk2unicode(questName)), GfxValue(path)))

    def onCancelTrack(self, *arg):
        stype = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        if stype == gametypes.QUEST_DISPLAY_TYPE_REGION:
            return
        if stype in QUEST_LOOP_DISPLAY_TYPES:
            realIdx = gameglobal.rds.ui.questLog._isCurrentQuest(idx, BigWorld.player().fetchAcQuestsList(stype)[0])
            BigWorld.player().cell.setQuestTracked(realIdx, gametypes.QUEST_TYPE_LOOP, False)
        else:
            realIdx = idx
            BigWorld.player().cell.setQuestTracked(realIdx, stype, False)
        if realIdx in gameglobal.rds.ui.questLog.checkList:
            gameglobal.rds.ui.questLog.checkList.remove(realIdx)
        if gameglobal.rds.ui.questLog.mediator:
            gameglobal.rds.ui.questLog.mediator.Invoke('cancelTrack', GfxValue(str(idx)))

    def refreshFubenTrack(self, isInFuben):
        if self.mediator:
            trackType = -1
            if not gameglobal.rds.configData.get('enableNewFubenTargetGuide', True):
                isInFuben = False
            if isInFuben:
                fubenNo = formula.getFubenNo(BigWorld.player().spaceNo)
                fgdData = FGD.data.get((fubenNo, 1), {})
                if fgdData:
                    trackType = FD.data.get(fubenNo, {}).get('trackType', 2)
                else:
                    isInFuben = False
            info = {'isInFuben': isInFuben,
             'trackType': trackType}
            self.mediator.Invoke('refreshFubenTrack', uiUtils.dict2GfxDict(info, True))

    def onGetFubenTrackType(self, *arg):
        trackType = -1
        spaceNo = BigWorld.player().spaceNo
        isInFuben = formula.spaceInFuben(spaceNo)
        if not gameglobal.rds.configData.get('enableNewFubenTargetGuide', True):
            isInFuben = False
        if isInFuben:
            fubenNo = formula.getFubenNo(spaceNo)
            fgdData = FGD.data.get((fubenNo, 1), {})
            if fgdData:
                trackType = FD.data.get(fubenNo, {}).get('trackType', 2)
            else:
                isInFuben = False
        info = {'isInFuben': isInFuben,
         'trackType': trackType}
        return uiUtils.dict2GfxDict(info, True)

    def onAutoAccQuest(self, *arg):
        questId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.autoAcceptQuest(questId)

    def onQuickGroup(self, *arg):
        if arg[3][0] is None:
            return
        else:
            groupInfo = []
            groupInfoGfx = uiUtils.gfxArray2Array(arg[3][0])
            p = BigWorld.player()
            if not uiUtils.groupMatchApplyCheck():
                return
            for i in range(0, len(groupInfoGfx)):
                groupInfo.append(int(groupInfoGfx[i].GetNumber()))

            p.onQEApplyGroupMatch(groupInfo[0], groupInfo[1], groupInfo[2], groupInfo[3])
            return

    def onRegionQuickGroup(self, *arg):
        if arg[3][0] is None:
            return
        else:
            activityId = int(arg[3][0].GetNumber())
            actIns = activityFactory.getInstance().actIns.get(activityId, None)
            if actIns:
                actIns.onGroupMatchClick()
            return

    def onQuestCompleted(self, event = None):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            self.refreshFindBeastOrNot(questId)
            self.removeQuestFromTrack(questId, 'completeQuest')
            return

    def onQuestAbandoned(self, event = None):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            self.removeQuestFromTrack(questId, 'abandonQuest')
            return

    def getTrackedIds(self, questId):
        return self.trackedIds.get(questId, [0])[0]

    def removeQuestFromTrack(self, questId, invokeFunc):
        oldIndex = self.getTrackedIds(questId) - 1
        questType = self.qif.removeQuest(questId)
        questTab = self.getTrackTabByQuestType(questType)
        self.qif.refreshQuestTrackIndex(self.trackedIds)
        if oldIndex == -1 or questTab < 0:
            return
        if not self.mediator:
            return
        if questTab == self.curTab:
            if oldIndex == 0:
                self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
            else:
                self.mediator.Invoke(invokeFunc, (GfxValue(questTab), GfxValue(oldIndex), GfxValue(questId)))
        else:
            self.mediator.Invoke('removeQuestNotify', GfxValue(questTab))

    def onQuestAccepted(self, event, isTracked = False):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            self.refreshFindBeastOrNot(questId)
            if not self.needShowQuestInTracker(questId):
                return
            questType, qItem = self.qif.addQuest(questId)
            questTab = self.getTrackTabByQuestType(questType)
            self.qif.refreshQuestTrackIndex(self.trackedIds)
            trackIdx = self.getTrackedIds(questId) - 1
            if trackIdx < 0 or questTab < 0:
                return
            if isTracked:
                trackIdx = 0
            if not self.mediator:
                return
            if questTab == self.curTab:
                qData = qItem.formatReturn()
                if trackIdx == 0:
                    self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
                else:
                    self.mediator.Invoke('acceptQuest', (GfxValue(questTab), GfxValue(trackIdx), uiUtils.dict2GfxDict(qData, True)))
            else:
                if questTab == TAB_SCENARIO and trackIdx == 0:
                    qItem.formatReturn()
                self.mediator.Invoke('newQuestNotify', GfxValue(questTab))
            return

    def needShowQuestInTracker(self, questId):
        showQuestTracker = QD.data.get(questId, {}).get('showQuestTracker', -1)
        if showQuestTracker >= 0:
            return showQuestTracker
        else:
            displayType = QD.data.get(questId, {}).get('displayType', 0)
            showQuestTracker = QTSD.data.get(displayType, {}).get('showQuestTracker', False)
            return showQuestTracker

    def onQuestInfoChanged(self, event = None):
        if event is None:
            return
        else:
            idSet = set(self.mqList) | set(event.data.get('mqList', []))
            self.mqList = list(idSet)
            self._onQuestInfoChanged()
            return

    @ui.callInCD(time=1)
    def _onQuestInfoChanged(self):
        qItemList = []
        indexList = []
        _bRefresh = False
        for questId in self.mqList:
            questType, qItem = self.qif.updateQuest(questId)
            self.qif.refreshQuestTrackIndex(self.trackedIds)
            questTab = self.getTrackTabByQuestType(questType)
            if questTab != self.curTab:
                if questTab == TAB_SCENARIO:
                    trackIdx = self.getTrackedIds(questId) - 1
                    if trackIdx == 0:
                        qItem.formatReturn(True)
                continue
            trackIndexs = self.trackedIds.get(questId, [0])
            for value in trackIndexs:
                trackIndex = value - 1
                if trackIndex < 0:
                    continue
                qItemList.append(qItem)
                indexList.append(trackIndex)
                if trackIndex == 0:
                    _bRefresh = True

        if len(qItemList) > 0 and self.mediator:
            qDataList = [ qItem.formatReturn(True) for qItem in qItemList ]
            if _bRefresh:
                self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
            else:
                self.mediator.Invoke('updateQuests', (GfxValue(self.curTab), uiUtils.array2GfxAarry(indexList, True), uiUtils.array2GfxAarry(qDataList, True)))
        gameglobal.rds.ui.littleMap.refreshNpcPos(self.qif)
        gameglobal.rds.ui.map.refreshNpcPos(self.qif)
        self.mqList = []

    def onQuestTrackChanged(self, event = None):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            isTracked = event.data.get('tracked', True)
            if not questId:
                return
            gameglobal.rds.ui.littleMap.refreshNpcPos(self.qif)
            gameglobal.rds.ui.map.refreshNpcPos(self.qif)
            if isTracked:
                self.onQuestAccepted(event, isTracked)
            else:
                self.onQuestAbandoned(event)
            return

    @ui.uiEvent(uiConst.WIDGET_TASK_TRACKING, RATQ_TRIGGER_EVENT)
    @ui.callAfterTime()
    def refreshAvailableTutorialQuest(self, event = None):
        p = BigWorld.player()
        tqdd = TQD.data
        avlSet = set((qId for qId in tqdd if p.availabelTutorialCheck(qId)))
        if avlSet == self.avlTutorialSet:
            return
        newAvl = avlSet.difference(self.avlTutorialSet)
        oldAvl = self.avlTutorialSet.difference(avlSet)
        for qid in newAvl:
            self.qif.addAvlTutorialQuest(qid)

        for qid in oldAvl:
            self.qif.removeAvlTutorialQuest(qid)

        self.qif.refreshQuestTrackIndex(self.trackedIds)
        gameglobal.rds.ui.littleMap.refreshNpcPos(self.qif)
        gameglobal.rds.ui.map.refreshNpcPos(self.qif)
        if not self.mediator:
            return
        if self.curTab != TAB_TUTORIAL:
            if len(oldAvl) > 0 and self.qif.countTabContentNum(TAB_TUTORIAL) != 0:
                self.mediator.Invoke('newQuestNotify', (GfxValue(TAB_TUTORIAL), GfxValue(len(newAvl))))
            if len(newAvl) > 0:
                self.mediator.Invoke('removeQuestNotify', (GfxValue(TAB_TUTORIAL), GfxValue(len(oldAvl))))
        else:
            self.mediator.Invoke('refreshTrackedContent', GfxValue(True))
        self.avlTutorialSet = avlSet

    def getTrackTabByQuestType(self, qType):
        for k, v in TAB_CONFIG.items():
            if qType in v[0]:
                return k

        return -1

    def resetFubenTargetGuideInfo(self):
        self.fbNo = None
        self.fbStage = None
        self.fbInfo = {}

    def onGetFubenTargetGuideInfo(self, *arg):
        self.refreshFubenTargetGuideInfo()

    def onCheckQuestTrackItemInfo(self, *arg):
        questId = int(arg[3][0].GetNumber())
        questType, qItem = self.qif.updateQuest(questId)
        if qItem:
            return uiUtils.dict2GfxDict(qItem.formatReturn(), True)

    def refreshFubenTargetGuideInfo(self):
        if self.mediator:
            info = {}
            fbMode = gameglobal.rds.ui.currentShishenMode
            info['fbMode'] = fbMode
            info['fbName'] = self.getFbName(self.fbNo, fbMode)
            fgdData = FGD.data.get((self.fbNo, self.fbStage), {})
            info['title'] = fgdData.get('title', '')
            info['titleDesc'] = fgdData.get('titleDesc', '')
            info['isReach'] = self.fbInfo.get(fgdData.get('stageTag', ''), False)
            fbArray = []
            if fgdData.has_key('reward'):
                reward = fgdData['reward']
                for rewardItem in reward:
                    if rewardItem[3] in self.fbInfo:
                        rewardCount = self.fbInfo.get(rewardItem[3], 0)
                        if rewardCount == None:
                            rewardCount = 0
                        rewardItemObj = {}
                        rewardItemObj['rewardDesc'] = rewardItem[2]
                        rewardItemObj['rewardMax'] = rewardItem[1][0]
                        rewardItemObj['rewardCount'] = rewardCount
                        fbArray.append(rewardItemObj)

            info['fbArray'] = fbArray
            if fbMode >= 4:
                shishenData = CSMD.data.get((fbMode, self.fbNo), {})
                shishenInfo = {}
                shishenInfo['atkLevel'] = shishenData.get('atkLevel', 0)
                shishenInfo['defLevel'] = shishenData.get('defLevel', 0)
                shishenInfo['aiLevel'] = shishenData.get('aiLevel', 0)
                shishenInfo['propRetrievalLevel'] = shishenData.get('propRetrievalLevel', 0)
                shishenInfo['tips'] = shishenData.get('tips', '')
                info['shishenInfo'] = shishenInfo
            self.mediator.Invoke('refreshFubenTargetGuideInfo', uiUtils.dict2GfxDict(info, True))

    def getFbName(self, spaceNo, currentMode):
        fbName = ''
        fbData = FD.data.get(spaceNo, {})
        baseName = fbData.get('name', '')
        fbName += baseName
        primaryLevelName = fbData.get('primaryLevelName', '')
        fbName += gameStrings.TEXT_HELPPROXY_512 + primaryLevelName
        shishenModeLevel = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        if currentMode > 4:
            currentMode = 4
        modeName = ''
        if currentMode > 0:
            modeName = shishenModeLevel[currentMode]
        elif currentMode == 0:
            modeName = fbData.get('modeName', '')
        fbName += gameStrings.TEXT_HELPPROXY_512 + modeName
        return fbName

    def updateFubenData(self, fbNo, fbStage, fbInfo):
        if self.fbNo == fbNo and self.fbStage == fbStage:
            self.fbInfo.update(fbInfo)
        else:
            self.fbInfo = fbInfo
        self.fbNo = fbNo
        self.fbStage = fbStage
        self.refreshFubenTargetGuideInfo()

    def updateWhenSpaceChange(self):
        if self.mediator and self.needRefreshMagnifier():
            self.mediator.Invoke('refreshTrackedContent', GfxValue(True))

    def needRefreshMagnifier(self):
        needFresh = False
        for tabId in TAB_CONFIG:
            allItem = self.qif.getQuestItemList(TAB_CONFIG[tabId][0])
            for qItems in allItem:
                for qItem in qItems:
                    if qItem.needRefreshMagnifier():
                        needFresh = True

        return needFresh

    def isTrackListShow(self):
        hideTrack = True
        if self.mediator:
            hideTrack = self.mediator.Invoke('getTrackHide').GetBool()
        return not hideTrack

    def needShowFindBeastTab(self):
        return True

    def onGetFindBeastTargetGuideInfo(self, *arg):
        self.refreshFindBeastTargetGuideInfo()

    def showFindBeastTrack(self, changeTab):
        if not self.mediator:
            return
        isShowTab = self.onGetIsShowFindBeast()
        isChangeTab = GfxValue(changeTab)
        self.mediator.Invoke('refreshFindBeastTrack', (isShowTab, isChangeTab))

    def refreshFindBeastTargetGuideInfo(self):
        if not self.mediator:
            return
        self.curInfo = self.getCurInfo()
        self.curInfo['showSeekBtn'] = self.needShowSeekBtn()
        self.curInfo['dealedLeaveTeamHint'] = self.getDealedLeaveTeamHint()
        self.curInfo['showNews'] = self.showNews and self.curInfo.get('specialSeekType') == 1
        self.mediator.Invoke('refreshFindBeastTargetGuideInfo', uiUtils.dict2GfxDict(self.curInfo, True))

    def refreshNews(self, isShow):
        self.showNews = isShow
        if self.curInfo and self.mediator:
            if self.curInfo.get('specialSeekType') != 1:
                return
            self.curInfo['showNews'] = isShow
            self.mediator.Invoke('refreshFindBeastNewsMc', GfxValue(self.curInfo.get('showNews', False)))

    def refreshLeaveHint(self, isShow):
        if self.curInfo and self.mediator:
            if self.curTab != TAB_FINDBEAST:
                return
            dealedLeaveTeamHint = self.getDealedLeaveTeamHint() if isShow else None
            self.mediator.Invoke('refreshFindBeastLeaveHintMc', GfxValue(gbk2unicode(dealedLeaveTeamHint)))

    def onHandleFindBeastGoto(self, *arg):
        self.doCurrFindBeastSeek()

    def getCurInfo(self):
        p = BigWorld.player()
        info = dict()
        questLoopChainId = self.initQuestLoopChainId()
        stageId = 0
        loop = p.questLoopInfo.get(questLoopChainId)
        loopInfo = loop.questInfo if loop else None
        currQuestId = loopInfo[-1][0] if loopInfo else None
        if loop is None:
            stageId = FINDBEAST_START
            item = self.getStartOrFinishItemByStageId(stageId)
            info.update(item)
        elif loop.getQuestLoopCnt(p, questLoopChainId):
            stageId = FINDBEAST_FINISH
            item = self.getStartOrFinishItemByStageId(stageId)
            info.update(item)
        else:
            questState = 0
            for k, v in QLCSD.data.iteritems():
                questIds = v.get('questId')
                if questIds and currQuestId in questIds:
                    questState = k[1]
                    info.update(v)
                    break

            for k, v in QLCD.data.iteritems():
                questStates = v.get('state')
                if questState and questState in questStates:
                    stageId = k[1]
                    break

        info['stageId'] = stageId
        info['stageNames'] = self.getAllStageName()
        info['rewardResult'] = self.calcReward(info.get('reward'))
        return info

    def calcReward(self, rewardId):
        if rewardId is None:
            return 0
        else:
            fd = FMLCD.data.get(rewardId)
            if not fd:
                return 0
            func = fd.get('formula')
            if not func:
                return 0
            p = BigWorld.player()
            res = gameStrings.FINDBEAST_EXPTEXT % func({'lv': p.lv,
             'carrierSatisfaction': p.carrierSatisfaction})
            return res

    def getAllStageName(self):
        stage = [None] * len(QLCD.data)
        for k, v in QLCD.data.iteritems():
            stage[k[1] - 1] = v.get('stageName')

        return stage

    def needShowConfirmView(self):
        p = BigWorld.player()
        questLoopChainId = self.initQuestLoopChainId()
        loop = p.questLoopInfo.get(questLoopChainId)
        if not loop:
            return False
        self.curInfo = self.getCurInfo()
        leaveTeamHint = self.curInfo.get('leaveTeamHint') if self.curInfo else None
        if not leaveTeamHint:
            return False
        condition = False
        if condition:
            return False
        else:
            return True

    def getDealedLeaveTeamHint(self):
        dealedLeaveTeamHint = self.curInfo.get('leaveTeamHint')
        if not dealedLeaveTeamHint:
            return None
        else:
            p = BigWorld.player()
            if p.isInTeam() or p.isInGroup():
                return None
            return dealedLeaveTeamHint

    def needShowSeekBtn(self):
        btnText = self.curInfo.get('btnText')
        if not btnText:
            return False
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        hideSeek = self.curInfo.get('hideSeek', False)
        if hideSeek and p.inFuben() and formula.whatFubenType(fbNo) in (const.FB_TYPE_GROUP,):
            return False
        return True

    def initQuestLoopChainId(self):
        if not self.questLoopChainId:
            ret = QLCD.data.keys()
            self.questLoopChainId = ret[0][0]
        return self.questLoopChainId

    def onGetIsShowFindBeast(self, *args):
        if not gameglobal.rds.configData.get('enableQuestLoopChain', False):
            return GfxValue(False)
        lvLimitL = -1
        lvLimitH = -1
        for item in PRID.data.itervalues():
            if item.get('funcType') == gametypes.RECOMMEND_TYPE_FIND_BEAST:
                lvLimitL, lvLimitH = item.get('lv')

        if lvLimitL == -1 or lvLimitH == -1:
            return GfxValue(False)
        curLv = BigWorld.player().lv
        if lvLimitL <= curLv <= lvLimitH:
            return GfxValue(True)
        else:
            return GfxValue(False)

    def getStartOrFinishItemByStageId(self, stageId):
        questState = FINDBEAST_START_STATE if stageId == FINDBEAST_START else FINDBEAST_FINISH_STATE
        for k, v in QLCSD.data.iteritems():
            if v.get('questState') == questState:
                return v

    def refreshFindBeastOrNot(self, questId):
        self.initFindBeastQuests()
        if questId not in self.findBeastQuests:
            return
        self.showFindBeastTrack(True)
        gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()

    def initFindBeastQuests(self):
        if self.findBeastQuests:
            return
        self.findBeastQuests = []
        for kState, vState in QLCSD.data.iteritems():
            questIds = vState.get('questId')
            questIds and self.findBeastQuests.extend(questIds)

    def doCurrFindBeastSeek(self):
        if self.curInfo is None:
            return
        else:
            specialSeekType = self.curInfo.get('specialSeekType')
            p = BigWorld.player()
            if not specialSeekType:
                seekId = self.curInfo.get('seekId')
                seekId and uiUtils.findPosWithAlert(seekId)
            elif specialSeekType == SPECIAL_SEEK_CUREBEAST:
                buffId = self.curInfo.get('buffId')
                buffId and p.cell.useSkillPosOfBuff(buffId, p.position)
            elif specialSeekType == SPECIAL_SEEK_MULTICARRIER:
                if p.carrier.isNoneState():
                    seekId = self.curInfo.get('seekId')
                    seekId and uiUtils.findPosWithAlert(seekId)
                elif p.carrier.isRunningState() and p.id not in p.carrier:
                    self.dynamicPathSearchStart()
            return

    def getCurrFindBeastSeekState(self):
        if self.curInfo is None:
            self.curInfo = self.getCurInfo()
        bShow = self.needShowSeekBtn()
        btnText = self.curInfo.get('btnText')
        return (btnText, bShow)

    def refreshFindBeastExpText(self):
        if not self.mediator:
            return
        elif self.curInfo is None:
            return
        else:
            self.curInfo['rewardResult'] = self.calcReward(self.curInfo.get('reward'))
            self.mediator.Invoke('refreshFindBeastOtherMc', uiUtils.dict2GfxDict(self.curInfo, True))
            return

    def dynamicPathSearchStart(self):
        self.searchPathCallbackHandle and BigWorld.cancelCallback(self.searchPathCallbackHandle)
        BigWorld.player().cell.reqCarrierPosition()
        self.searchPathCallbackHandle = BigWorld.callback(SCD.data.get('findBeastPathSearchInterval', 20), self.dynamicPathSearchStart)

    def dynamicPathSearchStop(self):
        if not self.searchPathCallbackHandle:
            return
        else:
            BigWorld.cancelCallback(self.searchPathCallbackHandle)
            self.searchPathCallbackHandle = None
            self.searchSpaceNo = None
            self.searchPosition = None
            return

    def needRestartFindPath(self, spaceNo, position):
        if not self.searchPathCallbackHandle:
            return False
        if self.searchSpaceNo == spaceNo and self.searchPosition == position:
            return False
        self.searchSpaceNo = spaceNo
        self.searchPosition = position
        return True

    def onIsInGuildSpace(self, *args):
        return GfxValue(utils.inRange(const.GUILD_SPACENO_RANGE, BigWorld.player().spaceNo))

    def onTeleportToStart(self, *args):
        startTrackId = int(args[3][0].GetNumber())
        msg = uiUtils.getTextFromGMD(GMDD.data.TELEPORTTO_QUESTSTART_TEXT)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.sendTeleportCMD, startTrackId))

    @ui.callFilter(10)
    def sendTeleportCMD(self, trackId):
        BigWorld.player().cell.teleportToTrackForNewbie(trackId)

    def handleClickTabSetting(self):
        if self.mediator:
            self.mediator.Invoke('handleClickTabSetting')

    def handleClickAlpha(self):
        if self.mediator:
            self.mediator.Invoke('handleClickAlpha')

    def showWorldBossTrack(self, changeTab):
        if not self.mediator:
            return
        isShowTab = self.onGetIsShowWorldBoss()
        isChangeTab = GfxValue(changeTab)
        self.mediator.Invoke('refreshWorldBossTrack', (isShowTab, isChangeTab))

    def onGetWorldBossInfo(self, *args):
        self.refreshWorldBossInfo()

    def refreshWorldBossInfo(self):
        if not self.mediator:
            return
        refId = worldBossHelper.getInstance().getCacheRefId()
        if not refId:
            self.mediator.Invoke('refreshWorldBossTrack', (GfxValue(False), GfxValue(False)))
            return
        worldBossDetail = worldBossHelper.getInstance().getWorldBossDetail(refId)
        if not worldBossDetail:
            self.mediator.Invoke('refreshWorldBossTrack', (GfxValue(False), GfxValue(False)))
            return
        bossInfo = self.getCurrWorldBossInfo(worldBossDetail)
        self.mediator.Invoke('refreshWorldBossInfo', uiUtils.dict2GfxDict(bossInfo, True))

    def getCurrWorldBossInfo(self, bossDetail):
        bossInfo = {}
        bossInfo['bossIcon'] = bossDetail['bossRoundIcon']
        bossInfo['bossName'] = bossDetail['bossName']
        bossInfo['rankList'] = bossDetail.get('guildRank', [])
        bossInfo['refId'] = bossDetail['refId']
        bossInfo['attendVal'] = self.getAttendStr(bossDetail)
        bossInfo['remainTime'] = max(bossDetail['ttl'] - (utils.getNow() - bossDetail['startTime']), 0)
        bossInfo['isLive'] = bossDetail['isLive']
        bossInfo['tipText'] = worldBossHelper.getInstance().getStageTipText()
        bossInfo['attendTip'] = DCD.data.get('worldBossAttendTip', '')
        return bossInfo

    def getAttendStr(self, bossDetail):
        attendVal = bossDetail.get('attendVal', '')
        worldBossNeedJoinInfo = DCD.data.get('worldBossNeedJoin', (10, 10))
        if bossDetail.get('isRare', False):
            worldBossNeedJoin = worldBossNeedJoinInfo[gametypes.WOLRD_BOSS_RARE]
        else:
            worldBossNeedJoin = worldBossNeedJoinInfo[gametypes.WOLRD_BOSS_NORMAL]
        attendVal = min(attendVal, worldBossNeedJoin)
        return gameStrings.WORLD_BOSS_ATTEND_TEXT % (int(attendVal), worldBossNeedJoin)

    def onGetIsShowWorldBoss(self, *args):
        return GfxValue(worldBossHelper.getInstance().isShowQuestTrack())

    def onShowWorldBossDetail(self, *args):
        refId = int(args[3][0].GetNumber())
        gameglobal.rds.ui.worldBossDetail.show(refId)

    def onSeekWorldBoss(self, *args):
        refId = int(args[3][0].GetNumber())
        worldBossHelper.getInstance().seekToWorldBoss(refId)
