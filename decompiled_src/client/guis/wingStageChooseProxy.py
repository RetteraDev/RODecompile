#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingStageChooseProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import ui
from guis.asObject import ASObject
from gamestrings import gameStrings
from guis import uiUtils
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import wing_world_config_data as WWCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
BTN_NUM = 9
roundNumList = [9,
 5,
 3,
 2,
 1]

class WingStageChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingStageChooseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.version = 0
        self.roundNo = 0
        self.matches = {}
        self.teams = {}
        self.players = {}
        self.allows = ()
        self.loses = ()
        self.selMatchNo = 1
        self.currChoose = {}
        self.callback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_STAGET_CHOOSE, self.hide)

    def reset(self):
        self.selMatchNo = 1

    def onGetServerData(self, data):
        if data:
            self.roundNo = data.get('roundNo', 0)
            self.matches = data.get('matches', {})
            self.teams = data.get('teams', {})
            self.players = data.get('players', {})
            self.allows = data.get('allows', ())
            self.loses = data.get('loses', ())
            self.version = data.get('version', 0)
            self.selMatchNo = self.selMatchNo if self.selMatchNo else 1
        if self.callback:
            self.callback()
            self.callback = None
        if self.widget:
            self.refreshArenaList()

    def onApplyArenaSucc(self, matchNo):
        self.currChoose[self.roundNo] = matchNo
        if self.widget:
            self.showCurrentChoose()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_STAGET_CHOOSE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def refreshArenaList(self):
        if not self.widget:
            return
        else:
            isAllowed = self.needChooseArena()
            self.initTeamVisible()
            for i in range(BTN_NUM):
                itemMc = getattr(self.widget, 'stage%d' % i, None)
                if itemMc:
                    itemMc.visible = False

            for index, matchNo in enumerate(self.matches):
                matchBtn = self.widget.getChildByName('stage%d' % index)
                ASUtils.setHitTestDisable(matchBtn.currentChoose, True)
                ASUtils.setHitTestDisable(matchBtn.inCombatText, True)
                matchBtn.currentChoose.visible = False
                matchInfo = self.matches.get(matchNo, ((), 0, 0))
                groupIds = matchInfo[0]
                state = matchInfo[2]
                matchBtn.inCombatText.text = gameStrings.WING_WORLD_ARENA_STATE_LABEL[state]
                matchBtn.data = matchNo
                matchBtn.chooseBtn.label = gameStrings.WING_WORLD_ARENA_LABEL[matchNo]
                matchBtn.addEventListener(events.MOUSE_CLICK, self.onClickMatchBtn, False, 0, True)
                matchBtn.visible = True
                if matchNo == self.selMatchNo:
                    self.selectBtnByIndex(matchNo - 1)
                    self.showTeamInfo(self.selMatchNo)

            self.showCurrentChoose()
            return

    def onClickMatchBtn(self, *args):
        e = ASObject(args[3][0])
        matchNo = e.currentTarget.data
        self.selMatchNo = matchNo
        self.selectBtnByIndex(matchNo - 1)
        matchInfo = self.matches.get(matchNo, ((), 0, 0))
        state = matchInfo[2]
        self.showTeamInfo(self.selMatchNo)

    def selectBtnByIndex(self, selIndex):
        for index in range(BTN_NUM):
            matchBtn = self.widget.getChildByName('stage%d' % index)
            matchBtn.chooseBtn.selected = index == selIndex

    def showCurrentChoose(self):
        p = BigWorld.player()
        selIndex = self.currChoose.get(self.roundNo, 0) - 1
        for index in range(BTN_NUM):
            matchBtn = self.widget.getChildByName('stage%d' % index)
            matchBtn.currentChoose.visible = index == selIndex

    def onFocusOut(self, *args):
        e = ASObject(args[3][0])
        self.selMatchNo = 0
        self.initTeamVisible()

    def initTeamVisible(self):
        for i in range(2):
            itemMc = self.widget.getChildByName('team%d' % i)
            itemMc.visible = False

    def showTeamInfo(self, matchNo):
        matchInfo = self.matches.get(matchNo, ((), 0, 0))
        groupNUIDs = matchInfo[0]
        winnerGroupNUID = matchInfo[1]
        self.widget.team0.visible = False
        self.widget.team1.visible = False
        self.initTeamVisible()
        for index, id in enumerate(groupNUIDs):
            teamInfo = self.teams.get(id, ('', (), 0))
            teamName = teamInfo[0]
            memberGbIds = teamInfo[1]
            headerGBId = teamInfo[2]
            szDesc = ''
            if id == winnerGroupNUID:
                szDesc = gameStrings.WING_STAGE_CHOOLSE_TEAM_DESC0 if len(groupNUIDs) == 1 else gameStrings.WING_STAGE_CHOOLSE_TEAM_DESC1
            itemMc = self.widget.getChildByName('team%d' % index)
            itemMc.visible = True
            itemMc.teamName.text = teamName + szDesc
            for i in xrange(5):
                memberMc = itemMc.getChildByName('player%d' % i)
                memberMc.visible = False

            for memberIndex, memberId in enumerate(memberGbIds):
                playerInfo = self.players.get(memberId, ('', 0))
                name = playerInfo[0]
                school = playerInfo[1]
                if memberIndex > 4:
                    continue
                memberMc = itemMc.getChildByName('player%d' % memberIndex)
                memberMc.visible = True
                memberMc.leaderIcon.visible = memberId == headerGBId
                memberMc.playerName.text = name
                memberMc.playerSchool.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_STAGET_CHOOSE)

    def show(self):
        self.queryServerInfo()
        if self.widget:
            self.refreshArenaList()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_STAGET_CHOOSE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.onRefreshBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick, False, 0, True)
        self.refreshArenaList()

    def refreshInfo(self):
        if not self.widget:
            return

    @ui.callFilter(2, True)
    def onConfirmBtnClick(self, *args):
        if self.needChooseArena():
            p = BigWorld.player()
            self.queryServerInfo()
            p.cell.applyWingWorldXinMoArena(self.selMatchNo)
            p.base.queryWingWorldXinMoArena(self.version)
        else:
            gameglobal.rds.ui.zhiQiangDuiJue.show(0, self.roundNo, self.selMatchNo)
            self.clearWidget()

    def onRefreshBtnClick(self, *args):
        self.queryServerInfo()

    @ui.callFilter(5, True)
    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.queryWingWorldXinMoArena(self.version)

    @ui.callFilter(5, True)
    def queryDataWithCallBack(self, dataCallback):
        p = BigWorld.player()
        p.base.queryWingWorldXinMoArena(self.version)
        self.callback = dataCallback

    def needChooseArena(self):
        p = BigWorld.player()
        alreadyChoose = False
        for matchNo in self.matches:
            groupNUIDs, winGroupNUID, state = self.matches.get(matchNo, ((), 0, 0))
            if p.groupNUID in groupNUIDs:
                alreadyChoose = True

        isAllowd = self.isAllowdLeader()
        isLose = False
        if p.groupNUID in self.loses:
            isLose = True
        return isAllowd and not alreadyChoose and not isLose

    def getAvaliableArena(self):
        avaliabeList = []
        for matchNo in self.matches:
            matchInfo = self.matches.get(matchNo, (0, 0, 0))
            arenaState = matchInfo[2]
            if arenaState == const.WING_WORLD_XINMO_ARENA_MATCH_STATE_PREPARE or arenaState == const.WING_WORLD_XINMO_ARENA_MATCH_STATE_RUNNING:
                avaliabeList.append(matchNo)

        return avaliabeList

    def isAllowdLeader(self):
        requireItemId = WWCD.data.get('xinmoTicketItemId', 0)
        p = BigWorld.player()
        itemNum = p.crossInv.countItemInPages(requireItemId)
        if (itemNum or p.groupNUID in self.allows) and p.isTeamLeader():
            return True
        else:
            return False
