#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArenaHoverProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import const
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
ARENA_PANEL_STAGE_INIT = 1
ARENA_PANEL_STAGE_WAITING_TEAM = 2
ARENA_PANEL_STAGE_MATCHING = 3
ARENA_PANEL_STAGE_IN_GAME = 4
ARENA_PANEL_STAGE_MATCHED = 5
ARENA_MODE_RANK = 1
ARENA_MODE_SHUANGREN = 2
ARENA_MODE_SCORE_PLAYOFF = 3

class BalanceArenaHoverProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArenaHoverProxy, self).__init__(uiAdapter)
        self.widget = None
        self.arenaMode = 0
        self.stage = 1
        self.mode = ARENA_MODE_RANK
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_HOVER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_HOVER)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_HOVER)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.templateBtn.addEventListener(events.BUTTON_CLICK, self.showTemplates)
        p = BigWorld.player()
        self.widget.adjustMenu.visible = False
        if p.canChangeTemplate():
            self.widget.adjustMenu.adjustSkillBtn.addEventListener(events.MOUSE_DOWN, self.openSkillWindow, False, 0, True)
            self.widget.adjustMenu.adjustPropBtn.addEventListener(events.MOUSE_DOWN, self.openPropWindow, False, 0, True)
            self.widget.adjustBtn.addEventListener(events.BUTTON_CLICK, self.showAdjustMenu)
            self.widget.adjustMenu.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.hideAdjustMenu, False, 0, True)
        else:
            self.widget.adjustBtn.enabled = False
        self.widget.matchBtn.addEventListener(events.BUTTON_CLICK, self.matchArena)
        self.addEvent(events.EVENT_CHANGE_GROUP_STATE, self.onGroupStateChanged)
        self.addEvent(events.EVENT_CHANGE_ARENA_STATE, self.refreshInfo)

    def showAdjustMenu(self, *args):
        self.widget.adjustMenu.visible = True
        self.widget.adjustMenu.gotoAndPlay(1)
        self.widget.stage.focus = self.widget.adjustMenu

    def hideAdjustMenu(self, *args):
        e = ASObject(args[3][0])
        if not self.widget:
            return
        self.widget.adjustMenu.visible = False

    def openPropWindow(self, *args):
        gameglobal.rds.ui.roleInfo.show()

    def openSkillWindow(self, *args):
        gameglobal.rds.ui.skill.show()

    def showTemplates(self, *args):
        gameglobal.rds.ui.balanceArenaTemplate.show()

    def matchArena(self, *args):
        p = BigWorld.player()
        stage = getattr(p, 'arenaStage', 1)
        if self.stage != stage:
            self.refreshInfo()
        if self.stage == ARENA_PANEL_STAGE_MATCHING or self.stage == ARENA_PANEL_STAGE_WAITING_TEAM:
            p.cancelApplyArena()
        else:
            arenaMode = self.arenaMode
            if not self.arenaMode:
                if p and hasattr(p, 'reportClientException'):
                    msg = 'balanceArenaHover dont have arenaMode,current spaceNo:%s,%s' % (p.spaceNo, getattr(p, 'arenaModeCache', -1))
                    p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})
                return
            if self.mode == ARENA_MODE_RANK:
                p.arenaMode = arenaMode
                p.applyArena()
            elif self.mode == ARENA_MODE_SHUANGREN:
                p = BigWorld.player()
                if p.isInDoubleArenaState16():
                    p.cell.dArenaApplyEnterSixteenArena()
                else:
                    p.arenaMode = arenaMode
                    p.cell.dArenaApplyArena(arenaMode)
            elif self.mode == ARENA_MODE_SCORE_PLAYOFF:
                if p.isInArenaScoreStateJiFen():
                    p.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE
                    p.base.applyArenaOfFounder(const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE)
                elif p.isInArenaScoreStateWuDao():
                    msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_PLAYOFFS_JOIN_MSG)
                    self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.enterPlayoffsArena)
                elif p.getArenaScoreState() == gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT:
                    p.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE
                    p.base.applyArenaOfFounder(const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE)
            else:
                p.arenaMode = arenaMode
                p.applyArena()

    def onGroupStateChanged(self):
        if self.widget:
            self.refreshInfo()

    def getMathBtnLabel(self):
        p = BigWorld.player()
        if self.stage == ARENA_PANEL_STAGE_MATCHING or self.stage == ARENA_PANEL_STAGE_WAITING_TEAM:
            return gameStrings.BALANCE_ARENA_QUIT_MATCH
        if self.mode == ARENA_MODE_RANK:
            if p.isInTeam():
                return gameStrings.TEXT_BALANCEARENAHOVERPROXY_143
            else:
                return gameStrings.TEXT_BALANCEARENAHOVERPROXY_145
        else:
            if self.mode == ARENA_MODE_SHUANGREN or self.mode == ARENA_MODE_SCORE_PLAYOFF:
                return gameStrings.TEXT_BALANCEARENAHOVERPROXY_147
            return gameStrings.TEXT_BALANCEARENAHOVERPROXY_149

    def onChangeArenaMode(self, arenaMode):
        p = BigWorld.player()
        self.arenaMode = arenaMode
        if self.arenaMode in const.CROSS_DOUBLE_ARENA:
            self.mode = ARENA_MODE_SHUANGREN
        elif self.arenaMode in const.CROSS_BALANCE_ARENA_SCORE:
            self.mode = ARENA_MODE_SCORE_PLAYOFF
        else:
            self.mode = ARENA_MODE_RANK
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.stage = getattr(p, 'arenaStage', 1)
        self.widget.matchBtn.label = self.getMathBtnLabel()
