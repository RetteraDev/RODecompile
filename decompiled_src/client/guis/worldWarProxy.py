#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import gametypes
import utils
import ui
import formula
import clientUtils
import commonWorldWar
import worldWarActivity
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from uiProxy import SlotDataProxy
from guis import events
from guis import activityFactory
from callbackHelper import Functor
from gameclass import PSkillInfo
from helpers import taboo
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import world_war_data as WWD
from data import world_war_config_data as WWCD
from data import region_server_config_data as RSCD
from cdata import game_msg_def_data as GMDD
from data import world_war_score_data as WWSD
from data import juewei_data as JD
from data import juewei_type_data as JWD
from data import bonus_data as BD
from data import npc_item_commit_data as NICD
from data import item_data as ID
from data import item_commit_config_data as ICCD
from data import fame_data as FD
from data import world_war_fort_data as WWFD
from data import world_war_relive_board_data as WWRBD
from data import world_war_battle_reward_data as WWBRD
from data import world_war_battle_task_reward_data as WWBTRD
from data import world_war_army_data as WWAD
from data import wing_world_army_data as WIWAD
from data import wing_world_config_data as WIWCD
WW_STEP_APPLY_CHALLENGE = 1
WW_STEP_OTHER_CHALLENGE = 2
WW_STEP_ROUND_DONE = 3
WW_STEP_ROUND_SKIPPED = 4
WW_BATTLE_ACTIDS = {1: 9,
 2: 10}
WW_SKILL_BINDING = 'skill'
WW_PS_SKILL_BINDING = 'psSkill'
WW_IMPEACH_REVIEW_VOTE = 0
WW_IMPEACH_REVIEW_VOTE_FINISH = 1

class WorldWarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(WorldWarProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCountryInfo': self.onGetCountryInfo,
         'getQuestInfo': self.onGetQuestInfo,
         'getDayActivies': self.onGetDayActivies,
         'getLuckyReward': self.onGetLuckyReward,
         'showChallenge': self.onShowChallenge,
         'showBid': self.onShowBid,
         'applyTargets': self.onApplyTargets,
         'clickFindPlace': self.onClickFindPlace,
         'clickFindNpcWithFly': self.onClickFindNpcWithFly,
         'clickFindPlaceWithFly': self.onClickFindPlaceWithFly,
         'clickFindNpc': self.onClickFindNPC,
         'getActivityDetail': self.onGetActivityDetail,
         'getJueWeiInfo': self.onGetJueWeiInfo,
         'clickJWLvUp': self.onClickJWLvUp,
         'showWorldWar': self.onShowWarldWar,
         'showKillRank': self.onShowKillRank,
         'showResourceRank': self.onShowResourceRank,
         'gotoWorldWarNpc': self.onGotoWorldWarNpc,
         'showDetailScore': self.onShowScoreDetail,
         'showCommitItem': self.onShowCommitItemBox,
         'commitItem': self.onCommitItem,
         'clickJoinAct': self.onClickJoinAct,
         'showWWBattleRank': self.onShowWWBattleRank,
         'showWWBattleTarget': self.onShowWWBattleTarget,
         'getJueWeiRecomendAct': self.onGetJueWeiRecomendAct,
         'showRewardDesc': self.onShowWWRewardDesc,
         'clickArmyOpBtn': self.onClickArmyOpBtn,
         'saveArmyNotice': self.onSaveArmyNotice,
         'refreshVoteList': self.onRefreshVoteList,
         'voteByGbId': self.onVoteByGbId,
         'getArmyInfo': self.onGetArmyInfo,
         'getArmyMgrInfo': self.onGetArmyMgrInfo,
         'showAppointWWAramy': self.onShowAppointWWAramy,
         'appointArmy': self.onAppointArmy,
         'markArmy': self.onMarkArmy,
         'clickWWArmySkill': self.onClickWWArmySkill,
         'showWWArmySkill': self.onShowWWArmySkill,
         'confirmWWImpeach': self.onConfirmWWImpeach,
         'impeachVote': self.onImpeachVote,
         'clickFightForOther': self.onClickFightForOther,
         'getImpeachReviewState': self.onGetImpeachReviewState,
         'refreshImpeachReview': self.onRefreshImpeachReview}
        self.bindType = 'worldWar'
        self.type = 'worldWar'
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onSpaceNoChanged, 0, True)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_CHALLEGNGE, self.hideChallenge)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_COMMIT_ITEM_VIEW, self.hideItemCommitView)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_COMMIT_ITEM_BOX, self.hideItemCommitBox)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_BATTLE_TARGET, self.hideWWTarget)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_ARMY_MARK, self.hideArmyMark)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_IMPEACH_START, self.hideWWImpeachStart)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_GUILD_SCORE_DETAIL, self.hideWWGuildScoreDetail)
        self.actFactory = activityFactory.getInstance()
        self.queueConfirmHandler = None
        self.battleQueueConfirmHandler = None
        self.wwRobConfirmHandler = None
        self.wwBattleMed = None
        self.wwIconMed = None
        self.battleResultData = None
        self.appointPostId = 0
        self.lastQueueType = -1
        self.macResult = 0
        self.wwQueueIdDict = {gametypes.WORLD_WAR_TYPE_NORMAL: -1,
         gametypes.WORLD_WAR_TYPE_BATTLE: -1,
         gametypes.WORLD_WAR_TYPE_ROB: -1,
         gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG: -1,
         gametypes.WORLD_WAR_TYPE_ROB_YOUNG: -1}
        self.wwQueueMedDict = {gametypes.WORLD_WAR_TYPE_NORMAL: None,
         gametypes.WORLD_WAR_TYPE_BATTLE: None,
         gametypes.WORLD_WAR_TYPE_ROB: None,
         gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG: None,
         gametypes.WORLD_WAR_TYPE_ROB_YOUNG: None}
        self.checkInactiveTimerId = 0
        self.notifyInactiveTimerId = 0
        self.bInactive = False
        self.tInactive = 0
        self.impeachVoteInfo = None
        self.impeachReviewState = WW_IMPEACH_REVIEW_VOTE
        self.serverListInfo = None
        self.impeachReviewClockId = None
        self.voteGroupType = 0
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        initData = None
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_WW_CHALLEGNGE:
            self.wwChallengMed = mediator
            initData = self.getChallegeData()
        elif widgetId == uiConst.WIDGET_WW_GUILD_SCORE_DETAIL:
            initData = self.getWWScoreData()
        elif widgetId == uiConst.WIDGET_WW_COMMIT_ITEM_VIEW:
            initData = self.getWWItemCommitData()
            self.commitMed = mediator
        elif widgetId == uiConst.WIDGET_WW_COMMIT_ITEM_BOX:
            initData = self.getWWCommitItemInfo()
        elif widgetId == uiConst.WIDGET_WW_BATTLE:
            self.wwBattleMed = mediator
            initData = self.getWWBattleData()
            self.uiAdapter.questTrack.hideTrackPanel(True)
        else:
            if widgetId == uiConst.WIDGET_WW_BATTLE_TARGET:
                initData = self.getWWBattleRewardData()
                return uiUtils.dict2GfxDict(initData, True)
            if widgetId == uiConst.WIDGET_WORLD_WAR_ICON:
                initData = {'tipTxt': WWCD.data.get('wwActNoFinishedTip', ''),
                 'allDone': worldWarActivity.isAllWWActDone(uiUtils.getWeekDay())}
                self.wwIconMed = mediator
            elif widgetId == uiConst.WIDGET_WW_ARMY_VOTE:
                initData = self.getVoteData()
                self.wwVoteMed = mediator
                p.cell.queryWorldWarArmyCandidate(p.worldWar.armyCandidateVer, p.worldWar.armyCandidateVoteVer)
            elif widgetId == uiConst.WIDGET_WW_ARMY_MARK:
                if gameglobal.rds.configData.get('enableWingWorld', False):
                    postList = gametypes.WING_WORLD_ARMY_SUPER_MGR_POST_IDS
                    initData = {'armyNames': [ WIWAD.data.get(post).get('categoryName') for post in postList ],
                     'markTips': WIWCD.data.get('armyMarkTips', ''),
                     'armyIds': postList}
                    self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_MARK)
                elif self.voteGroupType == gametypes.WW_ARMY_GROUP_TYPE_QINGLONG:
                    if not gameglobal.rds.configData.get('enableWorldWarArmyYoungGroup'):
                        postList = gametypes.WW_ARMY_SUPER_MGR_POST_IDS
                    else:
                        postList = gametypes.WW_ARMY_SUPER_MGR_POST_OLD
                    initData = {'armyNames': [ WWAD.data.get(post).get('categoryName') for post in postList ],
                     'markTips': WWCD.data.get('armyMarkTips', ''),
                     'armyIds': [ WWAD.data.get(post).get('category') for post in postList ]}
                else:
                    postList = gametypes.WW_ARMY_SUPER_MGR_POST_YOUNG
                    initData = {'armyNames': [ WWAD.data.get(post).get('categoryName') for post in postList ],
                     'markTips': WWCD.data.get('armyMarkTips', ''),
                     'armyIds': [ WWAD.data.get(post).get('category') for post in postList ]}
            elif widgetId == uiConst.WIDGET_WW_IMPEACH_START:
                self.wwImpeachStart = mediator
                initData = self.getWWImpeachStartData()
        if initData:
            return uiUtils.dict2GfxDict(initData, True)
        else:
            return

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_WW_CHALLEGNGE:
            self.hideChallenge()
        elif widgetId == uiConst.WIDGET_WW_COMMIT_ITEM_VIEW:
            self.hideItemCommitView()
            self.hideItemCommitBox()
        elif widgetId == uiConst.WIDGET_WW_COMMIT_ITEM_BOX:
            self.hideItemCommitBox()
        elif widgetId == uiConst.WIDGET_WW_BATTLE:
            self.hideWorldWarBattle()
        elif widgetId == uiConst.WIDGET_WW_BATTLE_TARGET:
            self.hideWWTarget()
        elif widgetId == uiConst.WIDGET_WW_ARMY_VOTE:
            self.hideWWArmyVote()
        elif widgetId == uiConst.WIDGET_WW_ARMY_MARK:
            self.hideArmyMark()
        elif widgetId == uiConst.WIDGET_WW_IMPEACH_START:
            self.hideWWImpeachStart()
        elif widgetId == uiConst.WIDGET_WW_GUILD_SCORE_DETAIL:
            self.hideWWGuildScoreDetail()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def show(self):
        if self.enableWorldWar():
            p = BigWorld.player()
            p.cell.queryWorldWar(p.worldWar.ver)
            p.cell.queryWorldWarKillAvatarRank()
            p.cell.queryWorldWarRecord(p.worldWar.recordVer)
            p.cell.queryWorldWarRank(p.worldWar.rankVer)
            p.cell.queryWorldWarArmy(p.worldWar.armyVer, p.worldWar.armyOnlineVer)
            p.cell.queryWWArmyMark(p.worldWar.armyMarkVer)
            if p.worldWar.getCountry().groupId not in gametypes.WORLD_WAR_GROUP:
                p.showGameMsg(GMDD.data.WORLD_WAR_NO_GROUP, ())
                return
            if p.worldWar.state == gametypes.WORLD_WAR_STATE_CLOSE:
                p.showGameMsg(GMDD.data.WORLD_WAR_NOT_OPEN, ())
                return

    def showWorldWarBattle(self):
        if self.enableWorldWarBattle():
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_BATTLE)
            p = BigWorld.player()
            p.cell.queryWorldWarBattleFort(p.worldWar.fortVer)

    def onShowWWBattleTarget(self, *args):
        if self.enableWorldWarBattle():
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_BATTLE_TARGET)

    def onShowWWBattleRank(self, *args):
        pass

    def onShowWWBattleResult(self, *args):
        if self.enableWorldWarBattle():
            p = BigWorld.player()
            modal = p.inWorldWarBattle()
            if p.inWorldWarBattle():
                pass
            elif not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY)
            elif p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE:
                self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_OLD)
            elif p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
                self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_YOUNG)

    def onGetJueWeiRecomendAct(self, *args):
        return uiUtils.dict2GfxDict(worldWarActivity.getRecommendActList(), True)

    def onShowWWRewardDesc(self, *args):
        self.wwBattleRewardDesc = unicode2gbk(args[3][0].GetString())

    def onClickArmyOpBtn(self, *args):
        if self.wwVoteMed:
            return
        self.voteGroupType = int(args[3][0].GetNumber())
        p = BigWorld.player()
        if self.voteGroupType == gametypes.WW_ARMY_GROUP_TYPE_BAIHU and p.lv > WWCD.data.get('voteLv', 69):
            if p.worldWar.inVotePhase():
                if p.worldWar.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE:
                    p.showGameMsg(GMDD.data.WW_ARMY_VOTE_LV_BH, ())
                    return
            else:
                p.showGameMsg(GMDD.data.WW_ARMY_MARK_LV_BH, ())
                return
        if p.worldWar.inVotePhase():
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_VOTE)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_MARK)

    def onSaveArmyNotice(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        flag, msg = self.uiAdapter.chat._tabooCheck(const.CHAT_CHANNEL_WORLD, msg)
        if not flag:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        p.cell.updateWWAnnoucement(msg)
        return GfxValue(True)

    @ui.callFilter(2)
    def onRefreshVoteList(self, *args):
        p = BigWorld.player()
        p.cell.queryWorldWarArmyCandidate(p.worldWar.armyCandidateVer, p.worldWar.armyCandidateVoteVer)

    def onVoteByGbId(self, *args):
        gbId = int(args[3][0].GetString())
        BigWorld.player().cell.voteWorldWarArmyCandidate(self.voteGroupType, gbId)

    def onGetArmyInfo(self, *args):
        postId = BigWorld.player().worldWar.getPostByGbId()
        ret = {'postIds': gametypes.WW_ARMY_SUPER_MGR_POST_IDS,
         'labels': [ WWAD.data.get(post).get('categoryName') for post in gametypes.WW_ARMY_SUPER_MGR_POST_IDS ],
         'idx': WWAD.data.get(postId, {}).get('category', 1) - 1,
         'enableWWArmySkill': gameglobal.rds.configData.get('enableWorldWarArmySkill', False),
         'armyDesc': WWCD.data.get('armyDesc', '')}
        return uiUtils.dict2GfxDict(ret, True)

    def onGetArmyMgrInfo(self, *args):
        postId = int(args[3][0].GetNumber())
        return uiUtils.dict2GfxDict(self.getArmyMgrInfo(postId), True)

    def onShowAppointWWAramy(self, *args):
        pass

    def onAppointArmy(self, *args):
        self.appointPostId = int(args[3][0].GetNumber())
        gbId = int(args[3][1].GetString())
        roleName = unicode2gbk(args[3][2].GetString())
        p = BigWorld.player()
        if gbId:
            msg = uiUtils.getTextFromGMD(GMDD.data.REMOVE_WW_ARMY_POST_MSG, '%s') % roleName
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.cell.removeWWArmyPost, gbId))

    def onMarkArmy(self, *args):
        score = uiUtils.gfxArray2Array(args[3][0])
        armyIds = uiUtils.gfxArray2Array(args[3][1])
        realScore = []
        realArmyIds = []
        size = len(score)
        for i in xrange(0, size):
            realScore.append(int(score[i].GetNumber()))
            realArmyIds.append(int(armyIds[i].GetNumber()))

        if gameglobal.rds.configData.get('enableWingWorld', False):
            self.uiAdapter.wingWorldOverView.onMarkArmy(realScore, realArmyIds)
            return
        p = BigWorld.player()
        if realScore and realArmyIds:
            msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ARMY_MARK_CONFIRM, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.markWWArmy, realScore, realArmyIds))
        else:
            p.showGameMsg(GMDD.data.WORLD_WAR_ARMY_MARK_ZORE, ())

    def markWWArmy(self, scores, armyIds):
        BigWorld.player().cell.markWWArmy(armyIds, scores)
        self.hideArmyMark()

    def onClickWWArmySkill(self, *args):
        BigWorld.player().showGameMsg(GMDD.data.USE_WW_ARMY_SKILL_MSG, ())

    def onShowWWArmySkill(self, *args):
        pass

    def onConfirmWWImpeach(self, *args):
        p = BigWorld.player()
        text = unicode2gbk(args[3][0].GetString())
        p.cell.wwArmyImpeachApply(text)

    def onImpeachVote(self, *arg):
        p = BigWorld.player()
        isAgree = int(arg[3][0].GetNumber())
        p.cell.wwArmyImpeachVote(isAgree)

    def onGetImpeachReviewState(self, *arg):
        p = BigWorld.player()
        data = {}
        data['state'] = self.impeachReviewState
        if p.wwscoreLastWeek < WWCD.data.get('candidateWWScore', 0):
            data['agree'] = gametypes.WW_ARMY_IMPEACH_NO_RIGHT_VOTE
        else:
            data['agree'] = BigWorld.player().wwArmyImpeachVoted
        return uiUtils.dict2GfxDict(data)

    def onRefreshImpeachReview(self, *arg):
        p = BigWorld.player()
        p.cell.queryWWArmyImpeach(0)
        self.refreshImpeachReview()

    def getVoteText(self):
        data = {}
        data['agreeText'] = gameStrings.TEXT_WORLDWARPROXY_436
        data['disagreeText'] = gameStrings.TEXT_WORLDWARPROXY_437
        data['abstainText'] = gameStrings.TEXT_WORLDWARPROXY_438
        return data

    def refreshImpeachReviewState(self, agree = 0):
        p = BigWorld.player()
        if p.wwscoreLastWeek < WWCD.data.get('candidateWWScore', 0):
            self.impeachReviewState = WW_IMPEACH_REVIEW_VOTE_FINISH
            return
        if agree:
            self.impeachReviewState = WW_IMPEACH_REVIEW_VOTE_FINISH
        else:
            self.impeachReviewState = WW_IMPEACH_REVIEW_VOTE

    def goToImpeachResult(self, agree):
        if agree == None:
            agree = 0
        self.wwImpeachReview.Invoke('goToImpeachResult', GfxValue(agree))

    def clearWidget(self):
        self.hideChallenge()
        self.hideArmyMark()

    def reset(self):
        self.wwChallengMed = None
        self.detailId = 0
        self.matchMsgId = None
        self.selectWeekDay = 0
        self.wwVoteMed = None
        self.selectActivityId = 0
        self.tabIdx = 1
        self.selServerWidget = None
        self.selServerBtn = None

    def enableWorldWar(self):
        return gameglobal.rds.configData.get('enableWorldWar', False)

    def enableWWNpcItemCommit(self):
        return gameglobal.rds.configData.get('enableWWNpcItemCommit', False)

    def enableWorldWarBattle(self):
        return gameglobal.rds.configData.get('enableWorldWarBattle', False)

    def enableWorldWarRob(self):
        return gameglobal.rds.configData.get('enableWorldWarRob', False)

    def enableWorldWarByType(self, wwtype):
        if wwtype == gametypes.WORLD_WAR_TYPE_NORMAL:
            return gameglobal.rds.configData.get('enableWorldWar', False)
        if wwtype == gametypes.WORLD_WAR_TYPE_BATTLE:
            return gameglobal.rds.configData.get('enableWorldWarBattle', False)
        if wwtype == gametypes.WORLD_WAR_TYPE_ROB:
            return gameglobal.rds.configData.get('enableWorldWarRob', False)

    def enableWorldWarArmy(self):
        return gameglobal.rds.configData.get('enableWorldWarArmy', False)

    def enableWWQuestGuide(self):
        return gameglobal.rds.configData.get('enableWWQuestGuide', False)

    def enableWorldWarBattleHire(self):
        return gameglobal.rds.configData.get('enableWorldWarBattleHire', False)

    def hideChallenge(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_CHALLEGNGE)

    def hideWWGuildScoreDetail(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_GUILD_SCORE_DETAIL)

    def showWWItemCommitView(self, npc, npcCommitId):
        if self.enableWWNpcItemCommit():
            self.commitNpc = npc
            self.npcComitId = npcCommitId
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_COMMIT_ITEM_VIEW)

    def showWWImpeachStart(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_WW_IMPEACH_START)

    def showWWImpeachReview(self, dto = None):
        if getattr(self, 'wwImpeachStart', None):
            return
        else:
            if dto:
                self.impeachVoteInfo = dto
            return

    def hideItemCommitView(self):
        self.commitNpc = None
        self.commitMed = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_COMMIT_ITEM_VIEW)

    def hideItemCommitBox(self):
        self.commitItemId = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_COMMIT_ITEM_BOX)

    def hideWorldWarBattle(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_BATTLE)
        self.wwBattleMed = None

    def hideWWTarget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_BATTLE_TARGET)

    def hideWWBattleResult(self):
        if BigWorld.player().inWorldWarBattle():
            BigWorld.player().cell.exitWorldWar()

    def hideWWBattleRank(self):
        pass

    def hideWWQueue(self, wwType):
        if self.wwQueueIdDict[wwType] >= 0:
            self.uiAdapter.unLoadWidget(self.wwQueueIdDict[wwType])
            self.wwQueueIdDict[wwType] = -1
            self.wwQueueMedDict[wwType] = None
            msgQueueType = self.getMsgQueueType(wwType)
            if BigWorld.player().inWWQueueByType(wwType):
                self.uiAdapter.pushMessage.addPushMsg(msgQueueType)
            else:
                self.uiAdapter.pushMessage.removePushMsg(msgQueueType)

    def hideWWArmyVote(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_ARMY_VOTE)
        self.wwVoteMed = None

    def hideArmyMark(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_ARMY_MARK)

    def hideWWImpeachStart(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_IMPEACH_START)
        self.uiAdapter.funcNpc.close()
        self.wwImpeachStart = None

    def closeWWImpeachStart(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WW_IMPEACH_START)
        self.wwImpeachStart = None

    def hideWWImpeachReview(self):
        p = BigWorld.player()
        self.wwImpeachReview = None
        if self.impeachReviewClockId:
            BigWorld.cancelCallback(self.impeachReviewClockId)
            self.impeachReviewClockId = None
        if p.worldWar.impeachState == gametypes.WW_ARMY_IMPEACH_STATE_VOTE:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_IMPEACH_VOTE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_IMPEACH_VOTE, {'click': self.onClickImpeachVotePushMessage})
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_IMPEACH_VOTE)

    def onClickImpeachVotePushMessage(self):
        self.showWWImpeachReview()

    def getMsgQueueType(self, queueType):
        msgQueueType = uiConst.WW_TYPE_TO_MESSAGE_TYPE[queueType]
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            if queueType == uiConst.WW_QUEUE_TYPE_BATTLE:
                msgQueueType = uiConst.MESSAGE_TYPE_WW_BATTLE_QUEUE
        return msgQueueType

    def getChallegeData(self):
        p = BigWorld.player()
        ww = p.worldWar
        country = ww.getCountry()
        cList = []
        initMedData = {'step': ww.state,
         'isAttack': country.camp == gametypes.WORLD_WAR_CAMP_ATTACK,
         'rankTxt': WWCD.data.get('applyTargetTips', {}).get(country.camp, gameStrings.TEXT_WORLDWARPROXY_609) % country.applyIdx,
         'bidDesc': WWCD.data.get('bidDesc', gameStrings.TEXT_WORLDWARPROXY_610) % country.bidDeclarePoint,
         'stepDes': WWCD.data.get('stepTimeDes', {1: 'des1',
                     2: 'des2',
                     4: 'des4'}),
         'countryList': cList,
         'intentTargets': ww.intentTargets,
         'isTargetApplyed': bool(ww.intentTargets and len(ww.intentTargets))}
        if ww.state == gametypes.WORLD_WAR_STATE_APPLY_TARGETS:
            initMedData['rankTxt'] = WWCD.data.get('applyTargetTips', {}).get(country.camp, gameStrings.TEXT_WORLDWARPROXY_617) % country.applyIdx
        else:
            initMedData['rankTxt'] = WWCD.data.get('applyTargetNormalTips', {}).get(country.camp, gameStrings.TEXT_WORLDWARPROXY_617) % country.applyIdx
        leftTime = max(0, ww.applyTargetsEndTime - utils.getNow())
        initMedData['leftTime'] = leftTime
        for c in ww.country.values():
            if ww.state == gametypes.WORLD_WAR_STATE_APPLY_TARGETS and country.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
                if not c.camp or c.camp == country.camp:
                    continue
            if c.hostId == country.hostId:
                continue
            if c.inLuckyWeek() or ww.luckyHostId == c.hostId:
                continue
            questStarLv, enemyQuestStarLv = p.worldWar.calcQuestStarLv(c.hostId)
            cList.append({'countryName': utils.getServerName(c.hostId),
             'zhanli': c.combatScore,
             'zhengZhan': c.declarePoint,
             'myQuestStar': questStarLv,
             'enemyQuestStar': enemyQuestStarLv,
             'hostId': c.hostId})

        return initMedData

    def refreshChallege(self):
        if self.wwChallengMed:
            self.wwChallengMed.Invoke('refreshView', uiUtils.dict2GfxDict(self.getChallegeData(), True))

    def refreshImpeachReviewTime(self):
        p = BigWorld.player()
        timeEnd = 0
        if hasattr(p.worldWar, 'impeachVoteEndTime'):
            timeEnd = p.worldWar.impeachVoteEndTime - utils.getNow()
            if timeEnd < 0:
                timeEnd = 0
            timeLeftTxt = gameStrings.IMPEACH_REVIEW_TIME_LEFT % utils.formatTimeStr(timeEnd, 'h:m:s')
            self.wwImpeachReview.Invoke('refreshTime', GfxValue(gbk2unicode(timeLeftTxt)))
        self.impeachReviewClockId = BigWorld.callback(1, self.refreshImpeachReviewTime)

    def refreshImpeachReview(self):
        if not getattr(self, 'wwImpeachReview', None):
            return
        elif not self.impeachVoteInfo:
            return
        else:
            p = BigWorld.player()
            if self.impeachReviewClockId:
                BigWorld.cancelCallback(self.impeachReviewClockId)
            self.refreshImpeachReviewTime()
            impeachText, voteEndTime, agreeNum, totalNum, leaderDTO, applyDTO = self.impeachVoteInfo
            applyGbId = applyDTO and applyDTO[0] or 0
            applyer = p.worldWar.getArmyByGbId(applyGbId)
            applyPhoto = p._getFriendPhoto(applyer, applyer.school, applyer.sex)
            applyPostName = WWAD.data.get(applyer.postId, {}).get('desc', '')
            applyName = applyer.name
            leaderGbId = leaderDTO and leaderDTO[0] or 0
            leader = p.worldWar.getArmyByGbId(leaderGbId)
            leaderPhoto = p._getFriendPhoto(leader, leader.school, leader.sex)
            leaderPostName = WWAD.data.get(leader.postId, {}).get('desc', '')
            leaderName = leader.name
            impeachRule = WWCD.data.get('impeachRule', '')
            impeachTitle = WWCD.data.get('impeachTitle', '%s_%s_%s_%s') % (applyPostName,
             applyName,
             leaderPostName,
             leaderName)
            if totalNum:
                value = float(agreeNum) / float(totalNum) * 100
            else:
                value = 0
            agreePercent = str('%.2f%%' % value)
            data = {'impeachText': impeachText,
             'voteEndTime': voteEndTime,
             'agreeNum': agreeNum,
             'totalNum': totalNum,
             'agreePercent': agreePercent,
             'leaderPhoto': leaderPhoto,
             'leaderName': leaderName,
             'leaderPostName': leaderPostName,
             'applyPhoto': applyPhoto,
             'applyName': applyName,
             'applyPostName': applyPostName,
             'impeachTitle': impeachTitle,
             'impeachRule': impeachRule}
            self.wwImpeachReview.Invoke('refreshView', uiUtils.dict2GfxDict(data, True))
            return

    def setImpeachVoteInfo(self, dto):
        p = BigWorld.player()
        self.impeachVoteInfo = dto
        self.refreshImpeachReviewState(p.wwArmyImpeachVoted)
        if getattr(self, 'wwImpeachReview', None):
            if self.impeachReviewState == WW_IMPEACH_REVIEW_VOTE_FINISH:
                self.goToImpeachResult(p.wwArmyImpeachVoted)
            self.refreshImpeachReview()

    def isJWCanLvUp(self):
        p = BigWorld.player()
        if p.jueWeiLv >= const.MAX_JUE_WEI_LV:
            return False
        jData = JD.data.get(p.jueWeiLv, {})
        needHonor = jData.get('needHonor', 0)
        if not p.enoughFame([(const.WW_HONOR_FAME_ID, needHonor)]):
            return False
        curJueWeiType = jData.get('type', 0)
        if curJueWeiType == 0 or curJueWeiType >= const.MAX_JUE_WEI_TYPE:
            return False
        nextJueWeiType = JD.data.get(p.jueWeiLv + 1, {}).get('type', 0)
        if curJueWeiType == nextJueWeiType:
            return False
        tData = JWD.data.get(curJueWeiType, {})
        needLv = tData.get('needLv', 0)
        if p.jueWeiLv < needLv:
            return False
        return True

    def worldWarApplyBid(self, declarePoint):
        BigWorld.player().cell.worldWarApplyBid(declarePoint)

    def showLucky(self):
        if self.matchMsgId:
            self.uiAdapter.messageBox.dismiss(self.matchMsgId, needDissMissCallBack=False)
        msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_MATCH_SUCC_LUCKY, gameStrings.TEXT_WORLDWARPROXY_732)
        self.matchMsgId = self.uiAdapter.messageBox.showMsgBox(msg, callback=self.hideChallenge)

    def applyEndTargetEnd(self):
        ww = BigWorld.player().worldWar
        if ww.getEnemyHostId():
            if self.matchMsgId:
                self.uiAdapter.messageBox.dismiss(self.matchMsgId, needDissMissCallBack=False)
            msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_MATCH_SUCC, gameStrings.TEXT_WORLDWARPROXY_741) % utils.getServerName(ww.getEnemyHostId())
            self.matchMsgId = self.uiAdapter.messageBox.showMsgBox(msg, callback=self.hideChallenge)
        elif ww.getCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
            if self.matchMsgId:
                self.uiAdapter.messageBox.dismiss(self.matchMsgId, needDissMissCallBack=False)
            msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_MATCH_FAIL, gameStrings.TEXT_WORLDWARPROXY_748)
            self.matchMsgId = self.uiAdapter.messageBox.showMsgBox(msg, callback=self.onShowChallenge)

    def clickPush(self, msgType):
        p = BigWorld.player()
        if msgType == uiConst.MESSAGE_TYPE_WW_BATTLE_QUEUE:
            p.cell.enterWorldWarEvent(gametypes.WORLD_WAR_TYPE_BATTLE)
        elif msgType in uiConst.MESSAGE_TYPE_TO_WW_TYPE:
            p.cell.enterWorldWarEvent(uiConst.MESSAGE_TYPE_TO_WW_TYPE[msgType])
        elif msgType == uiConst.MESSAGE_TYPE_WW_QUEUE:
            wwTicketHostId = p.worldWar.wwTicketHosts.get(gametypes.WORLD_WAR_TYPE_NORMAL, 0)
            p.cell.enterWorldWar(p.worldWar.getCountry(wwTicketHostId).camp)
        elif msgType == uiConst.MESSAGE_TYPE_WW_MATCH_SUCC:
            if self.matchMsgId:
                self.uiAdapter.messageBox.dismiss(self.matchMsgId, needDissMissCallBack=False)
            msg = ''
            ww = p.worldWar
            if ww.getCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                msg = uiUtils.getTextFromGMD(GMDD.data.WW_MATCH_ATTACK_NOTIFY, '')
                if msg:
                    msg = msg % (ww.applyRoleName,
                     ww.getCountry().declarePoint,
                     ww.monthRank and ww.monthRank or '--',
                     ww.bidDeclarePoint,
                     utils.getServerName(ww.getCountry().enemyHostId))
            elif ww.getCamp() == gametypes.WORLD_WAR_CAMP_DEFEND:
                msg = uiUtils.getTextFromGMD(GMDD.data.WW_MATCH_DEFEND_NOTIFY, '')
                if msg:
                    msg = msg % (ww.applyRoleName,
                     ww.getCountry().declarePoint,
                     ww.monthRank and ww.monthRank or '--',
                     utils.getServerName(ww.getCountry().enemyHostId))
            self.uiAdapter.pushMessage.removePushMsg(msgType)
            if msg:
                self.matchMsgId = self.uiAdapter.messageBox.showMsgBox(msg, yesBtnText=gameStrings.TEXT_WORLDWARPROXY_776, callback=self.onMatchSuccOK, textAlign='left')
            else:
                self.show()
        else:
            self.uiAdapter.pushMessage.removePushMsg(msgType)
            if msgType in (uiConst.MESSAGE_TYPE_WW_NO_BID, uiConst.MESSAGE_TYPE_WW_APPLY_TARGET, uiConst.MESSAGE_TYPE_WW_MATCH_FAIL):
                self.onShowChallenge()
            else:
                self.show()

    def onMatchSuccOK(self):
        self.show()

    def _getScoreInfo(self):
        p = BigWorld.player()
        ww = p.worldWar
        country = ww.getCountry()
        data = {}
        if ww.isLucky():
            data = {'hasScore': False,
             'content': WWCD.data.get('luckyScoreContent', '')}
        elif ww.lastEnemyHostId:
            if ww.lastEnemyHostId == ww.getCountry().enemyHostId and not ww.isRunning():
                data = {'hasScore': False,
                 'content': WWCD.data.get('noScoreContent', '')}
            else:
                data = {'hasScore': True}
                ww.recalcScore()
                myScore = ww.getCountry().score
                enemyScore = ww.getCountry(ww.lastEnemyHostId).score
                r = commonWorldWar.calcResult(myScore, enemyScore)
                if myScore == enemyScore:
                    r = const.TIE
                if ww.isRunning():
                    data['title'] = WWCD.data.get('wwCurrentResultLabel', '') % uiConst.WORLD_WAR_CURRENT_RESULT_NAME.get(r, '')
                else:
                    grade = country.gradeScoreDelta
                    data['title'] = WWCD.data.get('wwResultLabel', '') % (uiConst.WORLD_WAR_RESULT_NAME.get(r, ''), grade)
                data['myScore'] = myScore
                data['enemyScore'] = enemyScore
                data['myCountry'] = utils.getServerName(utils.getHostId())
                data['enemyCountry'] = utils.getServerName(ww.lastEnemyHostId)
        else:
            data = {'hasScore': False,
             'content': WWCD.data.get('noScoreContent', '')}
        return data

    def getWWScoreData(self):
        p = BigWorld.player()
        ww = p.worldWar
        c1 = ww.getCountry()
        c2 = ww.getCountry(ww.lastEnemyHostId)
        tmpScoreData = {}
        for rType in gametypes.WORLD_WAR_RECORD_JUDGE_TYPES:
            val1 = c1.record.get(rType, 0)
            val2 = c2.record.get(rType, 0)
            s1, s2 = commonWorldWar.judgeRecord(rType, c1, c2)
            tmpScoreData[rType] = {'tip': WWCD.data.get('wwRecoredTips', {}).get(rType, ''),
             'myValue': val1,
             'enemyValue': val2,
             'myScore': s1,
             'enemyScore': s2}

        self.dictAdd(tmpScoreData.get(gametypes.WORLD_WAR_RECORD_BATTLE), tmpScoreData.get(gametypes.WORLD_WAR_RECORD_BATTLE_YOUNG), ('tip',))
        tmpScoreData.pop(gametypes.WORLD_WAR_RECORD_BATTLE_YOUNG, None)
        self.dictAdd(tmpScoreData.get(gametypes.WORLD_WAR_RECORD_ROB), tmpScoreData.get(gametypes.WORLD_WAR_RECORD_ROB_YOUNG), ('tip',))
        tmpScoreData.pop(gametypes.WORLD_WAR_RECORD_ROB_YOUNG, None)
        data = {'myCountry': utils.getServerName(utils.getHostId()),
         'enemyCountry': utils.getServerName(ww.lastEnemyHostId),
         'scoreData': tmpScoreData.values()}
        return data

    def dictAdd(self, dis, source, excludeKey = ()):
        if not dis or not source:
            return
        for k, v in source.items():
            if k in excludeKey:
                continue
            if k in dis:
                dis[k] += v
            else:
                dis[k] = v

    def getWWItemCommitData(self):
        p = BigWorld.player()
        ww = p.worldWar
        if self.commitNpc:
            val = NICD.data.get(self.npcComitId, {})
            weekCnt = p.itemCommitInfo.get(self.npcComitId, {}).get('weeklyCnt', 0)
            weekCntMax = val.get('weeklyCnt', 0)
            dailyCntMax = val.get('dailyCnt', 0)
            items = []
            enemyScore = ww.getEnemyCountry().lastScore if ww.getEnemyHostId() else 0
            rate = utils.getWWItemCommiteRewardRate(p, ww.getCountry().lastScore, enemyScore)
            data = {'isClosed': False,
             'rateMsg': ICCD.data.get('itemCommitRateMsg', {}).get(rate, ''),
             'commitCntTxt': ICCD.data.get('commitCntTxt', '%s %s %s') % (dailyCntMax, weekCntMax, '%s/%s' % (weekCnt, weekCntMax)),
             'title': val.get('title', '')}
            for itemId in val.get('items', ()):
                itemData = ID.data.get(itemId, {})
                commitCnt = itemData.get('commitCnt', 0)
                inv = p.crossInv if p._isSoul() else p.inv
                cnt = inv.countItemInPages(itemId)
                itemCnt = uiUtils.convertNumStr(cnt, commitCnt)
                fameId = itemData.get('commitRewardFames', ((0, 0),))[0][0]
                rewardCnt = itemData.get('commitRewardFames', ((0, 0),))[0][1]
                items.append({'item': uiUtils.getGfxItemById(itemId, itemCnt),
                 'fameCnt': '%s%s' % (rewardCnt, FD.data.get(fameId, {}).get('name', ''))})

            data['commitItems'] = items
        else:
            data = {}
        return data

    def getWWCommitItemInfo(self):
        data = {}
        p = BigWorld.player()
        if self.commitItemId and self.commitNpc:
            itemData = ID.data.get(self.commitItemId, {})
            commitCnt = itemData.get('commitCnt', 0)
            inv = p.crossInv if p._isSoul() else p.inv
            cnt = uiUtils.convertNumStr(inv.countItemInPages(self.commitItemId), commitCnt)
            data['commitItem'] = uiUtils.getGfxItemById(self.commitItemId, cnt)
            rewardCnt = itemData.get('commitRewardFames', ((0, 0),))[0][1]
            fameId = itemData.get('commitRewardFames', ((0, 0),))[0][0]
            data['rewardCnt'] = '%s%s' % (rewardCnt, FD.data.get(fameId, {}).get('name', ''))
            val = NICD.data.get(self.npcComitId, {})
            weekCntMax = val.get('weeklyCnt', 0)
            dailyCntMax = val.get('dailyCnt', 0)
            weeklyCnt = p.itemCommitInfo.get(self.npcComitId, {}).get('weeklyCnt', 0)
            dailyCnt = p.itemCommitInfo.get(self.npcComitId, {}).get('dailyCnt', 0)
            hasExtraBonus = dailyCnt < dailyCntMax and weeklyCnt < weekCntMax
            data['hasExtraBonus'] = int(hasExtraBonus)
            if hasExtraBonus:
                extraItem, extraFame = [], []
                for itemId, amount in itemData.get('commitRewardItems', ()):
                    extraItem.append(uiUtils.getGfxItemById(itemId, amount))

                for fameId, amount in itemData.get('commitRewardExtraFames', ()):
                    extraFame.append('%s%s' % (amount, FD.data.get(fameId, {}).get('name', '')))

                data['extraItem'] = extraItem
                data['extraFame'] = extraFame
                data['cntMsg'] = ICCD.data.get('canExtraRewordMsg', '%s') % (dailyCntMax - dailyCnt)
            elif weeklyCnt >= weekCntMax:
                data['cntMsg'] = ICCD.data.get('commitWeekMax', '%s') % weekCntMax
            else:
                data['cntMsg'] = ICCD.data.get('commitDaily', '%s') % dailyCntMax
        return data

    def getWWBattleData(self, inclueFort = True):
        p = BigWorld.player()
        ww = p.worldWar
        resourceCore = ww.getCountry().battleRes
        data = {'endTime': ww.battleEndTime,
         'killTxt': ww.battleKillAvatar,
         'assitTxt': ww.battleAssist,
         'score': ww.battleScore,
         'resTxt': ww.battleRes,
         'extraTxt': WWCD.data.get('wwBattleResourceText', '%s') % resourceCore,
         'extraTxtTips': WWCD.data.get('wwBattleResourceTips', ''),
         'camp': ww.getBattleCamp(),
         'enableWorldWarBattleHire': gameglobal.rds.configData.get('enableWorldWarBattleHire', False)}
        if ww.getBattleCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
            data['attackName'] = utils.getServerName(p.getWBHostId())
            data['defendName'] = utils.getServerName(ww.getBattleEnemyHostId())
            data['attackScore'], data['defendScore'] = ww.getBattleScores(p.getWBHostId())
        else:
            data['defendName'] = utils.getServerName(p.getWBHostId())
            data['attackName'] = utils.getServerName(ww.getBattleEnemyHostId())
            data['defendScore'], data['attackScore'] = ww.getBattleScores(p.getWBHostId())
        if inclueFort:
            data['detail'] = self.getWWBattleFortData()
        data['awardLabel'] = gameStrings.TEXT_WORLDWARPROXY_961 if p._getWBHireHostId() else gameStrings.TEXT_WORLDWARPROXY_961_1
        data['isWBHire'] = bool(p._getWBHireHostId())
        return data

    def getWWBattleFortData(self):
        p = BigWorld.player()
        ww = p.worldWar
        detail = {}
        for fortId in sorted(WWFD.data.keys()):
            val = WWFD.data.get(fortId)
            camp = gametypes.WOLD_WAR_CAMP_NONE
            hostId = ww.getFortHostId(fortId)
            if hostId:
                camp = ww.getCountry(hostId).camp
            fortVal = {'camp': camp,
             'occupied': 0,
             'value': 100,
             'name': val.get('name', ''),
             'id': fortId,
             'shortName': val.get('shortName', fortId),
             'tips': val.get('tips', fortId),
             'inCombat': ww.getFort(fortId).inCombat}
            if val.get('type') == gametypes.WW_BATTLE_FORT_TYPE_YAOSAI:
                detail.setdefault('forts', []).append(fortVal)
            elif val.get('type') == gametypes.WW_BATTLE_FORT_TYPE_ZHENYING:
                detail.setdefault('camp', []).append(fortVal)

        for reliveId in sorted(WWRBD.data.keys()):
            val = WWRBD.data.get(reliveId)
            if val.get('canOccupy'):
                camp = gametypes.WOLD_WAR_CAMP_NONE
                hostId = ww.reliveBoard.get(reliveId)
                if hostId:
                    camp = ww.getCountry(hostId).camp
                reliveVal = {'camp': camp,
                 'shortName': val.get('shortName', reliveId),
                 'tips': val.get('tips', reliveId),
                 'name': val.get('name', ''),
                 'id': reliveId,
                 'inCombat': False}
                detail.setdefault('relive', []).append(reliveVal)
            else:
                detail.setdefault('relive', []).append({'name': val.get('name'),
                 'id': reliveId,
                 'tips': val.get('tips', reliveId)})

        return detail

    def getWWBattleResultData(self):
        data = {}
        if self.battleResultData:
            tops, myRankAll, winnerCamp, scores, taskIds, myRank = self.battleResultData
            p = BigWorld.player()
            ww = p.worldWar
            data['win'] = int(winnerCamp == ww.getBattleCamp())
            myName = utils.getServerName(p.getWBHostId())
            enemyName = utils.getServerName(ww.getBattleEnemyHostId())
            if ww.getBattleCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                data['attackName'] = myName
                data['defendName'] = enemyName
            else:
                data['attackName'] = enemyName
                data['defendName'] = myName
            data['attackScore'] = scores.get(gametypes.WORLD_WAR_CAMP_ATTACK, 0)
            data['defendScore'] = scores.get(gametypes.WORLD_WAR_CAMP_DEFEND, 0)
            data['isHired'] = p._getWBHireHostId() > 0
            if p._getWBHireHostId():
                data['myRank'] = gameStrings.TEXT_WORLDWARPROXY_1026
            else:
                data['myRank'] = myRankAll if myRankAll else gameStrings.TEXT_CLANWARPROXY_421
            if p.inWorldWarBattle():
                data['closeLabel'] = gameStrings.TEXT_WORLDWARPROXY_1030
            else:
                data['closeLabel'] = gameStrings.TEXT_BATTLEFIELDPROXY_197
            topData = [{'kill': ww.battleKillAvatar,
              'assist': ww.battleAssist,
              'res': ww.battleRes,
              'name': p.realRoleName,
              'score': ww.battleScore,
              'school': const.SCHOOL_DICT.get(p.school, '')}]
            for gbId, name, school, val in tops:
                score, kill, assist, res = val
                topData.append({'kill': kill,
                 'assist': assist,
                 'res': res,
                 'name': name,
                 'score': score,
                 'school': const.SCHOOL_DICT.get(school, '')})

            data['topData'] = topData
            data['star'] = len([ taskId for taskId in taskIds if not commonWorldWar.isWinTask(taskId) ])
            if scores.get(ww.getBattleCamp()) == 0:
                data['star'] = 0
            elif scores.get(ww.getBattleEnemyCamp()) == 0:
                data['star'] = 3
            wbHireHostId = p._getWBHireHostId()
            if wbHireHostId:
                rankBonusIds = []
                if p.worldWar.battleScore >= WWCD.data.get('battlePersonalRewardScore', 0):
                    rankBonusIds.append(WWCD.data.get('hireRewardBonusId', 0))
            else:
                rankBonusIds = [ww.getBattleRankReward(myRank)]
            taskPersonalReward = ww.getBattleTaskPersonalReward(taskIds)
            taskCountryReward = ww.getBattleTaskCountryReward(taskIds)
            rewardList = []
            for rewards in (rankBonusIds, taskPersonalReward, taskCountryReward):
                rewardItems = []
                for bonusId in rewards:
                    if bonusId:
                        itemId, cnt = clientUtils.genItemBonus(bonusId)[0]
                        rewardItems.append(itemId)

                if rewards == rankBonusIds:
                    if wbHireHostId and p.worldWar.battleScore >= WWCD.data.get('hireRewardScore', 100):
                        rewardItems.append(WWCD.data.get('hireRewardItemId', 0))
                rewardList.append(rewardItems)

            allRewardList = self.getWWBattleRewardData().get('list', [])
            for idx, val in enumerate(allRewardList):
                for v in val.get('list', []):
                    v['enabled'] = v.get('itemId', 0) in rewardList[idx]

            data['rewardList'] = allRewardList
            if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE or p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
                    data['groupTypeVisible'] = True
                    data['groupType'] = p.recentEnterWWType
                else:
                    data['groupTypeVisible'] = False
            else:
                data['groupTypeVisible'] = False
        return data

    def getWWBattleRewardData(self):
        p = BigWorld.player()
        ww = BigWorld.player().worldWar
        data = []
        isHired = BigWorld.player()._getWBHireHostId() > 0
        rewardWay = WWCD.data.get('rewardWayLabels', ('', '', ''))
        if isHired:
            hireRewardLabels = WWCD.data.get('hireRewardLabels', ('', ''))
            arr = []
            itemId = clientUtils.genItemBonus(WWCD.data.get('hireRewardBonusId', 0))[0][0]
            desc = WWCD.data.get('hireRewardBonusDesc', '')
            arr.append({'itemData': uiUtils.getGfxItemById(itemId),
             'desc': desc,
             'itemId': itemId})
            itemId = WWCD.data.get('hireRewardItemId', 0)
            desc = WWCD.data.get('hireRewardItemDesc', '')
            arr.append({'itemData': uiUtils.getGfxItemById(itemId),
             'desc': desc,
             'itemId': itemId})
            data.append({'list': arr,
             'title': hireRewardLabels[0],
             'rewardWay': rewardWay[0]})
            camp = ww.getBattleCamp()
            starLv1, starLv2 = ww.calcBattleQuestStarLv()
            arr = []
            for key in WWBTRD.data.keys():
                tmpCamp, lv1, lv2, _ = key
                if tmpCamp == camp and lv1 == starLv1 and lv2 == starLv2:
                    val = WWBTRD.data.get(key)
                    if val.get('hireBonusId'):
                        itemId, cnt = clientUtils.genItemBonus(val.get('hireBonusId'))[0]
                        arr.append({'itemData': uiUtils.getGfxItemById(itemId, cnt),
                         'desc': val.get('desc', ''),
                         'order': val.get('order', 0),
                         'itemId': itemId})

            arr.sort(cmp=lambda x, y: cmp(x['order'], y['order']))
            data.append({'list': arr,
             'title': hireRewardLabels[1],
             'rewardWay': rewardWay[0]})
        else:
            rewardLabels = WWCD.data.get('rewardLabels', ('', '', ''))
            arr = []
            wwBattleRankReward = WWCD.data.get('wwBattleRankReward', {}).get(p.recentEnterWWType, [])
            for val in wwBattleRankReward:
                itemId, cnt = clientUtils.genItemBonus(val.get('bonusId'))[0]
                arr.append({'itemData': uiUtils.getGfxItemById(itemId, cnt),
                 'desc': val.get('desc', ''),
                 'itemId': itemId})

            data.append({'list': arr,
             'title': rewardLabels[0],
             'rewardWay': rewardWay[0]})
            camp = ww.getBattleCamp()
            starLv1, starLv2 = ww.calcBattleQuestStarLv()
            arr = []
            for key in WWBTRD.data.keys():
                tmpCamp, lv1, lv2, _ = key
                if tmpCamp == camp and lv1 == starLv1 and lv2 == starLv2:
                    val = WWBTRD.data.get(key)
                    itemId, cnt = clientUtils.genItemBonus(val.get('bonusId'))[0]
                    arr.append({'itemData': uiUtils.getGfxItemById(itemId, cnt),
                     'desc': val.get('desc', ''),
                     'order': val.get('order', 0),
                     'itemId': itemId})

            arr.sort(cmp=lambda x, y: cmp(x['order'], y['order']))
            data.append({'list': arr,
             'title': rewardLabels[1],
             'rewardWay': rewardWay[1]})
            arr = []
            for key in WWBRD.data.keys():
                tmpCamp, lv1, lv2, _ = key
                if tmpCamp == camp and lv1 == starLv1 and lv2 == starLv2:
                    val = WWBRD.data.get(key)
                    itemId, cnt = clientUtils.genItemBonus(val.get('bonusId'))[0]
                    arr.append({'itemData': uiUtils.getGfxItemById(itemId, cnt),
                     'desc': val.get('desc', ''),
                     'order': val.get('order', 0),
                     'itemId': itemId})

            arr.sort(cmp=lambda x, y: cmp(x['order'], y['order']))
            data.append({'list': arr,
             'title': rewardLabels[2],
             'rewardWay': rewardWay[2]})
        ret = {'list': data,
         'isHired': isHired}
        return ret

    def getWWImpeachStartData(self):
        consumeItem = WWCD.data.get('impeachConsumeItems', None)
        consumeItemId = consumeItem[0][0]
        consumeItemNum = consumeItem[0][1]
        iconData = uiUtils.getGfxItemById(consumeItemId)
        p = BigWorld.player()
        inv = p.crossInv if p._isSoul() else p.inv
        cnt = inv.countItemInPages(consumeItemId)
        numStr = uiUtils.convertNumStr(cnt, consumeItemNum)
        iconData['count'] = numStr
        itemName = ID.data.get(consumeItemId, 0).get('name', '')
        return {'iconData': iconData,
         'itemName': itemName}

    def onGetCountryInfo(self, *args):
        p = BigWorld.player()
        ww = p.worldWar
        country = ww.getCountry()
        if ww.isLucky():
            step = WW_STEP_ROUND_SKIPPED
        elif ww.getEnemyHostId():
            step = WW_STEP_ROUND_DONE
        elif ww.applyGbId == p.gbId:
            step = WW_STEP_APPLY_CHALLENGE
        else:
            step = WW_STEP_OTHER_CHALLENGE
        info = {'currentStep': step,
         'groupId': country.groupId,
         'delcarePointTxt': gameStrings.TEXT_WORLDWARPROXY_1207 % country.declarePoint,
         'groupTxt': WWCD.data.get('generationNames', [gameStrings.TEXT_WORLDWARPROXY_1208] * 4)[country.groupId],
         'combatScoreTxt': gameStrings.TEXT_WORLDWARPROXY_1209 % country.combatScore,
         'applyNameTxt': gameStrings.TEXT_WORLDWARPROXY_1210 % ww.applyRoleName,
         'enemyTxt': gameStrings.TEXT_WORLDWARPROXY_1211 % RSCD.data.get(country.enemyHostId, {}).get('serverName', gameStrings.TEXT_ROLEINFOPROXY_2565) if country.enemyHostId else '',
         'luckTip': WWCD.data.get('luckTip', ''),
         'worldWarNpcMsg': WWCD.data.get('worldWarNpcMsg', ''),
         'gradeTxt': gameStrings.TEXT_WORLDWARPROXY_1214 % country.gradeScore,
         'inBlookWeek': ww.inBloodWeek(),
         'bloodWeekTip': WWCD.data.get('bloodWeekTip', '')}
        if country.camp:
            info['campTxt'] = WWCD.data.get('campDesc', {}).get(country.camp, '')
        else:
            info['campTxt'] = ''
        history = []
        for hostId, cnt in ww.winCount.items():
            winHostName = utils.getServerName(hostId)
            if winHostName:
                history.append({'serverName': winHostName,
                 'time': cnt})

        history.sort(cmp=lambda x, y: cmp(y['time'], x['time']))
        result = {'info': info,
         'history': history,
         'score': self._getScoreInfo()}
        result['enableArmy'] = self.enableWorldWarArmy()
        opLabel = gameStrings.TEXT_WORLDWARPROXY_1230
        if ww.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE:
            opLabel = gameStrings.TEXT_WORLDWARPROXY_1232
        elif ww.inVotePhase():
            opLabel = gameStrings.TEXT_WORLDWARPROXY_1234
        armyInfo = {'notice': ww.announcement,
         'noticeMaxChars': WWCD.data.get('armyNoticeMaxChars', 100),
         'enableEditNotice': ww.getPostByGbId() == gametypes.WW_ARMY_LEADER_POST_ID,
         'opLabel': opLabel}
        if not gameglobal.rds.configData.get('enableWorldWarArmyYoungGroup', False):
            armyInfo['opVisibleOld'] = (ww.inVotePhase() or not p.wwArmyMark) and p.worldWar.armyState != gametypes.WORLD_WAR_ARMY_STATE_CLOSE
        else:
            wwArmyMarkYoung = False
            wwArmyMarkOld = False
            if p.wwArmyMark.get(gametypes.WW_ARMY_YOUNG_LEADER_POST_ID, -1) >= 0:
                wwArmyMarkYoung = True
            if p.wwArmyMark.get(gametypes.WW_ARMY_SUPER_MGR_POST_OLD[0], -1) >= 0 or p.wwArmyMark.get(gametypes.WW_ARMY_SUPER_MGR_POST_OLD[1], -1) >= 0:
                wwArmyMarkOld = True
            armyInfo['opVisibleOld'] = (ww.inVotePhase() or not wwArmyMarkOld) and p.worldWar.armyState != gametypes.WORLD_WAR_ARMY_STATE_CLOSE
            armyInfo['opVisibleYoung'] = (ww.inVotePhase() or not wwArmyMarkYoung) and p.worldWar.armyState != gametypes.WORLD_WAR_ARMY_STATE_CLOSE
        armyMgrs = []
        for postId in gametypes.WW_ARMY_SUPER_MGR_POST_IDS:
            val = ww.getArmyByPostId(postId)
            name = val.name if val else gameStrings.TEXT_BATTLEFIELDPROXY_1605
            if val and postId in gametypes.WW_ARMY_SUPER_MGR_POST_OLD:
                armyInfo['opVisibleOld'] = True
            if val and postId == gametypes.WW_ARMY_YOUNG_LEADER_POST_ID:
                armyInfo['opVisibleYoung'] = True
            star = p.worldWar.armyMark.get(postId, (0, 0))[0]
            armyMgrs.append({'impeached': False,
             'title': WWAD.data.get(postId).get('categoryName', ''),
             'name': '%s:%s' % (WWAD.data.get(postId).get('name', ''), name),
             'star': star})

        armyInfo['armyMgrs'] = armyMgrs
        result['armyInfo'] = armyInfo
        return uiUtils.dict2GfxDict(result, True)

    def onGetQuestInfo(self, *args):
        p = BigWorld.player()
        scoreLvs = []
        score = p.getFame(const.WW_WAR_SCORE_FAME_ID)
        itemMsg = ''
        rewardItemIds = []
        for key in sorted(WWSD.data.keys()):
            val = WWSD.data.get(key, {})
            tmpScore = val.get('score', 0)
            if tmpScore > score and not itemMsg:
                itemMsg = gameStrings.TEXT_WORLDWARPROXY_1284 % (tmpScore - score, val.get('name', ''))
                fixedBounus = BD.data.get(val.get('bonusId', 0), {}).get('fixedBonus')
                if fixedBounus:
                    for _, itemId, _ in fixedBounus:
                        rewardItemIds.append(itemId)

                starLv = p.getWorldWarQuestStarLv()
                starBonusId = val.get('starBonusId%s' % starLv, 0)
                if starBonusId:
                    rewardItemIds.append(BD.data.get(starBonusId).get('fixedBonus')[0][1])
                if p.worldWar.getCountry().groupId == gametypes.WORLD_WAR_GROUP_WANGZHE and gameglobal.rds.configData.get('enableWorldWarUpgrade', False):
                    wzBonusId = val.get('zhengbaBonusId', 0)
                    if wzBonusId:
                        rewardItemIds.append(BD.data.get(wzBonusId).get('fixedBonus')[0][1])
                rewardItemIds = utils.filtItemByConfig(rewardItemIds, lambda e: e)
            scoreLvs.append(tmpScore)

        dayLabels = WWCD.data.get('dayLabels', {}).get(p.worldWar.getCountry().camp, [''] * 7)
        questStarLv, enemyQuestStarLv = p.worldWar.calcQuestStarLv(p.worldWar.getCountry().enemyHostId)
        wwQuestItem = WWCD.data.get('wwQuestItem', 331931)
        usedNum = uiUtils.getItemUseNum(wwQuestItem, gametypes.ITEM_USE_LIMIT_TYPE_DAY)
        usedLimit = uiUtils.getItemUseLimit(wwQuestItem, gametypes.ITEM_USE_LIMIT_TYPE_DAY)
        result = {'itemMsg': itemMsg,
         'rewardItem': [ uiUtils.getGfxItemById(id) for id in reversed(rewardItemIds) ],
         'maxEnemy': p.getFameMaxVal(const.WW_KILL_ENEMY_FAME_ID),
         'enemy': p.getFame(const.WW_KILL_ENEMY_FAME_ID),
         'maxResource': p.getFameMaxVal(const.WW_RESORCE_FAME_ID),
         'resource': p.getFame(const.WW_RESORCE_FAME_ID),
         'maxShiQi': p.getFameMaxVal(const.WW_MORALE_FAME_ID),
         'shiQi': p.getFame(const.WW_MORALE_FAME_ID),
         'questStar': questStarLv,
         'enemyQuestStar': enemyQuestStarLv,
         'dayLabels': dayLabels,
         'maxScore': p.getFameMaxVal(const.WW_WAR_SCORE_FAME_ID),
         'scoreTxt': gameStrings.TEXT_WORLDWARPROXY_1317 % score,
         'score': score,
         'scoreLvs': scoreLvs,
         'killEnemyDesc': WWCD.data.get('killEnemyDesc', gameStrings.TEXT_WORLDWARPROXY_1320),
         'resouceDesc': WWCD.data.get('resouceDesc', gameStrings.TEXT_WORLDWARPROXY_1321),
         'moraleDesc': WWCD.data.get('moraleDesc', gameStrings.TEXT_WORLDWARPROXY_1322),
         'dayDesc': WWCD.data.get('wwDayDesc', {}).get(p.worldWar.getCamp(), [''] * 7)[uiUtils.getWeekDay()],
         'currentDay': uiUtils.getWeekDay(),
         'hasQuest': p.worldWar.getCountry().enemyHostId > 0 and p.worldWar.getCamp(),
         'enableWWGuide': self.enableWWQuestGuide(),
         'useItemCnt': '%s/%s' % (usedNum, usedLimit),
         'wwQuestItemData': uiUtils.getGfxItemById(wwQuestItem)}
        return uiUtils.dict2GfxDict(result, True)

    def onGetDayActivies(self, *args):
        weekDay = int(args[3][0].GetNumber())
        self.selectWeekDay = weekDay
        if self.enableWWQuestGuide():
            ret = worldWarActivity.getActInfosByDay(weekDay)
        else:
            ret = self._getWWActFromActBasic(weekDay)
        result = {'activities': ret}
        if self.selectActivityId:
            for idx, val in enumerate(ret):
                if val.get('actId') == self.selectActivityId:
                    result['selectIdx'] = idx
                    break

        return uiUtils.dict2GfxDict(result, True)

    def onGetLuckyReward(self, *args):
        BigWorld.player().cell.applyWorldWarLuckyHostAward()

    def onShowChallenge(self, *args):
        if self.enableWorldWar():
            p = BigWorld.player()
            p.cell.queryWorldWarCountries(p.worldWar.countryVer)
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_CHALLEGNGE)

    def onShowBid(self, *args):
        self.uiAdapter.messageBox.showYesNoInput(gameStrings.TEXT_WORLDWARPROXY_1357, self.worldWarApplyBid)

    def onApplyTargets(self, *args):
        source = args[3][0]
        size = source.GetArraySize()
        result = []
        for i in range(size):
            result.append(int(source.GetElement(i).GetNumber()))

        if result:
            BigWorld.player().cell.worldWarApplyTargets(result)

    def onClickFindNPC(self, *arg):
        buttonIdx = int(arg[3][0].GetNumber())
        i = int(arg[3][1].GetString())
        actIns = self.actFactory.actIns.get(self.detailId, None)
        if not actIns.canBeTrack():
            raise Exception('onClickFindNPC:this is activity can not be track!!!')
        indexList = actIns.getIndexList()
        if i < 0 or i >= len(indexList):
            return
        else:
            index = indexList[i]
            npcIds = actIns.getNPCId()
            if index < 0 or index >= len(npcIds):
                return
            seekId = npcIds[index]
            if buttonIdx == uiConst.LEFT_BUTTON:
                uiUtils.findPosById(str(seekId))
            elif buttonIdx == uiConst.RIGHT_BUTTON:
                gameglobal.rds.ui.littleMap.showTrackTarget(seekId)
            gameglobal.rds.uiLog.addPathLog(seekId)
            return

    def onClickFindPlace(self, *arg):
        buttonIdx = int(arg[3][0].GetNumber())
        i = int(arg[3][1].GetString())
        actIns = self.actFactory.actIns.get(self.detailId, None)
        if not actIns.canBeTrack():
            raise Exception('onClickFindPlace: this is activity can not be track!!!')
        indexList = actIns.getIndexList()
        if len(indexList) == 0 or i >= len(indexList) or i < 0:
            return
        else:
            index = indexList[i]
            seekId = actIns.getPlaceId()[index]
            if buttonIdx == uiConst.LEFT_BUTTON:
                uiUtils.findPosById(str(seekId))
            elif buttonIdx == uiConst.RIGHT_BUTTON:
                gameglobal.rds.ui.littleMap.showTrackTarget(seekId)
            gameglobal.rds.uiLog.addPathLog(seekId)
            return

    def onClickFindNpcWithFly(self, *arg):
        i = int(arg[3][0].GetString())
        actIns = self.actFactory.actIns.get(self.detailId, None)
        if actIns is None:
            return
        else:
            if not actIns.canBeTrack():
                raise Exception('onClickFindNPC:this is activity can not be track!!!')
            indexList = actIns.getIndexList()
            if len(indexList) == 0 or i >= len(indexList) or i < 0:
                return
            index = indexList[i]
            seekId = actIns.getNPCId()[index]
            uiUtils.gotoTrack(seekId)
            gameglobal.rds.uiLog.addFlyLog(seekId)
            return

    def onClickFindPlaceWithFly(self, *arg):
        i = int(arg[3][0].GetString())
        actIns = self.actFactory.actIns.get(self.detailId, None)
        if actIns is None:
            return
        else:
            if not actIns.canBeTrack():
                raise Exception('onClickFindPlace: this is activity can not be track!!!')
            indexList = actIns.getIndexList()
            if len(indexList) == 0 or i >= len(indexList) or i < 0:
                return
            index = indexList[i]
            seekId = actIns.getPlaceId()[index]
            uiUtils.gotoTrack(seekId)
            gameglobal.rds.uiLog.addFlyLog(seekId)
            return

    def onGetActivityDetail(self, *arg):
        self.detailId = int(arg[3][0].GetNumber())
        if self.enableWWQuestGuide():
            return uiUtils.dict2GfxDict(worldWarActivity.getActDetail(self.detailId, self.selectWeekDay), True)
        else:
            actIns = self.actFactory.actIns.get(self.detailId, None)
            gameglobal.rds.uiLog.addItemLog(self.detailId)
            return actIns.getItemDetail(self.selectWeekDay)

    def onClickJoinAct(self, *args):
        actId = int(args[3][0].GetNumber())
        if self.enableWWQuestGuide():
            worldWarActivity.getActById(actId, self.selectWeekDay).onBtnClick()
        else:
            actIns = self.actFactory.actIns.get(actId, None)
            actIns.onActionBtnClick()

    def onClickFightForOther(self, *args):
        p = BigWorld.player()
        if p.getWBHireState() == gametypes.WB_HIRE_UNHIRED:
            p.cell.queryWBHireInfo(p.worldWar.hireVer)
        else:
            wwtype = commonWorldWar.getBattleHireTypeByLevel(p.lv)
            p.cell.enterWorldWarEvent(wwtype)

    def onGetJueWeiInfo(self, *arg):
        p = BigWorld.player()
        ww = p.worldWar
        honorFameWeekMax = JD.data.get(p.jueWeiLv, {}).get('maxHonourWeekly', 0)
        contribFameWeekMax = JD.data.get(p.jueWeiLv, {}).get('maxContribWeekly', 0)
        calcJWLv = p.jueWeiLv
        honor = p.getFame(const.WW_HONOR_FAME_ID)
        for key, data in JD.data.items():
            if data.has_key('needHonor') and data.get('needHonor', 0) <= honor and key < const.MAX_JUE_WEI_LV:
                calcJWLv = key + 1
            else:
                break

        if calcJWLv >= const.MAX_JUE_WEI_LV + 1:
            progress = 1
        else:
            progress = (calcJWLv - 1) * 1.0 / const.MAX_JUE_WEI_LV
            lastLvNeedHonor = JD.data.get(calcJWLv - 1, {}).get('needHonor', 0)
            lvNeedHonor = JD.data.get(calcJWLv, {}).get('needHonor', 0)
            progress = min(progress + (honor - lastLvNeedHonor) * 1.0 / (lvNeedHonor - lastLvNeedHonor) / const.MAX_JUE_WEI_LV, 1)
        rankDefaultTxt = gameStrings.TEXT_WORLDWARPROXY_1494
        contriWeek = p.fameWeek.get(const.WW_CONTRIB_FAME_ID, (0, contribFameWeekMax))[0]
        honnorWeek, honnorWeekMax = p.fameWeek.get(const.WW_HONOR_FAME_ID, (0, honorFameWeekMax))
        honnorWeetStr = honnorWeek if honnorWeek < honnorWeekMax else gameStrings.TEXT_WORLDWARPROXY_1497 % honnorWeek
        result = {'lv': p.jueWeiLv,
         'name': JD.data.get(p.jueWeiLv, {}).get('name', gameStrings.TEXT_WORLDWARPROXY_1499),
         'honorWeek': gameStrings.TEXT_WORLDWARPROXY_1500 + uiUtils.toHtml(honnorWeetStr, '#FFFFFF'),
         'honorMax': p.getFameMaxVal(const.WW_HONOR_FAME_ID),
         'honor': p.getFame(const.WW_HONOR_FAME_ID),
         'progress': progress,
         'contrib': p.getFame(const.WW_CONTRIB_FAME_ID),
         'contribWeek': contriWeek if contriWeek < contribFameWeekMax else gameStrings.TEXT_WORLDWARPROXY_1497 % contriWeek,
         'contribWeekMax': contribFameWeekMax,
         'killEnemy': ww.killAvatarCnt,
         'rank': ww.weeklyKillAvatarRank if ww.weeklyKillAvatarRank else rankDefaultTxt,
         'guildRank': ww.weeklyKillAvatarSchoolRank if ww.weeklyKillAvatarSchoolRank else rankDefaultTxt,
         'hRank': ww.totalKillAvatarRank if ww.totalKillAvatarRank else rankDefaultTxt,
         'hKillEnemy': ww.killAvatarCntTotal,
         'hGuildRank': ww.totalKillAvatarSchoolRank if ww.totalKillAvatarSchoolRank else rankDefaultTxt,
         'jwTip': [ JD.data.get(key, {}).get('desc', key) for key in sorted(JD.data.keys()) ],
         'canLvUp': self.isJWCanLvUp(),
         'enableWWGuide': self.enableWWQuestGuide()}
        return uiUtils.dict2GfxDict(result, True)

    def onClickJWLvUp(self, *arg):
        p = BigWorld.player()
        consumeItem = JWD.data.get(JD.data.get(p.jueWeiLv, {}).get('type', 0), 0).get('consumeItem', 0)
        if consumeItem:
            self.uiAdapter.messageBox.showYesNoMsgBox(WWCD.data.get('jueWeiLvUpTip', gameStrings.TEXT_WORLDWARPROXY_1523), p.cell.jueWeiLvUp, itemData=uiUtils.getGfxItemById(consumeItem))

    def onShowWarldWar(self, *arg):
        self.show()

    def onShowKillRank(self, *arg):
        pass

    def onShowResourceRank(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())

    def onGotoWorldWarNpc(self, *args):
        wwNpcSeekId = WWCD.data.get('wwNpcSeekId')
        if wwNpcSeekId:
            uiUtils.gotoTrack(wwNpcSeekId)
            gameglobal.rds.uiLog.addFlyLog(wwNpcSeekId)

    def onShowScoreDetail(self, *args):
        if gameglobal.rds.configData.get('enableWWGuildTournament'):
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_GUILD_SCORE_DETAIL)

    def onShowCommitItemBox(self, *args):
        self.commitItemId = int(args[3][0].GetNumber())
        self.uiAdapter.loadWidget(uiConst.WIDGET_WW_COMMIT_ITEM_BOX)

    def onCommitItem(self, *args):
        commitAll = args[3][0].GetBool()
        hasExtraReward = args[3][1].GetBool()
        if self.commitNpc and self.commitItemId:
            if commitAll:
                p = BigWorld.player()
                itemData = ID.data.get(self.commitItemId, {})
                commitCnt = itemData.get('commitCnt', 0)
                inv = p.crossInv if p._isSoul() else p.inv
                cnt = inv.countItemInPages(self.commitItemId)
                if cnt < commitCnt:
                    p.showGameMsg(GMDD.data.WW_ITEM_COMMIT_RESULT_2, ())
                commitTimes = int(cnt / commitCnt)
                if hasExtraReward:
                    val = NICD.data.get(self.npcComitId, {})
                    weekCntMax = val.get('weeklyCnt', 0)
                    dailyCntMax = val.get('dailyCnt', 0)
                    weeklyCnt = p.itemCommitInfo.get(self.npcComitId, {}).get('weeklyCnt', 0)
                    dailyCnt = p.itemCommitInfo.get(self.npcComitId, {}).get('dailyCnt', 0)
                    rewardCnt = min(weekCntMax - weeklyCnt, dailyCntMax - dailyCnt, commitTimes)
                    msg = ICCD.data.get('commitAllMsg', '%s') % rewardCnt
                    self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.commitNpc.cell.commitItems, self.commitItemId, commitTimes, True))
                else:
                    self.commitNpc.cell.commitItems(self.commitItemId, commitTimes, True)
            else:
                self.commitNpc.cell.commitItem(self.commitItemId, True)

    def onItemCommitResult(self, res):
        p = BigWorld.player()
        msgIdName = 'WW_ITEM_COMMIT_RESULT_%s' % res
        p.showGameMsg(getattr(GMDD.data, msgIdName, 0), ())
        if res == gametypes.COMMIT_SUC:
            self.hideItemCommitBox()
            if self.commitMed:
                self.commitMed.Invoke('refreshView', uiUtils.dict2GfxDict(self.getWWItemCommitData(), True))

    def onSpaceNoChanged(self, e):
        oldSpaceNo = e.data
        p = BigWorld.player()
        if self.enableWorldWar() and formula.spaceInWorldWar(p.spaceNo):
            self.uiAdapter.questTrack.hideTrackPanel(True)
            needShowIcon = True
            if p.worldWar.getCountry().groupId not in gametypes.WORLD_WAR_GROUP:
                needShowIcon = False
            if p.worldWar.state == gametypes.WORLD_WAR_STATE_CLOSE:
                needShowIcon = False
            if needShowIcon:
                self.uiAdapter.playRecommPushIcon.hide()
                self.uiAdapter.playRecommTopPush.hide()
                self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_WAR_ICON)
            self.hideWWQueue(gametypes.WORLD_WAR_TYPE_NORMAL)
        elif formula.spaceInWorldWar(oldSpaceNo):
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_WAR_ICON)
            self.wwIconMed = None
            self.uiAdapter.playRecommTopPush.show()
        if self.enableWorldWarBattle():
            if oldSpaceNo != p.spaceNo and formula.spaceInWorldWarBattle(oldSpaceNo):
                self.hideWorldWarBattle()
                self.hideWWBattleRank()
                self.hideWWTarget()
                self.hideWWBattleResult()
                self.uiAdapter.littleMap.delWWBattleIcon()
                self.uiAdapter.playRecommTopPush.show()
            if formula.spaceInWorldWarBattle(p.spaceNo):
                self.showWorldWarBattle()
                self.uiAdapter.littleMap.addWWBattleIcon()
                self.uiAdapter.littleMap.addWWReliveIcon()
                self.uiAdapter.map.addWWBattleIcon(True)
                self.uiAdapter.playRecommPushIcon.hide()
                self.uiAdapter.playRecommTopPush.hide()
                self.uiAdapter.questTrack.hideTrackPanel(True)
                self.hideWWQueue(gametypes.WORLD_WAR_TYPE_BATTLE)
                self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_QUEUE)
        if self.enableWorldWarRob():
            if formula.spaceInWorldWarRob(p.spaceNo) or formula.spaceInWorldWarRob(oldSpaceNo):
                gameglobal.rds.ui.littleMap.addWWRBattleIcon()
                gameglobal.rds.ui.littleMap.addRobZaiju()
                if formula.spaceInWorldWarRob(p.spaceNo):
                    self.uiAdapter.questTrack.hideTrackPanel(True)
                    self.hideWWQueue(gametypes.WORLD_WAR_TYPE_ROB)
                    self.uiAdapter.worldWarRobOverview.show()
                if formula.spaceInWorldWarRob(oldSpaceNo):
                    self.uiAdapter.worldWarRobOverview.clearWidget()
        if formula.spaceInWorldWarEx(oldSpaceNo):
            p.topLogo.removeGuildIcon()
            p.topLogo.addGuildIcon(p.guildFlag)
        if p.inWorldWarEx():
            p.topLogo.refreshGuildIconInWorldWarEx()

    def refreshWWBattleFort(self):
        if self.wwBattleMed:
            self.wwBattleMed.Invoke('refreshDetailIcon', uiUtils.dict2GfxDict(self.getWWBattleFortData(), True))
        self.uiAdapter.littleMap.addWWBattleIcon()
        self.uiAdapter.littleMap.addWWReliveIcon()
        self.refreshWWBattleScore()

    def refreshWWBattleScore(self):
        if self.wwBattleMed:
            self.wwBattleMed.Invoke('refreshScore', uiUtils.dict2GfxDict(self.getWWBattleData(False), True))

    def onStateUpdate(self):
        state = BigWorld.player().worldWar.state
        if state == gametypes.WORLD_WAR_STATE_APPLY_END:
            if self.wwChallengMed:
                self.hideChallenge()
        else:
            self.refreshChallege()

    def onApplyMatches(self):
        ww = BigWorld.player().worldWar
        if ww.getCountry().enemyHostId:
            self.hideChallenge()
        else:
            self.refreshChallege()

    def onWorldWarQueueReady(self, hostId, countDown = 0, macResult = 0):
        self.hideWWQueue(gametypes.WORLD_WAR_TYPE_NORMAL)
        msgQueueType = self.getMsgQueueType(gametypes.WORLD_WAR_TYPE_NORMAL)
        self.uiAdapter.pushMessage.removePushMsg(msgQueueType)
        if self.queueConfirmHandler:
            gameglobal.rds.ui.messageBox.dismiss(self.queueConfirmHandler)
        side = hostId == utils.getHostId() and gameStrings.TEXT_WORLDWARPROXY_1691 or gameStrings.TEXT_WORLDWARPROXY_1691_1
        msg = WWCD.data.get('warQueueTip', gameStrings.TEXT_WORLDWARPROXY_1692) % side
        if macResult == gametypes.WW_MAC_ADDRESS_QUEUE:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_QUEUE)
        elif macResult == gametypes.WW_MAC_ADDRESS_ENTER:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_ENTER)
        self.queueConfirmHandler = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._queueReadyOK), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self._queueReadyCancel), gameStrings.TEXT_PLAYRECOMMPROXY_494_1, True, repeat=countDown or WWCD.data.get('wwQueueCountDown', {}).get(gametypes.WORLD_WAR_TYPE_NORMAL, 10), forbidFastKey=True)

    def onWorldWarBattleQueueReady(self, wwtype, countDown = 0, macResult = 0):
        self.hideWWQueue(wwtype)
        msgQueueType = self.getMsgQueueType(wwtype)
        self.uiAdapter.pushMessage.removePushMsg(msgQueueType)
        if self.battleQueueConfirmHandler:
            gameglobal.rds.ui.messageBox.dismiss(self.battleQueueConfirmHandler)
        if BigWorld.player().isWBHired():
            yesBtnText = WWCD.data.get('battleQueueHireConfirmTxt', '')
            msg = WWCD.data.get('battleQueueHireTip', '')
        else:
            yesBtnText = WWCD.data.get('battleQueueConfirmTxt', '')
            msg = WWCD.data.get('battleQueueTip', '')
        if macResult == gametypes.WW_MAC_ADDRESS_QUEUE:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_QUEUE)
        elif macResult == gametypes.WW_MAC_ADDRESS_ENTER:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_ENTER)
        self.battleQueueConfirmHandler = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._battleQueueReadyOK, wwtype), yesBtnText, Functor(self._battleQueueReadyCancel, wwtype), gameStrings.TEXT_WORLDWARPROXY_1726, False, repeat=countDown or WWCD.data.get('wwQueueCountDown', {}).get(wwtype, 10), countDownFunctor=self.onWWBattleQueueTimeOut, forbidFastKey=True)

    def onWorldWarRobQueueReady(self, wwtype, hostId, countDown = 0, macResult = 0):
        self.hideWWQueue(wwtype)
        msgQueueType = self.getMsgQueueType(wwtype)
        self.uiAdapter.pushMessage.removePushMsg(msgQueueType)
        if self.wwRobConfirmHandler:
            gameglobal.rds.ui.messageBox.dismiss(self.wwRobConfirmHandler)
        side = hostId == utils.getHostId() and gameStrings.TEXT_WORLDWARPROXY_1691 or gameStrings.TEXT_WORLDWARPROXY_1691_1
        groupType = gameStrings.TEXT_WORLDWARPROXY_1739 % gametypes.WORLD_WAR_TYPE_GROUP_TXT[wwtype]
        msg = WWCD.data.get('warRobQueueTip', gameStrings.TEXT_WORLDWARPROXY_1740) % (groupType, side)
        if macResult == gametypes.WW_MAC_ADDRESS_QUEUE:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_QUEUE)
        elif macResult == gametypes.WW_MAC_ADDRESS_ENTER:
            msg = msg + uiUtils.getTextFromGMD(GMDD.data.WW_MAC_ADDRESS_CHECK_ENTER)
        self.wwRobConfirmHandler = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._robQueueReadyOk, wwtype), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self._robQueueReadyCancel, wwtype), gameStrings.TEXT_PLAYRECOMMPROXY_494_1, False, repeat=countDown or WWCD.data.get('wwQueueCountDown', {}).get(gametypes.WORLD_WAR_TYPE_ROB, 10))

    def onWWBattleQueueTimeOut(self):
        if self.battleQueueConfirmHandler:
            self.uiAdapter.messageBox.dismiss(self.battleQueueConfirmHandler)
            self.battleQueueConfirmHandler = None
        self.uiAdapter.messageBox.showAlertBox(WWCD.data.get('battleQueueTimeOutTip', ''))

    def _robQueueReadyOk(self, wwtype):
        self.wwRobConfirmHandler = None
        BigWorld.player().cell.enterWorldWarEvent(wwtype)

    def _robQueueReadyCancel(self, wwtype):
        self.wwRobConfirmHandler = None
        BigWorld.player().cell.worldWarCancelQueue(wwtype)

    def _queueReadyOK(self):
        self.queueConfirmHandler = None
        BigWorld.player().cell.enterWorldWarWithTicket()

    def _queueReadyCancel(self):
        self.queueConfirmHandler = None
        BigWorld.player().cell.worldWarCancelQueue(gametypes.WORLD_WAR_TYPE_NORMAL)

    def _battleQueueReadyOK(self, wwtype):
        self.battleQueueConfirmHandler = None
        BigWorld.player().cell.enterWorldWarEvent(wwtype)

    def _battleQueueReadyCancel(self, wwtype):
        self.battleQueueConfirmHandler = None
        BigWorld.player().cell.worldWarCancelQueue(wwtype)

    def onWorldWarEnterQueue(self, wwType, macResult = 0):
        if self.wwQueueIdDict[wwType] > 0:
            self.hideWWQueue(wwType)
        self.lastQueueType = wwType
        msgQueueType = self.getMsgQueueType(wwType)
        self.uiAdapter.pushMessage.addPushMsg(msgQueueType)
        if wwType == gametypes.WORLD_WAR_TYPE_BATTLE or gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            self.macResult = macResult

    def onWorldWarQueueOrderUpdate(self, wwType, macResult = 0):
        if self.wwQueueMedDict[wwType]:
            self.wwQueueMedDict[wwType].Invoke('updateMsg', GfxValue(gbk2unicode(BigWorld.player().worldWar.getQueueBoxMsg(wwType))))
        else:
            self.lastQueueType = wwType
            if wwType == gametypes.WORLD_WAR_TYPE_BATTLE or gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
                self.macResult = macResult

    def _getWWActFromActBasic(self, weekDay):
        clsType = uiConst.SCHE_CLASS_WORLD_WAR
        ret = []
        for key, _ in self.uiAdapter.schedule.sortedAct:
            actIns = self.actFactory.actIns[key]
            if clsType not in actIns.getClass():
                continue
            visibleCamp = actIns.getVisibleCamp()
            if visibleCamp and BigWorld.player().worldWar.getDayCamp(weekDay) != visibleCamp:
                continue
            startCrons, endCrons = actIns.getAvailableTime()
            startCrons = startCrons or (utils.CRON_ANY,)
            endCrons = endCrons or (utils.CRON_ANY,)
            if len(startCrons) != len(endCrons):
                continue
            if not actIns.getShowFlag():
                continue
            if actIns.isInvalidWeek():
                continue
            sec = int(utils.getNow() + (weekDay - uiUtils.getWeekDay()) * const.TIME_INTERVAL_DAY)
            for i in xrange(len(startCrons)):
                if not utils.inDateRange(startCrons[i], endCrons[i], sec):
                    continue
                obj = {'activityName': actIns.getName(),
                 'time': self.uiAdapter.schedule.formatStr(startCrons[i], endCrons[i]),
                 'actId': key,
                 'timeValid': utils.inTimeRange(startCrons[i], endCrons[i])}
                joinActTime = actIns.getJoinActTime()
                if utils.inTimeRange(joinActTime[0], joinActTime[1]):
                    obj['btnName'] = actIns.getBtnActionName()
                ret.append(obj)

        return ret

    @ui.uiEvent(uiConst.WIDGET_WORLD_WAR_ICON, events.EVENT_QUEST_COMPLETE)
    def refreshWWIconState(self):
        if self.wwIconMed:
            self.wwIconMed.Invoke('setAllDone', GfxValue(worldWarActivity.isAllWWActDone(uiUtils.getWeekDay())))

    def getVoteData(self):
        p = BigWorld.player()
        voteList = []
        if not gameglobal.rds.configData.get('enableWorldWarArmyYoungGroup', False):
            maxVote = sum([ cVal.votes for cVal in p.worldWar.armyCandidate ])
        else:
            maxVote = 0
            for cVal in p.worldWar.armyCandidate:
                if cVal.groupType != self.voteGroupType:
                    continue
                maxVote += cVal.votes

        if not p.worldWar.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE:
            p.worldWar.armyCandidate.sort(key=lambda x: x.votes * 100 - x.ctype * 10 - x.rank, reverse=True)
        for cVal in p.worldWar.armyCandidate:
            if cVal.groupType != self.voteGroupType:
                continue
            rate = int(cVal.votes * 100 / maxVote) if maxVote else 0
            voteList.append({'name': cVal.name,
             'desc': WWCD.data.get('candidateTopDesc', {}).get(cVal.ctype) % (cVal.ctype != gametypes.WW_ARMY_CANDIDATE_MERGED and cVal.rank or ''),
             'currentVote': cVal.votes,
             'voteTxt': '%d%%' % rate,
             'maxVote': maxVote,
             'gbId': str(cVal.gbId),
             'guildName': cVal.guildName})

        return {'voteGbId': str(p.wwArmyVotes.get(self.voteGroupType, '')) if p.wwArmyVotes.get(self.voteGroupType, '') else '',
         'voteList': voteList,
         'voteGroupType': self.voteGroupType,
         'inVote': p.worldWar.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE,
         'wwArmyVoteRule': WWCD.data.get('wwArmyVoteRule', {}).get(self.voteGroupType, '')}

    def refreshVoteList(self):
        if self.wwVoteMed:
            self.wwVoteMed.Invoke('refreshView', uiUtils.dict2GfxDict(self.getVoteData(), True))

    def getArmyMgrInfo(self, postId):
        p = BigWorld.player()
        ww = p.worldWar
        canAppoint = False
        myPostId = ww.getPostByGbId(p.gbId)
        if myPostId:
            canAppoint = bool(WWAD.data.get(myPostId, '').get('subPostIds'))
        info = {'postId': postId,
         'canAppoint': canAppoint,
         'mgr': self._getGfxArmyVal(postId)}
        return info

    def _getGfxArmyVal(self, postId, index = 0):
        p = BigWorld.player()
        val = p.worldWar.getArmyByPostId(postId, index)
        armyData = WWAD.data.get(postId)
        hasSubPost = bool(armyData.get('subPostIds'))
        ret = {'title': armyData.get('name'),
         'postId': postId,
         'subPosts': [],
         'hasSubPosts': hasSubPost}
        if hasSubPost:
            subId = armyData.get('subPostIds')[0]
            ret['subTitle'] = WWAD.data.get(subId, '').get('name', '')
        if val:
            ret['gbId'] = str(val.gbId)
            ret['roleName'] = val.name
            ret['headIcon'] = p._getFriendPhoto(val, val.school, val.sex)
            ret['lv'] = val.lv
            ret['school'] = const.SCHOOL_DICT.get(val.school)
            ret['score'] = val.combatScore
            ret['armyName'] = WWAD.data.get(val.postId, {}).get('name', '')
            ret['online'] = val.bOnline
        else:
            if armyData.get('mgrPostId') not in gametypes.WW_ARMY_SUPER_MGR_POST_IDS and postId not in gametypes.WW_ARMY_SUPER_MGR_POST_IDS:
                return
            ret['roleName'] = gameStrings.TEXT_ARENAPLAYOFFSPROXY_565
            ret['headIcon'] = ''
            ret['gbId'] = ''
        for subId in armyData.get('subPostIds', ()):
            subData = WWAD.data.get(subId)
            if gameglobal.rds.configData.get('enableWorldWarArmyYoungGroup', False):
                subNum = subData.get('maxNumNew', 1)
            else:
                subNum = subData.get('maxNum', 1)
            for i in xrange(subNum):
                subVal = self._getGfxArmyVal(subId, i)
                if subVal:
                    ret['subPosts'].append(subVal)

        return ret

    def getAppointData(self):
        p = BigWorld.player()
        subList = []
        val = p.worldWar.getArmyByGbId(p.gbId)
        if val:
            armyData = WWAD.data.get(val.postId)
            for subPostId in armyData.get('subPostIds', ()):
                subData = WWAD.data.get(subPostId)
                if gameglobal.rds.configData.get('enableWorldWarArmyYoungGroup', False):
                    subNum = subData.get('maxNumNew', 1)
                else:
                    subNum = subData.get('maxNum', 1)
                for i in xrange(subNum):
                    pVal = p.worldWar.getArmyByPostId(subPostId, i)
                    if pVal:
                        subList.append({'roleName': pVal.name,
                         'title': subData.get('name'),
                         'gbId': str(pVal.gbId),
                         'postId': subPostId,
                         'opLabel': gameStrings.TEXT_WORLDWARPROXY_1953})
                    else:
                        subList.append({'roleName': gameStrings.TEXT_ARENAPLAYOFFSPROXY_565,
                         'title': subData.get('name'),
                         'gbId': '0',
                         'postId': subPostId,
                         'opLabel': gameStrings.TEXT_WORLDWARPROXY_1959})

        return {'list': subList}

    def refreshAppointView(self):
        pass

    def appointPostByGbId(self, gbId, roleName):
        BigWorld.player().cell.appointWWArmyPost(gbId, self.appointPostId)

    def onAppointWWArmyPostOK(self, gbId, postId):
        self.uiAdapter.searchPlayer.hide()
        self.refreshAppointView()

    def onRemoveWWArmyPostOK(self, gbId, postId):
        self.refreshAppointView()

    def clickWWBattlePush(self, pushId):
        p = BigWorld.player()
        self.uiAdapter.pushMessage.removePushMsg(pushId)
        self.selectActivityId = WW_BATTLE_ACTIDS.get(p.worldWar.getCurrCamp(), 0)

    def onBattleStateUpdate(self):
        p = BigWorld.player()
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_APPLY)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_OPEN)
        lv, score = WWCD.data.get('wwBattlePushContidtion', (69, 3000))
        if p.lv >= lv and p.getFame(const.WW_WAR_SCORE_FAME_ID) >= score:
            pushId = 0
            if p.worldWar.battleState == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                pushId = uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_APPLY
            elif p.worldWar.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                pushId = uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_OPEN
            if pushId:
                self.uiAdapter.pushMessage.addPushMsg(pushId)

    def clickWWArmyVotePush(self, pushId):
        p = BigWorld.player()
        self.uiAdapter.pushMessage.removePushMsg(pushId)
        if pushId == uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_NOTIFY:
            self.hide()
            self.tabIdx = 0
            self.show()
            self.hideWWArmyVote()
            if not gameglobal.rds.configData.get('enableWorldWarQuickJoinGroup', False):
                self.voteGroupType = gametypes.WW_ARMY_GROUP_TYPE_QINGLONG
            elif p.lv > WWCD.data.get('voteLv', 69):
                self.voteGroupType = gametypes.WW_ARMY_GROUP_TYPE_QINGLONG
            else:
                self.voteGroupType = gametypes.WW_ARMY_GROUP_TYPE_BAIHU
            self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_VOTE)
        elif pushId == uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_RESULT_NOTIFY:
            self.hide()
            self.tabIdx = 3
            self.show()

    def clickWWArmyMarkPush(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WW_ARMY_MARK_NOTIFY)
        self.hide()
        self.tabIdx = 0
        self.show()
        self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_MARK)

    def clickWWBattleResultPush(self, pushId):
        self.uiAdapter.pushMessage.removePushMsg(pushId)

    def onGetTooltip(self, *args):
        key = args[3][0].GetString()
        _, skillId = self.getSkillIDByBinding(key)
        if key.find(WW_SKILL_BINDING) >= 0:
            return self.uiAdapter.skill.formatTooltip(skillId)
        else:
            return self.uiAdapter.skill.formatPSkillTooltip(skillId)

    def getSkillIDByBinding(self, key):
        skills = []
        idx = 0
        skillType = ''
        if key.find(WW_PS_SKILL_BINDING) >= 0:
            idx = int(key[len('worldWar.' + WW_PS_SKILL_BINDING):])
            skills = WWCD.data.get('armyPsSkills', ())
            skillType = WW_PS_SKILL_BINDING
        elif key.find(WW_SKILL_BINDING) >= 0:
            idx = int(key[len('worldWar.' + WW_SKILL_BINDING):])
            skills = WWCD.data.get('armySkills', ())
            skillType = WW_SKILL_BINDING
        if idx < len(skills):
            return (skillType, skills[idx])
        return ('', 0)

    def getSlotID(self, key):
        return self.getSkillIDByBinding(key)

    def getSlotValue(self, movie, idItem, idCon):
        if idCon:
            if idCon == WW_PS_SKILL_BINDING:
                skillData = PSkillInfo(idItem, 1)
                icon = 'skill/icon/%d.dds' % skillData.getSkillData('icon', 0)
            else:
                icon = self.uiAdapter.actionbar._getSkillIcon(idItem)
            data = {'iconPath': icon}
            return uiUtils.dict2GfxDict(data, True)

    def resetInactive(self):
        self.bInactive = False
        self.tInactive = 0
        if self.notifyInactiveTimerId:
            BigWorld.cancelCallback(self.notifyInactiveTimerId)
            self.notifyInactiveTimerId = 0

    def setInactive(self):
        self.bInactive = True
        self.tInactive = utils.getNow()
        if self.notifyInactiveTimerId:
            BigWorld.cancelCallback(self.notifyInactiveTimerId)
            self.notifyInactiveTimerId = 0
        self._notifyInactive()

    def startCheckInactive(self):
        p = BigWorld.player()
        p.tLastMoving = utils.getNow()
        if self.checkInactiveTimerId:
            BigWorld.cancelCallback(self.checkInactiveTimerId)
            self.checkInactiveTimerId = 0
        self.resetInactive()
        self._checkInactive()

    def _checkInactive(self):
        self.checkInactiveTimerId = 0
        p = BigWorld.player()
        if not p or not p.inWorld or not p.inWorldWarEx():
            self.resetInactive()
            return
        if p.inWorldWar() and not p.worldWar.isNeedCheckInactive:
            return
        if p.isMoving or utils.getNow() - p.tLastMoving <= const.WORLD_WAR_BATTLE_INACTIVE_TIME:
            self.resetInactive()
        elif not self.bInactive:
            self.setInactive()
        self.checkInactiveTimerId = BigWorld.callback(5, self._checkInactive)

    def _notifyInactive(self):
        self.notifyInactiveTimerId = 0
        p = BigWorld.player()
        if not p or not p.inWorld or not p.inWorldWarEx():
            return
        if not self.bInactive:
            return
        if p.isMoving or utils.getNow() - p.tLastMoving <= const.WORLD_WAR_BATTLE_INACTIVE_TIME:
            self.resetInactive()
            return
        if utils.getNow() - self.tInactive >= const.WORLD_WAR_BATTLE_INACTIVE_NOTIFY_TIME:
            p.cell.exitWorldWarInactive()
            return
        if p.inWorldWarBattle():
            p.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_INACTIVE, ())
        elif p.inWorldWar():
            p.showGameMsg(GMDD.data.WORLD_WAR_INACTIVE, ())
        elif formula.spaceInWorldWarRob(p.spaceNo):
            p.showGameMsg(GMDD.data.WORLD_WAR_ROB_INACTIVE, ())
        self.notifyInactiveTimerId = BigWorld.callback(5, self._notifyInactive)

    def isWWQuestTabEnabled(self):
        p = BigWorld.player()
        return p.worldWar.state in gametypes.WORLD_WAR_STATE_RUNNING and not p.worldWar.isLucky()

    def _registerASWidget(self, widgetId, widget):
        self.selServerWidget = widget
        widget.defaultCloseBtn = widget.closeBtn
        widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.onClickRef)
        widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onComfirmApply)
        widget.serverList.column = 2
        widget.serverList.itemHeight = 33
        widget.serverList.itemWidth = 162
        widget.serverList.itemRenderer = 'WWServerList_ServerItemRenderer'
        widget.serverList.lableFunction = self.serverLabelFun
        self.setServerList(self.serverListInfo)

    @ui.callFilter(3, True)
    def onClickRef(self, *args):
        p = BigWorld.player()
        p.cell.queryWBHireInfo(p.worldWar.hireVer)

    def onComfirmApply(self, *args):
        if self.selServerBtn:
            hostId = int(self.selServerBtn.data[0])
            p = BigWorld.player()
            if p.wbApplyHireHostId and p.wbApplyHireHostId != hostId:
                hireHostName = utils.getServerName(p.wbApplyHireHostId)
                selServerName = utils.getServerName(hostId)
                msg = uiUtils.getTextFromGMD(GMDD.data.WB_REPLACE_BATTLE_HIRE_COMFIRM, '%s_%s') % (hireHostName, selServerName)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmApplyHire, hostId))
            elif p.wbApplyHireHostId == 0 and p.wbHireHostId == 0:
                msg = uiUtils.getTextFromGMD(GMDD.data.WB_APPLY_HIRE_COMFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmApplyHire, hostId))
            else:
                wwtype = commonWorldWar.getBattleHireTypeByLevel(p.lv)
                p.cell.applyWorldWarBattleHire(hostId, wwtype)

    def onConfirmApplyHire(self, hostId):
        p = BigWorld.player()
        if p.worldWar.wwTicketHosts.get(gametypes.WORLD_WAR_TYPE_BATTLE, 0):
            p.cell.worldWarCancelQueue(gametypes.WORLD_WAR_TYPE_BATTLE)
        wwtype = commonWorldWar.getBattleHireTypeByLevel(p.lv)
        p.cell.applyWorldWarBattleHire(hostId, wwtype)

    def hideSelServer(self):
        self.selServerWidget = None
        self.selServerBtn = None

    def serverLabelFun(self, *args):
        mc = ASObject(args[3][1])
        obj = ASObject(args[3][0])
        mc.nameBtn.data = obj
        mc.nameBtn.selected = False
        mc.nameBtn.label = utils.getServerName(obj[0])
        mc.hireFlag.visible = obj[0] == BigWorld.player().wbApplyHireHostId
        mc.nameBtn.addEventListener(events.MOUSE_CLICK, self.onSelectServer)
        mc.nameBtn.stateIcon.gotoAndStop('state%d' % obj[1])
        if mc.index == 0:
            mc.nameBtn.selected = True
            self.selServerBtn = mc.nameBtn
            self.selServerWidget.confirmBtn.enabled = obj[0] != BigWorld.player().wbApplyHireHostId

    def onSelectServer(self, *args):
        target = ASObject(args[3][0]).currentTarget
        target.selected = True
        if self.selServerBtn:
            self.selServerBtn.selected = False
        self.selServerBtn = target
        if self.selServerWidget:
            self.selServerWidget.confirmBtn.enabled = target.data[0] != BigWorld.player().wbApplyHireHostId

    def setServerList(self, data):
        self.serverListInfo = data
        if self.selServerWidget:
            self.selServerWidget.serverList.dataArray = data

    def refreshServerList(self):
        if self.selServerWidget:
            self.selServerWidget.serverList.dataArray = self.serverListInfo
