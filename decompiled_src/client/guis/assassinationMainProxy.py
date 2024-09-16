#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationMainProxy.o
import BigWorld
import sMath
import gameglobal
import uiConst
import events
import gametypes
import const
import ui
import clientUtils
import utils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from assassination import Assassination
from assassination import AssassinationVal
import assassinationUtils as assUtils
from callbackHelper import Functor
from cdata import assassination_config_data as ACD
from cdata import game_msg_def_data as GMDD
ASSDATA_HAS_RECEIVE = 1
ASSDATA_CAN_RECEIVE = 2

class AssassinationMainProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ASSASSINATION_MAIN, self.hide)

    def reset(self):
        self.onlineCheckBoxData = False
        self.mineCheckBoxData = False
        self.todayIssueNums = 0
        self.todayReceiveNums = 0
        self.assassinationServerData = []
        self.assassinationListData = []
        self.assassinationDictData = {}
        self.issueLimitNums = 0
        self.receiveLimitNums = 0
        self.tipsMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_MAIN:
            self.widget = widget
            self.initData()
            self.initUI()
            self.requestGetAllData()
            self.refreshInfo(self.assassinationServerData)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_MAIN)

    def show(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_MAIN)

    def requestGetAllData(self):
        if self.widget:
            BigWorld.player().base.queryAssassination()

    def initData(self):
        self.issueLimitNums = ACD.data.get('assassinationOnBoardLimit', 59)
        self.receiveLimitNums = ACD.data.get('assassinationOffBoardLimit', 59)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.issueBtn.addEventListener(events.BUTTON_CLICK, self.handleIssueBtnClick, False, 0, True)
        self.widget.onlineCheckBox.selected = self.onlineCheckBoxData
        self.widget.onlineCheckBox.addEventListener(events.BUTTON_CLICK, self.handleOnlineCheckBoxClick, False, 0, True)
        self.widget.mineCheckBox.selected = self.mineCheckBoxData
        self.widget.mineCheckBox.addEventListener(events.BUTTON_CLICK, self.handleMineCheckBoxClick, False, 0, True)
        self.widget.helpInfoBtn.visible = True
        self.refreshHelpInfoPanel(open=True, refMc=self.widget.helpInfoBtn)
        self.widget.helpInfoBtn.addEventListener(events.BUTTON_CLICK, self.handleHelpInfoBtnClick, False, 0, True)
        self.initList()

    def initList(self):
        listMc = self.widget.assassinationList
        listMc.itemRenderer = 'AssassinationMain_AssassinationItem'
        listMc.lableFunction = self.assassinationListLabelFunction
        listMc.column = 4
        listMc.itemWidth = 178
        listMc.itemHeight = 247
        listMc.dataArray = self.assassinationListData
        listMc.validateNow()

    def handleRefreshBtnClick(self, *args):
        self.requestGetAllData()

    def handleIssueBtnClick(self, *args):
        self.showAssIssuePanel()

    def handleOnlineCheckBoxClick(self, *args):
        e = ASObject(args[3][0])
        self.onlineCheckBoxData = e.currentTarget.selected
        self.refreshList()

    def handleMineCheckBoxClick(self, *args):
        e = ASObject(args[3][0])
        self.mineCheckBoxData = e.currentTarget.selected
        self.refreshList()

    def handleHelpInfoBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.tipsMc:
            self.refreshHelpInfoPanel(open=True, refMc=e.currentTarget)
        else:
            self.refreshHelpInfoPanel(open=False, refMc=None)

    def handleHelpInfoClose(self, *args):
        self.refreshHelpInfoPanel(open=False, refMc=None)

    def assassinationListLabelFunction(self, *args):
        assGbIdAndFromGbId = ASObject(args[3][0])
        assMc = ASObject(args[3][1])
        realAssGbIdAndFromGbId = (long(assGbIdAndFromGbId[0]), long(assGbIdAndFromGbId[1]))
        assData = self.assassinationDictData.get(realAssGbIdAndFromGbId, None)
        if not assData:
            assMc.visible = False
            return
        else:
            assMc.data = assData
            assMc.portrait.headIcon.fitSize = True
            assMc.portrait.headIcon.dragable = False
            assMc.portrait.headIcon.loadImage('headIcon/%s.dds' % str(assData.school * 10 + assData.sex))
            assMc.lvMc.text = assData.lv
            assMc.onlineMc.visible = assData.isOn
            assMc.hideMc.visible = not assData.isOn
            if not assData.isOn:
                ASUtils.setMcEffect(assMc.portrait.headIcon, 'gray')
            else:
                ASUtils.setMcEffect(assMc.portrait.headIcon)
            assMc.moneyMc.text = assData.reward
            assMc.combatScoreMc.text = str(assData.score)[0] + '?' * (len(str(assData.score)) - 1)
            assMc.loseMc.htmlText = gameStrings.ASSASSINATION_FAIL_HINT % assData.lose
            assMc.leftTimeMc.htmlText = str(self.getOnffBoardLeftTimeByAssData(assData))
            assDataStatus = self.checkAssDataStatus(assData)
            if assDataStatus == ASSDATA_HAS_RECEIVE:
                assMc.btn.gotoAndStop('hasReceive')
            elif assDataStatus == ASSDATA_CAN_RECEIVE:
                if assData.fromGbId == BigWorld.player().gbId:
                    assMc.btn.gotoAndStop('changeMoney')
                    assMc.btn.changeMoney.gbIdAndFromGbId = realAssGbIdAndFromGbId
                    assMc.btn.changeMoney.addEventListener(events.BUTTON_CLICK, self.handleChangeMoneyBtn, False, 0, True)
                else:
                    assMc.btn.gotoAndStop('receive')
                    assMc.btn.receiveBtn.gbIdAndFromGbId = realAssGbIdAndFromGbId
                    assMc.btn.receiveBtn.addEventListener(events.BUTTON_CLICK, self.handleReceiveBtn, False, 0, True)
            gradeData = self.checkMoneyGrade(assData.reward)
            if gradeData:
                assMc.gradeMc.gotoAndStop('grade%d' % gradeData['level'])
            return

    def handleReceiveBtn(self, *args):
        receiveBtn = ASObject(args[3][0]).currentTarget
        assData = self.getAssDataByGbIdAndFromGbId(receiveBtn.gbIdAndFromGbId[0], receiveBtn.gbIdAndFromGbId[1])
        if not assData:
            return
        if self.checkReceive(assData):
            marginRatio = ACD.data.get('assassinationOffBoardCost', 0.2)
            money = assData.reward
            onLineText = gameStrings.PLAYER_STATE_MPA[1] if assData.isOn else gameStrings.PLAYER_STATE_MPA[0]
            msg = gameStrings.ASSASSINATION_RECEIVE_SECOND_CONFIRM % (onLineText, int(marginRatio * 100), int(money * marginRatio))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.confirmReceive, assData.gbId, assData.fromGbId))

    def handleChangeMoneyBtn(self, *args):
        receiveBtn = ASObject(args[3][0]).currentTarget
        assData = self.getAssDataByGbIdAndFromGbId(receiveBtn.gbIdAndFromGbId[0], receiveBtn.gbIdAndFromGbId[1])
        if not assData:
            return
        gbId = long(assData.gbId)
        money = int(assData.reward)
        moneyUpperLimit = ACD.data.get('rewardUpperLimit', 0)
        msg = gameStrings.ASSASSINATION_CHANGE_MONEY_CONFIRM % ACD.data.get('assassinationAddRewardLimitNums', 1)
        gameglobal.rds.ui.messageBox.showYesNoInput(msg=msg, yesCallback=Functor(self.confirmChangeMoney, gbId, money), inputMax=moneyUpperLimit, style=uiConst.MSG_BOX_INPUT_INT, defaultInput=money)

    def confirmReceive(self, gbId, fromGbId):
        if self.checkSecondReceive(long(gbId)):
            BigWorld.player().base.putAssassinationOffBoard(long(gbId), long(fromGbId))

    def confirmChangeMoney(self, gbId, lastMoney, inputStr):
        curChangeMoney = int(inputStr)
        if self.checkChangeMoney(lastMoney, curChangeMoney):
            moneyOffset = curChangeMoney - lastMoney
            if moneyOffset >= 0:
                BigWorld.player().base.addRewardOnBoard(gbId, moneyOffset)

    def refreshInfo(self, assDataList):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            return
        self.refreshData(assDataList)
        self.refreshUI()

    def refreshData(self, assDataList):
        p = BigWorld.player()
        myAssOnBoardData = getattr(p, 'myAssOnBoardData', {})
        myAssExtraData = getattr(p, 'myAssExtraData', {})
        self.todayIssueNums = len(myAssOnBoardData)
        self.todayReceiveNums = myAssExtraData.get(assUtils.EXTRA_OFF_CNT, 0)
        if not assDataList:
            return
        self.assassinationServerData = assDataList
        del self.assassinationListData[:]
        self.assassinationDictData.clear()
        for assData in assDataList:
            assVal = AssassinationVal().fromDTO(assData)
            gbIdAndFromGbId = (assVal.gbId, assVal.fromGbId)
            self.assassinationDictData[gbIdAndFromGbId] = assVal
            self.assassinationListData.append(gbIdAndFromGbId)

    def refreshUI(self):
        self.widget.todayIssueHint.text = gameStrings.ASSASSINATION_ISSUE_HINT % (self.todayIssueNums, self.issueLimitNums)
        self.widget.todayReceiveHint.text = gameStrings.ASSASSINATION_RECEIVE_HINT % (self.todayReceiveNums, self.receiveLimitNums)
        self.refreshList()

    def refreshList(self):
        realAssListData = self.assassinationListData
        if self.mineCheckBoxData:
            realAssListData = self.filterMineData(realAssListData)
        if self.onlineCheckBoxData:
            realAssListData = self.filterOnlineData(realAssListData)
        self.widget.assassinationList.dataArray = realAssListData
        self.widget.assassinationList.validateNow()

    def refreshHelpInfoPanel(self, open = False, refMc = None):
        if open:
            playRecommActId = ACD.data.get('assassinationPlayRecommActivityId', 0)
            if playRecommActId:
                tipData = gameglobal.rds.ui.playRecomm.getPlayTipData(playRecommId=playRecommActId, seekId='', prid=0)
                if self.tipsMc == None:
                    self.tipsMc = self.widget.getInstByClsName('Activity_Tip_TipMc')
                    ASUtils.setHitTestDisable(self.tipsMc, False)
                self.tipsMc.visible = True
                self.tipsMc.tipData = tipData
                self.tipsMc.model = None
                self.tipsMc.refMc = refMc
                self.tipsMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleHelpInfoClose, False, 0, True)
                self.widget.addChild(self.tipsMc)
                self.tipsMc.x = int(self.widget.closeBtn.x + 50)
                self.tipsMc.y = int(self.widget.closeBtn.y)
        elif self.tipsMc:
            self.tipsMc.refMc = None
            self.widget.removeToCache(self.tipsMc)
            self.tipsMc = None

    def checkIssue(self):
        p = BigWorld.player()
        lvLimit = ACD.data.get('assassinationLvLimit', 59)
        if p.lv < lvLimit:
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_LV_LIMIT, ())
            return False
        return True

    def checkReceive(self, assData):
        p = BigWorld.player()
        lvLimit = ACD.data.get('assassinationLvLimit', 59)
        if p.lv < lvLimit:
            p.showGameMsg(GMDD.data.ASSASSINATION_RECEIVE_LV_LIMIT, ())
            return False
        if assData.fromGbId == p.gbId:
            p.showGameMsg(GMDD.data.ASSASSINATION_RECEIVE_MINE_ISSUE_LIMIT, ())
            return False
        return True

    def checkSecondReceive(self, gbId):
        p = BigWorld.player()
        if gbId == p.gbId:
            p.showGameMsg(GMDD.data.ASSASSINATION_RECEIVE_MINE_LIMIT, ())
            return False
        return True

    def checkAssDataStatus(self, assData):
        if long(assData.toGbId) != 0 and utils.getNow() - assData.tOff <= ACD.data.get('assassinationToffInterval', 14400):
            return ASSDATA_HAS_RECEIVE
        else:
            return ASSDATA_CAN_RECEIVE

    def checkChangeMoney(self, lastMoney, curMoney):
        p = BigWorld.player()
        moneyAddLimit = ACD.data.get('assassinationAddRewardLimitNums', 1)
        moneyUpperLimit = ACD.data.get('rewardUpperLimit', 0)
        moneyLowerLimit = lastMoney
        if not moneyLowerLimit <= curMoney:
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_MONEY_CHANGE, ())
            return False
        if not curMoney <= moneyUpperLimit:
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_MONEY_ERROR, (moneyUpperLimit, moneyLowerLimit))
            return False
        if curMoney - lastMoney < moneyAddLimit:
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_CHANGE_MONEY_ADD_LIMIT_ERROR, (moneyAddLimit,))
            return False
        return True

    def checkMoneyGrade(self, money):
        moneyGradeList = ACD.data.get('assassinationAnonymityCostGradeList', [])
        for gradeData in moneyGradeList:
            if gradeData['low'] <= money <= gradeData['up']:
                return gradeData

    def filterOnlineData(self, assassinationListData):
        assOnlineListData = []
        for gbIdAndFromGbId in assassinationListData:
            if self.assassinationDictData[gbIdAndFromGbId].isOn:
                assOnlineListData.append(gbIdAndFromGbId)

        return assOnlineListData

    def filterMineData(self, assassinationListData):
        assassMineListData = []
        for gbIdAndFromGbId in assassinationListData:
            if self.assassinationDictData[gbIdAndFromGbId].fromGbId == BigWorld.player().gbId:
                assassMineListData.append(gbIdAndFromGbId)

        return assassMineListData

    def getAssDataByGbIdAndFromGbId(self, gbId, fromGbId):
        realGbIdAndFromGbId = (long(gbId), long(fromGbId))
        assData = self.assassinationDictData.get(realGbIdAndFromGbId, None)
        return assData

    def getOnffBoardLeftTimeByAssData(self, assData):
        curINtervalTime = utils.getNow() - long(assData.tOn)
        intervalLimitTime = ACD.data.get('assassinationTonInterval', const.TIME_INTERVAL_DAY)
        leftTime = sMath.clamp(intervalLimitTime - curINtervalTime, 0, intervalLimitTime)
        return utils.formatTimeStr(leftTime, gameStrings.ASSASSINATION_LEFT_TIME_HINT, True)

    def showAssIssuePanel(self):
        if self.checkIssue():
            gameglobal.rds.ui.assassinationIssue.show()

    def showAssIssuePanelByGbID(self, gbId):
        p = BigWorld.player()
        if gbId:
            p.base.searchAssassinationTarget(gbId)
        gameglobal.rds.ui.assassinationMain.showAssIssuePanel()
