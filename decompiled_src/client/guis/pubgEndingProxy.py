#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgEndingProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import keys
import gametypes
import const
import pubgUtils
import ui
import utils
from uiProxy import UIProxy
from item import Item
from guis import uiUtils
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
import clientUtils
from data import consumable_item_data as CID
from data import duel_config_data as DCD
MAX_TEAMMATE_NUMS = 5

class PubgEndingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgEndingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.serverResData = dict()
        self.curRankNums = 0
        self.allRankNums = 0
        self.curDanGrading = 0
        self.curDanGradingOffset = 0
        self.curWeekMaxRank = 0
        self.allBattleTime = 0
        self.allTeammateData = list()
        self.centerHintTxt = ''
        self.confirmBtnTimerCountDown = 30

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_ENDING_WIDGET:
            self.widget = widget
            self.initData()
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_ENDING_WIDGET)

    def initData(self):
        p = BigWorld.player()
        self.curRankNums = self.serverResData.get(pubgUtils.PUBG_ENDING_RANK_IDX, 0)
        self.allRankNums = self.serverResData.get(pubgUtils.PUBG_ENDING_ALL_RANK_IDX, 0)
        self.allBattleTime = utils.formatTimeStr(self.serverResData.get(pubgUtils.PUBG_ENDING_DURING_TIME_IDX, 0), formatStr='h:m:s', zeroShow=True, sNum=2, mNum=2, hNum=2)
        allTeammateDataDict = self.serverResData.get(pubgUtils.PUBG_ENDING_OTHERS_IDX, {})
        self.allTeammateData = allTeammateDataDict.values()
        self.curDanGrading = allTeammateDataDict.get(p.gbId, {}).get(pubgUtils.PUBG_ENDING_POINT_IDX, 0)
        self.curDanGradingOffset = allTeammateDataDict.get(p.gbId, {}).get(pubgUtils.PUBG_ENDING_DELTA_POINT_IDX, 0)
        self.curWeekMaxRank = allTeammateDataDict.get(p.gbId, {}).get(pubgUtils.PUBG_ENDING_WEEK_MAX_RANK_IDX, 0)
        self.centerHintTxt = DCD.data.get('pubgEndingCenterHintTxt', '')
        self.confirmBtnTimerCountDown = DCD.data.get('pubgEndingConfirmBtnTimerCountDown', 30)

    def initUI(self):
        if not self.widget:
            return
        self.initOwnDataUI()
        self.initAllTeammateDataUI()
        self.initComfirmBtnUI()

    def initOwnDataUI(self):
        if self.curRankNums <= 9:
            self.widget.myRankingMc.gotoAndStop('OneDigit')
        else:
            self.widget.myRankingMc.gotoAndStop('DoubleDigit')
        self.widget.firstPrizeEffect.visible = True if self.curRankNums == 1 else False
        self.widget.myRankingMc.curNums.text = self.curRankNums
        self.widget.myRankingMc.allNums.text = self.allRankNums
        if self.curDanGradingOffset >= 0:
            curDanGradingTxt = str(self.curDanGrading) + gameStrings.PUBG_ENDING_DAN_GRADING_ADD_TXT % self.curDanGradingOffset
        else:
            curDanGradingTxt = str(self.curDanGrading) + gameStrings.PUBG_ENDING_DAN_GRADING_REDUCE_TXT % abs(self.curDanGradingOffset)
        self.widget.curDanGrading.text.htmlText = curDanGradingTxt
        self.widget.curWeekMaxRank.text.htmlText = gameStrings.PUBG_ENDING_CUR_WEEK_MAX_RANKING % self.curWeekMaxRank
        self.widget.allBattleTime.text.text = self.allBattleTime
        self.widget.centerHintTxt.text.text = self.centerHintTxt
        self.widget.danGradingHelpIcon.helpKey = DCD.data.get('pubgDanGradingHelpKey', 0)

    def initAllTeammateDataUI(self):
        p = BigWorld.player()
        for idx in xrange(MAX_TEAMMATE_NUMS):
            teammateDataMc = getattr(self.widget, 'teammateData%d' % idx)
            if idx >= len(self.allTeammateData):
                teammateDataMc.visible = False
                continue
            else:
                teammateData = self.allTeammateData[idx]
                teammateDataMc.visible = True
                if teammateData[pubgUtils.PUBG_ENDING_GBID_IDX] == p.gbId:
                    teammateDataMc.gotoAndStop('mine')
                else:
                    teammateDataMc.gotoAndStop('others')
                teammateDataMc.playerName.text = str(teammateData[pubgUtils.PUBG_ENDING_ROLENAME_IDX])
                teammateDataMc.killAndAssist.text = '%d/%d' % (teammateData[pubgUtils.PUBG_ENDING_KILL_IDX], teammateData[pubgUtils.PUBG_ENDING_ASSIST_KILL_IDX])
                teammateDataMc.battleScore.text = str(teammateData[pubgUtils.PUBG_ENDING_BATTLE_SCORE_IDX])
                teammateDataMc.activeScore.text = str(teammateData[pubgUtils.PUBG_ENDING_ACTIVE_SCORE_IDX])
                teammateDataMc.award.text = str(teammateData[pubgUtils.PUBG_ENDING_AWARD_IDX])
                TipManager.addTip(teammateDataMc.awardIcon, DCD.data.get('pubgEndingUIAwardIconTip', ''))
                treasureBoxId = DCD.data.get('pubgTopRankItemId', {}).get(self.curRankNums, 0)
                if treasureBoxId:
                    teammateDataMc.treasureBoxSlot.visible = True
                    teammateDataMc.treasureBoxSlot.setItemSlotData(uiUtils.getGfxItemById(treasureBoxId))
                else:
                    teammateDataMc.treasureBoxSlot.visible = False

    def initComfirmBtnUI(self):
        self.updateConfirmBtnTimer()
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def handleConfirmBtnClick(self, *args):
        self.leavePUBG()

    def updateConfirmBtnTimer(self):
        p = BigWorld.player()
        if not self.widget:
            return
        self.confirmBtnTimerCountDown -= 1
        if p.isInPUBG():
            confirmBtnLabel = gameStrings.PUBG_ENDING_CONFIRM_BTN_LABEL
        else:
            confirmBtnLabel = gameStrings.PUBG_ENDING_CONFIRM_BTN_CLOSE_LABEL
        self.widget.confirmBtn.label = confirmBtnLabel % self.confirmBtnTimerCountDown
        if self.confirmBtnTimerCountDown > 0:
            self.updateTimeCB = BigWorld.callback(1, self.updateConfirmBtnTimer)
        else:
            self.leavePUBG()

    def leavePUBG(self):
        if self.widget:
            self.hide()
        p = BigWorld.player()
        if p.isInPUBG():
            p.leavePUBG(warningMsg=False, pubgEnding=True)

    def show(self, res):
        self.serverResData = res
        gameglobal.rds.ui.deadAndRelive.hide()
        gameglobal.rds.ui.fightObserve.closeActionBar()
        gameglobal.rds.ui.pubgAutoPick.hide()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_ENDING_WIDGET)
