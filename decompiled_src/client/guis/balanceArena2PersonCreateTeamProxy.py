#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonCreateTeamProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
from guis import events
from uiProxy import UIProxy
from data import duel_config_data as DCD
from guis.asObject import ASUtils
from cdata import game_msg_def_data as GMDD
from helpers import taboo

class BalanceArena2PersonCreateTeamProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonCreateTeamProxy, self).__init__(uiAdapter)
        self.widget = None
        self.recommendCamp = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_2PERSON_CREATE, self.hide)

    def reset(self):
        self.currentZhenYing = -1
        self.teamName = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_2PERSON_CREATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_CREATE)

    def show(self, recommendCamp = 0):
        if not self.widget:
            self.recommendCamp = recommendCamp
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_CREATE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.teamNameInput.maxChars = 8
        self.widget.createBtn.addEventListener(events.BUTTON_CLICK, self.onCreateBtnClick, False, 0, True)
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        zhenYingList = []
        for i in zhenyingInfos:
            zhenYingList.append({'label': zhenyingInfos.get(i).get('name', '')})

        ASUtils.setDropdownMenuData(self.widget.zhenyingDropMenu, zhenYingList)
        self.widget.zhenyingDropMenu.selectedIndex = self.recommendCamp - 1

    def onCreateBtnClick(self, *args):
        self.currentZhenYing = self.widget.zhenyingDropMenu.selectedIndex + 1
        self.teamName = self.widget.teamNameInput.text
        p = BigWorld.player()
        if not self.teamName:
            p.showGameMsg(GMDD.data.DOUBLEARENA_TEAMNAME_EMPTY, ())
            return
        retval, _ = taboo.checkNameDisWord(self.teamName)
        if not retval:
            p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_TEAM_NAME_INVALID, ())
            return
        if self.currentZhenYing <= 0:
            p.showGameMsg(GMDD.data.DOUBLEARENA_ZHENYING_NOT_CHOOSE, ())
            return
        gamelog.debug('dxk@balanceArena2PersonCreateTEamProxy create DoubleArena Team', self.currentZhenYing, self.teamName)
        p.cell.dArenaApplyTeam(self.teamName, self.currentZhenYing)
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
