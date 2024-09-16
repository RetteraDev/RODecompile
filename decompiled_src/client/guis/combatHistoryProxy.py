#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/combatHistoryProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
from guis import ui
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings

class CombatHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CombatHistoryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rounds = {}
        self.players = {}
        self.version = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_COMBAT_HISTORY, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_COMBAT_HISTORY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_COMBAT_HISTORY)

    def onGetServerData(self, data):
        self.rounds = data.get('rounds', {})
        self.players = data.get('players', {})
        self.version = data.get('version', 0)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_COMBAT_HISTORY)
        else:
            self.refreshHistory()

    def show(self):
        if self.version:
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_WING_COMBAT_HISTORY)
        self.queryServerInfo()

    @ui.callInCD(5)
    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.queryWingWorldXinMoArenaHistory(self.version)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.roundDrop.labelFunction = self.dropDownlabelFunction
        self.widget.roundDrop.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
        for i in range(9):
            matchMc = self.widget.getChildByName('match%d' % i)
            matchMc.addEventListener(events.MOUSE_ROLL_OVER, self.onItemMouseOver)
            matchMc.addEventListener(events.MOUSE_ROLL_OUT, self.onItemMouseOut)
            matchMc.addEventListener(events.MOUSE_CLICK, self.onItemClick)

        self.refreshHistory()
        self.widget.roundDrop.selectedIndex = 0

    def refreshHistory(self):
        ASUtils.setDropdownMenuData(self.widget.roundDrop, self.getArenaList())
        self.showHistory(1)

    def handleIndexChange(self, *args):
        self.roundNo = self.widget.roundDrop.selectedIndex + 1
        self.showHistory(self.roundNo)

    def showHistory(self, roundNo):
        self.clearArenaList()
        self.roundNo = roundNo
        roundInfo = self.rounds.get(roundNo, {})
        matches = roundInfo.get('matches', {})
        for i, matchNo in enumerate(matches):
            matchMc = self.widget.getChildByName('match%d' % i)
            matchMc.visible = True
            self.setMatchInfo(i, matchNo, 'up')

    def setMatchInfo(self, index, matchNo, state):
        if matchNo == None:
            return
        else:
            matchMc = self.widget.getChildByName('match%d' % index)
            if matchMc.selected:
                matchMc.gotoAndStop('select')
            else:
                matchMc.gotoAndStop(state)
            matchMc.index = index
            matchMc.matchNo = matchNo
            roundInfo = self.rounds.get(self.roundNo, {})
            matchInfo = roundInfo.get('matches', {}).get(matchNo, ((), 0))
            teams = roundInfo.get('teams', {})
            groupIds = matchInfo[0]
            winnerGroupId = matchInfo[1]
            if not groupIds:
                matchMc.visible = False
            matchMc.arenaName.text = gameStrings.WING_WORLD_ARENA_LABEL[matchNo]
            for i, groupId in enumerate(groupIds):
                matchMc.vsTxt.text = gameStrings.WING_WORLD_ARENA_VS
                teamName = teams.get(groupId, '')[0]
                if len(groupIds) == 1:
                    matchMc.winIcon0.visible = True
                    matchMc.teamName0.text = teamName
                    matchMc.vsTxt.text = gameStrings.WING_WORLD_ARENA_VS_NONE
                    matchMc.winIcon1.visible = False
                    matchMc.teamName1.text = ''
                else:
                    matchMc.getChildByName('winIcon%d' % i).visible = groupId == winnerGroupId
                    matchMc.getChildByName('teamName%d' % i).text = teamName

            return

    def onItemMouseOver(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.setMatchInfo(itemMc.index, itemMc.matchNo, 'over')

    def onItemMouseOut(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.setMatchInfo(itemMc.index, itemMc.matchNo, 'up')

    def onItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        for i in range(9):
            matchMc = self.widget.getChildByName('match%d' % i)
            if i == itemMc.index:
                matchMc.selected = True
                self.setMatchInfo(i, itemMc.matchNo, 'select')
                self.showTeamInfo(itemMc.matchNo)
            else:
                matchMc.selected = False
                if matchMc.matchNo and matchMc.visible:
                    self.setMatchInfo(i, matchMc.matchNo, 'up')

    def showTeamInfo(self, matchNo):
        roundInfo = self.rounds.get(self.roundNo, {})
        matchInfo = roundInfo.get('matches', {}).get(matchNo, ((), 0))
        teams = roundInfo.get('teams', {})
        groupIds = matchInfo[0]
        winnerGroupId = matchInfo[1]
        for i in range(2):
            teamMc = self.widget.getChildByName('team%d' % i)
            teamMc.visible = False

        for i, groupId in enumerate(groupIds):
            teamMc = self.widget.getChildByName('team%d' % i)
            teamMc.visible = True
            teamInfo = teams.get(groupId, ('', (), 0))
            teamName = teamInfo[0]
            memberGbIds = teamInfo[1]
            headerGbId = teamInfo[2]
            teamMc.teamName.text = teamName
            teamMc.winIcon.visible = winnerGroupId == groupId
            for memberIndex in range(5):
                playerMc = teamMc.getChildByName('player%d' % memberIndex)
                playerMc.visible = False

            for memberIndex, memberId in enumerate(memberGbIds):
                playerMc = teamMc.getChildByName('player%d' % memberIndex)
                playerMc.visible = True
                playerMc.leaderIcon.visible = memberId == headerGbId
                playerInfo = self.players.get(memberId, ('', 0))
                playerMc.playerName.text = playerInfo[0]
                playerMc.playerSchool.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(playerInfo[1], 'yuxu'))

    def getArenaList(self):
        arenaList = []
        for roundNo in self.rounds.keys():
            info = {}
            info['round'] = roundNo
            info['label'] = gameStrings.WING_WORLD_ROUND_LABEL[roundNo]
            arenaList.append(info)

        return arenaList

    def clearArenaList(self):
        for i in range(9):
            itemMc = self.widget.getChildByName('match%d' % i)
            itemMc.visible = False

        self.widget.team0.visible = False
        self.widget.team1.visible = False

    def dropDownlabelFunction(self, *args):
        label = ASObject(args[3][0]).label
        return GfxValue(ui.gbk2unicode(label))

    def refreshInfo(self):
        if not self.widget:
            return
