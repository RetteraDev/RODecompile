#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArenaPlayoffsProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import copy
import datetime
import uiUtils
import const
import gametypes
import events
import formula
import duelUtils
from guis.asObject import ASUtils
from guis import ui
from uiProxy import UIProxy
from guis import pinyinConvert
from guis import uiConst
from guis.asObject import ASObject
from guis.asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
from guis import menuManager
from guis.asObject import MenuManager
from guis import arenaPlayoffsProxy
from data import duel_config_data as DCD
from data import arena_score_schedule_desc_data as ASSDD
from data import arena_score_group_duel_data as ASGDD
from cdata import game_msg_def_data as GMDD
from helpers import taboo
STATE_NO_TEAM = 1
STATE_NO_REQUIEMENT = 2
STATE_LEADER = 3
STATE_TEAMER = 4
STATE_NORMAL = 5
MAX_TEAM_MEMBER = 4
ARENA_PANEL_STAGE_INIT = 1
ARENA_PANEL_STAGE_WAITING_TEAM = 2
ARENA_PANEL_STAGE_MATCHING = 3
ARENA_PANEL_STAGE_IN_GAME = 4
ARENA_PANEL_STAGE_MATCHED = 5

class BalanceArenaPlayoffsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArenaPlayoffsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.addEvent(events.EVENT_CHANGE_ARENA_STATE, self.refreshPlayoffsPanel)

    def initVisible(self):
        self.widget.addMemberBtn.visible = False
        self.widget.dismissTeamBtn.visible = False
        self.widget.dismissTeamBtn2.visible = False
        self.widget.applyTeamBtn.visible = False
        self.widget.leaveBtn.visible = False
        self.widget.teamName.visible = False
        self.widget.createTeam.visible = False
        self.widget.playerList.visible = False
        self.widget.requirementTxt.visible = False
        self.widget.createTeam2.visible = False
        self.widget.inviteFriendsList.visible = False
        self.widget.statistics.visible = False
        self.widget.levelHint.visible = False
        self.widget.teleportBtn.enabled = False
        self.widget.participateBtn.enabled = False

    def refreshView(self):
        info = self.getArenaPlayoffsInfo()
        self.widget.firstTitle.htmlText = info['title']
        self.widget.secondTitle.htmlText = info['secondTitle']
        self.widget.descPanel.canvas.text.htmlText = gameStrings.PVP_PLAYOFFS_V2_OPENING_TIME + '\n' + info['timeDesc'] + '\n' + gameStrings.PVP_PLAYOFFS_V2_HOW_TO_PLAY + '\n' + info['playDesc']
        self.initVisible()
        p = BigWorld.player()
        if info['state'] == STATE_LEADER:
            self.widget.addMemberBtn.visible = True
            self.widget.dismissTeamBtn.visible = True
            self.widget.applyTeamBtn.visible = True
            self.widget.addMemberBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.dismissTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.applyTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.addMemberBtn.enabled = info['canAddMember']
            self.widget.applyTeamBtn.enabled = info['canApplyTeam']
            if p.isArenaScoreTeamCreated():
                self.widget.applyTeamBtn.visible = False
                self.widget.dismissTeamBtn2.visible = True
                self.widget.dismissTeamBtn2.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == STATE_TEAMER or info['state'] == STATE_NORMAL:
            self.widget.leaveBtn.visible = True
            self.widget.leaveBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == STATE_NO_TEAM:
            self.widget.createTeam.visible = True
            self.widget.createTeam.createTeamBtn.enabled = p.canArenaScoreCreateTeam()
            self.widget.levelHint.visible = True
            self.widget.createTeam.createTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == STATE_NO_REQUIEMENT:
            self.widget.requirementTxt.visible = True
            self.widget.requirementTxt.text.htmlText = info['requiementDesc'].replace('\n', '')
        if info['state'] == STATE_LEADER or info['state'] == STATE_TEAMER or info['state'] == STATE_NORMAL:
            self.widget.playerList.visible = True
            self.widget.teamName.visible = True
            p = BigWorld.player()
            self.refreshPlayers(info['players'], p.getArenaScoreUIState(isDone=False))
            self.widget.teamName.teamNameTxt.htmlText = info['teamName']
        if info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN:
            self.widget.requirementTxt.visible = True
            self.widget.requirementTxt.text.htmlText = gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME
        self.widget.participateBtn.enabled = self.isInArenaScoreDiGong()
        self.widget.reportBtn.enabled = info['canViewReport']
        if p.isInArenaScoreStateJiFen():
            self.widget.betBtn.visible = False
        else:
            self.widget.betBtn.visible = info['betBtnVisible']
        if p.isBalancePlayoffs():
            if p.canArenaScoreTeleport():
                self.widget.teleportBtn.enabled = True
            self.refreshStatistics()
            if p.isInArenaScoreStateApply():
                self.widget.reportBtn.visible = False
            else:
                self.widget.reportBtn.visible = True
                if p.isInArenaScoreStateJiFen():
                    self.widget.reportBtn.label = gameStrings.RANK_LABEL
                else:
                    self.widget.reportBtn.label = gameStrings.ZHANBAO_LABEL
            if self.isInArenaScoreDiGong():
                self.widget.teleportBtn.visible = False
                self.widget.participateBtn.visible = True
                self.stage = getattr(p, 'arenaStage', 1)
                if self.stage == ARENA_PANEL_STAGE_MATCHING or self.stage == ARENA_PANEL_STAGE_WAITING_TEAM:
                    self.widget.participateBtn.label = gameStrings.DOUBLEARENA_QUITMATCH
                else:
                    self.widget.participateBtn.label = gameStrings.DOUBLEARENA_STARTMATCH
            else:
                self.widget.teleportBtn.visible = True
                self.widget.participateBtn.visible = False

    def isInArenaScoreDiGong(self):
        p = BigWorld.player()
        return formula.isPlayoffsArenaCrossServerML(formula.getMLGNo(p.spaceNo))

    def refreshStatistics(self):
        p = BigWorld.player()
        if p.isArenaScoreTeamCreated() and p.isInArenaScoreStateJiFen():
            self.widget.statistics.visible = True
            scoreInfo = p.getArenaPlayoffsTeam().get('score', {})
            self.widget.statistics.score.text = scoreInfo.get('score', 0)
            self.widget.statistics.attendCnt.text = scoreInfo.get('totalCnt', 0)
            self.widget.statistics.winCnt.text = scoreInfo.get('winCnt', 0)
            playerScoreInfo = p.arenaScorePlayerScore.get(const.ARENA_SCORE_TYPE_1, None)
            totalPlayerScore = 0
            todayPlayerScore = 0
            if playerScoreInfo:
                totalPlayerScore = playerScoreInfo.score
                todayPlayerScore = playerScoreInfo.dailyScore
            self.widget.statistics.attendScore.text = totalPlayerScore
            TipManager.addTip(self.widget.statistics.attr1, DCD.data.get('arenaScoreAttendScoreTip', 'this is the attend score tip%s') % (todayPlayerScore,))

    def refreshPlayers(self, players, state):
        p = BigWorld.player()
        for i in xrange(MAX_TEAM_MEMBER):
            player = self.widget.playerList.getChildByName('player%d' % i)
            if player:
                if len(players) <= i:
                    player.visible = False
                else:
                    obj = players[i]
                    player.visible = True
                    player.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleBtnStateChanged, False, 0, True)
                    player.data = obj
                    player.playerNameTxt.text = obj['name']
                    player.scoreTxt.text = obj['score']
                    ASUtils.truncateString(player.scoreTxt)
                    if obj['selected']:
                        player.flagBtn.text = gameStrings.PVP_PLAYOFFS_V2_FIGHT
                        player.substituteBtn.label = gameStrings.PVP_PLAYOFFS_V2_SET_SUBSTITUTE
                    else:
                        player.flagBtn.text = gameStrings.PVP_PLAYOFFS_V2_SUBSTITUTE
                        player.substituteBtn.label = gameStrings.PVP_PLAYOFFS_V2_SET_FIGHT
                    player.substituteBtn.addEventListener(events.MOUSE_CLICK, self.handleFlagClick, False, 0, True)
                    player.removeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
                    if state == STATE_LEADER:
                        player.substituteBtn.visible = True
                        player.removeBtn.visible = not self.isLeader(player.data['gbId'])
                    else:
                        player.substituteBtn.visible = False
                        player.removeBtn.visible = False
                    if p.isArenaScoreTeamCreated() and p.isBeforeArenaScoreState64():
                        player.inviteBtn.visible = p.gbId != int(player.data['gbId'])
                        player.inviteBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
                        player.removeBtn.visible = False
                    else:
                        player.inviteBtn.visible = False
                    if p.gbId != long(player.data['gbId']):
                        menuParam = {'roleName': obj['name'],
                         'gbId': long(player.data['gbId']),
                         'fid': long(player.data['gbId'])}
                        MenuManager.getInstance().registerMenuById(player.playerNameTxt, uiConst.MENU_ARENA_PLAYOFFS_TEAM_INFO, menuParam)

    def isLeader(self, gbId):
        gbId = int(gbId)
        p = BigWorld.player()
        if p.getArenaPlayoffsTeamNUID():
            if p.getArenaPlayoffsTeamHeader() == gbId:
                return True
        return False

    def handleFlagClick(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        obj = e.currentTarget.parent.data
        if p.isInArenaScoreStateNotJiFen():
            BigWorld.player().cell.setArenaPlayoffsTeamDuelFlag(int(obj['gbId']), not obj['selected'])
        else:
            p.cell.setArenaScoreTeamDuelFlag(const.ARENA_SCORE_TYPE_1, int(obj['gbId']), not obj['selected'])

    def handleBtnStateChanged(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        targetBtn.playerNameTxt.text = targetBtn.data['name']
        targetBtn.scoreTxt.text = targetBtn.data['score']
        ASUtils.truncateString(targetBtn.scoreTxt)

    def handleClickBtn(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        btnName = targetBtn.name
        p = BigWorld.player()
        if btnName == 'createTeamBtn':
            gameglobal.rds.ui.arenaPlayoffs.showCreateScoreTeam()
        elif btnName == 'dismissTeamBtn':
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_ARENA_PLAYOFFS_TEAM_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.cell.disbandArenaScoreTeam, const.ARENA_SCORE_TYPE_1))
        elif btnName == 'dismissTeamBtn2':
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_ARENA_PLAYOFFS_TEAM_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.cell.disbandArenaScoreTeam, const.ARENA_SCORE_TYPE_1))
        elif btnName == 'leaveBtn':
            msg = uiUtils.getTextFromGMD(GMDD.data.LEAVE_ARENA_PLAYOFFS_TEAM_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.cell.quitArenaScoreTeam, const.ARENA_SCORE_TYPE_1))
        elif btnName == 'applyTeamBtn':
            self.applyTeamDone()
        elif btnName == 'participateBtn':
            stage = getattr(p, 'arenaStage', 1)
            if stage == ARENA_PANEL_STAGE_MATCHING or stage == ARENA_PANEL_STAGE_WAITING_TEAM:
                p.cancelApplyArena()
            else:
                p = BigWorld.player()
                if p.isInArenaScoreStateJiFen():
                    p.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE
                    p.base.applyArenaOfFounder(const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE)
                elif p.isInArenaScoreStateWuDao():
                    msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_PLAYOFFS_JOIN_MSG)
                    self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.enterPlayoffsArena)
                elif p.getArenaScoreState() == gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT:
                    p.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE
                    p.base.applyArenaOfFounder(const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE)
        elif btnName == 'reportBtn':
            p = BigWorld.player()
            if p.isInArenaScoreStateJiFen():
                gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_CROSS_ARENA_SCORE_PLAYOFFS)
            else:
                self.uiAdapter.arenaPlayoffs.showPlayoffsReport()
        elif btnName == 'betBtn':
            self.uiAdapter.arenaPlayoffsBet.show(uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4)
        elif btnName == 'addMemberBtn':
            self.widget.inviteFriendsList.visible = not self.widget.inviteFriendsList.visible
            if self.widget.inviteFriendsList.visible:
                self.refreshInviteFriendsList()
        elif btnName == 'removeBtn':
            if targetBtn.parent.data['gbId']:
                self.removeTeamer(targetBtn.parent.data['gbId'])
        elif btnName == 'inviteBtn':
            if targetBtn.parent.data['name']:
                if p._isSoul():
                    targetRoleName = '%s-%s' % (targetBtn.parent.data['name'], utils.getServerName(utils.getHostId()))
                else:
                    targetRoleName = targetBtn.parent.data['name']
                menuTarget = menuManager.getInstance().menuTarget
                menuTarget.apply(roleName=targetRoleName)
                if menuTarget.canInviteTeam(p):
                    menuManager.getInstance().inviteTeam()
        elif btnName == 'templateBtn':
            gameglobal.rds.ui.balanceArenaTemplate.show()
        elif btnName == 'teleportBtn':
            p.cell.applyEnterBalanceReadyRoom(const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE)

    @ui.checkInventoryLock()
    def applyTeamDone(self):
        p = BigWorld.player()
        p.cell.applyArenaScoreTeamDone(const.ARENA_SCORE_TYPE_1)

    def removeTeamer(self, id):
        gbId = int(id)
        p = BigWorld.player()
        roleName = p.getArenaPlayoffsMember().get(gbId, {}).get('roleName', '')
        playoffsMember = p.getArenaPlayoffsMember()
        if gbId in playoffsMember.keys():
            msg = uiUtils.getTextFromGMD(GMDD.data.KICK_OUT_ARENA_PLAYOFFS_TEAM_MSG, '%s') % roleName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.kickoutArenaScoreTeam, const.ARENA_SCORE_TYPE_1, gbId, roleName))

    def refreshInviteFriendsList(self):
        self.selectedFriends = []
        inviteFriendsList = self.widget.inviteFriendsList
        friendList = inviteFriendsList.friendList
        friendList.itemRenderer = 'M12_DefaultCheckBoxShen'
        friendList.itemHeight = 28
        friendList.labelFunction = self.friendLableFunc
        friendList.dataArray = self.getMyFriendList()
        inviteFriendsList.desc.htmlText = DCD.data.get('inviteMemberTip', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME)
        inviteFriendsList.filterInput.addEventListener(events.EVENT_CHANGE, self.handleFilterChanged, False, 0, True)
        inviteFriendsList.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHideFriendList, False, 0, True)
        inviteFriendsList.clearFilterBtn.addEventListener(events.MOUSE_CLICK, self.handleClearFilter, False, 0, True)
        inviteFriendsList.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleInviteFriends, False, 0, True)

    def handleFilterChanged(self, *args):
        inviteFriendsList = self.widget.inviteFriendsList
        filterInput = inviteFriendsList.filterInput
        fMsgPinYin = pinyinConvert.strPinyin(filterInput.text).lower()
        if fMsgPinYin:
            inviteFriendsList.clearFilterBtn.visible = True
            friends = []
            for fVal in self.getMyFriendList():
                fPinYinNames = fVal['pinYinNames']
                if fMsgPinYin in fPinYinNames[0].lower() or fMsgPinYin in fPinYinNames[1].lower():
                    friends.append(fVal)

            inviteFriendsList.friendList.dataArray = friends
        else:
            inviteFriendsList.friendList.dataArray = self.getMyFriendList()
            inviteFriendsList.clearFilterBtn.visible = False

    def handleInviteFriends(self, *args):
        p = BigWorld.player()
        for data in self.selectedFriends:
            p.cell.inviteArenaScoreTeam(const.ARENA_SCORE_TYPE_1, int(data.gbId))

        self.selectedFriends = []
        self.handleClearFilter()

    def handleHideFriendList(self, *args):
        self.widget.inviteFriendsList.visible = False

    def handleClearFilter(self, *args):
        inviteFriendsList = self.widget.inviteFriendsList
        inviteFriendsList.filterInput.text = ''
        inviteFriendsList.friendList.dataArray = None
        inviteFriendsList.friendList.dataArray = self.getMyFriendList()

    def friendLableFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.width = 180
        itemMc.label = itemData.roleName
        itemMc.removeEventListener(events.EVENT_SELECT, self.handleSelecteFriend)
        itemMc.data = itemData
        itemMc.focusable = False
        itemMc.selected = self.contains(itemData)
        itemMc.addEventListener(events.EVENT_SELECT, self.handleSelecteFriend, False, 0, True)
        itemMc.validateNow()

    def handleSelecteFriend(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.data
        if e.currentTarget.selected:
            if len(self.selectedFriends) >= DCD.data.get('maxInviteMember', 2):
                e.currentTarget.selected = False
                return
            if not self.contains(itemData):
                self.selectedFriends.append(itemData)
        else:
            self.selectedFriends.remove(itemData)

    def contains(self, itemData):
        for data in self.selectedFriends:
            if data.gbId == itemData.gbId:
                return True

        return False

    def getMyFriendList(self):
        p = BigWorld.player()
        friends = []
        for gbId, fVal in p.friend.items():
            if p.friend.isFriendGroup(fVal.group) and p.friend.isVisible(fVal.state) and not fVal.deleted:
                friends.append({'gbId': str(gbId),
                 'roleName': fVal.getFullName(),
                 'pinYinNames': (pinyinConvert.strPinyinFirst(fVal.getFullName()), pinyinConvert.strPinyin(fVal.getFullName()))})

        return friends

    def getArenaPlayoffsInfo(self):
        p = BigWorld.player()
        memebers = []
        for gbId, member in p.getArenaPlayoffsMember().items():
            memebers.append({'gbId': str(gbId),
             'name': member.get('roleName', ''),
             'online': member.get('isOn', 0),
             'selected': member.get('duelFlag', 0),
             'schoolTxt': uiConst.SCHOOL_FRAME_DESC.get(member.get('school', 0)),
             'score': member.get('tempName', '')})

        curSch = self.getCurPlayoffsSchedule()
        info = {'state': p.getArenaScoreUIState(),
         'canAddMember': len(p.getArenaPlayoffsMember()) < const.ARENA_PLAYOFFS_TEAM_MAX_NUM,
         'maxInviteMember': DCD.data.get('maxInviteMember', 2),
         'players': memebers,
         'canMark': p.getArenaPlayoffsTeamHeader() == p.gbId,
         'myGbId': p.gbId,
         'title': curSch.get('title', ''),
         'secondTitle': curSch.get('name', ''),
         'timeDesc': curSch.get('playoffsPlayDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'playDesc': curSch.get('playoffsTeamDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'inviteMemberTip': DCD.data.get('inviteMemberTip', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'requiementDesc': gameStrings.ARENA_SCORE_NO_REQUIREMENT,
         'groupTxt': gameStrings.PVP_PLAYOFFS_V2_GROUP + uiUtils.toHtml(uiUtils.lv2ArenaPlayoffsTeamGroup(p.lv), '#ffbf40'),
         'teamName': p.getArenaPlayoffsTeam().get('teamName', ''),
         'canApplyTeam': len(p.getArenaPlayoffsMember()) >= const.ARENA_PLAYOFFS_TEAM_MAX_NUM - 1,
         'canJoin': p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL or p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL,
         'canViewReport': True,
         'betBtnVisible': gameglobal.rds.configData.get('enableArenaPlayoffsBet', False) and p.canArenaScoreBet()}
        return info

    def getCurPlayoffsSchedule(self):
        p = BigWorld.player()
        defaultInfo = {'title': gameStrings.TEXT_BALANCEARENAPLAYOFFSPROXY_452}
        schedule = self.getArenaPlayOffSchedule()
        if p.isInArenaScoreStateFinal():
            return ASSDD.data.get(4)
        if p.isInArenaScoreStateGroup():
            return ASSDD.data.get(3)
        if p.isInArenaScoreStateJiFen():
            val = copy.deepcopy(ASSDD.data.get(2))
            return val
        if p.isInArenaScoreStateApply() or utils.inCrontabRange(schedule['applyShowTime'], schedule['applyStartCrontab']):
            val = copy.deepcopy(ASSDD.data.get(1))
            val['playoffsPlayDesc'] = gameStrings.ARENA_SCORE_PLAYOFFS_APPLY_DESC % (schedule['applyStartTime'].month,
             schedule['applyStartTime'].day,
             schedule['applyEndTime'].month,
             schedule['applyEndTime'].day)
            return val
        return defaultInfo

    def getCrontabByState(self, curArenaPlayoffsSeason, state):
        stateIdx = duelUtils.getCrontabIdByPlayoffsState(gametypes.ARENA_PLAYOFFS_TYPE_BALANCE, state)
        return duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_BALANCE)

    def getPlayoffsSeason(self):
        timeoffset = const.TIME_INTERVAL_DAY * 2
        return formula.getPlayoffsSeason(utils.getNow() + timeoffset)

    def getArenaPlayOffSchedule(self):
        p = BigWorld.player()
        curArenaPlayoffsSeason = self.getPlayoffsSeason()
        schedule = {}
        applyStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD)
        startTime = utils.getDisposableCronTabTimeStamp(applyStartCrontab)
        applyDateTime = datetime.datetime.fromtimestamp(startTime)
        applyShowTime = applyDateTime - datetime.timedelta(days=2)
        applyEndCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD)
        applyEndTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(applyEndCrontab))
        scoreStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE)
        scoreStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(scoreStartCrontab))
        scoreEndCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE)
        scoreEndTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(scoreEndCrontab))
        groupStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING)
        groupStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(groupStartCrontab))
        kickOutStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING)
        kickOutStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(kickOutStartCrontab))
        schedule['applyShowTime'] = '0 8 %d %d *' % (applyShowTime.day, applyShowTime.month)
        schedule['startCrontab'] = applyStartCrontab
        schedule['scoreStartTime'] = scoreStartTime
        schedule['scoreStartCrontab'] = scoreStartCrontab
        schedule['scoreEndTime'] = scoreEndTime
        schedule['scoreEndCrontab'] = scoreEndCrontab
        schedule['startTime'] = startTime
        schedule['applyDateTime'] = applyDateTime
        schedule['applyStartTime'] = applyDateTime
        schedule['applyStartCrontab'] = applyStartCrontab
        schedule['applyEndTime'] = applyEndTime
        schedule['applyEndCrontab'] = applyEndCrontab
        schedule['groupStartTime'] = groupStartTime
        schedule['groupStartCrontab'] = groupStartCrontab
        schedule['kickOutStartTime'] = kickOutStartTime
        schedule['kickOutStartCrontab'] = kickOutStartCrontab
        return schedule

    def getPlayoffsDayLabel(self):
        curArenaPlayoffsSeason = self.getPlayoffsSeason()
        dayLabels = []
        index = 0
        for key in sorted(ASGDD.data.keys()):
            val = ASGDD.data[key]
            if val.get('type') == arenaPlayoffsProxy.TYPE_FINAL_DUEL:
                stateIdx = duelUtils.getCrontabIdByPlayoffsFinalIdx(gametypes.ARENA_PLAYOFFS_TYPE_BALANCE, index)
                macthDateTimeStr = duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_BALANCE)
                macthDateTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(macthDateTimeStr))
                startTimeStr = val.get('startTime', '%d.%d.%d.19.0.0')
                endTimeStr = val.get('endTime', '%d.%d.%d.20.20.0')
                startTime = startTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                endTime = endTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                dayLabels.append({'week': '%d.%d' % (macthDateTime.month, macthDateTime.day),
                 'date': val.get('date', ''),
                 'state': gameglobal.rds.ui.arenaPlayoffs.getTimeState(startTime, endTime)})
                index += 1

        return dayLabels

    def getMatchesSchedule(self):
        matchesSchedule = []
        curArenaPlayoffsSeason = self.getPlayoffsSeason()
        index = 0
        for key in sorted(ASGDD.data.keys()):
            mathchRoundDesc = {}
            val = ASGDD.data[key]
            if val.get('type') == arenaPlayoffsProxy.TYPE_GROUP_DUEL:
                stateIdx = duelUtils.getCrontabIdByPlayoffsGroupIdx(gametypes.ARENA_PLAYOFFS_TYPE_BALANCE, index)
                matchRoundStr = duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_BALANCE)
                matchRound = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(matchRoundStr))
                mathchRoundDesc['startStage'] = 0
                mathchRoundDesc['type'] = val.get('type')
                now = utils.getNow()
                currentYear = datetime.datetime.fromtimestamp(now).year
                defaultStartCrontab = '30 19 %d %d * %d'
                defaultEnterCrontab = '20 19 %d %d * %d'
                if key % 2 != 1:
                    defaultStartCrontab = '40 20 %d %d * %d'
                    defaultEnterCrontab = '30 20 %d %d * %d'
                startContab = val.get('startContab', defaultStartCrontab)
                enterCrontab = val.get('enterCrontab', defaultEnterCrontab)
                startTime = val.get('startTime', '%d.%d.%d.19.0.0')
                endTime = val.get('endTime', '%d.%d.%d.20.20.0')
                matchRoundCrontab = startContab % (matchRound.day, matchRound.month, currentYear)
                matchRoundEnterCrontab = enterCrontab % (matchRound.day, matchRound.month, currentYear)
                mathchRoundDesc['startStage'] = 0
                if utils.inTimeRange(matchRoundEnterCrontab, matchRoundCrontab):
                    if index % 2:
                        mathchRoundDesc['startStage'] = 1
                    else:
                        mathchRoundDesc['startStage'] = 2
                matchTime = utils.getDisposableCronTabTimeStamp(matchRoundCrontab)
                macthDateTime = datetime.datetime.fromtimestamp(matchTime)
                matchEnterTime = utils.getDisposableCronTabTimeStamp(matchRoundEnterCrontab)
                matchDataEnterTime = datetime.datetime.fromtimestamp(matchEnterTime)
                mathchRoundDesc['week'] = gameStrings.ARENA_GROUP_MATCH_WEEK_TXT % gameStrings.NUM_TO_CN_WEEK[macthDateTime.weekday()]
                mathchRoundDesc['date'] = '%d.%d' % (macthDateTime.month, macthDateTime.day)
                mathchRoundDesc['time'] = gameStrings.ARENA_GROUP_MATCH_TIME_TXT % (macthDateTime.hour, macthDateTime.minute)
                mathchRoundDesc['startTime'] = startTime % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                mathchRoundDesc['endTime'] = endTime % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                mathchRoundDesc['name'] = gameStrings.ARENA_GROUP_MATCH_ENTER_TIME_TXT % (matchDataEnterTime.hour, matchDataEnterTime.minute)
                matchesSchedule.append(mathchRoundDesc)
                index += 1

        return matchesSchedule

    def getArenaFinalSchedule(self):
        curArenaPlayoffsSeason = self.getPlayoffsSeason()
        index = 0
        schedules = []
        for key in sorted(ASGDD.data.keys()):
            val = ASGDD.data[key]
            if val.get('type') == arenaPlayoffsProxy.TYPE_FINAL_DUEL:
                scheduleInfo = copy.deepcopy(ASGDD.data[key])
                stateIdx = duelUtils.getCrontabIdByPlayoffsFinalIdx(gametypes.ARENA_PLAYOFFS_TYPE_BALANCE, index)
                macthDateTimeStr = duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_BALANCE)
                macthDateTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(macthDateTimeStr))
                startTimeStr = val.get('startTime', '%d.%d.%d.19.0.0')
                endTimeStr = val.get('endTime', '%d.%d.%d.20.20.0')
                startTime = startTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                endTime = endTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                scheduleInfo['startTime'] = startTime
                scheduleInfo['endTime'] = endTime
                schedules.append(scheduleInfo)

        return schedules

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.refreshView()
        self.widget.betBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.reportBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.participateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.templateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.teleportBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.netUrl.htmlText = DCD.data.get('arenaPlayoffsLinkText', '')
        self.widget.dandanUrl.htmlText = DCD.data.get('arenaPlayoffsScoreDanDanText', gameStrings.ARENA_SCORE_DANDAN_TEXT)

    def refreshPlayoffsPanel(self):
        if self.widget:
            self.refreshView()
