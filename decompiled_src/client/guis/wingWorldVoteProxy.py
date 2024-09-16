#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldVoteProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import tipUtils
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis import ui
from guis.asObject import ASObject
from commonWingWorld import WWArmyPostVal
from asObject import TipManager
from gamestrings import gameStrings

class WingWorldVoteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldVoteProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_VOTE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_VOTE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleCloseClick, False, 0, True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_VOTE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_VOTE)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        p.cell.queryWingWorldArmy(p.wingWorld.armyVer, p.wingWorld.armyOnlineVer)
        self.refreshVoteBtns(p.wingWorldArmyVoteGbId)

    def handleCloseClick(self, *args):
        self.clearWidget()

    def handleVoteClick(self, *args):
        btn = ASObject(args[3][0]).target
        p = BigWorld.player()
        if btn.label == gameStrings.TEXT_WINGWORLDVOTEPROXY_53:
            p.cell.voteWingWorldArmyLeader(int(btn.gbId))
        else:
            p.cell.abandonVoteWingWorldArmyLeader()

    def refreshVoteBtns(self, gbId):
        if not self.widget:
            return
        armyList = gameglobal.rds.ui.wingWorld.getVoteArmyInfo()
        for i, player in enumerate(armyList):
            item = self.widget.voteList.canvas.getChildByName('player%d' % i)
            if not item:
                continue
            item.visible = True
            item.index.text = str(player[1]['index'])
            item.playerName.text = player[1]['name']
            item.guildName.text = player[1]['guildName']
            item.source.text = player[1]['source']
            item.votes.text = str(player[1]['votes'])
            item.voteBtn.visible = player[1]['canVote']
            item.voteBtn.gbId = player[1]['gbId']
            item.voteBtn.addEventListener(events.BUTTON_CLICK, self.handleVoteClick, False, 0, True)
            if gbId == 0:
                item.voteBtn.enabled = True
                item.voteBtn.label = gameStrings.TEXT_WINGWORLDVOTEPROXY_53
            elif player[1]['gbId'] == gbId:
                item.voteBtn.label = gameStrings.TEXT_WINGWORLDVOTEPROXY_81
            else:
                item.voteBtn.enabled = False
                item.voteBtn.label = gameStrings.TEXT_WINGWORLDVOTEPROXY_53
            votesInfo = player[1]['votesInfo']
            if votesInfo:
                tipString = gameStrings.WING_WORLD_VOTE_TIP_TITLE
                for info in votesInfo:
                    tipString = tipString + gameStrings.WING_WORLD_VOTE_TIP_INFO % (info['guildName'], info['name'])

                TipManager.addTip(item, tipString, tipUtils.TYPE_DEFAULT_BLACK, 'over', 'mouse')

        for i in range(len(armyList), 13):
            item = self.widget.voteList.canvas.getChildByName('player%d' % i)
            item.visible = False

    def updateArmyPostData(self, armyInfo, armyVer):
        dto = armyInfo.getDTO()
        p = BigWorld.player()
        p.wingWorld.refreshArmy(p.gbId, dto)
        p.wingWorld.armyVer = armyVer
        self.refreshInfo()
