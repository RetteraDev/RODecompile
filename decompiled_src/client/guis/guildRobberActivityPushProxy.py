#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRobberActivityPushProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import uiUtils
import utils
import logicInfo
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from callbackHelper import Functor
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
ROBBER_STATE_NO = 0
ROBBER_STATE_OPEN = 1
ROBBER_STATE_END = 2

class GuildRobberActivityPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRobberActivityPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.state = ROBBER_STATE_NO
        self.beginTime = 0
        self.endTime = 0
        self.allRobbers = 0
        self.killedRobbers = 0
        self.useTime = 0
        self.addEvent(events.EVENT_ENTER_GUILD_SPACE, self.show, isGlobal=True)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_ROBBER_ACTIVITY_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_ROBBER_ACTIVITY_PUSH)

    def clearAll(self):
        self.state = ROBBER_STATE_NO
        self.beginTime = 0
        self.endTime = 0
        self.allRobbers = 0
        self.killedRobbers = 0
        self.useTime = 0

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildRobber', False):
            return
        if self.widget:
            self.refreshInfo()
        elif self.state in (ROBBER_STATE_OPEN, ROBBER_STATE_END):
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_ROBBER_ACTIVITY_PUSH)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget.hintEff, True)
        self.widget.pushIcon.expandBtn.addEventListener(events.MOUSE_CLICK, self.onClickExpandTip, False, 0, True)
        self.widget.pushIcon.tipsText.textMc.closeBtn.addEventListener(events.MOUSE_CLICK, self.onClickCloseTip, False, 0, True)
        self.widget.pushIcon.openIcon.addEventListener(events.MOUSE_CLICK, self.onClickPushIcon, False, 0, True)
        self.widget.pushIcon.endIcon.addEventListener(events.MOUSE_CLICK, self.onClickPushIcon, False, 0, True)
        TipManager.addTip(self.widget.pushIcon.countdown, gameStrings.TEXT_GUILDROBBERACTIVITYPUSHPROXY_83)

    def onClickExpandTip(self, *args):
        self.widget.pushIcon.expandBtn.visible = False
        self.widget.pushIcon.tipsText.gotoAndPlay('on')

    def onClickCloseTip(self, *args):
        self.widget.pushIcon.expandBtn.visible = True
        self.widget.pushIcon.tipsText.gotoAndPlay('off')

    def onClickPushIcon(self, *args):
        self.widget.hintEff.visible = False
        self.widget.hintEff.gotoAndStop(1)
        p = BigWorld.player()
        if self.state == ROBBER_STATE_OPEN:
            p.showGameMsg(GMDD.data.GUILD_ROBBER_OPEN_PLAYER_IN_GUILD_SPACE, ())
        elif self.state == ROBBER_STATE_END:
            p.showGameMsg(GMDD.data.GUILD_ROBBER_END_PLAYER_IN_GUILD_SPACE, ())

    def refreshInfo(self):
        if not self.widget:
            return
        if self.state == ROBBER_STATE_NO:
            self.hide()
            return
        if self.state == ROBBER_STATE_OPEN:
            self.widget.pushIcon.openIcon.visible = True
            self.widget.pushIcon.endIcon.visible = False
            self.widget.pushIcon.tipsText.textMc.mainLeft.htmlText = gameStrings.TEXT_GUILDROBBERACTIVITYPUSHPROXY_114 % self.allRobbers
            self.widget.pushIcon.tipsText.textMc.mainRight.htmlText = gameStrings.TEXT_GUILDROBBERACTIVITYPUSHPROXY_115 % (self.killedRobbers, self.allRobbers - self.killedRobbers)
            self.widget.pushIcon.tipsText.textMc.desc.htmlText = uiUtils.toHtml(gameStrings.GUILD_ROBBER_ACTIVITY_PUSH_OPEN, color='#E53900')
        elif self.state == ROBBER_STATE_END:
            self.widget.pushIcon.openIcon.visible = False
            self.widget.pushIcon.endIcon.visible = True
            self.widget.pushIcon.tipsText.textMc.mainLeft.htmlText = gameStrings.TEXT_GUILDROBBERACTIVITYPUSHPROXY_122
            self.widget.pushIcon.tipsText.textMc.mainRight.htmlText = gameStrings.TEXT_GUILDROBBERACTIVITYPUSHPROXY_123 % utils.formatTimeStr(self.useTime, formatStr='h:m:s', zeroShow=True, sNum=2, mNum=2)
            self.widget.pushIcon.tipsText.textMc.desc.htmlText = uiUtils.toHtml(gameStrings.GUILD_ROBBER_ACTIVITY_PUSH_END, color='#73E539')
        self.widget.hintEff.visible = True
        self.widget.hintEff.gotoAndPlay(1)
        self.widget.pushIcon.expandBtn.visible = False
        self.widget.pushIcon.tipsText.gotoAndPlay('on')
        self.stopTimer()
        self.updateTime()

    def updateTime(self):
        if not self.widget:
            return
        if self.state != ROBBER_STATE_OPEN:
            leftTime = 0
        else:
            leftTime = max(self.endTime - utils.getNow(), 0)
        self.widget.pushIcon.countdown.textField.text = utils.formatTimeStr(leftTime, formatStr='h:m:s', zeroShow=True, sNum=2, mNum=2)
        if leftTime > 0:
            self.timer = BigWorld.callback(1, self.updateTime)

    def activityOpen(self, beginTime, endTime, allRobbers, killedRobbers):
        self.state = ROBBER_STATE_OPEN
        self.beginTime = beginTime
        self.endTime = endTime
        self.allRobbers = allRobbers
        self.killedRobbers = killedRobbers
        if BigWorld.player().inGuildSpace():
            self.show()
        else:
            self.addActivityOpenPush()

    def updateInfo(self, allRobbers, killedRobbers):
        self.allRobbers = allRobbers
        self.killedRobbers = killedRobbers
        self.refreshInfo()

    def activityEnd(self, result, useTime):
        if result:
            self.state = ROBBER_STATE_END
            self.useTime = useTime
            BigWorld.player().showGameMsg(GMDD.data.GUILD_ROBBER_END_PLAYER_IN_GUILD_SPACE, ())
            if BigWorld.player().inGuildSpace():
                self.show()
            else:
                self.addActivityEndPush()
        else:
            self.hide()

    def updateBoxStatus(self, boxStatus):
        if boxStatus in (gametypes.GUILD_ROBBER_BIG_BOX_OPENED, gametypes.GUILD_ROBBER_BIG_BOX_OVERDUE):
            self.state = ROBBER_STATE_NO
            self.refreshInfo()

    def addActivityOpenPush(self):
        if not gameglobal.rds.configData.get('enableGuildRobber', False):
            return
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_OPEN)

    def clickActivityOpenPush(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_OPEN)
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_ROBBER_ACTIVITY_PUSH_OPEN_HINT, '')
        yesBtnText = gameStrings.GUILD_ROBBER_ACTIVITY_PUSH_YES_BTN_LABEL
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.gotoGuildSpace, yesBtnText=yesBtnText)

    def addActivityEndPush(self):
        if not gameglobal.rds.configData.get('enableGuildRobber', False):
            return
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_END)

    def clickActivityEndPush(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_END)
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_ROBBER_ACTIVITY_PUSH_END_HINT, '')
        yesBtnText = gameStrings.GUILD_ROBBER_ACTIVITY_PUSH_YES_BTN_LABEL
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.gotoGuildSpace, yesBtnText=yesBtnText)

    def gotoGuildSpace(self):
        p = BigWorld.player()
        if p.guildMemberSkills.has_key(uiConst.GUILD_SKILL_DZG):
            canUse = logicInfo.isUseableGuildMemberSkill(uiConst.GUILD_SKILL_DZG)
            canUseReset = p.canResetCD(uiConst.GUILD_SKILL_DZG)
            if not canUse and not canUseReset:
                seekId = GCD.data.get('guildRobberSeekId', ())
                msg = uiUtils.getTextFromGMD(GMDD.data.SKILL_DZG_CANNOT_USE_TO_GUILD, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(uiUtils.findPosById, seekId))
            else:
                gameglobal.rds.ui.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG)
        else:
            seekId = GCD.data.get('guildRobberSeekId', ())
            uiUtils.findPosById(seekId)
