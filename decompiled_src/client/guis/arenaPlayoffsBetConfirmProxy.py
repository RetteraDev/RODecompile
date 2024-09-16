#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetConfirmProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import events
import const
import gametypes
import copy
import gameglobal
from uiProxy import UIProxy
from asObject import ASObject
from data import duel_config_data as DCD
from data import arena_playoffs_bet_time_data as APBTD
from data import arena_playoffs_5v5_bet_time_data as AP5BTD

class ArenaPlayoffsBetConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.info = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_PLAYOFFS_BET_CONFIRM, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_BET_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_BET_CONFIRM)

    def show(self, info):
        self.info = info
        self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_BET_CONFIRM, isModal=True)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.costAmountIcon.bonusType = 'wudao'
        self.widget.diKouIcon.bonusType = 'wudao'
        self.widget.diKouInput.addEventListener(events.EVENT_CHANGE, self.handleInputChange, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        costAmount = self.info.get('costAmount', 0)
        self.widget.costAmount.text = format(costAmount, ',')
        lvKey = self.info.get('lvKey', '')
        betKey = (self.info.get('bType', 0), self.info.get('betId', 0))
        if self.info.get('isArena5v5', False):
            self.widget.content.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_60 % (lvKey.replace('_', '-'), AP5BTD.data.get(betKey, {}).get('descName', ''))
        elif self.info.get('isArenaScore', False):
            self.widget.content.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_63 % APBTD.data.get(betKey, {}).get('descName', '')
        else:
            self.widget.content.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_60 % (lvKey.replace('_', '-'), APBTD.data.get(betKey, {}).get('descName', ''))
        self.widget.hint.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_66
        junziDiKou = int(p.getFame(const.JUN_ZI_FAME_ID)) / DCD.data.get('ARENA_PLAYOFFS_CASH_2_JUNZI_NUM', 2)
        self.widget.diKouInput.maxNum = min(junziDiKou, costAmount)
        self.widget.diKouInput.text = '0'
        self.widget.diKou.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_71

    def handleInputChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.maxNum > 0:
            diKou = int(e.currentTarget.text) if itemMc.text != '' else 0
            diKou *= DCD.data.get('ARENA_PLAYOFFS_CASH_2_JUNZI_NUM', 2)
        else:
            diKou = 0
            self.widget.diKouInput.text = '0'
        self.widget.diKou.text = gameStrings.TEXT_ARENAPLAYOFFSBETCONFIRMPROXY_82 % format(diKou, ',')

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        lvKey = self.info.get('lvKey', '')
        bType = self.info.get('bType', 0)
        betId = self.info.get('betId', 0)
        multiple = self.info.get('multiple', 0)
        costAmount = self.info.get('costAmount', 0)
        cashCntWithJunzi = int(self.widget.diKouInput.text) if self.widget.diKouInput.text != '' else 0
        cash = costAmount - cashCntWithJunzi
        if bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL:
            team1NUIDs = self.info.get('team1NUIDs', [])
            team2NUIDs = self.info.get('team2NUIDs', [])
            scoreList1 = self.info.get('scoreList1', [])
            scoreList2 = self.info.get('scoreList2', [])
            p.cell.addArenaPlayoffsDuelBet(betId, lvKey, bType, cash, multiple, cashCntWithJunzi, team1NUIDs, team2NUIDs, scoreList1, scoreList2)
        elif bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL:
            teamNUIDs = copy.deepcopy(self.info.get('teamNUIDs', []))
            teamNUIDs.reverse()
            p.cell.addArenaPlayoffsFinalBet(betId, lvKey, bType, cash, multiple, cashCntWithJunzi, teamNUIDs)
        self.hide()
