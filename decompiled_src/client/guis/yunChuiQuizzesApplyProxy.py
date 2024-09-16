#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yunChuiQuizzesApplyProxy.o
import BigWorld
import uiConst
import events
import gameglobal
import utils
import clientUtils
import gamelog
import gametypes
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import quizzes_config_data as QCD
ACT_TYPE_NORMAL = 1
ACT_TYPE_FISH = 2

class YunChuiQuizzesApplyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YunChuiQuizzesApplyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.activityState = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YUNCHUI_QUIZZES_APPLY, self.hide)

    def reset(self):
        self.widget = None
        self.isJoined = False
        self.joinedNum = 1000
        self.curActivityId = 0
        self.timer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YUNCHUI_QUIZZES_APPLY:
            self.widget = widget
            self.delTimer()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.delTimer()
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES_APPLY)

    def setInfo(self, isJoined, joinedNum, activityId):
        self.isJoined = isJoined
        self.joinedNum = joinedNum
        self.curActivityId = activityId
        self.refreshInfo()

    def setActivityState(self, activityState):
        self.activityState = activityState

    def show(self):
        p = BigWorld.player()
        if not self.curActivityId or self.activityState != gametypes.QUIZZES_ACTIVITY_STAGE_OPEN:
            p.showGameMsg(GMDD.data.QUIZZES_SIGNUP_NOT_START, ())
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES_APPLY)
        else:
            self.initUI()
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        data = QCD.data.get(self.curActivityId, {})
        title = gameStrings.YUNCHUI_QUIZZES_APPLY_TITLE % data.get('title', '')
        self.widget.title.textField.text = title

    def refreshInfo(self):
        if not self.widget:
            return
        if self.isJoined:
            self.widget.confirmBtn.disabled = True
            self.widget.confirmBtn.label = gameStrings.YUNCHUI_QUIZZES_APPLYED
        else:
            self.widget.confirmBtn.disabled = False
            self.widget.confirmBtn.label = gameStrings.YUNCHUI_QUIZZES_APPLY
        data = QCD.data.get(self.curActivityId, {})
        beginTime = data.get('beginDate')
        intervalJoin = data.get('intervalJoin')
        intervalStart = data.get('intervalStart')
        beginTimeTxt = utils.formatTimeEx(utils.getDisposableCronTabTimeStamp(beginTime) + intervalJoin + intervalStart)[0:5]
        self.widget.time.text = beginTimeTxt
        self.widget.problemNum.text = data.get('questionNum', 12)
        shareReward = data.get('shareReward')
        rewardType = shareReward[0]
        rewardNum = shareReward[1]
        self.widget.moneyDesc.visible = bool(rewardNum)
        self.widget.icon.visible = bool(rewardNum)
        self.widget.count.visible = bool(rewardNum)
        if rewardNum:
            self.widget.moneyDesc.text = data.get('shareRewardTitle')
            if rewardType == SCD.data.get('quizzesRewardBindCoin', 1):
                bonusType = 'tianBi'
            elif rewardType == SCD.data.get('quizzesRewardCash', 2):
                bonusType = 'cash'
            elif rewardType == SCD.data.get('quizzesRewardBindCash', 3):
                bonusType = 'bindCash'
            elif rewardType == SCD.data.get('quizzesRewardFame', 4):
                bonusType = 'yunChui'
            self.widget.icon.bonusType = bonusType
            self.widget.count.text = rewardNum
        fixedBonus = data.get('fixedBonus')
        fixedItemBonus = clientUtils.genItemBonus(fixedBonus)
        fixedBonusId = fixedItemBonus[0][0]
        fixedBonusCount = fixedItemBonus[0][1]
        itemMc = self.widget.item0
        itemMc.dragable = False
        itemMc.itemId = fixedBonusId
        itemMc.setItemSlotData(uiUtils.getGfxItemById(fixedBonusId, fixedBonusCount))

    def refreshJoinedNum(self):
        if self.widget:
            self.widget.joinedNum.text = self.joinedNum

    def handleConfirmBtnClick(self, *args):
        BigWorld.player().base.joinQuizzes()

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(5, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        BigWorld.player().base.queryQuizzesJoinedNum()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def pushApplyMessage(self):
        if uiConst.MESSAGE_TYPE_QUIZZES_APPLY not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_QUIZZES_APPLY)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_QUIZZES_APPLY, {'click': self.onPushMsgClick})

    def removeApplyPushMsg(self):
        if uiConst.MESSAGE_TYPE_QUIZZES_APPLY in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_QUIZZES_APPLY)

    def onPushMsgClick(self):
        if not self.widget:
            BigWorld.player().base.queryQuizzesJoinedInfo()
        self.removeApplyPushMsg()

    def isFishQuizzes(self):
        data = QCD.data.get(self.curActivityId, {})
        actType = data.get('actType', 1)
        return actType == ACT_TYPE_FISH
