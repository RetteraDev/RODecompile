#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamSSCMsgBoxProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import const
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import duel_config_data as DCD
from data import sheng_si_chang_data as SSCD
from data import sys_config_data as SCD
CONFIRM_ENTER = 0
ROUND_WIN = 1
FINAL_WIN = 2
INVITE_APPLY = 3
SHOWTYPE_CLASSNAME = ['TeamSSCMsgBox_ConfirmEnter',
 'TeamSSCMsgBox_RoundWin',
 'TeamSSCMsgBox_FinalWin',
 'TeamSSCMsgBox_InviteApply']
CONTENT_POS = [[30, 62],
 [40, 72],
 [43, 62],
 [39, 72]]
BUTTON_NORMAL_POS_X = 24
BUTTON_CENTER_POS_X = 72

class TeamSSCMsgBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamSSCMsgBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handler = None
        self.clickCancelOrMinimize = False
        self.reset()

    def reset(self):
        self.showType = CONFIRM_ENTER
        self.msgBoxData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TEAM_SSC_MSGBOX:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TEAM_SSC_MSGBOX)
        self.handler and BigWorld.cancelCallback(self.handler)
        self.handler = None

    def show(self, showType):
        self.showType = showType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TEAM_SSC_MSGBOX)
        else:
            self.removeContent()
            self.initUI()

    def removeContent(self):
        if not self.widget:
            return
        self.widget.removeChild(self.content)

    def initUI(self):
        self.initContent()
        self.widget.addChild(self.content)
        self.refreshCountDown()

    def refreshInfo(self):
        if not self.widget:
            return

    def initContent(self):
        msgData = self.getMsgData()
        self.content = self.widget.getInstByClsName(SHOWTYPE_CLASSNAME[self.showType])
        self.content.desc.htmlText = msgData.get('text')
        self.content.loading.maxValue = msgData.get('totalTime', 45)
        self.content.loading.currrentValue = self.content.loading.maxValue
        self.content.x = CONTENT_POS[self.showType][0]
        self.content.y = CONTENT_POS[self.showType][1]
        self.initConfirmEnterWndBtn(self.content)
        self.initLeaveWndBtn(self.content)
        self.initInviteApplyWndBtn(self.content)

    def initConfirmEnterWndBtn(self, content):
        msgData = self.getMsgData()
        okBtn = content.okBtn
        if okBtn:
            okBtn.visible = not msgData.get('isConfirmed', False)
            okBtn.addEventListener(events.BUTTON_CLICK, self.handleOkBtnClick, False, 0, True)
            okBtn.x = BUTTON_NORMAL_POS_X
        cancelBtn = content.cancelBtn
        if cancelBtn:
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
                cancelBtn.visible = not msgData.get('isConfirmed', False) and msgData.get('isFirst', False)
                if okBtn and okBtn.visible and not cancelBtn.visible:
                    okBtn.x = BUTTON_CENTER_POS_X
            else:
                cancelBtn.visible = not msgData.get('isConfirmed', False)
            cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def initLeaveWndBtn(self, content):
        leaveBtn = content.leaveBtn
        leaveBtn and leaveBtn.addEventListener(events.BUTTON_CLICK, self.handleLeaveBtnClick, False, 0, True)

    def initInviteApplyWndBtn(self, content):
        acceptBtn = content.acceptBtn
        acceptBtn and acceptBtn.addEventListener(events.BUTTON_CLICK, self.handleAcceptBtnClick, False, 0, True)
        refuseBtn = content.refuseBtn
        refuseBtn and refuseBtn.addEventListener(events.BUTTON_CLICK, self.handleRefuseBtnClick, False, 0, True)

    def handleOkBtnClick(self, *args):
        BigWorld.player().cell.confirmEnterTeamShengSiChang()

    def handleCancelBtnClick(self, *args):
        p = BigWorld.player()
        p.cell.cancelEnterTeamShengSiChang()
        p.showGameMsg(GMDD.data.TEAM_SSC_CANCEL_ENTER, ())
        self.removeConfirmMsg()
        self.hide()
        self.clickCancelOrMinimize = True

    def handleLeaveBtnClick(self, *args):
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            p.cell.leaveTeamShengSiChang()
        self.removeLeaveMsg()
        self.hide()

    def handleAcceptBtnClick(self, *args):
        p = BigWorld.player()
        if hasattr(p, 'headerGbId'):
            p.cell.acceptInvitedTeamSSC(p.headerGbId)
        self.removeInviteApplyMsg()
        self.hide()

    def handleRefuseBtnClick(self, *args):
        p = BigWorld.player()
        if hasattr(p, 'headerGbId'):
            p.cell.rejectInvitedTeamSSC(p.headerGbId)
        self.removeInviteApplyMsg()
        self.hide()

    def _onMiniBtnClick(self, e):
        self.hide()
        self.clickCancelOrMinimize = True

    def refreshCountDown(self):
        self.handler and BigWorld.cancelCallback(self.handler)
        remainTime = self.getRemainTime()
        self.content.loading.currentValue = max(remainTime, 0)
        if remainTime < 0:
            self.handleOkBtnClick()
            return
        self.handler = BigWorld.callback(0.5, self.refreshCountDown)

    def getRemainTime(self):
        now = utils.getNow()
        msgData = self.getMsgData()
        totalTime = msgData.get('totalTime', 45)
        startTime = msgData.get('startTime', now)
        return int(totalTime - (now - startTime))

    def confirmEnterTimeout(self, msgData = None):
        if self.isConfirmed():
            self.hide()
            self.removeConfirmMsg()
            self.showCreateDelayNotify()
        else:
            self.handleOkBtnClick()
            self.hide()
            self.removeConfirmMsg()

    def leaveTimeout(self, msgData = None):
        self.handleLeaveBtnClick()
        self.removeLeaveMsg()
        self.hide()

    def isConfirmed(self):
        msgData = self.getMsgData()
        return msgData.get('isConfirmed', False)

    def inviteApplyTimeout(self, msgData = None):
        self.handleRefuseBtnClick()

    def showCreateDelayNotify(self):
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_DELAY_NOTIFY, 'delay notify')
        gameglobal.rds.ui.messageBox.showAlertBox(msg)

    def getMsgData(self):
        if self.showType == CONFIRM_ENTER:
            return gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_TEAM_SSC_START)
        elif self.showType == ROUND_WIN:
            return gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_TEAM_SSC_ROUND_WIN)
        elif self.showType == INVITE_APPLY:
            return gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_TEAM_SSC_INVITE_APPLY)
        else:
            return {}

    def confirmEnterSucc(self):
        msgData = self.getMsgData()
        msgData['text'] = DCD.data.get('teamSSCConfirmedText', 'confirmed')
        msgData['isConfirmed'] = True
        if not self.widget:
            return
        if self.showType != CONFIRM_ENTER:
            return
        self.content.desc.text = msgData['text']
        self.content.okBtn.visible = False
        self.content.cancelBtn.visible = False

    def onEnterTeamSSC(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_START)
        self.hide()

    def onLeaveTeamSSC(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_ROUND_WIN)
        if gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_TEAM_SSC_START):
            self.show(CONFIRM_ENTER)
        else:
            self.hide()

    def showConfirmMsg(self, isFirst):
        p = BigWorld.player()
        text = DCD.data.get('teamSSCFirstConfirmEnterText', 'team ssc first open') if isFirst else DCD.data.get('teamSSCConfirmEnterText', 'team ssc open')
        if isFirst:
            totalTime = const.DUEL_PREPARE_DELAY
        else:
            quitTime = SSCD.data.get(BigWorld.player().getShengSiChangFbNo(), {}).get('quitTime', 30)
            roundIntervalTime = SSCD.data.get(const.FB_NO_TEAM_SHENG_SI_CHANG, {}).get('nextRoundPrepareTime', 120)
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False):
                totalTime = roundIntervalTime
            else:
                totalTime = quitTime + roundIntervalTime - 10
        msgData = {'totalTime': totalTime,
         'startTime': utils.getNow(),
         'text': text,
         'isFirst': isFirst}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_START, msgData)
        if not BigWorld.player().inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            self.clickConfirmMsg()
        self.clickCancelOrMinimize = False

    def showRoundWinMsg(self, isFinalMatch):
        if not isFinalMatch:
            text = DCD.data.get('teamSSCRoundWinText', 'win leave')
        else:
            text = DCD.data.get('teamSSCFinalWinText', 'win final leave')
        quitTime = SSCD.data.get(BigWorld.player().getShengSiChangFbNo(), {}).get('quitTime', 30)
        msgData = {'totalTime': quitTime,
         'startTime': utils.getNow(),
         'text': text}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_ROUND_WIN, msgData)
        if BigWorld.player().inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            self.clickRoundWinMsg()

    def showInviteApplyMsg(self, inviterName):
        totalTime = SCD.data.get('TEAM_SHENG_SI_CHANG_INVITE_CONFIRM_TIME', 30)
        text = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_INVITE_NOTIFY, '%s invite you') % inviterName
        msgData = {'totalTime': totalTime,
         'startTime': utils.getNow(),
         'text': text}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_INVITE_APPLY, msgData)
        self.clickInviteApplyMsg()

    def clickConfirmMsg(self):
        self.show(CONFIRM_ENTER)

    def clickRoundWinMsg(self):
        self.show(ROUND_WIN)

    def clickInviteApplyMsg(self):
        self.show(INVITE_APPLY)

    def removeConfirmMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_START)

    def removeLeaveMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_ROUND_WIN)

    def removeInviteApplyMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TEAM_SSC_INVITE_APPLY)

    def checkEnterWndShow(self, isFirst):
        if self.widget:
            return
        if self.clickCancelOrMinimize:
            return
        p = BigWorld.player()
        if not p:
            return
        if p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            return
        if gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_TEAM_SSC_START):
            self.clickConfirmMsg()
        else:
            msg = DCD.data.get('teamSSCFirstConfirmEnterText', 'team ssc first open') if isFirst else DCD.data.get('teamSSCConfirmEnterText', 'team ssc open')
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and not isFirst:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.handleOkBtnClick, canEsc=False)
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.handleOkBtnClick, noCallback=self.handleCancelBtnClick, canEsc=False)
