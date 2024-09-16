#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpPlayoffs5V5Proxy.o
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
import uiConst
import formula
import duelUtils
from guis import ui
from uiProxy import UIProxy
from guis import pinyinConvert
from guis import uiConst
from guis.asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
from guis import arenaPlayoffsProxy
from guis.asObject import MenuManager
from data import duel_config_data as DCD
from data import arena_5v5_schedule_desc_data as A5SDD
from data import arena_5v5_group_duel_data as A5GDD
from cdata import game_msg_def_data as GMDD
MAX_TEAM_MEMBER = 6

class PvpPlayoffs5V5Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpPlayoffs5V5Proxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initVisible(self):
        self.widget.addMemberBtn.visible = False
        self.widget.dismissTeamBtn.visible = False
        self.widget.applyTeamBtn.visible = False
        self.widget.leaveBtn.visible = False
        self.widget.teamName.visible = False
        self.widget.createTeam.visible = False
        self.widget.playerList.visible = False
        self.widget.requirementTxt.visible = False
        self.widget.inviteFriendsList.visible = False
        self.widget.sendVoteBtn.visible = False
        self.widget.voteBtn.visible = False
        self.widget.attendRequirement.visible = False

    def refreshView(self):
        p = BigWorld.player()
        info = self.getArenaPlayoffsInfo()
        self.widget.firstTitle.htmlText = info['title']
        self.widget.secondTitle.htmlText = info['secondTitle']
        self.widget.descPanel.canvas.text.htmlText = gameStrings.PVP_PLAYOFFS_V2_OPENING_TIME + '\n' + info['timeDesc'] + '\n' + gameStrings.PVP_PLAYOFFS_V2_HOW_TO_PLAY + '\n' + info['playDesc']
        self.initVisible()
        playoffsState = BigWorld.player().getArenaPlayoffs5V5State()
        if playoffsState == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD:
            self.widget.createTeam.createTeamBtn.enabled = True
        else:
            self.widget.createTeam.createTeamBtn.enabled = False
        if info['state'] == uiConst.ARENA_PLAYOFFS_STATE_LEADER:
            self.widget.addMemberBtn.visible = True
            self.widget.dismissTeamBtn.visible = True
            self.widget.applyTeamBtn.visible = True
            self.widget.addMemberBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.dismissTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.applyTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.addMemberBtn.enabled = info['canAddMember']
            self.widget.applyTeamBtn.enabled = info['canApplyTeam']
        elif info['state'] == uiConst.ARENA_PLAYOFFS_STATE_TEAMER or info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NORMAL:
            self.widget.leaveBtn.visible = True
            self.widget.leaveBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NO_TEAM:
            self.widget.attendRequirement.visible = True
            self.widget.createTeam.visible = True
            self.widget.createTeam.createTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NO_REQUIEMENT:
            self.widget.attendRequirement.visible = True
            self.widget.createTeam.visible = True
            self.widget.createTeam.createTeamBtn.enabled = False
            self.widget.createTeam.createTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        if info['state'] == uiConst.ARENA_PLAYOFFS_STATE_LEADER or info['state'] == uiConst.ARENA_PLAYOFFS_STATE_TEAMER or info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NORMAL:
            self.widget.playerList.visible = True
            self.widget.teamName.visible = True
            p = BigWorld.player()
            self.refreshPlayers(info['players'], p.getPlayoffs5V5UIState(isDone=False))
            self.widget.teamName.teamNameTxt.htmlText = info['teamName']
        if info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN:
            self.widget.requirementTxt.visible = True
            self.widget.requirementTxt.text.htmlText = gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME
        if playoffsState in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE,):
            self.widget.voteBtn.visible = True
            self.widget.rankBtn.visible = False
            if self.canBeVoted():
                self.widget.sendVoteBtn.visible = True
        if playoffsState == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD:
            self.widget.rankBtn.visible = True
        else:
            self.widget.rankBtn.visible = False
        if p.isPlayoffAidStateValid() and gameglobal.rds.configData.get('enableArenaPlayoffsAid', False):
            self.widget.supportBtn.visible = True
        else:
            self.widget.supportBtn.visible = False
        self.widget.supportBtn.addEventListener(events.BUTTON_CLICK, self.onSupportBtnClick)
        self.widget.participateBtn.enabled = info['canJoin']
        self.widget.reportBtn.visible = info['canViewReport']
        self.widget.betBtn.visible = info['betBtnVisible']

    def canBeVoted(self):
        p = BigWorld.player()
        if hasattr(p, 'arenaPlayoffsTeam'):
            if p.arenaPlayoffsTeam.get('canVoted', False):
                return True
        return False

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
                    if obj['selected']:
                        player.flagBtn.text = gameStrings.PVP_PLAYOFFS_V2_FIGHT
                        player.substituteBtn.label = gameStrings.PVP_PLAYOFFS_V2_SET_SUBSTITUTE
                    else:
                        player.flagBtn.text = gameStrings.PVP_PLAYOFFS_V2_SUBSTITUTE
                        player.substituteBtn.label = gameStrings.PVP_PLAYOFFS_V2_SET_FIGHT
                    player.substituteBtn.addEventListener(events.MOUSE_CLICK, self.handleFlagClick, False, 0, True)
                    player.removeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
                    if state == uiConst.ARENA_PLAYOFFS_STATE_LEADER:
                        player.substituteBtn.visible = True
                        player.removeBtn.visible = not self.isLeader(player.data['gbId'])
                    else:
                        player.substituteBtn.visible = False
                        player.removeBtn.visible = False
                    if p.gbId != long(player.data['gbId']):
                        menuParam = {'roleName': obj['name'],
                         'gbId': long(player.data['gbId']),
                         'fid': long(player.data['gbId'])}
                        MenuManager.getInstance().registerMenuById(player.playerNameTxt, uiConst.MENU_ARENA_PLAYOFFS_TEAM_INFO, menuParam)

    def isLeader(self, gbId):
        gbId = int(gbId)
        p = BigWorld.player()
        if p.arenaPlayoffsTeamNUID:
            if p.arenaPlayoffsTeamHeader == gbId:
                return True
        return False

    def handleFlagClick(self, *args):
        e = ASObject(args[3][0])
        obj = e.currentTarget.parent.data
        BigWorld.player().cell.setArenaPlayoffsTeamDuelFlag(int(obj['gbId']), not obj['selected'])

    def handleBtnStateChanged(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        targetBtn.playerNameTxt.text = targetBtn.data['name']
        targetBtn.scoreTxt.text = targetBtn.data['score']

    def onSupportBtnClick(self, *args):
        gameglobal.rds.ui.arenaPlayoffsSupport.show()

    def handleClickBtn(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        btnName = targetBtn.name
        p = BigWorld.player()
        if btnName == 'createTeamBtn':
            self.uiAdapter.arenaPlayoffs.showCreateTeam()
        elif btnName == 'dismissTeamBtn':
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_ARENA_PLAYOFFS_TEAM_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.disbandArenaPlayoffsTeam)
        elif btnName == 'leaveBtn':
            msg = uiUtils.getTextFromGMD(GMDD.data.LEAVE_ARENA_PLAYOFFS_TEAM_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitArenaPlayoffsTeam)
        elif btnName == 'applyTeamBtn':
            self.applyTeamDone()
        elif btnName == 'participateBtn':
            msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_PLAYOFFS_JOIN_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.enterPlayoffsArena)
        elif btnName == 'reportBtn':
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
        elif btnName == 'rewardBtn':
            gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_ARENA_PLAYOFFS_5V5)
        elif btnName == 'rankBtn':
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_PLAYOFFS_TEAM_COMBATSCORE)
        elif btnName == 'voteBtn':
            canAddFuDai = False
            if self.canBeVoted():
                canAddFuDai = True
            gameglobal.rds.ui.pvpPlayoffs5v5Vote.show(canAddFuDai)
        elif btnName == 'sendVoteBtn':
            self.sendVoteLink()

    def onVoteItemClick(self):
        p = BigWorld.player()
        playoffsState = BigWorld.player().getArenaPlayoffs5V5State()
        if playoffsState in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE,):
            canAddFuDai = False
            if self.canBeVoted():
                canAddFuDai = True
            gameglobal.rds.ui.pvpPlayoffs5v5Vote.show(canAddFuDai)
            gameglobal.rds.ui.pvpPlayoffs5v5Vote.show()
        elif p.isPlayoffAidStateValid():
            gameglobal.rds.ui.arenaPlayoffsSupport.show()
        else:
            BigWorld.player().showGameMsg(GMDD.data.PLAYOFFS_NOT_IN_VOTE_TIME, ())

    def sendVoteLink(self):
        p = BigWorld.player()
        lvKey = utils.lv2ArenaPlayoffsTeamkey(p.lv, gametypes.ARENA_PLAYOFFS_TYPE_5V5)
        if lvKey:
            mainTxt = DCD.data.get('playoffsVoteText', '%s') % p.arenaPlayoffsTeam.get('teamName', '')
            linkText = "<font color = \'#ffe566\' >%s</font><font color = \'#27A5D9\' ><a href=\"event:dPlayoffsCheer:%s,%s\"><u>[%s]</u></a></font>" % (mainTxt,
             str(lvKey),
             str(p.arenaPlayoffsTeamNUID),
             gameStrings.PVP_PLAYOFFS_VOTE_TXT)
            gameglobal.rds.ui.sendLink(linkText)

    @ui.checkInventoryLock()
    def applyTeamDone(self):
        BigWorld.player().cell.applyArenaPlayoffsTeamDone()

    def removeTeamer(self, id):
        gbId = int(id)
        p = BigWorld.player()
        roleName = p.arenaPlayoffsMember.get(gbId, {}).get('roleName', '')
        if gbId in p.arenaPlayoffsMember.keys():
            msg = uiUtils.getTextFromGMD(GMDD.data.KICK_OUT_ARENA_PLAYOFFS_TEAM_MSG, '%s') % roleName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.kickoutArenaPlayoffsTeam, gbId, roleName))

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
        for data in self.selectedFriends:
            BigWorld.player().cell.inviteArenaPlayoffsTeam(int(data.gbId))

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
        for gbId, member in p.arenaPlayoffsMember.items():
            memebers.append({'gbId': str(gbId),
             'name': member.get('roleName', ''),
             'online': member.get('isOn', 0),
             'selected': member.get('duelFlag', 0),
             'schoolTxt': uiConst.SCHOOL_FRAME_DESC.get(member.get('school', 0)),
             'score': member.get('lastSeasonScore')})

        curSch = self.getCurPlayoffsSchedule()
        info = {'state': p.getPlayoffs5V5UIState(),
         'canAddMember': len(p.arenaPlayoffsMember) < const.ARENA_PLAYOFFS_5V5_TEAM_MAX_NUM,
         'maxInviteMember': DCD.data.get('maxInviteMember', 2),
         'players': memebers,
         'canMark': p.arenaPlayoffsTeamHeader == p.gbId,
         'myGbId': p.gbId,
         'title': curSch.get('title', ''),
         'secondTitle': curSch.get('name', ''),
         'timeDesc': curSch.get('playoffsPlayDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'playDesc': curSch.get('playoffsTeamDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'playoffsTeamDesc': DCD.data.get('playoffsTeamDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'inviteMemberTip': DCD.data.get('inviteMemberTip', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'requiementDesc': gameStrings.ARENA_SCORE_NO_REQUIREMENT,
         'groupTxt': gameStrings.PVP_PLAYOFFS_V2_GROUP + uiUtils.toHtml(uiUtils.lv2ArenaPlayoffsTeamGroup(p.lv), '#ffbf40'),
         'teamName': p.arenaPlayoffsTeam.get('teamName', ''),
         'canApplyTeam': len(p.arenaPlayoffsMember) >= const.ARENA_PLAYOFFS_5V5_TEAM_MIN_NUM,
         'canJoin': p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL or p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL,
         'canViewReport': self.canViewReport(),
         'betBtnVisible': gameglobal.rds.configData.get('enableArenaPlayoffsBet', False)}
        return info

    def canViewReport(self):
        p = BigWorld.player()
        playoffsState = p.getArenaPlayoffs5V5State()
        return playoffsState in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_READY,
         gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING,
         gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_FINISHED,
         gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_READY,
         gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING,
         gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED)

    def getPlayoffsStateIndex(self, state):
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD):
            return 1
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE):
            return 2
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_READY, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_FINISHED):
            return 3
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_READY, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED):
            return 4
        return -1

    def getPlayoffsSeason(self):
        timeoffset = const.TIME_INTERVAL_DAY * 2
        return formula.getPlayoffsSeason(utils.getNow() + timeoffset)

    def getCurPlayoffsSchedule(self):
        defaultInfo = {'title': gameStrings.PLAYOFFS_5V5_TITLE}
        p = BigWorld.player()
        state = p.getArenaPlayoffs5V5State()
        schedule = self.getArenaPlayOffSchedule()
        stateIndex = self.getPlayoffsStateIndex(state)
        if stateIndex == 1:
            val = copy.deepcopy(A5SDD.data.get(1))
            val['playoffsPlayDesc'] = gameStrings.ARENA_PLAYOFFS_5V5_DESC % (schedule['applyStartTime'].month,
             schedule['applyStartTime'].day,
             schedule['applyEndTime'].month,
             schedule['applyEndTime'].day)
            return val
        if stateIndex in (2, 3, 4):
            val = A5SDD.data.get(stateIndex)
            return val
        if utils.inCrontabRange(schedule['applyShowTime'], schedule['applyStartCrontab']):
            val = copy.deepcopy(A5SDD.data.get(1))
            val['playoffsPlayDesc'] = gameStrings.ARENA_PLAYOFFS_5V5_DESC % (schedule['applyStartTime'].month,
             schedule['applyStartTime'].day,
             schedule['applyEndTime'].month,
             schedule['applyEndTime'].day)
            return val
        return defaultInfo

    def getCrontabByState(self, curArenaPlayoffsSeason, state):
        stateIdx = duelUtils.getCrontabIdByPlayoffsState(gametypes.ARENA_PLAYOFFS_TYPE_5V5, state)
        return duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_5V5)

    def getArenaPlayOffSchedule(self):
        curArenaPlayoffsSeason = self.getPlayoffsSeason()
        schedule = {}
        applyStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD)
        startTime = utils.getDisposableCronTabTimeStamp(applyStartCrontab)
        applyDateTime = datetime.datetime.fromtimestamp(startTime)
        applyShowTime = applyDateTime - datetime.timedelta(days=2)
        applyEndCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD)
        applyEndTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(applyEndCrontab))
        voteStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE)
        voteStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(voteStartCrontab))
        voteEndCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE)
        voteEndTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(voteEndCrontab))
        groupStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING)
        groupStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(groupStartCrontab))
        kickOutStartCrontab = self.getCrontabByState(curArenaPlayoffsSeason, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING)
        kickOutStartTime = datetime.datetime.fromtimestamp(utils.getDisposableCronTabTimeStamp(kickOutStartCrontab))
        schedule['applyShowTime'] = '0 8 %d %d *' % (applyShowTime.day, applyShowTime.month)
        schedule['startCrontab'] = applyStartCrontab
        schedule['startTime'] = startTime
        schedule['applyDateTime'] = applyDateTime
        schedule['applyStartTime'] = applyDateTime
        schedule['applyStartCrontab'] = applyStartCrontab
        schedule['applyEndTime'] = applyEndTime
        schedule['applyEndCrontab'] = applyEndCrontab
        schedule['voteStartTime'] = voteStartTime
        schedule['voteStartCrontab'] = voteStartCrontab
        schedule['voteEndTime'] = voteEndTime
        schedule['voteEndCrontab'] = voteEndCrontab
        schedule['groupStartTime'] = groupStartTime
        schedule['groupStartCrontab'] = groupStartCrontab
        schedule['kickOutStartTime'] = kickOutStartTime
        schedule['kickOutStartCrontab'] = kickOutStartCrontab
        return schedule

    def getMatchesSchedule(self):
        matchesSchedule = []
        schedule = self.getArenaPlayOffSchedule()
        firstRound = schedule['groupStartTime']
        dayOffset = 0
        index = 0
        for key in sorted(A5GDD.data.keys()):
            matchRound = firstRound + datetime.timedelta(days=dayOffset)
            mathchRoundDesc = {}
            val = A5GDD.data[key]
            lvKey = utils.lv2ArenaPlayoffs5v5Teamkey(BigWorld.player().lv)
            if val.get('type') == arenaPlayoffsProxy.TYPE_GROUP_DUEL and lvKey == key[1]:
                mathchRoundDesc['startStage'] = 0
                mathchRoundDesc['type'] = val.get('type')
                now = utils.getNow()
                currentYear = datetime.datetime.fromtimestamp(now).year
                startContab = val.get('startContab', '30 19 %d %d * %d')
                enterCrontab = val.get('enterCrontab', '20 19 %d %d * %d')
                startTime = val.get('startTime', '%d.%d.%d.19.0.0')
                endTime = val.get('endTime', '%d.%d.%d.20.20.0')
                matchRoundCrontab = startContab % (matchRound.day, matchRound.month, currentYear)
                matchRoundEnterCrontab = enterCrontab % (matchRound.day, matchRound.month, currentYear)
                mathchRoundDesc['startStage'] = 0
                if utils.inTimeRange(matchRoundCrontab, matchRoundEnterCrontab):
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

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.refreshView()
        self.widget.betBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.rankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.reportBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.participateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.sendVoteBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.voteBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.netUrl.htmlText = DCD.data.get('arenaPlayoffs5v5LinkText', '')
        self.widget.dandanUrl.htmlText = DCD.data.get('arenaPlayoffs5v5DanDanText', gameStrings.TEXT_PVPPLAYOFFS5V5PROXY_534)

    def refreshPlayoffsPanel(self):
        if self.isTeamCreated():
            self.removePlayoffs5v5PushMsg()
        if self.widget:
            self.refreshView()

    def isTeamCreated(self):
        p = BigWorld.player()
        if hasattr(p, 'arenaPlayoffsTeam') and p.arenaPlayoffsTeam.get('isDone', False):
            return True
        return False

    def addPlayoffsPushMsg(self, lvKey, state):
        p = BigWorld.player()
        if lvKey == utils.lv2ArenaPlayoffsTeamkey(p.lv, gametypes.ARENA_PLAYOFFS_TYPE_5V5):
            if state == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START, {'click': self.onPlayoffs5v5PushMsgClick})
            elif uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START in gameglobal.rds.ui.pushMessage.msgs:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START)

    def removePlayoffs5v5PushMsg(self):
        if uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_PLAYOFFS_5V5_START)

    def onPlayoffs5v5PushMsgClick(self):
        gameglobal.rds.ui.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_5V5_PLAYOFFS)
        self.removePlayoffs5v5PushMsg()
