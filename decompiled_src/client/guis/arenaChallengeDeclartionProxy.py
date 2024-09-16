#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaChallengeDeclartionProxy.o
import BigWorld
import gametypes
import gameglobal
import utils
import uiConst
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import messageBoxProxy
from callbackHelper import Functor
from guis import uiUtils
from data import arena_mode_data as AMD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
APPLY_RESULT_FRAMENAME = ['yingzhan', 'rengsong']
APPLY_SOUND_ID = 40
ACCEPT_SOUND_ID = 41
REFUSE_SOUND_ID = 42
SOUND_LIST = [APPLY_SOUND_ID, ACCEPT_SOUND_ID, REFUSE_SOUND_ID]
SCROLL_TEXT_DELAY = 0.1
START_SCROLL_TEXT_DELAY = 4
RESTART_SCROLL_TEXT_DELAY = 2
SCROLL_TEXT_DELTA = 5

class ArenaChallengeDeclartionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaChallengeDeclartionProxy, self).__init__(uiAdapter)
        self.widget = None
        self.closeHandle = None
        self.scrollHandle = None
        self.msgList = []
        self.reset()
        self.pushMsgDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENACHALLENGE_DECLARTION, self.hide)

    def reset(self):
        self.afficheDict = {}
        self.closeHandle and BigWorld.cancelCallback(self.closeHandle)
        self.scrollHandle and BigWorld.cancelCallback(self.scrollHandle)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENACHALLENGE_DECLARTION:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENACHALLENGE_DECLARTION)

    def show(self, showType, data):
        gameglobal.rds.sound.playSound(SOUND_LIST[showType])
        self.showType = showType
        self.afficheDict.update(data)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENACHALLENGE_DECLARTION)
        else:
            self.initUI()

    def initUI(self):
        self.closeHandle and BigWorld.cancelCallback(self.closeHandle)
        self.refreshTextInfo()
        self.refreshTween()
        self.closeHandle = BigWorld.callback(DCD.data.get('declartionHoldTime', 20), self.autoClose)

    def refreshTextInfo(self):
        if not self.widget:
            return
        challengeMode = self.afficheDict.get('challengeMode')
        self.widget.mainMc.infoMc.declartionTitleText.text = DCD.data.get('arenaChallengeDeclartionTitle', '%s') % AMD.data.get(challengeMode, {}).get('modeName')
        self.widget.mainMc.infoMc.srcServerName.text = '(%s)' % utils.getServerName(self.afficheDict.get('srcHostId'))
        self.widget.mainMc.infoMc.srcRoleName.text = self.afficheDict.get('srcRoleName')
        self.widget.mainMc.infoMc.tgtServerName.text = '(%s)' % utils.getServerName(self.afficheDict.get('tgtHostId'))
        self.widget.mainMc.infoMc.tgtRoleName.text = self.afficheDict.get('tgtRoleName')
        self.widget.mainMc.infoMc.declartionText.text = self.afficheDict.get('msg')
        self.resetTextScroll()
        BigWorld.callback(START_SCROLL_TEXT_DELAY, self.textScroll)

    def resetTextScroll(self):
        scrollTf = self.widget.mainMc.infoMc.declartionText
        scrollTf.mouseWheelEnabled = False
        scrollTf.scrollH = 0

    def textScroll(self, delay = SCROLL_TEXT_DELAY):
        self.scrollHandle and BigWorld.cancelCallback(self.scrollHandle)
        if not self.widget:
            return
        scrollTf = self.widget.mainMc.infoMc.declartionText
        if scrollTf.scrollH + scrollTf.width >= scrollTf.textWidth:
            scrollTf.scrollH = 0
        else:
            scrollTf.scrollH += SCROLL_TEXT_DELTA
        isBeforeRestart = scrollTf.scrollH + scrollTf.width >= scrollTf.textWidth
        isAfterRestart = scrollTf.scrollH == 0
        if isBeforeRestart or isAfterRestart:
            delay = RESTART_SCROLL_TEXT_DELAY
        self.scrollHandle = BigWorld.callback(delay, self.textScroll)

    def refreshTween(self):
        if not self.widget:
            return
        if self.showType == uiConst.ARENA_CHALLENGE_DECLARTION_SHOW:
            self.widget.mainMc.stateMc.gotoAndStop('applyShow')
        else:
            self.widget.mainMc.stateMc.stateMc.gotoAndStop(APPLY_RESULT_FRAMENAME[self.showType])
            self.widget.mainMc.stateMc.gotoAndPlay('applyShow')

    def showAcceptChallengeMsgBox(self):
        p = BigWorld.player()
        if p.arenaChallengeStatus != gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY:
            return
        srcServerName = utils.getServerName(self.pushMsgDict.get('srcHostId'))
        srcRoleName = self.pushMsgDict.get('srcRoleName')
        modeName = AMD.data.get(self.pushMsgDict.get('challengeMode'), {}).get('title')
        title = gameStrings.ARENA_CHALLENGEMODE_ACCEPT_MSG_TITLE
        msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_CHAT_ACCEPT, '%s %s %s') % (srcServerName, srcRoleName, modeName)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.ARENA_CHALLENGEMODE_ACCEPT_MSG_ACCEPT, self.acceptChallenge), MBButton(gameStrings.ARENA_CHALLENGEMODE_ACCEPT_MSG_REFUSE, self.refuseChallenge)]
        self.uiAdapter.messageBox.show(True, title, msg, buttons, textAlign='left', forbidFastKey=True, needDissMissCallBack=False)

    def acceptChallenge(self):
        BigWorld.player().cell.acceptArenaChallenge()

    def refuseChallenge(self):
        BigWorld.player().cell.rejectArenaChallenge()

    def autoClose(self, *args):
        self.uiAdapter.setVisRecord(uiConst.WIDGET_ARENACHALLENGE_DECLARTION, False)
        self.hide()

    def addPushMsg(self, msgType, msgInfoDict = None):
        if msgInfoDict:
            self.pushMsgDict = msgInfoDict
        pushMsg = gameglobal.rds.ui.pushMessage
        if pushMsg.hasMsgType(msgType):
            return
        callBackDict = {'click': Functor(self.onClickPushMsg, msgType, msgInfoDict)}
        pushMsg.addPushMsg(msgType)
        pushMsg.setCallBack(msgType, callBackDict)
        self.msgList.append(msgType)

    def removeAllArenaMsg(self):
        pushMsg = gameglobal.rds.ui.pushMessage
        for msg in self.msgList:
            pushMsg.hasMsgType(msg) and pushMsg.removePushMsg(msg)

        self.msgList = []

    def onClickPushMsg(self, msgType, msgInfoDict):
        if msgType == uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_APPLY:
            self.showApplyMsgBox(msgInfoDict)
        elif msgType == uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ACCEPT:
            self.showAcceptMsgBox(msgInfoDict)
        elif msgType == uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_REFUSE:
            self.showRefuseMsgBox(msgInfoDict)
        elif msgType == uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ENTER:
            self.showEnterMsgBox()

    def showApplyMsgBox(self, msgInfoDict):
        srcServerName = utils.getServerName(msgInfoDict.get('srcHostId'))
        srcRoleName = msgInfoDict.get('srcRoleName')
        modeName = AMD.data.get(msgInfoDict.get('challengeMode'), {}).get('title')
        msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_PUSHMSG_APPLY, '%s %s %s') % (srcServerName, srcRoleName, modeName)
        title = DCD.data.get('arenaChallengePushMsgTitle')
        confirmText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CONFIRM
        cancelText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CANCEL
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(confirmText, Functor(self.seekToEnterArenaNpc)), MBButton(cancelText)]
        self.uiAdapter.messageBox.show(True, title, msg, buttons, forbidFastKey=True)

    def showAcceptMsgBox(self, msgInfoDict):
        tgtServerName = utils.getServerName(msgInfoDict.get('tgtHostId'))
        tgtRoleName = msgInfoDict.get('tgtRoleName')
        msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_PUSHMSG_ACCEPT, '%s %s') % (tgtServerName, tgtRoleName)
        title = DCD.data.get('arenaChallengePushMsgTitle')
        confirmText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CONFIRM
        cancelText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CANCEL
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(confirmText, Functor(self.seekToEnterArenaNpc)), MBButton(cancelText)]
        self.uiAdapter.messageBox.show(True, title, msg, buttons, forbidFastKey=True)

    def showRefuseMsgBox(self, msgInfoDict):
        tgtServerName = utils.getServerName(msgInfoDict.get('tgtHostId'))
        tgtRoleName = msgInfoDict.get('tgtRoleName')
        msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_PUSHMSG_REFUSE, '%s %s') % (tgtServerName, tgtRoleName)
        title = DCD.data.get('arenaChallengePushMsgTitle')
        self.uiAdapter.messageBox.showMsgBox(showTitle=title, msg=msg)

    def showEnterMsgBox(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_ENTER_NOTIFY)
        title = DCD.data.get('arenaChallengePushMsgTitle')
        confirmText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CONFIRM
        cancelText = gameStrings.ARENA_CHALLENGE_PUSHMSG_CANCEL
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(confirmText, Functor(self.seekToEnterArenaNpc)), MBButton(cancelText)]
        self.uiAdapter.messageBox.show(True, title, msg, buttons, forbidFastKey=True)

    def seekToEnterArenaNpc(self, *args):
        seekId = DCD.data.get('arenaChallengeSeekId')
        seekId and uiUtils.findPosWithAlert(seekId)

    def enterArena(self):
        p = BigWorld.player()
        if p.arenaChallengeStatus not in [gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC, gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY_SUCC]:
            p.cell.enterArenaChallenge()
            return
        modeMemberMax = int(AMD.data.get(self.pushMsgDict.get('challengeMode'), {}).get('modeName', '1v1')[0])
        memberCnt = max(len(p.members), 1)
        if memberCnt < modeMemberMax:
            msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_ENTER_WARNING, '%d') % modeMemberMax
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.enterArenaChallenge)
        else:
            p.cell.enterArenaChallenge()

    def showMsgInChat(self, info, extra):
        p = BigWorld.player()
        msgId = GMDD.data.ARENA_CHALLENGE_ACCEPT_INCHAT
        modeName = AMD.data.get(info.get('challengeMode'), {}).get('modeName')
        srcServerName = utils.getServerName(info.get('srcHostId'))
        srcRoleName = info.get('srcRoleName')
        tgtServerName = utils.getServerName(info.get('tgtHostId'))
        tgtRoleName = info.get('tgtRoleName')
        gbIdSrc = extra.get('srcGbId')
        gbIdTgt = extra.get('tgtGbId')
        p.showGameMsgEx(msgId, (tgtServerName,
         tgtRoleName,
         srcServerName,
         srcRoleName,
         modeName,
         (gbIdSrc, gbIdTgt)))
