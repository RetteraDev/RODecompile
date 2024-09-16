#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetPeakProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import utils
import gameglobal
import ui
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import duel_config_data as DCD

class ArenaPlayoffsBetPeakProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetPeakProxy, self).__init__(uiAdapter)
        self.widget = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.queryInfo()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        pass

    def queryInfo(self):
        p = BigWorld.player()
        version = self.uiAdapter.arenaPlayoffsBet.betFailedCashDict.get('version', 0)
        p.cell.queryArenaPlayoffsBetCalcInfo(version)

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            self.widget.removeAllInst(self.widget.mainMc.scrollWnd.canvas)
            rewardDescList = DCD.data.get('ARENA_PLAYOFFS_TOP_REWARD_DESC_LIST', ())
            posY = 0
            if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                keys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
            elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
                keys = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS
            else:
                keys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
            for lvKey in keys:
                itemMc = self.widget.getInstByClsName('ArenaPlayoffsBetPeak_BlockItem')
                if lvKey == gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE:
                    title = gameStrings.TEXT_ARENAPLAYOFFSBETPEAKPROXY_60
                else:
                    title = gameStrings.TEXT_ARENAPLAYOFFSBETPEAKPROXY_62 % lvKey.replace('_', '-')
                ASUtils.textFieldAutoSize(itemMc.title.textField, title)
                if lvKey == '1_59':
                    itemMc.title.helpIcon.visible = True
                    itemMc.title.helpIcon.helpKey = 303
                    itemMc.title.helpIcon.x = itemMc.title.textField.x + itemMc.title.textField.width + 5
                else:
                    itemMc.title.helpIcon.visible = False
                itemMc.title.bg.gotoAndStop('dark')
                for j in xrange(len(rewardDescList)):
                    contentMc = getattr(itemMc, 'content%d' % j, None)
                    if not contentMc:
                        continue
                    contentMc.rankName.text = rewardDescList[j][1]
                    contentMc.rewardIcon.bonusType = 'wudao'
                    betFailedCashDict = self.uiAdapter.arenaPlayoffsBet.betFailedCashDict
                    lastSeasonRestCash = betFailedCashDict.get('lastSeasonRestCashInfo', {}).get(lvKey, 0)
                    betFailedAccumulateCash = betFailedCashDict.get('betFailedAccumulateCashInfo', {}).get(lvKey, 0)
                    reward = utils.calcArenaPlayoffsTopRewardCash(lvKey, rewardDescList[j][0], lastSeasonRestCash, betFailedAccumulateCash)
                    ASUtils.textFieldAutoSize(contentMc.reward, format(reward, ','))
                    contentMc.arrowFlag.x = contentMc.reward.x + contentMc.reward.width
                    contentMc.bg.gotoAndStop('light' if j % 2 == 0 else 'dark')

                itemMc.y = posY
                posY += itemMc.height
                self.widget.mainMc.scrollWnd.canvas.addChild(itemMc)

            self.widget.mainMc.scrollWnd.refreshHeight()
            return
