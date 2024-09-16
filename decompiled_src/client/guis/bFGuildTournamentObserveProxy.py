#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFGuildTournamentObserveProxy.o
import BigWorld
import gameglobal
import utils
import gametypes
from gamestrings import gameStrings
import uiConst
import events
import formula
from data import clan_war_challenge_config_data as CWCCD
from uiProxy import UIProxy
OFFSET = 53
BTN_NAMES = ['statisticBtn',
 'encourageBtn',
 'praiseBtn',
 'switchCameraBtn',
 'leaveBtn']
START_X = 22
BTN_WIDTH = 48

class BFGuildTournamentObserveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFGuildTournamentObserveProxy, self).__init__(uiAdapter)
        self.widget = None
        self.coolDownTimeTick = None

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_OBSERVE)

    def initUI(self):
        panel = self.widget.panel
        panel.statisticBtn.addEventListener(events.MOUSE_CLICK, self.handleClickStatistic)
        panel.encourageBtn.btn.addEventListener(events.MOUSE_CLICK, self.handleClickEncourage)
        panel.praiseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPraise)
        panel.switchCameraBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSwitchCamera)
        panel.leaveBtn.addEventListener(events.MOUSE_CLICK, self.handleClickLeave)
        self.refreshCoolDown()
        self.relayout()

    def refreshCoolDown(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if p.inClanChallengeOb():
                self.refreshClanWarChallengeInspreInfo(getattr(p, 'clanChallengeInspireCnt', 0), None)
            gameglobal.rds.ui.bFGuildTournamentLive.refreshCoolDownWithMc(self.widget.panel.encourageBtn)
            return

    def refreshClanWarChallengeInspreInfo(self, inspreCnt, oldValue):
        if oldValue != None and inspreCnt != oldValue:
            coolDownReady = utils.getNow() + CWCCD.data.get('inspireInterval', 60)
            BigWorld.player().onUpdateGtInspireCoolDown(coolDownReady)
        if self.widget:
            self.widget.panel.encourageBtn.btn.label = gameStrings.CLAN_CHALLENGE_INSPIRE_CNT % inspreCnt

    def setCoolDown(self, coolDownReady):
        self.coolDownReady = coolDownReady
        if self.coolDownTimeTick:
            BigWorld.cancelCallback(self.coolDownTimeTick)
        self.coolDownTimeTick = BigWorld.callback(1, self.handleCoolDown)

    def handleCoolDown(self):
        countTime = gameglobal.rds.ui.bFGuildTournamentLive.getCoolDownDurationTime()
        if countTime <= 0:
            BigWorld.cancelCallback(self.coolDownTimeTick)
        else:
            self.coolDownTimeTick = BigWorld.callback(1, self.handleCoolDown)
        self.refreshCoolDown()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_OBSERVE)

    def isAvaliable(self):
        p = BigWorld.player()
        if p.inFightObserve() and (formula.inGuildTournamentBH(getattr(p, 'mapID', 0)) or formula.inGuildTournamentQL(getattr(p, 'mapID', 0))):
            return True
        if p.inFightObserve() and (formula.inNewGuildTournamentQL(getattr(p, 'mapID', 0)) or formula.inNewGuildTournamentBH(getattr(p, 'mapID', 0))):
            return True
        return False

    def relayout(self):
        p = BigWorld.player()
        if p.inClanChallengeOb():
            self.widget.panel.praiseBtn.visbile = False
            poxX = self.widget.panel.praiseBtn.x
            self.widget.panel.switchCameraBtn.x = poxX
            poxX += 43
            self.widget.panel.leaveBtn.x = poxX
            return
        if not hasattr(p, 'bfAllSideNUID'):
            return
        isNeedEncourage = False
        for sideNUID in p.bfAllSideNUID:
            guildNUID = sideNUID >> 1
            if p.guildNUID == guildNUID:
                isNeedEncourage = True

        if not isNeedEncourage:
            self.widget.panel.encourageBtn.visible = False
            self.widget.panel.praiseBtn.x = self.widget.panel.praiseBtn.x - OFFSET
            self.widget.panel.switchCameraBtn.x = self.widget.panel.switchCameraBtn.x - OFFSET
            self.widget.panel.leaveBtn.x = self.widget.panel.leaveBtn.x - OFFSET
        if formula.inNewGuildTournamentQL(getattr(p, 'mapID', 0)) or formula.inNewGuildTournamentBH(getattr(p, 'mapID', 0)):
            self.widget.panel.encourageBtn.visible = True
            self.widget.panel.praiseBtn.visible = False
        currX = START_X
        for btnName in BTN_NAMES:
            itemMc = self.widget.panel.getChildByName(btnName)
            if itemMc.visible:
                itemMc.x = currX
                currX += BTN_WIDTH

    def handleClickStatistic(self, *args):
        if BigWorld.player().inClanChallengeOb():
            clanChallengeCombatResult = getattr(BigWorld.player(), 'clanChallengeCombatResult', {})
            BigWorld.player().cell.queryClanWarChallengeCombatInfo(clanChallengeCombatResult[0], BigWorld.player().getClanChallengeHostId())
        else:
            gameglobal.rds.ui.battleField.showBFTmpResultWidget()

    def handleClickPraise(self, *args):
        p = BigWorld.player()
        p.cell.requireAddPraiseForGTournament(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL)

    def handleClickEncourage(self, *args):
        p = BigWorld.player()
        if p.inClanChallengeOb():
            p.cell.inspireClanWarChallenge()
        else:
            p.cell.requireInspireGuildTournamentMembers()

    def handleClickSwitchCamera(self, *args):
        BigWorld.player().cell.obRandomTgt()

    def handleClickLeave(self, *args):
        if BigWorld.player().inClanChallengeOb():
            BigWorld.player().cell.endObserveFuben()
            return
        BigWorld.player().cell.quitBattleField()
