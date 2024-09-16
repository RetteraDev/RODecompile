#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpPlayoffsV2Proxy.o
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
from data import duel_config_data as DCD
from guis.asObject import MenuManager
from data import arena_playoffs_schedule_desc_data as APSDD
from cdata import game_msg_def_data as GMDD
STATE_NO_TEAM = 1
STATE_NO_REQUIEMENT = 2
STATE_LEADER = 3
STATE_TEAMER = 4
STATE_NORMAL = 5
MAX_TEAM_MEMBER = 4

class PvpPlayoffsV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpPlayoffsV2Proxy, self).__init__(uiAdapter)
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

    def refreshView(self):
        info = self.getArenaPlayoffsInfo()
        self.widget.secondTitle.htmlText = info['secondTitle']
        self.widget.descPanel.canvas.text.htmlText = gameStrings.PVP_PLAYOFFS_V2_OPENING_TIME + '\n' + info['timeDesc'] + '\n' + gameStrings.PVP_PLAYOFFS_V2_HOW_TO_PLAY + '\n' + info['playDesc']
        self.initVisible()
        if info['state'] == STATE_LEADER:
            self.widget.addMemberBtn.visible = True
            self.widget.dismissTeamBtn.visible = True
            self.widget.applyTeamBtn.visible = True
            self.widget.addMemberBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.dismissTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.applyTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            self.widget.addMemberBtn.enabled = info['canAddMember']
            self.widget.applyTeamBtn.enabled = info['canApplyTeam']
        elif info['state'] == STATE_TEAMER or info['state'] == STATE_NORMAL:
            self.widget.leaveBtn.visible = True
            self.widget.leaveBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == STATE_NO_TEAM:
            self.widget.createTeam.visible = True
            self.widget.createTeam.createTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        elif info['state'] == STATE_NO_REQUIEMENT:
            self.widget.requirementTxt.visible = True
            self.widget.requirementTxt.text.htmlText = info['requiementDesc'].replace('\n', '')
        if info['state'] == STATE_LEADER or info['state'] == STATE_TEAMER or info['state'] == STATE_NORMAL:
            self.widget.playerList.visible = True
            self.widget.teamName.visible = True
            p = BigWorld.player()
            self.refreshPlayers(info['players'], p.getPlayoffsUIState(isDone=False))
            self.widget.teamName.teamNameTxt.htmlText = info['teamName']
        if info['state'] == uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN:
            self.widget.requirementTxt.visible = True
            self.widget.requirementTxt.text.htmlText = gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME
        self.widget.participateBtn.enabled = info['canJoin']
        self.widget.reportBtn.enabled = info['canViewReport']
        self.widget.betBtn.visible = info['betBtnVisible']

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
                    if state == STATE_LEADER:
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
        info = {'state': p.getPlayoffsUIState(),
         'canAddMember': len(p.arenaPlayoffsMember) < const.ARENA_PLAYOFFS_TEAM_MAX_NUM,
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
         'requiementDesc': DCD.data.get('requiementDesc', gameStrings.ARENA_PLAYOFFS_NOT_IN_TIME),
         'groupTxt': gameStrings.PVP_PLAYOFFS_V2_GROUP + uiUtils.toHtml(uiUtils.lv2ArenaPlayoffsTeamGroup(p.lv), '#ffbf40'),
         'teamName': p.arenaPlayoffsTeam.get('teamName', ''),
         'canApplyTeam': len(p.arenaPlayoffsMember) >= const.ARENA_PLAYOFFS_TEAM_MAX_NUM - 1,
         'canJoin': p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL or p.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL,
         'canViewReport': True,
         'betBtnVisible': gameglobal.rds.configData.get('enableArenaPlayoffsBet', False)}
        return info

    def getPlayoffsStateIndex(self, state):
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD):
            return 1
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_READY, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING, gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_FINISHED):
            return 2
        if state in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_READY, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING, gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED):
            return 3
        return -1

    def getCurPlayoffsSchedule(self):
        p = BigWorld.player()
        state = p.getArenaPlayoffs3V3State()
        stateIndex = self.getPlayoffsStateIndex(state)
        schedule = self.getArenaPlayOffSchedule()
        if stateIndex in (2, 3):
            return APSDD.data.get(stateIndex)
        elif stateIndex == 1:
            val = copy.deepcopy(APSDD.data.get(1))
            val['playoffsPlayDesc'] = gameStrings.ARENA_PLAYOFFS_DESC % (schedule['applyStartTime'].month,
             schedule['applyStartTime'].day,
             schedule['applyEndTime'].month,
             schedule['applyEndTime'].day)
            return val
        elif utils.inCrontabRange(schedule['applyShowTime'], schedule['applyEndCrontab']):
            val = copy.deepcopy(APSDD.data.get(1))
            val['playoffsPlayDesc'] = gameStrings.ARENA_PLAYOFFS_DESC % (schedule['applyStartTime'].month,
             schedule['applyStartTime'].day,
             schedule['applyEndTime'].month,
             schedule['applyEndTime'].day)
            return val
        else:
            return {}

    def getPlayoffsSeason(self):
        timeoffset = const.TIME_INTERVAL_DAY * 2
        return formula.getPlayoffsSeason(utils.getNow() + timeoffset)

    def getCrontabByState(self, curArenaPlayoffsSeason, state):
        stateIdx = duelUtils.getCrontabIdByPlayoffsState(gametypes.ARENA_PLAYOFFS_TYPE_3V3, state)
        return duelUtils.genArenaPlayoffsCrontabStr(curArenaPlayoffsSeason, stateIdx, gametypes.ARENA_PLAYOFFS_TYPE_3V3)

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

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.refreshView()
        self.widget.betBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.reportBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
        self.widget.participateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)

    def refreshPlayoffsPanel(self):
        if self.widget:
            self.refreshView()
