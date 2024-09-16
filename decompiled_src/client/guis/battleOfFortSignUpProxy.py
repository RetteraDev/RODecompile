#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleOfFortSignUpProxy.o
import BigWorld
import uiConst
import gametypes
import gameglobal
import math
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from asObject import ASUtils
from guis.asObject import ASObject
from callbackHelper import Functor
from data import battle_field_mode_data as BFMD
from cdata import game_msg_def_data as GMDD

class BattleOfFortSignUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleOfFortSignUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.battleId = 0
        self.battleMode = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_BATTLE_OF_FORT_SIGN_UP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BATTLE_OF_FORT_SIGN_UP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_OF_FORT_SIGN_UP)

    def reset(self):
        self.battleId = 0
        self.battleMode = 0

    def show(self, battleId = 0):
        p = BigWorld.player()
        self.battleId = battleId
        self.battleMode = self.battleData.get('mode', 0)
        if not self.battleId or not self.battleMode:
            return
        if self.battleMode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            if not gameglobal.rds.configData.get('enableNewFlagBF', False):
                return
        elif self.battleMode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
            if not p.isCanJoinTimingPUBG():
                return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_OF_FORT_SIGN_UP)

    @property
    def battleData(self):
        return BFMD.data.get(self.battleId, {})

    def initUI(self):
        battleData = self.battleData
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.titleName.text = battleData.get('name', '')
        ASUtils.setHitTestDisable(self.widget.titleName, True)
        self.showApplyCommanderCheckBox()
        self.showGuildRankBtn()
        self.showHelpIcon()
        self.widget.signUpTimeText.text = battleData.get('battleOfFortTotalTime', '13:30-21:30')
        self.widget.ruleDesc.htmlText = battleData.get('battleOfFortRuleDesc', '')
        self.widget.tipDesc.htmlText = battleData.get('battleOfFortTipDesc', '')

    def showApplyCommanderCheckBox(self):
        self.widget.checkBox.visible = False
        self.widget.checkBox.selected = False
        if self.battleMode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            self.widget.checkBox.visible = True
            self.widget.checkBox.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox, False, 0, True)

    def showGuildRankBtn(self):
        self.widget.guildRankBtn.visible = False
        if self.battleMode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            self.widget.guildRankBtn.visible = True
            self.widget.guildRankBtn.addEventListener(events.BUTTON_CLICK, self.handleGuildRankBtnClick, False, 0, True)

    def showHelpIcon(self):
        helpKey = self.battleData.get('timingBattleSignUpHelpKey', 0)
        self.widget.helpIcon.visible = False
        if helpKey:
            self.widget.helpIcon.visible = True
            self.widget.helpIcon.helpKey = helpKey

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        startBattleTimeParts = self.battleData.get('startBattleTimeParts', ['14:00-14.30',
         '14:30-15:00',
         '21:00-21:30',
         '21:30-22:00'])
        self.widget.partTimeMc.gotoAndStop('part%d' % len(startBattleTimeParts))
        for actId in xrange(1, 5):
            timeBtn = self.widget.partTimeMc.getChildByName('timeBtn%d' % actId)
            timeBtn.visible = actId <= len(startBattleTimeParts)

        for actId in xrange(1, len(startBattleTimeParts) + 1):
            timeText = self.widget.partTimeMc.getChildByName('timeText%d' % actId)
            timeBtn = self.widget.partTimeMc.getChildByName('timeBtn%d' % actId)
            timeBtn.removeEventListener(events.BUTTON_CLICK, self.handleTimeBtnClick)
            timeText.text = startBattleTimeParts[actId - 1]
            stage = 0
            if self.battleId in p.newFlagBattleFieldStage and actId in p.newFlagBattleFieldStage[self.battleId]:
                stage = p.newFlagBattleFieldStage[self.battleId][actId]
            if stage == gametypes.NEW_FLAG_BF_STAGE_NOT_OPEN:
                timeBtn.label = gameStrings.BATTLE_NEW_FLAG_BF_STAGE_DESC.get(stage, '')
                timeBtn.enabled = False
            elif stage == gametypes.NEW_FLAG_BF_STAGE_OPEN:
                timeBtn.label = gameStrings.BATTLE_NEW_FLAG_BF_STAGE_DESC.get(stage, '')
                timeBtn.enabled = True
            status = 0
            if self.battleId in p.newFlagBattleFieldStatus and actId in p.newFlagBattleFieldStatus[self.battleId]:
                status = p.newFlagBattleFieldStatus[self.battleId][actId]
            if status >= gametypes.NEW_FLAG_BF_STATE_CONFIRMED_APPLY:
                timeBtn.label = gameStrings.BATTLE_NEW_FLAG_BF_STATE_APPLYED
                timeBtn.enabled = True
            if stage == gametypes.NEW_FLAG_BF_STAGE_START:
                timeBtn.label = gameStrings.BATTLE_NEW_FLAG_BF_STAGE_DESC.get(stage, '')
                timeBtn.enabled = False
            elif stage == gametypes.NEW_FLAG_BF_STAGE_CLOSE:
                timeBtn.label = gameStrings.BATTLE_NEW_FLAG_BF_STAGE_DESC.get(stage, '')
                timeBtn.enabled = False
            timeBtn.actId = actId
            timeBtn.timeText = startBattleTimeParts[actId - 1]
            timeBtn.addEventListener(events.BUTTON_CLICK, self.handleTimeBtnClick, False, 0, True)

        self.updateCombatReward()

    def handleGuildRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_GUILD_NEW_FLAG)

    def handleSelectCheckBox(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget

    def handleTimeBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        p = BigWorld.player()
        if p.isInTeam() or p.isInGroup():
            if len(p.members.keys()) > self.battleData.get('timingBattleMemberLimitCount', 5):
                p.showGameMsg(self.battleData.get('timingBattleMemberLimitCountMsgId', 0), ())
                return
        actId = target.actId
        if target.label == gameStrings.BATTLE_NEW_FLAG_BF_STATE_APPLYED:
            self.showCancleJoinMsgTip(target)
        elif target.label == gameStrings.BATTLE_NEW_FLAG_BF_APPLY_DESC:
            if self.checkCanApplyBattleField():
                if self.battleMode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
                    p.cell.applyTimingPUBGBattleField(self.battleId, actId, False)
                else:
                    isSelected = self.widget.checkBox.selected
                    p.cell.applyNewFlagBattleField(self.battleId, actId, isSelected)

    def checkCanApplyBattleField(self):
        p = BigWorld.player()
        if self.battleId not in p.newFlagBattleFieldStatus:
            return True
        for actId, actStatus in p.newFlagBattleFieldStatus[self.battleId].iteritems():
            if actStatus == gametypes.NEW_FLAG_BF_STATE_CONFIRMING_APPLY:
                p.showGameMsg(self.battleData.get('timingBattleOtherApplyConfirming', 0), (actId,))
                return False

        return True

    def showCancleJoinMsgTip(self, targetBtnMc):
        p = BigWorld.player()
        actId = targetBtnMc.actId
        if self.battleMode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
            cancelJoinCB = Functor(p.cell.cancelJoinTimingPUBG, self.battleId, actId)
        else:
            cancelJoinCB = Functor(p.cell.cancelJoinNewFlag, self.battleId, actId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(self.battleData.get('timingBattleCancelJoinMsg', '%s%s') % (str(targetBtnMc.actId), str(targetBtnMc.timeText)), yesBtnText=gameStrings.COMMON_BTN_YES, yesCallback=cancelJoinCB, noBtnText=gameStrings.COMMON_BTN_NO, noCallback=None, canEsc=False)

    def updateCombatReward(self):
        p = BigWorld.player()
        myScore = p.newFlagZhanxunDaily.get(self.battleId, 0)
        self.widget.myCombatScore.text = '%d' % myScore
        self.widget.myIcon.bonusType = 'newFlagGongxian'
        battleExtraRewards = self.battleData.get('battleExtraRewards', [(0, 150), (0, 250), (0, 350)])
        valueList = []
        for i, values in enumerate(battleExtraRewards):
            slot = self.widget.getChildByName('slot%d' % i)
            combatScore = self.widget.getChildByName('combatScore%d' % i)
            iconType = self.widget.getChildByName('icon%d' % i)
            itemInfo = uiUtils.getGfxItemById(values[0])
            slot.dragable = False
            slot.setItemSlotData(itemInfo)
            combatScore.text = values[1]
            iconType.bonusType = 'newFlagGongxian'
            valueList.append(values[1])

        for i in xrange(len(valueList)):
            arrowState = 'dislight'
            if myScore >= valueList[i]:
                if i != 0:
                    arrowState = 'light'
            elif i > 0 and myScore > valueList[i - 1]:
                arrowState = 'half'
            if i != 0:
                progress = self.widget.getChildByName('progress%d' % i)
                if progress:
                    progress.gotoAndStop(arrowState)
